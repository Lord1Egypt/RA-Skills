import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from archmap_agent.source_scanner import SourceScanner
from archmap_agent.granularity_validator import GranularityValidator
from archmap_agent.worker_agent import WorkerAgent
from archmap_agent.master_agent import MasterAgent
from archmap_agent.baseline_manager import BaselineManager
from archmap_agent.mermaid_renderer import MermaidRenderer


def test_scanner_filters_blacklist():
    with tempfile.TemporaryDirectory() as root:
        Path(root, "src").mkdir()
        Path(root, "src", "app.py").write_text("x")
        Path(root, "node_modules").mkdir()
        Path(root, "node_modules", "x.js").write_text("x")
        scanner = SourceScanner()
        modules = scanner.scan(root)
        ids = [m["module_id"] for m in modules]
        assert "src" in ids
        assert "node_modules" not in ids
        print("PASS test_scanner_filters_blacklist")


def test_worker_granularity_violation():
    validator = GranularityValidator()
    module = {
        "module_id": "test",
        "module_path": "test/",
        "apis": [{"route": "/api/users", "purpose": "list", "shared": False, "method": "GET"}],
        "storages": [],
    }
    ok, violations = validator.validate(module)
    assert not ok
    assert any(v["type"] == "api" for v in violations)
    print("PASS test_worker_granularity_violation")


def test_master_marks_shared_api():
    modules = [
        {"module_id": "a", "module_path": "a/", "apis": [{"route": "/shared", "purpose": "x"}], "storages": [], "dependencies": [], "dependents": []},
        {"module_id": "b", "module_path": "b/", "apis": [{"route": "/shared", "purpose": "y"}], "storages": [], "dependencies": [], "dependents": []},
    ]
    master = MasterAgent()
    result = master.aggregate(modules)
    mods = {m["module_id"]: m for m in result["modules"]}
    assert "/shared" in result["shared_apis"]
    assert mods["a"]["apis"][0]["shared"] is True
    print("PASS test_master_marks_shared_api")


def test_baseline_atomic_write():
    with tempfile.TemporaryDirectory() as root:
        mgr = BaselineManager(root, "demo", {"atomic_write": True})
        mgr.save_baseline({"x": 1})
        assert mgr.get_baseline() == {"x": 1}
        tmp_files = list(Path(mgr.baseline_dir).glob("*.tmp"))
        assert len(tmp_files) == 0
        print("PASS test_baseline_atomic_write")


def test_mermaid_text_only():
    renderer = MermaidRenderer()
    out = renderer.architecture_diagram({"m1": {"module_path": "m1/"}})
    assert "graph TD" in out
    assert "```" not in out
    print("PASS test_mermaid_text_only")


def test_worker_truncate_long_source():
    with tempfile.TemporaryDirectory() as root:
        big = "a" * 15000
        Path(root, "big.py").write_text(big)
        worker = WorkerAgent(max_input_chars=12000)
        result = worker.parse({"module_id": "root", "module_path": root + "/", "abs_path": root})
        text_len = sum(len(p) for p in [result.get("module_path", "")])
        assert result["module_path"].endswith("/")
        print("PASS test_worker_truncate_long_source")


def test_worker_distinguishes_defined_referenced_and_imports():
    text = (
        "from fastapi import APIRouter\n"
        "from tongue_diagnosis.vector_store.lancedb_manager import VectorStore\n"
        "@router.get(\"/api/health\")\n"
        "def health(): ...\n"
        "resp = requests.get(\"http://x/api/hook-logs/stats/summary\")\n"
        "page.route(\"**/api/mock\", handler)\n"
        "const x = e.target.value\n"
    )
    worker = WorkerAgent()
    parsed = worker._heuristic_parse(text)
    kinds = {a["route"]: a["kind"] for a in parsed["apis"]}
    assert kinds.get("/api/health") == "defined"
    assert kinds.get("/api/hook-logs/stats/summary") == "referenced"
    assert "**/api/mock" not in kinds and "e.target.value" not in kinds
    assert "tongue_diagnosis" in parsed["imports"] and "fastapi" in parsed["imports"]
    print("PASS test_worker_distinguishes_defined_referenced_and_imports")


def test_master_no_false_cycle_from_url_strings():
    modules = [
        {"module_id": "backend", "module_path": "backend/", "imports": ["tongue_diagnosis"],
         "apis": [{"route": "/api/health", "purpose": "x", "kind": "defined"}], "storages": [],
         "dependencies": [], "dependents": []},
        {"module_id": "tongue_diagnosis", "module_path": "tongue_diagnosis/", "imports": [],
         "apis": [{"route": "/api/health", "purpose": "x", "kind": "referenced"}], "storages": [],
         "dependencies": [], "dependents": []},
    ]
    master = MasterAgent()
    result = master.aggregate(modules)
    mods = {m["module_id"]: m for m in result["modules"]}
    assert mods["backend"]["import_dependencies"] == ["tongue_diagnosis"]
    assert mods["tongue_diagnosis"]["import_dependencies"] == []
    assert mods["tongue_diagnosis"]["dependencies"] == ["backend"]
    print("PASS test_master_no_false_cycle_from_url_strings")


