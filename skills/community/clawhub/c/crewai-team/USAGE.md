# CrewAI 产品需求收集团队 - 使用指南

## 📦 安装

### 方式 1：使用 Python 3.10

```bash
cd ~/.openclaw/workspace/crewai_team
python3.10 -m pip install -r requirements.txt
```

### 方式 2：使用 uv（推荐，更快）

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
cd ~/.openclaw/workspace/crewai_team
uv pip install -r requirements.txt
```

---

## 🔑 配置 API Key

```bash
# 复制环境变量配置
cp .env.example .env

# 编辑 .env 文件，填入你的 DashScope API Key
# 从 https://dashscope.console.aliyun.com/ 获取
```

---

## 🚀 快速开始

### 命令行使用

```bash
# 运行团队分析
python3.10 run_team.py "一个 AI 驱动的需求收集机器人"
```

### Python 代码使用

```python
from team_config import create_product_team

# 定义产品创意
product_idea = """
一个 AI 驱动的需求收集机器人，能够：
- 主动引导客户沟通需求
- 按 PRD 框架结构化提问
- 自动输出标准 PRD 文档
"""

# 创建团队
crew = create_product_team(product_idea, verbose=True)

# 执行分析
result = crew.kickoff()
print(result)
```

### OpenClaw 集成使用

在 OpenClaw 中调用：

```python
# 通过 OpenClaw 子代理调用
sessions_spawn(
    task="用 CrewAI 分析产品需求：一个 AI 需求收集机器人",
    runtime="subagent",
    cwd="/Users/dayangyu/.openclaw/workspace/crewai_team"
)
```

---

## 👥 团队成员

| 角色 | 职责 | 输出 |
|------|------|------|
| 📊 市场调研分析师 | 竞品分析、用户研究 | 市场调研报告 |
| 🎨 产品设计专家 | 功能设计、UI 建议 | 产品设计方案 |
| 🏗️ 技术总监 | 架构设计、任务拆分 | 技术方案文档 |
| 💻 全栈技术专家 | 代码实现、示例 | 开发指南 |
| ✅ 质量专家 | 测试计划、验收标准 | 质量保障计划 |

---

## 📋 工作流程

```
需求输入
    ↓
📊 市场调研（用户画像、竞品分析、市场规模）
    ↓
🎨 产品设计（功能列表、用户流程、验收标准）
    ↓
🏗️ 技术架构（技术栈、系统架构、任务拆分）
    ↓
💻 开发实现（代码示例、项目结构）
    ↓
✅ 质量保障（测试用例、验收清单）
    ↓
📄 PRD 汇总（完整文档）
```

---

## ⚙️ 高级配置

### 修改 LLM 模型

编辑 `team_config.py`：

```python
# 使用 Qwen-Max
llm = ChatOpenAI(
    model="qwen3-max-2026-01-23",
    base_url="https://coding.dashscope.aliyuncs.com/v1",
    api_key=os.environ.get("DASHSCOPE_API_KEY")
)

# 或使用 OpenAI GPT-4
llm = ChatOpenAI(
    model="gpt-4-turbo",
    api_key=os.environ.get("OPENAI_API_KEY")
)
```

### 并行执行任务

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.hierarchical  # 或 sequential
)
```

### 添加自定义工具

```python
from crewai_tools import ScrapeWebsiteTool, FileReadTool

# 添加网站抓取工具
scrape_tool = ScrapeWebsiteTool(website_url="https://example.com")

# 添加到 Agent
market_analyst = Agent(
    ...,
    tools=[search_tool, scrape_tool]
)
```

---

## 📁 项目结构

```
crewai_team/
├── README.md              # 团队说明
├── team_config.py         # 团队配置（Agents + Tasks）
├── run_team.py           # 运行脚本
├── requirements.txt       # 依赖列表
├── .env.example          # 环境变量示例
└── USAGE.md              # 使用指南（本文件）
```

---

## ❓ 常见问题

### Q: 安装失败怎么办？
A: 确保使用 Python 3.10+，推荐使用 uv 安装。

### Q: API 调用失败？
A: 检查 `.env` 文件中的 API Key 是否正确，确保有足够余额。

### Q: 输出太长怎么办？
A: 可以设置 `verbose=False` 减少中间输出，或只运行特定任务。

### Q: 如何自定义 Agent？
A: 编辑 `team_config.py` 中的 Agent 定义，修改 role/goal/backstory。

### Q: 如何保存输出结果？
A: 修改 `run_team.py`，将 `result` 写入文件：
```python
with open("prd_output.md", "w") as f:
    f.write(str(result))
```

---

## 🎯 最佳实践

1. **明确产品创意** - 输入越详细，输出越精准
2. **分阶段执行** - 复杂产品可以分多次运行
3. **人工 Review** - AI 输出需要人工审核和补充
4. **迭代优化** - 根据输出质量调整 Agent 配置

---

*先生，有任何问题随时告诉我，我可以帮您调整配置。*
