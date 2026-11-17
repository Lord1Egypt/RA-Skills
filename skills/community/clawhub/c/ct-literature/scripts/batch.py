#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-literature 批量检索入口。

调用通用引擎 batch_lib.run_batch；本文件只声明本技能的 ADAPTER（字段→CLI flag
映射）。引擎完全通用，差异仅在此字典——兄弟技能（ct-safety / ct-registry）
各自提供一份等结构的 batch.py 即可复用同一引擎。

规格格式与字段表见 references/batch_spec.md。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch_lib

ADAPTER = {
    "script": "ct_literature.py",
    "default_skill": "ct-literature",
    "supported_skills": ["ct-literature"],   # v1 仅单技能；跨技能待 v2
    "primary_field": "topic",                # 行列表中"|"前的文本落位到此字段
    "fields": {
        # ---- 检索主体 ----
        "topic":            {"flag": "topic", "kind": "value", "required": True},
        "review_type":      {"flag": "review-type", "kind": "value"},
        "year_from":        {"flag": "year-from", "kind": "value"},
        "year_to":          {"flag": "year-to", "kind": "value"},
        "max":              {"flag": "max", "kind": "value"},
        "sources":          {"flag": "sources", "kind": "value"},
        "depth":            {"flag": "depth", "kind": "value"},
        "keywords":         {"flag": "keywords", "kind": "value"},
        "verify":           {"flag": "verify", "kind": "value"},
        "only_type":        {"flag": "only-type", "kind": "value"},
        # ---- 日期窗口（route B）----
        "date_from":        {"flag": "date-from", "kind": "value"},
        "date_to":          {"flag": "date-to", "kind": "value"},
        "recent_months":    {"flag": "recent-months", "kind": "value"},
        # ---- 结构化概念（可重复）----
        "concepts":         {"flag": "concept", "kind": "append"},
        # ---- 布尔开关 ----
        "safety":                 {"flag": "safety", "kind": "flag_true"},
        "cochrane":               {"flag": "cochrane", "kind": "flag_true"},
        "snowball":               {"flag": "snowball", "kind": "flag_true"},
        "with_arxiv":             {"flag": "with-arxiv", "kind": "flag_true"},
        "with_semantic_scholar":  {"flag": "with-semantic-scholar", "kind": "flag_true"},
        "include_reviews":        {"flag": "include-reviews", "kind": "flag_booloptional"},
        "with_europepmc":         {"flag": "with-europepmc", "kind": "flag_booloptional"},
        "with_biorxiv":           {"flag": "with-biorxiv", "kind": "flag_booloptional"},
        "with_medrxiv":           {"flag": "with-medrxiv", "kind": "flag_booloptional"},
        "with_guidelines":        {"flag": "with-guidelines", "kind": "flag_booloptional"},
        # 2026-11-08 能力对齐：v1.7.0 PubMed 独立车道 / v1.7.3 DOI 审计 / doc-type 反向甄别
        "with_pubmed":            {"flag": "with-pubmed", "kind": "flag_true"},
        "pubmed_fallback":        {"flag": "pubmed-fallback", "kind": "flag_booloptional"},
        "verify_dois":            {"flag": "verify-dois", "kind": "flag_true"},
        "original_only":          {"flag": "original-only", "kind": "flag_true"},
        "online":                 {"flag": "online", "kind": "flag_true"},
        "offline":                {"flag": "offline", "kind": "flag_true"},
        "local":                  {"flag": "local", "kind": "flag_true"},
    },
    "required": ["topic"],
    # 配额闸门：OpenAlex 免 key 100/天（since 2026-02-13）
    "quota": {
        "api": "OpenAlex",
        "free_daily": 100,
        "per_entry_estimate": 1,
        "warn_at": 90,
    },
    # pack 模式配置（--pack，2026-10-20）：一次 Coze 调用打包多个 entry。
    # - coze_sources：走 Coze 端的源（复刻 dispatch 的 Coze 路由）；
    #   semantic_scholar 恒本地（2026-09-06 决策：私人 key 零传递）不进包；
    #   openalex 仅本机无 key 时进包（有 key 走本地 keyed pool，由 --from-pack
    #   子进程按原路由执行——见 batch_lib._pack_sources_for）。
    # - 契约详见 references/batch_search_contract.md。
    "pack": {
        "mode": "batch_search",
        "coze_sources": ["openalex", "europepmc", "biorxiv", "medrxiv", "arxiv"],
        "default_size": 8,
        # entry 未显式 max= 时，pack 查询的每源上限——与 ct_literature.py
        # --max 默认值（50）对齐，保证 pack 与非 pack 路径结果量一致。
        "default_max": 50,
    },
}


def main():
    args = batch_lib.build_arg_parser().parse_args()
    engine_script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.exit(batch_lib.run_batch(args.spec_file, ADAPTER, engine_script_dir, args))


if __name__ == "__main__":
    main()
