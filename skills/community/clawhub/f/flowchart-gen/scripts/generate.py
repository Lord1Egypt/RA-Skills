#!/usr/bin/env python3
"""
流程图生成器 - 将自然语言描述或Mermaid代码转换为流程图图片

版本: 1.0.0
发布日期: 2026-03-17

功能：
1. 将自然语言描述转换为Mermaid流程图代码（DeepSeek API智能生成）
2. 使用Mermaid CLI将代码渲染为PNG/SVG/PDF
3. 支持8种Mermaid图表类型和31个预置模板
4. 智能错误处理和故障排除系统
"""

import argparse
import subprocess
import os
import sys
import tempfile
from pathlib import Path
import json

# 版本信息
__version__ = "1.1.0"
__release_date__ = "2026-04-17"

# 设置Puppeteer使用系统Chrome
if 'PUPPETEER_EXECUTABLE_PATH' not in os.environ:
    chrome_paths = [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    ]
    for path in chrome_paths:
        if os.path.exists(path):
            os.environ['PUPPETEER_EXECUTABLE_PATH'] = path
            break

# ============================================================================
# 配置
# ============================================================================

DEFAULT_OUTPUT = "flowchart.png"
SUPPORTED_FORMATS = ["png", "svg", "pdf"]
SUPPORTED_THEMES = ["default", "dark", "forest", "neutral"]

# LLM API配置（支持DeepSeek和OpenAI）
LLM_CONFIG = {
    "provider": "deepseek",  # deepseek 或 openai
    "api_key": None,
    "base_url": "https://api.deepseek.com/v1",  # DeepSeek默认，OpenAI会自动覆盖
    "model": "deepseek-chat",  # deepseek-chat 或 gpt-4o
    "timeout": 30
}

def load_llm_config(args=None):
    """
    加载LLM API配置，支持DeepSeek和OpenAI
    
    优先级（从高到低）：
    1. 命令行参数 (--api-key, --api-provider, --api-base-url)
    2. 环境变量 (DEEPSEEK_API_KEY, OPENAI_API_KEY)
    3. OpenClaw配置文件 (~/.openclaw/openclaw.json)
    
    参数:
        args: argparse.Namespace对象，包含命令行参数
    
    返回:
        bool: 是否成功加载配置
    """
    import json
    import os
    
    # 重置配置
    LLM_CONFIG.update({
        "provider": "deepseek",
        "api_key": None,
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "timeout": 30
    })
    
    # 1. 检查命令行参数（优先级最高）
    if args and args.api_key:
        LLM_CONFIG["api_key"] = args.api_key
        if args.api_provider:
            LLM_CONFIG["provider"] = args.api_provider
        if args.api_base_url:
            LLM_CONFIG["base_url"] = args.api_base_url
        
        # 根据provider设置默认值
        if LLM_CONFIG["provider"] == "openai":
            if not args.api_base_url:
                LLM_CONFIG["base_url"] = "https://api.openai.com/v1"
            LLM_CONFIG["model"] = "gpt-4o"
        else:  # deepseek
            if not args.api_base_url:
                LLM_CONFIG["base_url"] = "https://api.deepseek.com/v1"
            LLM_CONFIG["model"] = "deepseek-chat"
        
        return True
    
    # 2. 检查环境变量
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    
    if deepseek_key:
        LLM_CONFIG["provider"] = "deepseek"
        LLM_CONFIG["api_key"] = deepseek_key
        LLM_CONFIG["base_url"] = "https://api.deepseek.com/v1"
        LLM_CONFIG["model"] = "deepseek-chat"
        return True
    
    if openai_key:
        LLM_CONFIG["provider"] = "openai"
        LLM_CONFIG["api_key"] = openai_key
        LLM_CONFIG["base_url"] = "https://api.openai.com/v1"
        LLM_CONFIG["model"] = "gpt-4o"
        return True
    
    # 3. 检查OpenClaw配置文件（DeepSeek配置）
    config_paths = [
        os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json"),
        "C:\\Users\\AA\\.openclaw\\openclaw.json"  # Windows特定路径
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 提取DeepSeek配置
                providers = config.get("models", {}).get("providers", {})
                deepseek_config = providers.get("custom-api-deepseek-com", {})
                
                if deepseek_config:
                    LLM_CONFIG["provider"] = "deepseek"
                    LLM_CONFIG["api_key"] = deepseek_config.get("apiKey") or deepseek_config.get("api_key")
                    LLM_CONFIG["base_url"] = deepseek_config.get("baseUrl") or deepseek_config.get("base_url", "https://api.deepseek.com/v1")
                    
                    # 检查是否有可用的模型
                    models = deepseek_config.get("models", [])
                    if models:
                        # 优先使用deepseek-chat，如果没有则使用第一个
                        chat_model = next((m for m in models if m.get("id") == "deepseek-chat"), None)
                        if chat_model:
                            LLM_CONFIG["model"] = "deepseek-chat"
                        else:
                            LLM_CONFIG["model"] = models[0].get("id", "deepseek-chat")
                    
                    return True
            except Exception:
                pass
    
    # 没有找到任何配置
    return False

# ============================================================================
# 环境依赖检查和错误处理
# ============================================================================

class EnvironmentError(Exception):
    """环境依赖错误"""
    pass

def check_mermaid_cli():
    """检查Mermaid CLI是否可用"""
    import subprocess
    import os
    import sys
    
    # 在Windows上，可能需要使用mmdc.cmd
    if sys.platform == "win32":
        commands_to_try = ["mmdc.cmd", "mmdc"]
    else:
        commands_to_try = ["mmdc"]
    
    for cmd in commands_to_try:
        try:
            # 在Windows上使用shell=True可能更可靠
            if sys.platform == "win32":
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True, shell=True)
            else:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
        except (FileNotFoundError, OSError):
            continue
    
    return False

def check_environment_dependencies(verbose: bool = False) -> tuple[bool, list[str]]:
    """
    检查环境依赖是否满足
    
    Returns:
        (是否满足依赖, 缺失依赖列表)
    """
    missing_deps = []
    
    # 检查Mermaid CLI
    if not check_mermaid_cli():
        missing_deps.append("Mermaid CLI (mmdc)")
        if verbose:
            print("[WARN] 未找到Mermaid CLI (mmdc)")
    
    # 检查Python库
    try:
        import requests
    except ImportError:
        missing_deps.append("requests库")
        if verbose:
            print("[WARN] 未找到requests库")
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("PIL库 (pillow)")
        if verbose:
            print("[WARN] 未找到PIL库 (pillow)")
    
    return len(missing_deps) == 0, missing_deps

def print_dependency_help(missing_deps: list[str]):
    """打印依赖安装帮助"""
    if not missing_deps:
        return
    
    print("\n" + "="*60)
    print("环境依赖问题")
    print("="*60)
    
    for dep in missing_deps:
        if dep == "Mermaid CLI (mmdc)":
            print(f"\n❌ 缺少Mermaid CLI (mmdc)")
            print("   安装方法: npm install -g @mermaid-js/mermaid-cli")
            print("   验证安装: mmdc --version")
            print("   注意事项:")
            print("     - 确保Node.js已安装 (node --version)")
            print("     - 如果使用Windows，可能需要管理员权限")
            print("     - 如果网络问题，使用淘宝镜像:")
            print("       npm config set registry https://registry.npmmirror.com")
            print("       npm install -g @mermaid-js/mermaid-cli")
            print("       npm config set registry https://registry.npmjs.org")
        
        elif dep == "requests库":
            print(f"\n❌ 缺少requests库")
            print("   安装方法: pip install requests")
            print("   或: python -m pip install requests")
        
        elif dep == "PIL库 (pillow)":
            print(f"\n❌ 缺少PIL库 (pillow)")
            print("   安装方法: pip install pillow")
            print("   或: python -m pip install pillow")
    
    print("\n" + "="*60)

