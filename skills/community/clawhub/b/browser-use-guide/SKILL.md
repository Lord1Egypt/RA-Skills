---
name: browser-use
description: 让AI代理控制浏览器自动化网页操作。支持 Claude/GPT/Gemini/Ollama，可执行填表、购物、搜索等任务。
---

# browser-use

> 🌐 Make websites accessible for AI agents  
> GitHub: [browser-use/browser-use](https://github.com/browser-use/browser-use) (90k+ ⭐)  
> License: MIT | Language: Python 3.11+ | 安装方式: uv

---

## 一、核心定位

browser-use 让 AI 代理能够控制浏览器完成网页自动化任务，核心理念：

> **Tell your computer what to do, and it gets it done.**

---

## 二、核心能力

| 能力 | 说明 |
|------|------|
| **填表** | 自动填写表单、求职申请 |
| **购物** | 读取购物列表，自动在 Instacart 下单 |
| **搜索比价** | 帮用户找 PC 配件、比较价格 |
| **网页操作** | 点击、输入、截图、导航 |
| **多平台集成** | Gmail、Slack、Notion 等 1000+ 集成 |

---

## 三、安装方式

### 3.1 快速安装（uv）

```bash
# 1. 创建环境并安装
uv init && uv add browser-use && uv sync

# 2. 安装 Chromium（若无浏览器）
uvx browser-use install

# 3. 运行第一个代理
uvx browser-use init --template default
```

### 3.2 OpenClaw 集成安装

```bash
# 克隆到 skills 目录
cd /root/.openclaw/workspace/skills
git clone https://github.com/browser-use/browser-use.git browser-use

# 或直接安装
npx clawhub@latest install browser-use
```

---

## 四、配置 API Key

### 4.1 环境变量配置

```bash
# 创建 .env 文件
cat > .env << EOF
# Browser Use 云端 API（推荐，支持 Stealth + Proxy）
BROWSER_USE_API_KEY=your-key

# 或使用其他 LLM
GOOGLE_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
OPENAI_API_KEY=your-key
EOF
```

### 4.2 API Key 获取

| 服务 | 地址 | 费用 |
|------|------|------|
| **Browser Use Cloud** | cloud.browser-use.com | 免费额度 + 按量付费 |
| **Google AI** | aistudio.google.com | 免费额度 |
| **Anthropic** | console.anthropic.com | 按量付费 |
| **OpenAI** | platform.openai.com | 按量付费 |
| **Ollama（本地）** | ollama.com | 免费（自托管）|

---

## 五、快速开始

### 5.1 基础代理代码

```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def main():
    browser = Browser()  # 本地浏览器
    # browser = Browser(use_cloud=True)  # 云端 Stealth 浏览器

    agent = Agent(
        task="Find the number of stars of the browser-use repo",
        llm=ChatBrowserUse(),  # 或 ChatAnthropic(model='claude-sonnet-4-6')
        browser=browser,
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### 5.2 指定 LLM 提供商

```python
# Google Gemini
from browser_use import ChatGoogle
agent = Agent(task="...", llm=ChatGoogle(model='gemini-3-flash-preview'), browser=browser)

# Anthropic Claude
from browser_use import ChatAnthropic
agent = Agent(task="...", llm=ChatAnthropic(model='claude-sonnet-4-6'), browser=browser)

# 本地 Ollama
from browser_use import ChatOllama
agent = Agent(task="...", llm=ChatOllama(model='llama3'), browser=browser)
```

---

## 六、CLI 工具

### 6.1 常用命令

```bash
# 打开网页
browser-use open https://example.com

# 查看可点击元素
browser-use state

# 点击元素（按索引）
browser-use click 5

# 输入文本
browser-use type "Hello World"

# 截图
browser-use screenshot page.png

# 关闭浏览器
browser-use close
```

### 6.2 模板生成

```bash
# 生成默认模板
uvx browser-use init --template default

# 生成高级配置模板
uvx browser-use init --template advanced

# 生成自定义工具示例
uvx browser-use init --template tools
```

---

## 七、自定义工具

```python
from browser_use import Agent, Browser, Tools

# 定义自定义工具
tools = Tools()

@tools.action(description='获取指定 GitHub 仓库的星数')
def get_github_stars(repo: str) -> str:
    """查询 GitHub 仓库的星数"""
    import requests
    r = requests.get(f"https://api.github.com/repos/{repo}")
    return r.json().get("stargazers_count", "Unknown")

# 创建代理
agent = Agent(
    task="查询 browser-use 仓库的星数",
    llm=ChatBrowserUse(),
    browser=Browser(),
    tools=tools,
)
await agent.run()
```

---

## 八、认证与持久化

### 8.1 复用 Chrome 配置

```python
from browser_use import Agent, Browser

browser = Browser(
    chrome_instance_path="/path/to/chrome",  # 复用本地 Chrome
)

agent = Agent(
    task="登录我的 Gmail 并发送邮件",
    llm=ChatBrowserUse(),
    browser=browser,
)
```

### 8.2 同步云端配置

```bash
# 同步认证信息到云端
curl -fsSL https://browser-use.com/profile.sh | \
  BROWSER_USE_API_KEY=XXXX sh
```

---

## 九、云端 vs 开源

| 特性 | 开源版 | 云端版（推荐）|
|------|--------|-------------|
| **费用** | 免费（需自备 LLM API）| 免费额度 + 按量 |
| **Stealth** | ❌ 需自配 | ✅ Proxy 轮换 + CAPTCHA 解决 |
| **维护** | 需自己运维 | ✅ 全托管 |
| **自定义工具** | ✅ 深度集成 | ✅ 支持 |
| **并发规模** | 受限于本地资源 | ✅ 可水平扩展 |

---

## 十、应用场景示例

### 10.1 求职申请

```python
agent = Agent(
    task="Fill in this job application with my resume and information.",
    llm=ChatBrowserUse(),
    browser=Browser(),
)
await agent.run()
```

### 10.2 购物

```python
agent = Agent(
    task="Put this list of items into my instacart: milk, eggs, bread.",
    llm=ChatBrowserUse(),
    browser=Browser(),
)
await agent.run()
```

### 10.3 比价搜索

```python
agent = Agent(
    task="Help me find parts for a custom PC within budget $1500.",
    llm=ChatBrowserUse(),
    browser=Browser(),
)
await agent.run()
```

---

## 十一、故障排除

| 问题 | 解决方案 |
|------|---------|
| **Chromium 未安装** | `uvx browser-use install` |
| **API Key 报错** | 检查 .env 文件配置 |
| **浏览器无法启动** | `chrome --version` 确认已安装 Chrome |
| **被网站检测** | 使用云端版 `Browser(use_cloud=True)` |
| **任务失败** | 增加 `max_steps` 参数 |

---

## 十二、OpenClaw 集成

### 12.1 MCP 服务方式（推荐）

```bash
# 安装 MCP
cd /root/.openclaw/workspace
npx clawhub@latest install browser-use-mcp

# 添加到 mcporter 配置
openclaw mcp add browser-use --command "python -m browser_use.mcp"
```

### 12.2 Claude Code Skill

```bash
mkdir -p ~/.claude/skills/browser-use
curl -o ~/.claude/skills/browser-use/SKILL.md \
  https://raw.githubusercontent.com/browser-use/browser-use/main/skills/browser-use/SKILL.md
```

---

## 十三、费用参考

### ChatBrowserUse 模型定价（推荐）

| 类型 | 价格（每 1M tokens）|
|------|---------------------|
| **输入** | $0.20 |
| **缓存输入** | $0.02 |
| **输出** | $2.00 |

### 其他模型对比

| 模型 | 特点 |
|------|------|
| **bu-30b-a3b-preview** | Browser Use 专用优化模型 |
| **claude-sonnet-4-6** | Anthropic 最新旗舰 |
| **gemini-3-flash-preview** | Google 高效模型 |
| **llama3（Ollama）** | 免费本地运行 |

---

## 十四、使用方式

### 触发场景

```
用户说「帮我自动填表」→ browser-use 填表示例
用户说「自动帮我购物」→ browser-use 购物示例
用户说「AI 控制浏览器」→ 展示 browser-use 能力
用户说「安装 browser-use」→ 执行安装步骤
用户说「配置 API key」→ 执行配置流程
```

### 组合使用

```
用户：「帮我自动化完成这个求职申请流程」
→ 分析表单字段
→ 调用 browser-use Agent
→ 配置 ChatBrowserUse() LLM
→ 自动执行填表 + 上传简历
```

---

## 十五、关联技能

| 关联技能 | 关系 |
|---------|------|
| `chrome-devtools-mcp` | 浏览器自动化底层工具 |
| `browser-automation-stealth` | 隐身浏览器技术 |
| `cognee-memory` | 记忆管理（跨会话持久化）|
| `ai-research-tools` | 科研数据自动采集 |

---

## 十六、注意事项

```
⚠️ 注意事项：
- Python >= 3.11 required
- 建议使用 uv 管理依赖
- 云端版有免费额度
- 部分网站有反爬机制，建议使用云端 stealth 浏览器
- 遵守网站使用条款，勿用于非法爬虫
```

---

*本技能整合 browser-use 完整安装配置与应用指南*
