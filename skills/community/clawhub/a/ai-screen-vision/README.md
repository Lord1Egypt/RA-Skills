# 🖥️ Screen Vision

**AI Screen Vision & Desktop Control Skill for OpenClaw**

让 AI 看到屏幕、理解界面、操控电脑——像人一样使用桌面。

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai/guitu917/ai-screen-vision)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-green)]()
[![Version](https://img.shields.io/badge/Version-1.1.0-orange)]()

---

## ✨ 功能特性

- 🖱️ **鼠标操控** — 点击、双击、右键、拖拽
- ⌨️ **键盘输入** — 打字、快捷键、功能键
- 📸 **屏幕理解** — AI 视觉分析屏幕内容
- 🔄 **自主循环** — 截图→分析→操作→循环直到完成
- 💡 **智能省 Token** — diff 检测，画面没变化不重复分析
- 🔒 **安全机制** — 拦截危险操作，敏感操作需确认
- 🖥️ **跨平台** — Linux / macOS / Windows 全支持
- 📱 **远程观看** — 无桌面服务器可用 noVNC 网页实时观看

## 🎬 工作原理

```
用户说 "帮我打开浏览器搜索天气"
           │
           ▼
    ┌─ 截屏（scrot/screencapture/pyautogui）
    ├─ AI 视觉分析（用户自选模型）
    │   ├─ 看到什么？
    │   ├─ 下一步做什么？
    │   └─ 操作坐标是什么？
    ├─ 执行操作（xdotool/cliclick/pyautogui）
    ├─ 等待 1 秒
    └─ 再次截屏 → 循环
        │
        ▼
    任务完成 → 截图汇报结果
```

## 📦 安装

### 方式一：ClawHub 一键安装（推荐）

```bash
clawhub install ai-screen-vision
```

### 方式二：手动安装

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/guitu917/screen-vision.git ~/.openclaw/workspace/skills/screen-vision

# 进入目录运行安装脚本
cd ~/.openclaw/workspace/skills/screen-vision
bash install.sh
```

### 方式三：发送给 OpenClaw

直接把压缩包发给 OpenClaw，AI 会自动解压安装！

### 一键安装脚本参数

```bash
bash install.sh                              # 自动检测平台
bash install.sh --api-key YOUR_API_KEY       # 带 API Key 安装
bash install.sh --headless                   # Linux 无桌面服务器模式
bash install.sh --desktop                    # Linux 有桌面环境
```

## ⚙️ 配置

### API Key（必须）

复制配置模板并填入你的视觉 API Key：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "vision": {
    "baseUrl": "https://api.siliconflow.cn/v1",
    "apiKey": "YOUR_API_KEY",
    "model": "Qwen/Qwen3-VL-32B"
  }
}
```

或使用环境变量：

```bash
export SV_VISION_API_KEY=your_api_key
export SV_VISION_BASE_URL=https://api.siliconflow.cn/v1
export SV_VISION_MODEL=Qwen/Qwen3-VL-32B
```

### 支持的视觉模型

本技能支持**所有 OpenAI 兼容的视觉 API**，不限厂商，用户自由选择。

| 模型 | 平台 | 费用/任务 | 准确度 |
|------|------|----------|--------|
| Qwen3-VL-32B | 硅基流动 | 低 | ⭐⭐⭐⭐ |
| GLM-4V-Plus | 智谱 BigModel | 低 | ⭐⭐⭐⭐ |
| GPT-5.4-Mini | OpenAI / 中转站 | 中 | ⭐⭐⭐⭐⭐ |
| GPT-5.4 CUA | OpenAI | 高 | ⭐⭐⭐⭐⭐ |
| Llama 3.2 Vision | Ollama 本地 | 免费 | ⭐⭐ |

详细配置见 [references/API_CONFIG.md](references/API_CONFIG.md)，包含各平台注册地址和配置示例。

## 🖥️ 平台支持

### Linux

**有桌面环境（Ubuntu Desktop 等）：**
```bash
bash scripts/setup/setup-linux.sh --desktop
```
工具：`scrot` + `xdotool`，直接操控现有桌面

**无桌面服务器（Headless）：**
```bash
bash scripts/setup/setup-linux.sh --headless
```
自动安装：XFCE4 桌面 + VNC 服务器 + noVNC 网页端
- 启动：`sv-start`
- 停止：`sv-stop`
- 浏览器访问：`http://<IP>:6080/vnc.html`

### macOS

```bash
bash scripts/setup/setup-mac.sh
```
工具：`screencapture` + `cliclick`

⚠️ 需要授权：系统设置 → 隐私与安全 → 辅助功能 → 添加终端/OpenClaw

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup/setup-win.ps1
```
工具：`pyautogui`（Python），无需额外配置

## 🎯 使用方式

在 OpenClaw 中直接用自然语言：

```
"帮我打开Chrome搜索北京天气"
"看看屏幕上有什么"
"帮我打开终端执行 ls -la"
"截个屏给我看看"
"帮我把这个文件拖到回收站"
"打开微信发消息给张三"
```

## 📁 项目结构

```
screen-vision/
├── SKILL.md                    # Skill 入口说明（AI 读取）
├── config.example.json         # 配置模板
├── install.sh                  # 一键安装脚本
│
├── scripts/
│   ├── setup/                  # 各平台安装脚本
│   │   ├── setup-linux.sh
│   │   ├── setup-mac.sh
│   │   └── setup-win.ps1
│   │
│   ├── platform/               # 平台适配层
│   │   ├── detect_os.sh        # 平台检测
│   │   ├── screenshot.sh       # 跨平台截屏
│   │   └── execute.py          # 统一操作执行器
│   │
│   ├── vision/                 # 视觉引擎
│   │   ├── analyze.py          # AI 视觉 API 调用
│   │   └── diff_check.py       # 图片变化检测（省 Token）
│   │
│   └── core/                   # 核心引擎
│       ├── run_task.py         # 主循环任务执行器
│       ├── safety_check.py     # 安全检查
│       └── config.py           # 配置管理
│
└── references/                 # 参考文档
    ├── PLATFORM_GUIDE.md       # 各平台工具详情
    ├── API_CONFIG.md           # API 配置说明
    └── EXAMPLES.md             # 使用示例
```

## 🔒 安全机制

- ❌ **自动拦截**：`rm -rf /`、格式化磁盘、`shutdown`、`drop database` 等
- ⚠️ **需确认**：涉及删除、sudo、支付等敏感操作
- ⏱️ **超时保护**：最长 5 分钟 / 100 步自动停止
- 📸 **操作日志**：所有截图保存到 `/tmp/screen-vision/logs/`
- 🛑 **错误停止**：API 错误自动停止任务

## 📄 License

MIT License

---

**Powered by [OpenClaw](https://openclaw.ai)** | Published on [ClawHub](https://clawhub.ai/guitu917/ai-screen-vision)
