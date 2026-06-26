"""LAS-AI PDF 解析 Skill（las_pdf_parse_doubao）

封装 LAS 异步算子调用流程：submit -> poll -> check-and-notify。

所有过程日志输出到 stderr，stdout 只输出结构化结果（task_id / markdown / JSON）。

API Key / 环境变量加载优先级：
1) --env-file 参数指定的文件（强制覆盖已有环境变量）
2) skill 目录下的 env.sh（不覆盖已有环境变量）
3) 当前工作目录的 env.sh（不覆盖已有环境变量）
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests

from tos_utils import handle_url_input


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

DEFAULT_REGION = "cn-beijing"
REGION_TO_DOMAIN = {
    "cn-beijing": "operator.las.cn-beijing.volces.com",
    "cn-shanghai": "operator.las.cn-shanghai.volces.com",
}

OPERATOR_ID = "las_pdf_parse_doubao"
OPERATOR_VERSION = "v1"

PARSE_MODE_ALIASES = {
    "normal": "normal",
    "detail": "detail",
    "fast": "normal",
    "标准": "normal",
    "简单": "normal",
    "详细": "detail",
    "精细": "detail",
}

# env.sh 解析正则
_ENV_LINE_RE = re.compile(
    r"""^\s*(?:export\s+)?(\w+)\s*=\s*(?:"([^"]*)"|'([^']*)'|(\S+))\s*$"""
)

# 预估耗时（秒）
_ETA_MAP = {
    "remote_url": (10, 60),
    "tos_path": (10, 60),
    "local_pdf": (15, 90),
    "local_image": (20, 60),
    "local_image_long": (40, 120),
}


# ---------------------------------------------------------------------------
# 日志工具
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    """过程日志统一输出到 stderr，保持 stdout 干净给 Agent 解析。"""
    print(msg, file=sys.stderr)


def _err(msg: str) -> None:
    """错误信息输出到 stderr。"""
    print(f"✗ {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# env.sh 自动加载
# ---------------------------------------------------------------------------

def _get_script_dir() -> Path:
    """获取 skill.py 所在目录。"""
    return Path(__file__).resolve().parent


def _load_env_file(env_file: Path) -> Dict[str, str]:
    """从 env.sh 解析所有环境变量，返回 {key: value} 字典。"""
    if not env_file.exists():
        return {}

    result = {}
    content = env_file.read_text(encoding="utf-8", errors="ignore")
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _ENV_LINE_RE.match(line)
        if m:
            key = m.group(1)
            value = m.group(2) or m.group(3) or m.group(4) or ""
            if value:
                result[key] = value
    return result


def _auto_load_env(cli_env_file: Optional[str] = None) -> None:
    """自动查找并加载 env.sh，将变量注入 os.environ。

    覆盖策略：
    - --env-file 显式指定的文件：**强制覆盖**已有环境变量（用户明确意图优先）
    - 自动发现的 env.sh（skill 目录 / cwd）：不覆盖已有环境变量

    查找优先级：
    1. --env-file 参数指定的文件（强制覆盖）
    2. skill 目录（scripts/ 的父目录）下的 env.sh（不覆盖）
    3. 当前工作目录的 env.sh（不覆盖）
    """
    # 1) 显式指定的 env-file → 强制覆盖
    if cli_env_file:
        p = Path(cli_env_file).resolve()
        if p.exists():
            envs = _load_env_file(p)
            if envs:
                loaded_keys = []
                overwritten_keys = []
                for k, v in envs.items():
                    if k in os.environ and os.environ[k] != v:
                        overwritten_keys.append(k)
                    os.environ[k] = v
                    loaded_keys.append(k)
                parts = []
                if loaded_keys:
                    parts.append(f"已从 {p} 加载环境变量: {', '.join(loaded_keys)}")
                if overwritten_keys:
                    parts.append(f"(覆盖已有: {', '.join(overwritten_keys)})")
                if parts:
                    _log(" ".join(parts))
                return
        else:
            _log(f"警告: 指定的 env 文件不存在: {cli_env_file}")

    # 2) 自动发现 → 不覆盖已有
    skill_dir = _get_script_dir().parent
    auto_paths = [skill_dir / "env.sh", Path.cwd() / "env.sh"]

    for env_path in auto_paths:
        if env_path.exists():
            envs = _load_env_file(env_path)
            if envs:
                loaded_keys = []
                for k, v in envs.items():
                    if k not in os.environ:
                        os.environ[k] = v
                        loaded_keys.append(k)
                if loaded_keys:
                    _log(f"已从 {env_path} 加载环境变量: {', '.join(loaded_keys)}")
                return

    _log("未找到 env.sh 文件，使用已有环境变量")


# ---------------------------------------------------------------------------
# IP 与 URL 校验
# ---------------------------------------------------------------------------

def _is_private_ip(ip_str: str) -> bool:
    """使用标准库判断是否为私有/保留 IP。"""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_reserved or ip.is_loopback
    except ValueError:
        return False


def _validate_url(url: str) -> str:
    import socket

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https", "tos"):
        raise ValueError(f"不支持的 URL 协议: {parsed.scheme}，仅支持 http/https/tos")
    if not parsed.netloc:
        raise ValueError(f"无效的 URL: {url}")
    if parsed.scheme in ("http", "https"):
        hostname = parsed.hostname
        if not hostname:
            raise ValueError(f"无效的 URL hostname: {url}")
        try:
            ip = socket.gethostbyname(hostname)
            if _is_private_ip(ip):
                raise ValueError(f"禁止访问内网地址: {hostname} ({ip})")
        except socket.gaierror as e:
            raise ValueError(f"无法解析域名: {hostname}") from e
    return url


# ---------------------------------------------------------------------------
# API Key
# ---------------------------------------------------------------------------

def get_api_key() -> str:
    key_name = "LAS_API_KEY"
    api_key = os.environ.get(key_name)
    if api_key:
        return api_key
    raise ValueError(f"无法找到 {key_name}：请设置环境变量或提供 env.sh 文件")


def _headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_api_key()}",
    }