def load_llm_config_verbose():
    """显示LLM API配置状态（详细输出）"""
    import os
    
    # 显示当前配置状态
    provider = LLM_CONFIG["provider"]
    api_key = LLM_CONFIG["api_key"]
    model = LLM_CONFIG["model"]
    base_url = LLM_CONFIG["base_url"]
    
    if api_key:
        api_key_preview = api_key[:10] + '...' if len(api_key) > 10 else '***'
        print(f"[INFO] {provider} API配置: 密钥={api_key_preview}, 模型={model}, 端点={base_url}")
        return True
    else:
        # 检查环境变量
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")
        
        if deepseek_key:
            print(f"[INFO] 找到环境变量 DEEPSEEK_API_KEY (长度={len(deepseek_key)})")
            print(f"      设置 provider=deepseek, 模型=deepseek-chat")
            return True
        elif openai_key:
            print(f"[INFO] 找到环境变量 OPENAI_API_KEY (长度={len(openai_key)})")
            print(f"      设置 provider=openai, 模型=gpt-4o")
            return True
        else:
            print("[WARN] 未找到LLM API配置")
            print("      可能的配置方式:")
            print("      1. 设置环境变量 DEEPSEEK_API_KEY 或 OPENAI_API_KEY")
            print("      2. 配置OpenClaw的DeepSeek设置（~/.openclaw/openclaw.json）")
            print("      3. 使用 --no-llm 参数跳过API调用，使用模板匹配")
            return False

# 加载配置
CONFIG_LOADED = load_llm_config()

# ============================================================================
# 模板系统
# ============================================================================

