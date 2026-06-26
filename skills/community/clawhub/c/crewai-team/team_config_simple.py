"""
CrewAI 产品需求收集团队配置 - 简化版
先生，这个版本使用 CrewAI 内置工具，减少外部依赖
"""

from crewai import Agent, Task, Crew, Process
import os

# ==================== LLM 配置 ====================

# 使用阿里云 DashScope (Qwen 模型)
# API Key 已配置在 ~/.openclaw/openclaw.json 中
dashscope_api_key = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"

os.environ["OPENAI_API_KEY"] = dashscope_api_key
os.environ["OPENAI_API_BASE"] = "https://coding.dashscope.aliyuncs.com/v1"

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
    allow_delegation=False
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
    allow_delegation=False
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
    allow_delegation=False
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
    allow_delegation=False
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
    allow_delegation=False
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
        3. 市场规模和趋势
        4. 竞品定价策略分析
        5. 市场机会点和建议
        
        输出格式：结构化的市场调研报告
        """,
        expected_output="市场调研报告，包含用户画像、竞品分析、市场规模、定价策略和机会点",
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
        3. 信息架构设计
        4. UI/UX 设计建议
        5. 产品验收标准
        
        输出格式：结构化的产品设计方案
        """,
        expected_output="产品设计方案，包含功能列表、用户流程、信息架构、UI 建议和验收标准",
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
        2. 系统架构描述
        3. 数据模型设计
        4. API 设计概要
        5. 研发任务拆分
        6. 技术风险评估
        
        输出格式：结构化的技术方案文档
        """,
        expected_output="技术方案文档，包含技术栈、架构、数据模型、API 设计和任务拆分",
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
        2. 核心模块代码示例
        3. 数据库设计示例
        4. API 实现示例
        
        输出格式：结构化的开发指南
        """,
        expected_output="开发指南，包含项目结构、核心代码示例和 API 实现",
        agent=fullstack_dev
    )

def create_qa_task(product_idea: str) -> Task:
    """质量保障任务"""
    return Task(
        description=f"""
        基于产品设计和开发方案，制定质量保障计划：
        产品创意：{product_idea}
        
        请完成以下内容：
        1. 测试策略
        2. 测试用例设计
        3. 性能测试方案
        4. 验收测试清单
        5. 发布检查清单
        
        输出格式：结构化的质量保障计划
        """,
        expected_output="质量保障计划，包含测试策略、用例设计、性能测试方案和验收清单",
        agent=qa_expert
    )

def create_prd_summary_task() -> Task:
    """PRD 汇总任务"""
    return Task(
        description="""
        汇总所有分析和设计结果，生成完整的 PRD 文档：
        
        请整合以下内容：
        1. 执行摘要
        2. 市场调研结论
        3. 产品功能设计
        4. 技术方案
        5. 开发计划
        6. 质量保障计划
        7. 风险与应对
        
        输出格式：标准 PRD 文档
        """,
        expected_output="完整的 PRD 文档",
        agent=design_expert
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
    tasks = [
        create_market_research_task(product_idea),
        create_product_design_task(product_idea),
        create_architecture_task(product_idea),
        create_development_task(product_idea),
        create_qa_task(product_idea),
        create_prd_summary_task()
    ]
    
    crew = Crew(
        agents=[market_analyst, design_expert, tech_director, fullstack_dev, qa_expert],
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose
    )
    
    return crew

if __name__ == "__main__":
    product_idea = "一个 AI 驱动的需求收集机器人"
    crew = create_product_team(product_idea, verbose=True)
    print("团队创建成功！")
    print(f"Agent 数量：{len(crew.agents)}")
    print(f"任务数量：{len(crew.tasks)}")
