#!/usr/bin/env python3
"""check_model.py — semantic.yaml 铁律 lint（ai-data-delivery v0.0.7）

把五条铁律与评测暴露的元数据缺陷落成机器检查。发布门禁：零 ERROR。

用法：
  python check_model.py -f semantic.yaml [--strict]   # --strict：WARN 也视为失败
  python check_model.py -f semantic.yaml --drift 上一版.yaml [--drift-report drift.json]
      # 维护模式：与基线对比，输出 新增/删除/变更/破坏 四级分类；有 breaking 即退出码 1
  python check_model.py -f semantic.yaml --history quality_history.jsonl
      # 追加一条质量记录（release 趋势用），不影响门禁退出码

规则（E=ERROR / W=WARN）：
  E01 数据集缺 grain（粒度声明是第一约束，粒度不清则聚合必错）
  E02 数据集主键缺失
  E03 字段 role 非法（必须 ∈ pk/fk/dim/measure/time/attr）
  E04 疑似敏感字段未标记（身份证/手机号/资格证号等，必须 sensitive: true 或 allow_llm: false）
  E05 ratio 指标缺分子/分母（禁行级平均 DEC-METRIC-01）
  E06 ratio 指标表达式含 AVG(（行级平均，F01 实测事故）
  E07 structured 指标缺 expr 且缺分子分母（指标必须自含全口径）
  E08 指标挂载的数据集不存在 / 指标 time_field 不在数据集字段中
  E09 关系缺 join_key/cardinality/traversable，或 from/to 不是已声明数据集
       （traversable=true 必须有真实 join_key；弱关联必须 traversable=false 且有 note）
  E10 概念缺可执行展开（expand.dataset/field/values 或 union；无展开条件的概念不准发布）
  E11 id/name/term 重复
  E12 本体实体 name 缺失/重复、is_a 指向未声明实体、is_a 成环
  E13 本体关系端点不是已声明本体实体、缺 predicate、mapping 非法，
       或 mapping≠equi_key 而无 note（无键关系必须写明落地说明）
  E14 投影回指悬空：dataset/relationship 的 ontology_ref 指向不存在的本体对象
       （含声明了 ontology_ref 但模型无 ontology 段；实体引用接受 name 或 uid 两种写法）
  E15 无键关系被投影：合同 relationship 的 ontology_ref 指向 mapping≠equi_key 的本体关系
       （合同只承载等值键关系；本体表达得了 ≠ 合同该承载）
  E16 概念禁用词与自身 term/synonyms 冲突（禁用词是被禁止的说法，不能同时是别名）
  E17 指标 on_zero_denominator 非法（∈ null/zero/error；缺省为 null）
  E18 明细模板 id 重复 / 挂载数据集不存在 / columns、time_field 引用数据集没有的字段
  E19 受支持的 structured 单表指标引用未声明字段，或混用聚合与逐行语义
  W01 数据集缺 ai.instructions（表描述是给模型的路由+边界指令，不是给人看的说明书）
  W02 维度字段缺 enum（若该字段是状态/枚举类，缺字典则模型写错过滤条件且不报错）
  W03 数据集无 time 角色字段（时间围栏无法落地，"今天/本月"必错）
  W04 structured 指标缺 time_field
  W05 structured 指标还是 草案 状态
  W06 tenant_field 指向不存在字段
  W07 本体实体未被任何数据集投影且未写 unprojected_reason（未投影必须说明原因）
  W08 本体关系 mapping=equi_key 但未被任何合同关系投影（声明了可落地关系却未落地）
  W09 同一 domain 内两个概念认领同一 synonym（路由会歧义）
  W10 概念 valid_to 已过期（需复审：续期、下线或改口径）
  W11 比率指标有分母但未显式声明 on_zero_denominator（缺省 null 会把除零静默变 NULL）
  W13 不可遍历关系未写明原因（note）
  W14 无 datasets 的纯本体草案（仅做本体结构检查；投影对账与合同检查不适用）
  W15 unit 为 % 的 ratio 未声明 display_scale（编译值是 0–1 分数，×100 展示责任必须显式落地）
  W16 指标 filters / 概念 expand 的取值不在字段 enum 字典中（会静默错过滤）
  W17 structured 指标同义词 <3 个（同义词是指标命中路由的生命线，命中不了就掉进慢速 NL2SQL）
  W18 明细模板缺 time_field（明细也必须时间围栏）或同义词 <3 个
  W19 本地编译器未覆盖该 structured 指标，表达式依赖未验证（不等于业务定义非法）
  W12 本体实体缺 uid（缺省以 name 为身份，重命名后 drift/历史不可追踪；建议 ent_xxx 稳定 ID）

本体段是声明式事实清单：本工具只做静态结构检查与两层对账，不做任何跨声明推导
（不推 is-a 传递、不推子类继承关系、不推逆关系、不做逻辑一致性判定；不是 OWL/SHACL）。
"""
import argparse
import re
import sys

