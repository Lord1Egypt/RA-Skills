#!/usr/bin/env python3
"""patch_model.py — semantic.yaml 幂等补丁器（ai-data-delivery v0.0.9）

权威源 Schema（semantic.yaml，唯一事实源）：
  datasets[]:       name / display_name / source(物理表) / grain / primary_key
                    / ai{instructions, synonyms[]} / tenant_field
                    / fields[]{name,cn,role(pk|fk|dim|measure|time|attr),type,enum,sensitive,synonyms}
  concepts[]:       term / aliases[] / expand{dataset,field,values[] | union[]} / note
  relationships[]:  from / to / type / join_key / cardinality / traversable / note
  metrics[]:        id / name / type(count|ratio|sum|avg|list) / structured / dataset
                    / expr / numerator{expr,dialect} / denominator{expr,dialect}
                    / extra_where / time_field / unit / grain
                    / caliber{note,basis} / synonyms[] / status
  ontology:         entities[]{name,uid,...} / relations[]

五个子命令（全部幂等：内容无变化时不写盘；写盘为原子写：tmp + os.replace，
Windows 安全软件偶发拦写时自动重试一次）：

  syn    补同义词（自然问法）。三类目标：
           python patch_model.py -f semantic.yaml syn 指标ID 词1 词2 ...
           python patch_model.py -f semantic.yaml syn --dataset 数据集名 词1 词2 ...
           python patch_model.py -f semantic.yaml syn --concept 概念名 词1 词2 ...

  struct 结构化指标（自含全口径：expr/分子分母 + extra_where + time_field）：
           python patch_model.py -f semantic.yaml struct 指标ID \
               --expr "COUNT(*)" --extra-where "rectify_status = '待整改'" \
               --time-field stat_date --unit 条 \
               --caliber-note "待整改重大隐患" --caliber-basis "内部约定" \
               --synonym 自然问法1 --synonym 自然问法2
           新建指标（默认必须已存在，防笔误造重复指标）：
               ... struct 新ID --create --name 指标名 --type count --dataset 数据集 ...
           ratio 型用 --numerator/--denominator（禁止行级平均）：
               ... struct 指标ID --numerator "SUM(a)" --denominator "SUM(b)"

  set    改键值：
           python patch_model.py -f semantic.yaml set 指标ID --key extra_where --value "..."
           python patch_model.py -f semantic.yaml set --path engine.timezone --value Asia/Shanghai

  batch  批量补丁（ops.yaml 一次写入，避免逐条整文件重写）：
           python patch_model.py -f semantic.yaml batch ops.yaml [--db 物理库.db]
           ops.yaml 格式：
             ops:
               - op: syn
                 metric: 指标ID          # 三选一：metric / dataset / concept
                 words: [词1, 词2]
               - op: struct
                 id: 指标ID
                 create: true            # 新建时需提供 name/type/dataset
                 name: 指标名
                 type: count
                 dataset: 数据集
                 expr: "COUNT(*)"
                 extra_where: "..."
                 time_field: stat_date
                 unit: 条
                 synonyms: [词1, 词2]
               - op: set
                 metric: 指标ID          # 或 path: engine.timezone
                 key: extra_where
                 value: "..."
               - op: set_uid
                 entity: 企业
                 uid: ent_enterprise
           逐条应用、单条失败跳过并继续，最后汇总；任一失败退出码 1。
           --db 作用于所有未自带 db 的 struct op（写入口径前逐条验算）。

  fixuid 给缺 uid 的本体实体补稳定身份（drift/历史可追踪的前提）：
           python patch_model.py -f semantic.yaml fixuid [--map uid_map.yaml]
           --map 格式：{实体name: uid}；未命中映射的实体用内置词表（企业→enterprise 等），
           再未命中回退 ent_<sha1前6位>。全部逐条打印，请人工审阅后再提交。

提供 --db 时编译完整单表口径并检查可执行性；提供 --expect 时再对拍期望。
错误/NULL 拒绝写入（--force 会绕过，不能作为验证证据）；零值本身不是错误。
未提供 --db 时只生成草案并提醒未验证。

注意：PyYAML 重写会丢失原文件注释，重要注释请迁移到 caliber.note / description 字段；
batch 模式把多次重写收敛为一次，是把注释损失降到最小的推荐用法。
"""
import argparse
import copy
import os
import re
import sys
import time

