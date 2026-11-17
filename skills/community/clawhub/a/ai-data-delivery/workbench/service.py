"""Workbench operations. Reuses CLI validators; never executes uploaded code/DDL."""
import base64
import copy
from contextlib import contextmanager
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import time
import urllib.request
import urllib.parse
import uuid
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_model
import check_constraints
import check_join_graph
import guide_model
from _contract import top_shape_error, quote, relation_keys
from _sql import compile_single
from ingest_ddl import parse_sql
from derive_ontology import derive
from select_context import select_context
from query_bundle import run_bundle
from gen_dictionary import fmt_metric
from workbench.store import Store, digest, encode, edit_asset, collection, identity, now

PROFILES = {
    "metric": {"label": "指标问数", "required": ["audience", "time_scope", "acceptance"]},
    "nl2sql": {"label": "自由问数 / NL2SQL", "required": ["audience", "time_scope", "access_boundary", "refusal", "acceptance"]},
    "action": {"label": "一句话办事", "required": ["action_target", "eligibility", "permission", "confirmation", "idempotency", "receipt"]},
    "policy": {"label": "政策适用", "required": ["policy_source", "effective_period", "jurisdiction", "eligibility", "exceptions", "reviewer"]},
    "decision": {"label": "分析与决策", "required": ["objective", "alternatives", "constraints", "baseline", "assumptions", "evaluation"]},
}
LABELS = {"audience": "谁使用结果", "time_scope": "时间范围与统计时点", "acceptance": "预期结果与核对依据",
          "access_boundary": "数据访问范围", "refusal": "不能回答时如何处理", "action_target": "办理对象与动作",
          "eligibility": "适用条件", "permission": "谁有办理权限", "confirmation": "提交前确认点",
          "idempotency": "重复请求与重试约定", "receipt": "回执、失败与补偿", "policy_source": "条款来源与版本",
          "effective_period": "生效与失效时间", "jurisdiction": "适用地域与人群", "exceptions": "例外与冲突处理",
          "reviewer": "复核责任人", "objective": "决策目标", "alternatives": "备选方案", "constraints": "资源与业务约束",
          "baseline": "比较基线", "assumptions": "假设与不确定性", "evaluation": "评价方法与结果核验"}


def validate_document(model):
    error = top_shape_error(model)
    if error:
        raise ValueError(error)
    # Structural drafts are allowed; malformed containers are not editable safely.
    for kind in ("datasets", "metrics", "templates", "concepts", "relationships", "constraints", "query_plans"):
        if kind in model and (not isinstance(model[kind], list) or any(not isinstance(x, dict) for x in model[kind])):
            raise ValueError(f"{kind} 必须是对象列表")
    for ds in model.get("datasets", []):
        if not ds.get("name") or not isinstance(ds.get("fields", []), list) or any(not isinstance(f, dict) or not f.get("name") for f in ds.get("fields", [])):
            raise ValueError("数据集需要 name；fields 必须是带 name 的字段列表")
    for kind, key in (("metrics", "id"), ("templates", "id"), ("concepts", "term")):
        if any(not x.get(key) for x in model.get(kind, [])):
            raise ValueError(f"{kind} 缺稳定标识 {key}")
    ont = model.get("ontology", {})
    for section in ("entities", "relations"):
        if section in ont and (not isinstance(ont[section], list) or any(not isinstance(x, dict) for x in ont[section])):
            raise ValueError("本体实体和关系必须是对象列表")
    if any(not x.get("name") for x in ont.get("entities", [])):
        raise ValueError("本体实体缺 name")
    encode(model)  # Reject cycles, dates and non-JSON scalars instead of dropping fields.