import yaml
from _contract import load

ROLES = {"pk", "fk", "dim", "measure", "time", "attr"}
SENSITIVE_PAT = re.compile(
    r"身份证|手机号|电话|资格证号|证件号|护照|银行卡|社保卡|医保|邮箱|"
    r"license_no|id_card|phone|mobile|ssn|passport|bank_card|card_no|email", re.I)
ENUM_HINT = re.compile(r"状态|类型|等级|类别|方式|来源|是否|标志|类目|岗位|"
                       r"status|type|level|category|class|post|source|is_", re.I)


class Reporter:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, code, where, msg):
        self.errors.append(f"[ERROR {code}] {where} —— {msg}")

    def warn(self, code, where, msg):
        self.warnings.append(f"[WARN  {code}] {where} —— {msg}")


def field_names(ds):
    return {f.get("name") for f in ds.get("fields", []) if isinstance(f, dict)}


def check_datasets(m, rep):
    seen = set()
    for ds in m.get("datasets", []) or []:
        name = ds.get("name", "?")
        where = f"dataset[{name}]"
        if name in seen:
            rep.error("E11", where, "数据集 name 重复")
        seen.add(name)
        if not ds.get("grain"):
            rep.error("E01", where, "缺 grain 粒度声明（一行代表什么）")
        if not ds.get("primary_key"):
            rep.error("E02", where, "缺 primary_key（去重与 join 依据）")
        else:
            from _contract import keys
            if not set(keys(ds["primary_key"])) <= field_names(ds):
                rep.error("E02", where, "primary_key 引用了不存在的字段")
        if not (ds.get("ai") or {}).get("instructions"):
            rep.warn("W01", where, "缺 ai.instructions（能答什么/不能答什么/必带过滤）")
        tf = ds.get("tenant_field")
        if tf and tf not in field_names(ds):
            rep.warn("W06", where, f"tenant_field {tf!r} 不在字段清单中")
        has_time = False
        for f in ds.get("fields", []) or []:
            fn, fw = f.get("name", "?"), f"{where}.fields[{f.get('name', '?')}]"
            if f.get("role") not in ROLES:
                rep.error("E03", fw, f"role 非法：{f.get('role')!r}（∈ {sorted(ROLES)}）")
            if f.get("role") == "time":
                has_time = True
            cn = str(f.get("cn", ""))
            if f.get("role") == "dim" and not f.get("enum") and ENUM_HINT.search(fn + " " + cn):
                rep.warn("W02", fw, "疑似枚举类 dim 缺 enum 值字典（缺则模型写错过滤条件且不报错）")
            if SENSITIVE_PAT.search(fn) or SENSITIVE_PAT.search(cn):
                if not (f.get("sensitive") or f.get("allow_llm") is False):
                    rep.error("E04", fw, "疑似敏感字段未标记 sensitive: true / allow_llm: false")
        if not has_time:
            rep.warn("W03", where, "无 time 角色字段（时间围栏与相对时间口径无法落地）")


