---
name: claw-markdown-preview
description: Local Markdown preview skill. Trigger when the user explicitly asks to preview a markdown file — e.g. "preview this markdown file", "open markdown preview", "markdown preview", or the Chinese "预览这个 markdown 文件" / "打开 markdown 预览" / "markdown 预览一下".
version: 1.4.15
metadata:
  openclaw:
    emoji: "📄"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["python3"]
    install: []
    permissions:
      - filesystem:read
      - filesystem:write
      - network:localhost
      - process:spawn
---

# Markdown 编辑、多风格预览 / Markdown Editing & Multi-style Preview

通过浏览器编辑、预览AI生成的 Markdown 内容、用户本地 MarkDown 文件。支持多主题风格切换、实时编辑、富文本复制（可粘贴到公众号/知乎）、图片粘贴  

Edit & preview AI-generated or local Markdown in the browser. Multi-theme switching, live editing, rich-text copy (for WeChat/Zhihu), and image paste.

## 触发方式 / Trigger

当用户明确请求预览 Markdown 文件时触发，例如："预览这个 markdown 文件" / "打开 markdown 预览" / "markdown 预览一下"。非 Markdown 预览请求（如普通文本渲染、图片查看）不触发。  

Triggers when the user explicitly asks to preview a Markdown file, e.g. "预览这个 markdown 文件" / "打开 markdown 预览" / "markdown 预览一下". Not for generic text rendering or image viewing.

## 执行入口

**前提检查：**
- 确认目标文件路径存在且为 `.md` 文件
- 确认 `scripts/preview_server.py` 存在且可用（路径相对于技能目录）

**执行（两步，替换 `<MD_FILE_PATH>` 后运行）：**

**第 1 步 —— 以独立进程方式启动服务（关键：必须脱离 WorkBuddy 托管后台任务树，否则对话闲置约 20 分钟服务会被回收而"断开"。脱离由 python 内部跨平台实现，不依赖 shell `setsid`）：**

```bash
# 单实例清理：只终止上一次本技能启动的预览实例（PID 文件精确定位），不误伤其他进程。整条命令以 python3 常驻结尾。（脱离托管由 python 内部实现跨平台双 fork/detach，不依赖 shell setsid，多行 if 块部分环境识别不到 python3）。
[ -f /tmp/claw-markdown-preview.pid ] && OLD_PID=$(cat /tmp/claw-markdown-preview.pid 2>/dev/null) && [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null && kill "$OLD_PID" 2>/dev/null; rm -f /tmp/claw-markdown-preview.pid; python3 scripts/preview_server.py --file "<MD_FILE_PATH>" --no-open --heartbeat-timeout 7200 > /tmp/claw-md-preview.log 2>&1
```

> 关键：脱离托管由 `preview_server.py` **内部自行实现**（macOS/Linux 用 `os.fork() + os.setsid()` 双 fork 成为独立 session leader，Windows 用 `subprocess.Popen` + `DETACHED_PROCESS` 启动独立实例），脚本自动判断、不依赖 shell 命令。效果与 shell `setsid` 一致：服务脱离 WorkBuddy 托管后台任务树，不被"对话闲置回收"机制杀掉（实测托管任务约 20 分钟闲置即回收子进程）。服务因此常驻，离开多久 / 切窗口 / 睡眠都不受影响。跨平台通用，无需 `setsid` / `start /B` 等 shell 命令。

**第 2 步 —— 探测端口并打开浏览器（普通命令即可）：**

```bash
# 就绪轮询：服务绑定端口后即可响应，不必固定等待 2 秒（跨平台通用，不依赖任何运行时专属能力）
PORT=8765
for i in $(seq 1 20); do
  if curl -s -o /dev/null -w '%{http_code}' --max-time 1 "http://127.0.0.1:$PORT/" | grep -q 200; then
    break
  fi
  sleep 0.1
done
# 若默认端口仍未就绪（如端口冲突），从日志提取实际端口
if ! curl -s -o /dev/null -w '%{http_code}' --max-time 1 "http://127.0.0.1:$PORT/" | grep -q 200; then
  PORT=$(grep -oE '127\.0\.0\.1:[0-9]+' /tmp/claw-md-preview.log | head -1 | sed 's/.*://')
fi
# 记录本次实例 PID，供下次重启时精准终止（替代 pkill 全杀）
lsof -iTCP:$PORT -sTCP:LISTEN -t | head -1 > /tmp/claw-markdown-preview.pid
open "http://127.0.0.1:$PORT"
```