def lint(model):
    rep = check_model.Reporter()
    try:
        validate_document(model)
        if not model.get("datasets") and not model.get("ontology", {}).get("entities"):
            rep.error("E00", "model", "先导入结构或创建业务对象")
        elif not model.get("datasets"):
            rep.warn("W14", "model", "纯业务本体草案，尚未投影数据")
        ds = {d.get("name"): d for d in model.get("datasets", [])}
        check_model.check_datasets(model, rep)
        check_model.check_relationships(model, rep, set(ds))
        check_model.check_concepts(model, rep, ds)
        check_model.check_metrics(model, rep, ds)
        check_model.check_templates(model, rep, ds)
        check_model.check_ontology(model, rep)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        rep.error("E00", "model", str(exc))
    return {"status": "fail" if rep.errors else ("attention" if rep.warnings else "pass"),
            "errors": rep.errors, "warnings": rep.warnings}


def gaps(document):
    """Requirements are generated from current facts, never read from test gold guidance."""
    model = document["model"]
    result = []
    def add(kind, key, prop, question, role, options=None):
        result.append({"id": digest([kind, key, prop])[:16], "kind": kind, "key": key,
                       "property": prop, "question": question, "role": role, "options": options})
    for ds in model.get("datasets", []):
        for prop, question, role, options in (
            ("grain", "一行代表什么？例如：每个学院每个学年一行。", "business_owner", None),
            ("primary_key", "哪个字段或复合键标识这一行？", "data_owner", None),
            ("source", "对应哪个物理表或视图？", "data_owner", None),
            ("ai.instructions", "这份数据能回答什么，哪些问题不能回答？", "business_owner", None),
            ("temporal.kind", "数据记录的是当前状态、发生事件还是定期快照？", "data_owner", ["current", "event", "snapshot"])):
            if not guide_model.get_value(ds, prop):
                add("datasets", ds["name"], prop, question, role, options)
    for metric in model.get("metrics", []):
        for prop, question in (("caliber.note", "明确包含、排除及统计范围。"), ("unit", "结果使用什么单位？"),
                               ("time_field", "按哪个业务时间字段统计？")):
            if prop == 'time_field' and metric.get('time_requirement') == 'current':
                continue
            if not guide_model.get_value(metric, prop):
                add("metrics", metric["id"], prop, question, "business_owner")
        if metric.get("type") == "ratio":
            if "on_zero_denominator" not in metric:
                add("metrics", metric["id"], "on_zero_denominator", "分母为零时返回空值、零还是错误？", "business_owner", ["null", "zero", "error"])
            if metric.get("unit") == "%" and "display_scale" not in metric:
                add("metrics", metric["id"], "display_scale", "计算值以 0–1 存储时，百分数展示乘数是否为 100？", "business_owner")
    return result


def scene_status(document):
    output = []
    datasets = {d["name"] for d in document["model"].get("datasets", [])}
    metrics = {m["id"] for m in document["model"].get("metrics", [])}
    for s in document.get("scenarios", []):
        profile = PROFILES.get(s.get("profile"), PROFILES["metric"])
        missing = [LABELS[k] for k in profile["required"] if not s.get("requirements", {}).get(k)]
        if not s.get("question"):
            missing.append("具体业务问题")
        if s.get("profile") in {"metric", "nl2sql"} and not s.get("datasets"):
            missing.append("本次涉及的数据集")
        if not set(s.get("datasets", [])) <= datasets or not set(s.get("metrics", [])) <= metrics:
            missing.append("引用的数据集或指标不存在")
        relevant = [g for g in gaps(document) if (g["kind"] == "datasets" and g["key"] in s.get("datasets", [])) or
                    (g["kind"] == "metrics" and g["key"] in s.get("metrics", []))]
        missing += [g["question"] for g in relevant]
        output.append({**s, "missing": missing, "status": "needs_input" if missing else "declared",
                       "runtime": "需在检查页核对结果" if s.get("profile") == "metric" else "仅完成需求与语义声明；专用执行器尚未接入"})
    return output


