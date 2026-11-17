"""diff_engine.py — 版本差异影响面引擎（archmap 模式 F）

纯静态分析，零 LLM 调用：行级快照比对（difflib，git 无关）→ 文件级依赖图
（Python AST import + JS/TS import/require 正则解析 + 跨语言路由供需边）
→ 反向传播影响闭包 → 测试选择。行级快照与依赖图缓存仅在 full/sync 基线时刻写入；
diff 模式对未变更文件零重算（行哈希比对 + 依赖图缓存复用），仅变更/新增/缓存缺失
文件重新解析；新增/删除文件属于结构性变更，依赖图全量重解析一次（防边缺失）。
有变更时自动追加 diff_history.jsonl 并重渲染 10_变更历史.md（时间+修改内容留痕）。

v2 升级（2026-08-14）：
1. 变更检测从仅 .py 扩展到 .py/.ts/.tsx/.js/.jsx/.vue/.sql/.yaml/.yml
   （配置/契约变更同样影响行为；.json 刻意排除——状态类 json 噪音大于信号）
2. 依赖边从仅 Python import 扩展为三类：
   a. Python 静态 import（AST）
   b. JS/TS/Vue import/require/dynamic-import（正则 + 相对路径与 @/→src/ 别名解析）
   c. 跨语言路由供需边：FastAPI/Flask/Express 路由定义（供给）× 全文件路由字符串
      字面量（需求，仅命中真实定义的路由才成边，零噪音）——前后端 HTTP 调用关系
      自动入闭包，双向传播
3. 变更符号映射：.py 变更行区间 → AST 定位所属函数/类名（changed_symbols）
4. 备份目录屏蔽：_backups / migration_backup 不参与 diff 扫描
5. 行级快照带 _schema 版本标记，v1 快照自动迁移（重建快照，不产生伪变更洪峰）
"""
import ast
import difflib
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from .source_scanner import DEFAULT_BLACKLIST

SNAPSHOT_NAME = "file_line_hashes.json"
IMPORTS_NAME = "file_imports.json"
ROUTES_NAME = "file_routes.json"
DIFF_OUT_NAME = "diff_impact.json"
HISTORY_NAME = "diff_history.jsonl"
HISTORY_DOC_NAME = "10_变更历史.md"
TEST_DIR_NAMES = {"test", "tests", "spec", "specs"}
_SNAPSHOT_SCHEMA = 2

# diff 模式扫描范围：测试目录参与选择映射；备份/迁移目录屏蔽（防死代码噪音入闭包）
_SCAN_BLACKLIST = (DEFAULT_BLACKLIST - TEST_DIR_NAMES) | {"_backups", "migration_backup"}

# 纳入变更检测的扩展名（.json 刻意排除：状态/锁文件 churn 是噪音）
TRACKED_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".vue", ".sql", ".yaml", ".yml"}
_JS_RESOLVE_EXTS = [".ts", ".tsx", ".js", ".jsx", ".vue", ".json"]

_JS_IMPORT_RE = re.compile(
    r"(?:import|export)\s[^'\"]*?from\s*['\"]([^'\"]+)['\"]"   # import/export ... from 'x'
    r"|require\(\s*['\"]([^'\"]+)['\"]\s*\)"                    # require('x')
    r"|import\(\s*['\"]([^'\"]+)['\"]\s*\)"                     # import('x')
    r"|import\s*['\"]([^'\"]+)['\"]"                            # import 'x'（副作用导入）
)
_ROUTE_DEF_RES = [
    re.compile(r"@\w+\.(?:get|post|put|delete|patch|route|websocket)\(\s*['\"]([^'\"]+)['\"]"),
    re.compile(r"\b(?:app|router)\.(?:get|post|put|delete|patch)\(\s*['\"](/[^'\"]+)['\"]"),
]
_ROUTE_LIT_RE = re.compile(r"['\"](/[a-zA-Z0-9_\-/{}/.:]+)(?:\?[^'\"]*)?(?:\#[^'\"]*)?['\"]")
_ROUTE_PARAM_RE = re.compile(r"\{[^}]*\}|:[^/]+")