def check_relationships(m, rep, ds_names):
    from check_join_graph import validate_relation
    ds_index = {d["name"]: d for d in m.get("datasets", [])}
    for r in m.get("relationships", []) or []:
        where = f"relationship[{r.get('from','?')}→{r.get('to','?')}]"
        for ep in (r.get("from"), r.get("to")):
            if ep not in ds_names:
                rep.error("E09", where, f"端点 {ep!r} 不是已声明数据集")
        if r.get("cardinality") is None:
            rep.error("E09", where, "缺 cardinality")
        trav = r.get("traversable")
        if trav is None:
            rep.error("E09", where, "缺 traversable 标记")
        if trav:
            try:
                validate_relation(r, ds_index)
            except (ValueError, TypeError) as exc:
                rep.error("E09", where, str(exc))
        elif not isinstance(trav, bool):
            rep.error("E09", where, "traversable 必须为布尔值")
        if trav is False and not r.get("note"):
            rep.warn("W13", where, "不可遍历关系应写明原因（note），防静默弱 join")


def check_concepts(m, rep, ds_index):
    import datetime as dt
    seen = set()
    synonym_owner = {}
    for c in m.get("concepts", []) or []:
        term = c.get("term", "?")
        where = f"concept[{term}]"
        if term in seen:
            rep.error("E11", where, "概念 term 重复")
        seen.add(term)
        own_words = {term} | set(c.get("synonyms", []) or []) | set(c.get("aliases", []) or [])
        forbidden = set(c.get("forbidden", []) or [])
        if forbidden & own_words:
            rep.error("E16", where, f"禁用词与自身说法冲突：{sorted(forbidden & own_words)}")
        domain = c.get("domain", "")
        for syn in (c.get("synonyms", []) or []) + (c.get("aliases", []) or []):
            key = (domain, syn)
            if key in synonym_owner and synonym_owner[key] != term:
                rep.warn("W09", where,
                         f"synonym {syn!r} 在同 domain 内已被概念 {synonym_owner[key]!r} 认领")
            synonym_owner.setdefault(key, term)
        valid_to = c.get("valid_to")
        if valid_to:
            try:
                if dt.date.fromisoformat(str(valid_to)[:10]) < dt.date.today():
                    rep.warn("W10", where, f"valid_to {valid_to} 已过期（需复审：续期/下线/改口径）")
            except ValueError:
                rep.warn("W10", where, f"valid_to {valid_to!r} 不是 ISO 日期")
        ex = c.get("expand")
        if not ex:
            rep.error("E10", where, "无 expand 展开条件（概念必须可执行，不准发布）")
            continue
        branches = ex.get("union") if isinstance(ex.get("union"), list) else [ex]
        for b in branches:
            dsn, fld = b.get("dataset"), b.get("field")
            if not dsn or not fld or b.get("values") is None:
                rep.error("E10", where, "expand 分支缺 dataset/field/values")
                continue
            ds = ds_index.get(dsn)
            if ds is None:
                rep.error("E10", where, f"expand.dataset {dsn!r} 不存在")
            elif fld not in field_names(ds):
                rep.error("E10", where, f"expand.field {fld!r} 不在 {dsn} 的字段中")
            else:
                _check_values_in_enum(rep, where + ".expand", ds, fld, b.get("values"))


def _enum_of(ds, fld):
    for f in ds.get("fields", []) or []:
        if f.get("name") == fld and f.get("enum"):
            return {str(v) for v in f["enum"]}
    return None


def _check_values_in_enum(rep, where, ds, fld, values):
    """W16：过滤/展开取值必须在字段 enum 字典内（不在则引擎静默错过滤）。"""
    enum = _enum_of(ds, fld)
    if enum is None or not isinstance(values, list):
        return
    missing = [v for v in values if str(v) not in enum]
    if missing:
        rep.warn("W16", where,
                 f"取值 {missing} 不在 {ds.get('name')}.{fld} 的 enum {sorted(enum)} 中（会静默错过滤）")


