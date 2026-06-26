# 国内化安装指引

> 内容工坊是独立 Skill，**不需要安装上游**。
> 所需工具已内置或通过 pip/npm 安装，无需额外注册 MCP。

## 0. 环境要求

```bash
python3 --version   # 需要 3.9+
node --version      # 需要 18+（场景5 PPT 生成需要）
git --version       # 任意
```

## 1. 安装 Skill 文件

Skill 由 AI 自动安装到 `~/.workbuddy/skills/ContentForge/`，
通常通过 Skill Hub 一键装或 git clone：

```bash
mkdir -p ~/.workbuddy/skills/
cd ~/.workbuddy/skills/
git clone https://github.com/SirKayZh/ContentForge
cd ContentForge
```

## 2. 安装核心依赖

```bash
# Python 依赖（httpx / playwright 等）
pip3 install -r requirements.txt 2>/dev/null || true

# yt-dlp（B站/YouTube 视频下载，场景5 需要）
pip3 install yt-dlp

# ffmpeg（音轨提取，macOS 用 brew install ffmpeg）
# Linux: sudo apt install ffmpeg

# Node.js 依赖（场景5 html2pptx 需要）
npm install  # 如有 package.json
```

## 3. 安装 NotebookLM CLI（如需路径 A）

```bash
pip install notebooklm-cli
# 或
npm install -g @notebooklm/cli
```

然后登录（需要海外代理）：

```bash
notebooklm login
# 触发浏览器授权，完成后验证：
notebooklm status
```

> 国内网络配置见 `references/china-network.md`。

## 4.（可选）安装协同 Skill

如果需要输出到飞书或 IMA，另装这两个 Skill：

```bash
# 飞书文档
# → 安装 lark-master Skill（见 lark-master/SKILL.md）

# IMA 笔记 / 知识库
# → 安装 ima-skill（见 ima-skill/SKILL.md）
```

## 5. 环境检查

```bash
cd ~/.workbuddy/skills/ContentForge
bash scripts/check-prereq.sh
```

13 项检查全绿代表就绪。然后在 WorkBuddy 对话里试跑：

```
把这篇公众号文章深度分析并写入 IMA：
https://mp.weixin.qq.com/s/Hu3LHuxqD4xaKEjox4lXyg
```

## 6.（可选）配置播客转写 API

仅「小宇宙播客」「视频号」场景需要。注册 Get笔记（getnote.ai）拿 API Key：

```bash
# 加到 ~/.zshrc
export GETNOTE_API_KEY="your_api_key"
export GETNOTE_CLIENT_ID="your_client_id"

source ~/.zshrc
```

## 卸载

```bash
rm -rf ~/.workbuddy/skills/ContentForge
# 协同 Skill 如不再需要，另删 lark-master / ima-skill
```