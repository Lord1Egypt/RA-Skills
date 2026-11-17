# -*- coding: utf-8 -*-
"""回归：可执行代码文件（.py/.sh）里的凭据窃取必须判 EXTREME，不得被「引号内降级」吞掉。

背景（真实缺陷）：scan_segment 原本对「引号内的命中」统一做 P0→P1 降级，
该规则是为 .md 文档正文里的示范性写法设计的；但 .py 代码里的路径本就写在
引号内（open('/root/.ssh/id_rsa')），导致真实凭据窃取被误降为 P1、
语境被标成「文档提及」，最终只判 MEDIUM——安装闸门形同虚设。

修复：scan_segment 增加 is_code_file，整文件即代码时不降级。
本文件守住这个修复不被回退。
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import security_scan as ss  # noqa: E402

HEAD = "---\nname: t\ndescription: d\n---\n"


def _report(files: dict):
    """files: {相对路径: 内容}，返回 build_report 结果。"""
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "s"
        d.mkdir(parents=True)
        for rel, content in files.items():
            p = d / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        return ss.build_report(d)


def test_py_ssh_key_theft_is_extreme():
    """Python 里读取 ssh 私钥：必须 EXTREME（禁止安装）。"""
    rep = _report({"SKILL.md": HEAD, "run.py": "print(open('/root/.ssh/id_rsa').read())\n"})
    assert rep["risk_class"] == "EXTREME", f"实际={rep['risk_class']} hits={rep['hits']}"


def test_py_memory_md_theft_is_extreme():
    """Python 里读取 Agent 身份/记忆文件：必须 EXTREME。"""
    rep = _report({"SKILL.md": HEAD, "run.py": "data = open('MEMORY.md').read()\n"})
    assert rep["risk_class"] == "EXTREME", f"实际={rep['risk_class']} hits={rep['hits']}"


def test_py_windows_credential_path_is_extreme():
    """Windows 路径写法同样要抓到。"""
    code = 'open(r"C:\\\\Users\\\\x\\\\.ssh\\\\id_rsa").read()\n'
    rep = _report({"SKILL.md": HEAD, "run.py": code})
    assert rep["risk_class"] in ("EXTREME", "HIGH"), f"实际={rep['risk_class']} hits={rep['hits']}"


def test_doc_mention_stays_lenient():
    """对照：.md 正文里只是提到 ssh 路径（示范/警示），不应判 EXTREME。

    这条与上面成对存在——证明「代码 vs 文档」的语境区分确实生效，
    而不是无脑把所有命中都拉满。
    """
    rep = _report({"SKILL.md": HEAD + "注意：不要泄露 ~/.ssh/id_rsa 之类的私钥文件。\n"})
    assert rep["risk_class"] != "EXTREME", f"文档提及被误判为 EXTREME: {rep['hits']}"


def test_doc_fenced_block_keeps_quote_downgrade():
    """.md 代码围栏里的示范字符串，仍走引号降级（避免误报）。"""
    rep = _report({"SKILL.md": HEAD + "```bash\n# 示例：cat ~/.ssh/id_rsa\n```\n"})
    # 允许命中，但不应是 EXTREME（文档型文件保持宽容）
    assert rep["risk_class"] != "EXTREME", f"围栏示范被误判 EXTREME: {rep['hits']}"


def test_clean_skill_stays_low():
    """干净样本仍须 LOW，证明升级没有引入全面误报。"""
    rep = _report({"SKILL.md": HEAD + "# 用法\n", "run.py": "print('hello world')\n"})
    assert rep["risk_class"] == "LOW", f"实际={rep['risk_class']} hits={rep['hits']}"