def _is_test(rel: str) -> bool:
    name = Path(rel).name
    return (any(p in TEST_DIR_NAMES for p in Path(rel).parts)
            or name.startswith("test_")
            or name.endswith((".spec.ts", ".spec.tsx", ".test.ts", ".test.tsx",
                              ".spec.js", ".spec.jsx", ".test.js", ".test.jsx")))


def enumerate_src(source_root: str | Path) -> list[str]:
    root = Path(source_root).resolve()
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SCAN_BLACKLIST and not d.startswith(".")]
        out += [str((Path(dirpath) / f).relative_to(root))
                for f in filenames if Path(f).suffix.lower() in TRACKED_EXTS]
    return sorted(out)


# 兼容旧名（历史契约：diff 仅 Python 时代的入口名）
enumerate_py = enumerate_src


def _line_hashes(path: Path) -> list[str]:
    return [hashlib.sha1(l.encode("utf-8", "ignore")).hexdigest()[:16]
            for l in path.read_text(encoding="utf-8", errors="ignore").splitlines()]


def write_line_snapshot(source_root: str | Path, baseline_root: str | Path) -> str:
    snap = {rel: _line_hashes(Path(source_root) / rel) for rel in enumerate_src(source_root)}
    p = Path(baseline_root) / SNAPSHOT_NAME
    p.write_text(json.dumps({"_schema": _SNAPSHOT_SCHEMA, "files": snap}), encoding="utf-8")
    return str(p)


def write_import_snapshot(source_root: str | Path, baseline_root: str | Path) -> str:
    """依赖图缓存：file_imports.json（import 边）+ file_routes.json（路由供需边）。"""
    root = Path(source_root).resolve()
    files = enumerate_src(root)
    all_set = set(files)
    snap = {rel: sorted(_import_targets(rel, root, all_set)) for rel in files}
    p = Path(baseline_root) / IMPORTS_NAME
    p.write_text(json.dumps(snap), encoding="utf-8")
    _write_route_snapshot(root, baseline_root, files)
    return str(p)


# ---------------------------------------------------------------- 路由供需边

def _norm_route(r: str) -> str:
    return (_ROUTE_PARAM_RE.sub("{}", r).rstrip("/") or "/")


def _route_defined(text: str) -> set[str]:
    out = set()
    for rx in _ROUTE_DEF_RES:
        for m in rx.findall(text):
            out.add(_norm_route(m))
    return out


def _route_refs(text: str, defined_set: set[str]) -> set[str]:
    return {n for n in (_norm_route(m) for m in _ROUTE_LIT_RE.findall(text)) if n in defined_set}


def _scan_file_routes(root: Path, rel: str, defined_set: set[str] | None = None) -> tuple[list[str], list[str]]:
    try:
        text = (root / rel).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return [], []
    defined = sorted(_route_defined(text))
    refs = sorted(_route_refs(text, defined_set)) if defined_set is not None else []
    return defined, refs


def _write_route_snapshot(root: Path, baseline_root: str | Path, files: list[str]) -> str:
    defined: dict[str, list[str]] = {}
    for rel in files:
        d, _ = _scan_file_routes(root, rel)
        if d:
            defined[rel] = d
    defined_set = {r for rs in defined.values() for r in rs}
    refs: dict[str, list[str]] = {}
    for rel in files:
        _, r = _scan_file_routes(root, rel, defined_set)
        if r:
            refs[rel] = r
    payload = {"defined": defined, "refs": refs, "_defined_set": sorted(defined_set)}
    p = Path(baseline_root) / ROUTES_NAME
    p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------- 变更历史渲染