TEMPLATES = {
    "login": """graph TD
    A[用户访问网站] --> B{已登录?}
    B -->|否| C[显示登录表单]
    B -->|是| D[跳转到首页]
    C --> E[输入用户名密码]
    E --> F{验证成功?}
    F -->|是| D
    F -->|否| G[显示错误信息]
    G --> C""",
    
    "api-call": """sequenceDiagram
    participant Client
    participant API
    participant DB
    
    Client->>API: 请求
    API->>DB: 查询
    DB-->>API: 数据
    API-->>Client: 响应""",
    
    "shopping": """graph TD
    A[浏览商品] --> B[加入购物车]
    B --> C{继续购物?}
    C -->|是| A
    C -->|否| D[结算]
    D --> E[填写收货信息]
    E --> F[选择支付方式]
    F --> G[确认订单]
    G --> H[完成购买]""",
    
    "decision": """graph TD
    A[开始] --> B{条件判断}
    B -->|条件1| C[操作1]
    B -->|条件2| D[操作2]
    B -->|条件3| E[操作3]
    C --> F[结束]
    D --> F
    E --> F""",
    
    # ============================================================================
    # 业务流程类模板
    # ============================================================================
    
    "order-processing": """graph TD
    A[客户下单] --> B[订单创建]
    B --> C[库存检查]
    C --> D{库存充足?}
    D -->|是| E[订单确认]
    D -->|否| F[通知库存不足]
    F --> G[订单取消]
    E --> H[准备发货]
    H --> I[生成运单]
    I --> J[发货]
    J --> K[客户收货]
    K --> L[订单完成]""",
    
    "customer-service": """graph TD
    A[客户提交问题] --> B[客服接收]
    B --> C[问题分类]
    C --> D{问题类型}
    D -->|技术问题| E[转技术部门]
    D -->|账单问题| F[转财务部门]
    D -->|一般咨询| G[客服直接处理]
    E --> H[技术解决]
    F --> I[财务处理]
    G --> J[客服回复]
    H --> K[回复客户]
    I --> K
    J --> K
    K --> L[问题关闭]""",
    
    "inventory-management": """graph TD
    A[库存监控] --> B{库存低于阈值?}
    B -->|是| C[生成采购需求]
    B -->|否| D[继续监控]
    C --> E[采购审批]
    E --> F[采购执行]
    F --> G[货物验收]
    G --> H[入库登记]
    H --> I[库存更新]
    I --> D""",
    
    "refund-process": """graph TD
    A[客户申请退款] --> B[客服初审]
    B --> C{符合退款政策?}
    C -->|是| D[财务审核]
    C -->|否| E[拒绝退款]
    E --> F[通知客户]
    D --> G{审核通过?}
    G -->|是| H[执行退款]
    G -->|否| E
    H --> I[退款完成]
    I --> J[通知客户]""",
    
    # ============================================================================
    # 技术架构类模板
    # ============================================================================
    
    "system-deployment": """graph TD
    A[代码提交] --> B[持续集成]
    B --> C[自动化测试]
    C --> D{测试通过?}
    D -->|是| E[构建镜像]
    D -->|否| F[修复问题]
    F --> A
    E --> G[部署到测试环境]
    G --> H[集成测试]
    H --> I{测试通过?}
    I -->|是| J[部署到生产环境]
    I -->|否| K[回滚]
    K --> F
    J --> L[监控和告警]""",
    
    "data-pipeline": """graph LR
    A[数据源1] --> F[数据采集]
    B[数据源2] --> F
    C[数据源3] --> F
    F --> G[数据清洗]
    G --> H[数据转换]
    H --> I[数据加载]
    I --> J[数据仓库]
    J --> K[数据分析]
    K --> L[数据可视化]""",
    
    "api-gateway": """graph TD
    A[客户端请求] --> B[API网关]
    B --> C{请求验证}
    C -->|有效| D[路由到微服务]
    C -->|无效| E[返回错误]
    D --> F[微服务1]
    D --> G[微服务2]
    D --> H[微服务3]
    F --> I[聚合响应]
    G --> I
    H --> I
    I --> J[返回客户端]""",
    
    "backup-recovery": """graph TD
    A[开始备份] --> B[检查存储空间]
    B --> C{空间充足?}
    C -->|是| D[执行数据备份]
    C -->|否| E[清理旧备份]
    E --> D
    D --> F[验证备份完整性]
    F --> G{验证通过?}
    G -->|是| H[备份完成]
    G -->|否| I[重新备份]
    I --> D
    subgraph 恢复流程
        J[数据丢失] --> K[选择恢复点]
        K --> L[执行恢复]
        L --> M[验证恢复数据]
        M --> N[恢复完成]
    end""",
    
    # ============================================================================
    # 项目管理类模板
    # ============================================================================
    
    "project-approval": """graph TD
    A[项目提案] --> B[部门评审]
    B --> C{评审通过?}
    C -->|是| D[预算审批]
    C -->|否| E[提案驳回]
    D --> F{预算批准?}
    F -->|是| G[项目立项]
    F -->|否| H[预算调整]
    H --> D
    G --> I[组建项目团队]
    I --> J[项目启动]""",
    
    "task-workflow": """graph TD
    A[任务创建] --> B[任务分配]
    B --> C[开始执行]
    C --> D[进度跟踪]
    D --> E{任务完成?}
    E -->|是| F[质量检查]
    E -->|否| G[继续执行]
    G --> D
    F --> H{检查通过?}
    H -->|是| I[任务关闭]
    H -->|否| J[返工修改]
    J --> C""",
    
    "release-process": """graph TD
    A[开发完成] --> B[代码审查]
    B --> C{审查通过?}
    C -->|是| D[测试环境部署]
    C -->|否| E[修改代码]
    E --> B
    D --> F[测试验证]
    F --> G{测试通过?}
    G -->|是| H[预生产环境部署]
    G -->|否| I[修复缺陷]
    I --> D
    H --> J[最终验证]
    J --> K{验证通过?}
    K -->|是| L[生产环境发布]
    K -->|否| M[回滚]
    M --> I
    L --> N[发布完成]""",
    
    "risk-management": """graph TD
    A[风险识别] --> B[风险评估]
    B --> C[风险分类]
    C --> D{风险等级}
    D -->|高风险| E[立即处理]
    D -->|中风险| F[制定应对计划]
    D -->|低风险| G[监控观察]
    E --> H[风险缓解]
    F --> I[计划执行]
    G --> J[定期复查]
    H --> K[风险关闭]
    I --> K
    J --> K""",
    
    # ============================================================================
    # 教育培训类模板
    # ============================================================================
    
    "training-process": """graph TD
    A[培训需求分析] --> B[制定培训计划]
    B --> C[设计培训内容]
    C --> D[准备培训材料]
    D --> E[组织培训]
    E --> F[培训实施]
    F --> G[培训评估]
    G --> H{评估结果}
    H -->|良好| I[培训完成]
    H -->|需改进| J[优化培训]
    J --> C""",
    
    "exam-process": """graph TD
    A[考试报名] --> B[资格审核]
    B --> C{审核通过?}
    C -->|是| D[缴纳费用]
    C -->|否| E[报名失败]
    D --> F[准考证发放]
    F --> G[参加考试]
    G --> H[阅卷评分]
    H --> I[成绩公布]
    I --> J{考试通过?}
    J -->|是| K[证书发放]
    J -->|否| L[准备补考]
    L --> A""",
    
    "onboarding-process": """graph TD
    A[录用通知] --> B[入职准备]
    B --> C[办理入职手续]
    C --> D[公司介绍]
    D --> E[部门介绍]
    E --> F[岗位培训]
    F --> G[导师分配]
    G --> H[试用期考核]
    H --> I{考核通过?}
    I -->|是| J[转正]
    I -->|否| K[延长试用期]
    K --> H""",
    
    "performance-review": """graph TD
    A[设定绩效目标] --> B[日常工作]
    B --> C[中期评估]
    C --> D[调整工作方向]
    D --> B
    B --> E[年度评估]
    E --> F[自我评价]
    F --> G[上级评价]
    G --> H[绩效面谈]
    H --> I[制定发展计划]
    I --> A""",
    
    # ============================================================================
    # 其他常用模板
    # ============================================================================
    
    "purchase-process": """graph TD
    A[需求提出] --> B[预算申请]
    B --> C{预算批准?}
    C -->|是| D[供应商选择]
    C -->|否| E[申请驳回]
    D --> F[采购申请]
    F --> G[采购审批]
    G --> H{审批通过?}
    H -->|是| I[合同签订]
    H -->|否| J[重新申请]
    J --> F
    I --> K[付款]
    K --> L[货物验收]
    L --> M[入库登记]""",
    
    "incident-response": """graph TD
    A[事件发现] --> B[初步评估]
    B --> C{事件严重程度}
    C -->|严重| D[升级处理]
    C -->|一般| E[常规处理]
    D --> F[成立应急小组]
    E --> G[指派处理人]
    F --> H[制定解决方案]
    G --> H
    H --> I[执行解决方案]
    I --> J[验证解决效果]
    J --> K{问题解决?}
    K -->|是| L[事件关闭]
    K -->|否| M[重新处理]
    M --> H
    L --> N[编写事件报告]""",
    
    "recruitment-process": """graph TD
    A[职位发布] --> B[简历筛选]
    B --> C[初试面试]
    C --> D{初试通过?}
    D -->|是| E[复试面试]
    D -->|否| F[简历库储备]
    E --> G{复试通过?}
    G -->|是| H[薪资谈判]
    G -->|否| F
    H --> I{达成一致?}
    I -->|是| J[发放录用通知]
    I -->|否| K[谈判终止]
    J --> L[背景调查]
    L --> M{调查通过?}
    M -->|是| N[办理入职]
    M -->|否| O[取消录用]""",
    
    "change-request": """graph TD
    A[变更申请] --> B[影响分析]
    B --> C[风险评估]
    C --> D[变更审批]
    D --> E{审批通过?}
    E -->|是| F[制定实施计划]
    E -->|否| G[变更拒绝]
    F --> H[测试验证]
    H --> I{测试通过?}
    I -->|是| J[实施变更]
    I -->|否| K[调整计划]
    K --> F
    J --> L[验证变更效果]
    L --> M{变更成功?}
    M -->|是| N[变更完成]
    M -->|否| O[回滚变更]
    O --> P[分析失败原因]""",
    
    # ============================================================================
    # 更多Mermaid图表类型模板
    # ============================================================================
    
    "gantt-project": """gantt
    title 软件开发项目计划
    dateFormat YYYY-MM-DD
    
    section 需求阶段
    需求收集 : 2024-01-01, 10d
    需求分析 : 2024-01-11, 7d
    需求评审 : 2024-01-18, 3d
    
    section 开发阶段
    架构设计 : 2024-01-22, 7d
    前端开发 : 2024-01-29, 15d
    后端开发 : 2024-01-29, 20d
    数据库设计 : 2024-02-05, 10d
    
    section 测试部署
    单元测试 : 2024-02-19, 7d
    集成测试 : 2024-02-26, 10d
    用户验收测试 : 2024-03-07, 7d
    上线部署 : 2024-03-14, 5d""",
    
    "class-diagram": """classDiagram
    class Vehicle {
        +String make
        +String model
        +int year
        +start()
        +stop()
    }
    
    class Car {
        +int doors
        +openTrunk()
    }
    
    class Motorcycle {
        +boolean hasSidecar
        +wheelie()
    }
    
    class Truck {
        +float loadCapacity
        +loadCargo()
    }
    
    Vehicle <|-- Car
    Vehicle <|-- Motorcycle
    Vehicle <|-- Truck
    
    class Customer {
        +String name
        +String email
        +placeOrder()
    }
    
    class Order {
        +int orderId
        +Date orderDate
        +float total
        +addItem()
        +calculateTotal()
    }
    
    class Product {
        +String name
        +float price
        +int stock
        +updateStock()
    }
    
    Customer "1" --> "*" Order : 创建
    Order "*" --> "1" Product : 包含""",
    
    "state-diagram": """stateDiagram-v2
    [*] --> Idle
    
    Idle --> Active : start
    Active --> Paused : pause
    Paused --> Active : resume
    Active --> Completed : finish
    Paused --> Completed : finish
    Completed --> [*]
    
    state Active {
        [*] --> Processing
        Processing --> Validating : process
        Validating --> [*] : valid
        Validating --> Processing : invalid
    }
    
    state Paused {
        [*] --> Suspended
        Suspended --> Waiting
        Waiting --> Suspended : timeout
    }""",
    
    "pie-chart": """pie title 编程语言市场份额
    "Python" : 30
    "JavaScript" : 25
    "Java" : 20
    "C++" : 10
    "其他" : 15""",
    
    "journey-diagram": """journey
    title 用户在线购物旅程
    
    section 浏览阶段
      浏览商品: 5: 用户
      搜索商品: 4: 用户
      筛选结果: 3: 用户
    
    section 决策阶段
      查看详情: 5: 用户
      比较价格: 4: 用户
      阅读评价: 5: 用户
    
    section 购买阶段
      加入购物车: 5: 用户
      结算支付: 5: 用户
      确认订单: 4: 用户
    
    section 售后阶段
      等待收货: 3: 用户
      确认收货: 4: 用户
      评价商品: 2: 用户""",
    
    "timeline-diagram": """timeline
    title 互联网发展历程
    
    1990s : 万维网诞生
           : HTML标准发布
           : 浏览器普及
    
    2000s : Web 2.0兴起
           : 社交网络出现
           : 移动互联网开始
    
    2010s : 智能手机普及
           : 云计算成熟
           : 人工智能兴起
    
    2020s : 5G商用
           : 元宇宙概念
           : AI大模型爆发""",
    
    "sequence-diagram": """sequenceDiagram
    participant 用户
    participant 前端
    participant API网关
    participant 认证服务
    participant 用户服务
    participant 数据库
    
    用户->>前端: 访问登录页面
    前端->>API网关: 登录请求
    API网关->>认证服务: 验证请求格式
    认证服务->>数据库: 查询用户信息
    数据库-->>认证服务: 返回用户数据
    认证服务-->>API网关: 验证结果
    API网关->>用户服务: 获取用户详情
    用户服务-->>API网关: 返回用户信息
    API网关-->>前端: 登录响应
    前端-->>用户: 显示登录结果"""
}

