---
name: aioom
description: "AI-powered memory guardian for Windows. Manage system memory, kill high-risk processes, monitor in background, and view real-time Web GUI dashboard. Triggers: 内存占用高, 清理内存, 查看内存, 启动aioom, 打开aioom界面."
version: "2.1.0"
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
        - psutil
    emoji: "🦞"
    homepage: https://github.com/bettermen/aioom
---

# aioom — AI Memory Guardian Skill

> **AI 内存守护工具技能**
> 智能监控并清理 Windows 系统内存，基于 AI 评分机制识别高风险进程。

# aioom — AI内存守护工具技能

## 概述

aioom 是一个 AI 驱动的内存守护进程，参考 earlyoom 设计，通过 AI 评分机制智能识别内存泄漏进程并执行清理。支持 CLI 守护模式和 Web GUI 可视化面板两种形态。

**项目路径：** `C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom\`
**Web 端口：** `http://localhost:8866`
**日志文件：** `C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom.log`

---

## 调用方式自动检测

优先使用打包后的 exe，回退到 Python 脚本：

```python
import os, subprocess

PROJECT_DIR = r"C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom"
EXE_PATH    = r"C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom\dist\aioom.exe"
WEB_EXE     = r"C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom\dist\aioom-web.exe"
PY_AIOOM    = os.path.join(PROJECT_DIR, "aioom.py")
PY_WEB      = os.path.join(PROJECT_DIR, "web.py")

def get_runner(target="cli"):
    """返回 (cmd_prefix, cwd)"""
    if target == "cli":
        if os.path.exists(EXE_PATH):
            return [EXE_PATH], PROJECT_DIR
        return ["python", PY_AIOOM], PROJECT_DIR
    else:  # web
        if os.path.exists(WEB_EXE):
            return [WEB_EXE], PROJECT_DIR
        return ["python", PY_WEB], PROJECT_DIR
```

---

## 功能一：查看系统内存状态

使用 psutil 快速获取当前内存信息（无需启动 aioom 守护进程）：

```python
import psutil

mem = psutil.virtual_memory()
swap = psutil.swap_memory()
print(f"内存：{mem.percent:.1f}% 已用 | 可用 {mem.available / 1024**3:.2f} GB / 总计 {mem.total / 1024**3:.2f} GB")
print(f"SWAP：{swap.percent:.1f}% 已用")

# 列出前10个内存占用最高的进程
procs = sorted(psutil.process_iter(['pid','name','memory_percent']),
               key=lambda p: p.info['memory_percent'] or 0, reverse=True)
for p in procs[:10]:
    print(f"  PID {p.info['pid']:6d}  {p.info['memory_percent']:.1f}%  {p.info['name']}")
```

---

## 功能二：干跑分析（只分析不清理）

适合在执行清理前确认目标进程：

```bash
# CLI 方式
python "C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom\aioom.py" --dryrun -v
# 或 exe 方式
"C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom\dist\aioom.exe" --dryrun -v
```

- `--dryrun`：只打印分析结果，不执行任何 kill 操作
- `-v`：详细输出，显示每个进程的 AI 评分

---

## 功能三：启动守护进程（后台持续监控）

```python
import subprocess

cmd, cwd = get_runner("cli")
# 后台运行，日志输出到文件
proc = subprocess.Popen(
    cmd + ["--interval", "5", "-v"],
    cwd=cwd,
    stdout=open(r"C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom.log", "a"),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.CREATE_NO_WINDOW  # Windows 无窗口后台运行
)
print(f"aioom 守护进程已启动，PID: {proc.pid}")
```

常用参数：
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--interval N` | 检测间隔秒数 | 2 |
| `--dryrun` | 干跑模式 | 关闭 |
| `-v` | 详细输出 | 关闭 |
| `--config path` | 自定义配置文件 | config.toml |

---

## 功能四：停止 aioom 守护进程

```python
import psutil

killed = []
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmdline = ' '.join(proc.info['cmdline'] or [])
        if 'aioom' in cmdline.lower() and 'aioom-web' not in cmdline.lower():
            proc.terminate()
            killed.append(proc.info['pid'])
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
print(f"已停止 {len(killed)} 个 aioom 进程：{killed}")
```

---

## 功能五：打开 Web GUI 面板

```python
import subprocess, webbrowser, time

