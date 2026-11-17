#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""create_must_baseline.py - 创建MUST基准人群并轮询量级。凭证自动加载。

⚠️ 必须通过 dmp_api_client.py（鉴权技能）调用DMP API，禁止裸urllib。
⚠️ 组合规则必须通过 rules_helper.build_rules_http() 构建，禁止手写JSON。
⚠️ 支持自动维度分组OR + 父子标签去重（通过tag_hierarchy模块）。

输入格式（JSON文件，二选一）：
  1. 扁平列表（旧格式，向后兼容）：[15705, 15687, 15688, 15564]
     → 自动调用 tag_hierarchy.must_to_or_groups() 做维度分组+父子去重
  2. 已分组的二维列表（推荐）：[[15705], [15687,15688,15689], [34080,34082], [15564]]
     → 每个子列表是同维度OR，跨列表AND
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent))
from dmp_api_client import DmpClient, ensure_ok
from auth import add_auth_args
# 兼容两套服务端口径：优先使用group嵌套结构；如需旧版扁平rule可切换
from rules_helper_v2 import (
    build_grouped_data_http,
    validate_grouped_data_http,
    build_rules_http,
    validate_rules_http,
)
from tag_hierarchy import must_to_or_groups

CREATE_PATH = "/audience/manage/combine/create"
TASK_LIST_PATH = "/audience/manage/taskList"


def load_tag_pool(skill_dir: Path) -> List[Dict]:
    """加载tag_pool.json（用于维度分组和父子去重）。"""
    pool_path = skill_dir / "tag_pool.json"
    if pool_path.exists():
        with open(pool_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def load_must_and_group(path: str, tag_pool: List[Dict],
                        core_kws: List[str]) -> tuple:
    """加载MUST标签并自动做维度分组+父子去重。

    返回: (or_groups, removed_optional, warnings)
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 解析输入
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], list):
            # 已是二维列表（or_groups格式），直接使用
            or_groups = [sorted([int(x) for x in g if x is not None]) for g in data if g]
            return or_groups, [], []
        elif isinstance(data[0], dict):
            # dict列表（含tagId字段）
            must_ids = [int(x["tagId"]) for x in data if x.get("tagId") is not None]
        else:
            # 扁平ID列表（旧格式）→ 自动分组+去重
            must_ids = [int(x) for x in data if x is not None]
    else:
        raise SystemExit("must.json 格式错误：需是非空列表")

    if not must_ids:
        raise SystemExit("must.json 为空或无法解析 tagId")

    # 自动维度分组 + 父子去重
    if tag_pool:
        or_groups, removed, warnings = must_to_or_groups(must_ids, tag_pool, core_kws)
    else:
        # 无tag_pool时降级为每个tag独立AND（旧行为）
        or_groups = [[tid] for tid in must_ids]
        removed = []
        warnings = ["⚠️ tag_pool.json未找到，无法自动维度分组和父子去重，每个标签将独立AND"]
    return or_groups, removed, warnings


def poll_until_done(client, audience_id, timeout_sec=900):
    """轮询直到任务终态（严格按状态码）：
    - 0: 失败 → 返回（status=0，amount无效）
    - 1: 成功 → 返回（status=1，amount有效）
    - 2: 等待中 → 继续轮询
    - 3: 计算中 → 继续轮询
    """
    start = time.time()
    sleep_s = 3
    last = {}
    while True:
        resp = client.post(TASK_LIST_PATH, {"audienceIds": [audience_id]})
        ensure_ok(resp)
        items = resp.get("data") or []
        last = items[0] if items else {}
        status = last.get("audienceStatus")
        # 严格：只有0(失败)和1(成功)是终态
        if status == 1:
            last["_success"] = True
            return last
        if status == 0:
            last["_success"] = False
            last["_error"] = last.get("taskLog", "") or "人群计算失败"
            return last
        # status=2(等待中) 或 status=3(计算中) → 继续轮询
        if time.time() - start > timeout_sec:
            last["timeout"] = True
            last["_success"] = False
            last["_error"] = f"轮询超时（{timeout_sec}s），最后状态: {status}"
            return last
        time.sleep(sleep_s)
        sleep_s = min(int(sleep_s * 1.5), 20)


def main():
    ap = argparse.ArgumentParser()
    add_auth_args(ap)
    ap.add_argument("--must", required=True, help="must.json（扁平列表或二维or_groups）")
    ap.add_argument("--name", required=True, help="人群名称")
    ap.add_argument("--track-type", required=True, choices=["MOBILE", "PC", "OTT"])
    ap.add_argument("--id-types", required=True, nargs="+")
    ap.add_argument("--core-kws", default="美妆个护,护肤,彩妆",
                    help="核心兴趣关键词(逗号分隔)，用于维度分组")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()

    skill_dir = Path(__file__).parent.parent  # 技能根目录（tag_pool.json在根目录）
    tag_pool = load_tag_pool(skill_dir)
    core_kws = [kw.strip() for kw in args.core_kws.split(",") if kw.strip()]

    or_groups, removed, warnings = load_must_and_group(args.must, tag_pool, core_kws)

    if not or_groups:
        raise SystemExit("分组后无有效MUST标签")

    # 打印警告
    for w in warnings:
        print(f"⚠️ {w}", file=sys.stderr)

    # 构建规则（优先使用group嵌套结构，以适配你方示例口径）
    data_rules = build_grouped_data_http(or_groups)
    errors = validate_grouped_data_http(data_rules)
    if errors:
        # 兼容回退：如果group结构校验不通过，再尝试旧版扁平rule结构
        data_rules = build_rules_http(or_groups)
        errors = validate_rules_http(data_rules)
        if errors:
            raise SystemExit(f"规则校验失败: {'; '.join(errors)}")

    client = DmpClient.from_config(ak=args.ak, sk=args.sk, base_url=args.base_url)

    resp = client.post(CREATE_PATH, {
        "name": args.name, "trackType": args.track_type,
        "idTypes": args.id_types, "data": data_rules,
    })
    ensure_ok(resp)
    audience_id = (resp.get("data") or {}).get("audienceId")
    if audience_id is None:
        raise SystemExit("创建成功但未返回 audienceId")

    result = poll_until_done(client, int(audience_id), timeout_sec=args.timeout)

    success = bool(result.get("_success"))
    status = result.get("audienceStatus")
    amount = result.get("audienceAmount") if success else None
    error_msg = result.get("_error", "") if not success else None

    out = {
        "ok": success,
        "audienceId_M": int(audience_id),
        "amount_M": amount,
        "status": status,
        "name": args.name,
        "or_groups": or_groups,
        "removed_to_optional": removed,
        "warnings": warnings,
        "timeout": bool(result.get("timeout", False))
    }
    if error_msg:
        out["error"] = error_msg
    print(json.dumps(out, ensure_ascii=False))

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