# ============================================================================
# DeepSeek API调用函数
# ============================================================================

def call_llm_api(prompt: str, system_prompt: str = None, verbose: bool = False) -> str:
    """
    调用LLM API生成响应（支持DeepSeek和OpenAI）
    
    Args:
        prompt: 用户提示
        system_prompt: 系统提示词（可选）
        verbose: 是否显示详细输出
    
    Returns:
        API响应文本，失败时返回空字符串
    """
    if not LLM_CONFIG["api_key"]:
        if verbose:
            print(f"[WARN] {LLM_CONFIG['provider']} API密钥未配置，无法调用API")
        return ""
    
    import requests
    import json
    
    provider = LLM_CONFIG["provider"]
    api_key = LLM_CONFIG["api_key"]
    base_url = LLM_CONFIG["base_url"]
    model = LLM_CONFIG["model"]
    timeout = LLM_CONFIG["timeout"]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # OpenAI需要特定的组织头（可选）
    if provider == "openai":
        org_id = os.environ.get("OPENAI_ORG_ID")
        if org_id:
            headers["OpenAI-Organization"] = org_id
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.1,  # 低温度以获得更确定性的输出
        "stream": False
    }
    
    try:
        if verbose:
            print(f"[INFO] 调用{provider} API: {model}")
            print(f"[DEBUG] 请求URL: {base_url}/chat/completions")
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=timeout
        )
        
        if verbose:
            print(f"[DEBUG] 响应状态码: {response.status_code}")
        
        if response.status_code != 200:
            if verbose:
                print(f"[ERROR] {provider} API调用失败: {response.status_code} - {response.text}")
            return ""
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        if verbose:
            print(f"[INFO] {provider} API调用成功，响应长度: {len(content)} 字符")
        
        return content.strip()
    
    except requests.exceptions.Timeout:
        if verbose:
            print(f"[ERROR] {provider} API调用超时")
        return ""
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"[ERROR] {provider} API请求异常: {e}")
        return ""
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        if verbose:
            print(f"[ERROR] 解析{provider} API响应失败: {e}")
            if 'result' in locals():
                print(f"[DEBUG] 原始响应: {result}")
        return ""

def generate_mermaid_with_llm(prompt: str, verbose: bool = False) -> str:
    """
    使用LLM API将自然语言描述转换为Mermaid代码（支持DeepSeek/OpenAI）
    
    Args:
        prompt: 自然语言描述
        verbose: 是否显示详细输出
    
    Returns:
        Mermaid代码，失败时返回空字符串
    """
    if not CONFIG_LOADED:
        if verbose:
            print(f"[WARN] {LLM_CONFIG['provider']} API配置未加载，无法使用API")
        return ""
    
    # 系统提示词 - 指导模型生成Mermaid代码（支持多种图表类型）
    system_prompt = """你是一个Mermaid图表专家，负责将用户的需求描述转换为准确、简洁的Mermaid代码。

要求：
1. 只返回Mermaid代码，不要任何额外的解释、说明或注释
2. 根据描述内容自动选择合适的Mermaid图表类型：
   
   a) 流程/步骤/顺序 → 流程图 (graph TD / flowchart TD)
     - 语法: graph TD 或 flowchart TD
     - 用途: 业务流程、工作流程、算法流程
     - 示例: A[开始] --> B[步骤1] --> C[结束]
   
   b) 时间/进度/计划 → 甘特图 (gantt)
     - 语法: gantt
     - 用途: 项目时间规划、进度跟踪、时间线
     - 示例: title 项目计划\nsection 阶段1\n任务1: 2024-01-01, 30d
   
   c) 系统/组件/类 → 类图 (classDiagram)
     - 语法: classDiagram
     - 用途: 面向对象设计、系统架构、类关系
     - 示例: class Animal {\n+String name\n+eat()\n}
   
   d) 状态/状态机 → 状态图 (stateDiagram-v2)
     - 语法: stateDiagram-v2
     - 用途: 状态机表示、状态转换、有限状态机
     - 示例: [*] --> State1\nState1 --> State2 : 事件
   
   e) 序列/交互 → 序列图 (sequenceDiagram)
     - 语法: sequenceDiagram
     - 用途: 系统交互、消息序列、API调用
     - 示例: A->>B: 请求\nB-->>A: 响应
   
   f) 数据/比例 → 饼图 (pie)
     - 语法: pie
     - 用途: 数据比例、百分比分布、统计图表
     - 示例: title 市场份额\n"产品A": 40\n"产品B": 30
   
   g) 旅程/体验 → 用户旅程图 (journey)
     - 语法: journey
     - 用途: 用户体验、用户旅程、服务蓝图
     - 示例: title 用户购物旅程\nsection 浏览\n点击商品: 5: 用户
   
   h) 时间/历史 → 时间线图 (timeline)
     - 语法: timeline
     - 用途: 历史事件、项目里程碑、发展历程
     - 示例: timeline\n2024-01: 项目启动\n2024-06: 版本发布
   
   i) 其他类型: 思维导图 (mindmap)、象限图 (quadrantChart)、需求图 (requirementDiagram)、Git图 (gitGraph)等

3. 使用中文标签（如果描述是中文）
4. 保持代码简洁但完整
5. 对于复杂图表，适当使用子图和样式

示例：
用户：用户登录流程
输出：```mermaid
graph TD
    A[用户访问网站] --> B{已登录?}
    B -->|否| C[显示登录表单]
    B -->|是| D[跳转到首页]
    C --> E[输入用户名密码]
    E --> F{验证成功?}
    F -->|是| D
    F -->|否| G[显示错误信息]
    G --> C
```

用户：项目开发时间计划
输出：```mermaid
gantt
    title 项目开发计划
    dateFormat YYYY-MM-DD
    
    section 需求分析
    需求收集 : 2024-01-01, 10d
    需求评审 : 2024-01-11, 5d
    
    section 开发阶段
    前端开发 : 2024-01-16, 20d
    后端开发 : 2024-01-16, 25d
    
    section 测试部署
    系统测试 : 2024-02-10, 15d
    上线部署 : 2024-02-25, 5d
```

用户：电商系统类图设计
输出：```mermaid
classDiagram
    class User {
        +String username
        +String email
        +login()
        +logout()
    }
    
    class Product {
        +String name
        +Float price
        +getDetails()
    }
    
    class Order {
        +Date orderDate
        +Float total
        +placeOrder()
        +cancelOrder()
    }
    
    User "1" --> "*" Order : 创建
    Order "*" --> "1" Product : 包含
```

现在，请根据以下用户描述生成Mermaid代码："""
    
    full_prompt = f"{prompt}\n\n请生成对应的Mermaid流程图代码。"
    
    response = call_llm_api(full_prompt, system_prompt, verbose)
    
    if not response:
        return ""
    
    # 清理响应，提取Mermaid代码
    # 移除可能存在的代码块标记
    import re
    
    # 查找 ```mermaid ... ``` 代码块
    mermaid_pattern = r'```(?:mermaid)?\s*(.*?)\s*```'
    matches = re.findall(mermaid_pattern, response, re.DOTALL)
    
    if matches:
        # 使用第一个匹配的代码块
        mermaid_code = matches[0].strip()
    else:
        # 如果没有代码块，假设整个响应就是Mermaid代码
        mermaid_code = response.strip()
    
    # 验证基本的Mermaid语法
    if not mermaid_code.startswith(('graph', 'sequenceDiagram', 'flowchart', 'gantt', 
                                   'classDiagram', 'stateDiagram', 'pie', 'gitGraph',
                                   'journey', 'requirementDiagram', 'quadrantChart',
                                   'timeline', 'mindmap', 'xyChart', 'blockDiagram')):
        if verbose:
            print(f"[WARN] 生成的代码可能不是有效的Mermaid语法")
            print(f"[DEBUG] 响应内容: {response[:200]}...")
        
        # 如果不是有效的Mermaid，尝试包装成流程图
        mermaid_code = f"graph TD\n    Start[{prompt[:30]}...] --> End[结束]"
    
    return mermaid_code