def check_ontology(m, rep):
    """本体段结构检查 + 合同投影对账。ontology 段是声明式事实清单，不做推理。"""
    from _contract import (MAPPINGS, EVIDENCE_SOURCES, evidence_source,
                           ont_entities, ont_relations, ont_relation_id)
    entities = ont_entities(m)
    relations = ont_relations(m)
    datasets = m.get("datasets", []) or []
    contract_rels = m.get("relationships", []) or []
    has_refs = any(d.get("ontology_ref") for d in datasets) or \
        any(r.get("ontology_ref") for r in contract_rels)
    if not entities and not relations:
        if has_refs:
            rep.error("E14", "model", "声明了 ontology_ref 但模型无 ontology 段")
        return
    ent_names = set()
    ent_uids = set()
    uid2name = {}
    for e in entities:
        name = e.get("name")
        where = f"ontology.entity[{name or '?'}]"
        if not name:
            rep.error("E12", "ontology.entity[?]", "缺 name")
            continue
        if name in ent_names:
            rep.error("E12", where, "本体实体 name 重复")
        ent_names.add(name)
        uid = e.get("uid")
        if uid:
            if uid in ent_uids:
                rep.error("E11", where, f"本体实体 uid 重复：{uid!r}")
            ent_uids.add(uid)
            uid2name[uid] = name
        else:
            rep.warn("W12", where, "缺 uid（缺省以 name 为身份，重命名后 drift 不可追踪）")
        source = evidence_source(e)
        if e.get("evidence") is not None and source is None:
            rep.warn("W12", where,
                     f"evidence.source 非法（∈ {sorted(EVIDENCE_SOURCES)}），可视化将忽略证据着色")
    for e in entities:
        name, parent = e.get("name"), e.get("is_a")
        if parent is not None and parent not in ent_names:
            rep.error("E12", f"ontology.entity[{name}]", f"is_a 指向未声明实体 {parent!r}")
    # is_a 环检测（静态结构检查，不是推理）
    parent_of = {e.get("name"): e.get("is_a") for e in entities if e.get("name")}
    for start in parent_of:
        seen, node = set(), start
        while node in parent_of and parent_of[node]:
            node = parent_of[node]
            if node in seen or node == start:
                rep.error("E12", f"ontology.entity[{start}]", "is_a 成环")
                break
            seen.add(node)
    rel_ids = set()
    for r in relations:
        rid = ont_relation_id(r)
        where = f"ontology.relation[{rid}]"
        if rid in rel_ids:
            rep.error("E11", where, "本体关系 id 重复（平行边请显式给 id）")
        rel_ids.add(rid)
        for ep in (r.get("from"), r.get("to")):
            if ep not in ent_names:
                rep.error("E13", where, f"端点 {ep!r} 不是已声明本体实体")
        if not r.get("predicate"):
            rep.error("E13", where, "缺 predicate（语义谓词是关系的核心，键只是落地方式之一）")
        mapping = r.get("mapping")
        if mapping not in MAPPINGS:
            rep.error("E13", where, f"mapping 非法：{mapping!r}（∈ {sorted(MAPPINGS)}）")
        elif mapping != "equi_key" and not r.get("note"):
            rep.error("E13", where, "mapping≠equi_key 必须写 note（无键关系的落地说明）")
    # 投影对账（ontology_ref 接受实体 name 或 uid 两种写法，内部统一归一为 name）
    ent_refs = ent_names | set(uid2name)
    projected_entities = set()
    for d in datasets:
        ref = d.get("ontology_ref")
        if ref:
            if ref not in ent_refs:
                rep.error("E14", f"dataset[{d.get('name','?')}]", f"ontology_ref 指向未声明实体 {ref!r}")
            projected_entities.add(uid2name.get(ref, ref))
    ont_rel_by_id = {ont_relation_id(r): r for r in relations}
    projected_rel_ids = set()
    for r in contract_rels:
        ref = r.get("ontology_ref")
        if not ref:
            continue
        where = f"relationship[{r.get('from','?')}→{r.get('to','?')}]"
        target = ont_rel_by_id.get(ref)
        if target is None:
            rep.error("E14", where, f"ontology_ref 指向未声明本体关系 {ref!r}")
        elif target.get("mapping") != "equi_key":
            rep.error("E15", where,
                      f"无键关系不得投影：{ref!r} 的 mapping={target.get('mapping')!r}，合同只承载 equi_key")
        projected_rel_ids.add(ref)
    for e in entities:
        name = e.get("name")
        if name and name not in projected_entities and not e.get("unprojected_reason"):
            rep.warn("W07", f"ontology.entity[{name}]",
                     "未被任何数据集投影且未写 unprojected_reason")
    for r in relations:
        rid = ont_relation_id(r)
        if r.get("mapping") == "equi_key" and rid not in projected_rel_ids:
            rep.warn("W08", f"ontology.relation[{rid}]", "equi_key 关系未被任何合同关系投影")