def _render_history_doc(broot: Path) -> str:
    hp = broot / HISTORY_NAME
    recs = [json.loads(l) for l in hp.read_text(encoding="utf-8").splitlines() if l.strip()]
    out = ["# 变更历史（archmap diff 自动维护）", "",
           "> 时机：功能新增/修改完成后、复盘阶段前执行 `/archmap <项目路径> diff [修改内容备注]` 自动追加本记录。",
           "> 与 diff_impact.json 同源；验收通过后 full/sync 刷新基线并回补 01~09 分析文档，三者构成一个整体。", ""]
    for i, r in enumerate(recs):
        s = r["stats"]
        out += [f"## #{i + 1} ｜ {r['recorded_at']}", "",
                f"- 修改内容：{r['note'] or '（未填写备注）'}",
                f"- 变更文件 {s['changed_files']} 个 / 变更区间 {s['changed_ranges']} 段 / 删除 {s['deleted_files']} 个"
                f" / 影响闭包 {s['closure_files']} 文件 / 测试选中 {s['tests_selected']} 跳过 {s['tests_skipped']}", "",
                "| 文件 | 类型 | 层级 | 变更行区间 |", "|------|------|------|-----------|"]
        out += [f"| {c['path']} | {c['change_type']} | {c.get('tier', '-')} | {c['changed_ranges']} |" for c in r["changed_files"]]
        if r["deleted_files"]:
            out += ["", "- 删除文件：" + "、".join(f"`{p}`" for p in r["deleted_files"])]
        if r["affected_closure"]["propagated"]:
            out += ["", "- 传导影响（未直接变更但被波及）：" + "、".join(f"`{p}`" for p in r["affected_closure"]["propagated"])]
        if r["test_selection"]["untested_changes"]:
            out += ["", "- ⚠️ 无测试覆盖的变更：" + "、".join(f"`{p}`" for p in r["test_selection"]["untested_changes"])]
        out.append("")
    p = broot / HISTORY_DOC_NAME
    p.write_text("\n".join(out), encoding="utf-8")
    return str(p)


def _change_fingerprint(result: dict) -> str:
    """变更指纹：changed_files（按路径排序，含 changed_ranges/symbols）+ deleted_files
    的规范化 JSON → sha1 前 12 位。同一变更区间重复跑 diff 指纹相同。"""
    files = sorted(({"path": c["path"], "change_type": c["change_type"],
                     "changed_ranges": c["changed_ranges"],
                     "symbols": sorted(c.get("symbols", []))} for c in result["changed_files"]),
                   key=lambda c: c["path"])
    payload = {"changed_files": files, "deleted_files": sorted(result["deleted_files"])}
    return hashlib.sha1(json.dumps(payload, ensure_ascii=False, sort_keys=True)
                        .encode("utf-8")).hexdigest()[:12]


def _record_history(broot: Path, result: dict, note: str | None) -> str | None:
    if not result["changed_files"] and not result["deleted_files"]:
        return None
    hp = broot / HISTORY_NAME
    fp = _change_fingerprint(result)
    # 幂等：追加前与台账末条指纹比对，同指纹跳过写入与文档重渲染（存在即跳过，
    # 对齐 agent-harness 幂等治理模式）；指纹字段缺失的旧记录视为不同指纹，向后兼容
    if hp.exists():
        lines = [l for l in hp.read_text(encoding="utf-8").splitlines() if l.strip()]
        if lines:
            try:
                last_rec = json.loads(lines[-1])
            except json.JSONDecodeError:
                last_rec = {}
            if last_rec.get("fingerprint") == fp:
                msg = f"幂等跳过：同指纹变更已记录（#{len(lines)}，指纹 {fp}）"
                print(msg)
                result["history_idempotent_skip"] = msg
                return None
    rec = {"recorded_at": result["computed_at"], "note": note or "", "fingerprint": fp,
           "changed_files": result["changed_files"], "deleted_files": result["deleted_files"],
           "affected_closure": result["affected_closure"], "test_selection": result["test_selection"],
           "stats": result["stats"]}
    with hp.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    _render_history_doc(broot)
    return str(hp)


