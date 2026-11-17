"""ETL 底层规则探查：检测 ETL 项目特征目录，生成 7 项变更维护服务产出。

产出（写入 <项目路径>/archmap/etl_rules/）：
  ① ETL规则索引总目录.md        分层目录树 + 规则编码 + 关键词标签 + 检索快捷索引
  ② details/ETL-{CODE}.md       每规则独立文档（7 章节：标识/逻辑/定位/约束/依赖/历史/测试）
  ③ etl_rule_mapping.json       规则-代码-配置映射对照表（机器可读）
  ④ ETL规则依赖链路图.md        Mermaid 依赖图 + 文字影响清单 + 影响分级
  ⑤ ETL全局参数基线表.md        参数基线速查
  ⑥ ETL规则变更风险评估清单.md  变更风险清单
  ⑦ etl_rule_search_index.json  机器检索索引（含关键词快捷索引）

行号防漂移：源码定位一律运行时按「函数名/特征串」grep 解析，文档只写解析后的当前行号。
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .etl_rule_registry import CONFIG_READS as _CONFIG_READS  # 兼容别名（真实数据已迁入注册表 config_reads）
from .etl_rule_registry import Registry, get_registry, rule_priority


def detect_etl_project(source_root: str | Path) -> bool:
    """检测项目是否生成 ETL 探查产出。

    项目存在自定义注册表（archmap/etl_rule_registry.json）→ 必触发；
    否则按注册表特征目录检测（内置：tongue_diagnosis/etl、etl_config、etl/core
    及通用项 etl、etl_pipeline、pipelines；自定义注册表用其 etl_detect_dirs）。
    """
    root = Path(source_root)
    reg = get_registry(root)
    if reg.is_custom:
        return True
    return any((root / d).is_dir() for d in reg.etl_detect_dirs)


def _resolve_src_line(source_root: Path, src: dict) -> Optional[int]:
    """按函数名/特征串解析源码当前行号；文件或特征缺失返回 None（不编造）。"""
    path = source_root / src["file"]
    if not path.is_file():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    if src.get("fn"):
        fn = src["fn"].rsplit(".", 1)[-1]  # 兼容 "Class.method" 点号写法
        for i, ln in enumerate(lines, 1):
            if (ln.startswith(f"def {fn}(") or ln.startswith(f"    def {fn}(")
                    or ln.startswith(f"class {fn}(") or ln.startswith(f"class {fn}:")):
                return i
    elif src.get("pattern"):
        for i, ln in enumerate(lines, 1):
            if ln.startswith(src["pattern"]) or src["pattern"] in ln:
                return i
    return None


def _load_config_params(source_root: Path, config_reads: dict | None = None) -> dict[str, dict]:
    """运行时读取真实配置参数（sync 回填依据）；文件缺失/解析失败回退注册表基线，不编造。

    config_reads 缺省时按 source_root 解析注册表（项目覆盖优先，内置兜底）。
    """
    import yaml
    if config_reads is None:
        config_reads = get_registry(source_root).config_reads
    out: dict[str, dict] = {}
    source_root = Path(source_root)
    for code, (rel, pairs) in config_reads.items():
        path = source_root / rel
        if not path.is_file():
            continue
        try:
            cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            params = {}
            for key, dot_path in pairs:
                v = cfg
                for part in dot_path.split("."):
                    v = (v or {}).get(part, {})
                if v != {}:
                    params[key] = v
            if params:
                out[code] = params
        except (OSError, UnicodeDecodeError, yaml.YAMLError):
            continue
    return out


def _resolve_all_lines(source_root: Path, reg: Registry) -> dict[str, list[dict]]:
    """全部规则源码定位分级解析：{code: [{file, line, fn|pattern, depth}]}。

    P0/P1 深度解析：运行时 grep 函数名/特征串产出真实行号，未解析标 None。
    P2 轻量解析：仅校验文件存在性，行号固定 None 且 depth=file_check（不计入 unresolved）。
    """
    resolved = {}
    for r in reg.rules:
        depth = "file_check" if rule_priority(r) == "P2" else "full"
        locs = []
        for src in r["src"]:
            line = None if depth == "file_check" else _resolve_src_line(source_root, src)
            locs.append({"file": src["file"], "fn": src.get("fn"), "pattern": src.get("pattern"),
                         "line": line, "depth": depth,
                         "file_exists": (source_root / src["file"]).is_file()})
        resolved[r["code"]] = locs
    return resolved


def _loc_md(locs: list[dict]) -> str:
    """源码定位章节表格（full 深度行号缺失标「需人工核对」；P2 轻量解析标注文件存在性）。"""
    rows = []
    for loc in locs:
        name = loc.get("fn") or loc.get("pattern") or "（整文件）"
        if loc["line"]:
            line = f"{loc['line']}"
        elif loc.get("depth") == "file_check":
            line = "P2 轻量·文件存在 ✓" if loc.get("file_exists") else "P2 轻量·文件缺失 ✗"
        else:
            line = "需人工核对"
        rows.append(f"| {loc['file']} | `{name}` | {line} |")
    return "\n".join(rows) if rows else "| - | - | - |"


# ── ① 索引总目录 ──

def _md_index(reg: Registry, resolved: dict, project: str, now: str) -> str:
    parts = [f"# ETL 规则索引总目录\n",
             f"> 项目：{project} ｜ 生成时间：{now} ｜ 规则总数：{len(reg.rules)} ｜ 行号运行时解析防漂移",
             f"> 解析分级：P0 深度解析（行号+配置+契约）｜ P1 标准解析（行号）｜ P2 轻量解析（仅文件存在性）",
             f"> 用途：修改任意 ETL 步骤/规则时，先查本目录定位规则编码 → 打开对应详情文档 → 查依赖链路 → 查风险清单 → 按测试用例验证。\n",
             "## 分层目录树"]
    for layer_code, layer_name_cn in reg.layers:
        rules = [r for r in reg.rules if r["layer"] == layer_code]
        parts.append(f"\n### {layer_code} · {layer_name_cn}（{len(rules)} 条）")
        for r in rules:
            tags = "、".join(f"`{k}`" for k in r["keywords"][:4])
            parts.append(f"- {r['code']} **{r['name']}**（{r['rid']} · {rule_priority(r)}）— {tags} → [详情](details/{r['code']}.md)")
    parts.append("\n## 检索快捷索引（关键词 → 规则编码）\n")
    parts.append("| 关键词 | 规则编码 |")
    parts.append("|--------|---------|")
    for kw, codes in sorted(reg.keyword_index.items()):
        parts.append(f"| `{kw}` | {', '.join(codes)} |")
    parts.append("""\n## 使用流程（7 步）