**说明：**
- 第 1 步把服务跑成托管后台任务（常驻、脱离启动命令的进程树），第 2 步再探测端口并打开浏览器。两步拆分是为了让服务不被启动命令的进程树回收而误杀。
- 服务启动后：`curl` 快速探测默认端口 8765 → 被占用时从日志精确提取端口 → 记录 PID → 打开浏览器。
- 首次运行用默认端口 8765，`curl` 直通不进正则分支；仅端口冲突时才走日志提取降级路径。
- 心跳 120 分钟（7200 秒）兜底——页面关闭/后台冻结/睡眠后最多等待 120 分钟才自停；正常预览、切窗口、睡眠都不会触发超时，且选中的预览风格会持久化保留。

> **不要用 `present_files`**，内置浏览器窗口太挤，用系统命令 `open` 打开外部浏览器。

## 可选参数

| 参数 | 说明 |
|------|------|
| `--file <路径>` | 预览指定 markdown 文件 |
| `--port <端口>` | 指定端口，默认 `8765` |
| `--stdin` | 从标准输入读取 markdown 内容 |
| `--no-open` | 不自动打开系统浏览器（后台/Agent 场景必加） |
| `--verbose` | 输出访问日志，便于调试 |
| `--heartbeat-timeout <秒>` | 心跳超时秒数，页面关闭/冻结/睡眠后超时自动停止服务（默认 `7200`，即 120 分钟；刻意设大以彻底避免后台标签页节流与睡眠导致的误杀） |

如果没有指定 `--file` 或 `--stdin`，服务启动后页面显示空编辑器，用户可自行粘贴 markdown。

## 功能说明

1. **编辑模式**：CodeMirror 编辑器，编辑 Markdown 原文
2. **预览模式**：渲染后的富文本预览，支持主题切换
3. **双栏模式**：编辑器和预览左右并排，支持滚动同步
4. **手机预览**：以手机宽度（500px）居中渲染预览

## 主题

22 种预览主题 + 9 种代码高亮主题，可在页面顶部下拉选择。

## 富文本复制

点击预览区的复制按钮，将当前主题样式内联后的 HTML 写入剪贴板，可直接粘贴到公众号编辑器等平台。复制时会 `fetch` 本地预览服务（仅监听 `127.0.0.1`）的图片并内联为 base64，不访问任何其它外部地址，公众号粘贴后自动识别本地图片。

## 粘贴图片

在编辑模式或双栏模式下，可直接粘贴剪贴板中的图片（Ctrl+V / Cmd+V）。预览页会拦截默认粘贴动作，将图片经由本地预览服务（仅监听 `127.0.0.1`）的 `/api/image` 端点写入本地磁盘、保存到被预览 Markdown 同目录的 `images/` 文件夹，并插入本地引用 `![](images/img-xxx.png)`。整个过程不出本机、不经任何外部服务器。

- 单张图片大小限制 5MB
- 图片以文件形式存储，跟随 md 文件，换浏览器/电脑不丢失

## 注意事项

- 预览服务运行在 `assets/` 子目录上，文件由 `preview_server.py` 自动定位
- 端口默认 8765，被占用时自动递增寻找空闲端口（+20 以内）
- **热更新**：使用 `--file` 模式时，页面每 3 秒轮询文件内容变化，在 Agent 中修改文件后页面自动刷新（弹出"外部内容已更新"提示）
- **常驻 + 心跳兜底**：服务脱离 WorkBuddy 托管常驻（跨平台，python 内部实现脱离，不依赖 shell setsid），不会因对话闲置 / 切窗口 / 睡眠被回收；页面每 5 秒心跳仅作兜底，关闭页面后最多等待 `--heartbeat-timeout` 秒（默认 120 分钟）才自停，刻意设长以避免后台标签页冻结 / 睡眠误杀
- **风格记忆**：顶部选择的预览风格与代码主题会持久化到本机用户目录（`~/.config/claw-markdown-preview/prefs.json`；Windows 为 `%APPDATA%/claw-markdown-preview/prefs.json`，不在技能目录内，重装不丢），刷新页面或下次打开预览自动沿用上次选择，无需重选。
- **⚠️ 编辑即自动保存并覆盖原文件**：在编辑器中修改后停顿约 5 秒，内容会自动经 `/api/save` 写回被预览的 md 文件并覆盖原内容（无备份）；也可点"保存"按钮手动保存。关闭预览页面**不会**自动保存，如有未保存改动会提示确认离开，离开则未保存内容丢弃。
- `--stdin` 模式不支持热更新和粘贴图片（内容固定）
- 服务终止方式：`kill $(cat /tmp/claw-markdown-preview.pid)`

## 后台运行说明

执行入口第 1 步以「托管后台任务」方式常驻服务（脱离启动命令的进程树，命令返回也不会被回收）；第 2 步负责端口探测（curl）/ PID 获取（lsof）/ 残留清理（pkill）。若需手动启动，参考上述命令结构，务必使用 `python3`（与 frontmatter `requires: python3` 一致）而非绝对路径；切勿用命令内 `&` 把服务挂到返回命令的进程树下的写法，否则服务会被进程树清理杀掉。