import yaml

from _contract import load as _contract_load


# ---------- 基础读写 ----------

def load(path):
    return _contract_load(path) or {}


def dump_if_changed(path, before, after):
    if before == after:
        print("no change（已是最新，幂等跳过）")
        return False
    import shutil
    backup = path + ".bak"
    shutil.copyfile(path, backup)
    payload = yaml.safe_dump(after, allow_unicode=True, sort_keys=False,
                             default_flow_style=False, width=120)
    # 原子写：先写临时文件再 os.replace，避免半写文件；Windows 安全软件偶发
    # 拦写（OSError 22）时等待后重试一次。
    tmp = path + ".tmp"
    last = None
    for attempt in (0, 1):
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(payload)
            os.replace(tmp, path)
            last = None
            break
        except OSError as e:
            last = e
            if attempt == 0:
                time.sleep(0.6)
    if last is not None:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except OSError:
            pass
        raise last
    print(f"patched ✓（原文已备份 → {backup}）")
    return True


def err(msg):
    print(f"错误：{msg}", file=sys.stderr)
    return 1


def find_one(items, key, value):
    for item in items or []:
        if isinstance(item, dict) and item.get(key) == value:
            return item
    return None


def merge_synonyms(existing, new_words):
    """保序去重合并：已有顺序不动，新词追加。"""
    out = list(existing or [])
    added = []
    for w in new_words:
        if w not in out:
            out.append(w)
            added.append(w)
    return out, added


# ---------- 物理库验算 ----------

def compile_full_sql(model, mt):
    """指标完整口径（expr/分子分母 + filters + extra_where）→ 可执行 SQL。返回 (sql, err)。"""
    from _sql import compile_single
    ds = find_one(model.get("datasets"), "name", mt.get("dataset"))
    return compile_single(mt, ds)


def verify_with_db(db_path, model, mt, expect=None, tol=1e-6):
    """对物理库验算 patched 后的完整口径。返回 (ok, detail)。
    给了 --expect 就对拍数值；没给只证明可执行且非 NULL，不证明业务正确。"""
    sql, err_ = compile_full_sql(model, mt)
    if err_:
        return False, err_
    try:
        from _contract import readonly
        conn = readonly(db_path)
        row = conn.execute(sql).fetchone()
        conn.close()
    except Exception as e:
        return False, f"验算 SQL 执行失败：{e}\n  SQL: {sql}"
    v = row[0] if row else None
    if v is None:
        return False, f"验算结果为 NULL（口径可能过严或枚举值写错）\n  SQL: {sql}"
    if expect is not None:
        try:
            ok = abs(float(v) - float(expect)) <= tol
        except (TypeError, ValueError):
            return False, f"验算结果 {v!r} 非数值，无法与 --expect {expect} 对拍\n  SQL: {sql}"
        if not ok:
            return False, (f"验算对拍失败：实算 {v} ≠ 期望 {expect}（容差 {tol}）\n  SQL: {sql}\n"
                           "  口径改错了还是金标准变了？先确认再 --force")
        return True, f"验算对拍通过：{v} ≈ {expect}\n  SQL: {sql}"
    return True, f"可执行性检查通过：值 {v}；未提供 --expect，业务口径正确性未验证\n  SQL: {sql}"


# ---------- 核心操作（原地改 data，返回退出码；供 CLI 与 batch 复用） ----------

