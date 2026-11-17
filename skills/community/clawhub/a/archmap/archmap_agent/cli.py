import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def _module_vector_text(m: dict) -> str:
    """模块向量文本：路径 + API 路由 + 存储 + import 依赖，让语义匹配命中模块内容而非仅目录名。"""
    apis = " ".join(a.get("route", "") for a in m.get("apis", []))
    storages = " ".join(s.get("name", "") for s in m.get("storages", []))
    imports = " ".join(m.get("imports", []))
    return " ".join(x for x in (m.get("module_path", ""), apis, storages, imports) if x)


def _keyword_match_modules(requirement: str, modules: list[dict]) -> set[str]:
    """向量匹配未命中时的关键词回退：按需求关键词与模块语料（路径+API+存储）的匹配度选 Top-K。"""
    req = re.sub(r"[^一-龥a-zA-Z0-9]", " ", requirement).lower()
    raw_tokens = [k for k in req.split() if len(k) >= 2]
    keywords = []
    for token in raw_tokens:
        if re.search(r"[一-龥]", token):
            for i in range(len(token) - 1):
                keywords.append(token[i:i + 2])
        else:
            keywords.append(token)
    expanded = []
    for k in keywords:
        expanded.append(k)
        if k in CN_TO_EN_KEYWORDS:
            expanded.extend(CN_TO_EN_KEYWORDS[k].split())
    if not expanded:
        return set()

    scored = []
    for m in modules:
        corpus = _module_vector_text(m).lower()
        hits = sum(1 for k in expanded if k in corpus)
        if hits > 0:
            scored.append((hits, m["module_id"]))
    scored.sort(reverse=True)
    # 取相关度 > 0 的前 3 个模块，至少保证有反馈
    return set(mid for _, mid in scored[:3])


from .config_loader import ConfigLoader
from .baseline_manager import BaselineManager
from .source_scanner import SourceScanner
from .vector_recognizer import VectorRecognizer
from .worker_agent import WorkerAgent
from .master_agent import MasterAgent
from .mermaid_renderer import MermaidRenderer
from .report_generator import ReportGenerator
from .review_gate import ReviewGate
from .module_detail_analyzer import ModuleDetailAnalyzer, CN_TO_EN_KEYWORDS
from .recall_engine import hashes_fp, expand_recall, recall_validate
from .etl_profiler import detect_etl_project, generate_etl_reports
from .diff_engine import run_diff_impact, write_import_snapshot, write_line_snapshot


def _modules_as_dict(modules: list[dict] | dict[str, dict]) -> dict[str, dict]:
    """兼容 modules 为数组或对象两种历史格式。"""
    if isinstance(modules, dict):
        return modules
    return {m["module_id"]: m for m in modules}


def run_full(config: dict) -> dict:
    cfg_global = config["global_config"]
    cfg_baseline = config["baseline_config"]
    cfg_worker = config["worker_agent_config"]
    cfg_render = config["render_config"]
    cfg_recognizer = config["recognizer_config"]

    cfg_render["project_name"] = cfg_global["project_name"]
    cfg_render["mode"] = "全量基线构建"

    baseline_mgr = BaselineManager(cfg_global["baseline_root"], cfg_global["project_name"], cfg_baseline)
    scanner = SourceScanner()
    modules = scanner.scan(cfg_global["source_root"])

    worker = WorkerAgent(max_input_chars=cfg_global["max_input_chars"])
    parsed = worker.parse_batch(modules)

    master = MasterAgent()
    aggregated = master.aggregate(parsed)

    recognizer = VectorRecognizer(cfg_global.get("embedding_model"))
    vectors = {m["module_id"]: recognizer.encode(_module_vector_text(m)) for m in parsed}

    mermaid = MermaidRenderer().render_all(aggregated)
    violations = [v for m in parsed for v in m.get("violations", [])]
    reports = ReportGenerator(Path(__file__).parent / "templates").generate_full(aggregated, mermaid, violations, cfg_render)

    baseline_mgr.save_baseline(aggregated)
    baseline_mgr.save_vector_cache(vectors)
    # 记录模块内容指纹，供同步模式识别变更
    baseline_mgr.write_json("module_hashes.json", worker.module_hashes(modules))
    write_line_snapshot(cfg_global["source_root"], cfg_global["baseline_root"])  # 行级快照，供 diff 模式比对
    write_import_snapshot(cfg_global["source_root"], cfg_global["baseline_root"])  # 导入图缓存，diff 增量复用
    for name, content in reports.items():
        baseline_mgr.write_text(name, content)

    etl_rules = generate_etl_reports(baseline_mgr, cfg_global["source_root"]) if detect_etl_project(cfg_global["source_root"]) else {}

    return {"status": "ok", "modules": len(parsed), "reports": list(reports.keys()), "violations": len(violations),
            "etl_rules": etl_rules}


