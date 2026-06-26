### 🦾 OpenClaw - Windows 自动化技能包

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows_10/11-blue.svg)]()
[![Last Update](https://img.shields.io/badge/更新-2026.04-orange.svg)]()

**claw-windows-automator**（又名 **Claw Windows Automator**）是一个**高稳定、可视化、安全可中断**的 Windows 桌面自动化引擎，专为 LLM 大模型（如 Claude、GPT、Grok、DeepSeek 等）设计。

它彻底解决了传统 `pyautogui` 脚本的三大痛点：
- 中文输入法导致命令乱码
- 用户不知道脚本在干什么
- 脚本卡死后无法安全停止

通过**全屏半透明 Overlay 实时提示 + 鼠标左键一键强制终止**，让自动化过程既专业又安全。

---

## ✨ 核心特性

- **全屏可视化 Overlay**  
  半透明黑色遮罩 + 超大醒目标题 + 实时动态更新任务状态，支持五种位置切换和字体大小调节

- **鼠标左键一键强制终止**  
  任意时刻点击鼠标左键即可立即停止所有任务，并触发清理回调

- **智能英文输入法切换**  
  Windows API + `Win+Space` 热键双保险，彻底杜绝输入法干扰

- **CMD 自动打开与高容错执行**  
  指定目录自动打开 CMD，支持重试、容错继续模式

- **GitHub 最新发布包一键下载**  
  自动解析 `/releases/latest`，智能获取最新 tag 并下载源码 ZIP

- **统一 CLI 入口**  
  `list` 查看所有任务、`run --task xxx` 执行任务

- **模块化设计**  
  易于扩展，新增任务只需注册到 `OPERATIONS` 字典即可被 LLM 调用

- **安全睡眠与界面刷新**  
  `safe_sleep` 保证长时间运行时 Overlay 不卡死

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/wangminrui2022/claw-windows-automator.git
cd openclaw
```

### 2. 查看所有可用任务
```bash
python scripts/operations.py list
```

### 3. 执行任务示例

**示例1：指定目录下自动打开 CMD 并执行命令**
```bash
python scripts/operations.py run --task "cmd_task" --path "D:\openclaw-2026.4.2-test" --script "node openclaw.mjs dashboard"
```

**示例2：一键下载 GitHub 仓库最新源码**
```bash
python scripts/operations.py run --task "github_download"  --url "https://github.com/openclaw/openclaw"
```

---

## 📋 支持的任务

| 任务名称           | 描述                                      | 必填参数                  | 推荐场景                  |
|--------------------|-------------------------------------------|---------------------------|---------------------------|
| `cmd_task`         | 指定目录打开 CMD 并执行命令/脚本          | `--path`, `--script`      | 项目初始化、批量部署、运行 bat |
| `github_download`  | 自动下载 GitHub 仓库最新源码 ZIP         | `--url`                   | 快速拉取开源项目最新版    |

---

## 📁 项目结构

```
openclaw/
├── operations.py              # CLI 入口 + 任务调度核心
├── base_automator.py          # 基础类（输入法切换、日志）
├── cmd_automator.py           # CMD 自动打开模块
├── gradient_overlay.py        # 全屏可视化 Overlay（核心）
└── ......
```

---

## 🛠️ 工作原理（简要）

1. **启动 Overlay** → 全屏半透明提示，用户可实时看到当前任务
2. **智能切换英文输入法** → 避免中文输入法干扰
3. **执行任务** → `cmd_task` 或 `github_download`
4. **用户可随时干预** → 鼠标左键点击 → 触发终止回调 → 安全退出
5. **任务结束** → 自动关闭 Overlay 并清理资源

---

## 📸 界面预览

（实际运行时效果）

- 全屏半透明黑色遮罩 + 绿色大标题
- 右下角显示“正在自动化操作，请勿移动鼠标/键盘...”
- 鼠标左键点击任意位置即可强制停止
- 支持实时更新标题（如“正在执行 pip install...”）

---

## ⚙️ 高级用法

### 自定义任务
在 `operations.py` 的 `OPERATIONS` 字典中添加新任务即可：

```python
OPERATIONS = {
    "cmd_task": {"func": cmd_task.execute, "desc": "打开CMD执行命令"},
    "github_download": {"func": github_download.execute, "desc": "下载GitHub最新版"},
    # 新增你的任务...
}
```

### 容错模式
`cmd_task` 默认开启 `continue_on_error=True`，即使某条命令失败也会继续执行后续步骤。

---

## 🧪 环境要求

- **操作系统**：Windows 10 / 11（已做 DPI 适配）
- **Python**：3.8 及以上
- **权限**：普通用户权限即可（无需管理员）

---

## 📜 License

本项目采用 **Apache License** 开源。

---

**Star 支持一下吧！** ⭐  
你的每一个 Star 都是对 OpenClaw 持续维护的最大鼓励！

---