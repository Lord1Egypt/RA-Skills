#!/usr/bin/env python3
"""
Apify Actor 执行引擎
功能：试跑验证 + 全量执行 + 自动分批 + 轮询等待
"""

import json
import sys
import os
import argparse
import time
import math
import requests

# 默认参数
DEFAULT_POLL_INTERVAL = 5       # 轮询间隔（秒）
DEFAULT_TIMEOUT = 600           # 单批超时（秒）
DEFAULT_BATCH_SIZE = 50         # 默认分批大小
BATCH_PAUSE = 3                 # 批次间歇（秒）
PROBE_TIMEOUT = 120             # 试跑超时（秒）

API_BASE = "https://api.apify.com/v2"


def load_token(config_path, token_name="default"):
    """从 config.json 加载 Token"""
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        tokens = config.get("tokens", {})
        token = tokens.get(token_name) or tokens.get("default")
        if token:
            return token
    # fallback to env
    return os.environ.get("APIFY_TOKEN", "")


def start_run(actor_id, run_input, token):
    """启动 Actor Run"""
    url = f"{API_BASE}/acts/{actor_id.replace('/', '~')}/runs"
    resp = requests.post(
        url,
        json=run_input,
        headers={"Content-Type": "application/json"},
        params={"token": token},
    )
    resp.raise_for_status()
    data = resp.json().get("data", {})
    return data.get("id"), data.get("defaultDatasetId")


def poll_run(run_id, token, timeout=DEFAULT_TIMEOUT, interval=DEFAULT_POLL_INTERVAL):
    """轮询等待 Run 完成"""
    url = f"{API_BASE}/actor-runs/{run_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, params={"token": token})
        resp.raise_for_status()
        status = resp.json().get("data", {}).get("status", "UNKNOWN")
        elapsed = int(time.time() - start)
        print(f"  ⏳ [{elapsed}s] {status}", file=sys.stderr)
        if status == "SUCCEEDED":
            return "SUCCEEDED"
        if status in ("FAILED", "ABORTED", "TIMED-OUT"):
            return status
        time.sleep(interval)
    return "TIMEOUT"


def abort_run(run_id, token):
    """中止 Run"""
    url = f"{API_BASE}/actor-runs/{run_id}/abort"
    try:
        requests.post(url, params={"token": token})
    except Exception:
        pass


def get_dataset(dataset_id, token):
    """获取 Dataset 结果"""
    url = f"{API_BASE}/datasets/{dataset_id}/items"
    resp = requests.get(url, params={"token": token})
    resp.raise_for_status()
    return resp.json()


def probe(actor_id, run_input, token):
    """
    小批量试跑验证
    返回 (success: bool, message: str)
    """
    print(f"🔍 试跑验证: {actor_id}", file=sys.stderr)
    try:
        run_id, dataset_id = start_run(actor_id, run_input, token)
    except requests.HTTPError as e:
        return False, f"启动失败: {e.response.status_code} {e.response.text[:200]}"

    status = poll_run(run_id, token, timeout=PROBE_TIMEOUT)
    if status != "SUCCEEDED":
        abort_run(run_id, token)
        return False, f"运行状态: {status}"

    items = get_dataset(dataset_id, token)
    if not items:
        return False, "运行成功但返回数据为空"

    print(f"  ✅ 试跑通过: {len(items)} 条数据", file=sys.stderr)
    return True, f"试跑成功，返回 {len(items)} 条数据"


def run_batch(actor_id, run_input, token, timeout=DEFAULT_TIMEOUT):
    """执行单批"""
    run_id, dataset_id = start_run(actor_id, run_input, token)
    status = poll_run(run_id, token, timeout=timeout)
    if status != "SUCCEEDED":
        return [], status
    items = get_dataset(dataset_id, token)
    return items, status


