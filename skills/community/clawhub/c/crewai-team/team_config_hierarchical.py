"""
CrewAI 团队 - Hierarchical 层级执行版
先生，这个版本由主管统一协调，部分任务并行执行

模式 2: Hierarchical
- 👔 主管：产品设计专家（协调所有角色）
- ⚡ 部分并行：调研、架构可以同时进行
- 📊 主管负责任务分配和结果整合
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
    "manager": LLM(model="qwen3-max-2026-01-23", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.7),
    "research": LLM(model="qwen3.5-plus", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.7),
    "architecture": LLM(model="qwen3-coder-plus", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.5),
    "development": LLM(model="qwen3-coder-next", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.3),
    "qa": LLM(model="qwen3.5-plus", base_url=DASHSCOPE_BASE_URL, api_key=DASHSCOPE_API_KEY, temperature=0.4)
}

# ==================== Agent 定义 ====================

# 👔 主管 Agent（产品设计专家兼任）
manager_agent = Agent(
    role="首席产品官 & 团队主管",
    goal="协调团队工作，确保产品质量和进度",
    backstory="""你是一位资深首席产品官，有 20 年产品管理和团队协调经验。
你擅长：
- 任务分解和分配
- 跨角色协调
- 质量把控
- 决策和风险管理

你负责协调市场调研、技术架构、开发和质检团队，确保产品成功交付。""",
    verbose=True,
    allow_delegation=True,
    llm=MODELS["manager"]
)

# 📊 市场调研分析师
market_analyst = Agent(
    role="市场调研分析师",
    goal="提供数据驱动的市场洞察",
    backstory="你是一位资深市场调研分析师，拥有 10 年科技行业研究经验。擅长竞品分析、用户研究、市场趋势分析。",
    verbose=True,
    allow_delegation=False,
    llm=MODELS["research"]
)

# 🏗️ 技术总监
tech_director = Agent(
    role="技术总监",
    goal="设计可扩展的技术架构",
    backstory="你是一位资深技术总监，有 15 年技术架构经验。擅长分布式系统架构、技术选型、研发任务拆分。",
    verbose=True,
    allow_delegation=False,
    llm=MODELS["architecture"]
)

# 💻 全栈技术专家
fullstack_dev = Agent(
    role="全栈技术专家",
    goal="高质量完成代码开发",
    backstory="你是一位全栈技术专家，精通前后端开发。擅长 React/Vue、Node.js/Python、数据库设计、API 开发。",
    verbose=True,
    allow_delegation=False,
    llm=MODELS["development"]
)

# ✅ 质量专家
qa_expert = Agent(
    role="质量专家",
    goal="确保产品质量符合标准",
    backstory="你是一位资深质量保障专家，对细节有严格要求。擅长测试用例设计、功能验证、性能测试。",
    verbose=True,
    allow_delegation=False,
    llm=MODELS["qa"]
)

# ==================== 任务定义 ====================

def create_hierarchical_tasks(product_idea: str):
    """
    创建层级模式的任务
    特点：主管负责任务分配和结果整合
    """
    
    # 任务 1: 项目启动（主管负责）
    project_kickoff = Task(
        description=f"""
        启动产品分析项目：
        产品创意：{product_idea}
        
        请完成：
        1. 分析产品创意的核心价值
        2. 识别关键风险点
        3. 制定分析计划
        4. 分配任务给各角色：
           - 市场调研分析师：用户画像和竞品分析
           - 技术总监：技术可行性评估
           - 全栈技术专家：技术选型建议
           - 质量专家：质量风险评估
        
        输出：项目启动报告，包含任务分配清单
        """,
        expected_output="项目启动报告",
        agent=manager_agent
    )
    
    # 任务 2: 市场调研（并行任务 1）
    market_research = Task(
        description="""
        执行市场调研（根据主管的任务分配）：
        
        请分析：
        1. 目标用户画像（年龄、职业、痛点、使用场景）
        2. 竞品分析（至少 3 个直接竞品）
        3. 市场规模和趋势
        4. 市场机会点和建议
        
        输出：市场调研报告
        """,
        expected_output="市场调研报告",
        agent=market_analyst,
        context=[project_kickoff]
    )
    
    # 任务 3: 技术评估（并行任务 2）
    tech_assessment = Task(
        description="""
        执行技术评估（根据主管的任务分配）：
        
        请分析：
        1. 技术可行性
        2. 技术栈选型建议
        3. 技术风险评估
        4. 研发工作量预估
        
        输出：技术评估报告
        """,
        expected_output="技术评估报告",
        agent=tech_director,
        context=[project_kickoff]
    )
    
    # 任务 4: 整合报告（主管整合调研和技术评估）
    integration_report = Task(
        description="""
        整合市场调研和技术评估结果：
        
        请完成：
        1. 综合市场和技术分析
        2. 产品功能优先级排序（P0/P1/P2）
        3. 产品路线图规划
        4. 资源需求评估
        
        输出：整合分析报告
        """,
        expected_output="整合分析报告",
        agent=manager_agent,
        context=[market_research, tech_assessment]
    )
    
    # 任务 5: 开发计划
    development_plan = Task(
        description="""
        基于整合报告，制定开发计划：
        
        请完成：
        1. 项目目录结构设计
        2. 核心模块开发计划
        3. 里程碑规划
        4. 开发资源分配建议
        
        输出：开发计划文档
        """,
        expected_output="开发计划文档",
        agent=fullstack_dev,
        context=[integration_report]
    )
    
    # 任务 6: 质量保障计划
    qa_plan = Task(
        description="""
        基于整合报告和开发计划，制定质量保障计划：
        
        请完成：
        1. 测试策略
        2. 测试用例设计大纲
        3. 性能测试方案
        4. 发布标准
        
        输出：质量保障计划
        """,
        expected_output="质量保障计划",
        agent=qa_expert,
        context=[integration_report, development_plan]
    )
    
    # 任务 7: 最终汇报（主管向用户汇报）
    final_presentation = Task(
        description="""
        向用户做最终汇报：
        
        请整合所有内容，形成完整的 PRD 文档：
        1. 执行摘要
        2. 市场调研结论
        3. 技术方案
        4. 开发计划
        5. 质量保障计划
        6. 风险与应对
        7. 下一步行动建议
        
        输出：完整 PRD 文档
        """,
        expected_output="完整 PRD 文档",
        agent=manager_agent,
        context=[integration_report, development_plan, qa_plan]
    )
    
    return [
        project_kickoff,      # 1. 项目启动（主管）
        market_research,      # 2. 市场调研（并行）
        tech_assessment,      # 3. 技术评估（并行）
        integration_report,   # 4. 整合报告（主管）
        development_plan,     # 5. 开发计划
        qa_plan,              # 6. 质量保障
        final_presentation    # 7. 最终汇报（主管）
    ]

# ==================== Crew 创建 ====================

def create_hierarchical_team(product_idea: str, verbose: bool = False):
    """
    创建层级执行团队
    
    特点：
    - 主管统一协调
    - 部分任务并行（市场调研 + 技术评估）
    - 主管负责任务分配和结果整合
    """
    
    tasks = create_hierarchical_tasks(product_idea)
    
    # 使用 Hierarchical 模式
    crew = Crew(
        agents=[market_analyst, tech_director, fullstack_dev, qa_expert],  # ⭐ 不包含主管
        tasks=tasks,
        process=Process.hierarchical,  # ⭐ 层级模式
        manager_agent=manager_agent,   # ⭐ 指定主管
        verbose=verbose
    )
    
    return crew

if __name__ == "__main__":
    product_idea = "一个 AI 驱动的需求收集机器人"
    crew = create_hierarchical_team(product_idea, verbose=False)
    
    print("=" * 70)
    print("✅ CrewAI Hierarchical 团队配置完成")
    print("=" * 70)
    print("\n👥 团队结构:")
    print("  👔 首席产品官 & 团队主管（产品设计专家）")
    print("  📊 市场调研分析师")
    print("  🏗️ 技术总监")
    print("  💻 全栈技术专家")
    print("  ✅ 质量专家")
    
    print(f"\n📋 任务数量：{len(crew.tasks)}")
    print("\n⚡ 执行特性:")
    print("  ✅ 主管统一协调")
    print("  ✅ 部分并行（调研 + 技术评估）")
    print("  ✅ 主管负责任务分配和整合")
    print("\n⏱️ 预计时间：4-8 分钟")
    print("=" * 70)