1. 确定要修改的 ETL 行为 → 提炼 1-3 个关键词
2. 用关键词在上表/`etl_rule_search_index.json` 查规则编码
3. 打开 `details/{编码}.md` 阅读 7 章节（含源码行号）
4. 打开 `ETL规则依赖链路图.md` 确认上下游影响
5. 打开 `ETL规则变更风险评估清单.md` 评估风险
6. 改代码 → 按详情文档第 7 章测试用例验证
7. 改配置 → 按 `ETL全局参数基线表.md` 核对基线值
""")
    return "\n".join(parts)


# ── ② 单规则详情（7 章节） ──

def _md_detail(reg: Registry, r: dict, resolved_locs: list[dict], now: str, params: dict | None = None) -> str:
    dep_up = "、".join(f"`{c}` {reg.rules_by_code[c]['name']}" for c in r["depends"]) or "无"
    dep_down = "、".join(f"`{c}` {reg.rules_by_code[c]['name']}" for c in reg.downstream_codes(r["code"])) or "无"
    consumers = "、".join(r["consumers"]) or "无（ETL 内部）"
    tests = "、".join(r["tests"]) or "暂无专项用例"
    params = "\n".join(f"- `{k}` = {v}" for k, v in (params or r["params"]).items()) or "无参数基线"
    history = "\n".join(f"- {h}" for h in r["history"]) or "- 暂无记录（2026-08-05 清单调研起）"
    locs = _loc_md(resolved_locs)
    prio = rule_priority(r)
    depth_desc = {"P0": "深度解析", "P1": "标准解析", "P2": "轻量解析"}[prio]
    return f"""# {r['code']} {r['name']}（{r['rid']}）