# ---------------------------------------------------------------------------
# Region 与 Endpoint
# ---------------------------------------------------------------------------

def resolve_region(cli_region: Optional[str] = None) -> str:
    """统一 resolve region，保证返回非 None 的有效值。"""
    if cli_region:
        return cli_region
    return (
        os.environ.get("LAS_REGION")
        or os.environ.get("REGION")
        or os.environ.get("region")
        or DEFAULT_REGION
    )


def get_api_base(*, cli_api_base: Optional[str] = None, region: str = DEFAULT_REGION) -> str:
    if cli_api_base:
        return cli_api_base.rstrip("/")
    env_api_base = os.environ.get("LAS_API_BASE")
    if env_api_base:
        return env_api_base.rstrip("/")
    domain = REGION_TO_DOMAIN.get(region)
    if not domain:
        raise ValueError(f"未知 region: {region}；请使用 --api-base 显式指定")
    return f"https://{domain}/api/v1"


def get_endpoints(*, cli_api_base: Optional[str] = None, region: str = DEFAULT_REGION) -> Tuple[str, str]:
    api_base = get_api_base(cli_api_base=cli_api_base, region=region)
    return f"{api_base}/submit", f"{api_base}/poll"


# ---------------------------------------------------------------------------
# 错误处理
# ---------------------------------------------------------------------------

def _extract_error_meta(resp_json: Any) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    if not isinstance(resp_json, dict):
        return None, None, None
    meta = resp_json.get("metadata")
    if not isinstance(meta, dict):
        return None, None, None
    return meta.get("business_code"), meta.get("error_msg"), meta.get("request_id")


def _print_http_error(e: Exception) -> None:
    if isinstance(e, requests.HTTPError) and getattr(e, "response", None) is not None:
        r = e.response
        try:
            j = r.json()
            bc, em, rid = _extract_error_meta(j)
            _err(f"HTTP {r.status_code} {r.reason}")
            if bc or em or rid:
                _err(f"business_code: {bc}, error_msg: {em}, request_id: {rid}")
            else:
                _err(json.dumps(j, ensure_ascii=False)[:2000])
            return
        except Exception:
            pass
        _err(f"HTTP {r.status_code} {r.reason}")
        try:
            _err((r.text or "")[:2000])
        except Exception:
            _err("(无法读取响应内容)")
        return
    _err(f"请求失败: {e}")