def apply_syn(data, target, words, dataset=False, concept=False):
    if not words:
        return err("syn 需要一个以上同义词（位置参数或 --synonym）")
    if dataset:
        ds = find_one(data.get("datasets"), "name", target)
        if ds is None:
            return err(f"数据集 {target!r} 不存在于 datasets")
        syns = ds.setdefault("ai", {}).setdefault("synonyms", [])
        merged, added = merge_synonyms(syns, words)
        ds["ai"]["synonyms"] = merged
        print(f"数据集 {target!r} 新增同义词 {added}" if added else "同义词已存在")
    elif concept:
        c = find_one(data.get("concepts"), "term", target)
        if c is None:
            return err(f"概念 {target!r} 不存在于 concepts")
        merged, added = merge_synonyms(c.setdefault("aliases", []), words)
        c["aliases"] = merged
        print(f"概念 {target!r} 新增别名 {added}" if added else "别名已存在")
    else:
        m = find_one(data.get("metrics"), "id", target)
        if m is None:
            return err(f"指标 {target!r} 不存在于 metrics（按 id 寻址；数据集用 --dataset，概念用 --concept）")
        merged, added = merge_synonyms(m.setdefault("synonyms", []), words)
        m["synonyms"] = merged
        print(f"指标 {target!r} 新增同义词 {added}" if added else "同义词已存在")
    return 0


def apply_struct(data, target, *, expr=None, numerator=None, denominator=None,
                 extra_where=None, time_field=None, unit=None, grain=None,
                 caliber_note=None, caliber_basis=None, synonyms=None,
                 create=False, name=None, type_=None, dataset=None,
                 db=None, expect=None, tol=1e-6, force=False):
    """结构化指标。返回 (exit_code, ok)；调用方负责 dump。"""
    metrics = data.setdefault("metrics", [])
    m = find_one(metrics, "id", target)

    if m is None:
        if not create:
            return err(f"指标 {target!r} 不存在；确认 id 后重试，或显式加 --create 新建"), False
        missing = [k for k, v in (("name", name), ("type", type_), ("dataset", dataset)) if not v]
        if missing:
            return err(f"--create 需提供 --name/--type/--dataset，缺：{missing}"), False
        if find_one(data.get("datasets"), "name", dataset) is None:
            return err(f"数据集 {dataset!r} 不存在，先建数据集再挂指标"), False
        m = {"id": target, "name": name, "type": type_,
             "dataset": dataset, "status": "草案", "synonyms": []}
        metrics.append(m)
        print(f"新建指标 {target!r}（status=草案，验收后改 已发布）")

    before_m = copy.deepcopy(m)

    # 幂等写入（先改内存副本，验算不过不落盘）
    m["structured"] = True
    if expr:
        m["expr"] = expr
        m.pop("numerator", None)
        m.pop("denominator", None)
    if numerator or denominator:
        if not (numerator and denominator):
            return err("ratio 口径必须同时给 --numerator 与 --denominator（禁行级平均）"), False
        m["numerator"] = {"expr": numerator, "dialect": "ANSI_SQL"}
        m["denominator"] = {"expr": denominator, "dialect": "ANSI_SQL"}
        m.pop("expr", None)
    if extra_where is not None:
        m["extra_where"] = extra_where
    if time_field:
        m["time_field"] = time_field
    if unit:
        m["unit"] = unit
    if grain:
        m["grain"] = grain
    if caliber_note or caliber_basis:
        cal = m.setdefault("caliber", {})
        if caliber_note:
            cal["note"] = caliber_note
        if caliber_basis:
            cal["basis"] = caliber_basis
    if synonyms:
        merged, added = merge_synonyms(m.get("synonyms"), synonyms)
        m["synonyms"] = merged
        if added:
            print(f"同步补充同义词 {added}")

    if not (m.get("expr") or m.get("numerator")):
        return err("结构化指标必须提供 --expr 或 --numerator/--denominator"), False
    if m.get("type") == "ratio":
        expr_text = " ".join([m.get("expr", ""),
                              (m.get("numerator") or {}).get("expr", ""),
                              (m.get("denominator") or {}).get("expr", "")])
        if re.search(r"\bAVG\s*\(", expr_text, re.I):
            return err("ratio 指标禁止行级平均（DEC-METRIC-01）：请用 SUM/SUM 分子分母"), False

    # 验算（铁律：写口径前必须验算；验算对象是 patched 后的完整口径——filters + extra_where 全量）
    if db:
        ok, detail = verify_with_db(db, data, m, expect=expect, tol=tol)
        print(detail)
        if not ok and not force:
            print("验算未通过，拒绝写入（确认无误后加 --force 强制写入）", file=sys.stderr)
            return 2, False
        if not ok:
            print("warning：--force 生效，验算未通过仍写入（必须在交付说明中声明）", file=sys.stderr)
    else:
        print("提醒：未提供 --db，本次口径写入未经物理库验算——交付前必须补验算并留痕", file=sys.stderr)
    print("边界声明：验算只保证口径可执行且非 NULL（或与 --expect 对拍一致）；"
          "口径语义正确性仍须金标准用例 run_eval 定向回归把关。")

    if m != before_m:
        m["status"] = "草案"
    n = sum(1 for t in metrics if t.get("structured"))
    print(f"structured: {n}/{len(metrics)}")
    return 0, True


