#!/usr/bin/env python3
"""token-stats regression test runner.

Runs non-destructive smoke/regression checks against available local Agent data.
Install, update, and uninstall are covered only with temporary HOME/PATH fixtures.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "token-stats.py"
PY = [sys.executable]


class Runner:
    def __init__(self, *, keep_exports: bool = False):
        self.keep_exports = keep_exports
        self.failures: list[str] = []
        self.export_dir = Path(tempfile.mkdtemp(prefix="token-stats-regression-export-"))

    def close(self):
        if self.keep_exports:
            print(f"\n导出文件保留在: {self.export_dir}")
        else:
            shutil.rmtree(self.export_dir, ignore_errors=True)

    def sep(self, title: str):
        print(f"\n{'#' * 78}\n# {title}\n{'#' * 78}\n")

    def run(self, name: str, cmd: list[str], *, timeout: int = 45, stdin: str | None = None,
            env: dict[str, str] | None = None, expect: list[str] | None = None,
            allow_fail: bool = False, cwd: Path | str | None = None) -> subprocess.CompletedProcess:
        print(f"$ {' '.join(str(c) for c in cmd)}")
        run_env = os.environ.copy()
        run_env.setdefault("PYTHONIOENCODING", "utf-8")
        if env:
            run_env.update(env)
        try:
            result = subprocess.run(
                [str(c) for c in cmd],
                capture_output=True,
                text=True,
                input=stdin,
                timeout=timeout,
                encoding="utf-8",
                errors="replace",
                env=run_env,
                cwd=str(cwd) if cwd is not None else None,
            )
        except subprocess.TimeoutExpired as exc:
            print("(超时)")
            self.failures.append(f"{name}: timeout after {timeout}s")
            return subprocess.CompletedProcess(cmd, 124, exc.stdout or "", exc.stderr or "")

        output = (result.stdout or "") + (result.stderr or "")
        print(output.strip() or "(无输出)")
        print()

        failed = result.returncode != 0 and not allow_fail
        if "读取失败" in output or "Traceback" in output:
            self.failures.append(f"{name}: unexpected runtime error output")
            failed = True
        if expect:
            for needle in expect:
                if needle not in output:
                    self.failures.append(f"{name}: missing expected output: {needle}")
                    failed = True
        if failed:
            self.failures.append(f"{name}: exit code {result.returncode}")
        return result

    def smoke(self):
        self.sep("1. 基础 CLI 与模块导入")
        self.run("py_compile", PY + ["-m", "py_compile", str(SCRIPT)] + [str(p) for p in sorted((ROOT / "token_stats").glob("*.py"))])
        self.run("monitor_unittest", PY + ["-m", "unittest", "test_monitor.py", "test_hermes.py"], cwd=ROOT)
        self.run("version", PY + [SCRIPT, "--version"], expect=["token-stats v"])
        self.run("help", PY + [SCRIPT, "--help"], expect=["命令大全", "--today", "--compare"])
        self.run("list_backends", PY + [SCRIPT, "--list-backends"], expect=["本机已安装"])
        self.codex_unit_regression()

    def codex_unit_regression(self):
        self.sep("1b. CodeX 统计口径离线回归")
        with tempfile.TemporaryDirectory(prefix="token-stats-codex-fixture-") as tmp:
            base = Path(tmp)
            codex_dir = base / ".codex"
            rollouts = codex_dir / "sessions" / "2026" / "05" / "31"
            rollouts.mkdir(parents=True)
            db = codex_dir / "state_5.sqlite"
            sqlite = sqlite3.connect(db)
            sqlite.execute(
                "CREATE TABLE threads ("
                "id TEXT PRIMARY KEY, model TEXT, model_provider TEXT, tokens_used INTEGER, "
                "rollout_path TEXT, updated_at INTEGER)"
            )
            rollout = rollouts / "rollout-main.jsonl"

            def evt(ts: str, total: dict | None):
                payload = {"type": "token_count", "info": None}
                if total is not None:
                    payload["info"] = {"total_token_usage": total}
                return {"timestamp": ts, "type": "event_msg", "payload": payload}

            rows = [
                evt("2026-05-30T09:50:00Z", None),
                evt("2026-05-30T10:00:00Z", {
                    "input_tokens": 100, "cached_input_tokens": 20,
                    "output_tokens": 10, "reasoning_output_tokens": 0,
                }),
                # Duplicate cumulative total: should not count as another call.
                evt("2026-05-30T10:01:00Z", {
                    "input_tokens": 100, "cached_input_tokens": 20,
                    "output_tokens": 10, "reasoning_output_tokens": 0,
                }),
                evt("2026-05-30T16:05:00Z", {
                    "input_tokens": 180, "cached_input_tokens": 50,
                    "output_tokens": 25, "reasoning_output_tokens": 5,
                }),
                evt("2026-05-30T16:06:00Z", None),
                evt("2026-05-30T16:07:00Z", {
                    "input_tokens": 250, "cached_input_tokens": 80,
                    "output_tokens": 40, "reasoning_output_tokens": 5,
                }),
            ]
            with rollout.open("w", encoding="utf-8") as f:
                for item in rows:
                    f.write(json.dumps(item) + "\n")
            sqlite.execute(
                "INSERT INTO threads VALUES (?,?,?,?,?,?)",
                ("main", "gpt-test", "openai", 999999, str(rollout), int(datetime(2026, 5, 31, 0, 10).timestamp())),
            )
            fallback_rollout = rollouts / "not-a-token-stream.jsonl"
            fallback_rollout.write_text('{"type":"session_meta"}\n', encoding="utf-8")
            sqlite.execute(
                "INSERT INTO threads VALUES (?,?,?,?,?,?)",
                ("fallback", "fallback-model", "openai", 321, str(fallback_rollout), int(datetime(2026, 5, 29, 12, 0).timestamp())),
            )
            sqlite.commit()
            sqlite.close()

            probe = base / "codex_probe.py"
            probe.write_text(
                "from token_stats.app import CodeXAgent, _codex_jsonl_cache\n"
                "from token_stats.dates import parse_date\n"
                "_codex_jsonl_cache.clear()\n"
                "a = CodeXAgent()\n"
                "def snap(label, lo=None, hi=None):\n"
                "    d = a.collect(from_ts=lo, to_ts=hi)\n"
                "    rows = sorted((pm['model'], pm['input'], pm['output'], pm['cache'], pm['calls']) for pm in (d.per_model or []))\n"
                "    print(label, d.token_mode, rows)\n"
                "snap('all')\n"
                "lo, hi = parse_date('2026-05-31'); snap('day', lo, hi)\n"
                "lo, hi = parse_date('2026-05-30'); snap('prev', lo, hi)\n"
                "lo, hi = parse_date('2026-05-28'); snap('empty', lo, hi)\n",
                encoding="utf-8",
            )
            env = {
                "HOME": str(base),
                "PYTHONPATH": str(ROOT),
            }
            result = self.run(
                "codex_fixture",
                PY + [probe],
                env=env,
                expect=[
                    "all total [('fallback-model', 321, 0, 0, 1), ('gpt-test', 170, 45, 80, 3)]",
                    "day split [('gpt-test', 90, 35, 60, 2)]",
                    "prev split [('gpt-test', 80, 10, 20, 1)]",
                    "empty split []",
                ],
            )
            if "999999" in ((result.stdout or "") + (result.stderr or "")):
                self.failures.append("codex_fixture: ranged JSONL data should not fall back to full tokens_used")

    def _detect_agents(self) -> list[str]:
        backends = self.run("detect_backends", PY + [SCRIPT, "--list-backends"]).stdout
        detected = []
        for name, marker in [
            ("claude-code", "Claude Code"),
            ("codex", "CodeX"),
            ("hermes", "Hermes"),
            ("openclaw", "OpenClaw"),
            ("reasonix", "Reasonix"),
            ("deepseek-tui", "DeepSeek TUI"),
        ]:
            if f"✅ {marker}" in backends:
                detected.append(name)
        return detected

    def _choose_primary_agent(self, agents: list[str]) -> str | None:
        for name in agents:
            result = self.run(f"probe_{name}", PY + [SCRIPT, "-a", name, "--month"], allow_fail=True)
            output = (result.stdout or "") + (result.stderr or "")
            if result.returncode == 0 and any(marker in output for marker in ("合计", "调用", "轮会话", "工具调用")):
                return name
        return agents[0] if agents else None

    def real_data(self):
        self.sep("2. README 核心命令回归")
        preferred = self._detect_agents()

        if not preferred:
            self.failures.append("real_data: no supported local Agent detected")
            return

        primary = self._choose_primary_agent(preferred)
        if not primary:
            self.failures.append("real_data: no primary Agent selected")
            return
        print(f"检测到可用 Agent: {', '.join(preferred)}；主回归 Agent: {primary}\n")
        today = date.today()
        month_start = today.replace(day=1)
        month_mid = month_start + (today - month_start) // 2
        second_half_start = month_mid + timedelta(days=1)

        snapshot_commands = [
            ("primary_all_history", ["-a", primary], ["📊"]),
            ("primary_now", ["-a", primary, "--now"], ["📊"]),
            ("primary_detail", ["-a", primary, "--detail"], ["📊"]),
            ("primary_today", ["-a", primary, "--today"], None),
            ("primary_yesterday", ["-a", primary, "--yesterday"], None),
            ("primary_week", ["-a", primary, "--week"], None),
            ("primary_last_7d", ["-a", primary, "--last-7d"], ["📊"]),
            ("primary_month", ["-a", primary, "--month"], ["📊"]),
            ("primary_year", ["-a", primary, "--year"], ["📊"]),
            ("primary_custom_range", ["-a", primary, "--from", month_start.isoformat(), "--to", today.isoformat()], ["📊"]),
        ]
        for name, args, expect in snapshot_commands:
            self.run(name, PY + [SCRIPT] + args, expect=expect)

        compare_commands = [
            ("compare_yesterday_today", ["-a", primary, "--compare", "--a", "yesterday", "--b", "today"]),
            ("compare_week", ["-a", primary, "--compare", "--a", "last-week", "--b", "this-week"]),
            ("compare_month", ["-a", primary, "--compare", "--a", "last-month", "--b", "this-month"]),
            ("compare_year", ["-a", primary, "--compare", "--a", "last-year", "--b", "this-year"]),
            ("compare_custom_dates", ["-a", primary, "--compare", "--a", month_start.isoformat(), "--b", today.isoformat()]),
            (
                "compare_custom_ranges",
                [
                    "-a", primary, "--compare",
                    "--a", f"{month_start.isoformat()}~{month_mid.isoformat()}",
                    "--b", f"{second_half_start.isoformat()}~{today.isoformat()}",
                ],
            ),
        ]
        for name, args in compare_commands:
            result = self.run(name, PY + [SCRIPT] + args)
            output = (result.stdout or "") + (result.stderr or "")
            if "对比" not in output and "两个时间段均无数据" not in output:
                self.failures.append(f"{name}: compare output missing expected summary")

        self.run("all_history", PY + [SCRIPT, "--all"], expect=["本机 Agent 统计汇总"])
        self.run("all_today", PY + [SCRIPT, "--all", "--today"], expect=["本机 Agent 统计汇总"])
        self.run("all_month", PY + [SCRIPT, "--all", "--month"], expect=["全部"])
        self.run("all_year", PY + [SCRIPT, "--all", "--year"], expect=["全部"])
        self.run("watch_all_rejected", PY + [SCRIPT, "--all", "--watch"], expect=["--watch 仅支持单个 Agent"])

        if len(preferred) > 1:
            self.run("multi_agent", PY + [SCRIPT, "-a", ",".join(preferred[:2]), "--today"], expect=["全部 Agent 总计"])
            self.run("watch_multi_rejected", PY + [SCRIPT, "-a", ",".join(preferred[:2]), "--watch"], expect=["--watch 仅支持单个 Agent"])

    def exports(self):
        self.sep("3. 导出回归")
        backends = self.run("detect_for_export", PY + [SCRIPT, "--list-backends"]).stdout
        primary = "codex" if "✅ CodeX" in backends else "claude-code"
        if f"✅ {'CodeX' if primary == 'codex' else 'Claude Code'}" not in backends:
            print("未检测到 CodeX/Claude Code，跳过单 Agent 导出；仍测试 --all 导出。")
            primary = None
        if primary:
            self.run("export_xlsx", PY + [SCRIPT, "-a", primary, "--month", "--export", self.export_dir], stdin="1\n")
            self.run("export_csv", PY + [SCRIPT, "-a", primary, "--today", "--export", self.export_dir], stdin="2\n")
            self.run("export_json", PY + [SCRIPT, "-a", primary, "--month", "--export", self.export_dir], stdin="3\n")
        self.run("export_all_xlsx", PY + [SCRIPT, "--all", "--year", "--export", self.export_dir], stdin="1\n")

        exported = list(self.export_dir.glob("*.xlsx")) + list(self.export_dir.glob("*.csv")) + list(self.export_dir.glob("*.json"))
        if not exported:
            self.failures.append("exports: no export files generated")
        else:
            print("导出文件:")
            for path in exported:
                print(f"  {path.name} ({path.stat().st_size} bytes)")
                if path.stat().st_size <= 0:
                    self.failures.append(f"exports: empty file {path.name}")

    def install_maintenance(self):
        self.sep("4. 安装/更新/卸载维护流回归（临时 HOME）")
        with tempfile.TemporaryDirectory(prefix="token-stats-install-home-") as home_tmp, \
                tempfile.TemporaryDirectory(prefix="token-stats-fake-bin-") as bin_tmp:
            home = Path(home_tmp)
            fake_bin = Path(bin_tmp)
            zshrc = home / ".zshrc"
            zshrc.write_text("# test shell rc\n", encoding="utf-8")
            bashrc = home / ".bashrc"
            legacy_block = (
                "\n# >>> token-stats PATH >>>\n"
                f"export PATH=\"$PATH:{home / '.local' / 'bin'}\"\n"
                "# <<< token-stats PATH <<<\n"
            )
            bashrc.write_text("# old shell rc\n" + legacy_block, encoding="utf-8")
            local_bin = home / ".local" / "bin"
            local_bin.mkdir(parents=True, exist_ok=True)
            clawhub_skill_dir = home / "skills" / "agent-usage-stats"
            clawhub_skill_dir.mkdir(parents=True, exist_ok=True)
            (clawhub_skill_dir / "token-stats.py").write_text("VERSION = \"0.0.1\"\n", encoding="utf-8")
            legacy_clawhub_skill_dir = home / ".clawhub" / "skills" / "agent-usage-stats"
            legacy_clawhub_skill_dir.mkdir(parents=True, exist_ok=True)
            (legacy_clawhub_skill_dir / "token-stats.py").write_text("VERSION = \"0.0.1\"\n", encoding="utf-8")
            local_bin_skill_dir = local_bin / "skills" / "agent-usage-stats"
            local_bin_skill_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SCRIPT, local_bin_skill_dir / "token-stats.py")
            shutil.copytree(ROOT / "token_stats", local_bin_skill_dir / "token_stats")
            shutil.copy2(ROOT / "model_prices.toml", local_bin_skill_dir / "model_prices.toml")
            fake_clawhub = fake_bin / "clawhub"
            fake_clawhub.write_text(
                "#!/bin/sh\n"
                "echo \"fake clawhub $@\"\n"
                "if [ \"$1\" = \"install\" ]; then\n"
                f"  echo \"✔ OK. Installed agent-usage-stats -> {local_bin_skill_dir}\"\n"
                "fi\n"
                "exit 0\n",
                encoding="utf-8",
            )
            fake_clawhub.chmod(0o755)
            env = {
                "HOME": str(home),
                "SHELL": "/bin/zsh",
                "PATH": f"{fake_bin}{os.pathsep}{local_bin}{os.pathsep}{os.environ.get('PATH', '')}",
            }

            setup = self.run(
                "setup_temp_home",
                PY + [SCRIPT, "setup"],
                env=env,
                expect=["已创建全局命令", "已添加到 PATH", "token-stats --version"],
            )
            install_dir = home / ".token-stats"
            wrapper = install_dir / "bin" / ("token-stats.cmd" if sys.platform == "win32" else "token-stats")
            if setup.returncode == 0:
                if not wrapper.exists():
                    self.failures.append("setup_temp_home: command wrapper was not created")
                if not (install_dir / "token-stats.py").exists():
                    self.failures.append("setup_temp_home: entry script was not copied")
                if sys.platform != "win32" and ".token-stats/bin" not in zshrc.read_text(encoding="utf-8"):
                    self.failures.append("setup_temp_home: PATH block missing from .zshrc")
                if sys.platform != "win32" and f"export PATH=\"{install_dir / 'bin'}:$PATH\"" not in zshrc.read_text(encoding="utf-8"):
                    self.failures.append("setup_temp_home: PATH block should prepend .token-stats/bin")
                if sys.platform != "win32" and "token-stats PATH" in bashrc.read_text(encoding="utf-8"):
                    self.failures.append("setup_temp_home: legacy PATH block still exists in .bashrc")

            setup_legacy_wrapper = local_bin / ("token-stats.cmd" if sys.platform == "win32" else "token-stats")
            if setup.returncode == 0 and setup_legacy_wrapper.exists():
                self.run(
                    "setup_legacy_wrapper_forwards",
                    [str(setup_legacy_wrapper), "--version"],
                    env=env,
                    expect=["token-stats v"],
                )

            if wrapper.exists():
                wrapper.unlink()
            legacy_wrapper = local_bin / ("token-stats.cmd" if sys.platform == "win32" else "token-stats")
            legacy_wrapper.parent.mkdir(parents=True, exist_ok=True)
            legacy_wrapper.write_text("legacy token-stats\n", encoding="utf-8")
            if sys.platform != "win32":
                legacy_wrapper.chmod(0o755)
            self.run(
                "update_repairs_wrapper",
                PY + [SCRIPT, "update"],
                env=env,
                cwd=local_bin,
                expect=[
                    "fake clawhub update agent-usage-stats",
                    f"Installed agent-usage-stats -> {local_bin_skill_dir}",
                    f"ClawHub 工作目录: {home}",
                    "已检查全局命令",
                    "已迁移旧版全局命令",
                    "hash -r",
                ],
            )
            if not wrapper.exists():
                self.failures.append("update_repairs_wrapper: wrapper was not repaired")
            if not legacy_wrapper.exists():
                self.failures.append("update_repairs_wrapper: legacy wrapper should remain as a forwarder")
            elif str(install_dir / "token-stats.py") not in legacy_wrapper.read_text(encoding="utf-8"):
                self.failures.append("update_repairs_wrapper: legacy wrapper should forward to install entry")
            if legacy_wrapper.exists():
                self.run(
                    "update_legacy_wrapper_forwards",
                    [str(legacy_wrapper), "--version"],
                    env=env,
                    expect=["token-stats v"],
                )
            if sys.platform != "win32" and f"export PATH=\"{install_dir / 'bin'}:$PATH\"" not in zshrc.read_text(encoding="utf-8"):
                self.failures.append("update_repairs_wrapper: PATH block should prepend .token-stats/bin")

            update_from_install_dir = self.run(
                "update_allows_inside_install_dir",
                PY + [SCRIPT, "update"],
                env=env,
                cwd=install_dir,
                expect=["fake clawhub update agent-usage-stats", "已检查全局命令"],
            )
            if "为避免删除或覆盖当前目录" in ((update_from_install_dir.stdout or "") + (update_from_install_dir.stderr or "")):
                self.failures.append("update_allows_inside_install_dir: update should not block inside install dir")

            blocked_install_uninstall = self.run(
                "uninstall_blocks_inside_install_dir",
                PY + [SCRIPT, "--uninstall"],
                env=env,
                cwd=install_dir,
                expect=["为避免删除或覆盖当前目录", "已停止卸载", str(install_dir), "cd ~"],
            )
            if blocked_install_uninstall.returncode == 0 and not install_dir.exists():
                self.failures.append("uninstall_blocks_inside_install_dir: install cwd should not be removed")

            blocked_update = self.run(
                "update_blocks_inside_managed_dir",
                PY + [SCRIPT, "update"],
                env=env,
                cwd=local_bin_skill_dir,
                expect=["为避免删除或覆盖当前目录", "已停止更新", str(local_bin_skill_dir), "cd ~"],
            )
            if blocked_update.returncode == 0 and "fake clawhub update" in ((blocked_update.stdout or "") + (blocked_update.stderr or "")):
                self.failures.append("update_blocks_inside_managed_dir: clawhub should not run from managed dir")

            blocked_uninstall = self.run(
                "uninstall_blocks_inside_managed_dir",
                PY + [SCRIPT, "--uninstall"],
                env=env,
                cwd=local_bin_skill_dir,
                expect=["为避免删除或覆盖当前目录", "已停止卸载", str(local_bin_skill_dir), "cd ~"],
            )
            if blocked_uninstall.returncode == 0 and not local_bin_skill_dir.exists():
                self.failures.append("uninstall_blocks_inside_managed_dir: managed cwd should not be removed")

            self.run(
                "uninstall_temp_home",
                PY + [SCRIPT, "--uninstall"],
                env=env,
                expect=["卸载完成"],
            )
            if wrapper.exists():
                self.failures.append("uninstall_temp_home: wrapper still exists")
            if legacy_wrapper.exists():
                self.failures.append("uninstall_temp_home: legacy wrapper still exists")
            if install_dir.exists():
                self.failures.append("uninstall_temp_home: install dir still exists")
            if clawhub_skill_dir.exists():
                self.failures.append("uninstall_temp_home: ClawHub skill dir still exists")
            if legacy_clawhub_skill_dir.exists():
                self.failures.append("uninstall_temp_home: legacy ClawHub skill dir still exists")
            if local_bin_skill_dir.exists():
                self.failures.append("uninstall_temp_home: local-bin ClawHub skill dir still exists")
            if sys.platform != "win32" and "token-stats PATH" in zshrc.read_text(encoding="utf-8"):
                self.failures.append("uninstall_temp_home: PATH block still exists")
            if sys.platform != "win32" and "token-stats PATH" in bashrc.read_text(encoding="utf-8"):
                self.failures.append("uninstall_temp_home: legacy PATH block still exists in .bashrc")

    def summary(self) -> int:
        self.sep("测试结论")
        if self.failures:
            print("发现问题:")
            for item in self.failures:
                print(f"  - {item}")
            return 1
        print("所有回归检查通过。")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run token-stats regression tests")
    parser.add_argument("--keep-exports", action="store_true", help="保留临时导出文件")
    args = parser.parse_args()

    runner = Runner(keep_exports=args.keep_exports)
    try:
        runner.smoke()
        runner.real_data()
        runner.exports()
        runner.install_maintenance()
        return runner.summary()
    finally:
        runner.close()


if __name__ == "__main__":
    raise SystemExit(main())
