---
name: claw-windows-automator
description: |
  当用户想要**Windows自动化**、**自动打开CMD**、**在指定目录执行命令**、**运行bat脚本**、**GitHub自动下载最新版**、**一键下载仓库源码**、**桌面GUI自动化**、**pyautogui任务**、**全屏可视化提示**、**鼠标单击强制停止**、**输入法自动切换**、**项目初始化**、**批量部署**、**安全可靠的Windows Agent** 等需求时自动触发。

  这是一个完整的高容错 Windows 桌面自动化技能，集成全屏半透明 Overlay 实时提示、鼠标左键一键强制终止、Windows API 智能英文输入法切换、CMD 自动打开与执行、GitHub 最新发布包智能下载等核心能力。
  支持通过 CLI 统一入口调用 `cmd_task`（目录下自动打开 CMD 并执行命令）和 `github_download`（自动解析并下载 GitHub 最新源码 ZIP），所有操作均带详细日志、可视化进度和紧急停止机制，完全本地运行，无需额外配置。

  【重要约束】仅处理 Windows 桌面自动化相关需求（CMD 执行、GitHub 下载、可视化提示等），其他类型任务（如音频处理、图片生成、网页爬取等）一律不触发此技能。

  常见触发口语（越多越好）：
  - “帮我自动打开CMD执行命令”
  - “在 D:\project 目录下运行 pip install”
  - “下载 GitHub 这个仓库的最新版”
  - “Windows自动化 执行这个脚本”
  - “一键下载 GitHub 源码包”
  - “启动自动化任务并显示进度”
  - “鼠标点击就能停止的自动化”
  - “自动切换英文输入法跑命令”
  - “批量初始化项目文件夹”
  - “GitHub 下载最新发布包”
  - “打开命令提示符执行 bat”
  - “可视化 Windows 自动化”
  - “安全可靠的桌面自动化”
metadata:
  openclaw:
    requires:
      bins:
        - python
    user-invocable: true
---

# OpenClaw Windows Automation Skill

**功能**：高稳定、可视化、安全可中断的 Windows 桌面自动化引擎。集成全屏 Overlay 实时进度提示、鼠标左键一键强制终止、输入法自动切换、CMD 自动打开执行命令、GitHub 最新源码一键下载等能力。通过统一 CLI 入口，让 LLM 大模型能够可靠地驱动 Windows 完成复杂自动化任务。

### 触发时机（Triggers）
- 用户明确提到 Windows 自动化、CMD 命令执行、GitHub 下载、项目初始化、批量部署等需求。
- 用户提供文件夹路径并要求“在该目录下执行命令/脚本”。
- 用户提供 GitHub 仓库地址并要求“下载最新版”或“下载源码包”。
- 用户希望看到实时进度提示或需要“鼠标一点就能停止”的安全自动化。
- 用户提到“自动打开命令提示符”“输入法干扰”“pyautogui”“桌面自动化”等关键词。

### 支持的任务（Tasks）
1. **`cmd_task`**（默认推荐）
   - 在指定目录自动打开 CMD 并执行任意命令或 bat 脚本
   - 支持失败重试 + 容错继续模式

2. **`github_download`**
   - 自动打开浏览器，智能解析 GitHub `/releases/latest`，一键下载最新源码 ZIP 包

（后续可无限扩展新任务，只需注册到 OPERATIONS 字典即可被 LLM 调用）

## 参数提取指南
当决定调用此技能时，请从用户消息中准确提取以下参数：

1. **`<任务名称>`** (必填): 必须是 `cmd_task` 或 `github_download` 中的一个。
2. **`<路径>`** (cmd_task 必填): 要打开 CMD 的文件夹路径（支持相对/绝对路径）。
3. **`<脚本/命令>`** (cmd_task 必填): 需要在 CMD 中执行的具体命令或脚本内容。
4. **`<GitHub地址>`** (github_download 必填): GitHub 仓库完整地址（如 `https://github.com/user/repo`）。
5. **`<容错模式>`** (cmd_task 选填): 默认开启（`continue_on_error=true`），出错后继续执行后续步骤。

### 执行步骤
1. **解析意图**：识别用户想要执行的任务类型（cmd_task 或 github_download）以及对应参数。
2. **路径/地址提取**：从用户消息中提取文件夹路径或 GitHub URL。
3. **任务选择**：根据用户关键词自动匹配对应 task。
4. **调用命令**：使用以下兼容性命令启动脚本（优先 `python3`，失败则 `python`）。脚本会自动启动 Overlay 提示、执行任务，并在结束或用户点击鼠标时安全退出。

   ```bash
   (python3 scripts/operations.py run --task "<任务名>" [--path "<路径>"] [--script "<脚本>"] [--url "<地址>"]) || (python scripts/operations.py run --task "<任务名>" [--path "<目录路径>"] [--script "<执行脚本>"] [--url "<连接地址>"])