def apply_set(data, target=None, key=None, path=None, value=None):
    try:
        parsed = yaml.safe_load(value) if isinstance(value, str) else value
    except yaml.YAMLError:
        parsed = value

    if path:
        keys = path.split(".")
        node = data
        for k in keys[:-1]:
            nxt = node.get(k)
            if not isinstance(nxt, dict):
                nxt = {}
                node[k] = nxt
            node = nxt
        node[keys[-1]] = parsed
        print(f"set {path} = {parsed!r}")
    else:
        if not key:
            return err("set 指标键值需要 --key 与 --value；全局点路径用 --path")
        m = find_one(data.get("metrics"), "id", target)
        if m is None:
            return err(f"指标 {target!r} 不存在")
        m[key] = parsed
        print(f"set {target}.{key} = {parsed!r}")
    return 0


# 内置实体 name → uid 词表（fixuid 用；命不中再回退哈希）
UID_VOCAB = {
    "企业": "enterprise", "公司": "company", "车辆": "vehicle", "人员": "person",
    "驾驶人": "driver", "驾驶员": "driver", "组织": "organization", "机构": "organization",
    "道路": "road", "路段": "road_section", "设备": "device", "设施": "facility",
    "事件": "event", "事故": "accident", "隐患": "hazard", "客户": "customer",
    "产品": "product", "订单": "order", "工单": "work_order", "员工": "employee",
    "部门": "department", "项目": "project", "合同": "contract", "供应商": "supplier",
    "学生": "student", "课程": "course", "学校": "school", "患者": "patient",
    "医生": "doctor", "科室": "department", "门店": "store", "商品": "goods",
    "用户": "user", "账户": "account", "案件": "case", "警情": "incident",
}


def apply_fixuid(data, uid_map=None, quiet=False):
    """给缺 uid 的本体实体补稳定身份。返回 (exit_code, [(name, uid, 来源)])。
    只读不写盘；调用方负责 dump。"""
    import hashlib
    from _contract import ont_entities
    uid_map = uid_map or {}
    taken = {e.get("uid") for e in ont_entities(data) if e.get("uid")}
    assigned = []
    for e in ont_entities(data):
        if e.get("uid") or not e.get("name"):
            continue
        name = e["name"]
        src = "map"
        uid = uid_map.get(name)
        if not uid:
            eng = UID_VOCAB.get(name)
            uid = f"ent_{eng}" if eng else None
            src = "内置词表" if eng else "哈希回退"
        if not uid:
            uid = f"ent_{hashlib.sha1(name.encode('utf-8')).hexdigest()[:6]}"
        if uid in taken:  # 撞车则加哈希后缀保唯一
            uid = f"{uid}_{hashlib.sha1(name.encode('utf-8')).hexdigest()[:4]}"
            src += "+去重"
        taken.add(uid)
        e["uid"] = uid
        assigned.append((name, uid, src))
        if not quiet:
            print(f"实体 {name!r} → uid {uid!r}（{src}）")
    if not assigned and not quiet:
        print("所有实体均已有 uid，无需处理")
    return 0, assigned


# ---------- 子命令 ----------