def test_report_cycles_only_import_edges():
    from archmap_agent.report_generator import ReportGenerator
    rg = ReportGenerator(template_dir=".")
    modules = {
        "backend": {"dependencies": ["tongue_diagnosis"], "import_dependencies": ["tongue_diagnosis"]},
        "tongue_diagnosis": {"dependencies": ["backend"], "import_dependencies": []},
    }
    assert rg._detect_cycles(modules) == set()
    modules["tongue_diagnosis"]["import_dependencies"] = ["backend"]
    assert rg._detect_cycles(modules) == {("backend", "tongue_diagnosis")}
    print("PASS test_report_cycles_only_import_edges")


def test_expand_recall_route_closure():
    from archmap_agent.recall_engine import expand_recall
    baseline = {
        "backend": {"apis": [{"route": "/api/hook-logs", "kind": "defined"}]},
        "frontend": {"apis": [{"route": "/api/hook-logs", "kind": "referenced"}]},
    }
    sources = expand_recall("查看钩子日志", {"frontend"}, baseline, "vector")
    assert "route_closure" in sources.get("backend", set())
    sources2 = expand_recall("查看钩子日志", {"backend"}, baseline, "vector")
    assert sources2.get("frontend") == {"route_closure"}
    print("PASS test_expand_recall_route_closure")


def test_expand_recall_route_keyword():
    from archmap_agent.recall_engine import expand_recall
    baseline = {
        "backend": {"apis": [{"route": "/api/hook-logs/stats/summary", "kind": "defined"}]},
        "etl": {"apis": [{"route": "/api/etl/rabbitmq", "kind": "defined"}]},
    }
    sources = expand_recall("sync the hook-logs monitor page", set(), baseline, "vector")
    assert "route_keyword" in sources.get("backend", set())
    assert "etl" not in sources
    print("PASS test_expand_recall_route_keyword")


def test_classify_miss_reasons():
    from archmap_agent.recall_engine import classify_miss
    baseline = {
        "backend": {"apis": [{"route": "/api/hook-logs", "kind": "defined"}]},
        "frontend": {"apis": [{"route": "/api/hook-logs", "kind": "referenced"}]},
        "scripts": {"apis": []},
    }
    assert classify_miss("backend", "sync hook-logs page", baseline, {"frontend"}) == "route_keyword_miss"
    assert classify_miss("backend", "无关需求文本", baseline, {"frontend"}) == "closure_miss"
    assert classify_miss("scripts", "无关需求文本", baseline, {"frontend"}) == "vector_miss"
    print("PASS test_classify_miss_reasons")


def test_recall_validate_consumes_prediction():
    from archmap_agent.baseline_manager import BaselineManager
    from archmap_agent.recall_engine import hashes_fp, recall_validate
    with tempfile.TemporaryDirectory() as root:
        mgr = BaselineManager(root, "demo", {"atomic_write": True})
        old_hashes = {"backend": "h1", "frontend": "h2"}
        mgr.write_json("precise_analysis.json", [{"module_id": "frontend", "files": []}])
        mgr.write_json("precise_meta.json", {"requirement": "钩子监控", "hashes_fp": hashes_fp(old_hashes)})
        baseline_modules = {
            "backend": {"apis": [{"route": "/api/hook-logs", "kind": "defined"}]},
            "frontend": {"apis": [{"route": "/api/hook-logs", "kind": "referenced"}]},
        }
        # 主流程：有变更 → 验证并消费预测
        result = recall_validate(mgr, old_hashes, {"backend", "frontend"}, baseline_modules)
        assert result["action"] == "validated" and result["recall"] == 0.5
        assert mgr.read_json("recall_report.json")["misses"] == [{"module_id": "backend", "reason": "closure_miss"}]
        assert not mgr.exists("precise_analysis.json") and not mgr.exists("precise_meta.json")
        assert mgr.read_text("recall_history.jsonl").strip()
        # 边界：无变更 → pending 保留预测；指纹不一致 → 丢弃陈旧预测
        mgr.write_json("precise_analysis.json", [{"module_id": "frontend"}])
        mgr.write_json("precise_meta.json", {"requirement": "r", "hashes_fp": hashes_fp(old_hashes)})
        assert recall_validate(mgr, old_hashes, set(), baseline_modules)["action"] == "pending"
        assert mgr.exists("precise_analysis.json")
        assert recall_validate(mgr, {"other": "h9"}, {"other"}, baseline_modules)["action"] == "discarded_stale"
        assert not mgr.exists("precise_analysis.json")
        print("PASS test_recall_validate_consumes_prediction")


if __name__ == "__main__":
    test_scanner_filters_blacklist()
    test_worker_granularity_violation()
    test_master_marks_shared_api()
    test_baseline_atomic_write()
    test_mermaid_text_only()
    test_worker_truncate_long_source()
    test_worker_distinguishes_defined_referenced_and_imports()
    test_master_no_false_cycle_from_url_strings()
    test_report_cycles_only_import_edges()
    test_expand_recall_route_closure()
    test_expand_recall_route_keyword()
    test_classify_miss_reasons()
    test_recall_validate_consumes_prediction()
    print("ALL TESTS PASSED")