# ---------------------------------------------------------------------------
# HTTP 重试
# ---------------------------------------------------------------------------

def _is_retryable_http_status(code: int) -> bool:
    return code in (408, 425, 429, 500, 502, 503, 504)


def _is_retryable_business_code(resp_json: Any) -> bool:
    if not isinstance(resp_json, dict):
        return False
    meta = resp_json.get("metadata")
    if not isinstance(meta, dict):
        return False
    bc = meta.get("business_code")
    return str(bc) in {"2002", "2003"} if bc is not None else False


def _post_json_with_retry(
    *,
    url: str,
    payload: Dict[str, Any],
    timeout_s: int,
    max_attempts: int = 3,
    backoff_s: float = 1.0,
) -> Dict[str, Any]:
    last_err: Optional[Exception] = None
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.post(url, headers=_headers(), json=payload, timeout=timeout_s)
            if not r.ok:
                if _is_retryable_http_status(r.status_code) and attempt < max_attempts:
                    time.sleep(backoff_s * (2 ** (attempt - 1)))
                    continue
                raise requests.HTTPError("request failed", response=r)

            j: Any = r.json()
            if not isinstance(j, dict):
                raise ValueError("返回不是 JSON object")

            if _is_retryable_business_code(j) and attempt < max_attempts:
                time.sleep(backoff_s * (2 ** (attempt - 1)))
                continue
            return j
        except Exception as e:
            last_err = e
            if attempt < max_attempts:
                time.sleep(backoff_s * (2 ** (attempt - 1)))
                continue
            raise
    raise RuntimeError(f"请求失败: {last_err}")


# ---------------------------------------------------------------------------
# 核心 API
# ---------------------------------------------------------------------------

def _normalize_parse_mode(v: Optional[str]) -> Optional[str]:
    if v is None:
        return None
    v = v.strip()
    return PARSE_MODE_ALIASES.get(v, v) if v else None


def submit_task(
    *,
    api_base: Optional[str],
    region: str,
    url: str,
    parse_mode: Optional[str] = None,
    start_page: int = 1,
    num_pages: Optional[int] = None,
    timeout_s: int = 60,
    dry_run: bool = False,
) -> Dict[str, Any]:
    if not url:
        raise ValueError("url 不能为空")
    _validate_url(url)

    submit_url, _ = get_endpoints(cli_api_base=api_base, region=region)
    data: Dict[str, Any] = {"url": url, "start_page": start_page}

    pm = _normalize_parse_mode(parse_mode)
    if pm:
        data["parse_mode"] = pm
    if num_pages is not None:
        data["num_pages"] = num_pages

    payload = {
        "operator_id": OPERATOR_ID,
        "operator_version": OPERATOR_VERSION,
        "data": data,
    }

    if dry_run:
        _log(json.dumps(payload, ensure_ascii=False, indent=2))
        return {"metadata": {"task_id": "DRY_RUN"}, "data": {}}

    return _post_json_with_retry(url=submit_url, payload=payload, timeout_s=timeout_s)


def poll_task(
    *,
    api_base: Optional[str],
    region: str,
    task_id: str,
    timeout_s: int = 60,
) -> Dict[str, Any]:
    if not task_id:
        raise ValueError("task_id 不能为空")
    _, poll_url = get_endpoints(cli_api_base=api_base, region=region)
    payload = {
        "operator_id": OPERATOR_ID,
        "operator_version": OPERATOR_VERSION,
        "task_id": task_id,
    }
    return _post_json_with_retry(url=poll_url, payload=payload, timeout_s=timeout_s)


def _get_markdown(res: Dict[str, Any]) -> str:
    data = res.get("data")
    if not isinstance(data, dict):
        return ""
    md = data.get("markdown")
    return md if isinstance(md, str) else ""


