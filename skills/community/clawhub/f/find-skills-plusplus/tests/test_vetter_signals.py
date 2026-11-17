# -*- coding: utf-8 -*-
"""对标 skill-vetter（31 万下载）补齐的 8 项红旗信号检测。

每项：恶意样本必须命中，且不得因误报控制被静默吞掉。
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import security_scan as ss  # noqa: E402

HEAD = "---\nname: t\ndescription: d\n---\n"


def _hits(md_body, py=None):
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "s"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(HEAD + md_body, encoding="utf-8")
        if py:
            (d / "scripts").mkdir()
            (d / "scripts" / "a.py").write_text(py, encoding="utf-8")
        rep = ss.build_report(d)
    return rep["hits"]


def _has(hits, keyword):
    return any(keyword in h["signal"] for h in hits)


def test_credential_dir_ssh():
    assert _has(_hits("```bash\ncat ~/.ssh/id_rsa\n```\n"), "凭据目录读取")


def test_credential_dir_aws():
    assert _has(_hits("```bash\ncat ~/.aws/credentials\n```\n"), "凭据目录读取")


def test_agent_identity_files():
    assert _has(_hits("```bash\ncp MEMORY.md /tmp/x\n```\n"), "Agent身份/记忆文件")


def test_agent_identity_identity_md():
    assert _has(_hits("```bash\ncat IDENTITY.md\n```\n"), "Agent身份/记忆文件")


def test_raw_ip_connection():
    assert _has(_hits("```bash\ncurl http://45.77.12.9/p\n```\n"), "裸IP直连")


def test_browser_cookies():
    assert _has(_hits("```bash\ncp ~/Library/Cookies/cookies.sqlite /tmp\n```\n"),
                "浏览器凭据")


def test_chmod_777():
    assert _has(_hits("```bash\nchmod 777 /var/www\n```\n"), "权限放宽")


def test_silent_package_install():
    assert _has(_hits("```bash\npip install requests\n```\n"), "静默安装依赖包")


def test_system_dir_write():
    assert _has(_hits("```bash\ncp x /etc/cron.d/y\n```\n"), "系统目录写入")


def test_obfuscated_escapes():
    py = "exec('\\x69\\x6d\\x70\\x6f\\x72\\x74\\x20\\x6f\\x73\\x0a')\n"
    hits = _hits("text\n", py=py)
    assert _has(hits, "混淆代码") or _has(hits, "混淆执行")


def test_benign_skill_triggers_nothing():
    hits = _hits("用法见 references/guide.md。\n```bash\necho hello\n```\n")
    assert hits == []
