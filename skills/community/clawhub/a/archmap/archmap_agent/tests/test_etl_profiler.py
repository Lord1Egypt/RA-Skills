"""ETL 规则探查模块测试：检测 / 行号解析 / 7 项产出 / 检索索引 / 注册表元数据 / 分级解析。

运行：cd archmap_agent && python3 -m pytest tests/test_etl_profiler.py -q
依赖真实 agent-harness 仓库（AGENT_HARNESS_ROOT 可覆盖，默认 ~/agent-harness）。

防漂移原则（2026-08-12 改造）：禁止硬编码行号 / 规则总数 / 参数具体值 / 契约状态统计。
所有期望从注册表（RULES / CONFIG_CONTRACTS / KEYWORD_INDEX）与被测仓库运行时内容动态派生，
测试目标是「解析与生成逻辑正确」，而非「当前数据快照 == 历史快照」。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
import yaml

from archmap_agent.baseline_manager import BaselineManager
from archmap_agent.etl_rule_registry import (CONFIG_CONTRACTS, KEYWORD_INDEX, LAYERS, RULES,
                                             RULES_BY_CODE, downstream_codes, layer_name, rule_priority)
from archmap_agent.etl_profiler import (_CONFIG_READS, _load_config_params, _resolve_src_line,
                                        _scan_config_contract, detect_etl_project, generate_etl_reports)

HARNESS = Path(os.environ.get("AGENT_HARNESS_ROOT", "/Users/xujin/agent-harness"))
pytestmark = pytest.mark.skipif(not HARNESS.is_dir(), reason=f"agent-harness 未找到: {HARNESS}")

EXPECTED_FILES = [
    "etl_rules/ETL规则索引总目录.md",
    "etl_rules/etl_rule_mapping.json",
    "etl_rules/ETL规则依赖链路图.md",
    "etl_rules/ETL全局参数基线表.md",
    "etl_rules/ETL规则变更风险评估清单.md",
    "etl_rules/etl_rule_search_index.json",
]

VALID_CONTRACT_STATUS = {"aligned", "unused", "stale", "missing_from_yaml", "symbol_missing"}


def _tmp_mgr() -> BaselineManager:
    tmp = tempfile.mkdtemp()
    return BaselineManager(tmp, "demo", {"baseline_dir": tmp, "atomic_write": True})


def _yaml(rel: str) -> dict:
    return yaml.safe_load((HARNESS / rel).read_text(encoding="utf-8")) or {}


def test_detect_etl_project():
    """检测：agent-harness 命中，普通目录未命中。"""
    assert detect_etl_project(HARNESS) is True
    with tempfile.TemporaryDirectory() as root:
        assert detect_etl_project(root) is False


def test_resolve_src_line_current():
    """行号解析：函数名/方法/特征串三类定位均解析出合法行号，且该行内容真实含目标符号。"""
    fn_cases = [
        ("tongue_diagnosis/etl/etl_pipeline.py", "chunk_doc"),
        ("tongue_diagnosis/etl/ingest_router.py", "route_and_ingest"),
        ("tongue_diagnosis/vector_store/lancedb_manager.py", "VectorStore._open_or_create"),
    ]
    for rel, fn in fn_cases:
        line = _resolve_src_line(HARNESS, {"file": rel, "fn": fn})
        assert isinstance(line, int) and line > 0, f"{rel}::{fn} 未解析出行号"
        symbol = fn.rsplit(".", 1)[-1]
        text_line = (HARNESS / rel).read_text(encoding="utf-8").splitlines()[line - 1]
        assert symbol in text_line, f"{rel}:{line} 行内容不含符号 {symbol}（解析错位）"
    pattern_line = _resolve_src_line(HARNESS, {"file": "tongue_diagnosis/etl_config/etl.yaml", "pattern": "etl:"})
    assert isinstance(pattern_line, int) and pattern_line > 0
    assert "etl:" in (HARNESS / "tongue_diagnosis/etl_config/etl.yaml").read_text(encoding="utf-8").splitlines()[pattern_line - 1]
    assert _resolve_src_line(HARNESS, {"file": "not_exist.py", "fn": "x"}) is None


def test_generate_all_seven_deliverables(tmp_path):
    """7 项产出全部落盘：索引/详情 N 份/映射 JSON/链路图/参数表/风险清单/检索索引。"""
    mgr = _tmp_mgr()
    summary = generate_etl_reports(mgr, HARNESS)
    out = Path(mgr.baseline_dir)
    assert summary["rules"] == len(RULES)
    assert summary["unresolved"] == 0, "全部 P0/P1 源码定位必须解析出真实行号"
    for name in EXPECTED_FILES:
        assert (out / name).is_file(), name
    details = sorted((out / "etl_rules" / "details").glob("*.md"))
    assert len(details) == len(RULES)
    assert all(d.stem in RULES_BY_CODE for d in details)
    mapping = json.loads((out / "etl_rules" / "etl_rule_mapping.json").read_text(encoding="utf-8"))
    assert len(mapping["rows"]) == len(RULES)
    # P0/P1 规则行号必须解析出；P2 规则按分级设计允许 line=None（轻量文件存在性检查）
    for row in mapping["rows"]:
        for s in row["src"]:
            if row["priority"] == "P2":
                assert s["line"] is None
            else:
                assert s["line"] is not None, f"{row['code']} ({row['priority']}) 行号未解析"


def test_search_index_and_keywords():
    """检索索引：规则条目与注册表一致，关键词索引与 KEYWORD_INDEX 完全同构。"""
    mgr = _tmp_mgr()
    generate_etl_reports(mgr, HARNESS)
    idx = json.loads((Path(mgr.baseline_dir) / "etl_rules" / "etl_rule_search_index.json").read_text(encoding="utf-8"))
    assert len(idx["rules"]) == len(RULES)
    codes = [r["code"] for r in idx["rules"]]
    assert len(set(codes)) == len(RULES)
    # 关键词命中动态验证：注册表中带「幂等/覆写」关键词的规则必须全部可检出
    expected = {r["code"] for r in RULES if {"幂等", "覆写"} & set(r["keywords"])}
    hit = {r["code"] for r in idx["rules"] if {"幂等", "覆写"} & set(r["keywords"])}
    assert expected and expected <= hit
    assert all(r["detail_doc"].startswith("etl_rules/details/") for r in idx["rules"])
    # 快捷索引与注册表 KEYWORD_INDEX 同构（不逐条硬编码）
    assert idx["keyword_index"] == {kw: codes for kw, codes in sorted(KEYWORD_INDEX.items())}
    for kw, codes in idx["keyword_index"].items():
        assert all(c in RULES_BY_CODE for c in codes), f"关键词 {kw} 索引失效编码"


def test_load_config_params_runtime_values():
    """参数回填：运行时读取的配置值与被测仓库 yaml 实际值动态一致（不硬编码期望值）。"""
    params = _load_config_params(HARNESS)
    assert set(params.keys()) == set(_CONFIG_READS.keys()), "三个配置文件的参数必须全部读到"
    vec, etl, chunk = (_yaml("config/embedding.yaml"),
                       _yaml("tongue_diagnosis/etl_config/etl.yaml"),
                       _yaml("tongue_diagnosis/etl_config/chunking.yaml"))
    assert params["ETL-VEC-01"]["dimension"] == vec["dimension"]
    assert params["ETL-VEC-01"]["model_name"] == vec["model_name"]
    assert params["ETL-ORCH-08"]["workers"] == etl["etl"]["workers"]
    assert params["ETL-ORCH-08"]["reconcile.enabled"] == etl["reconcile"]["enabled"]
    assert params["ETL-CHUNK-02"]["min_chars"] == chunk["chunking"]["min_chars"]
    assert params["ETL-CHUNK-02"]["overlap"] == chunk["chunking"]["overlap_chars"]
    # 配置文件不存在 → 回退注册表静态基线，不报错不编造
    with tempfile.TemporaryDirectory() as root:
        assert _load_config_params(root) == {}


def test_params_backfilled_into_deliverables(tmp_path):
    """回填贯通：⑤参数表与③⑦ JSON 均含运行时配置值（与 yaml 动态比对），而非仅注册表静态值。"""
    mgr = _tmp_mgr()
    generate_etl_reports(mgr, HARNESS)
    out = Path(mgr.baseline_dir)
    vec, etl, chunk = (_yaml("config/embedding.yaml"),
                       _yaml("tongue_diagnosis/etl_config/etl.yaml"),
                       _yaml("tongue_diagnosis/etl_config/chunking.yaml"))
    params_md = (out / "etl_rules" / "ETL全局参数基线表.md").read_text(encoding="utf-8")
    assert f"`{vec['dimension']}`" in params_md
    assert f"`{etl['etl']['workers']}`" in params_md
    assert f"`{chunk['chunking']['min_chars']}`" in params_md
    mapping = json.loads((out / "etl_rules" / "etl_rule_mapping.json").read_text(encoding="utf-8"))
    vec_row = next(r for r in mapping["rows"] if r["code"] == "ETL-VEC-01")
    assert vec_row["params"]["dimension"] == vec["dimension"]
    orch = next(r for r in mapping["rows"] if r["code"] == "ETL-ORCH-08")
    assert orch["params"]["workers"] == etl["etl"]["workers"]
    assert "etl.workers" not in orch["params"], "运行时值应覆盖静态键，不并存双套键名"
    idx = json.loads((out / "etl_rules" / "etl_rule_search_index.json").read_text(encoding="utf-8"))
    chunk_row = next(r for r in idx["rules"] if r["code"] == "ETL-CHUNK-02")
    assert chunk_row["params"]["max_chars"] == chunk["chunking"]["max_chars"]


def test_config_contract_scan_status():
    """契约检测：判定逻辑正确（状态与 read/use/in_yaml 的派生关系成立），不硬编码当前快照。"""
    rows = _scan_config_contract(HARNESS)
    assert len(rows) == len(CONFIG_CONTRACTS)
    for r in rows:
        assert r["status"] in VALID_CONTRACT_STATUS, f"非法状态 {r['status']}"
        if r["kind"] == "code_residual":
            # 符号缺失 → symbol_missing；有消费 → aligned；无消费 → stale
            if r["status"] == "symbol_missing":
                assert r["use_hits"] == 0
            elif r["status"] == "aligned":
                assert r["use_hits"] > 0
            else:
                assert r["status"] == "stale" and r["use_hits"] == 0
        else:
            if r["use_hits"] > 0:
                assert r["status"] == "aligned", f"{r['field']} 有消费却未判 aligned"
            elif r["in_yaml"] is False:
                assert r["status"] == "missing_from_yaml"
            else:
                assert r["status"] == "unused"


def test_config_contract_deliverable(tmp_path):
    """第 8 项产出落盘：对齐报告 md + JSON，统计自洽（各状态计数总和==字段总数），与扫描一致。"""
    mgr = _tmp_mgr()
    summary = generate_etl_reports(mgr, HARNESS)
    out = Path(mgr.baseline_dir)
    assert (out / "etl_rules" / "ETL配置契约对齐报告.md").is_file()
    report = json.loads((out / "etl_rules" / "config_contract_report.json").read_text(encoding="utf-8"))
    assert report["field_total"] == len(CONFIG_CONTRACTS)
    assert sum(report["status_counts"].values()) == report["field_total"], "状态计数必须闭合"
    assert summary["config_contract"] == report["status_counts"], "summary 与 JSON 报告统计必须一致"
    # JSON 与实时扫描结果一致（同一份数据的两个出口）
    live = _scan_config_contract(HARNESS)
    assert {(r["rule"], r["field"], r["status"]) for r in report["items"]} == \
           {(r["rule"], r["field"], r["status"]) for r in live}
    md = (out / "etl_rules" / "ETL配置契约对齐报告.md").read_text(encoding="utf-8")
    assert "aligned（已接线）" in md and "unused（死配置）" in md and "stale（代码残留）" in md
    for r in live:  # 每条契约的 note 必须原样进入 md（动态，不锁定具体文案）
        assert r["note"] in md


def test_registry_meta_consistency():
    """注册表元数据：编码唯一、分层归属合法、依赖引用闭合、keyword 索引有效、priority 合法。"""
    assert len(RULES) > 0, "注册表为空"
    assert len(RULES_BY_CODE) == len(RULES), "编码存在重复"
    layer_codes = [c for c, _ in LAYERS]
    for r in RULES:
        assert r["code"] in RULES_BY_CODE
        assert r["layer"] in layer_codes, r["code"]
        assert rule_priority(r) in {"P0", "P1", "P2"}, f"{r['code']} priority 非法"
        # 显式 priority 字段（如有）必须与 risk_level 推导一致，防止两套口径漂移
        if "priority" in r:
            assert r["priority"] == rule_priority(r)
        for dep in r["depends"]:
            assert dep in RULES_BY_CODE, f"{r['code']} 依赖未注册: {dep}"
        assert layer_name(r["code"]) == dict(LAYERS)[r["layer"]]
    for kw, codes in KEYWORD_INDEX.items():
        assert all(c in RULES_BY_CODE for c in codes), f"关键词 {kw} 索引失效编码"


def test_downstream_closure():
    """依赖方向图：全表反向一致性——对任意规则 r，其 depends 中每条上游的 downstream 必含 r。"""
    for r in RULES:
        for up in r["depends"]:
            assert r["code"] in downstream_codes(up), f"{r['code']} depends {up}，但 {up} 的 downstream 不含 {r['code']}"
    # downstream_codes 输出有序且无重
    for code in RULES_BY_CODE:
        down = downstream_codes(code)
        assert down == sorted(set(down))


def test_priority_derivation_and_depth():
    """P0/P1/P2 分级：risk_level→priority 推导正确；mapping JSON 携带 priority；分级统计闭合。"""
    mgr = _tmp_mgr()
    summary = generate_etl_reports(mgr, HARNESS)
    # 推导映射：高→P0 / 中→P1 / 低→P2
    expect = {"高": "P0", "中": "P1", "低": "P2"}
    for r in RULES:
        assert rule_priority(r) == expect[r["risk_level"]], f"{r['code']} 推导异常"
    # 分级统计与注册表一致
    counts = {"P0": 0, "P1": 0, "P2": 0}
    for r in RULES:
        counts[rule_priority(r)] += 1
    assert summary["priority_counts"] == counts
    assert sum(summary["priority_counts"].values()) == len(RULES)
    # mapping JSON 每行携带 priority 且与推导一致
    mapping = json.loads((Path(mgr.baseline_dir) / "etl_rules" / "etl_rule_mapping.json").read_text(encoding="utf-8"))
    for row in mapping["rows"]:
        assert row["priority"] == rule_priority(RULES_BY_CODE[row["code"]])
    # P2 轻量解析：行号跳过但文件存在性已验证；P0/P1 深度解析行号必须非空
    assert summary["parse_depth"]["full"] == counts["P0"] + counts["P1"]
    assert summary["parse_depth"]["file_check"] == counts["P2"]
