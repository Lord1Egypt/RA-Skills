"""
CrewAI 团队 - 极简实用版配置
先生，这个版本只保留最核心的功能，去掉所有花里胡哨的东西
"""

from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
import os

# ==================== API 配置 ====================

DASHSCOPE_API_KEY = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
DASHSCOPE_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

os.environ["OPENAI_API_KEY"] = DASHSCOPE_API_KEY
os.environ["OPENAI_API_BASE"] = DASHSCOPE_BASE_URL

# ==================== 模型配置（全部用性价比最高的） ====================

# 所有角色都用 qwen3.5-plus，够用就好
llm = LLM(
    model="qwen3.5-plus",
    base_url=DASHSCOPE_BASE_URL,
    api_key=DASHSCOPE_API_KEY,
    temperature=0.5  # 适中，务实
)

# ==================== 精简版 Agent 定义（只保留 3 个核心角色） ====================

# 1. 产品经理（兼任市场调研）
product_manager = Agent(
    role="产品经理",
    goal="定义最核心的功能，砍掉所有不必要的东西",
    backstory="""你是一位务实的产品经理，信奉"少即是多"。
你擅长：
- 识别核心痛点
- 砍掉花里胡哨的功能
- 聚焦 MVP

你的口头禅："这个功能真的必要吗？" """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. 技术负责人（兼任架构师和开发）
tech_lead = Agent(
    role="技术负责人",
    goal="用最简单的技术方案解决问题",
    backstory="""你是一位务实的技术负责人，有 10 年经验。
你擅长：
- 选择成熟稳定的技术
- 避免过度设计
- 快速交付可用产品

你的口头禅："能跑就行，别整那些花里胡哨的。" """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 3. 测试工程师（兼任质量保障）
qa_engineer = Agent(
    role="测试工程师",
    goal="确保核心功能没问题，其他无所谓",
    backstory="""你是一位务实的测试工程师。
你擅长：
- 测试核心流程
- 发现致命 bug
- 忽略边缘情况

你的口头禅："主流程能跑通就行。" """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==================== 精简版任务定义 ====================

def create_mvp_tasks(product_idea: str):
    """
    创建极简版任务，只关注核心
    """
    
    # 任务 1: 定义核心功能（砍掉 80% 不必要的）
    core_features = Task(
        description=f"""
        针对产品创意，只定义**最核心**的功能：
        产品创意：{product_idea}
        
        要求：
        1. 列出用户**最痛**的 3 个痛点
        2. 只保留**必须实现**的功能（P0），其他全部砍掉
        3. 每个功能用一句话说清楚价值
        4. 明确**不做**什么功能
        
        输出：简洁的功能清单（不超过 5 个功能）
        """,
        expected_output="核心功能清单（不超过 5 个）",
        agent=product_manager
    )
    
    # 任务 2: 技术方案（越简单越好）
    simple_tech = Task(
        description="""
        基于核心功能，设计**最简单**的技术方案：
        
        要求：
        1. 技术栈选**最成熟**的，不追新
        2. 能单体就不微服务，能单机就不集群
        3. 只设计**核心**数据表（不超过 5 张）
        4. 只定义**核心**API（不超过 10 个）
        5. 预估**最少**开发时间（人天）
        
        输出：简洁的技术方案
        """,
        expected_output="简洁技术方案",
        agent=tech_lead,
        context=[core_features]
    )
    
    # 任务 3: 核心测试（只测主流程）
    simple_qa = Task(
        description="""
        只测试**核心流程**，其他不管：
        
        要求：
        1. 只写**主流程**测试用例（不超过 10 个）
        2. 只关注**致命**和**严重**bug
        3. 性能要求：能用就行，不追求极致
        4. 发布标准：主流程无 bug 就上线
        
        输出：简洁的测试清单
        """,
        expected_output="简洁测试清单",
        agent=qa_engineer,
        context=[simple_tech]
    )
    
    # 任务 4: 最终总结（一页纸 PRD）
    one_page_prd = Task(
        description="""
        把所有内容总结到**一页纸**：
        
        包含：
        1. 产品定位（一句话说清楚）
        2. 核心功能（不超过 5 个）
        3. 技术方案（技术栈 + 核心表）
        4. 开发计划（几周 + 几人）
        5. 发布标准（主流程无 bug）
        
        输出：一页纸 PRD（不超过 2000 字）
        """,
        expected_output="一页纸 PRD",
        agent=product_manager,
        context=[core_features, simple_tech, simple_qa]
    )
    
    return [
        core_features,    # 1. 核心功能
        simple_tech,      # 2. 技术方案
        simple_qa,        # 3. 核心测试
        one_page_prd      # 4. 一页纸总结
    ]

# ==================== Crew 创建 ====================

def create_minimal_team(product_idea: str, verbose: bool = False):
    """
    创建极简团队
    
    特点：
    - 只保留 3 个核心角色
    - 只定义核心功能（不超过 5 个）
    - 技术方案越简单越好
    - 输出一页纸 PRD
    """
    
    tasks = create_mvp_tasks(product_idea)
    
    crew = Crew(
        agents=[product_manager, tech_lead, qa_engineer],
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose
    )
    
    return crew

if __name__ == "__main__":
    product_idea = "一个简化 OpenClaw 对接的 App"
    crew = create_minimal_team(product_idea, verbose=False)
    
    print("=" * 60)
    print("✅ CrewAI 极简实用版团队配置完成")
    print("=" * 60)
    print("\n👥 团队成员（只保留核心角色）:")
    print(f"  📋 产品经理（定义核心功能）")
    print(f"  🛠️ 技术负责人（简单技术方案）")
    print(f"  ✅ 测试工程师（只测主流程）")
    
    print(f"\n📋 任务数量：{len(crew.tasks)}")
    print("\n🎯 极简原则:")
    print("  ✅ 功能不超过 5 个")
    print("  ✅ 数据表不超过 5 张")
    print("  ✅ API 不超过 10 个")
    print("  ✅ 测试用例不超过 10 个")
    print("  ✅ 输出一页纸 PRD")
    print("\n⏱️ 预计时间：2-4 分钟")
    print("=" * 60)
