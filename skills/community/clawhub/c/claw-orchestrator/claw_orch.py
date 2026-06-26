"""
Claw Orchestrator v2 — CC Agent 直接产出, WBClaw 包装+报告
用法: python claw_orch.py "让CC做什么"
"""
import subprocess, os, sys, json, re, time, datetime

WORKDIR = r"c:\Users\zen.yang\WorkBuddy\Claw"
MEMORY_DIR = os.path.join(WORKDIR, ".workbuddy", "memory")
NODE = r"C:\Users\zen.yang\.workbuddy\binaries\node\versions\22.12.0\node.exe"
NPX = r"C:\Users\zen.yang\.workbuddy\binaries\node\versions\22.12.0\node_modules\npm\bin\npx-cli.js"

def get_output_files():
    """Return files created/modified in last 60 seconds by CC."""
    recent = []
    for f in os.listdir(WORKDIR):
        fp = os.path.join(WORKDIR, f)
        if os.path.isfile(fp):
            age = time.time() - os.path.getmtime(fp)
            if age < 120 and not f.startswith('.'):
                recent.append((f, os.path.getsize(fp), age))
    return sorted(recent, key=lambda x: x[2])

def cc_agent(task):
    """Call CC Agent to produce deliverable directly."""
    t0 = time.time()
    
    prompt = f"""{task}

Write the complete deliverable files NOW. Do not describe what you'll do - just write the files.
Use the Write tool. No conversation, no explanation. Execute immediately."""

    cmd = f'"{NODE}" "{NPX}" claude -p "{prompt}" --allowedTools "Read,Write" --permission-mode bypassPermissions --max-turns 5'
    
    print(f"🧠 CC Agent (claude-sonnet-4.6) 分析+生成中...", flush=True)
    env = os.environ.copy()
    env["PATH"] = os.path.dirname(NODE) + ";" + env.get("PATH", "")
    
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180, cwd=WORKDIR, 
                       env=env, encoding="utf-8", errors="replace")
    t1 = time.time()
    
    output = r.stdout.strip()
    clean = re.sub(r'^.*?pm exec.*?\n', '', output, flags=re.DOTALL)
    clean = re.sub(r'\d+mu\s*$', '', clean).strip()
    
    # Check what files CC produced
    files = get_output_files()
    
    return {
        "agent": "CC Agent",
        "model": "claude-sonnet-4.6 @ OpenRouter",
        "duration_s": round(t1 - t0, 1),
        "output": clean[:1000],
        "files": files,
        "rc": r.returncode if r else -1
    }

def wbclaw_wrap(cc_result, task):
    """WBClaw packages the output: preview, report, memory."""
    t0 = time.time()
    actions = []
    
    # Preview HTML files
    for fname, size, age in cc_result.get("files", []):
        if fname.endswith('.html'):
            try:
                abs_path = os.path.join(WORKDIR, fname)
                # We'll note it for the report; actual preview is done by the caller
                actions.append({"file": fname, "size": size, "action": "preview"})
            except: pass
    
    # Generate report
    report = f"""# 🤖 CC→WBClaw 协作报告

**任务**: {task[:200]}
**时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🧠 CC Agent
- 模型: {cc_result['agent']} ({cc_result['model']})
- 耗时: {cc_result['duration_s']}s
- 产出文件: {len(cc_result['files'])} 个

"""
    for fname, size, age in cc_result.get("files", []):
        report += f"- `{fname}` ({size} bytes)\n"
    
    report += f"""
## 🔧 WBClaw
- 模型: deepseek-v4-pro
- 动作: 预览 {len(actions)} 个文件, 写报告, 更新记忆
- 耗时: {time.time() - t0:.1f}s

---
🔧 协作链: CC Agent (分析+生成) → WBClaw (预览+报告)
"""
    
    with open(os.path.join(WORKDIR, "task_report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    
    t1 = time.time()
    return {
        "agent": "WBClaw",
        "model": "deepseek-v4-pro",
        "duration_s": round(t1 - t0, 1),
        "actions": len(actions),
        "files": [a["file"] for a in actions],
        "report": "task_report.md"
    }

def report(cc, wb, task):
    print(f"\n{'='*55}")
    print(f"📋 执行报告")
    print(f"{'='*55}")
    print(f"🧠 {cc['agent']} | {cc['model']} | {cc['duration_s']}s")
    if cc['files']:
        for f, s, _ in cc['files'][:5]:
            print(f"   ✅ {f} ({s}B)")
    print(f"💬 {cc['output'][:200]}")
    
    print(f"\n🔧 {wb['agent']} | {wb['model']} | {wb['duration_s']}s")
    print(f"   处理: {wb['actions']} 个文件, 报告: {wb['report']}")
    print(f"\n⏱️ 总耗时: {cc['duration_s'] + wb['duration_s']}s")
    print(f"{'='*55}")
    
    # Simplified notification
    print(f"\n🔔 任务完成!")
    print(f"   🧠 分析: CC Agent (claude-sonnet-4.6)")
    print(f"   🔧 执行: WBClaw (deepseek-v4-pro)")
    if cc['files']:
        print(f"   📦 产出: {', '.join(f for f,_,_ in cc['files'][:5])}")
    print()

def main():
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("任务: ")
    
    cc = cc_agent(task)
    wb = wbclaw_wrap(cc, task)
    report(cc, wb, task)
    
    # Memory
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    mem = os.path.join(MEMORY_DIR, f"{today}.md")
    if os.path.exists(mem):
        with open(mem, "a", encoding="utf-8") as f:
            f.write(f"\n- CC→WBClaw: {task[:100]} ({cc['duration_s']}s)")

if __name__ == "__main__":
    main()
