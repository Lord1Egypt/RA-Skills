#!/usr/bin/env python3
"""probe_model.py — 运行时模型快照核对（ai-data-delivery v0.0.4）

防"改了没生效"：服务加载旧模型/旧 jar、端口被旧实例占用时，
readiness 通过不代表是新实例。本工具直接核对运行时模型与本地权威源是否一致。

用法：
  python probe_model.py --endpoint http://localhost:7100
  python probe_model.py --endpoint http://localhost:7100 --model semantic.yaml

数据源（按序尝试）：
  GET /api/metrics/progress  → {modelVersion, total, structured}
  GET /api/model             → {version, datasets[], metrics[], ...}

退出码：0 = 一致（或未给 --model 仅报告）；1 = 不一致；2 = 端点不可达/返回无法解析。

安全声明：网络访问仅限 --endpoint 指定地址，默认仅本机/内网（端点守卫，远程需 --allow-remote）；无任何其他出站请求。
"""
import argparse
import json
import sys

import yaml

from _contract import guard_endpoint, load
from _network import safe_json, response_error


def get(url, timeout=15, allow_remote=False):
    try:
        result = safe_json(url, timeout=timeout, allow_remote=allow_remote)
        error = response_error(result)
        return (None, error) if error else (result, None)
    except Exception as e:
        return None, str(e)


def local_stats(path):
    m = load(path)
    metrics = m.get("metrics", [])
    return {
        "version": m.get("version"),
        "datasets": len(m.get("datasets", [])),
        "concepts": len(m.get("concepts", [])),
        "relationships": len(m.get("relationships", [])),
        "metrics": len(metrics),
        "structured": sum(1 for x in metrics if x.get("structured")),
    }


def remote_stats(endpoint, allow_remote=False):
    """返回 (stats, source, error)。"""
    base = endpoint.rstrip("/")
    prog, err1 = get(base + "/api/metrics/progress", allow_remote=allow_remote)
    full, err2 = get(base + "/api/model", allow_remote=allow_remote)
    if prog is not None and not any(prog.get(k) is not None for k in ("modelVersion", "total", "structured")):
        prog, err1 = None, "进度响应没有版本或计数字段"
    if full is not None and not (full.get("version") is not None or any(k in full for k in ("datasets", "metrics", "concepts", "relationships"))):
        full, err2 = None, "模型响应没有可核对字段"
    if full is not None and any(k in full and not isinstance(full[k], list) for k in ("datasets", "metrics", "concepts", "relationships")):
        full, err2 = None, "模型集合字段必须是列表"
    if prog is None and full is None:
        return None, None, f"两个端点都不可达：/api/metrics/progress={err1}；/api/model={err2}"
    stats = {}
    if full:
        metrics = full.get("metrics", [])
        stats = {
            "version": full.get("version"),
            "datasets": len(full["datasets"]) if "datasets" in full else None,
            "concepts": len(full["concepts"]) if "concepts" in full else None,
            "relationships": len(full["relationships"]) if "relationships" in full else None,
            "metrics": len(metrics) if "metrics" in full else None,
            "structured": sum(1 for x in metrics
                              if isinstance(x, dict) and x.get("structured")) if "metrics" in full else None,
        }
        source = "/api/model"
    else:
        stats = {"version": prog.get("modelVersion"),
                 "metrics": prog.get("total"),
                 "structured": prog.get("structured")}
        source = "/api/metrics/progress（轻量端点，仅版本与指标计数）"
    return stats, source, None


def main():
    ap = argparse.ArgumentParser(description="运行时模型快照核对")
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--model", default=None, help="本地权威源 semantic.yaml（可选，给则比对）")
    ap.add_argument("--allow-remote", action="store_true",
                    help="允许非本机/内网端点（默认拒绝，防误发业务内容到公网）")
    args = ap.parse_args()
    try:
        guard_endpoint(args.endpoint, args.allow_remote)
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    rstats, source, err = remote_stats(args.endpoint, allow_remote=args.allow_remote)
    if err:
        print(f"错误：{err}", file=sys.stderr)
        return 2

    print(f"运行时模型（{source}）：")
    for k, v in rstats.items():
        if v is not None:
            print(f"  {k:14s} {v}")

    if not args.model:
        print("\n未给 --model，仅报告不比。生产核对请提供本地权威源 semantic.yaml。")
        return 0

    lstats = local_stats(args.model)
    print(f"\n本地权威源（{args.model}）：")
    for k, v in lstats.items():
        print(f"  {k:14s} {v}")

    diffs = []
    for k, lv in lstats.items():
        rv = rstats.get(k)
        if rv is not None and lv != rv:
            diffs.append((k, lv, rv))
    if diffs:
        print("\n✗ 不一致——服务很可能加载了旧模型/旧实例：")
        for k, lv, rv in diffs:
            print(f"  {k:14s} 本地={lv}  运行时={rv}")
        print("处置：rebuild.py 重建（新鲜度校验防旧包）→ 确认端口无旧实例 → 重跑本探针")
        return 1
    print("\n✓ 已返回的模型版本/计数字段与本地一致；未返回字段未验证")
    return 0


if __name__ == "__main__":
    sys.exit(main())