# ---------------------------------------------------------------- 变更行区间与符号

def _changed_ranges(old: list[str], new: list[str]) -> list[list[int]]:
    ranges: list[list[int]] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag in ("replace", "insert") and j2 > j1:
            ranges.append([j1 + 1, j2])
        elif tag == "delete":  # 纯删除行以新文件边界行打点，否则删除型变更对 diff 隐形
            line = min(j1 + 1, max(len(new), 1))
            ranges.append([line, line])
    merged: list[list[int]] = []
    for s, e in sorted(ranges):
        if merged and s <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


def _symbols_for_ranges(path: Path, ranges: list[list[int]]) -> list[str]:
    """变更行区间 → 所属函数/类名（仅 .py，AST 定位；其它语言返回空）。"""
    if path.suffix != ".py" or not ranges:
        return []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except (SyntaxError, ValueError, OSError):
        return []
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            spans.append((node.lineno, getattr(node, "end_lineno", node.lineno),
                          node.name, isinstance(node, ast.ClassDef)))
    hits: set[str] = set()
    for s, e in ranges:
        best: tuple[int, str] | None = None
        for a, b, name, is_cls in spans:
            if a <= e and s <= b:  # 区间相交
                cand = (b - a, f"class {name}" if is_cls else name)
                if best is None or cand[0] < best[0]:  # 取最小包含跨度（内层优先）
                    best = cand
        if best:
            hits.add(best[1])
    return sorted(hits)


# ---------------------------------------------------------------- import 边提取

def _import_targets(rel: str, root: Path, all_files: set[str]) -> set[str]:
    if rel.endswith(".py"):
        return _py_import_targets(rel, root, all_files)
    if Path(rel).suffix.lower() in {".ts", ".tsx", ".js", ".jsx", ".vue"}:
        return _js_import_targets(rel, root, all_files)
    return set()


def _py_import_targets(rel: str, root: Path, all_files: set[str]) -> set[str]:
    try:
        tree = ast.parse((root / rel).read_text(encoding="utf-8", errors="ignore"))
    except (SyntaxError, ValueError):
        return set()
    pkg = Path(rel).parent
    found: set[str] = set()

    def add(mod: str):
        p = mod.strip(".").replace(".", "/")
        for cand in (f"{p}.py", f"{p}/__init__.py"):
            if cand in all_files:
                found.add(cand)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                add(a.name)
        elif isinstance(node, ast.ImportFrom):
            base = pkg if node.level else Path("")
            for _ in range(max(node.level - 1, 0)):
                base = base.parent
            base_s = "" if str(base) == "." else str(base)
            mod = f"{base_s}/{node.module}".strip("/") if node.module else base_s
            add(mod)
            for a in node.names:
                add(f"{mod}.{a.name}" if mod else a.name)
    found.discard(rel)
    return found


def _resolve_js(spec: str, pkg: Path, all_files: set[str]) -> str | None:
    if spec.startswith("@/"):
        base = f"src/{spec[2:]}"
    elif spec.startswith("."):
        base = os.path.normpath(str(pkg / spec)).replace(os.sep, "/")
        if base.startswith("../"):  # 解析出项目根，丢弃
            return None
    else:
        return None  # bare import（node_modules）不成边
    if base in all_files:
        return base
    for ext in _JS_RESOLVE_EXTS:
        if f"{base}{ext}" in all_files:
            return f"{base}{ext}"
    for ext in _JS_RESOLVE_EXTS:
        if f"{base}/index{ext}" in all_files:
            return f"{base}/index{ext}"
    return None


