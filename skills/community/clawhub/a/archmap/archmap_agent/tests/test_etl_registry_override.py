"""ETL 注册表项目级覆盖测试（通用生态组件改造）。

验证：
1. <source_root>/archmap/etl_rule_registry.json 存在时被加载并完全驱动产出（自定义规则/分层/关键词/config_reads）；
2. 损坏 JSON（语法错误 / 缺必需字段）抛 RegistryError，带明确路径与原因，不静默回退；
3. 无注册表时走内置逻辑：行为与改造前一致（内置特征目录检测、内置 34 条规则）；
4. 通用特征目录 etl / etl_pipeline / pipelines 命中检测；
5. 无注册表且无特征目录 → detect False（不产出 etl_rules/，行为完全不变）。

运行：cd /Users/xujin/.agents/skills/archmap && python3 -m pytest archmap_agent/tests/test_etl_registry_override.py -q
（本文件全部使用 tmp_path 假项目，不依赖 agent-harness 私有仓库。）
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest

from archmap_agent.baseline_manager import BaselineManager
from archmap_agent.etl_rule_registry import (CONFIG_READS, ETL_DETECT_DIRS, RULES,
                                             RegistryError, clear_registry_cache,
                                             get_registry)
from archmap_agent.etl_profiler import (_load_config_params, detect_etl_project,
                                        generate_etl_reports)


@pytest.fixture(autouse=True)
def _clean_registry_cache():
    clear_registry_cache()
    yield
    clear_registry_cache()


def _mgr(base: Path) -> BaselineManager:
    out = base / "baseline"
    return BaselineManager(str(out), "demo", {"baseline_dir": str(out), "atomic_write": True})


def _custom_registry() -> dict:
    """最小合法自定义注册表：2 条规则、2 个分层、关键词索引、1 条配置契约、config_reads。"""
    return {
        "layers": [["PIPE-EXTRACT", "数据抽取"], ["PIPE-LOAD", "数据加载"]],
        "rules": [
            {"code": "PIPE-EXTRACT-01", "rid": "R1", "name": "CSV 抽取", "layer": "PIPE-EXTRACT",
             "keywords": ["csv", "抽取"], "summary": "按 batch 读取 CSV 并产出记录流",
             "src": [{"file": "my_etl/extract.py", "fn": "extract_csv"}],
             "config": ["conf/pipe.yaml"], "params": {"batch": 100},
             "depends": [], "consumers": ["my_etl/load.py::load_records"],
             "risk_level": "中", "risk_desc": "抽取批量变更影响加载吞吐",
             "history": [], "tests": ["tests/test_extract.py"], "notes": ""},
            {"code": "PIPE-LOAD-01", "rid": "R2", "name": "记录加载", "layer": "PIPE-LOAD",
             "keywords": ["加载", "写入"], "summary": "批量写入目标库",
             "src": [{"file": "my_etl/load.py", "fn": "load_records"}],
             "config": [], "params": {},
             "depends": ["PIPE-EXTRACT-01"], "consumers": [],
             "risk_level": "高", "risk_desc": "写入语义变更破坏幂等",
             "history": [], "tests": [], "notes": ""},
        ],
        "keyword_index": {"csv": ["PIPE-EXTRACT-01"], "加载": ["PIPE-LOAD-01"]},
        "config_contracts": [
            {"kind": "config_field", "rule": "PIPE-EXTRACT-01", "file": "conf/pipe.yaml",
             "key": "pipe.batch", "code_file": "my_etl/extract.py",
             "read": 'cfg["batch"]', "use": 'batch=cfg["batch"]', "note": "抽取批大小"},
        ],
        "etl_detect_dirs": ["my_etl"],
        "config_reads": {"PIPE-EXTRACT-01": ["conf/pipe.yaml", [["batch", "pipe.batch"]]]},
    }


def _fake_project(root: Path, with_registry: bool = True) -> Path:
    """构造假项目：自定义源码 + 配置 + （可选）注册表 JSON。"""
    (root / "my_etl").mkdir(parents=True, exist_ok=True)
    (root / "my_etl" / "extract.py").write_text(
        'def extract_csv(cfg):\n    return read(batch=cfg["batch"])\n', encoding="utf-8")
    (root / "my_etl" / "load.py").write_text(
        "def load_records(records):\n    return len(records)\n", encoding="utf-8")
    (root / "conf").mkdir(exist_ok=True)
    (root / "conf" / "pipe.yaml").write_text("pipe:\n  batch: 500\n", encoding="utf-8")
    if with_registry:
        (root / "archmap").mkdir(exist_ok=True)
        (root / "archmap" / "etl_rule_registry.json").write_text(
            json.dumps(_custom_registry(), ensure_ascii=False, indent=2), encoding="utf-8")
    return root


# ── 1. 自定义注册表加载并驱动产出 ─────────────────────────────────────────

def test_custom_registry_loaded(tmp_path):
    """项目 JSON 被完整加载：分层/规则/关键词/config_reads 全部来自覆盖文件，非内置。"""
    proj = _fake_project(tmp_path)
    reg = get_registry(proj)
    assert reg.is_custom and reg.source.endswith("etl_rule_registry.json")
    assert [r["code"] for r in reg.rules] == ["PIPE-EXTRACT-01", "PIPE-LOAD-01"]
    assert reg.layers == [("PIPE-EXTRACT", "数据抽取"), ("PIPE-LOAD", "数据加载")]
    assert reg.keyword_index == {"csv": ["PIPE-EXTRACT-01"], "加载": ["PIPE-LOAD-01"]}
    assert reg.etl_detect_dirs == ("my_etl",)
    assert reg.config_reads == {"PIPE-EXTRACT-01": ("conf/pipe.yaml", [("batch", "pipe.batch")])}
    assert reg.rules_by_code["PIPE-EXTRACT-01"]["name"] == "CSV 抽取"
    assert reg.downstream_codes("PIPE-EXTRACT-01") == ["PIPE-LOAD-01"]
    assert reg.layer_name("PIPE-LOAD-01") == "数据加载"


def test_custom_registry_triggers_detect_without_feature_dirs(tmp_path):
    """有自定义注册表 → 必触发 ETL 探查，即使项目不存在任何特征目录。"""
    (tmp_path / "archmap").mkdir()
    data = _custom_registry()
    data["etl_detect_dirs"] = []  # 显式空特征目录
    (tmp_path / "archmap" / "etl_rule_registry.json").write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8")
    assert detect_etl_project(tmp_path) is True


def test_custom_registry_drives_deliverables(tmp_path):
    """产出完全由自定义注册表驱动：规则数、详情文档、分层名、关键词索引、配置回填、契约扫描。"""
    proj = _fake_project(tmp_path)
    mgr = _mgr(tmp_path)
    summary = generate_etl_reports(mgr, proj)
    out = Path(mgr.baseline_dir)

    assert summary["rules"] == 2 and summary["registry_source"].endswith("etl_rule_registry.json")
    assert summary["unresolved"] == 0, "假项目函数定位必须解析出真实行号"

    details = sorted(p.stem for p in (out / "etl_rules" / "details").glob("*.md"))
    assert details == ["PIPE-EXTRACT-01", "PIPE-LOAD-01"]

    index_md = (out / "etl_rules" / "ETL规则索引总目录.md").read_text(encoding="utf-8")
    assert "PIPE-EXTRACT · 数据抽取" in index_md and "PIPE-LOAD · 数据加载" in index_md
    assert "ETL-ORCH" not in index_md, "内置私有规则不得混入自定义产出"
    assert "`csv`" in index_md

    # 行号防漂移：extract_csv 在假项目第 1 行
    mapping = json.loads((out / "etl_rules" / "etl_rule_mapping.json").read_text(encoding="utf-8"))
    row = next(r for r in mapping["rows"] if r["code"] == "PIPE-EXTRACT-01")
    assert row["src"][0]["line"] == 1

    # config_reads 驱动运行时回填：yaml 实际值 500 覆盖注册表静态基线 100
    assert summary["config_params_read"] == ["PIPE-EXTRACT-01"]
    assert row["params"]["batch"] == 500

    idx = json.loads((out / "etl_rules" / "etl_rule_search_index.json").read_text(encoding="utf-8"))
    assert idx["keyword_index"] == {"csv": ["PIPE-EXTRACT-01"], "加载": ["PIPE-LOAD-01"]}
    assert idx["rule_total"] == 2
    load_row = next(r for r in idx["rules"] if r["code"] == "PIPE-LOAD-01")
    assert load_row["downstream"] == [] and load_row["depends"] == ["PIPE-EXTRACT-01"]

    # 自定义配置契约被扫描（yaml 键实存 + read/use 命中 → aligned）
    contract = json.loads((out / "etl_rules" / "config_contract_report.json").read_text(encoding="utf-8"))
    assert contract["field_total"] == 1
    assert contract["items"][0]["status"] == "aligned"


def test_custom_config_reads_runtime(tmp_path):
    """config_reads 运行时读取：假项目 yaml 值被读出；注册表未声明的规则不读。"""
    proj = _fake_project(tmp_path)
    params = _load_config_params(proj)
    assert params == {"PIPE-EXTRACT-01": {"batch": 500}}


# ── 2. 损坏 JSON 报明确错误（不静默回退） ────────────────────────────────

def test_corrupted_json_syntax_error(tmp_path):
    (tmp_path / "archmap").mkdir()
    bad = tmp_path / "archmap" / "etl_rule_registry.json"
    bad.write_text("{ not valid json", encoding="utf-8")
    with pytest.raises(RegistryError) as exc:
        get_registry(tmp_path)
    msg = str(exc.value)
    assert str(bad) in msg and "JSON 语法错误" in msg, msg
    # detect 同样抛错（禁止静默回退后误用内置私有规则）
    with pytest.raises(RegistryError):
        detect_etl_project(tmp_path)


def test_missing_required_key_error(tmp_path):
    (tmp_path / "archmap").mkdir()
    bad = tmp_path / "archmap" / "etl_rule_registry.json"
    data = _custom_registry()
    del data["keyword_index"]
    bad.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(RegistryError) as exc:
        get_registry(tmp_path)
    assert '缺少必需字段 "keyword_index"' in str(exc.value)


def test_invalid_rule_field_error(tmp_path):
    (tmp_path / "archmap").mkdir()
    bad = tmp_path / "archmap" / "etl_rule_registry.json"
    data = _custom_registry()
    del data["rules"][0]["risk_level"]
    bad.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(RegistryError) as exc:
        get_registry(tmp_path)
    assert "risk_level" in str(exc.value)


def test_dangling_dependency_error(tmp_path):
    (tmp_path / "archmap").mkdir()
    bad = tmp_path / "archmap" / "etl_rule_registry.json"
    data = _custom_registry()
    data["rules"][1]["depends"] = ["PIPE-NOPE-99"]
    bad.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(RegistryError) as exc:
        get_registry(tmp_path)
    assert "PIPE-NOPE-99" in str(exc.value)


# ── 3. 无注册表走内置逻辑（向后兼容） ────────────────────────────────────

def test_builtin_fallback_without_registry(tmp_path):
    """无注册表 → 内置注册表：34 条规则、内置特征目录、内置 config_reads，is_custom=False。"""
    reg = get_registry(tmp_path)
    assert reg.is_custom is False and reg.source == "builtin"
    assert reg.rules == RULES and len(reg.rules) == 34
    assert reg.etl_detect_dirs == ETL_DETECT_DIRS
    assert reg.config_reads == CONFIG_READS


def test_builtin_detect_dirs_preserved(tmp_path):
    """内置三项私有特征目录保留不删，且新增三项通用目录。"""
    for legacy in ("tongue_diagnosis/etl", "etl_config", "etl/core"):
        assert legacy in ETL_DETECT_DIRS
    for generic in ("etl", "etl_pipeline", "pipelines"):
        assert generic in ETL_DETECT_DIRS


@pytest.mark.parametrize("feature_dir", ["etl", "etl_pipeline", "pipelines"])
def test_generic_feature_dirs_trigger_detect(tmp_path, feature_dir):
    """通用特征目录（无注册表）命中检测。"""
    (tmp_path / feature_dir).mkdir()
    assert detect_etl_project(tmp_path) is True


def test_legacy_feature_dirs_still_trigger_detect(tmp_path):
    """原有三项私有特征目录仍然命中（向后兼容）。"""
    (tmp_path / "tongue_diagnosis" / "etl").mkdir(parents=True)
    assert detect_etl_project(tmp_path) is True


def test_no_registry_no_feature_dirs_unchanged(tmp_path):
    """无注册表且无特征目录 → detect False，行为完全不变（不产出 etl_rules/）。"""
    (tmp_path / "some_unrelated_dir").mkdir()
    assert detect_etl_project(tmp_path) is False
    # 与 cli.py 门控一致：detect False 时不会调用 generate_etl_reports
    assert not (tmp_path / "archmap" / "etl_rules").exists()