def check_metrics(m, rep, ds_index):
    from _sql import metric_dependencies
    seen = set()
    for mt in m.get("metrics", []) or []:
        mid = mt.get("id", "?")
        where = f"metric[{mid}]"
        if mid in seen:
            rep.error("E11", where, "指标 id 重复")
        seen.add(mid)

        dsn = mt.get("dataset")
        ds = ds_index.get(dsn)
        if mt.get("structured") and not dsn:
            rep.error("E08", where, "structured 指标缺 dataset 挂载")
        if dsn and ds is None:
            rep.error("E08", where, f"挂载的数据集 {dsn!r} 不存在")
        tf = mt.get("time_field")
        if ds is not None and tf and tf not in field_names(ds):
            rep.error("E08", where, f"time_field {tf!r} 不在 {dsn} 的字段中")

        expr = mt.get("expr") or ""
        num = (mt.get("numerator") or {}).get("expr", "")
        den = (mt.get("denominator") or {}).get("expr", "")
        if mt.get("structured"):
            # 编译强制只针对已结构化指标；未结构化指标保留 legacy 口径式，属"暂不落地"状态
            if mt.get("type") == "ratio":
                if not (num and den) and "/" not in expr:
                    rep.error("E05", where, "ratio 缺分子/分母（numerator/denominator 或含 / 的 expr）")
                if re.search(r"\bAVG\s*\(", " ".join([expr, num, den]), re.I):
                    rep.error("E06", where, "ratio 含 AVG( —— 禁行级平均，必须 SUM/SUM 加权")
            if den:
                policy = mt.get("on_zero_denominator")
                if policy is None:
                    rep.warn("W11", where, "有分母但未声明 on_zero_denominator（缺省 null 会把除零静默变 NULL）")
                elif policy not in {"null", "zero", "error"}:
                    rep.error("E17", where, f"on_zero_denominator 非法：{policy!r}（∈ null/zero/error）")
            if not (expr or num):
                rep.error("E07", where, "structured 指标缺 expr 且缺分子分母（口径未自含）")
            if ds is not None and (expr or num):
                dependencies = metric_dependencies(mt, ds)
                if dependencies.get("error"):
                    if dependencies.get("error_kind") in {"unknown_field", "invalid_aggregate"}:
                        rep.error("E19", where, dependencies["error"])
                    else:
                        rep.warn("W19", where,
                                 "本地单表依赖校验未完成，不据此判定业务口径非法：" + dependencies["error"])
            if not tf and mt.get('time_requirement') != 'current':
                rep.warn("W04", where, "尚未明确当前状态或统计时间字段；当前状态可声明 time_requirement: current")
            if mt.get("status") == "草案":
                rep.warn("W05", where, "structured 指标仍为 草案 状态，验收后改 已发布")
            for flt in mt.get("filters", []) or []:
                if ds is not None and isinstance(flt, dict) and flt.get("field") in field_names(ds):
                    _check_values_in_enum(rep, f"{where}.filters[{flt['field']}]",
                                          ds, flt["field"], flt.get("values"))
            if mt.get("type") == "ratio" and str(mt.get("unit", "")).strip() in {"%", "％", "百分比"} \
                    and mt.get("display_scale") is None:
                rep.warn("W15", where,
                         "unit 为 % 的 ratio 编译值是 0–1 分数；未声明 display_scale（如 100），×100 展示责任未落地")
            syns = mt.get("synonyms") or []
            if mt.get("status") != "停用" and len(syns) < 3:
                rep.warn("W17", where,
                         f"同义词仅 {len(syns)} 个（<3）：同义词是指标命中路由的生命线，"
                         "用户问法命中不了就会掉进慢速 NL2SQL 路径，请补到 3 个以上")