def _get_task_status(res: Dict[str, Any]) -> Optional[str]:
    meta = res.get("metadata") if isinstance(res, dict) else None
    return (meta if isinstance(meta, dict) else {}).get("task_status")


def _write_text(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# 预估耗时
# ---------------------------------------------------------------------------

def _estimate_eta(meta: dict, parse_mode: Optional[str] = None) -> str:
    """根据输入类型和处理信息返回预估耗时字符串。"""
    input_type = meta.get("input_type", "remote_url")
    is_long = meta.get("is_long_image", False)
    pages = meta.get("pages", 1)

    if input_type == "local_image" and is_long:
        key = "local_image_long"
    else:
        key = input_type

    lo, hi = _ETA_MAP.get(key, (10, 60))

    # detail 模式耗时更长
    if parse_mode == "detail":
        lo = int(lo * 1.5)
        hi = int(hi * 2)

    # 多页时增加耗时
    if pages > 4:
        factor = 1 + (pages - 4) * 0.1
        lo = int(lo * factor)
        hi = int(hi * factor)

    if lo >= 60 or hi >= 60:
        lo_str = f"{lo // 60}分{lo % 60}秒" if lo >= 60 else f"{lo}秒"
        hi_str = f"{hi // 60}分{hi % 60}秒" if hi >= 60 else f"{hi}秒"
    else:
        lo_str = f"{lo}秒"
        hi_str = f"{hi}秒"

    detail = []
    if input_type in ("local_image", "local_pdf") and pages > 1:
        detail.append(f"{pages}页")
    elif input_type == "local_image":
        detail.append(f"{pages}页")
    
    if input_type == "local_image" and is_long:
        detail.append("长图")
    if parse_mode == "detail":
        detail.append("高精度模式")

    suffix = f" ({', '.join(detail)})" if detail else ""
    return f"{lo_str}~{hi_str}{suffix}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="skill.py", description="LAS-AI PDF 解析")
    p.add_argument("--env-file", help="指定 env.sh 路径（自动加载环境变量）")
    sp = p.add_subparsers(dest="cmd")

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--region", choices=sorted(REGION_TO_DOMAIN.keys()))
    parent.add_argument("--api-base")

    sp.add_parser("info", parents=[parent], help="打印 endpoint")

    # submit
    p_submit = sp.add_parser("submit", parents=[parent], help="提交任务")
    p_submit.add_argument("--url", required=True, help="PDF URL 或本地文件路径")
    p_submit.add_argument("--parse-mode", default="normal", help="解析模式：normal / detail")
    p_submit.add_argument("--start-page", type=int, default=1)
    p_submit.add_argument("--num-pages", type=int)
    p_submit.add_argument("--dry-run", action="store_true")
    p_submit.add_argument("--tos-bucket")
    p_submit.add_argument("--tos-prefix")
    p_submit.add_argument("--no-use-llm", action="store_false", dest="use_llm", default=True)

    # check-and-notify (供定时任务后台调用)
    p_check = sp.add_parser("check-and-notify", parents=[parent],
                            help="后台轮询：检查任务状态，成功则保存结果，处理中则提示重试")
    p_check.add_argument("--task-id", required=True)
    p_check.add_argument("--output", help="结果保存目录（默认 /tmp/las_parse_{task_id}）")
    p_check.add_argument("--retry-count", type=int, default=0, help="当前已重试次数（仅向后兼容，推荐使用 --poll）")
    p_check.add_argument("--max-retries", type=int, default=30, help="最大重试次数")
    p_check.add_argument("--poll", action="store_true", help="启用内部轮询循环：脚本自行 sleep + 重试，直到成功/失败/超时，一次调用完成全部等待")
    p_check.add_argument("--poll-interval", type=int, help="轮询间隔秒数（仅 --poll 模式，若未指定则使用智能动态退避策略）")
    p_check.add_argument("--tos-bucket", help="TOS bucket（提供则归档到 TOS）")
    p_check.add_argument("--tos-prefix", default="las_pdf_parse", help="TOS 归档路径前缀")

    return p


def main(argv: list[str]) -> None:
    # 兼容：直接传 URL 时当作 submit
    known_cmds = {"info", "submit", "check-and-notify"}
    if argv and argv[0] not in known_cmds and not argv[0].startswith("-"):
        argv = ["submit", "--url", argv[0]] + argv[1:]

    parser = build_parser()
    if not argv:
        parser.print_help()
        return

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return

    # P0 修复：自动加载 env.sh
    _auto_load_env(getattr(args, "env_file", None))

    # P0 修复：统一 resolve region，后续所有调用都用确定值
    region = resolve_region(getattr(args, "region", None))

    # ----- info -----
    if args.cmd == "info":
        submit_url, poll_url = get_endpoints(cli_api_base=args.api_base, region=region)
        _log(f"operator_id: {OPERATOR_ID}")
        _log(f"operator_version: {OPERATOR_VERSION}")
        _log(f"region: {region}")
        _log(f"api_base: {get_api_base(cli_api_base=args.api_base, region=region)}")
        _log(f"submit: {submit_url}")
        _log(f"poll: {poll_url}")
        return

    # ----- submit -----
    if args.cmd == "submit":
        try:
            use_llm = getattr(args, "use_llm", False)
            final_url, input_meta = handle_url_input(
                args.url,
                region=region,
                tos_bucket=getattr(args, "tos_bucket", None),
                tos_prefix=getattr(args, "tos_prefix", None),
                use_llm=use_llm,
                llm_api_key=get_api_key() if use_llm else None,
            )
            res = submit_task(
                api_base=args.api_base,
                region=region,
                url=final_url,
                parse_mode=args.parse_mode,
                start_page=args.start_page,
                num_pages=args.num_pages,
                dry_run=args.dry_run,
            )
            meta = res.get("metadata") if isinstance(res, dict) else None
            meta = meta if isinstance(meta, dict) else {}
            task_id = meta.get("task_id")
            if not task_id:
                _err(json.dumps(res, ensure_ascii=False, indent=2)[:2000])
                raise ValueError("submit 返回缺少 metadata.task_id")

            # P2: 计算预估耗时
            eta = _estimate_eta(input_meta, args.parse_mode)

            # stdout 只输出结构化结果（一行 JSON），Agent 可靠解析
            result = {
                "task_id": task_id,
                "eta": eta,
                "input_type": input_meta.get("input_type", "unknown"),
            }
            if "pages" in input_meta:
                result["pages"] = input_meta["pages"]
            if input_meta.get("is_long_image"):
                result["is_long_image"] = True

            # 附带 tos_bucket 以便 Agent 转发给 check-and-notify
            _tos_bucket = getattr(args, "tos_bucket", None) or os.environ.get("TOS_BUCKET")
            if _tos_bucket:
                result["tos_bucket"] = _tos_bucket
            # 记录源文件 TOS 路径（便于追溯：结果 → 源文件）
            if final_url.startswith("tos://"):
                result["source_tos_url"] = final_url
            _tos_prefix = getattr(args, "tos_prefix", None)
            if _tos_prefix:
                result["tos_prefix"] = _tos_prefix

            print(json.dumps(result, ensure_ascii=False))
            return
        except Exception as e:
            _print_http_error(e)
            sys.exit(1)

    # ----- check-and-notify -----
    if args.cmd == "check-and-notify":
        _task_id = args.task_id
        _output_dir = args.output or f"/tmp/las_parse_{_task_id}"
        _tos_bucket = getattr(args, "tos_bucket", None)
        _tos_prefix = getattr(args, "tos_prefix", "las_pdf_parse")
        _max_retries = args.max_retries

        def _do_check_once(task_id, output_dir, tos_bucket, tos_prefix, region_val, api_base, retry_count, max_retries):
            """执行一次状态检查，返回 (exit_code, json_output)"""
            res = poll_task(api_base=api_base, region=region_val, task_id=task_id)
            status = _get_task_status(res)

            if status == "COMPLETED":
                md = _get_markdown(res)
                if md:
                    from save_utils import save_parse_result
                    summary = save_parse_result(
                        res,
                        output_dir=output_dir,
                        task_id=task_id,
                        tos_bucket=tos_bucket,
                        tos_prefix=tos_prefix,
                        region=region_val,
                    )
                    has_download_url = bool(summary.get("download_url"))
                    output = {
                        "status": "COMPLETED",
                        "task_id": task_id,
                        "has_download_url": has_download_url,
                    }
                    output.update(summary)
                    if has_download_url:
                        dl_url = summary["download_url"]
                        expires = summary.get("download_url_expires_hours", 24)
                        output["download_link_markdown"] = f"[点击下载ZIP（{expires}小时有效）]({dl_url})"
                        try:
                            os.makedirs(output_dir, exist_ok=True)
                            url_file = os.path.join(output_dir, "download_url.txt")
                            with open(url_file, "w") as f:
                                f.write(dl_url)
                        except Exception:
                            pass
                    else:
                        reasons = []
                        if not tos_bucket:
                            reasons.append("未配置 TOS bucket")
                        if summary.get("tos_error"):
                            reasons.append(f"TOS 归档失败: {summary['tos_error']}")
                        if summary.get("presign_error"):
                            reasons.append(f"预签名生成失败: {summary['presign_error']}")
                        output["download_url_missing_reasons"] = reasons or ["未知原因"]
                    return 0, output
                else:
                    return 0, {"status": "COMPLETED", "task_id": task_id, "has_download_url": False, "output_dir": output_dir, "markdown_size": 0, "preview": "(内容为空)", "download_url_missing_reasons": ["解析结果为空"]}

            elif status in ("FAILED", "TIMEOUT"):
                bc, em, rid = _extract_error_meta(res)
                return 1, {"status": status, "business_code": bc, "error_msg": em, "request_id": rid}

            else:
                if retry_count >= max_retries:
                    return 3, {"status": "TIMEOUT_POLL", "message": f"已轮询 {retry_count} 次仍未完成，请手动查询", "task_id": task_id}
                else:
                    return 2, {"status": "PROCESSING", "retry_count": retry_count, "next_retry": retry_count + 1, "task_id": task_id, "message": f"任务仍在处理中 (已轮询 {retry_count + 1}/{max_retries} 次)"}

        if getattr(args, "poll", False):
            # --poll 模式：脚本内部循环 sleep + 重试，一次调用完成全部等待
            for attempt in range(_max_retries):
                try:
                    code, result = _do_check_once(_task_id, _output_dir, _tos_bucket, _tos_prefix, region, args.api_base, attempt, _max_retries)
                except Exception as e:
                    _print_http_error(e)
                    sys.exit(1)
                if code != 2:
                    print(json.dumps(result, ensure_ascii=False))
                    sys.exit(code)
                
                # 智能退避策略：前2次 10s，随后3次 20s，之后 30s
                if args.poll_interval:
                    interval = args.poll_interval
                else:
                    if attempt < 2: interval = 10
                    elif attempt < 5: interval = 20
                    else: interval = 30
                
                # 仍在处理中，输出进度到 stderr 后 sleep
                print(f"[poll] 第 {attempt + 1}/{_max_retries} 次查询，仍在处理中，{interval}s 后重试...", file=sys.stderr)
                time.sleep(interval)
            
            # 循环结束仍未完成
            print(json.dumps({"status": "TIMEOUT_POLL", "message": f"已轮询 {_max_retries} 次仍未完成，请手动查询", "task_id": _task_id}, ensure_ascii=False))
            sys.exit(3)
        else:
            # 传统模式（向后兼容）：单次检查，由调用方控制重试
            try:
                code, result = _do_check_once(_task_id, _output_dir, _tos_bucket, _tos_prefix, region, args.api_base, args.retry_count, _max_retries)
                print(json.dumps(result, ensure_ascii=False))
                sys.exit(code)
            except Exception as e:
                _print_http_error(e)
                sys.exit(1)

    parser.print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