# ============================================================================
# AI转换函数（基础版）
# ============================================================================

def ai_to_mermaid(prompt: str, verbose: bool = False, use_llm: bool = True) -> str:
    """
    将自然语言描述转换为Mermaid代码
    
    策略：
    1. 首先尝试使用DeepSeek API（如果配置可用且use_llm=True）
    2. 如果API失败，回退到模板匹配
    3. 最后使用通用流程图生成
    
    Args:
        prompt: 自然语言描述
        verbose: 是否显示详细输出
        use_llm: 是否尝试使用LLM API
    
    Returns:
        Mermaid代码
    """
    prompt_lower = prompt.lower()
    
    # 步骤1：尝试使用DeepSeek API（如果启用且配置可用）
    if use_llm and CONFIG_LOADED:
        if verbose:
            print(f"[INFO] 尝试使用{LLM_CONFIG['provider']} API生成Mermaid代码...")
        
        mermaid_code = generate_mermaid_with_llm(prompt, verbose)
        
        if mermaid_code:
            if verbose:
                print(f"[INFO] {LLM_CONFIG['provider']} API生成成功")
            return mermaid_code
        else:
            if verbose:
                print("[WARN] DeepSeek API生成失败，回退到模板匹配")
    
    # 步骤2：模板匹配（如果API失败或未启用）
    if verbose:
        print("[INFO] 使用模板匹配生成Mermaid代码")
    
    # 模板关键词映射（关键词列表 -> 模板名称）
    template_keywords = {
        "login": ["登录", "auth", "认证", "登陆", "signin"],
        "api-call": ["api", "接口", "调用", "请求", "响应", "rest"],
        "shopping": ["购物", "电商", "结算", "购买", "商城"],  # 移除"订单"，避免与order-processing冲突
        "decision": ["决策", "判断", "分支", "条件", "选择"],
        "order-processing": ["订单处理", "订单流程", "订单", "order", "下单", "发货"],  # 添加"订单"关键词
        "customer-service": ["客服", "客户服务", "售后", "支持", "咨询"],
        "inventory-management": ["库存", "库存管理", "仓储", "入库", "出库"],
        "refund-process": ["退款", "退货", "refund", "return", "售后"],
        "system-deployment": ["系统部署", "部署", "发布", "上线", "运维"],
        "data-pipeline": ["数据管道", "数据流程", "etl", "数据处理", "数据流"],
        "api-gateway": ["api网关", "网关", "路由", "api gateway"],
        "backup-recovery": ["备份", "恢复", "数据备份", "灾难恢复"],
        "project-approval": ["项目审批", "立项", "项目申请", "审批流程"],
        "task-workflow": ["任务", "工作流", "任务流程", "工作流程"],
        "release-process": ["发布流程", "版本发布", "上线流程", "发版"],
        "risk-management": ["风险管理", "风险", "风险评估", "风险控制"],
        "training-process": ["培训", "培训流程", "学习", "教育"],
        "exam-process": ["考试", "考试流程", "测试", "考核", "测验"],
        "onboarding-process": ["入职", "入职流程", "新员工", "onboarding"],
        "performance-review": ["绩效", "绩效考核", "绩效评估", "绩效 review"],
        "purchase-process": ["采购", "采购流程", "购买流程", "采购申请"],
        "incident-response": ["事件", "故障", "事故", "应急", "响应"],
        "recruitment-process": ["招聘", "招聘流程", "recruitment", "招聘面试"],
        "change-request": ["变更", "变更请求", "变更流程", "change request"],
        "gantt-project": ["甘特图", "gantt", "时间计划", "项目计划", "时间线", "进度"],
        "class-diagram": ["类图", "classdiagram", "类设计", "面向对象", "uml", "类关系"],
        "state-diagram": ["状态图", "statediagram", "状态机", "状态转换", "有限状态机"],
        "pie-chart": ["饼图", "pie", "数据比例", "百分比", "统计图", "市场份额"],
        "journey-diagram": ["旅程图", "journey", "用户旅程", "用户体验", "用户路径"],
        "timeline-diagram": ["时间线", "timeline", "历史", "发展历程", "里程碑"],
        "sequence-diagram": ["序列图", "sequencediagram", "交互图", "消息序列", "顺序图"]
    }
    
    # 检查是否匹配已知模板（优化匹配逻辑）
    matched_template = None
    best_match_length = 0
    
    for template_name, keywords in template_keywords.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                # 选择更长的关键词匹配（更具体）
                if len(keyword) > best_match_length:
                    best_match_length = len(keyword)
                    matched_template = template_name
                # 如果长度相同，保持第一个匹配到的
                elif len(keyword) == best_match_length and matched_template is None:
                    matched_template = template_name
    
    if matched_template:
        if verbose:
            print(f"[INFO] 匹配到{matched_template}模板")
        return TEMPLATES[matched_template]
    
    # 步骤3：通用流程图生成（简单版本）
    if verbose:
        print("[INFO] 使用通用流程图模板")
    
    # 简单地将提示转换为节点
    words = prompt.split()
    if len(words) > 8:
        words = words[:8]
    
    nodes = []
    for i, word in enumerate(words):
        if i == 0:
            nodes.append(f"    Start[{word}...] --> Step1[步骤1]")
        elif i == len(words) - 1:
            nodes.append(f"    Step{i}[步骤{i}] --> End[结束]")
        else:
            nodes.append(f"    Step{i}[步骤{i}] --> Step{i+1}[步骤{i+1}]")
    
    # 构建基础流程图
    mermaid_code = "graph TD\n" + "\n".join(nodes)
    
    return mermaid_code