> 生成时间：{now} ｜ 分层：{reg.layer_name(r['code'])} ｜ 优先级：**{prio}**（{depth_desc}）｜ 风险等级：**{r['risk_level']}**

## 1. 规则基础标识
| 项 | 值 |
|----|-----|
| 规则编码 | `{r['code']}` |
| 规则标识 | {r['rid']} |
| 规则名称 | {r['name']} |
| 所属分层 | {reg.layer_name(r['code'])} |
| 关键词标签 | {'、'.join('`' + k + '`' for k in r['keywords'])} |
| 风险等级 | {r['risk_level']} |

## 2. 完整底层执行逻辑
{r['summary']}

## 3. 源码精准定位
| 文件 | 符号 | 当前行号 |
|------|------|---------|
{locs}

## 4. 输入输出约束
**参数基线：**
{params}

**约束说明：**
{r['notes'] if r['notes'] else '无额外约束'}

## 5. 关联依赖规则
**上游依赖（本规则依赖）：** {dep_up}

**下游依赖（依赖本规则）：** {dep_down}

**业务消费者：** {consumers}

## 6. 历史改动记录
{history}

## 7. 测试校验标准
**测试文件：** {tests}

**回归命令：** `python3 -m pytest tests/test_tongue_etl/ -x -q`（全量 218 passed / 10 skipped 基线）
"""


# ── ③ 映射对照表（JSON） ──

def _mapping_json(reg: Registry, resolved: dict, project: str, now: str, config_params: dict | None = None) -> dict:
    config_params = config_params or {}
    return {
        "generated_at": now, "project": project, "rule_total": len(reg.rules),
        "rows": [{
            "code": r["code"], "rid": r["rid"], "name": r["name"], "layer": reg.layer_name(r["code"]),
            "priority": rule_priority(r), "risk_level": r["risk_level"],
            "src": [{"file": loc["file"], "symbol": loc.get("fn") or loc.get("pattern"), "line": loc["line"]} for loc in resolved[r["code"]]],
            "config": r["config"], "params": {**r["params"], **config_params.get(r["code"], {})}, "depends": r["depends"],
            "tests": r["tests"],
        } for r in reg.rules],
    }


# ── ④ 依赖链路图 ──

def _md_dependency(reg: Registry, resolved: dict, project: str, now: str) -> str:
    node_lines = []
    edge_lines = []
    for layer_code, layer_name_cn in reg.layers:
        rules = [r for r in reg.rules if r["layer"] == layer_code]
        node_lines.append(f"  subgraph {layer_code}[{layer_name_cn}]")
        for r in rules:
            node_lines.append(f"    {r['code']}[\"{r['code']} {r['name']}\"]")
        node_lines.append("  end")
    for r in reg.rules:
        for dep in r["depends"]:
            edge_lines.append(f"  {dep} --> {r['code']}")
    mermaid = "\n".join(["```mermaid", "flowchart LR", *node_lines, *edge_lines, "```"])
    rows = []
    for r in reg.rules:
        down = reg.downstream_codes(r["code"])
        down_txt = "、".join(f"`{c}`" for c in down) or "无下游规则"
        consumers = "、".join(r["consumers"]) or "无业务消费者"
        rows.append(f"| {r['code']} | {r['name']} | **{r['risk_level']}** | {down_txt} | {consumers} |")
    impact = "\n".join(rows)
    return f"""# ETL 上下游依赖链路图 + 影响说明

> 项目：{project} ｜ 生成时间：{now}

## Mermaid 依赖链路图（实线 = 上游依赖 → 下游规则）

{mermaid}

## 文字影响清单（规则 → 下游规则 / 业务消费者 / 影响分级）

| 规则编码 | 规则名称 | 影响分级 | 下游规则 | 业务消费者 |
|---------|---------|---------|---------|-----------|
{impact}