def run_incremental(config: dict, requirement_text: str) -> dict:
    cfg_global = config["global_config"]
    cfg_baseline = config["baseline_config"]
    cfg_recognizer = config["recognizer_config"]

    baseline_mgr = BaselineManager(cfg_global["baseline_root"], cfg_global["project_name"], cfg_baseline)
    baseline = baseline_mgr.get_baseline()
    vectors = baseline_mgr.get_vector_cache()
    old_hashes = baseline_mgr.read_json("module_hashes.json")

    scanner = SourceScanner()
    modules = scanner.scan(cfg_global["source_root"])
    worker = WorkerAgent(max_input_chars=cfg_global["max_input_chars"])
    new_hashes = worker.module_hashes(modules)

    current_ids = {m["module_id"] for m in modules}
    baseline_ids = set(_modules_as_dict(baseline.get("modules", {})).keys())
    changed = {m["module_id"] for m in modules if old_hashes.get(m["module_id"]) != new_hashes.get(m["module_id"])} if old_hashes else set()
    removed = baseline_ids - current_ids

    recognizer = VectorRecognizer(cfg_global.get("embedding_model"))
    master = MasterAgent()

    # 1) 先同步源码中已发生变更的模块（复盘机制），避免基线 stale
    if changed or removed:
        sync_modules = [m for m in modules if m["module_id"] in changed]
        parsed_sync = worker.parse_batch(sync_modules)
        baseline = master.merge_incremental(baseline, parsed_sync, changed)
        baseline_modules = _modules_as_dict(baseline.get("modules", {}))
        for mid in removed:
            baseline_modules.pop(mid, None)
            vectors.pop(mid, None)
            new_hashes.pop(mid, None)
        baseline["modules"] = list(baseline_modules.values())
        parsed_sync_by_id = {m["module_id"]: m for m in parsed_sync}
        for m in sync_modules:
            vectors[m["module_id"]] = recognizer.encode(_module_vector_text(parsed_sync_by_id[m["module_id"]]))
        baseline_mgr.save_baseline(baseline)
        baseline_mgr.save_vector_cache(vectors)
        baseline_mgr.write_json("module_hashes.json", new_hashes)

    # 2) 基于最新基线做需求影响面匹配
    baseline_modules = _modules_as_dict(baseline.get("modules", {}))
    match = recognizer.match_modules(requirement_text, vectors)
    affected = set(match["high_confidence"] + match["low_confidence"])
    base_via = "vector"
    if not affected:
        affected = _keyword_match_modules(requirement_text, list(baseline_modules.values()))
        base_via = "keyword"
    # 召回补强：路由供需闭包 + 需求路由关键词硬匹配，不受向量阈值约束
    match_sources = expand_recall(requirement_text, affected, baseline_modules, base_via)
    affected = set(match_sources)

    need_parse = affected - changed
    if need_parse:
        req_modules = [m for m in modules if m["module_id"] in need_parse]
        parsed = worker.parse_batch(req_modules)
        baseline = master.merge_incremental(baseline, parsed, affected)
        parsed_by_id = {m["module_id"]: m for m in parsed}
        for m in req_modules:
            vectors[m["module_id"]] = recognizer.encode(_module_vector_text(parsed_by_id[m["module_id"]]))
        baseline_mgr.save_baseline(baseline)
        baseline_mgr.save_vector_cache(vectors)
        baseline_mgr.write_json("module_hashes.json", new_hashes)

    # 模块内精准定位（方向 B）
    analyzer = ModuleDetailAnalyzer(max_file_chars=cfg_global["max_input_chars"])
    precise_modules = [m for m in modules if m["module_id"] in affected]
    precise = analyzer.analyze_modules(precise_modules, requirement_text)

    # 预测元数据：需求文本 + 命中来源 + 基线指纹，供 sync 召回验证比对
    baseline_mgr.write_json("precise_meta.json", {
        "requirement": requirement_text,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hashes_fp": hashes_fp(baseline_mgr.read_json("module_hashes.json")),
        "match_sources": {k: sorted(v) for k, v in match_sources.items()},
    })

    return {
        "status": "ok",
        "affected_modules": sorted(affected),
        "match_sources": {k: sorted(v) for k, v in match_sources.items()},
        "synced_modules": sorted(changed),
        "removed_modules": sorted(removed),
        "parsed": len(need_parse),
        "precise_analysis": precise,
    }