def split_input_for_batches(run_input, list_key, batch_size):
    """
    将 run_input 中的列表字段分批
    list_key: run_input 中的列表字段名（如 directUrls, hashtags, startUrls）
    """
    items = run_input.get(list_key, [])
    if not items or len(items) <= batch_size:
        return [run_input]

    batches = []
    for i in range(0, len(items), batch_size):
        batch_input = dict(run_input)
        batch_input[list_key] = items[i:i + batch_size]
        batches.append(batch_input)
    return batches


def main():
    parser = argparse.ArgumentParser(description="Apify Actor 执行引擎")
    parser.add_argument("actor_id", help="Actor ID (如 apify/instagram-scraper)")
    parser.add_argument("--input", required=True, help="run_input JSON 字符串或文件路径")
    parser.add_argument("--config", default=None, help="config.json 路径")
    parser.add_argument("--token-name", default="default", help="Token 名称")
    parser.add_argument("--token", default=None, help="直接传 Token（优先级最高）")
    parser.add_argument("--output", default=None, help="输出 JSON 文件路径")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="单批超时秒数")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="分批大小")
    parser.add_argument("--list-key", default=None, help="run_input 中需要分批的列表字段名")
    parser.add_argument("--probe", action="store_true", help="先试跑验证")
    parser.add_argument("--probe-input", default=None, help="试跑用的 input（默认用 --input 的前 2 条）")
    parser.add_argument("--probe-only", action="store_true", help="仅试跑，不执行全量")

    args = parser.parse_args()

    # 加载 Token
    token = args.token or load_token(args.config, args.token_name)
    if not token:
        print("❌ 未找到 Token，请通过 --token、--config 或环境变量 APIFY_TOKEN 提供", file=sys.stderr)
        sys.exit(1)

    # 解析 run_input
    if os.path.isfile(args.input):
        with open(args.input, "r") as f:
            run_input = json.load(f)
    else:
        run_input = json.loads(args.input)

    # 试跑
    if args.probe or args.probe_only:
        if args.probe_input:
            if os.path.isfile(args.probe_input):
                with open(args.probe_input, "r") as f:
                    probe_input = json.load(f)
            else:
                probe_input = json.loads(args.probe_input)
        elif args.list_key and args.list_key in run_input:
            # 自动取前 2 条做试跑
            probe_input = dict(run_input)
            probe_input[args.list_key] = run_input[args.list_key][:2]
        else:
            probe_input = run_input

        success, msg = probe(args.actor_id, probe_input, token)
        if args.probe_only:
            result = {"status": "ok" if success else "failed", "message": msg, "actor_id": args.actor_id}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0 if success else 1)
        if not success:
            print(json.dumps({"status": "probe_failed", "message": msg, "actor_id": args.actor_id}, ensure_ascii=False, indent=2))
            sys.exit(1)

    # 分批执行
    if args.list_key:
        batches = split_input_for_batches(run_input, args.list_key, args.batch_size)
    else:
        batches = [run_input]

    all_items = []
    total_batches = len(batches)
    for i, batch_input in enumerate(batches, 1):
        if total_batches > 1:
            batch_count = len(batch_input.get(args.list_key, []))  if args.list_key else "all"
            print(f"\n📦 批次 {i}/{total_batches}（{batch_count} 条）", file=sys.stderr)

        try:
            items, status = run_batch(args.actor_id, batch_input, token, args.timeout)
        except requests.HTTPError as e:
            print(f"  ❌ 批次 {i} 失败: {e.response.status_code}", file=sys.stderr)
            continue

        if status == "SUCCEEDED":
            all_items.extend(items)
            print(f"  ✅ 批次 {i} 完成: {len(items)} 条", file=sys.stderr)
        else:
            print(f"  ❌ 批次 {i} 状态: {status}", file=sys.stderr)

        if i < total_batches:
            time.sleep(BATCH_PAUSE)

    # 输出结果
    result = {
        "status": "ok",
        "actor_id": args.actor_id,
        "total_items": len(all_items),
        "total_batches": total_batches,
        "items": all_items,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n📁 结果已保存: {args.output}（{len(all_items)} 条）", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