@contextmanager
def sample_db(store, document):
    sample = document.get("sample")
    if not sample:
        yield None
        return
    data = store.attachment(sample["id"])["content"]
    with tempfile.TemporaryDirectory(prefix="semantic-snapshot-") as td:
        p = Path(td) / "sample.sqlite"
        p.write_bytes(data)
        conn = sqlite3.connect(p.as_uri() + "?mode=ro&immutable=1", uri=True)
        try:
            conn.execute("PRAGMA query_only=ON")
            conn.execute("PRAGMA trusted_schema=OFF")
            deadline = time.monotonic() + 15
            conn.set_progress_handler(lambda: int(time.monotonic() > deadline), 10000)
            yield conn
        finally:
            conn.close()


def compare_rows(actual, expected):
    """Shape and every cell matter: [[11]] never satisfies [[11,25]]."""
    if not isinstance(actual, list) or not isinstance(expected, list) or len(actual) != len(expected):
        return False
    for left, right in zip(actual, expected):
        if not isinstance(left, list) or not isinstance(right, list) or len(left) != len(right):
            return False
        for a, b in zip(left, right):
            if isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
                if abs(a - b) > 0.0001:
                    return False
            elif a != b or type(a) is not type(b):
                return False
    return True


def consumer_projection(model):
    """Supported projection of the existing Java demo API, not a universal adapter."""
    aliases = {"displayName": "display_name", "primaryKey": "primary_key", "tenantField": "tenant_field",
               "knownDefect": "known_defect", "timeField": "time_field", "extraWhere": "extra_where",
               "joinKey": "join_key", "joinKeyFrom": "join_key_from", "joinKeyTo": "join_key_to",
               "fromColumns": "from_columns", "toColumns": "to_columns"}
    allowed = {
        "datasets": {"name", "source", "grain", "primary_key", "tenant_field", "fields"},
        "relationships": {"from", "to", "from_columns", "to_columns", "join_key", "join_key_from", "join_key_to", "cardinality", "traversable"},
        "metrics": {"id", "name", "type", "structured", "dataset", "time_field", "unit", "expr", "extra_where", "synonyms", "numerator", "denominator", "filters"},
        "concepts": {"term", "synonyms", "expand"},
    }
    def clean(value, preserve_empty=False):
        if isinstance(value, dict):
            result = {}
            for k, v in value.items():
                if not preserve_empty and (v is None or v == [] or v == {}):
                    continue
                key, val = aliases.get(k, k), clean(v, preserve_empty)
                if key in result and result[key] != val:
                    raise ValueError(f"消费者模型同义字段冲突：{key}")
                result[key] = val
            return result
        if isinstance(value, list):
            return [clean(v, preserve_empty) for v in value]
        return value
    out = {}
    for section, keys in allowed.items():
        if section == 'relationships':
            normalized = []
            for item in model.get(section, []):
                raw = clean(item, True)
                has_keys = any(k in raw for k in ('from_columns', 'to_columns', 'join_key', 'join_key_from', 'join_key_to'))
                if not has_keys and raw.get('traversable') is False:
                    normalized.append({k: v for k, v in clean(item).items() if k in keys})
                    continue
                left, right = relation_keys(raw)
                row = {k: v for k, v in clean(item).items() if k in keys and k not in {'join_key', 'join_key_from', 'join_key_to'}}
                row.update(from_columns=left, to_columns=right)
                normalized.append(row)
            out[section] = sorted(normalized, key=encode)
            continue
        rows = [{k: v for k, v in clean(x).items() if k in keys} for x in model.get(section, [])]
        if section == "datasets":
            for row in rows:
                row["fields"] = [{k: v for k, v in f.items() if k in {"name", "type", "role", "enum"}} for f in row.get("fields", [])]
                if isinstance(row.get('primary_key'), str):
                    row['primary_key'] = [row['primary_key']]
        out[section] = sorted(rows, key=encode)
    return out


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError("消费者接口不允许重定向")


