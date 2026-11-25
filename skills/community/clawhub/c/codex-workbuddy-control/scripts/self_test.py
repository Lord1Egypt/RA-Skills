#!/usr/bin/env python3
"""Isolated regression tests for codex-workbuddy-control."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
CLI = SKILL / "scripts" / "wb_bus.py"
PASS = 0


class Failure(RuntimeError):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def run(arguments: list[str], expected: int = 0) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(arguments, text=True, capture_output=True, env=env, check=False)
    if result.returncode != expected:
        raise Failure(
            f"命令退出码应为 {expected}，实际 {result.returncode}\n"
            f"CMD={shlex.join(arguments)}\nSTDOUT={result.stdout}\nSTDERR={result.stderr}"
        )
    return result


def json_output(result: subprocess.CompletedProcess[str]) -> dict:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise Failure(f"输出不是 JSON: {exc}\n{result.stdout}") from exc


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_init_and_layout(bus: Path) -> None:
    global PASS
    ledger = bus.parent / "custom-ledger.md"
    reviews = bus.parent / "custom-reviews"
    result = run(
        [
            sys.executable,
            str(CLI),
            "--root",
            str(bus),
            "--ledger",
            str(ledger),
            "--review-dir",
            str(reviews),
            "init",
        ]
    )
    data = json_output(result)
    check(data["status"] == "INITIALIZED", "init 状态错误")
    for name in ("queue", "tasks", "candidates", "待验证", "已验证", "返工"):
        check((bus / name).is_dir(), f"缺少目录 {name}")
    check(ledger.is_file(), "缺少自定义共享台账")
    check(list(reviews.glob("*.md")), "缺少自定义月度复盘")
    status = json_output(run([sys.executable, str(CLI), "status", "--root", str(bus)]))
    check(status["ledger"] == str(ledger.resolve()), "台账路径未持久化")
    check(status["review_dir"] == str(reviews.resolve()), "复盘路径未持久化")
    PASS += 1


def test_dispatch_claim_complete(bus: Path) -> None:
    global PASS
    task_id = "WB-20990101-001"
    result = run(
        [
            sys.executable,
            str(CLI),
            "--root",
            str(bus),
            "dispatch",
            "--id",
            task_id,
            "--title",
            "隔离执行任务",
            "--goal",
            "验证任务建包、领取和完成",
            "--acceptance",
            "回执存在且台账更新",
        ]
    )
    data = json_output(result)
    package = Path(data["package"])
    check(package.is_file(), "任务包未生成")
    check("WorkBuddy 执行；Codex 验收" in package.read_text(encoding="utf-8"), "任务角色错误")
    check((bus / "queue" / "pending" / f"{task_id}.json").is_file(), "任务未入队")
    claimed = json_output(run([sys.executable, str(CLI), "--root", str(bus), "claim", "--worker", "self-test"]))
    check(claimed["task_id"] == task_id and claimed["status"] == "IN_PROGRESS", "claim 结果错误")
    receipt = Path(claimed["receipt_path"])
    receipt.write_text("# 回执\n\n结论：PASS\n\n- 隔离测试证据\n", encoding="utf-8")
    done = json_output(run([sys.executable, str(CLI), "--root", str(bus), "complete", "--id", task_id]))
    check(done["result"] == "COMPLETED", "普通任务完成状态错误")
    check((bus / "queue" / "completed" / f"{task_id}.json").is_file(), "任务未移入 completed")
    ledger = (bus.parent / "custom-ledger.md").read_text(encoding="utf-8")
    check(f"`{task_id}`" in ledger and "`COMPLETED`" in ledger, "台账未更新普通任务")

    recovered_id = "WB-20990101-002"
    recovered = json_output(
        run(
            [
                sys.executable,
                str(CLI),
                "--root",
                str(bus),
                "dispatch",
                "--id",
                recovered_id,
                "--title",
                "回执恢复任务",
                "--goal",
                "验证回执已存在时仍可完成",
            ]
        )
    )
    recovered_receipt = Path(recovered["package"]).parent / "回执包.md"
    recovered_receipt.write_text("# 回执\n\n结论：PASS\n\n- 已存在回执的恢复测试\n", encoding="utf-8")
    recovered_claim = json_output(
        run([sys.executable, str(CLI), "--root", str(bus), "claim", "--worker", "self-test"])
    )
    check(
        recovered_claim["task_id"] == recovered_id and recovered_claim["status"] == "RECEIPT_EXISTS",
        "已有回执的 pending 任务未正确迁移",
    )
    recovered_done = json_output(
        run([sys.executable, str(CLI), "--root", str(bus), "complete", "--id", recovered_id])
    )
    check(recovered_done["result"] == "COMPLETED", "已有回执的任务无法接续完成")
    PASS += 1


def test_forward_verification(bus: Path, root: Path) -> None:
    global PASS
    changed = root / "changed.py"
    changed.write_text("print('verified')\n", encoding="utf-8")
    command = f"{shlex.quote(sys.executable)} -c \"print('VERIFY_OK')\""
    task_id = "WBV-20990101-001"
    result = run(
        [
            sys.executable,
            str(CLI),
            "--root",
            str(bus),
            "verify",
            "--id",
            task_id,
            "--title",
            "只读验收回归",
            "--goal",
            "复跑命令并保持文件哈希",
            "--changed-file",
            str(changed),
            "--cwd",
            str(root),
            "--command",
            command,
            "--evidence",
            "隔离自测 EXIT=0",
            "--acceptance",
            "结论为 WB_PASS",
        ]
    )
    package = Path(json_output(result)["package"])
    text = package.read_text(encoding="utf-8")
    check(sha256(changed) in text, "验收包缺少 SHA-256")
    check("WB_PASS" in text and "不得修改代码" in text, "验收包结论字段缺失或边界措辞异常")
    claimed = json_output(run([sys.executable, str(CLI), "--root", str(bus), "claim", "--worker", "self-test"]))
    check(claimed["kind"] == "verification", "验收类型错误")
    receipt = Path(claimed["receipt_path"])
    receipt.write_text("# 回执\n\n- 实际复跑：VERIFY_OK\n- EXIT=0\n\n结论：WB_PASS\n", encoding="utf-8")
    done = json_output(run([sys.executable, str(CLI), "--root", str(bus), "complete", "--id", task_id]))
    check(done["result"] == "WB_PASS", "WBV 结论未保存")
    PASS += 1


def test_rejections(bus: Path, root: Path) -> None:
    global PASS
    changed = root / "reject.py"
    changed.write_text("print('reject')\n", encoding="utf-8")
    missing = run(
        [
            sys.executable,
            str(CLI),
            "--root",
            str(bus),
            "verify",
            "--id",
            "WBV-20990101-002",
            "--title",
            "无命令",
            "--goal",
            "拒绝",
            "--changed-file",
            str(changed),
            "--cwd",
            str(root),
        ],
        expected=2,
    )
    check("至少提供一个可复跑" in missing.stderr, "无命令保护缺失")
    nonportable = run(
        [
            sys.executable,
            str(CLI),
            "--root",
            str(bus),
            "verify",
            "--id",
            "WBV-20990101-003",
            "--title",
            "不可移植命令",
            "--goal",
            "拒绝",
            "--changed-file",
            str(changed),
            "--cwd",
            str(root),
            "--command",
            "printf x | rg x",
        ],
        expected=2,
    )
    check("`rg`" in nonportable.stderr, "不可移植命令保护缺失")
    PASS += 1


def test_candidate(bus: Path, root: Path) -> None:
    global PASS
    task_id = "WBC-20990101-001"
    candidate = root / "candidate"
    candidate.mkdir()
    request = candidate / "验证请求.md"
    request.write_text(
        "# 验证请求\n\n- 编号：WBC-20990101-001\n- 候选目录：隔离目录\n- 数据边界：仅测试\n",
        encoding="utf-8",
    )
    registered = json_output(
        run(
            [
                sys.executable,
                str(CLI),
                "--root",
                str(bus),
                "verify",
                "--id",
                task_id,
                "--title",
                "隔离候选",
                "--candidate-dir",
                str(candidate),
            ]
        )
    )
    check(registered["status"] == "WAITING_VERIFY", "候选状态错误")
    check((bus / "待验证" / f"{task_id}.md").is_file(), "缺少待验证入口")
    completed = json_output(
        run(
            [
                sys.executable,
                str(CLI),
                "--root",
                str(bus),
                "complete",
                "--id",
                task_id,
                "--result",
                "PASS",
                "--evidence",
                "Codex 实际复跑，EXIT=0",
            ]
        )
    )
    check(completed["status"] == "VERIFIED", "候选 PASS 未进入 verified")
    result_file = candidate / "验证结果.md"
    check(result_file.is_file() and "PASS" in result_file.read_text(encoding="utf-8"), "验证结果未生成")
    check((bus / "已验证" / f"{task_id}.md").is_file(), "验证入口未移动")
    PASS += 1


def test_package_contract() -> None:
    global PASS
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', skill_text, re.M)
    check(match is not None, "SKILL.md 缺少 description")
    description = match.group(1).strip().strip('"\'')
    check(len(description) <= 45, f"description 超过 45 字: {len(description)}")
    check((SKILL / "SKILL.md").stat().st_size <= 8192, "SKILL.md 超过 8 KB")

    required = [
        "README.md",
        "README.en.md",
        "manifest.json",
        "_meta.json",
        "agents/openai.yaml",
        "references/architecture.md",
        "references/setup.md",
        "references/commands.md",
        "references/troubleshooting.md",
        "references/开工提示词.md",
        "references/step-prompts.md",
        "scripts/wb_bus.py",
        "scripts/self_test.py",
        "templates/任务包.md",
        "templates/回执包.md",
        "templates/验证请求.md",
        "templates/验证结果.md",
        "LICENSE.md",
        "NOTICE.md",
        "CHANGELOG.md",
    ]
    for relative in required:
        path = SKILL / relative
        check(path.is_file() and path.stat().st_size > 0, f"缺少或为空: {relative}")

    start_prompt = (SKILL / "references" / "开工提示词.md").read_text(encoding="utf-8")
    step_prompt = (SKILL / "references" / "step-prompts.md").read_text(encoding="utf-8")
    check("WBV-YYYYMMDD-NNN" in start_prompt and "WB_PASS" in start_prompt, "开工提示词缺少验收流程")
    check("WBC-YYYYMMDD-NNN" in start_prompt and "WBC-YYYYMMDD-NNN" in step_prompt, "提示词缺少候选流程")
    check("claim --worker workbuddy" in start_prompt, "开工提示词缺少自动领取命令")

    private_path = re.compile(r"/" + r"Users/[^/\s]+")
    home_path = re.compile(r"/" + r"home/[^/\s]+")
    secret_markers = [
        "-----BEGIN " + "PRIVATE " + "KEY-----",
        "AK" + "IA",
        "sk-" + "live_",
    ]
    for path in SKILL.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".zip"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        check(not private_path.search(text), f"包含机器专属用户路径: {path.relative_to(SKILL)}")
        check(not home_path.search(text), f"包含机器专属 home 路径: {path.relative_to(SKILL)}")
        for marker in secret_markers:
            check(marker not in text, f"疑似密钥标记: {path.relative_to(SKILL)}")
    PASS += 1


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="wb-bus-selftest-") as temporary:
            root = Path(temporary)
            bus = root / "bus"
            test_init_and_layout(bus)
            test_dispatch_claim_complete(bus)
            test_forward_verification(bus, root)
            test_rejections(bus, root)
            test_candidate(bus, root)
            test_package_contract()
            status = json_output(run([sys.executable, str(CLI), "--root", str(bus), "status"]))
            check(status["counts"]["pending"] == 0, "隔离测试后 pending 非 0")
            check(status["counts"]["claimed"] == 0, "隔离测试后 claimed 非 0")
            check(status["counts"]["waiting_verify"] == 0, "隔离测试后待验证非 0")
        print(f"SELF_TEST_PASS {PASS}/{PASS}")
        return 0
    except Failure as exc:
        print(f"SELF_TEST_FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
