#!/usr/bin/env python3
"""
Agnes AI 图片生成助手 — 封装重试、友好错误提示、自动本地保存。
用法:
  # 文生图
  python agnes_gen.py text2img --prompt "一只可爱的猫咪" --size 1024x1024 --n 1
  python agnes_gen.py text2img --prompt "..." --size 1024x768 --n 2 --key sk-xxx

  # 图生图
  python agnes_gen.py img2img --image ./input.jpg --prompt "赛博朋克风格" --size 1024x1024
  python agnes_gen.py img2img --image https://... --prompt "..." --size 1024x1024
"""

import argparse
import base64
import json
import os
import socket
import sys
import time
import urllib.request
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# ── 配置 ──────────────────────────────────────────────────
# 主端点 + 国内容灾端点：主端点访问不了时自动切换到国内网关
API_ENDPOINTS = [
    "https://apihub.agnes-ai.com/v1",   # 主端点（国际）
    "https://apihub.agnes-ai.cn/v1",    # 国内容灾端点（apihub.agnes-ai.com 访问不了时自动切换）
]
DEFAULT_MODEL_TEXT2IMG = "agnes-image-2.0-flash"
DEFAULT_MODEL_IMG2IMG = "agnes-image-2.0-flash"
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # 指数退避基数（秒）
ENDPOINT_PROBE_TIMEOUT = 8  # 端点连通性探测超时（秒）

# 内置默认 Key（兜底）
DEFAULT_API_KEY = "REDACTED-SECRET"


# ── 友好错误提示映射 ─────────────────────────────────────
def friendly_error(data):
    """
    将 API 返回的技术错误翻译成人话 + 告诉用户下一步怎么做。
    返回 (技术摘要, 友好提示)
    """
    try:
        error_info = data.get("error", {})
        err_type = error_info.get("type", "")
        err_code = error_info.get("code", "")
        err_msg = error_info.get("message", "")
    except Exception:
        err_type = err_code = ""
        err_msg = str(data)

    tech_summary = f"{err_type} / {err_code}: {err_msg}"

    # ── 逐个映射 ──
    mapping = {
        "invalid_api_key": (
            "API Key 无效",
            "你用的 API Key 不正确或已过期，我帮你梳理一下解决步骤：\n"
            "  1) 到 Agnes 官网 https://agnes-ai.com 登录账号\n"
            "  2) 进入控制台，复制新的 API Key（一般以 sk- 开头）\n"
            "  3) 告诉我「用我的 Key: sk-xxxx」或者设置环境变量 AGNES_API_KEY\n"
            "  4) 不想折腾的话，我可以直接用内置 Key 试试。"
        ),
        "authentication_error": (
            "身份验证失败",
            "API Key 没通过验证，可能原因和解决办法：\n"
            "  1) Key 复制时漏了字符 → 再复制一次试试\n"
            "  2) Key 已过期 → 登录 Agnes 控制台重新生成\n"
            "  3) 账户欠费 → 检查 Agnes 账户余额\n"
            "  4) 实在不行我可以先用内置 Key 帮你生成。"
        ),
        "rate_limit_exceeded": (
            "请求太频繁",
            "短时间内调太多次被限速了，别担心，通常等几十秒就好：\n"
            "  1) 等 30-60 秒后自动重试（我已经帮你设置了自动重试）\n"
            "  2) 下次可以把 n 设大一点，一次出多张\n"
            "  3) 如果一直不行，可能是账户配额用完了，去 Agnes 控制台看看。"
        ),
        "model_not_found": (
            "模型不可用",
            "指定的模型名称不存在或暂时下线了，可能原因：\n"
            "  1) 模型名称拼错了 → 文生图用 agnes-image-2.1-flash\n"
            "  2) 可能是服务端临时维护 → 等几分钟再试。"
        ),
        "invalid_image_format": (
            "图片格式不支持",
            "上传的图片格式有问题：\n"
            "  1) 确保是 JPG 或 PNG 格式\n"
            "  2) 如果用的是本地文件，检查文件是否损坏\n"
            "  3) 如果用的是网络图片，确保链接可以直接访问。"
        ),
        "prompt_too_long": (
            "描述内容太长",
            "提示词太长了，Agnes 这边有字数限制：\n"
            "  1) 精简一下描述，只保留关键信息\n"
            "  2) 去掉重复或多余的修饰词\n"
            "  3) 一般中文 200 字以内问题不大。"
        ),
        "network_error": (
            "网络连接失败",
            "连不上 Agnes 服务器：\n"
            "  1) 检查网络是否正常（打开个网页试试）\n"
            "  2) 可能 Agnes 服务端临时抽风 → 等一两分钟自动重试\n"
            "  3) 如果有代理/VPN，试试关掉或换个节点。"
        ),
        "timeout": (
            "请求超时",
            "等太久没返回，可能是网络慢或者生成图片比较花时间：\n"
            "  1) 图片尺寸越大生成越久，试试 512x512 看能不能跑通\n"
            "  2) 如果网络不稳定，换个网络环境试试\n"
            "  3) 我会自动重试，不用手动操作。"
        ),
    }

    # 精确匹配 + 模糊匹配
    if err_code in mapping:
        return mapping[err_code]
    for key in mapping:
        if key in err_type or key in err_code or key in err_msg:
            return mapping[key]

    # 兜底
    return (
        "请求出错",
        f"遇到一个意外错误（{err_code or '未知'}），可以这样做：\n"
        f"  1) 看看上面技术信息能不能看懂\n"
        f"  2) 换个描述/参数再试一次\n"
        f"  3) 还不行的话，可能是 Agnes 那边的问题，稍后再试。"
    )