def local_json(base, path, payload=None):
    parsed = urllib.parse.urlsplit(base)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"} or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
        raise ValueError("消费者地址仅支持 http://127.0.0.1:端口 或 http://localhost:端口")
    # Pin localhost to IPv4 loopback; proxies and redirects cannot move this request off host.
    url = f"http://127.0.0.1:{parsed.port or 80}{path}"
    req = urllib.request.Request(url, data=encode(payload).encode() if payload is not None else None,
                                 headers={"Content-Type": "application/json"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(req, timeout=15) as response:
        data = response.read(4 * 1024 * 1024 + 1)
    if len(data) > 4 * 1024 * 1024:
        raise ValueError("消费者响应超过 4 MB")
    return json.loads(data)


class Service:
    def __init__(self, directory):
        self.store = Store(directory)

    def state(self):
        state = self.store.read()
        return {**state, "layout": self.store.layouts(), "history": self.store.history(), "runs": self.store.runs(),
                "gaps": gaps(state["document"]), "scenarios": scene_status(state["document"]),
                "profiles": PROFILES, "labels": LABELS}

    def change(self, req, summary, fn):
        return self.store.change(req.get("revision"), req.get("actor", "local"), summary, fn)

    def import_file(self, req):
        raw = base64.b64decode(req["content"], validate=True)
        if len(raw) > 32 * 1024 * 1024:
            raise ValueError("单个导入文件上限 32 MB；大库请先导出小范围 SQLite 快照")
        kind, name = req["kind"], req["filename"]
        attachment = {"kind": kind, "filename": name, "sha256": hashlib.sha256(raw).hexdigest()}
        model, extra = None, {}
        if kind == "model":
            try:
                model = yaml.safe_load(raw.decode("utf-8-sig"))
            except (yaml.YAMLError, UnicodeError) as exc:
                mark = getattr(exc, 'problem_mark', None)
                location = f'（第 {mark.line+1} 行、第 {mark.column+1} 列）' if mark else ''
                raise ValueError('模型文件不是有效的 UTF-8 YAML/JSON'+location+'；请检查格式后重新导入。') from exc
            validate_document(model)
        elif kind == "ddl":
            tables, failures = parse_sql(raw.decode("utf-8-sig"), name)
            if not tables:
                raise ValueError("未找到受支持的 CREATE TABLE；请导出 SQLite/MySQL DDL")
            extra = {"parse_failures": failures, "note": "仅提取表和字段；外键及业务含义请在图中确认，DDL 从未执行。"}
            model = {"version": "draft-1", "datasets": []}
            for table in tables:
                model["datasets"].append({"name": table["name"], "source": table["name"], "grain": "",
                    "primary_key": table["pk_guess"], "fields": [{"name": c["name"], "type": c["type"], "cn": c.get("comment", ""),
                    "role": "pk" if c["pk"] else ("time" if c["is_time"] else "attr")} for c in table["columns"]]})
        elif kind == "sample":
            if not raw.startswith(b"SQLite format 3\x00"):
                raise ValueError("请导入独立 SQLite 快照文件")
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "sample.sqlite"; p.write_bytes(raw)
                conn = sqlite3.connect(p.as_uri() + "?mode=ro&immutable=1", uri=True)
                try:
                    if conn.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                        raise ValueError("SQLite 快照完整性检查未通过")
                    extra["tables"] = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
                finally:
                    conn.close()
            if req.get("provenance") not in {"demo", "deidentified", "production", "unknown"}:
                raise ValueError("请标记快照来源，未知来源不能当作生产数据")
            extra["provenance"] = req["provenance"]
            extra["snapshot_note"] = "仅上传已完成 checkpoint 的独立快照；WAL 模式请使用 SQLite backup API/导出流程生成一致快照，不能只复制主库文件。"
        elif kind == "inventory":
            inventory = json.loads(raw.decode("utf-8-sig"))
            extra["counts"] = {k: len(v) for k, v in inventory.items() if isinstance(v, list)} if isinstance(inventory, dict) else {"items": len(inventory)}
            extra["note"] = "保留原始指标/规则/案例清单；尚未自动转为可执行模型。请由 skill 对齐现有 ID、口径和来源。"
        else:
            raise ValueError("请选择模型、DDL、SQLite 快照或 JSON 清单")
        def mutate(doc):
            nonlocal attachment
            if model is not None:
                existing = doc["model"]
                occupied = any(existing.get(k) for k in ("datasets", "metrics", "ontology"))
                if occupied and not req.get("replace"):
                    raise ValueError("当前已有模型；导入替换需勾选确认，历史版本会保留。资料清单不会替换模型。")
                doc["model"] = copy.deepcopy(model)
            if kind in {'model', 'ddl', 'sample'} and doc.get('tutorial'):
                doc.pop('tutorial', None)
                doc['name'] = '语义项目（已更换资料）'
            attachment = {**saved, **extra}
            doc["sources"].append(attachment)
            if kind == "sample":
                doc["sample"] = attachment
            return attachment
        # Attach before revision transaction to avoid nested SQLite write locks.
        saved = self.store.attach(name, kind, raw)
        return self.change(req, f"导入 {name}", mutate)

    def derive(self, req):
        def mutate(doc):
            model, summary = derive(doc['model'])
            validate_document(model)
            doc['model'] = model
            return summary
        return self.change(req, '从元数据补充语义候选（待业务核对）', mutate)

    def edit(self, req):
        def mutate(doc):
            if req.get("remove") and req["kind"] in {"datasets", "metrics"}:
                if any(req["key"] in s.get(req["kind"], []) for s in doc["scenarios"]):
                    raise ValueError("场景仍在引用这个资产，请先调整场景范围")
            result = edit_asset(doc["model"], req["kind"], req.get("key"), req.get("patch", {}), req.get("remove", False))
            validate_document(doc["model"])
            return result
        return self.change(req, f"{'删除' if req.get('remove') else '编辑'} {req['kind']}", mutate)

    def answer(self, req):
        if not req.get("basis") or not req.get("actor") or not req.get("value"):
            raise ValueError("填写答案、确认人及依据后保存")
        def mutate(doc):
            gap = next((g for g in gaps(doc) if g["id"] == req["gap"]), None)
            if not gap:
                raise ValueError("缺口已改变，请刷新")
            if req.get("role") != gap["role"]:
                raise ValueError("请以对应责任角色记录确认；角色为本地留痕，不是权限认证")
            value = req["value"]
            if gap.get("options") and value not in gap["options"]:
                raise ValueError("请选择有效值")
            if gap["property"] == "primary_key":
                value = [v.strip() for v in str(value).split(",") if v.strip()]
                ds = next(x for x in doc["model"]["datasets"] if x["name"] == gap["key"])
                if not set(value) <= {f["name"] for f in ds.get("fields", [])}:
                    raise ValueError("主键必须使用已声明字段")
            if gap["property"] == "display_scale":
                value = float(value)
            obj = next(x for x in collection(doc["model"], gap["kind"]) if identity(gap["kind"], x) == gap["key"])
            guide_model.set_value(obj, gap["property"], value)
            doc["decisions"].append({**gap, "value": value, "basis": req["basis"], "actor": req["actor"], "role": req["role"], "created": now()})
        return self.change(req, "补齐语义并记录依据", mutate)

    def scene(self, req):
        scene = copy.deepcopy(req["scene"])
        if scene.get("profile") not in PROFILES or not scene.get("question"):
            raise ValueError("请选择场景类型并填写具体问题")
        if not isinstance(scene.get("requirements", {}), dict):
            raise ValueError("场景条件必须是属性对象")
        scene.setdefault("id", "scene_" + uuid.uuid4().hex[:12])
        for k in ("datasets", "metrics"):
            if not isinstance(scene.get(k, []), list):
                raise ValueError("场景引用需要列表")
        def mutate(doc):
            doc["scenarios"] = [s for s in doc["scenarios"] if s["id"] != scene["id"]] + [scene]
            return scene
        return self.change(req, "保存场景范围与验收约定", mutate)

    def check(self):
        state = self.store.read(); doc = state["document"]; model = doc["model"]
        report = {"model": lint(model), "gaps": gaps(doc), "scenarios": scene_status(doc),
                  "boundary": "只验证已声明范围；模拟数据通过不代表生产、权限、业务签署或政策合规通过。"}
        try:
            with sample_db(self.store, doc) as conn:
                if conn is None:
                    report["data"] = {"status": "not_ready", "records": [], "detail": "尚未导入数据快照"}
                else:
                    report["data"] = check_constraints.check_all(model, conn)
                try:
                    report["links"] = check_join_graph.analyze(model, conn)
                    if not report["links"]["relationships"]:
                        report["links"]["status"] = "not_ready"
                except (sqlite3.Error, OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
                    report["links"] = {"status": "error", "detail": str(exc), "relationships": []}
        except (sqlite3.Error, OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
            # A bad or missing imported snapshot is evidence of an incomplete run, not an HTTP failure.
            report["data"] = {"status": "error", "records": [], "detail": str(exc)}
            report["links"] = {"status": "error", "detail": str(exc), "relationships": []}
        bad_data = [r for r in report["data"]["records"] if r["status"] in {"fail", "error"}]
        report["next"] = (["补齐结构和语义：" + g["question"] for g in report["gaps"][:5]] +
                          ["核实并修复源数据：" + r["id"] for r in bad_data])
        if report["data"]["status"] == "not_ready" and not report["data"]["records"]:
            report["next"].append("导入快照并声明需要核验的约束；没有检查项不等于检查通过。")
        report["status"] = "blocked" if report["model"]["errors"] or bad_data else "review"
        report["provenance"] = doc.get("sample", {}).get("provenance", "unknown")
        rid = self.store.add_run(state, "check", report, doc.get("sample", {}).get("sha256"))
        return {"id": rid, **report}

    def query(self, req):
        state = self.store.read(); doc = state["document"]; model = doc["model"]
        metric = next((m for m in model.get("metrics", []) if m["id"] == req.get("metric")), None)
        if metric is None:
            raise ValueError("请选择指标")
        ds = next((d for d in model.get("datasets", []) if d["name"] == metric.get("dataset")), None)
        sql, reason = compile_single(metric, ds)
        report = {"metric": metric["id"], "sql": sql, "status": "not_ready", "detail": reason,
                  "unit": metric.get("unit"), "provenance": doc.get("sample", {}).get("provenance", "unknown"),
                  "scope": "指标自身声明的全范围；未自动追加自然语言问题的时间/组织条件"}
        if sql:
            try:
                with sample_db(self.store, doc) as conn:
                    if conn is None:
                        report["detail"] = "尚未导入 SQLite 快照"
                    else:
                        cursor = conn.execute(sql)
                        rows = [list(r) for r in cursor.fetchmany(501)]
                        if len(rows) > 500:
                            raise ValueError("结果超过 500 行，不能当作标量指标")
                        if any("ZERO_DENOMINATOR" in row for row in rows):
                            raise ValueError("分母为零，当前口径要求报错")
                        report.update(rows=rows, status="computed_only", detail="已执行；尚未与独立预期核对")
                        if "expected" in req:
                            if not isinstance(req["expected"], list):
                                raise ValueError("预期结果必须是完整二维数组")
                            report.update(expected=req["expected"], status="pass" if compare_rows(rows, req["expected"]) else "fail", detail="完整结果与用户给定预期逐行逐列比较")
                        if metric.get("display_scale") and len(rows) == 1 and len(rows[0]) == 1 and isinstance(rows[0][0], (int, float)):
                            report["display_value"] = rows[0][0] * float(metric["display_scale"])
            except (sqlite3.Error, OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
                report.update(status="error", detail=str(exc))
        rid = self.store.add_run(state, "query", report, doc.get("sample", {}).get("sha256"))
        return {"id": rid, **report}

    def context(self, req):
        state = self.store.read()
        result = select_context(state['document']['model'], req.get('metric'), req.get('columns', []))
        return {**result, 'source_revision': state['revision']}

    def bundle(self, req):
        state = self.store.read(); doc = state['document']
        with sample_db(self.store, doc) as conn:
            if conn is None:
                result = {'status': 'not_ready', 'error': {'code': 'SNAPSHOT_REQUIRED', 'message': '先导入 SQLite 快照'}}
            else:
                result = run_bundle(doc['model'], conn, req.get('metric'), req.get('columns'),
                                    limit=req.get('limit', 50), offset=req.get('offset', 0))
        if result['status'] == 'computed_only' and 'expected' in req:
            expected = req['expected']
            if not isinstance(expected, dict) or not {'metric_value', 'matched_row_count', 'detail_rows'} <= set(expected):
                raise ValueError('预期需要 metric_value、matched_row_count、detail_rows 三项；分页预期对应当前页')
            matched = (compare_rows([[result['metric_value'], result['matched_row_count']]],
                                    [[expected['metric_value'], expected['matched_row_count']]]) and
                       compare_rows(result['detail_rows'], expected['detail_rows']))
            result.update(status='pass' if matched else 'fail', expected=expected,
                          detail='指标、符合条件记录数和当前页明细分别与输入的独立预期核对')
        result.update(provenance=doc.get('sample', {}).get('provenance', 'unknown'),
                      boundary='同一模型与本地快照内的指标/明细核对；不是身份认证、生产接口联调或自然语言理解验收。')
        rid = self.store.add_run(state, 'bundle', result, doc.get('sample', {}).get('sha256'))
        return {'id': rid, **result}

    def feedback(self, req):
        if not req.get("text"):
            raise ValueError("填写问题、影响和需要谁处理")
        def mutate(doc):
            item = {"id": uuid.uuid4().hex[:12], "text": req["text"], "status": "open", "revision": req["revision"], "created": now()}
            doc["feedback"].append(item)
            return item
        return self.change(req, "记录交付问题", mutate)

    def resolve_feedback(self, req):
        if not req.get("resolution") or not req.get("actor"):
            raise ValueError("填写处理结果和责任人后关闭问题")
        def mutate(doc):
            item=next((x for x in doc["feedback"] if x["id"]==req.get("id")),None)
            if not item or item.get("status")!="open":
                raise ValueError("问题已关闭或不存在")
            item.update(status="resolved",resolution=req["resolution"],resolved_by=req["actor"],resolved_at=now())
        return self.change(req,"处理并关闭交付问题",mutate)

    def consumer(self, req):
        state = self.store.read()
        if not req.get("question"):
            raise ValueError("请填写要交给现有引擎的问题")
        endpoint = req.get("endpoint", "")
        loaded = local_json(endpoint, "/api/model")
        current = consumer_projection(state["document"]["model"])
        observed = consumer_projection(loaded)
        mismatch = [s for s in current if current[s] != observed[s]]
        if mismatch:
            result = {'status': 'model_mismatch', 'model_match': False,
                      'mismatch_sections': mismatch, 'consumer_model_sha256': digest(observed),
                      'question': req['question'], 'endpoint': endpoint, 'query_sent': False,
                      'boundary': '消费者模型不匹配，尚未发送问数请求；修复映射并重新检查。'}
            rid = self.store.add_run(state, 'consumer', result)
            return {'id': rid, **result}
        actual = local_json(endpoint, "/api/ask", {"question": req["question"]})
        if not isinstance(actual, dict):
            raise ValueError("消费者回执必须是对象；未获得可核对结果")
        rows = actual.get("rows")
        if rows is None and "value" in actual:
            rows = [[actual["value"]]]
        result = {"endpoint": endpoint, "question": req["question"], "actual": actual, "rows": rows,
                  "model_match": not mismatch, "mismatch_sections": mismatch,
                  "consumer_model_sha256": digest(observed), "status": "executed_only", "query_sent": True,
                  "boundary": "现有 Java 问数接口适配；投影匹配仅核对其已知字段。ontology、templates、constraints、除零与展示策略等扩展字段未证明被引擎消费。"}
        failed = (actual.get("rejected") is True or actual.get("success") is False or
                  bool(actual.get("error")) or ('status' in actual and str(actual['status']).lower() not in
                  {'ok', 'success', 'completed', 'done'}))
        if failed:
            result.update(status="consumer_not_completed", detail="消费者拒绝、报错或尚未完成；随回执携带的数值不能当作成功结果。")
        elif "expected" in req:
            result.update(expected=req["expected"], status="pass" if compare_rows(rows, req["expected"]) else "fail")
        rid = self.store.add_run(state, "consumer", result)
        return {"id": rid, **result}

    def review_data(self, state=None, runs=None):
        from visualize_model import ontology_view
        state = state or self.store.read()
        doc = state['document']
        runs = self.store.runs() if runs is None else runs
        names = {'bundle': '指标与明细核对', 'query': '指标直算', 'consumer': '消费者核对', 'check': '模型与数据检查'}
        return {'model': doc['model'], 'sha256': digest(doc['model']), 'ontology': ontology_view(doc['model']),
                'scenarios': doc['scenarios'], 'decisions': doc['decisions'], 'issues': doc['feedback'],
                'fingerprint_kind': '规范化模型内容SHA256',
                'gaps': gaps(doc), 'history': None,
                'reports': [{'name': names.get(r['kind'], r['kind'])+' · '+str(r['report'].get('metric', r['id']))+' · '+r['created'][:19],
                             'binding_errors': ['模型、快照或适用条件已变更'] if r['stale'] else [],
                             'stale': r['stale'], 'report': r['report']} for r in runs]}

    def review_html(self):
        from visualize_model import render_html
        return render_html(self.review_data()).encode('utf-8')

    def export(self, snapshot=False):
        from visualize_model import render_html
        state = self.store.read(); doc = state["document"]
        runs = self.store.runs()
        out = io.BytesIO()
        entries = {"semantic.yaml": yaml.safe_dump(doc["model"], allow_unicode=True, sort_keys=False).encode(),
                   "scenarios.json": encode(doc["scenarios"]).encode(), "decisions.json": encode(doc["decisions"]).encode(),
                   "issues.json": encode(doc["feedback"]).encode(), "evidence.json": encode(runs).encode(),
                   "00-human-review.html": render_html(self.review_data(state, runs)).encode('utf-8')}
        lines = ["# 语义字典", "", "此字典来自同版本模型。业务口径与标准适用性仍需责任人复核。", ""]
        for ds in doc["model"].get("datasets", []):
            lines += ["## " + ds.get("cn", ds["name"]), f"来源：{ds.get('source','未定')}；粒度：{ds.get('grain','未定')}", ""]
            lines += [f"- {f['name']}：{f.get('cn', '待补含义')}（{f.get('role','attr')}）" for f in ds.get("fields", [])]
        for metric in doc['model'].get('metrics', []):
            lines += ['', '## 指标：' + str(metric.get('name') or metric['id']),
                      f"挂载数据集：{metric.get('dataset', '未定')}；单位：{metric.get('unit', '未定')}",
                      '口径：' + fmt_metric(metric),
                      '说明：' + str((metric.get('caliber') or {}).get('note', '未定'))]
        entries["dictionary.md"] = "\n".join(lines).encode()
        if snapshot:
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "project.sqlite"; self.store.backup(p)
                entries["project.sqlite"] = p.read_bytes()
        manifest = {"format": "semantic-workbench-1", "revision": state["revision"], "model_sha256": digest(doc["model"]),
                    "kind": "private_project_backup" if snapshot else "semantic_delivery", "created": now(),
                    "includes_source_data": snapshot, "validation": "see evidence.json; stale evidence is not current proof",
                    "files": {k: hashlib.sha256(v).hexdigest() for k, v in entries.items()}}
        entries["manifest.json"] = encode(manifest).encode()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for name, value in entries.items():
                z.writestr(name, value)
        return out.getvalue()