# ============================================================================
# Mermaid渲染
# ============================================================================

def analyze_mermaid_error(error_msg: str, stdout_msg: str, mermaid_code: str, verbose: bool = False) -> str:
    """
    分析Mermaid错误并提供修复建议
    
    Args:
        error_msg: 错误消息
        stdout_msg: 标准输出消息
        mermaid_code: 导致错误的Mermaid代码
        verbose: 详细输出
    
    Returns:
        增强的错误消息
    """
    import re
    
    error_lower = error_msg.lower()
    enhanced_msg = f"Mermaid渲染失败:\n\n原始错误: {error_msg[:200]}..."
    
    # 常见错误类型分析
    if "syntax error" in error_lower or "parsing error" in error_lower:
        enhanced_msg += "\n\n🔍 语法错误检测:\n"
        
        # 尝试提取具体的语法错误位置
        line_match = re.search(r'line (\d+):', error_msg)
        if line_match:
            line_num = int(line_match.group(1))
            lines = mermaid_code.split('\n')
            if 1 <= line_num <= len(lines):
                enhanced_msg += f"   第{line_num}行可能有问题:\n"
                enhanced_msg += f"   \"{lines[line_num-1].strip()}\"\n"
        
        # 常见语法错误建议
        enhanced_msg += "\n💡 语法错误常见原因:\n"
        enhanced_msg += "   1. 缺少分号 (;) 在语句结尾\n"
        enhanced_msg += "   2. 括号不匹配 ({ } [ ] ( ))\n"
        enhanced_msg += "   3. 箭头语法错误 (应使用 --> 或 ->)\n"
        enhanced_msg += "   4. 节点标签未正确闭合 (如 A[标签])\n"
        enhanced_msg += "   5. 特殊字符未转义 (如 #, %, & 等)\n"
        
        enhanced_msg += "\n✅ 修复建议:\n"
        enhanced_msg += "   1. 使用在线Mermaid编辑器检查语法: https://mermaid.live\n"
        enhanced_msg += "   2. 简化图表，分步调试\n"
        enhanced_msg += "   3. 使用 --raw 参数直接调试Mermaid代码\n"
    
    elif "unknown diagram type" in error_lower:
        enhanced_msg += "\n\n🔍 未知图表类型错误:\n"
        enhanced_msg += "   检测到不支持的Mermaid图表类型\n"
        
        # 检查图表类型
        first_line = mermaid_code.split('\n')[0].strip()
        enhanced_msg += f"   第一行: \"{first_line}\"\n"
        
        enhanced_msg += "\n💡 支持的图表类型:\n"
        enhanced_msg += "   graph TD / graph LR - 流程图\n"
        enhanced_msg += "   sequenceDiagram - 序列图\n"
        enhanced_msg += "   gantt - 甘特图\n"
        enhanced_msg += "   classDiagram - 类图\n"
        enhanced_msg += "   stateDiagram-v2 - 状态图\n"
        enhanced_msg += "   pie - 饼图\n"
        enhanced_msg += "   journey - 用户旅程图\n"
        enhanced_msg += "   timeline - 时间线图\n"
        
        enhanced_msg += "\n✅ 修复建议:\n"
        enhanced_msg += "   1. 确保第一行是有效的图表类型声明\n"
        enhanced_msg += "   2. 检查拼写错误\n"
        enhanced_msg += "   3. 更新Mermaid CLI到最新版本\n"
    
    elif "puppeteer" in error_lower or "chrome" in error_lower:
        enhanced_msg += "\n\n🔍 Puppeteer/Chrome相关错误:\n"
        enhanced_msg += "   Mermaid CLI需要Chrome/Puppeteer来渲染图表\n"
        
        enhanced_msg += "\n💡 可能的原因:\n"
        enhanced_msg += "   1. Chrome未安装或版本不兼容\n"
        enhanced_msg += "   2. Puppeteer依赖缺失\n"
        enhanced_msg += "   3. 系统权限问题\n"
        
        enhanced_msg += "\n✅ 修复建议:\n"
        enhanced_msg += "   1. 安装Chrome浏览器\n"
        enhanced_msg += "   2. 重新安装Mermaid CLI:\n"
        enhanced_msg += "      npm uninstall -g @mermaid-js/mermaid-cli\n"
        enhanced_msg += "      npm install -g @mermaid-js/mermaid-cli\n"
        enhanced_msg += "   3. 尝试使用SVG格式: -f svg\n"
    
    elif "command not found" in error_lower or "不是内部或外部命令" in error_msg:
        enhanced_msg += "\n\n🔍 命令未找到错误:\n"
        enhanced_msg += "   Mermaid CLI (mmdc) 未正确安装或不在PATH中\n"
        
        enhanced_msg += "\n✅ 修复建议:\n"
        enhanced_msg += "   1. 确认安装: npm list -g @mermaid-js/mermaid-cli\n"
        enhanced_msg += "   2. 重新安装: npm install -g @mermaid-js/mermaid-cli\n"
        enhanced_msg += "   3. 检查PATH环境变量\n"
        enhanced_msg += "   4. Windows用户可能需要使用 mmdc.cmd\n"
    
    elif "eaccess" in error_lower or "permission denied" in error_lower:
        enhanced_msg += "\n\n🔍 权限错误:\n"
        enhanced_msg += "   文件访问权限不足\n"
        
        enhanced_msg += "\n✅ 修复建议:\n"
        enhanced_msg += "   1. 使用管理员权限运行\n"
        enhanced_msg += "   2. 更改输出目录到用户目录\n"
        enhanced_msg += "   3. 检查文件权限\n"
    
    else:
        enhanced_msg += "\n\n💡 一般性建议:\n"
        enhanced_msg += "   1. 使用 --verbose 查看详细输出\n"
        enhanced_msg += "   2. 简化Mermaid代码进行测试\n"
        enhanced_msg += "   3. 在线验证Mermaid语法: https://mermaid.live\n"
        enhanced_msg += "   4. 检查Mermaid CLI版本: mmdc --version\n"
        enhanced_msg += "   5. 更新到最新版本: npm update -g @mermaid-js/mermaid-cli\n"
    
    # 如果有stdout输出，也包含
    if stdout_msg and verbose:
        enhanced_msg += f"\n📋 标准输出: {stdout_msg[:200]}..."
    
    return enhanced_msg

