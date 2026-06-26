"""
CrewAI 团队 - 并行讨论版
先生，这个版本支持角色之间互相讨论和迭代
"""

from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
import os

# ==================== API 配置 ====================

DASHSCOPE_API_KEY = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
DASHSCOPE_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

os.environ["OPENAI_API_KEY"] = DASHSCOPE_API_KEY
os.environ["OPENAI_API_BASE"] = DASHSCOPE_BASE_URL

# ==================== 模型配置 ====================

MODELS = {
    "research": LLM(model="qwen3.5-plus", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.7),
    "design": LLM(model="qwen3-max-2026-01-23", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.8),
    "architecture": LLM(model="qwen3-coder-plus", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.5),
    "development": LLM(model="qwen3-coder-next", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.3),
    "qa": LLM(model="qwen3.5-plus", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.4)
}

# ==================== Agent 定义 ====================

market_analyst = Agent(
    role="市场调研分析师",
    goal="深度研究市场趋势和竞品，提供数据驱动的商业洞察",
    backstory="你是一位资深市场调研分析师，拥有 10 年科技行业研究经验。擅长竞品分析、用户研究、市场趋势分析。你的分析报告以数据为支撑，洞察深刻。",
    verbose=True,
    allow_delegation=True,  # ✅ 允许委托给其他角色
    llm=MODELS["research"]
)

design_expert = Agent(
    role="产品设计专家",
    goal="设计优秀的用户体验和产品方案",
    backstory="你是一位资深产品设计专家，曾在多家顶级科技公司工作。擅长产品功能设计、UI/UX 设计、用户流程优化。",
    verbose=True,
    allow_delegation=True,  # ✅ 允许委托
    llm=MODELS["design"]
)

tech_director = Agent(
    role="技术总监",
    goal="设计可扩展的技术架构",
    backstory="你是一位资深技术总监，有 15 年技术架构和团队管理经验。擅长分布式系统架构、技术选型、研发任务拆分。",
    verbose=True,
    allow_delegation=True,  # ✅ 允许委托
    llm=MODELS["architecture"]
)

fullstack_dev = Agent(
    role="全栈技术专家",
    goal="高质量完成代码开发",
    backstory="你是一位全栈技术专家，精通前后端开发。擅长 React/Vue、Node.js/Python、数据库设计、API 开发。",
    verbose=True,
    allow_delegation=False,
    llm=MODELS["development"]
)

qa_expert = Agent(
    role="质量专家",
    goal="确保产品质量符合标准",
    backstory="你是一位资深质量保障专家，对细节有严格要求。擅长测试用例设计、功能验证、性能测试。",
    verbose=True,
    allow_delegation=False,
    llm=MODELS["qa"]
)

# ==================== 任务定义（支持讨论） ====================

def create_discussion_tasks(product_idea: str):
    """
    创建支持讨论的任务
    特点：后续任务可以参考前面任务的输出，并可以要求返工
    """
    
    # 任务 1: 市场调研
    market_research = Task(
        description=f"""
        针对产品创意进行市场调研：
        产品创意：{product_idea}
        
        请分析：
        1. 目标用户画像
        2. 竞品分析（至少 3 个）
        3. 市场规模和趋势
        4. 市场机会点
        
        输出：结构化的市场调研报告
        """,
        expected_output="市场调研报告",
        agent=market_analyst
    )
    
    # 任务 2: 产品设计（可以参考市场调研结果）
    product_design = Task(
        description="""
        基于市场调研结果，进行产品设计：
        
        要求：
        1. 产品核心功能列表（P0/P1/P2 优先级）
        2. 用户流程图
        3. UI/UX 设计建议
        4. 产品验收标准
        
        注意：如果市场调研中发现重要信息，请在设计中体现
        
        输出：产品设计方案
        """,
        expected_output="产品设计方案",
        agent=design_expert,
        context=[market_research]  # ✅ 可以参考前一个任务的输出
    )
    
    # 任务 3: 技术架构（可以参考产品设计方案）
    tech_architecture = Task(
        description="""
        基于产品设计方案，设计技术架构：
        
        要求：
        1. 技术栈选型
        2. 系统架构描述
        3. 数据模型设计
        4. 研发任务拆分
        
        注意：
        - 如果产品功能有技术难点，请提出
        - 如果需要产品设计调整以适配技术，请说明
        
        输出：技术方案文档
        """,
        expected_output="技术方案文档",
        agent=tech_director,
        context=[product_design]  # ✅ 可以参考产品设计
    )
    
    # 任务 4: 开发实现
    development = Task(
        description="""
        基于技术方案，提供开发实现建议：
        
        要求：
        1. 项目目录结构
        2. 核心模块代码示例
        3. 数据库设计示例
        4. API 实现示例
        
        输出：开发指南
        """,
        expected_output="开发指南",
        agent=fullstack_dev,
        context=[tech_architecture]
    )
    
    # 任务 5: 质量保障
    qa_plan = Task(
        description="""
        基于产品设计和开发方案，制定质量保障计划：
        
        要求：
        1. 测试策略
        2. 测试用例设计
        3. 性能测试方案
        4. 验收测试清单
        
        输出：质量保障计划
        """,
        expected_output="质量保障计划",
        agent=qa_expert,
        context=[product_design, development]  # ✅ 可以参考多个任务
    )
    
    # 任务 6: 评审会议（所有角色参与讨论）
    review_meeting = Task(
        description="""
        组织一次产品评审会议，所有角色参与讨论：
        
        讨论议题：
        1. 市场调研是否充分？有没有遗漏的竞品或用户群体？
        2. 产品设计是否满足市场需求？有没有过度设计或设计不足？
        3. 技术方案是否可行？有没有技术风险？
        4. 开发工作量是否合理？是否需要分阶段？
        5. 质量保障是否全面？有没有遗漏的测试场景？
        
        每个角色请发表意见，并提出改进建议。
        
        输出：评审会议纪要，包含所有角色的意见和最终改进方案
        """,
        expected_output="评审会议纪要和改进方案",
        agent=design_expert,  # 由产品设计专家组织
        context=[market_research, product_design, tech_architecture, development, qa_plan]
    )
    
    return [
        market_research,
        product_design,
        tech_architecture,
        development,
        qa_plan,
        review_meeting  # ✅ 新增：评审会议，所有角色讨论
    ]

# ==================== Crew 创建 ====================

def create_discussion_team(product_idea: str, verbose: bool = False):
    """
    创建支持讨论的团队
    
    特点：
    - 任务之间可以传递上下文
    - 最后有评审会议，所有角色参与讨论
    - 支持返工和迭代
    """
    
    tasks = create_discussion_tasks(product_idea)
    
    # 使用 Hierarchical 模式，让设计专家作为主管协调讨论
    crew = Crew(
        agents=[market_analyst, design_expert, tech_director, fullstack_dev, qa_expert],
        tasks=tasks,
        process=Process.sequential,  # 顺序执行，但任务间有上下文传递
        verbose=verbose
    )
    
    return crew

if __name__ == "__main__":
    product_idea = "一个 AI 驱动的需求收集机器人"
    crew = create_discussion_team(product_idea, verbose=False)
    
    print("=" * 60)
    print("✅ CrewAI 讨论版团队配置完成")
    print("=" * 60)
    print("\n👥 团队成员:")
    for agent in crew.agents:
        print(f"  - {agent.role}")
    
    print(f"\n📋 任务数量：{len(crew.tasks)}")
    print("\n💬 讨论特性:")
    print("  ✅ 任务间传递上下文")
    print("  ✅ 最后有评审会议")
    print("  ✅ 所有角色参与讨论")
    print("=" * 60)
