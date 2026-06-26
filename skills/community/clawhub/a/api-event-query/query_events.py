#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件查询脚本

调用 ai-open-gateway 的 POST /api/event/query 接口，
支持自然语言查询设备事件，返回 AI 摘要和事件列表。

输出格式：JSON（供 agent 解析后格式化展示给用户）。
脚本只负责调用接口和裁剪数据，展示逻辑由 agent 根据 SKILL.md 规则完成。

配置来源（统一规则）：
  - 持久化：~/.openclaw/.env （OpenClaw 客户端的"设置 API Key"会自动写入此文件）
  - 临时覆盖：仅 API_KEY 支持命令行 --api-key，覆盖 .env 中的同名配置
  - 不再读取任何 AI_GATEWAY_* 环境变量

读取项：
  - AI_GATEWAY_API_KEY      —— 必填
  - AI_GATEWAY_HOST         —— 选填，缺省 https://ai-open.icloseli.com
  - AI_GATEWAY_VERIFY_SSL   —— 选填，true/false（默认 true，仅开发环境可关）

依赖：需要安装第三方包 httpx。
"""

import argparse
import json
import sys
from pathlib import Path

# 强制 stdout/stderr 使用 UTF-8，避免在 Windows cmd（cp936/GBK）等
# 非 UTF-8 终端下，输出的中文 JSON 被宿主 codepage 错误解码成乱码。
# 现象：返回值原本是合法 UTF-8（如 ai_scene 中的中文），但终端按 GBK 切片
# 读取后会显示成 IPA / 西里尔字符 + 大量空格。
# 仅当 stdout/stderr 支持 reconfigure（Python 3.7+ TextIO）时执行。
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

try:
    import httpx
except ImportError:
    print("❌ 缺少依赖 httpx，请先安装：python3 -m pip install httpx", file=sys.stderr)
    sys.exit(1)

# 默认网关地址
DEFAULT_API_HOST = "https://ai-open.icloseli.com"

# 最大展示事件数（减少输出量，避免 agent 上下文溢出）
MAX_EVENTS = 3


def load_env_file():
    """
    从 ~/.openclaw/.env 文件加载配置。
    这是 OpenClaw 客户端写入的持久化真值源，由所有 skill 共享。
    """
    env_path = Path.home() / ".openclaw" / ".env"
    if not env_path.exists():
        return {}
    result = {}
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    result[key] = value
    except Exception as e:
        # 读盘失败时按"未配置"继续，不阻断后续 CLI 参数兜底
        print(f"⚠️ 读取配置文件 {env_path} 失败，将按未配置处理: {e}", file=sys.stderr)
    return result


def get_api_key(cli_key, env_vars):
    """
    获取 API_KEY，优先级：
      1. --api-key             命令行临时覆盖（仅本次调用生效）
      2. ~/.openclaw/.env      客户端写入的持久值
    """
    if cli_key:
        return cli_key
    return env_vars.get("AI_GATEWAY_API_KEY")


def get_api_host(env_vars):
    """
    获取网关地址：~/.openclaw/.env 中的 AI_GATEWAY_HOST，未配置则用默认值。
    """
    host = env_vars.get("AI_GATEWAY_HOST")
    return host.rstrip("/") if host else DEFAULT_API_HOST


def get_verify_ssl(env_vars):
    """
    判断是否启用 TLS 证书验证。默认启用。
    仅当 ~/.openclaw/.env 中显式设置 AI_GATEWAY_VERIFY_SSL=false 时禁用（仅开发环境）。
    """
    val = env_vars.get("AI_GATEWAY_VERIFY_SSL", "true").lower()
    return val not in ("false", "0", "no")


def api_post(api_key, api_host, verify_ssl, path, body=None):
    """通用 POST 请求"""
    url = f"{api_host}{path}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = json.dumps(body).encode("utf-8") if body else b""
    try:
        with httpx.Client(verify=verify_ssl, timeout=120.0, headers=headers) as client:
            resp = client.post(url, content=data)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP 错误 {e.response.status_code}: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"❌ 网络错误: {e}", file=sys.stderr)
        print(f"   请确认网关服务 {api_host} 是否已启动", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询设备事件")
    parser.add_argument("--api-key", help="API Key 临时覆盖；持久化请写到 ~/.openclaw/.env")
    parser.add_argument("--device-ids", required=True, help="设备 ID 列表，逗号分隔")
    parser.add_argument("--start-date", required=True, help="开始日期，格式 yyyy-MM-dd")
    parser.add_argument("--end-date", required=True, help="结束日期，格式 yyyy-MM-dd")
    parser.add_argument("--query", required=True, help="自然语言查询，如「今天有没有人来过」")
    parser.add_argument("--locale", default="zh_CN", help="语言区域，默认 zh_CN")
    args = parser.parse_args()

    # 1. 单次读取持久化配置，注入所有 getter（避免脚本运行期 .env 被覆写导致来源不一致）
    env_vars = load_env_file()
    api_key = get_api_key(args.api_key, env_vars)
    if not api_key:
        print("❌ 未找到 AI_GATEWAY_API_KEY，请通过以下任一方式配置：", file=sys.stderr)
        print("   1. 在 ~/.openclaw/.env 中添加：AI_GATEWAY_API_KEY=your_key", file=sys.stderr)
        print("      （OpenClaw 客户端的\"设置 API Key\"会自动写入此文件）", file=sys.stderr)
        print("   2. 命令行临时覆盖：--api-key your_key", file=sys.stderr)
        print("      （仅本次调用生效，会覆盖 ~/.openclaw/.env 中的同名配置）", file=sys.stderr)
        sys.exit(1)

    # 2. 获取网关地址和 TLS 配置
    api_host = get_api_host(env_vars)
    verify_ssl = get_verify_ssl(env_vars)

    # 2.5 自动修正 device_id 大小写（XXXXS_ → xxxxS_）
    raw_ids = [d.strip() for d in args.device_ids.split(",") if d.strip()]
    device_ids = []
    for did in raw_ids:
        if did.upper().startswith("XXXXS_"):
            fixed = "xxxxS_" + did[6:]
            print(f"⚠️ 已自动修正 device_id 大小写: {did} → {fixed}", file=sys.stderr)
            device_ids.append(fixed)
        else:
            device_ids.append(did)

    # 3. 调用事件查询接口
    result = api_post(api_key, api_host, verify_ssl, "/api/event/query", {
        "device_ids": device_ids,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "query": args.query,
        "locale": args.locale,
    })

    # 4. 裁剪事件列表，只保留前 MAX_EVENTS 条（减少 token 量）
    #    在 JSON 中附加 _total_count 字段，供 agent 展示总数
    if result.get("code") == 0 and result.get("data"):
        events = result["data"].get("events", [])
        result["data"]["_total_count"] = len(events)
        result["data"]["events"] = events[:MAX_EVENTS]

    # 5. 输出 JSON（供 agent 解析后格式化展示）
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