def run_sync(config: dict, generate_reports: bool = True) -> dict:
    """同步模式：对比当前源码与已有基线，仅重新解析变更模块并合并更新基线。generate_reports=False 时跳过 01~09 全量报告重生成（lite 用）。"""
    cfg_global = config["global_config"]
    cfg_baseline = config["baseline_config"]
    cfg_worker = config["worker_agent_config"]
    cfg_render = config["render_config"]

    cfg_render["project_name"] = cfg_global["project_name"]
    cfg_render["mode"] = "同步更新"

    baseline_mgr = BaselineManager(cfg_global["baseline_root"], cfg_global["project_name"], cfg_baseline)
    baseline = baseline_mgr.get_baseline()
    old_hashes = baseline_mgr.read_json("module_hashes.json")
    old_vectors = baseline_mgr.get_vector_cache()

    scanner = SourceScanner()
    modules = scanner.scan(cfg_global["source_root"])

    worker = WorkerAgent(max_input_chars=cfg_global["max_input_chars"])
    new_hashes = worker.module_hashes(modules)

    current_ids = {m["module_id"] for m in modules}
    baseline_ids = set(_modules_as_dict(baseline.get("modules", {})).keys())

    changed = set()
    for m in modules:
        mid = m["module_id"]
        if mid not in old_hashes or old_hashes.get(mid) != new_hashes.get(mid):
            changed.add(mid)
    removed = baseline_ids - current_ids

    if not changed and not removed:
        etl_rules = generate_etl_reports(baseline_mgr, cfg_global["source_root"]) if detect_etl_project(cfg_global["source_root"]) else {}
        result = {"status": "ok", "changed_modules": [], "removed_modules": sorted(removed), "message": "无变更，无需更新",
                  "etl_rules": etl_rules}
        recall = recall_validate(baseline_mgr, old_hashes, changed, _modules_as_dict(baseline.get("modules", {})))
        if recall:
            result["recall"] = recall
        return result

    changed_modules = [m for m in modules if m["module_id"] in changed]
    parsed = worker.parse_batch(changed_modules)

    master = MasterAgent()
    merged = master.merge_incremental(baseline, parsed, changed)
    # 清理已删除模块
    merged_modules = _modules_as_dict(merged.get("modules", {}))
    for mid in removed:
        merged_modules.pop(mid, None)
        old_vectors.pop(mid, None)
        new_hashes.pop(mid, None)
    merged["modules"] = list(merged_modules.values())

    recognizer = VectorRecognizer(cfg_global.get("embedding_model"))
    parsed_by_id = {m["module_id"]: m for m in parsed}
    for m in changed_modules:
        old_vectors[m["module_id"]] = recognizer.encode(_module_vector_text(parsed_by_id[m["module_id"]]))

    violations = [v for mod in merged.get("modules", []) for v in mod.get("violations", [])]

    baseline_mgr.save_baseline(merged)
    baseline_mgr.save_vector_cache(old_vectors)
    baseline_mgr.write_json("module_hashes.json", new_hashes)
    write_line_snapshot(cfg_global["source_root"], cfg_global["baseline_root"])  # 行级快照随基线刷新
    write_import_snapshot(cfg_global["source_root"], cfg_global["baseline_root"])  # 导入图缓存随基线刷新
    report_names: list[str] = []
    if generate_reports:
        new_ids = {mid for mid in changed if mid not in old_hashes}
        mermaid = MermaidRenderer().render_all(merged, new_modules=new_ids, modified_modules=changed - new_ids, removed_modules=removed)
        reports = ReportGenerator(Path(__file__).parent / "templates").generate_full(merged, mermaid, violations, cfg_render)
        for name, content in reports.items():
            baseline_mgr.write_text(name, content)
        report_names = list(reports.keys())

    # ETL 探查产出刷新（行号随代码变更防漂移）
    etl_rules = generate_etl_reports(baseline_mgr, cfg_global["source_root"]) if detect_etl_project(cfg_global["source_root"]) else {}

    recall = recall_validate(baseline_mgr, old_hashes, changed, _modules_as_dict(merged.get("modules", {})))
    result = {
        "status": "ok",
        "changed_modules": sorted(changed),
        "removed_modules": sorted(removed),
        "parsed": len(parsed),
        "reports": report_names,
        "violations": len(violations),
        "etl_rules": etl_rules,
    }
    if recall:
        result["recall"] = recall
    return result