def _js_import_targets(rel: str, root: Path, all_files: set[str]) -> set[str]:
    try:
        text = (root / rel).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return set()
    pkg = Path(rel).parent
    found: set[str] = set()
    for m in _JS_IMPORT_RE.finditer(text):
        spec = next(g for g in m.groups() if g)
        hit = _resolve_js(spec, pkg, all_files)
        if hit:
            found.add(hit)
    found.discard(rel)
    return found


# ---------------------------------------------------------------- 主入口

def run_diff_impact(project_root: str | Path, baseline_root: str | Path, note: str | None = None) -> dict:
    root, broot = Path(project_root).resolve(), Path(baseline_root)
    snap_p = broot / SNAPSHOT_NAME
    old_raw = json.loads(snap_p.read_text(encoding="utf-8")) if snap_p.exists() else None
    cur_files = enumerate_src(root)
    if old_raw is None:
        write_line_snapshot(root, broot)
        write_import_snapshot(root, broot)
        return {"status": "snapshot_initialized", "detail": "首次运行已建立行级快照，变更自下次比对起可检测",
                "changed_files": [], "stats": {"files": len(cur_files)}}
    if not (isinstance(old_raw, dict) and old_raw.get("_schema") == _SNAPSHOT_SCHEMA):
        # v1 快照（仅 .py）自动迁移：重建三类快照，不产生伪变更洪峰
        write_line_snapshot(root, broot)
        write_import_snapshot(root, broot)
        return {"status": "snapshot_migrated_v2",
                "detail": "快照已从 v1（仅Python）迁移到 v2（多语言+路由边），变更自下次比对起可检测",
                "changed_files": [], "stats": {"files": len(cur_files)}}
    old = old_raw["files"]

    cur = {rel: _line_hashes(root / rel) for rel in cur_files}
    deleted = sorted(set(old) - set(cur_files))
    changed = []
    for rel in cur_files:
        if rel not in old:
            changed.append({"path": rel, "change_type": "added", "changed_ranges": [[1, max(len(cur[rel]), 1)]]})
        elif old[rel] != cur[rel] and (ranges := _changed_ranges(old[rel], cur[rel])):
            changed.append({"path": rel, "change_type": "modified", "changed_ranges": ranges})

    all_set = set(cur_files)
    # 依赖图缓存：仅变更/新增/缓存缺失文件重新解析；新增或删除文件属结构性变更，全量重解析一次
    imports_p = broot / IMPORTS_NAME
    imports: dict = json.loads(imports_p.read_text(encoding="utf-8")) if imports_p.exists() else {}
    for rel in set(imports) - all_set:
        imports.pop(rel)
    structural = bool(deleted) or any(c["change_type"] == "added" for c in changed)
    need = all_set if structural else ({c["path"] for c in changed} | (all_set - set(imports)))
    for rel in sorted(need):
        imports[rel] = sorted(_import_targets(rel, root, all_set))
    imports_p.write_text(json.dumps(imports), encoding="utf-8")

    # 路由供需边缓存：变更文件重扫；全局路由定义集变化时 refs 全量重算（防新路由漏边）
    routes_p = broot / ROUTES_NAME
    routes: dict = json.loads(routes_p.read_text(encoding="utf-8")) if routes_p.exists() \
        else {"defined": {}, "refs": {}, "_defined_set": []}
    for rel in set(routes["defined"]) | set(routes["refs"]):
        if rel not in all_set:
            routes["defined"].pop(rel, None)
            routes["refs"].pop(rel, None)
    for rel in sorted(need):
        d, _ = _scan_file_routes(root, rel)
        routes["defined"][rel] = d
        if not d:
            routes["defined"].pop(rel)
    defined_set = {r for rs in routes["defined"].values() for r in rs}
    if sorted(defined_set) != routes.get("_defined_set", []):
        rescan_refs = all_set  # 路由定义集变化 → 引用面全量重算
        routes["_defined_set"] = sorted(defined_set)
    else:
        rescan_refs = need
    for rel in sorted(rescan_refs):
        _, rr = _scan_file_routes(root, rel, defined_set)
        if rr:
            routes["refs"][rel] = rr
        else:
            routes["refs"].pop(rel, None)
    routes_p.write_text(json.dumps(routes), encoding="utf-8")

    # 依赖图合成：import 边 + 路由边（双向）
    dependents: dict[str, set[str]] = {}
    for src, targets in imports.items():
        for t in targets:
            dependents.setdefault(t, set()).add(src)
    route_dependents: dict[str, set[str]] = {}
    for ref_file, rlist in routes["refs"].items():
        for r in rlist:
            for def_file, dlist in routes["defined"].items():
                if r in dlist and def_file != ref_file:
                    route_dependents.setdefault(def_file, set()).add(ref_file)
                    route_dependents.setdefault(ref_file, set()).add(def_file)
    for t, srcs in route_dependents.items():
        dependents.setdefault(t, set()).update(srcs)

    changed_paths = {c["path"] for c in changed}
    biz_changed = {p for p in changed_paths if not _is_test(p)}

    def bfs(seeds: set[str], graph: dict[str, set[str]]) -> set[str]:
        closure, queue = set(seeds), list(seeds)
        while queue:
            for dep in graph.get(queue.pop(), ()):
                if dep not in closure:
                    closure.add(dep)
                    if not _is_test(dep):  # 测试文件是汇点，不继续传播
                        queue.append(dep)
        return closure

    closure = bfs(biz_changed, dependents)
    # import-only 闭包（单独成图，用于标记路由边带来的增量影响）
    import_dependents: dict[str, set[str]] = {}
    for src, targets in imports.items():
        for t in targets:
            import_dependents.setdefault(t, set()).add(src)
    import_only = bfs(biz_changed, import_dependents)
    via_route = sorted(closure - import_only)

    test_files = [rel for rel in cur_files if _is_test(rel)]
    selected = sorted(t for t in test_files if t in closure or t in changed_paths)
    untested = sorted(p for p in biz_changed if not any(t in closure for t in test_files))

    tiers_p = root / "coverage-tiers.json"
    tier_modules = json.loads(tiers_p.read_text(encoding="utf-8")).get("modules", []) if tiers_p.exists() else []
    for c in changed:
        hits = [m for m in tier_modules if c["path"] == m["path"].rstrip("/") or c["path"].startswith(m["path"].rstrip("/") + "/")]
        c["tier"] = (max(hits, key=lambda m: len(m["path"]))["tier"] if hits else "P2") if not _is_test(c["path"]) else "TEST"
        symbols = _symbols_for_ranges(root / c["path"], c["changed_ranges"])
        if symbols:
            c["symbols"] = symbols

    result = {"status": "ok", "schema_version": "1.1", "mode": "diff",
              "computed_at": datetime.now(timezone.utc).isoformat(),
              "base": {"type": "line_snapshot", "file": SNAPSHOT_NAME},
              "changed_files": changed, "deleted_files": deleted,
              "direct_dependents": {p: sorted(dependents.get(p, ())) for p in sorted(biz_changed)},
              "affected_closure": {"files": sorted(closure), "changed": sorted(biz_changed),
                                   "propagated": sorted(closure - biz_changed)},
              "affected_via_route": via_route,
              "test_selection": {"selected": selected, "skipped": sorted(set(test_files) - set(selected)),
                                 "untested_changes": untested},
              "stats": {"changed_files": len(changed), "changed_ranges": sum(len(c["changed_ranges"]) for c in changed),
                        "deleted_files": len(deleted), "closure_files": len(closure),
                        "route_linked_files": len(via_route),
                        "tests_selected": len(selected), "tests_skipped": len(set(test_files) - set(selected))}}
    (broot / DIFF_OUT_NAME).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    history_path = _record_history(broot, result, note)
    if history_path:
        result["history_path"] = history_path
        result["history_doc"] = str(broot / HISTORY_DOC_NAME)
    return result
