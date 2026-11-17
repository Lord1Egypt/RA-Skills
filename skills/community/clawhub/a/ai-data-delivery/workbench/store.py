"""Transactional project state, separate canvas layout and immutable revisions."""
import copy
import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import uuid
from contextlib import contextmanager


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


class Conflict(ValueError):
    pass


class Store:
    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "project.sqlite"
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS revisions (
                  revision INTEGER PRIMARY KEY, created TEXT NOT NULL,
                  actor TEXT NOT NULL, summary TEXT NOT NULL, document TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS layout (node TEXT PRIMARY KEY, x REAL, y REAL);
                CREATE TABLE IF NOT EXISTS runs (
                  id TEXT PRIMARY KEY, created TEXT, revision INTEGER, model_hash TEXT,
                  data_hash TEXT, kind TEXT, report TEXT);
                CREATE TABLE IF NOT EXISTS attachments (
                  id TEXT PRIMARY KEY, filename TEXT, kind TEXT, sha256 TEXT, content BLOB);
            """)
            if not db.execute("SELECT 1 FROM revisions LIMIT 1").fetchone():
                doc = {"name": "新的语义项目", "model": {"version": "draft-1", "datasets": [],
                       "relationships": [], "concepts": [], "metrics": []}, "scenarios": [],
                       "sources": [], "decisions": [], "feedback": [], "consumer": {}}
                db.execute("INSERT INTO revisions VALUES (0,?,?,?,?)", (now(), "local", "创建项目", encode(doc)))

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def read(self, revision=None):
        with self.connect() as db:
            row = db.execute("SELECT * FROM revisions ORDER BY revision DESC LIMIT 1" if revision is None else
                             "SELECT * FROM revisions WHERE revision=?", () if revision is None else (int(revision),)).fetchone()
        if row is None:
            raise ValueError("找不到项目版本")
        return {"revision": row["revision"], "document": json.loads(row["document"]), "updated": row["created"]}

    def change(self, expected_revision, actor, summary, mutate):
        if not isinstance(expected_revision, int):
            raise ValueError("操作需要当前项目版本，请刷新后重试")
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM revisions ORDER BY revision DESC LIMIT 1").fetchone()
            if row["revision"] != expected_revision:
                raise Conflict("项目已被另一操作修改；请刷新后审阅差异再保存")
            doc = json.loads(row["document"])
            result = mutate(doc)
            rendered = encode(doc)
            if rendered == row["document"]:
                return {"revision": expected_revision, "result": result}
            revision = expected_revision + 1
            db.execute("INSERT INTO revisions VALUES (?,?,?,?,?)", (revision, now(), actor or "local", summary, rendered))
        return {"revision": revision, "result": result}

    def history(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT revision,created,actor,summary FROM revisions ORDER BY revision DESC LIMIT 100")]

    def restore(self, target, expected):
        old = self.read(target)["document"]
        def replace(doc):
            doc.clear()
            doc.update(copy.deepcopy(old))
        return self.change(expected, "local", f"恢复版本 {target}（保留后续历史）", replace)

    def layouts(self):
        with self.connect() as db:
            return {r["node"]: {"x": r["x"], "y": r["y"]} for r in db.execute("SELECT * FROM layout")}

    def save_layout(self, positions):
        if len(positions) > 5000:
            raise ValueError("布局节点过多")
        import math
        rows = []
        for key, pos in positions.items():
            x, y = float(pos["x"]), float(pos["y"])
            if not math.isfinite(x + y) or max(abs(x), abs(y)) > 100000:
                raise ValueError("无效节点位置")
            rows.append((str(key), x, y))
        with self.connect() as db:
            db.executemany("INSERT OR REPLACE INTO layout VALUES (?,?,?)", rows)

    def attach(self, filename, kind, content):
        sha = hashlib.sha256(content).hexdigest()
        aid = sha[:24]
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO attachments VALUES (?,?,?,?,?)", (aid, Path(filename).name, kind, sha, content))
        return {"id": aid, "filename": Path(filename).name, "kind": kind, "sha256": sha, "bytes": len(content)}

    def attachment(self, aid):
        with self.connect() as db:
            row = db.execute("SELECT * FROM attachments WHERE id=?", (aid,)).fetchone()
        if not row:
            raise ValueError("资料不存在")
        return dict(row)

    def add_run(self, state, kind, report, data_hash=None):
        rid = uuid.uuid4().hex
        with self.connect() as db:
            db.execute("INSERT INTO runs VALUES (?,?,?,?,?,?,?)", (rid, now(), state["revision"],
                       digest(state["document"]["model"]), data_hash, kind, encode(report)))
        return rid

    def runs(self):
        state = self.read()
        model_hash = digest(state["document"]["model"])
        data_hash = (state["document"].get("sample") or {}).get("sha256")
        with self.connect() as db:
            rows = db.execute("SELECT * FROM runs ORDER BY created DESC LIMIT 100").fetchall()
        result = []
        for r in rows:
            item = dict(r)
            item["report"] = json.loads(item["report"])
            item["stale"] = item["model_hash"] != model_hash or (item["data_hash"] is not None and item["data_hash"] != data_hash)
            if item["kind"] in {"consumer", "check"} and item["revision"] != state["revision"]:
                item["stale"] = True  # Scene settings and confirmations are evidence inputs too.
            result.append(item)
        return result

    def backup(self, destination):
        destination = Path(destination)
        target = sqlite3.connect(destination)
        try:
            with self.connect() as source:
                source.backup(target)
        finally:
            target.close()


COLLECTIONS = {"datasets": ("datasets", "name"), "metrics": ("metrics", "id"),
               "templates": ("templates", "id"), "concepts": ("concepts", "term"),
               "relationships": ("relationships", "id"), "entities": ("ontology.entities", "uid"),
               "relations": ("ontology.relations", "id"), "constraints": ("constraints", "id")}


def collection(model, kind):
    if kind not in COLLECTIONS:
        raise ValueError("未知资产类型")
    path, _ = COLLECTIONS[kind]
    obj = model
    parts = path.split(".")
    for part in parts[:-1]:
        obj = obj.setdefault(part, {})
    return obj.setdefault(parts[-1], [])


def identity(kind, item):
    if kind == "entities":
        return item.get("uid") or item.get("name")
    if kind == "relationships":
        from _contract import relation_id
        return relation_id(item)
    if kind == "relations":
        return item.get("id") or f"{item.get('from')}->{item.get('to')}:{item.get('predicate')}"
    return item.get(COLLECTIONS[kind][1])


def merge(base, patch):
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge(base[key], value)
        else:
            base[key] = copy.deepcopy(value)


def edit_asset(model, kind, key, patch, remove=False):
    items = collection(model, kind)
    matches = [x for x in items if identity(kind, x) == key] if key else []
    if key and len(matches) != 1:
        raise ValueError("资产已改变或不存在，请重新选择")
    old = matches[0] if matches else None
    if remove:
        if old is None:
            raise ValueError("请选择要删除的资产")
        refs = references(model, kind, old)
        if refs:
            raise ValueError("仍被引用，请先处理：" + "、".join(refs[:8]))
        items.remove(old)
        return
    if not isinstance(patch, dict):
        raise ValueError("修改内容必须是对象")
    updated = copy.deepcopy(old or {})
    merge(updated, patch)
    id_field = COLLECTIONS[kind][1]
    if kind == "entities":
        updated.setdefault("uid", "ent_" + uuid.uuid4().hex[:12])
        if not updated.get("name"):
            raise ValueError("请填写业务对象名称")
    elif kind in {"relationships", "relations", "constraints", "templates", "metrics"}:
        updated.setdefault("id", identity(kind, old) if old else kind[:3] + "_" + uuid.uuid4().hex[:12])
    if not updated.get(id_field):
        raise ValueError("名称或标识不能为空")
    if old and kind != "entities" and old.get(id_field) and updated[id_field] != old[id_field]:
        raise ValueError("稳定标识不能在普通编辑中改名，请修改显示名称")
    if any(x is not old and (identity(kind, x) == identity(kind, updated) or
                            (kind == "entities" and x.get("name") == updated.get("name"))) for x in items):
        raise ValueError("名称或标识已存在")
    if kind == "relations":
        entities = {x["name"] for x in collection(model, "entities")}
        if updated.get("from") not in entities or updated.get("to") not in entities:
            raise ValueError("关系两端必须是已存在的业务对象")
        if not updated.get("predicate"):
            raise ValueError("请填写关系的业务含义")
        if updated.get("mapping") not in {"equi_key", "weak", "derived", "semantic_only"}:
            raise ValueError("请选择关系的落地方式")
        if updated["mapping"] != "equi_key" and not updated.get("note"):
            raise ValueError("请说明关系的依据或尚未落地的原因")
    if old and kind == "entities" and old.get("uid") and updated["uid"] != old["uid"]:
        raise ValueError("业务对象的稳定身份不能修改")
    if old and kind == "entities" and old["name"] != updated["name"]:
        before, after = old["name"], updated["name"]
        for rel in collection(model, "relations"):
            # Composite fallback IDs may also be referenced by a physical projection.
            # Freeze the old identity before renaming an endpoint, then update references below.
            if rel.get("id") is None and before in (rel.get("from"), rel.get("to")):
                rel["id"] = identity("relations", rel)
            for endpoint in ("from", "to"):
                if rel.get(endpoint) == before:
                    rel[endpoint] = after
        for entity in items:
            if entity.get("is_a") == before:
                entity["is_a"] = after
        for ds in model.get("datasets", []):
            if ds.get("ontology_ref") == before:
                ds["ontology_ref"] = updated["uid"]
    if old:
        items[items.index(old)] = updated
    else:
        items.append(updated)
    return updated


def references(model, kind, item):
    refs = []
    if kind == "entities":
        identifiers = {item.get("name"), item.get("uid")} - {None}
        refs += ["映射：" + d["name"] for d in model.get("datasets", []) if d.get("ontology_ref") in identifiers]
        refs += ["关系：" + str(r.get("predicate")) for r in collection(model, "relations") if r.get("from") in identifiers or r.get("to") in identifiers]
        refs += ["分类：" + e["name"] for e in collection(model, "entities") if e.get("is_a") in identifiers]
    if kind == "datasets":
        name = item["name"]
        for section in ("metrics", "templates", "constraints"):
            refs += [section + ":" + str(x.get("id")) for x in model.get(section, []) if x.get("dataset") == name or (x.get("references") or {}).get("dataset") == name]
        refs += ["关系" for r in model.get("relationships", []) if name in (r.get("from"), r.get("to"))]
        refs += ["概念：" + c.get("term", "") for c in model.get("concepts", []) if name in encode(c.get("expand", {}))]
    if kind == "relations":
        relation_key = identity("relations", item)
        refs += ["映射关系" for r in model.get("relationships", []) if r.get("ontology_ref") in {item.get("id"), relation_key}]
    if kind == "relationships":
        refs += ["查询路径：" + q.get("id", "") for q in model.get("query_plans", []) if identity(kind, item) in q.get("relationships", [])]
    if kind == "metrics":
        refs += ["查询路径：" + q.get("id", "") for q in model.get("query_plans", []) if q.get("metric") == item.get("id")]
    return refs