## 影响分级说明
- **高**：改动后需全库重灌 / 波及外部调用方（PDF 上传、迁移重跑、复盘入库）/ 破坏幂等
- **中**：影响检索命中或对账一致性，需重建索引或触发对账
- **低**：仅影响标注/分类等元数据，改动可局部验证
"""


# ── ⑤ 参数基线表 ──

def _md_params(reg: Registry, project: str, now: str, config_params: dict | None = None) -> str:
    config_params = config_params or {}
    rows = []
    for r in reg.rules:
        if not r["params"]:
            continue
        for k, v in {**r["params"], **config_params.get(r["code"], {})}.items():
            rows.append(f"| {r['code']} | {r['name']} | `{k}` | `{v}` | {'、'.join(r['config']) or '代码内默认'} |")
    body = "\n".join(rows)
    return f"""# ETL 全局参数基线表

> 项目：{project} ｜ 生成时间：{now} ｜ 用途：改配置前核对基线值，改后确认不漂移
> 参数值说明：ETL-ORCH-08 / ETL-VEC-01 / ETL-CHUNK-02 参数为运行时读取配置文件（sync 自动回填），其余为代码常量基线。

| 规则编码 | 规则名称 | 参数 | 基线值 | 来源（配置文件） |
|---------|---------|------|--------|----------------|
{body}
"""


# ── ⑥ 风险评估清单 ──

def _md_risk(reg: Registry, project: str, now: str) -> str:
    rows = []
    for r in reg.rules:
        rows.append(f"| {r['code']} | {r['name']} | **{r['risk_level']}** | {r['risk_desc']} | {'、'.join(r['tests']) or '暂无专项'} |")
    body = "\n".join(rows)
    return f"""# ETL 规则变更风险评估清单

> 项目：{project} ｜ 生成时间：{now} ｜ 用途：修改规则前先评估风险与回归范围

| 规则编码 | 规则名称 | 风险等级 | 风险描述 | 回归测试 |
|---------|---------|---------|---------|---------|
{body}

## 变更前置动作（硬性）
1. **高风险规则**（幂等/chunk_id/写路径/错误语义）：改前备份数据，改后全量重灌验证幂等（重跑行数不变）
2. **涉及配置**：改 `etl.yaml`/`embedding.yaml`/`chunking.yaml` 后同步更新参数基线表
3. **涉及契约**（24 字段/meta 结构）：同步 api_contract.json 与下游 ADAPTER/DELETE/MIGRATE
4. **涉及函数改名**：先 grep 全项目引用再改名（规则 14 跨文件审计）
"""


# ── ⑧ 配置契约漂移检测 ──

def _grep_hits(source_root: Path, rel: str, pattern: str) -> int:
    """代码文件内特征串命中计数；文件缺失/不可读返回 0（不编造）。"""
    path = source_root / rel
    if not path.is_file():
        return 0
    try:
        return path.read_text(encoding="utf-8").count(pattern)
    except (OSError, UnicodeDecodeError):
        return 0


def _key_in_yaml(source_root: Path, rel: str, key: str) -> bool:
    """yaml 文件内点号键实存检查；解析失败返回 False（不编造）。"""
    path = source_root / rel
    if not path.is_file():
        return False
    try:
        import yaml
        v = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for part in key.split("."):
            v = (v or {}).get(part, None)
            if v is None:
                return False
        return True
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return False


def _residual_use_hits(source_root: Path, rel: str, symbol: str, pattern: str) -> int:
    """代码残留参数检查：定位顶层符号定义，统计其函数体内指定使用模式命中数。"""
    path = source_root / rel
    if not path.is_file():
        return 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return 0
    start = next((i for i, ln in enumerate(lines) if ln.startswith(symbol)), None)
    if start is None:
        return -1  # 符号已不存在（残留已清理）
    body = "\n".join(lines[start + 1:start + 40])
    return body.count(pattern)


def _scan_config_contract(source_root: Path, contracts: list | None = None) -> dict:
    """扫描配置契约：yaml 键实存 + read/use 特征 grep → aligned / unused / stale / missing_from_yaml。

    contracts 缺省时按 source_root 解析注册表（项目覆盖优先，内置兜底）。
    """
    if contracts is None:
        contracts = get_registry(source_root).config_contracts
    rows = []
    for c in contracts:
        in_yaml = _key_in_yaml(source_root, c["file"], c["key"]) if c.get("file") else None
        if c["kind"] == "code_residual":
            use = _residual_use_hits(source_root, c["code_file"], c["symbol"], c["use"])
            status = "symbol_missing" if use < 0 else ("aligned" if use > 0 else "stale")
            row = {"kind": "code_residual", "rule": c["rule"], "file": c["code_file"], "field": c["symbol"],
                   "in_yaml": None, "read_hits": None, "use_hits": max(use, 0), "status": status, "note": c["note"]}
        else:
            read = _grep_hits(source_root, c["code_file"], c["read"])
            use = _grep_hits(source_root, c["code_file"], c["use"])
            status = "aligned" if use > 0 else ("missing_from_yaml" if in_yaml is False else "unused")
            row = {"kind": "config_field", "rule": c["rule"], "file": c["code_file"], "field": c.get("key") or c["read"],
                   "in_yaml": in_yaml, "read_hits": read, "use_hits": use, "status": status, "note": c["note"]}
        rows.append(row)
    return rows


def _md_config_contract(rows: list[dict], project: str, now: str) -> str:
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in
              ("aligned", "unused", "stale", "missing_from_yaml", "symbol_missing")}
    body = "\n".join(
        f"| {r['rule']} | `{r['file']}` | `{r['field']}` | {r['in_yaml'] if r['in_yaml'] is not None else '—'} | "
        f"{r['read_hits'] if r['read_hits'] is not None else '—'} | {r['use_hits']} | **{r['status']}** | {r['note']} |"
        for r in rows)
    advise = {
        "unused": "配置字段未被代码消费：删除 yaml 字段 或 接线消费点（如 reconcile.enabled 需 run_reconcile 接入调度）",
        "stale": "代码残留参数已写死废弃：清理函数签名/调用参数（如 _rrf_fuse weights）",
        "missing_from_yaml": "代码读取的键在 yaml 缺失：对齐键名/层级（契约不一致）",
    }
    advise_body = "\n".join(f"- **{k}**（{counts[k]} 处）：{v}" for k, v in advise.items() if counts[k] > 0)
    if not advise_body:
        advise_body = "- 当前无漂移，配置-代码契约全部对齐"
    return f"""# ETL 配置契约对齐报告

