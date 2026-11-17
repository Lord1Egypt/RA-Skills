"""diff_engine v2 边界测试：多语言检测 / JS import 边 / 跨语言路由边 / 符号映射 / 黑名单 / 快照迁移。

运行：cd /Users/xujin/.agents/skills/archmap && python3 -m pytest archmap_agent/tests/test_diff_engine_edges.py -q
"""
import json
from pathlib import Path

from archmap_agent.diff_engine import (
    IMPORTS_NAME, ROUTES_NAME, SNAPSHOT_NAME, run_diff_impact,
    write_import_snapshot, write_line_snapshot,
)


def _mk(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _bootstrap(root: Path, base: Path):
    base.mkdir(parents=True, exist_ok=True)
    write_line_snapshot(root, base)
    write_import_snapshot(root, base)


def test_ts_change_detected_and_js_import_closure(tmp_path):
    root, base = tmp_path / "proj", tmp_path / "base"
    _mk(root, "fe/api.ts", "export const x = 1\n")
    _mk(root, "fe/page.ts", "import { x } from './api'\nconsole.log(x)\n")
    _bootstrap(root, base)
    _mk(root, "fe/api.ts", "export const x = 2\n")
    d = run_diff_impact(root, base, note="ts 变更")
    assert d["status"] == "ok"
    assert d["changed_files"][0]["path"] == "fe/api.ts"
    assert "fe/page.ts" in d["affected_closure"]["files"]  # JS import 边传导


def test_cross_language_route_edge(tmp_path):
    root, base = tmp_path / "proj", tmp_path / "base"
    _mk(root, "be/api.py", "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/api/users')\ndef list_users():\n    return []\n")
    _mk(root, "fe/users.ts", "export async function load() {\n  return fetch('/api/users')\n}\n")
    _mk(root, "fe/unrelated.ts", "export const u = '/api/nonexistent'\n")
    _bootstrap(root, base)
    # 改后端路由实现 → 前端引用方必须入闭包（路由边），且无关字面量不成边
    _mk(root, "be/api.py", "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/api/users')\ndef list_users():\n    return [1]\n")
    d = run_diff_impact(root, base)
    files = d["affected_closure"]["files"]
    assert "fe/users.ts" in files
    assert "fe/unrelated.ts" not in files  # 未定义路由的字面量零噪音
    assert "fe/users.ts" in d["affected_via_route"]
    # 反向：改前端 → 后端路由定义方也入闭包（双向）
    _bootstrap(root, base)  # 重置快照
    _mk(root, "fe/users.ts", "export async function load() {\n  return fetch('/api/users?page=1')\n}\n")
    d2 = run_diff_impact(root, base)
    assert "be/api.py" in d2["affected_closure"]["files"]


def test_py_symbols_mapped(tmp_path):
    root, base = tmp_path / "proj", tmp_path / "base"
    before = "def alpha():\n    return 1\n\n\ndef beta():\n    return 2\n"
    _mk(root, "svc/mod.py", before)
    _bootstrap(root, base)
    _mk(root, "svc/mod.py", before.replace("return 2", "return 3"))
    d = run_diff_impact(root, base)
    assert d["changed_files"][0].get("symbols") == ["beta"]


def test_backup_dirs_excluded(tmp_path):
    root, base = tmp_path / "proj", tmp_path / "base"
    _mk(root, "core/hash.py", "def h():\n    return 1\n")
    _mk(root, "_backups/old_copy.py", "from core.hash import h\nprint(h)\n")
    _mk(root, "data/migration_backup/x/old.py", "from core.hash import h\nprint(h)\n")
    _bootstrap(root, base)
    _mk(root, "core/hash.py", "def h():\n    return 2\n")
    d = run_diff_impact(root, base)
    files = d["affected_closure"]["files"]
    assert not any("_backups" in f or "migration_backup" in f for f in files)


def test_v1_snapshot_migration(tmp_path):
    root, base = tmp_path / "proj", tmp_path / "base"
    _mk(root, "a/x.py", "v = 1\n")
    _mk(root, "b/y.ts", "export const y = 1\n")
    base.mkdir(parents=True)
    # 手写 v1 旧格式快照（扁平 dict，仅 py）
    (base / SNAPSHOT_NAME).write_text(json.dumps({"a/x.py": ["0" * 16]}))
    (base / IMPORTS_NAME).write_text(json.dumps({}))
    d = run_diff_impact(root, base)
    assert d["status"] == "snapshot_migrated_v2"
    assert d["changed_files"] == []  # 不产生伪变更洪峰
    # 迁移后正常检测
    _mk(root, "b/y.ts", "export const y = 2\n")
    d2 = run_diff_impact(root, base)
    assert d2["status"] == "ok"
    assert d2["changed_files"][0]["path"] == "b/y.ts"
    assert (base / ROUTES_NAME).exists()


def test_spec_files_are_test_sink(tmp_path):
    root, base = tmp_path / "proj", tmp_path / "base"
    _mk(root, "fe/api.ts", "export const x = 1\n")
    _mk(root, "fe/api.spec.ts", "import { x } from './api'\ntest('x', () => x)\n")
    _bootstrap(root, base)
    _mk(root, "fe/api.ts", "export const x = 2\n")
    d = run_diff_impact(root, base)
    assert "fe/api.spec.ts" in d["test_selection"]["selected"]
    assert d["test_selection"]["untested_changes"] == []