cmd, cwd = get_runner("web")
proc = subprocess.Popen(cmd, cwd=cwd, creationflags=subprocess.CREATE_NO_WINDOW)
time.sleep(2)  # 等待服务启动
webbrowser.open("http://localhost:8866")
print(f"Web GUI 已在 http://localhost:8866 启动，PID: {proc.pid}")
```

Web 面板功能：
- 实时内存/CPU 折线图（Chart.js）
- 进程列表及 AI 评分
- 一键终止高风险进程
- 配置阈值调整

---

## 配置文件说明

配置文件路径：`C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom\config.toml`

```toml
[threshold]
mem_percent = 85        # 触发清理的内存占用百分比
swap_percent = 80       # 触发清理的 SWAP 占用百分比

[ai]
term_confidence = 0.8   # SIGTERM 置信度阈值
kill_confidence = 0.95  # SIGKILL 置信度阈值

[protect]
ignore_patterns = ["sshd", "bash", "powershell", "explorer", "python.*aioom"]
ignore_root = true
protect_foreground = true

[notify]
log_file = "aioom.log"
verbose = true
```

修改配置时，直接编辑 config.toml，重启守护进程后生效。

---

## 常见场景处理

**场景：用户说"内存快满了，帮我清一下"**
1. 先用 psutil 展示当前内存状态
2. 运行 `--dryrun -v` 让用户确认目标进程
3. 征得确认后，正式启动（去掉 --dryrun）执行清理

**场景：用户说"启动aioom后台监控"**
1. 检查是否已有 aioom 进程在运行
2. 如有，提示用户当前状态
3. 如无，用后台模式启动守护进程

**场景：用户说"打开aioom界面"**
1. 直接执行功能五，启动 web.py 并打开浏览器

**场景：用户说"查看aioom日志"**
```python
log_path = r"C:\Users\PC\WorkBuddy\2026-05-15-task-3\aioom.log"
with open(log_path, encoding='utf-8') as f:
    lines = f.readlines()
print(''.join(lines[-50:]))  # 最后50行
```

---

## 功能六：存储清理（调用 storage-clean）

当用户说"帮我看看存储"、"清理磁盘垃圾"等，调用 storage-clean 技能：

```python
import subprocess, os, webbrowser

STORAGE_CLEAN_DIR = r"C:\Users\PC\.workbuddy\skills\storage-clean"
SCANNER_PY = os.path.join(STORAGE_CLEAN_DIR, "scripts", "scanner.py")
PYTHON_EXE = r"C:\Users\PC\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

def aioom_storage_scan():
    """运行存储扫描，生成 HTML 报告"""
    result = subprocess.run(
        [PYTHON_EXE, SCANNER_PY],
        cwd=STORAGE_CLEAN_DIR,
        capture_output=True,
        text=True,
        timeout=300
    )
    # 解析报告路径
    html_path = None
    for line in result.stdout.strip().split("\n"):
        if line.startswith("REPORT:"):
            html_path = line[7:].strip()
            break
    if html_path and os.path.exists(html_path):
        webbrowser.open(f"file://{html_path}")
        return True, html_path
    return False, result.stdout

def aioom_storage_clean(path, method="recycle"):
    """清理指定路径（调用 storage-clean/cleaner.py）"""
    CLEANER_PY = os.path.join(STORAGE_CLEAN_DIR, "scripts", "cleaner.py")
    result = subprocess.run(
        [PYTHON_EXE, CLEANER_PY, "--path", path, "--method", method],
        capture_output=True,
        text=True
    )
    import json
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"success": False, "message": result.stdout or result.stderr}
```

**调用流程：**
1. 用户说"帮我看看存储" → 调用 `aioom_storage_scan()` 生成报告
2. 用户在 HTML 报告中点击清理按钮 → 报告调用 `aioom_storage_clean(path, method)`
3. 清理完成后报告页面实时更新状态

**依赖：** storage-clean 技能已安装，psutil 已安装在 managed venv 中。
```