def run_diff(config: dict, note: str | None = None) -> dict:
    """diff 影响面模式：行级快照比对 + AST 导入图闭包 + 测试选择，产出 diff_impact.json；有变更时追加变更历史。"""
    cfg_global = config["global_config"]
    result = run_diff_impact(cfg_global["source_root"], cfg_global["baseline_root"], note=note)
    result["diff_impact_path"] = str(Path(cfg_global["baseline_root"]) / "diff_impact.json")
    return result


def run_lite(config: dict, note: str | None = None) -> dict:
    """lite 极简增量（日常迭代默认）：无基线自动转 full 初始化；有基线走 diff 变更检测+留痕，
    仅重解析变更模块合并基线，不重生成 01~09 全量报告与架构大图。"""
    cfg_global = config["global_config"]
    baseline_root = Path(cfg_global["baseline_root"])
    if not (baseline_root / "full_index.json").exists():
        result = run_full(config)
        result["routed_to"] = "full（无基线，自动执行完整初始化）"
        return result
    diff = run_diff_impact(cfg_global["source_root"], cfg_global["baseline_root"], note=note)
    if diff.get("status") in ("snapshot_initialized", "snapshot_migrated_v2"):
        return diff
    result = run_sync(config, generate_reports=False)
    result["diff_impact_path"] = str(baseline_root / "diff_impact.json")
    result["diff_stats"] = diff.get("stats")
    result["lite"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description="架构测绘Agent")
    parser.add_argument("--config-root", default="./configs", help="YAML配置目录")
    parser.add_argument("--mode", choices=["full", "incremental", "sync", "lite"], required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--source-root", default="", help="源码根目录（full/sync模式必填）")
    parser.add_argument("--baseline-root", default="./baselines", help="基线根目录")
    parser.add_argument("--requirement", default="", help="增量需求文本（incremental模式必填）")
    parser.add_argument("--review", choices=["approve", "reject"], default=None, help="人工审核决策")
    args = parser.parse_args()

    loader = ConfigLoader(args.config_root)
    config = loader.load_all()
    config["global_config"]["project_name"] = args.project_name
    config["global_config"]["baseline_root"] = args.baseline_root
    if args.source_root:
        config["global_config"]["source_root"] = args.source_root

    if args.mode == "full":
        result = run_full(config)
    elif args.mode == "sync":
        result = run_sync(config)
    elif args.mode == "lite":
        result = run_lite(config)
    else:
        if not args.requirement:
            raise ValueError("incremental模式必须提供 --requirement")
        result = run_incremental(config, args.requirement)

    if args.review:
        gate = ReviewGate()
        review_result = gate.review(args.review, {"project": args.project_name})
        result["review"] = review_result

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
