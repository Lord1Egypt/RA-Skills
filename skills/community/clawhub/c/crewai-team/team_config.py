"""
CrewAI 产品需求收集团队配置
先生，这是您的专属 AI 产品团队
"""

from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
import os

# ==================== 工具配置 ====================

# 搜索工具（使用免费方案）
search_tool = DuckDuckGoSearchRun()

# 如果您有 Tavily API key，可以使用更强大的搜索
# os.environ["TAVILY_API_KEY"] = "your-key"
# search_tool = TavilySearchResults(max_results=5)

# ==================== LLM 配置 ====================

# 使用 OpenAI 兼容接口（可配置为 Qwen/DeepSeek 等）
llm = ChatOpenAI(
    model="qwen3.5-plus",
    base_url="https://coding.dashscope.aliyuncs.com/v1",
    api_key=os.environ.get("DASHSCOPE_API_KEY", "sk-your-key")
)

# ==================== Agent 定义 ====================

# 1. 市场调研分析师
market_analyst = Agent(
    role="市场调研分析师",
    goal="深度研究市场趋势和竞品，提供数据驱动的商业洞察",
    backstory="""你是一位资深市场调研分析师，拥有 10 年科技行业研究经验。
你擅长：
- 竞品功能对比分析
- 目标用户画像研究
- 市场规模和趋势分析
- 竞品定价策略分析

你的分析报告以数据为支撑，洞察深刻，能直接影响产品决策。""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

# 2. 产品设计专家
design_expert = Agent(
    role="产品设计专家",
    goal="设计优秀的用户体验和产品方案，确保产品满足用户需求",
    backstory="""你是一位资深产品设计专家，曾在多家顶级科技公司工作。
你擅长：
- 产品功能设计和信息架构
- UI/UX 设计方案
- 用户流程优化
- 产品验收标准制定

你的设计理念是以用户为中心，平衡商业目标和用户体验。""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 3. 技术总监
tech_director = Agent(
    role="技术总监",
    goal="设计可扩展的技术架构，合理拆分研发任务",
    backstory="""你是一位资深技术总监，有 15 年技术架构和团队管理经验。
你擅长：
- 分布式系统架构设计
- 技术选型和评估
- 研发任务拆分和排期
- 技术风险评估和应对

你的技术方案兼顾短期交付和长期可维护性。""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 4. 全栈技术专家
fullstack_dev = Agent(
    role="全栈技术专家",
    goal="高质量完成代码开发，实现产品功能",
    backstory="""你是一位全栈技术专家，精通前后端开发。
你擅长：
- 前端开发 (React/Vue/HTML/CSS/JS)
- 后端开发 (Node.js/Python/Go)
- 数据库设计 (SQL/NoSQL)
- API 开发和集成

你的代码质量高，注释清晰，遵循最佳实践。""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 5. 质量专家
qa_expert = Agent(
    role="质量专家",
    goal="确保产品质量符合标准，发现并预防潜在问题",
    backstory="""你是一位资深质量保障专家，对细节有严格要求。
你擅长：
- 测试用例设计和执行
- 功能验证和回归测试
- 性能测试和优化
- 验收测试和发布评审

你的测试覆盖全面，能发现别人忽略的问题。""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==================== 任务定义 ====================

def create_market_research_task(product_idea: str) -> Task:
    """市场调研任务"""
    return Task(
        description=f"""
        针对产品创意进行市场调研：
        产品创意：{product_idea}
        
        请完成以下分析：
        1. 目标用户画像（年龄、职业、痛点、使用场景）
        2. 竞品分析（至少 3 个直接竞品，列出功能对比）
        3. 市场规模和趋势（TAM/SAM/SOM）
        4. 竞品定价策略分析
        5. 市场机会点和建议
        
        输出格式：结构化的市场调研报告，包含数据支撑
        """,
        expected_output="一份完整的市场调研报告，包含用户画像、竞品分析、市场规模、定价策略和机会点",
        agent=market_analyst
    )

def create_product_design_task(product_idea: str) -> Task:
    """产品设计任务"""
    return Task(
        description=f"""
        基于市场调研结果，进行产品设计：
        产品创意：{product_idea}
        
        请完成以下设计：
        1. 产品核心功能列表（按优先级排序：P0/P1/P2）
        2. 用户流程图（核心功能的使用流程）
        3. 信息架构设计（功能模块组织）
        4. UI/UX 设计建议（关键页面布局）
        5. 产品验收标准（每个功能的验收条件）
        
        输出格式：结构化的产品设计方案
        """,
        expected_output="一份完整的产品设计方案，包含功能列表、用户流程、信息架构、UI 建议和验收标准",
        agent=design_expert
    )

def create_architecture_task(product_idea: str) -> Task:
    """技术架构任务"""
    return Task(
        description=f"""
        基于产品设计方案，设计技术架构：
        产品创意：{product_idea}
        
        请完成以下设计：
        1. 技术栈选型（前端/后端/数据库/基础设施）
        2. 系统架构图（模块划分和交互）
        3. 数据模型设计（核心数据表和关系）
        4. API 设计（核心接口定义）
        5. 研发任务拆分（按模块和优先级）
        6. 技术风险评估和应对方案
        
        输出格式：结构化的技术方案文档
        """,
        expected_output="一份完整的技术方案文档，包含技术栈、架构图、数据模型、API 设计和任务拆分",
        agent=tech_director
    )

def create_development_task(product_idea: str) -> Task:
    """开发任务"""
    return Task(
        description=f"""
        基于技术方案，提供开发实现建议：
        产品创意：{product_idea}
        
        请完成以下内容：
        1. 项目目录结构建议
        2. 核心模块代码示例（关键功能实现）
        3. 数据库迁移脚本
        4. API 实现示例
        5. 前端组件示例
        
        输出格式：结构化的开发指南，包含代码示例
        """,
        expected_output="一份开发指南，包含项目结构、核心代码示例、数据库脚本和 API 实现",
        agent=fullstack_dev
    )

def create_qa_task(product_idea: str) -> Task:
    """质量保障任务"""
    return Task(
        description=f"""
        基于产品设计和开发方案，制定质量保障计划：
        产品创意：{product_idea}
        
        请完成以下内容：
        1. 测试策略（单元测试/集成测试/E2E 测试）
        2. 测试用例设计（覆盖核心功能）
        3. 性能测试方案（负载测试、压力测试）
        4. 验收测试清单
        5. 发布检查清单
        
        输出格式：结构化的质量保障计划
        """,
        expected_output="一份质量保障计划，包含测试策略、用例设计、性能测试方案和验收清单",
        agent=qa_expert
    )

def create_prd_summary_task() -> Task:
    """PRD 汇总任务"""
    return Task(
        description="""
        汇总所有分析和设计结果，生成完整的 PRD 文档：
        
        请整合以下内容：
        1. 执行摘要（产品概述、目标用户、核心价值）
        2. 市场调研结论
        3. 产品功能设计
        4. 技术方案
        5. 开发计划
        6. 质量保障计划
        7. 风险与应对
        
        输出格式：标准 PRD 文档格式，可直接用于研发
        """,
        expected_output="一份完整的 PRD 文档，包含所有必要章节，可直接用于研发",
        agent=design_expert  # 由产品设计专家汇总
    )

# ==================== Crew 创建 ====================

def create_product_team(product_idea: str, verbose: bool = False):
    """
    创建产品需求收集团队
    
    Args:
        product_idea: 产品创意描述
        verbose: 是否显示详细输出
    
    Returns:
        Crew 对象
    """
    # 创建任务列表
    tasks = [
        create_market_research_task(product_idea),
        create_product_design_task(product_idea),
        create_architecture_task(product_idea),
        create_development_task(product_idea),
        create_qa_task(product_idea),
        create_prd_summary_task()
    ]
    
    # 创建团队
    crew = Crew(
        agents=[market_analyst, design_expert, tech_director, fullstack_dev, qa_expert],
        tasks=tasks,
        process=Process.sequential,  # 顺序执行
        verbose=verbose
    )
    
    return crew

# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例：创建一个需求收集机器人产品
    product_idea = """
    一个 AI 驱动的需求收集机器人，能够：
    - 主动引导客户沟通需求
    - 按 PRD 框架结构化提问
    - 自动输出标准 PRD 文档
    - 限制只能做需求沟通，不能做其他事情
    """
    
    # 创建团队
    crew = create_product_team(product_idea, verbose=True)
    
    # 执行
    print("🚀 开始产品需求分析...")
    result = crew.kickoff()
    
    print("\n✅ 完成！PRD 文档已生成")
    print(result)
