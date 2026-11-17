#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dify.AI 知识库只读检索脚本（无第三方依赖，仅标准库）

用法：
  python search.py --query "WebRTC 弱网自适应" --top-k 5
  python search.py --query "云手机 PRD" --json

配置来源：命令行参数 > 环境变量（DIFY_API_BASE / DIFY_API_KEY / DIFY_DATASET_ID）。
只读脚本：仅调用检索接口，不做任何上传/修改操作。

退出码：0 成功；1 API 错误；2 配置错误。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

QUERY_MAX_LEN = 250


def fail(msg, code=2):
    print(f"[错误] {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Dify.AI 知识库只读检索")
    parser.add_argument("--query", required=True, help="检索问题（最长 250 字符）")
    parser.add_argument("--top-k", type=int, default=5, help="返回条数，默认 5")
    parser.add_argument("--score-threshold", type=float, default=None,
                        help="相似度阈值（如 0.5），提供则启用阈值过滤")
    parser.add_argument("--search-method", default="semantic_search",
                        choices=["semantic_search", "full_text_search", "hybrid_search"],
                        help="检索方式，默认 semantic_search")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--api-base", default=os.environ.get("DIFY_API_BASE", "https://api.dify.ai"))
    parser.add_argument("--api-key", default=os.environ.get("DIFY_API_KEY", ""))
    parser.add_argument("--dataset-id", default=os.environ.get("DIFY_DATASET_ID", ""))
    args = parser.parse_args()

    api_base = args.api_base.rstrip("/")
    if not args.api_key:
        fail("缺少 API Key：请设置环境变量 DIFY_API_KEY 或传 --api-key（密钥配置见 workspace/TOOLS.md）")
    if not args.dataset_id:
        fail("缺少 Dataset ID：请设置环境变量 DIFY_DATASET_ID 或传 --dataset-id"
             "（从 Dify 知识库页面 URL 的 /datasets/<id> 部分复制）")

    query = args.query.strip()
    if not query:
        fail("--query 不能为空")
    if len(query) > QUERY_MAX_LEN:
        print(f"[警告] query 超过 {QUERY_MAX_LEN} 字符，已截断", file=sys.stderr)
        query = query[:QUERY_MAX_LEN]

    # retrieval_model 必填字段：reranking_enable / score_threshold_enabled（缺失返回 400 invalid_param）
    retrieval_model = {
        "top_k": args.top_k,
        "search_method": args.search_method,
        "reranking_enable": False,
        "score_threshold_enabled": args.score_threshold is not None,
    }
    if args.score_threshold is not None:
        retrieval_model["score_threshold"] = args.score_threshold

    payload = json.dumps({"query": query, "retrieval_model": retrieval_model}).encode("utf-8")
    url = f"{api_base}/v1/datasets/{args.dataset_id}/retrieve"
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {args.api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        hints = {
            400: "retrieval_model 缺必填字段（reranking_enable / score_threshold_enabled）",
            401: "密钥无效或已被删除：在 Dify 控制台重新生成密钥并更新 TOOLS.md",
            403: "密钥访问范围不含该知识库，或该知识库关闭了「访问 API」开关：由用户在 Dify 控制台检查",
            404: "Dataset ID 不存在或拼写错误：核对知识库 URL 中的 /datasets/<id>",
            429: "触发 Dify Cloud 请求频率限制：稍后退避重试",
        }
        hint = hints.get(e.code, "")
        fail(f"HTTP {e.code} {body[:200]}" + (f"\n       提示：{hint}" if hint else ""), 1)
    except Exception as e:
        fail(f"请求失败：{e}（检查网络与 API 地址 {api_base}）", 1)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    records = data.get("records", [])
    if not records:
        print("（无检索结果）")
        return
    print(f"检索「{query}」命中 {len(records)} 条：\n")
    for i, rec in enumerate(records, 1):
        seg = rec.get("segment") or {}
        doc = (seg.get("document") or {}).get("name", "未知文档")
        score = rec.get("score", 0)
        content = (seg.get("content") or rec.get("content") or "").strip()
        print(f"[{i}] score={score:.4f} | 文档: {doc}")
        print(content[:500] + ("…" if len(content) > 500 else ""))
        print()


if __name__ == "__main__":
    main()
