# 🎯 Career Compass — 职场罗盘

> **by Barry** | 一站式求职辅助 Skill

整合简历解析优化、公司调研（就业向）、同城职位搜索、模拟面试四大模块。

支持更宽松的自然语言触发，不要求用户必须说出精确命令；只要表达与求职、跳槽、公司判断、岗位机会、面试准备、offer 评估等相关意图，即可被激活。
**skill使用大佬的逆向boss，以此获取信息，同时简历也可以同步获取进行分析，但是严格限制对话以及交谈，只用于分析jd和公司。**

**支持平台：** OpenClaw

---

## 功能概览

| 模块 | 依赖 | 说明 |
|------|------|------|
| 📋 **信息收集** | — | 对话引导收集简历/公司/JD |
| 📝 **简历优化** | — | 生成优化方向 + 自检清单 |
| 🏢 **公司调研** | `web_search`/`web_fetch` | 就业视角公司分析 |
| 🔍 **同城职位搜索** | `boss-cli` | BOSS 直聘只读查询 |
| 📄 **PDF 简历解析** | 系统 PDF 工具 | 提取简历文字 |
| 🎤 **模拟面试** | — | 面试练习 + 评分卡 |

---

## 安装方式

### 自动安装（推荐）

下载 `career-compass` 文件夹到 OpenClaw skills 目录后，OpenClaw 会自动执行 `SKILL.md` 中的安装脚本，安装 boss-cli 等所有依赖。

手动触发安装：
```bash
# 在 skill 目录下运行
bash INSTALL.sh   # macOS / Linux
INSTALL.bat       # Windows
```

### boss-cli 手动安装（如自动安装失败）

```bash
# 方式1: uv（推荐）
uv tool install kabi-boss-cli

# 方式2: pipx
pipx install kabi-boss-cli

# 方式3: pip
pip install kabi-boss-cli --user
```

### PDF 工具链（可选，用于解析简历 PDF）

```bash
# macOS
brew install poppler tesseract ghostscript

# Ubuntu/Debian
sudo apt install poppler-utils tesseract-ocr ghostscript

# Windows
# poppler: https://github.com/oschwartz10612/poppler-windows/releases
# tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# ghostscript: https://ghostscript.com/releases/gsdnld.html
```

> 💡 不安装 PDF 工具链也可以使用：直接复制简历内容粘贴给 AI 即可。

---

## BOSS 直聘登录

每个用户需要用自己的 BOSS 账号独立登录一次。

```bash
# 1. 确保浏览器已登录 zhipin.com

# 2. 运行登录
boss login

# 3. 验证
boss status
boss me --json   # 看到名字即成功

# 如自动提取失败
boss login --qrcode
```

Cookie 存在本地（`~/.config/boss-cli/credential.json`），有效期约 7 天。

**本 Skill 仅使用只读查询命令，不涉及投递/打招呼/聊天。**

---

## 快速开始

在 AI 对话中直接说：

```text
帮我全面准备面试
我要去XX公司面试，帮我模拟一下
帮我看看简历有哪些可以优化的地方
分析一下XX公司怎么样
帮我搜索XX城市的XX岗位
```

## 触发方式（增强版）

### 设计原则

- 支持模糊触发，不要求固定格式
- 支持关联触发，只要语义与求职场景相关即可进入对应流程
- 支持情绪化表达、口语化表达、半句式表达
- 当用户信息不足时，优先先触发再追问，而不是因为缺少关键词拒绝进入流程

### 推荐触发语示例

| 场景 | 精确触发 | 模糊/关联触发 |
|------|----------|---------------|
| 全面启动 | 帮我全面准备面试 | 我最近想换工作 / 帮我梳理一下求职方向 |
| 简历优化 | 帮我优化简历 | 我这份简历能打几分 / 你帮我改改简历 / 看看我的经历怎么写 |
| 公司调研 | 帮我调研XX公司 | 这家公司值不值得去 / 这家公司靠谱吗 / 这家公司会不会很卷 |
| 职位搜索 | 帮我搜索XX岗位 | 我现在适合找什么工作 / 看看最近有没有合适机会 |
| 模拟面试 | 帮我模拟面试 | 你来面我 / 帮我压力面一下 / 我明天有面试有点慌 |
| JD分析 | 帮我看看这个JD | 我能不能胜任这个岗位 / 这个岗位适不适合我 |
| Offer评估 | 帮我评估这个Offer | 这个 offer 值不值得接 / 这份工作能不能去 |
| 面试复盘 | 帮我复盘面试 | 我刚面完有点乱 / 帮我总结一下哪里答得不好 |

### 更自然的触发例子

```text
我最近想跳槽，你帮我一起梳理一下
这家公司靠谱不靠谱
我拿到一个 offer，不知道值不值得去
我这个背景现在还能找什么岗位
我明天面试，有点慌，你先拷打我一下
你帮我看看我这段项目经历怎么写更像样
```

---

## 隐私说明

- boss-cli Cookie 存在用户本地，不上传任何服务器
- PDF 处理在本地完成，不上传文件
- 简历信息仅用于当次对话分析
