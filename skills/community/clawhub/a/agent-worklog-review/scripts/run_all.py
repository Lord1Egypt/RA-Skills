#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键跑完整链路：扫描 → 提取任务 → 分类 → token 统计 → 刷新报告 → Excel 导出。

适配器架构：extract_tasks.py 与 stat_tokens.py 内部遍历 scripts/adapters/，
新增 Agent 只需加适配器文件，不用改本脚本。
缺失的 agent 静默跳过；dsh 压缩会话自动用带 zstandard 的 Python 处理。

交互模式：`python run_all.py --interactive`（或 WORKLOG_PROMPT=1）。
仅在 stdin 是 TTY 时才会提示，默认静默，后台/CI 跑不受影响。
"""
import os, sys, subprocess, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import out_dir, detect_python_with_zstd, ask, interactive_enabled

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
PY = sys.executable
OUT = out_dir()
ZSTD_PY = detect_python_with_zstd()

# --interactive 开关：透传给子进程（子进程继承 os.environ）
if "--interactive" in sys.argv:
    os.environ["WORKLOG_PROMPT"] = "1"
INTERACTIVE = interactive_enabled()


def run(script, python=None, desc=""):
    exe = python or PY
    path = os.path.join(SCRIPTS, script)
    print(f"\n{'='*60}\n>>> {desc}  [{os.path.basename(exe)}]\n{'='*60}", flush=True)
    try:
        r = subprocess.run([exe, path], capture_output=True, text=True, timeout=1800)
        for line in (r.stdout or "").strip().splitlines()[-20:]:
            print("  " + line, flush=True)
        if r.returncode != 0:
            for line in (r.stderr or "").strip().splitlines()[-10:]:
                print("  [ERR] " + line, flush=True)
            print(f"  !! {script} 退出码 {r.returncode}", flush=True)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  !! {script} 超时", flush=True)
        return False


def probe_wsl():
    """独立进程探测 WSL 路径（带超时）。交互模式下不捕获输出并延长超时。"""
    print("\n>>> 探测 WSL 路径（独立进程）...", flush=True)
    cmd = [PY, os.path.join(SCRIPTS, "probe_wsl.py")]
    timeout = 300 if INTERACTIVE else 40
    try:
        if INTERACTIVE:
            # 交互模式：不捕获输出，让用户能看到提示并输入
            r = subprocess.run(cmd, timeout=timeout)
            ok = r.returncode == 0
        else:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            for line in (r.stdout or "").strip().splitlines()[:8]:
                print("  " + line, flush=True)
            ok = r.returncode == 0
        if not ok:
            raise RuntimeError("probe 退出码非 0")
    except Exception as e:
        print(f"  WSL 探测跳过: {str(e)[:80]}", flush=True)
        print("  可设 WORKLOG_WSL_USER / WORKLOG_WSL_DISTRO 环境变量，或用 --interactive 手动输入", flush=True)
        with open(os.path.join(SCRIPTS, "_env_paths_cache.json"), "w", encoding="utf-8") as f:
            json.dump({"wsl_homes": []}, f)


def interactive_config():
    """交互模式下补齐项目规则与额外根目录配置。"""
    if not INTERACTIVE:
        return
    local = os.path.join(ROOT, "config", "local")
    os.makedirs(local, exist_ok=True)

    # 1) 项目规则缺失 → 提示项目名
    rules = os.path.join(local, "project_rules.local.json")
    if not os.path.isfile(rules):
        names = ask("要重点统计的项目名（逗号分隔，回车跳过）")
        if names:
            projects = [{"name": n.strip(), "patterns": [n.strip()]}
                        for n in names.replace("，", ",").split(",") if n.strip()]
            with open(rules, "w", encoding="utf-8") as f:
                json.dump({"_说明": "交互生成的项目分类规则", "projects": projects},
                          f, ensure_ascii=False, indent=2)
            print(f"  已写入 {rules}", flush=True)

    # 2) Agent 库路径特殊 → 提示额外根目录
    extra = os.path.join(local, "extra_roots.json")
    scan = os.path.join(OUT, "agent_scan_report.json")
    if os.path.isfile(scan) and not os.path.isfile(extra):
        try:
            agents = json.load(open(scan, encoding="utf-8")).get("agents", {})
            empty = [a for a, v in agents.items()
                     if v.get("roots") and not v.get("session_files")]
        except Exception:
            empty = []
        if empty:
            print(f"以下 Agent 检测到目录但未找到会话文件：{', '.join(empty)}", flush=True)
            path = ask("若有会话库在非标准路径，输入其根目录（回车跳过）",
                       validator=lambda x: os.path.isdir(x))
            if path:
                with open(extra, "w", encoding="utf-8") as f:
                    json.dump({"roots": [path]}, f, ensure_ascii=False, indent=2)
                print(f"  已写入 {extra}（将并入扫描根目录，需重跑生效）", flush=True)


def main():
    print(f"输出目录: {OUT}")
    print(f"zstd Python: {ZSTD_PY or '未找到（dsh 压缩会话将跳过）'}")
    print(f"交互模式: {'开启' if INTERACTIVE else '关闭（默认静默）'}"
          + ("　提示：--interactive 开启" if not INTERACTIVE else ""), flush=True)

    probe_wsl()
    run("scan_agents.py", desc="Step 1/6 扫描所有 Agent")
    interactive_config()  # 扫描后再提示，才能知道哪些 agent 无会话文件
    run("extract_tasks.py", python=ZSTD_PY or PY, desc="Step 2/6 提取会话任务（含 dsh zstd）")
    run("classify_tasks.py", desc="Step 3/6 任务分类与汇总")
    run("stat_tokens.py", python=ZSTD_PY or PY, desc="Step 4/6 统计 token 消耗")
    run("classify_tasks.py", desc="Step 5/6 刷新报告（含 token 章节）")
    run("export_excel.py", desc="Step 6/6 导出 Excel 工作簿（需 openpyxl）")

    print(f"\n{'='*60}\n全部完成。交付物在: {OUT}")
    for f in ["agent_scan_report.json", "all_tasks.jsonl", "tasks_classified.jsonl",
              "task_analysis_report.md", "token_usage.jsonl", "token_report.md",
              "agent_worklog.xlsx"]:
        p = os.path.join(OUT, f)
        if os.path.isfile(p):
            print(f"  ✓ {f}  ({os.path.getsize(p)//1024} KB)")


if __name__ == "__main__":
    main()