# ── API Key 解析 ─────────────────────────────────────────
def get_api_key(user_key=None):
    """优先级: 用户提供 > 环境变量 > 内置默认"""
    if user_key:
        return user_key
    env_key = os.environ.get("AGNES_API_KEY", "").strip()
    if env_key:
        return env_key
    return DEFAULT_API_KEY


# ── 图片编码 ─────────────────────────────────────────────
def encode_image(path_or_url):
    """本地路径 → base64 data URI 或保留 URL"""
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    p = Path(path_or_url)
    suffix = p.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


# ── 端点连通性探测 ───────────────────────────────────────
def host_reachable(url, timeout=ENDPOINT_PROBE_TIMEOUT):
    """快速探测端点主机是否可连接（TCP 层），避免主端点不可达时长时间空等。"""
    try:
        p = urlparse(url)
        host = p.hostname
        port = p.port or (443 if p.scheme == "https" else 80)
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False
    return False


# ── 单端点请求（含重试） ───────────────────────────────────
def _api_call_one(url, payload, api_key):
    """对单个端点做重试，返回 (body, tech_err, friendly_err)。"""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
            )
            resp = urllib.request.urlopen(req, timeout=120)
            body = json.loads(resp.read().decode("utf-8"))

            # 检查 API 返回的是否是错误
            if "error" in body:
                tech, friendly = friendly_error(body)
                is_rate_limit = "rate_limit" in body.get("error", {}).get("type", "")
                if is_rate_limit and attempt < MAX_RETRIES:
                    wait = RETRY_BACKOFF ** attempt
                    print(f"[限速] 限速了，{wait} 秒后自动重试（第 {attempt} 次）...")
                    time.sleep(wait)
                    last_error = (tech, friendly)
                    continue
                # 非可重试的错误，直接返回
                return None, tech, friendly

            return body, None, None

        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read().decode("utf-8"))
            except Exception:
                body = {"error": {"message": str(e), "type": f"http_{e.code}"}}
            tech, friendly = friendly_error(body)
            if e.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF ** attempt
                print(f"[重试] 服务器返回 {e.code}，{wait} 秒后自动重试（第 {attempt} 次）...")
                time.sleep(wait)
                last_error = (tech, friendly)
                continue
            return None, tech, friendly

        except (urllib.error.URLError, ConnectionError, TimeoutError, socket.timeout) as e:
            tech, friendly = friendly_error(
                {"error": {"message": str(e), "type": "network_error"}}
            )
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF ** attempt
                print(f"[重试] 网络不通，{wait} 秒后自动重试（第 {attempt} 次）...")
                time.sleep(wait)
                last_error = (tech, friendly)
                continue
            return None, tech, friendly

    return None, last_error[0] if last_error else "未知错误", \
                 last_error[1] if last_error else "未知错误"


# ── 多端点容灾请求 ───────────────────────────────────────
def api_call(endpoints, payload, api_key):
    """
    依次尝试多个端点：主端点（.com）→ 国内容灾端点（.cn）。
    若某端点 TCP 层不可达，立即跳过尝试下一个，避免空等；
    若端点可达但请求失败（限速/5xx），在该端点内重试，耗尽后跳到下一端点。
    返回 (body, tech_err, friendly_err, used_endpoint)。
    """
    last_error = None
    for ep_idx, base in enumerate(endpoints, 1):
        url = f"{base}/images/generations"
        if not host_reachable(url):
            print(f"[容灾] 端点不可达，跳过: {url}")
            if ep_idx < len(endpoints):
                print(f"        → 切换到下一端点重试...")
            continue
        print(f"[端点] 尝试: {url}  ({ep_idx}/{len(endpoints)})")
        body, tech_err, friendly_err = _api_call_one(url, payload, api_key)
        if body is not None:
            return body, None, None, base
        last_error = (tech_err, friendly_err)
        if ep_idx < len(endpoints):
            print(f"[容灾] 该端点请求失败，切换到下一端点重试...")

    if last_error:
        return None, last_error[0], last_error[1], None
    return None, "未知错误", "所有端点均不可达", None


