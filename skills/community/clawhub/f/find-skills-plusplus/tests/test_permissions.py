# -*- coding: utf-8 -*-
"""权限清单提取（对标 skill-vetter Step 3 三问：文件 / 网络 / 命令）。"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import security_scan as ss  # noqa: E402

HEAD = "---\nname: t\ndescription: d\n---\n"


def _perm(md_body):
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "s"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(HEAD + md_body, encoding="utf-8")
        return ss.build_report(d)["permissions"]


def test_extracts_network_host():
    p = _perm("```bash\ncurl https://api.example.com/v1\n```\n")
    assert "api.example.com" in p["network"]


def test_extracts_commands():
    p = _perm("```bash\npip install x\ncurl https://a.com\nsudo chmod 777 /tmp\n```\n")
    for c in ("pip", "curl", "sudo", "chmod"):
        assert c in p["commands"], f"缺少命令 {c}"


def test_extracts_sensitive_files():
    p = _perm("```bash\ncat ~/.ssh/id_rsa\ncp MEMORY.md /tmp\n```\n")
    joined = " ".join(p["files"])
    assert "ssh" in joined or "id_rsa" in joined
    assert "MEMORY.md" in joined


def test_extracts_system_paths():
    p = _perm("```bash\ncp x /etc/cron.d/y\n```\n")
    assert any("/etc" in f for f in p["files"])


def test_report_has_permission_block():
    p = _perm("ok\n")
    assert set(p.keys()) == {"network", "files", "commands"}
    assert all(isinstance(v, list) for v in p.values())


def test_empty_skill_no_permissions():
    p = _perm("纯提示词技能，无脚本无外联。\n")
    assert p["commands"] == [] and p["network"] == []


def test_self_permissions_present():
    rep = ss.build_report(ROOT, exclude_tests=True)
    assert "permissions" in rep
    assert isinstance(rep["permissions"]["commands"], list)
