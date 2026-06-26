# 🎁 ComfyUI 全自动运行 Skill 分享包

> **适用版本**：ComfyUI-aki-v3 / ComfyUI-aki-v1.4 + OpenClaw agent + Edge 浏览器  
> **更新日期**：2026-04-05

---

## 📦 分享文件清单

```
comfyui-running/
├── SKILL.md                      ✅ AI Agent 主文档
├── SHARING_PACKAGE.md            ✅ 分享说明（本文件）
├── comfyui_browser.py             ✅ 浏览器 CDP 自动化脚本
├── lib/
│   ├── __init__.py               ✅ 包初始化
│   ├── comfyui_config.py         ✅ 配置读取器（跨平台自动检测）
│   └── comfyui_automation.py     ✅ REST API 自动化核心
├── scripts/
│   └── comfyui_setup.py          ✅ 自动配置脚本
└── example_workflows/
    ├── default_api_format.json   ✅ 默认文生图工作流（已修复）
    └── 文生图_api_format.json     ✅ 完整文生图工作流（9节点）
```

**❌ 不包含的文件（自动生成/缓存）**：
- `config.json` — 自动检测生成
- `__pycache__/` — Python 缓存（自动生成）
- `memory/` — 记忆目录

---

## 🚀 快速安装

### 方式一：复制文件夹（推荐）

将整个 `comfyui-running/` 文件夹复制到 OpenClaw 的 `skills/` 目录下：

```
OpenClaw安装目录/
└── skills/
    └── comfyui-running/    ← 复制到这里
```

### 方式二：手动指定路径

对 AI 说：
```
帮我启动ComfyUI并生成一张猫咪图片
```

AI 会自动：
1. 从 config.json 读取配置（如无，自动检测）
2. 启动 ComfyUI（如未运行）
3. 加载工作流 → 执行 → 下载图片

---

## ⚙️ 自动检测路径

Skill 会在以下路径自动搜索 ComfyUI：

| 平台 | 搜索路径 |
|------|---------|
| Windows | `C:/D:/E:/F:/G:/H:/I:/J:/K:/` + `ComfyUI-aki-v3/ComfyUI`, `ComfyUI-aki-v1.4/...`, `ComfyUI/ComfyUI` 等 |
| Linux/WSL | `/mnt/h/g/f/e/d/c/...` + 同上，以及 `/opt/ComfyUI/ComfyUI` |

---

## 📁 工作流说明

| 文件 | 节点数 | 说明 |
|------|--------|------|
| `default_api_format.json` | 7 | 简洁文生图，含 CLIPTextEncode（正/负向） |
| `文生图_api_format.json` | 9 | 完整版，同 `文生图`（KSampler + CheckpointLoader + VAEDecode + SaveImage）|

两个工作流均已验证可在 ComfyUI 0.15 下正常运行。

---

## 🔧 依赖

Skill 会自动安装以下依赖（如未安装）：
- `requests` — HTTP 请求
- `websockets` — WebSocket（CDP 模式用）

---

## ⚠️ 已知问题

### 1. 语法警告（Python 3.12+）
`comfyui_config.py` 的 docstring 中包含 `\D` 等路径写法，会产生 SyntaxWarning，不影响运行。

### 2. UI 格式工作流
原有的 `default.json`（UI 格式）因 ComfyUI 版本差异不再包含完整参数，已移除。仅保留 API 格式工作流（`.json` 直接可用）。

---

*文档版本：v3.0 | 更新日期：2026-04-05*