def generate_with_mermaid(mermaid_code: str, output_path: str, 
                         format: str = "png", theme: str = "default",
                         verbose: bool = False, debug: bool = False) -> tuple[bool, str]:
    """
    使用Mermaid CLI生成图片
    
    Args:
        mermaid_code: Mermaid代码
        output_path: 输出文件路径
        format: 输出格式 (png, svg, pdf)
        theme: 主题
        verbose: 详细输出
    
    Returns:
        (成功标志, 消息)
    """
    # 检查mmdc是否可用
    if not check_mermaid_cli():
        return False, "未找到Mermaid CLI (mmdc)。请安装: npm install -g @mermaid-js/mermaid-cli"
    
    try:
        # 创建临时文件保存Mermaid代码
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', 
                                       delete=False, encoding='utf-8') as f:
            f.write(mermaid_code)
            mmd_file = f.name
        
        if verbose:
            print(f"[DEBUG] 临时文件: {mmd_file}")
            print(f"[DEBUG] 输出路径: {output_path}")
        
        # 构建命令
        if sys.platform == "win32":
            mmdc_cmd = "mmdc.cmd"
        else:
            mmdc_cmd = "mmdc"
        
        cmd = [
            mmdc_cmd,
            "-i", mmd_file,
            "-o", output_path,
            "-t", theme,
            "-b", "white"
        ]
        
        # 添加格式参数
        if format != "png":
            cmd.extend(["-e", f".{format}"])
        
        if verbose:
            print(f"[DEBUG] 执行命令: {' '.join(cmd)}")
        
        # 执行命令
                # 执行命令
        if sys.platform == "win32":
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=True)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # 清理临时文件（debug模式不删除）
        if not debug:
            try:
                os.unlink(mmd_file)
            except:
                pass
        elif verbose:
            print(f"[DEBUG] 临时文件保留（debug模式）: {mmd_file}")
        
        if result.returncode != 0:
            error_msg = result.stderr or "未知错误"
            stdout_msg = result.stdout or ""
            
            # 分析常见错误类型并提供修复建议
            enhanced_error = analyze_mermaid_error(error_msg, stdout_msg, mermaid_code, verbose)
            return False, enhanced_error
        
        # 检查输出文件是否存在
        if not os.path.exists(output_path):
            return False, "输出文件未生成"
        
        return True, f"流程图已生成: {output_path} ({os.path.getsize(output_path)} bytes)"
    
    except subprocess.TimeoutExpired:
        return False, "Mermaid渲染超时（30秒）。这可能是因为:\n  1. Mermaid CLI版本问题\n  2. 图表过于复杂\n  3. 系统资源不足\n建议:\n  1. 升级Mermaid CLI: npm update -g @mermaid-js/mermaid-cli\n  2. 简化图表内容\n  3. 增加超时时间（需要修改代码）"
    except Exception as e:
        return False, f"渲染过程中出错: {str(e)}\n建议:\n  1. 检查临时文件权限\n  2. 确保磁盘空间充足\n  3. 检查Mermaid CLI安装是否正确"

# ============================================================================
# 备选方案：使用Python生成简单图像（当Mermaid不可用时）
# ============================================================================

