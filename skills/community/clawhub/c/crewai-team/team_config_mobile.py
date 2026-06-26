"""
CrewAI 团队 - 移动端极简版配置
先生，这个版本专注于移动端 App，连接自建 OpenClaw，一切以简便实用为主
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

llm = LLM(
    model="qwen3.5-plus",
    base_url=DASHSCOPE_BASE_URL,
    api_key=DASHSCOPE_API_KEY,
    temperature=0.5
)

# ==================== 移动端专属 Agent 定义（3 个核心角色） ====================

# 1. 产品经理（移动端专家）
product_manager = Agent(
    role="移动端产品经理",
    goal="定义移动端最核心的功能，砍掉所有不必要的",
    backstory="""你是一位专注移动端的产品经理，信奉"手指友好，极简操作"。
你擅长：
- 识别移动端核心场景
- 砍掉桌面端思维的功能
- 聚焦单手操作体验

你的口头禅："这个功能在手机上真的用得上吗？" """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. 移动端技术负责人（跨平台专家）
mobile_tech_lead = Agent(
    role="移动端技术负责人",
    goal="用最简单的跨平台方案，一套代码多端运行",
    backstory="""你是一位务实的移动端架构师，有 10 年经验。
你擅长：
- 选择跨平台框架（Flutter/React Native）
- 避免原生开发的双倍成本
- 设计简洁的 API 接口

你的口头禅："能跨平台就别原生，一套代码搞定。" """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 3. UX 设计师（移动端体验）
ux_designer = Agent(
    role="移动端 UX 设计师",
    goal="设计简单直观的移动端界面，老人都会用",
    backstory="""你是一位专注移动端的 UX 设计师。
你擅长：
- 设计大按钮和清晰反馈
- 减少输入，多用选择
- 优化弱网和离线体验

你的口头禅："别让用户思考，点一下就行。" """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==================== 移动端专属任务定义 ====================

def create_mobile_tasks(product_idea: str):
    """
    创建移动端专属任务，只关注核心
    """
    
    # 任务 1: 移动端核心功能（和桌面端完全不同）
    mobile_features = Task(
        description=f"""
        针对移动端产品创意，只定义**手机上最实用**的功能：
        产品创意：{product_idea}
        
        要求：
        1. 列出移动端**特有**的 3 个使用场景（和桌面端不同）
        2. 只保留**必须实现**的功能（P0），不超过 5 个
        3. 每个功能用一句话说清楚**在什么场景下用**
        4. 明确**不做**什么功能（桌面端功能直接砍掉）
        
        输出：简洁的移动端功能清单
        """,
        expected_output="移动端核心功能清单（不超过 5 个）",
        agent=product_manager
    )
    
    # 任务 2: 跨平台技术方案（Flutter/React Native 二选一）
    mobile_tech = Task(
        description="""
        基于核心功能，设计**最简单**的移动端技术方案：
        
        要求：
        1. 框架选择：Flutter 或 React Native（二选一，说明理由）
        2. 只设计**核心**页面（不超过 5 个）
        3. 只定义**核心**API（不超过 10 个，考虑弱网）
        4. 数据存储：本地 SQLite 或 AsyncStorage
        5. 预估**最少**开发时间（人天）
        
        输出：简洁的移动端技术方案
        """,
        expected_output="简洁移动端技术方案",
        agent=mobile_tech_lead,
        context=[mobile_features]
    )
    
    # 任务 3: 移动端 UX 设计（大按钮，少输入）
    mobile_ux = Task(
        description="""
        设计**简单直观**的移动端界面：
        
        要求：
        1. 核心流程图（不超过 5 步完成主要任务）
        2. 界面设计原则：
           - 按钮够大（最小 44x44pt）
           - 文字清晰（最小 14pt）
           - 减少输入（多用选择/扫码）
           - 即时反馈（加载/成功/失败）
        3. 弱网和离线体验设计
        4. 单手操作优化
        
        输出：简洁的 UX 设计方案
        """,
        expected_output="简洁 UX 设计方案",
        agent=ux_designer,
        context=[mobile_tech]
    )
    
    # 任务 4: 一页纸 PRD（移动端专属）
    one_page_prd = Task(
        description="""
        把所有内容总结到**一页纸**：
        
        包含：
        1. 产品定位（一句话说清楚移动端价值）
        2. 核心功能（不超过 5 个，移动端特有场景）
        3. 技术方案（跨平台框架 + 核心页面）
        4. 开发计划（几周 + 几人）
        5. 发布标准（主流程无 bug + 核心体验流畅）
        
        输出：一页纸 PRD（不超过 2000 字）
        """,
        expected_output="一页纸移动端 PRD",
        agent=product_manager,
        context=[mobile_features, mobile_tech, mobile_ux]
    )
    
    return [
        mobile_features,  # 1. 移动端核心功能
        mobile_tech,      # 2. 跨平台技术方案
        mobile_ux,        # 3. 移动端 UX 设计
        one_page_prd      # 4. 一页纸总结
    ]

# ==================== Crew 创建 ====================

def create_mobile_team(product_idea: str, verbose: bool = False):
    """
    创建移动端极简团队
    
    特点：
    - 只保留 3 个移动端核心角色
    - 只定义移动端核心功能（不超过 5 个）
    - 跨平台技术方案（Flutter/React Native）
    - 输出一页纸 PRD
    """
    
    tasks = create_mobile_tasks(product_idea)
    
    crew = Crew(
        agents=[product_manager, mobile_tech_lead, ux_designer],
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose
    )
    
    return crew

if __name__ == "__main__":
    product_idea = "移动端 OpenClaw 连接 App"
    crew = create_mobile_team(product_idea, verbose=False)
    
    print("=" * 60)
    print("✅ CrewAI 移动端极简版团队配置完成")
    print("=" * 60)
    print("\n👥 团队成员（移动端专属）:")
    print(f"  📱 移动端产品经理（定义核心场景）")
    print(f"  🛠️ 移动端技术负责人（跨平台方案）")
    print(f"  🎨 UX 设计师（简单直观界面）")
    
    print(f"\n📋 任务数量：{len(crew.tasks)}")
    print("\n🎯 移动端原则:")
    print("  ✅ 功能不超过 5 个（移动端特有）")
    print("  ✅ 页面不超过 5 个")
    print("  ✅ API 不超过 10 个（考虑弱网）")
    print("  ✅ 跨平台框架（Flutter/React Native）")
    print("  ✅ 输出一页纸 PRD")
    print("\n⏱️ 预计时间：2-4 分钟")
    print("=" * 60)
