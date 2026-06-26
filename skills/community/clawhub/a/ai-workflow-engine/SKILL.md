# AI Workflow Skill
## 智能工作流自动化引擎

> 让AI工作流变得像说话一样简单

---

## 核心功能

### 1. 工作流编排
- ✅ 线性执行 - 按顺序执行任务
- ✅ 条件分支 - 根据条件选择路径
- ✅ 并行执行 - 多任务同时运行
- ✅ 循环执行 - 失败自动重试
- ✅ 事件驱动 - 定时/文件/触发器

### 2. Agent智能体
- ✅ 角色定义 - 设定Agent能力和边界
- ✅ 多Agent协作 - 任务分配与结果汇总
- ✅ 记忆系统 - 短期/长期记忆
- ✅ 工具调用 - 执行代码/查询等

### 3. RAG知识库
- ✅ 文档向量化 - 多种格式支持
- ✅ 智能检索 - 语义搜索
- ✅ 生成答案 - 结合上下文回答
- ✅ 多轮对话 - 记住对话历史

### 4. 数据处理
- ✅ ETL自动化 - 抽取/转换/加载
- ✅ AI清洗 - 自动修复异常数据
- ✅ 质量监控 - 实时数据质量

### 5. 代码生成 (核心!)
根据你的简单描述,自动生成完整工作流!

---

## 快速开始

### 方式一: 描述需求,自动生成

```python
from ai_workflow import WorkflowGenerator

gen = WorkflowGenerator()

# 描述你的需求
workflow = gen.generate("""
    1. 爬取某网站数据
    2. 清洗数据
    3. 存入数据库
    4. 生成分析报告
    5. 发送到我的邮箱
""")

# 执行工作流
workflow.run()
```

### 方式二: 手动构建

```python
from ai_workflow import Workflow, Step, Parallel

# 构建工作流
wf = Workflow([
    Step("爬取", fetch_data),
    Step("清洗", clean_data),
    Step("分析", analyze),
    Step("报告", generate_report)
])

wf.run()
```

### 方式三: Agent编排

```python
from ai_workflow import Agent, orchestrate

agents = [
    Agent("研究员", search_and_analyze),
    Agent("分析师", deep_analyze),
    Agent("写手", write_report)
]

result = orchestrate(agents, task="分析BTC价格趋势")
```

---

## 工作流模式

### 1. 线性执行
```python
wf = Workflow([
    Step("第一步", do_something),
    Step("第二步", do_next),
    Step("第三步", final_step)
])
```

### 2. 条件分支
```python
from ai_workflow import Condition

wf = Workflow([
    Step("检查", check_status),
    Condition(
        if_true=Step("成功", handle_success),
        if_false=Step("失败", handle_failure)
    )
])
```

### 3. 并行执行
```python
from ai_workflow import ParallelStep

wf = Workflow([
    ParallelStep([
        Step("任务A", task_a),
        Step("任务B", task_b),
        Step("任务C", task_c)
    ]),
    Step("汇总", aggregate_results)
])
```

### 4. 循环重试
```python
from ai_workflow import Retry, Loop

# 失败重试3次
wf = Workflow([
    Retry(max_attempts=3)(
        Step("可能失败", risky_task)
    )
])

# 循环直到成功
wf = Workflow([
    Loop(until="success")(
        Step("尝试", try_task)
    )
])
```

---

## Agent系统

### 创建Agent

```python
from ai_workflow import Agent

# 创建研究员Agent
researcher = Agent(
    name="研究员",
    role="负责信息搜集和分析",
    tools=[search_web, read_file],
    knowledge="专业领域知识库"
)

# 创建写手Agent
writer = Agent(
    name="写手",
    role="负责内容创作",
    tools=[write_file, send_email]
)
```

### Agent协作

```python
from ai_workflow import orchestrate

result = orchestrate(
    agents=[researcher, analyst, writer],
    task="写一篇关于AI的工作报告",
    mode="sequential"  # 或 parallel
)
```

---

## RAG知识库

### 构建知识库

```python
from ai_workflow import KnowledgeBase

kb = KnowledgeBase("公司知识库")

# 添加文档
kb.add_document("产品介绍.pdf")
kb.add_document("技术文档.docx")
kb.add_document("常见问题.md")

# 问答
answer = kb.query("公司的使命是什么?")
print(answer.text)
print(answer.sources)  # 引用来源
```

### 带工具的RAG

```python
# 当RAG无法回答时,自动调用工具
kb = KnowledgeBase("助手", tools=[search_web, calculator])

answer = kb.query("昨天BTC价格是多少?")
# 如果知识库没有,自动搜索网络
```

---

## 代码生成示例

### 输入简单的描述

```
帮我写一个爬虫工作流:
1. 爬取某网站的产品数据
2. 清洗数据(去重、填充缺失)
3. 存入MySQL数据库
4. 生成Excel报表
5. 发送到邮箱
```

### 自动生成完整代码

```python
# 生成的代码会自动包含:
# 1. 爬虫实现
# 2. 数据清洗
# 3. 数据库操作
# 4. Excel导出
# 5. 邮件发送
# 6. 错误处理
# 7. 日志记录
# 8. 配置文件

# 执行
workflow.run()
```

---

## 配置

```python
from ai_workflow import Config

# 配置AI模型
Config.set("openai_key", "sk-xxx")
Config.set("model", "gpt-4")

# 配置数据库
Config.set("db_url", "mysql://user:pass@localhost/db")

# 配置邮件
Config.set("smtp", {"host": "smtp.gmail.com", "port": 587})
```

---

## 依赖

```bash
pip install pandas openpyxl requests beautifulsoup4
pip install chromadb pypdf  # RAG
pip install openai anthropic  # AI模型
```

---

## 示例工作流

### 1. 内容创作工作流
```python
workflow = generate_workflow("""
    1. 搜索AI最新新闻
    2. 分析热点话题
    3. 撰写文章
    4. 生成配图
    5. 发布到博客
""")
```

### 2. 数据分析工作流
```python
workflow = generate_workflow("""
    1. 从数据库读取销售数据
    2. 分析销售趋势
    3. 生成可视化图表
    4. 输出分析报告
""")
```

### 3. 客服工作流
```python
workflow = generate_workflow("""
    1. 接收用户问题
    2. 查询FAQ知识库
    3. 如无法回答,搜索文档
    4. 生成回复
    5. 记录对话
""")
```

---

## 许可证

MIT License