# ── 图片下载 ──────────────────────────────────────────────
def download_images(image_urls, output_dir, prefix="agnes"):
    """下载所有图片到本地，返回本地路径列表。"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, url in enumerate(image_urls):
        suffix = ".png"
        fname = f"{prefix}_{timestamp}_{i+1}{suffix}" if len(image_urls) > 1 \
                else f"{prefix}_{timestamp}{suffix}"
        fpath = output_dir / fname
        try:
            urllib.request.urlretrieve(url, str(fpath))
            size_kb = fpath.stat().st_size / 1024
            print(f"[保存] 已保存: {fpath} ({size_kb:.1f} KB)")
            saved.append(str(fpath))
        except Exception as e:
            print(f"[失败] 下载失败 [{url[:60]}...]: {e}")
            saved.append(None)
    return saved


# ── 主流程 ────────────────────────────────────────────────
def text2img(args):
    """文生图"""
    api_key = get_api_key(args.key)

    print(f"[生成] 正在用 Agnes 生成图片...")
    print(f"   模型: {DEFAULT_MODEL_TEXT2IMG}")
    print(f"   尺寸: {args.size}  |  数量: {args.n}")
    if args.key:
        print(f"   Key:  使用你提供的自定义 Key")
    elif api_key == DEFAULT_API_KEY:
        print(f"   Key:  使用内置默认 Key")
    else:
        print(f"   Key:  环境变量 AGNES_API_KEY")

    body, tech_err, friendly_err, used_base = api_call(
        API_ENDPOINTS,
        {
            "model": DEFAULT_MODEL_TEXT2IMG,
            "prompt": args.prompt,
            "size": args.size,
            "extra_body": {
                "response_format": "url"
            }
        },
        api_key,
    )

    if body is None:
        print(f"\n[失败] 生成失败")
        print(f"──────────────────────────────")
        print(f"[技术] 技术信息: {tech_err}")
        print(f"──────────────────────────────")
        print(f"[提示] {friendly_err}")
        sys.exit(1)

    print(f"[端点] 本次使用: {used_base}")

    # 提取 URL 并立即下载
    urls = [item["url"] for item in body.get("data", [])]
    print(f"\n[成功] 生成成功！（剩余重试: 无需）")

    output_dir = args.output or os.getcwd()
    saved = download_images(urls, output_dir)

    # 输出 JSON 结果（便于调用方解析）
    result = {
        "success": True,
        "model": DEFAULT_MODEL_TEXT2IMG,
        "files": [s for s in saved if s],
        "urls": urls,
    }
    print(f"\n[结果] 结果: {json.dumps(result, ensure_ascii=False)}")
    return result


def img2img(args):
    """图生图"""
    api_key = get_api_key(args.key)

    print(f"[编辑] 正在用 Agnes 编辑图片...")
    print(f"   模型: {DEFAULT_MODEL_IMG2IMG}")
    print(f"   原图: {args.image}")
    print(f"   尺寸: {args.size}  |  数量: {args.n}")

    img_data = encode_image(args.image)

    body, tech_err, friendly_err, used_base = api_call(
        API_ENDPOINTS,
        {
            "model": DEFAULT_MODEL_IMG2IMG,
            "prompt": args.prompt,
            "size": args.size,
            "extra_body": {
                "image": [img_data],
                "response_format": "url"
            }
        },
        api_key,
    )

    if body is None:
        print(f"\n[失败] 生成失败")
        print(f"──────────────────────────────")
        print(f"[技术] 技术信息: {tech_err}")
        print(f"──────────────────────────────")
        print(f"[提示] {friendly_err}")
        sys.exit(1)

    print(f"[端点] 本次使用: {used_base}")

    urls = [item["url"] for item in body.get("data", [])]
    print(f"\n[成功] 生成成功！")

    output_dir = args.output or os.getcwd()
    saved = download_images(urls, output_dir)

    result = {
        "success": True,
        "model": DEFAULT_MODEL_IMG2IMG,
        "files": [s for s in saved if s],
        "urls": urls,
    }
    print(f"\n[结果] 结果: {json.dumps(result, ensure_ascii=False)}")
    return result


# ── CLI ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Agnes AI 图片生成（含自动重试+友好错误提示+自动下载）"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # 文生图
    t2i = sub.add_parser("text2img", help="文生图")
    t2i.add_argument("--prompt", "-p", required=True, help="图片描述（中英文均可）")
    t2i.add_argument("--size", "-s", default="1024x1024",
                     choices=["1024x1024", "1024x768", "768x1024"], help="输出图像尺寸")
    t2i.add_argument("--n", type=int, default=1, help="生成张数（1-4，部分模型可能忽略）")
    t2i.add_argument("--key", help="自定义 API Key（可选）")
    t2i.add_argument("--output", "-o", help="保存目录（默认当前目录）")

    # 图生图
    i2i = sub.add_parser("img2img", help="图生图")
    i2i.add_argument("--image", "-i", required=True, help="原图路径或 URL")
    i2i.add_argument("--prompt", "-p", required=True, help="编辑指令描述")
    i2i.add_argument("--size", "-s", default="1024x1024",
                     choices=["1024x1024", "1024x768", "768x1024"], help="输出图像尺寸")
    i2i.add_argument("--n", type=int, default=1, help="生成张数（1-4，部分模型可能忽略）")
    i2i.add_argument("--key", help="自定义 API Key（可选）")
    i2i.add_argument("--output", "-o", help="保存目录（默认当前目录）")

    args = parser.parse_args()

    if args.cmd == "text2img":
        text2img(args)
    elif args.cmd == "img2img":
        img2img(args)


if __name__ == "__main__":
    main()