def check_templates(m, rep, ds_index):
    """明细查询模板（一等资产）：结构非法 E18，缺时间围栏/同义词 W18。"""
    seen = set()
    for t in m.get("templates", []) or []:
        tid = t.get("id", "?")
        where = f"template[{tid}]"
        if tid in seen:
            rep.error("E18", where, "模板 id 重复")
        seen.add(tid)
        ds = ds_index.get(t.get("dataset"))
        if ds is None:
            rep.error("E18", where, f"挂载的数据集 {t.get('dataset')!r} 不存在")
        else:
            fnames = field_names(ds)
            for c in t.get("columns", []) or []:
                if c not in fnames:
                    rep.error("E18", where, f"columns 引用了数据集没有的字段 {c!r}")
            tf = t.get("time_field")
            if tf and tf not in fnames:
                rep.error("E18", where, f"time_field {tf!r} 不在数据集字段中")
            if not tf and t.get('time_requirement') != 'current':
                rep.warn("W18", where, "尚未明确当前状态或统计时间字段；当前状态可声明 time_requirement: current")
        if t.get("status") != "停用" and len(t.get("synonyms") or []) < 3:
            rep.warn("W18", where, "同义词 <3 个（明细模板同样靠同义词命中路由）")


def model_index(m):
    """按稳定身份索引全部可维护对象。身份优先级：uid > id > name/term/relation_id。"""
    from _contract import (keys, ont_entities, ont_entity_id, ont_relations,
                           ont_relation_id, relation_id)
    idx = {}
    for d in m.get("datasets", []) or []:
        idx[("dataset", d.get("name"))] = d
    for mt in m.get("metrics", []) or []:
        idx[("metric", mt.get("id"))] = mt
    for t in m.get("templates", []) or []:
        idx[("template", t.get("id"))] = t
    for r in m.get("relationships", []) or []:
        idx[("relationship", relation_id(r))] = r
    for c in m.get("concepts", []) or []:
        idx[("concept", c.get("term"))] = c
    for e in ont_entities(m):
        idx[("ontology_entity", ont_entity_id(e))] = e
    for r in ont_relations(m):
        idx[("ontology_relation", ont_relation_id(r))] = r
    return {k: v for k, v in idx.items() if k[1]}