def generate_simple_image(mermaid_code: str, output_path: str, 
                         verbose: bool = False) -> tuple[bool, str]:
    """
    使用PIL生成简单图像（当Mermaid不可用时）
    
    这是一个备选方案，只生成文本表示的基础图像
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False, "缺少PIL库。请安装: pip install pillow"
    
    try:
        # 创建图像
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 尝试加载字体
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # 添加标题
        title = "流程图（Mermaid代码）"
        draw.text((20, 20), title, fill=(0, 0, 0), font=font)
        
        # 添加Mermaid代码
        y_offset = 60
        for i, line in enumerate(mermaid_code.split('\n')):
            if y_offset < height - 40:
                draw.text((20, y_offset), line, fill=(50, 50, 50), font=font)
                y_offset += 25
            else:
                break
        
        # 添加边框
        draw.rectangle([10, 10, width-10, height-10], outline=(200, 200, 200), width=2)
        
        # 保存图像
        image.save(output_path, "PNG")
        
        if verbose:
            print(f"[INFO] 使用PIL生成基础图像: {output_path}")
        
        return True, f"基础图像已生成（Mermaid不可用）: {output_path}"
    
    except Exception as e:
        return False, f"PIL图像生成失败: {str(e)}"

# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="生成流程图 - 将自然语言描述或Mermaid代码转换为流程图图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "用户登录认证流程" -o login.png
  %(prog)s "API调用序列" -o api.svg -f svg -t dark
  %(prog)s --raw "graph TD; A[开始]-->B[结束]" -o simple.png
  %(prog)s "购物流程" --verbose
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="流程图描述（自然语言）或Mermaid代码（使用--raw时）"
    )
    
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT,
        help=f"输出文件路径 (默认: {DEFAULT_OUTPUT})"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=SUPPORTED_FORMATS,
        default="png",
        help=f"输出格式 (默认: png)"
    )
    
    parser.add_argument(
        "-t", "--theme",
        default="default",
        help=f"主题: {', '.join(SUPPORTED_THEMES)} (默认: default)"
    )
    
    parser.add_argument(
        "--api-key",
        help="手动指定API密钥（优先级最高）"
    )
    
    parser.add_argument(
        "--api-provider",
        choices=["deepseek", "openai"],
        default="deepseek",
        help="API提供商：deepseek 或 openai (默认: deepseek)"
    )
    
    parser.add_argument(
        "--api-base-url",
        help="自定义API基础URL（通常无需指定）"
    )
    
    parser.add_argument(
        "--raw",
        action="store_true",
        help="直接使用输入作为Mermaid代码（跳过AI转换）"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细输出"
    )
    
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="禁用LLM API，强制使用模板匹配"
    )
    
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="列出可用模板"
    )
    
    parser.add_argument(
        "--use-template",
        help="使用预置模板（输入模板名称，如 login, api-call, order-processing 等）"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="调试模式：保存临时文件，显示更详细的信息"
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="显示版本信息并退出"
    )
    
    args = parser.parse_args()
    
    # 处理版本信息
    if args.version:
        print(f"流程图生成器 v{__version__}")
        print(f"发布日期: {__release_date__}")
        print(f"Python脚本: {os.path.basename(__file__)}")
        print(f"功能特性:")
        print(f"  - DeepSeek API智能生成")
        print(f"  - 31个预置模板，覆盖常用场景")
        print(f"  - 8种Mermaid图表类型支持")
        print(f"  - 智能错误处理和故障排除")
        print(f"  - 多格式输出 (PNG/SVG/PDF)")
        print(f"  - 多主题支持")
        return
    
    # ======================================================================
    # 加载LLM API配置（根据优先级：命令行参数 > 环境变量 > OpenClaw配置）
    # ======================================================================
    global CONFIG_LOADED  # 声明全局变量以便修改
    
    # 调用配置加载函数，传入命令行参数
    CONFIG_LOADED = load_llm_config(args)
    
    # 配置向导：如果API配置失败且需要LLM，提供详细指引
    need_llm = not (args.no_llm or args.raw or args.use_template)
    if not CONFIG_LOADED and need_llm:
        print("⚠️  LLM API配置未找到")
        print("=" * 60)
        print("配置指引：以下任一方式配置API密钥")
        print("=" * 60)
        print("1. 命令行参数（优先级最高）：")
        print("   --api-key sk-xxx --api-provider deepseek")
        print("2. 环境变量（推荐）：")
        print("   export DEEPSEEK_API_KEY=sk-xxx  # Linux/macOS")
        print("   set DEEPSEEK_API_KEY=sk-xxx     # Windows")
        print("3. OpenClaw配置文件（自动读取）：")
        print("   ~/.openclaw/openclaw.json 中的 DeepSeek 配置")
        print("4. 使用模板或跳过API（无配置）：")
        print("   --no-llm              # 禁用LLM，使用模板匹配")
        print("   --use-template <name> # 使用预置模板")
        print("   --raw                 # 直接输入Mermaid代码")
        print("=" * 60)
        print("\n是否继续使用模板匹配？（选择N将退出）")
        response = input("继续使用 --no-llm 模式？(Y/n): ").strip().lower()
        if response in ("", "y", "yes"):
            args.no_llm = True
            print("[INFO] 已启用 --no-llm 模式，使用模板匹配")
        else:
            print("操作已取消")
            sys.exit(1)
    
    # 检查是否缺少必要的参数
    # 需要prompt的情况：没有使用--list-templates、--use-template、--version等不需要prompt的操作
    if args.prompt is None and not (args.list_templates or args.use_template):
        parser.print_help()
        print("\n错误: 缺少必要的描述参数。")
        print("请提供流程图描述，或使用 --list-templates、--use-template 等选项。")
        sys.exit(1)
    
    # 显示配置状态（详细模式）
    if args.verbose:
        # 显示LLM API配置状态
        load_llm_config_verbose()
        
        # 显示环境依赖状态
        deps_ok, missing_deps = check_environment_dependencies(verbose=True)
        if deps_ok:
            print("[INFO] 环境依赖检查通过")
        else:
            print(f"[WARN] 环境依赖检查失败，缺少: {', '.join(missing_deps)}")
    
    # 检查环境依赖（非列表模板时）
    if not args.list_templates:
        deps_ok, missing_deps = check_environment_dependencies(verbose=args.verbose)
        if not deps_ok:
            print_dependency_help(missing_deps)
            print(f"\n💡 虽然缺少依赖，但可以尝试继续运行（部分功能可能受限）")
            response = input("是否继续？(y/N): ").strip().lower()
            if response != 'y':
                print("操作已取消")
                return
    
    # 列出模板
    if args.list_templates:
        print("可用模板:")
        for name, code in TEMPLATES.items():
            print(f"\n--- {name} ---")
            print(code[:200] + "..." if len(code) > 200 else code)
        return
    
    # 使用模板
    if args.use_template:
        if args.use_template in TEMPLATES:
            mermaid_code = TEMPLATES[args.use_template]
            if args.verbose:
                print(f"[INFO] 使用模板: {args.use_template}")
        else:
            print(f"错误: 未知模板 '{args.use_template}'")
            print(f"可用模板: {', '.join(TEMPLATES.keys())}")
            return
    elif args.raw:
        # 直接使用输入作为Mermaid代码
        mermaid_code = args.prompt
        if args.verbose:
            print("[INFO] 直接使用输入的Mermaid代码")
    else:
        # AI转换
        if args.verbose:
            print(f"[INFO] 将自然语言转换为Mermaid代码: {args.prompt}")
            if args.no_llm:
                print("[INFO] LLM API已禁用，使用模板匹配")
            elif CONFIG_LOADED:
                print("[INFO] 尝试使用DeepSeek API生成Mermaid代码")
            else:
                print("[INFO] DeepSeek配置未加载，使用模板匹配")
        
        use_llm = not args.no_llm
        mermaid_code = ai_to_mermaid(args.prompt, args.verbose, use_llm)
    
    # 显示生成的代码
    print("\n" + "="*60)
    print("生成的Mermaid代码:")
    print("="*60)
    print("```mermaid")
    print(mermaid_code)
    print("```")
    print("="*60 + "\n")
    
    # 确定输出文件扩展名
    output_path = args.output
    if not any(output_path.lower().endswith(f".{fmt}") for fmt in SUPPORTED_FORMATS):
        output_path = f"{output_path}.{args.format}"
    
    # 使用Mermaid CLI生成图像
    if args.verbose:
        print(f"[INFO] 使用Mermaid CLI生成图像: {output_path}")
    
    success, message = generate_with_mermaid(
        mermaid_code, 
        output_path,
        args.format,
        args.theme,
        args.verbose,
        args.debug
    )
    
    # 如果Mermaid失败，尝试使用PIL生成基础图像
    if not success and args.format == "png":
        if args.verbose:
            print(f"[WARN] Mermaid渲染失败: {message}")
            print("[INFO] 尝试使用PIL生成基础图像...")
        
        success, message = generate_simple_image(mermaid_code, output_path, args.verbose)
    
    # 输出结果
    if success:
        print(f"[SUCCESS] {message}")
        
        # 显示文件信息
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"   文件: {os.path.abspath(output_path)}")
            print(f"   大小: {size:,} bytes")
            
            # 如果是图片，显示尺寸（如果可获取）
            if output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    from PIL import Image
                    with Image.open(output_path) as img:
                        print(f"   尺寸: {img.width} x {img.height}")
                except:
                    pass
    else:
        print(f"[ERROR] {message}")
        
        # 提供详细的故障排除指南
        print("\n" + "="*60)
        print("📚 故障排除指南")
        print("="*60)
        
        # 根据错误类型提供具体建议
        error_msg_lower = message.lower()
        
        if "mermaid cli" in error_msg_lower or "mmdc" in error_msg_lower:
            print("\n🔧 Mermaid CLI 问题:")
            print("   1. 确认Node.js已安装: node --version")
            print("   2. 安装Mermaid CLI: npm install -g @mermaid-js/mermaid-cli")
            print("   3. 验证安装: mmdc --version")
            print("   4. Windows用户注意: 使用 mmdc.cmd 或确保PATH正确")
            
        if "syntax" in error_msg_lower:
            print("\n🔧 语法错误:")
            print("   1. 在线检查语法: https://mermaid.live")
            print("   2. 简化图表测试:")
            print("      python scripts/generate.py --raw \"graph TD; A[开始]-->B[结束]\" -o test.png")
            print("   3. 常见语法问题:")
            print("      - 确保箭头使用 --> 或 ->")
            print("      - 节点标签用方括号: A[标签]")
            print("      - 判断节点用花括号: B{条件}")
            
        if "puppeteer" in error_msg_lower or "chrome" in error_msg_lower:
            print("\n🔧 Chrome/Puppeteer 问题:")
            print("   1. 安装Chrome浏览器")
            print("   2. 重新安装Mermaid CLI:")
            print("      npm uninstall -g @mermaid-js/mermaid-cli")
            print("      npm install -g @mermaid-js/mermaid-cli")
            print("   3. 尝试SVG格式: -f svg")
            
        print("\n💡 调试技巧:")
        print("   1. 使用 --verbose 查看详细输出")
        print("   2. 使用 --no-llm 禁用AI生成，测试模板")
        print("   3. 使用 --raw 直接输入Mermaid代码测试")
        print("   4. 使用 --use-template 测试特定模板")
        
        print("\n🔍 快速测试命令:")
        print("   # 测试Mermaid CLI是否工作")
        print("   mmdc --version")
        print("   # 测试简单图表")
        print("   python scripts/generate.py --raw \"graph TD; A[开始]-->B[结束]\" -o test.png --verbose")
        print("   # 测试模板功能")
        print("   python scripts/generate.py \"用户登录\" --no-llm -o test.png")
        
        print("\n🌐 在线资源:")
        print("   - Mermaid官方文档: https://mermaid.js.org")
        print("   - 在线编辑器: https://mermaid.live")
        print("   - 语法参考: https://mermaid.js.org/syntax/flowchart.html")
        
        print("\n" + "="*60)
        print("如果问题持续，请将以上信息反馈给开发者。")
        
        sys.exit(1)

if __name__ == "__main__":
    main()