> 项目：{project} ｜ 生成时间：{now} ｜ 用途：定期对齐配置字段与代码消费点（字段存在 ≠ 生效）
> 检测方式：yaml 点号键实存检查 + read/use 特征串代码 grep，全部运行时解析，不编造
> 状态含义：aligned=已接线 ｜ unused=配置未消费（死配置） ｜ stale=代码残留已写死 ｜ missing_from_yaml=代码读但 yaml 缺失

## 状态速览
| 状态 | 数量 |
|------|------|
| aligned（已接线） | {counts['aligned']} |
| unused（死配置） | {counts['unused']} |
| stale（代码残留） | {counts['stale']} |
| missing_from_yaml（契约不一致） | {counts['missing_from_yaml']} |
| symbol_missing（残留已清理） | {counts['symbol_missing']} |

## 逐字段契约核对表
| 规则 | 配置文件 | 字段 | yaml 实存 | 代码读取 | 代码消费 | 状态 | 说明 |
|------|---------|------|----------|---------|---------|------|------|
{body}

## 处置建议（对齐动作）
{advise_body}
"""


def _config_contract_json(rows: list[dict], project: str, now: str) -> dict:
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in
              ("aligned", "unused", "stale", "missing_from_yaml", "symbol_missing")}
    return {"generated_at": now, "project": project, "field_total": len(rows), "status_counts": counts,
            "items": rows}


# ── ⑦ 机器检索索引 ──

def _search_index_json(reg: Registry, resolved: dict, project: str, now: str, config_params: dict | None = None) -> dict:
    config_params = config_params or {}
    return {
        "version": 1, "generated_at": now, "project": project, "rule_total": len(reg.rules),
        "keyword_index": {kw: codes for kw, codes in sorted(reg.keyword_index.items())},
        "rules": [{
            "code": r["code"], "rid": r["rid"], "name": r["name"], "layer": reg.layer_name(r["code"]),
            "priority": rule_priority(r),
            "keywords": r["keywords"], "summary": r["summary"][:160],
            "src": [{"file": loc["file"], "symbol": loc.get("fn") or loc.get("pattern"), "line": loc["line"]} for loc in resolved[r["code"]]],
            "config": r["config"], "params": {**r["params"], **config_params.get(r["code"], {})}, "depends": r["depends"],
            "downstream": reg.downstream_codes(r["code"]), "risk_level": r["risk_level"],
            "tests": r["tests"], "detail_doc": f"etl_rules/details/{r['code']}.md",
        } for r in reg.rules],
    }


def generate_etl_reports(baseline_mgr, source_root: str | Path) -> dict:
    """生成 7 项 ETL 探查产出到 <基线目录>/etl_rules/，返回生成摘要。

    注册表按 source_root 解析：项目 archmap/etl_rule_registry.json 覆盖优先，内置兜底。
    """
    project = baseline_mgr.project_name
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    source_root = Path(source_root)
    reg = get_registry(source_root)
    resolved = _resolve_all_lines(source_root, reg)
    config_params = _load_config_params(source_root, reg.config_reads)
    total_locs = sum(len(v) for v in resolved.values())
    full_locs = [loc for locs in resolved.values() for loc in locs if loc["depth"] == "full"]
    resolved_lines = sum(1 for loc in full_locs if loc["line"])
    priority_counts = {p: sum(1 for r in reg.rules if rule_priority(r) == p) for p in ("P0", "P1", "P2")}

    etl_dir = Path(baseline_mgr.baseline_dir) / "etl_rules"
    (etl_dir / "details").mkdir(parents=True, exist_ok=True)
    baseline_mgr.write_text("etl_rules/ETL规则索引总目录.md", _md_index(reg, resolved, project, now))
    for r in reg.rules:
        baseline_mgr.write_text(f"etl_rules/details/{r['code']}.md",
                                _md_detail(reg, r, resolved[r["code"]], now, config_params.get(r["code"])))
    baseline_mgr.write_json("etl_rules/etl_rule_mapping.json", _mapping_json(reg, resolved, project, now, config_params))
    baseline_mgr.write_text("etl_rules/ETL规则依赖链路图.md", _md_dependency(reg, resolved, project, now))
    baseline_mgr.write_text("etl_rules/ETL全局参数基线表.md", _md_params(reg, project, now, config_params))
    baseline_mgr.write_text("etl_rules/ETL规则变更风险评估清单.md", _md_risk(reg, project, now))
    baseline_mgr.write_json("etl_rules/etl_rule_search_index.json", _search_index_json(reg, resolved, project, now, config_params))

    # 第 8 项：配置契约漂移检测（定期对齐依据）
    contract_rows = _scan_config_contract(source_root, reg.config_contracts)
    contract_counts = {s: sum(1 for r in contract_rows if r["status"] == s) for s in
                       ("aligned", "unused", "stale", "missing_from_yaml", "symbol_missing")}
    baseline_mgr.write_text("etl_rules/ETL配置契约对齐报告.md", _md_config_contract(contract_rows, project, now))
    baseline_mgr.write_json("etl_rules/config_contract_report.json",
                            _config_contract_json(contract_rows, project, now))

    return {"detected": True, "rules": len(reg.rules), "src_locs": total_locs,
            "resolved_lines": resolved_lines, "unresolved": len(full_locs) - resolved_lines,
            "priority_counts": priority_counts,
            "parse_depth": {"full": priority_counts["P0"] + priority_counts["P1"],
                            "file_check": priority_counts["P2"]},
            "registry_source": reg.source,
            "config_params_read": list(config_params.keys()),
            "config_contract": contract_counts,
            "files": ["etl_rules/ETL规则索引总目录.md", f"etl_rules/details/*.md ({len(reg.rules)})",
                      "etl_rules/etl_rule_mapping.json", "etl_rules/ETL规则依赖链路图.md",
                      "etl_rules/ETL全局参数基线表.md", "etl_rules/ETL规则变更风险评估清单.md",
                      "etl_rules/etl_rule_search_index.json",
                      "etl_rules/ETL配置契约对齐报告.md", "etl_rules/config_contract_report.json"]}