def cmd_syn(args):
    data = load(args.file)
    before = copy.deepcopy(data)
    words = list(args.words or []) + list(args.synonym or [])
    rc = apply_syn(data, args.target, words, dataset=args.dataset, concept=args.concept)
    if rc:
        return rc
    dump_if_changed(args.file, before, data)
    return 0


def cmd_struct(args):
    data = load(args.file)
    before = copy.deepcopy(data)
    rc, _ok = apply_struct(
        data, args.target, expr=args.expr, numerator=args.numerator,
        denominator=args.denominator, extra_where=args.extra_where,
        time_field=args.time_field, unit=args.unit, grain=args.grain,
        caliber_note=args.caliber_note, caliber_basis=args.caliber_basis,
        synonyms=list(args.synonym or []), create=args.create, name=args.name,
        type_=args.type, dataset=args.dataset, db=args.db, expect=args.expect,
        tol=args.tol, force=args.force)
    if rc:
        return rc
    dump_if_changed(args.file, before, data)
    return 0


def cmd_set(args):
    data = load(args.file)
    before = copy.deepcopy(data)
    rc = apply_set(data, target=args.target, key=args.key, path=args.path, value=args.value)
    if rc:
        return rc
    dump_if_changed(args.file, before, data)
    return 0


def cmd_batch(args):
    ops_doc = load(args.ops)
    ops = ops_doc.get("ops")
    if not isinstance(ops, list) or not ops:
        return err(f"{args.ops} 缺 ops 列表")
    data = load(args.file)
    before = copy.deepcopy(data)
    ok_n, fail = 0, []
    for i, op in enumerate(ops, 1):
        if not isinstance(op, dict) or "op" not in op:
            fail.append((i, "缺 op 字段"))
            print(f"[{i}/{len(ops)}] ✗ 缺 op 字段", file=sys.stderr)
            continue
        kind = op["op"]
        snap = copy.deepcopy(data)
        print(f"[{i}/{len(ops)}] op={kind}", end=" ")
        if kind == "syn":
            target = op.get("metric") or op.get("dataset") or op.get("concept")
            words = list(op.get("words") or []) + list(op.get("synonyms") or [])
            rc = apply_syn(data, target, words,
                           dataset=bool(op.get("dataset")), concept=bool(op.get("concept")))
            if rc:
                data = snap
                fail.append((i, f"syn {target!r} 失败"))
                continue
        elif kind == "struct":
            rc, applied = apply_struct(
                data, op.get("id"), expr=op.get("expr"), numerator=op.get("numerator"),
                denominator=op.get("denominator"), extra_where=op.get("extra_where"),
                time_field=op.get("time_field"), unit=op.get("unit"), grain=op.get("grain"),
                caliber_note=op.get("caliber_note"), caliber_basis=op.get("caliber_basis"),
                synonyms=list(op.get("synonyms") or []), create=bool(op.get("create")),
                name=op.get("name"), type_=op.get("type"), dataset=op.get("dataset"),
                db=op.get("db") or args.db, expect=op.get("expect"),
                tol=float(op.get("tol", 1e-6)), force=bool(op.get("force")))
            if not applied:
                data = snap
                fail.append((i, f"struct {op.get('id')!r} 失败/被拒"))
                continue
        elif kind == "set":
            rc = apply_set(data, target=op.get("metric"), key=op.get("key"),
                           path=op.get("path"), value=op.get("value"))
            if rc:
                data = snap
                fail.append((i, "set 失败"))
                continue
        elif kind == "set_uid":
            ent_name, uid = op.get("entity"), op.get("uid")
            if not ent_name or not uid:
                data = snap
                fail.append((i, "set_uid 缺 entity/uid"))
                print("✗ set_uid 缺 entity/uid", file=sys.stderr)
                continue
            from _contract import ont_entities
            ent = find_one(ont_entities(data), "name", ent_name)
            if ent is None:
                data = snap
                fail.append((i, f"set_uid 实体 {ent_name!r} 不存在"))
                print(f"✗ 实体 {ent_name!r} 不存在", file=sys.stderr)
                continue
            ent["uid"] = uid
            print(f"实体 {ent_name!r} → uid {uid!r}")
        else:
            fail.append((i, f"未知 op {kind!r}"))
            print(f"✗ 未知 op {kind!r}", file=sys.stderr)
            continue
        ok_n += 1
    print(f"\nbatch 汇总：{ok_n}/{len(ops)} 条应用成功" +
          (f"；失败 {len(fail)} 条：{[f'#{i} {m}' for i, m in fail]}" if fail else ""))
    dump_if_changed(args.file, before, data)
    return 1 if fail else 0


