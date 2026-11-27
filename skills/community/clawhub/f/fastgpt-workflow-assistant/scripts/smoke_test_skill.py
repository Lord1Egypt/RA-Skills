#!/usr/bin/env python3
"""验证 FastGPT工作流生成助手导入包的结构、版本和核心脚本。"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_NAME = "fastgpt-workflow-assistant"
EXPECTED_VERSION = "3.0.2"


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, *arguments], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=30,
    )
    if result.returncode:
        raise AssertionError(
            f"命令失败({result.returncode}): {arguments}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def main() -> int:
    manifest = json.loads((ROOT / "assets" / "skill-version.json").read_text(encoding="utf-8-sig"))
    assert manifest["skill_name"] == EXPECTED_NAME
    assert manifest["version"] == EXPECTED_VERSION

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8-sig")
    agent_text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8-sig")
    release = json.loads((ROOT / "assets" / "发布清单示例.json").read_text(encoding="utf-8-sig"))
    assert f"当前版本 {EXPECTED_VERSION}" in skill_text
    assert f"v{EXPECTED_VERSION}" in skill_text and f"v{EXPECTED_VERSION}" in agent_text
    assert release["skill_version"] == EXPECTED_VERSION
    import re
    for ref in (ROOT / "references").glob("*.md"):
        for declared in re.findall(r"(?:本技能|当前技能版本|当前版本)[：: ]+`?[vV]?(\d+\.\d+\.\d+)", ref.read_text(encoding="utf-8")):
            assert declared == EXPECTED_VERSION, (ref.name, declared)


    required = [
        "check_skill_version.py", "create_workflow_from_template.py",
        "validate_fastgpt_workflow.py", "audit_fastgpt_kb.py",
        "compare_fastgpt_roundtrip.py", "generate_test_cases.py",
        "evaluate_agent_results.py", "run_share_api_regression.py",
        "generate_random_test_cases.py", "compare_workflow_versions.py",
        "configure_file_input.py", "summarize_chat_export.py",
        "inspect_expert_versions.py", "check_route_contract.py", "check_http_contract.py", "prepare_share_window_test.py", "run_share_url_regression.py", "verify_expert_install.py",
    ]
    for filename in required:
        script = ROOT / "scripts" / filename
        assert script.is_file(), filename
        run(str(script), "--help")

    assert (ROOT / "scripts" / "execution_binding_checks.py").is_file()
    assert (ROOT / "assets" / "execution-binding-contract.example.json").is_file()
    assert (ROOT / "assets" / "http-execution-contract.example.json").is_file()
    assert (ROOT / "assets" / "http-failure-behavior.example.json").is_file()
    assert (ROOT / "references" / "免登录窗口测试与引导.md").is_file()
    assert (ROOT / "references" / "分享URL直接回归入口.md").is_file()
    assert (ROOT / "assets" / "share-instances.example.json").is_file()
    assert (ROOT / "scripts" / "run_code_contract.js").is_file()
    assert (ROOT / "references" / "文件输入与多文件审核.md").is_file()
    assert (ROOT / "references" / "桌面Agent分发.md").is_file()
    assert (ROOT / "references" / "对话日志驱动优化.md").is_file()

    with tempfile.TemporaryDirectory() as directory:
        workflow = Path(directory) / "minimal.json"
        run(str(ROOT / "scripts" / "create_workflow_from_template.py"), str(workflow))
        run(str(ROOT / "scripts" / "validate_fastgpt_workflow.py"), str(workflow), "--strict")
        bound_workflow = Path(directory) / "bound.json"
        bound_contract = Path(directory) / "bound-contract.json"
        bound_workflow.write_text(json.dumps({"nodes": [
            {"nodeId": "start", "outputs": [{"id": "userChatInput", "key": "userChatInput"}]},
            {"nodeId": "echo", "flowNodeType": "code", "inputs": [
                {"key": "code", "value": "function main({input}){return {text:input}}"},
                {"key": "input", "renderTypeList": ["reference"], "value": ["start", "userChatInput"]}]
            }]}), encoding="utf-8")
        bound_contract.write_text(json.dumps({"cases": [{"name": "extracted bound smoke", "mode": "bound", "node_id": "echo", "seeds": {"start": {"userChatInput": "bound-ok"}}, "required_inputs": {"echo": ["input"]}, "expected": {"text": "bound-ok"}}]}), encoding="utf-8")
        node = shutil.which("node")
        assert node, "Node.js required for bound smoke"
        executed = subprocess.run([node, str(ROOT / "scripts" / "run_code_contract.js"), str(bound_workflow), str(bound_contract)], capture_output=True, text=True, encoding="utf-8", timeout=20)
        assert executed.returncode == 0, executed.stdout + executed.stderr
        assert json.loads(executed.stdout)["passed"]
        # Also exercise imports of shared compatibility helpers in extracted packages.
        run(str(ROOT / "scripts" / "compare_fastgpt_roundtrip.py"), str(workflow), str(workflow), "--strict")

    print(f"OK: {EXPECTED_NAME} v{EXPECTED_VERSION} 精简生产包冒烟检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