def drift_report(current, baseline):
    """四级 drift 分类。breaking = 会破坏现有消费者的变更（删除被引用对象、改主键/粒度/映射）。"""
    from _contract import keys, object_digest
    from _sql import metric_dependencies
    cur, base = model_index(current), model_index(baseline)
    added = sorted(k for k in cur if k not in base)
    removed = sorted(k for k in base if k not in cur)
    changed = sorted(k for k in cur if k in base
                     and object_digest(cur[k]) != object_digest(base[k]))
    breaking = []
    cur_ds = {d.get("name"): d for d in current.get("datasets", []) or []}
    cur_ents = {e.get("name") for e in (current.get("ontology") or {}).get("entities", []) or []}
    removed_names = {k for k in removed}

    def broke(kind, key, reason):
        breaking.append({"kind": kind, "key": key, "reason": reason})

    for kind, key in removed:
        if kind == "dataset":
            for mt in current.get("metrics", []) or []:
                if mt.get("dataset") == key:
                    broke(kind, key, f"数据集已删除但指标 {mt.get('id')} 仍挂载")
            for t in current.get("templates", []) or []:
                if t.get("dataset") == key:
                    broke(kind, key, f"数据集已删除但明细模板 {t.get('id')} 仍挂载")
            for r in current.get("relationships", []) or []:
                if key in (r.get("from"), r.get("to")):
                    broke(kind, key, "数据集已删除但仍是合同关系端点")
        if kind == "ontology_entity":
            base_ent = base[("ontology_entity", key)]
            for d in current.get("datasets", []) or []:
                if d.get("ontology_ref") in {key, base_ent.get("name")}:
                    broke(kind, key, f"实体已删除但数据集 {d.get('name')} 仍投影它")
        if kind == "ontology_relation":
            for r in current.get("relationships", []) or []:
                if r.get("ontology_ref") == key:
                    broke(kind, key, "本体关系已删除但合同关系仍回指")
    for kind, key in changed:
        before, after = base[(kind, key)], cur[(kind, key)]
        if kind == "dataset":
            if before.get("primary_key") != after.get("primary_key"):
                broke(kind, key, "primary_key 变更（去重与 join 依据改变）")
            if before.get("grain") != after.get("grain"):
                broke(kind, key, "grain 粒度变更（所有聚合口径失效）")
            lost = {f.get("name") for f in before.get("fields", []) or []} - \
                   {f.get("name") for f in after.get("fields", []) or []}
            for mt in current.get("metrics", []) or []:
                if mt.get("dataset") != key:
                    continue
                if mt.get("time_field") in lost:
                    broke(kind, key, f"字段 {mt.get('time_field')} 已删但指标 {mt.get('id')} 用作 time_field")
                if lost and mt.get("structured"):
                    # Analyze the current expression against both schemas so removed
                    # fields remain resolvable. A changed metric that no longer uses
                    # them must not be marked breaking. Literals are not references.
                    known_fields = {f.get("name"): f for f in before.get("fields", []) or []}
                    known_fields.update({f.get("name"): f for f in after.get("fields", []) or []})
                    dependency_ds = dict(after, fields=list(known_fields.values()))
                    dependencies = metric_dependencies(mt, dependency_ds)
                    if not dependencies.get("error"):
                        removed_refs = lost & set(dependencies["fields"])
                        if removed_refs:
                            broke(kind, key,
                                  f"字段 {', '.join(sorted(removed_refs))} 已删但指标 {mt.get('id')} "
                                  "的表达式或过滤仍引用（按单表编译依赖核对）")
        if kind == "ontology_relation" and before.get("mapping") != after.get("mapping"):
            if before.get("mapping") == "equi_key":
                broke(kind, key, f"mapping 由 equi_key 变为 {after.get('mapping')!r}（已投影关系失去落地键）")
        if kind == "ontology_entity" and before.get("name") != after.get("name"):
            if before.get("name") not in cur_ents:
                for d in current.get("datasets", []) or []:
                    if d.get("ontology_ref") == before.get("name"):
                        broke(kind, key, f"实体重命名 {before.get('name')!r}→{after.get('name')!r} "
                                         f"但数据集 {d.get('name')} 仍按旧名投影（uid 保住了身份，引用要跟着改）")
    return {"schema_version": "1.0", "baseline_objects": len(base), "current_objects": len(cur),
            "added": [{"kind": k, "key": v} for k, v in added],
            "removed": [{"kind": k, "key": v} for k, v in removed],
            "changed": [{"kind": k, "key": v} for k, v in changed],
            "breaking": breaking}