def cmd_fixuid(args):
    uid_map = {}
    if args.map:
        uid_map = load(args.map)
        if not isinstance(uid_map, dict):
            return err(f"{args.map} 应为 {{实体name: uid}} 映射")
    data = load(args.file)
    before = copy.deepcopy(data)
    _rc, assigned = apply_fixuid(data, uid_map=uid_map)
    if assigned:
        print("请人工审阅以上 uid 分配（uid 是稳定身份，一旦发布不要改）", file=sys.stderr)
    dump_if_changed(args.file, before, data)
    return 0


def main():
    ap = argparse.ArgumentParser(description="semantic.yaml 幂等补丁器（v0.0.9）")
    ap.add_argument("-f", "--file", required=True, help="semantic.yaml 路径")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("syn", help="补同义词（指标/数据集/概念）")
    p.add_argument("target", help="指标 id；或配合 --dataset/--concept 的目标名")
    p.add_argument("words", nargs="*")
    p.add_argument("--dataset", action="store_true", help="target 按数据集名解析")
    p.add_argument("--concept", action="store_true", help="target 按概念 term 解析")
    p.add_argument("--synonym", action="append", default=[])
    p.set_defaults(fn=cmd_syn)

    p = sub.add_parser("struct", help="结构化指标（自含全口径）")
    p.add_argument("target", help="指标 id")
    p.add_argument("--expr", default=None)
    p.add_argument("--numerator", default=None, help="ratio 分子表达式")
    p.add_argument("--denominator", default=None, help="ratio 分母表达式")
    p.add_argument("--extra-where", dest="extra_where", default=None)
    p.add_argument("--time-field", dest="time_field", default=None)
    p.add_argument("--unit", default=None)
    p.add_argument("--grain", default=None)
    p.add_argument("--caliber-note", dest="caliber_note", default=None)
    p.add_argument("--caliber-basis", dest="caliber_basis", default=None)
    p.add_argument("--synonym", action="append", default=[])
    p.add_argument("--create", action="store_true", help="指标不存在时新建（需 --name/--type/--dataset）")
    p.add_argument("--name", default=None)
    p.add_argument("--type", default=None)
    p.add_argument("--dataset", default=None)
    p.add_argument("--db", default=None, help="物理库（sqlite）路径：写入前自动验算完整口径")
    p.add_argument("--expect", default=None,
                   help="期望值对拍：验算结果与之一致才允许写入（如金标准值 15）")
    p.add_argument("--tol", type=float, default=1e-6, help="--expect 对拍容差")
    p.add_argument("--force", action="store_true", help="验算未通过仍强制写入（须声明）")
    p.set_defaults(fn=cmd_struct)

    p = sub.add_parser("set", help="改键值（指标键或全局点路径）")
    p.add_argument("target", nargs="?", default=None, help="指标 id（用 --path 时省略）")
    p.add_argument("--key", default=None)
    p.add_argument("--path", default=None, help="全局点路径，如 engine.timezone")
    p.add_argument("--value", required=True)
    p.set_defaults(fn=cmd_set)

    p = sub.add_parser("batch", help="批量补丁（ops.yaml 一次写入）")
    p.add_argument("ops", help="ops.yaml 路径（ops: [...]）")
    p.add_argument("--db", default=None, help="作用于所有未自带 db 的 struct op")
    p.set_defaults(fn=cmd_batch)

    p = sub.add_parser("fixuid", help="给缺 uid 的本体实体补稳定身份")
    p.add_argument("--map", dest="map", default=None, help="uid_map.yaml：{实体name: uid}")
    p.set_defaults(fn=cmd_fixuid)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