def append_history(path, model_path, m, rep):
    import json as _json
    from _contract import digest, now
    by_code = {}
    for line in rep.errors + rep.warnings:
        code = line.split("]", 1)[0].split()[-1]
        by_code[code] = by_code.get(code, 0) + 1
    record = {"at": now(), "model_sha256": digest(model_path),
              "model_version": m.get("version"),
              "errors": len(rep.errors), "warnings": len(rep.warnings), "by_code": by_code}
    with open(path, "a", encoding="utf-8") as stream:
        stream.write(_json.dumps(record, ensure_ascii=False) + "\n")
    return record
def main():
    ap = argparse.ArgumentParser(description="semantic.yaml 铁律 lint")
    ap.add_argument("-f", "--file", required=True)
    ap.add_argument("--strict", action="store_true", help="WARN 也视为失败")
    ap.add_argument("--drift", help="基线 semantic.yaml：输出新增/删除/变更/破坏四级分类")
    ap.add_argument("--drift-report", help="drift 结果 JSON 输出路径")
    ap.add_argument("--history", help="追加一条质量记录到 JSONL（release 趋势用）")
    args = ap.parse_args()

    m = load(args.file) or {}
    rep = Reporter()
    from _contract import top_shape_error
    shape_err = top_shape_error(m)
    if shape_err:
        print(f"[ERROR E00] {shape_err}")
        return 1
    if not m.get("datasets"):
        if (m.get("ontology") or {}).get("entities"):
            rep.warn("W14", "model", "无 datasets 的纯本体草案：仅做本体结构检查，"
                     "投影对账与合同检查不适用（先业务后物理的合法中间态）")
        else:
            print("[ERROR E00] 模型必须包含非空 datasets"
                  "（或先以 ontology.entities 声明业务对象，进入纯本体草案态）")
            return 1
    ds_index = {d.get("name"): d for d in m.get("datasets", []) or []}

    check_datasets(m, rep)
    check_relationships(m, rep, set(ds_index))
    check_concepts(m, rep, ds_index)
    check_metrics(m, rep, ds_index)
    check_templates(m, rep, ds_index)
    check_ontology(m, rep)

    for line in rep.errors + rep.warnings:
        print(line)
    from _contract import ont_entities, ont_relations
    print(f"\nlint 结果：{len(rep.errors)} ERROR / {len(rep.warnings)} WARN"
          f"（数据集 {len(ds_index)}，关系 {len(m.get('relationships', []) or [])}，"
          f"概念 {len(m.get('concepts', []) or [])}，指标 {len(m.get('metrics', []) or [])}，"
          f"模板 {len(m.get('templates', []) or [])}，"
          f"本体实体 {len(ont_entities(m))}，本体关系 {len(ont_relations(m))}）")
    exit_code = 0
    if rep.errors or (args.strict and rep.warnings):
        print("门禁：未通过")
        exit_code = 1
    else:
        print("门禁：通过")
    if args.drift:
        baseline = load(args.drift) or {}
        drift = drift_report(m, baseline)
        print(f"\ndrift：+{len(drift['added'])} 新增 / -{len(drift['removed'])} 删除 / "
              f"~{len(drift['changed'])} 变更 / !{len(drift['breaking'])} 破坏")
        for cls, mark in (("added", "+"), ("removed", "-"), ("changed", "~")):
            for item in drift[cls]:
                print(f"  {mark} {item['kind']}[{item['key']}]")
        for item in drift["breaking"]:
            print(f"  ! {item['kind']}[{item['key']}] —— {item['reason']}")
        if args.drift_report:
            from _contract import write
            write(args.drift_report, drift)
        if drift["breaking"]:
            print("drift 门禁：存在破坏性变更")
            exit_code = 1
    if args.history:
        record = append_history(args.history, args.file, m, rep)
        print(f"质量记录已追加 → {args.history}（{record['errors']} ERROR / {record['warnings']} WARN）")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
