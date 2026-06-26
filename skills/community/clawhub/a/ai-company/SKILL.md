---
name: ai-company
description: 完全自主的AI公司运营系统 - 7×24小时自动化发现需求、设计、开发、销售、运维，实现盈利的轻量级解决方案
---

# AI Company 自动化运营技能

## 概述

> **重要说明**：这是一个**技能定义**，不是完整的项目实现。使用本技能来创建和运行您的AI公司。

这个技能教你如何构建一个**完全由AI员工组成的公司**，实现：

- **自主发现需求**：扫描GitHub、Reddit、Twitter等平台发现机会
- **智能设计开发**：AI产品设计师和开发者团队协作
- **自动化销售**：AI销售和营销自动获取客户
- **持续交付支持**：AI客服和DevOps自动运维
- **数据驱动优化**：基于反馈持续迭代产品和流程
- **版本化管理**：所有AI员工可版本控制和快速回滚

## 核心特点

### 1. 去中心化AI员工网络
每个AI员工都是独立的智能体，通过事件总线协作，无单点故障：

```
机会发现层 → 产品设计层 → 开发交付层 → 商业运营层 → 监控优化层
```

### 2. 持续优化循环
系统不断学习和改进：

```
发现机会 → 开发产品 → 获取客户 → 收集反馈 → 分析学习 → 产品迭代 → 重复
```

### 3. 轻量级技术栈
只需Python + JSON文件，无需复杂的基础设施：

```
- Python 3.10+
- Claude Agent SDK
- 简单的JSON文件存储
- cron定时任务
- 可选GitHub Actions
```

### 4. 人类监督保障
AI监控AI，异常时自动告警人类：

```
自我监控 → 同伴监控 → 人类监控面板 → 介入决策
```

## AI员工角色

### Market Research AI（市场研究专家）
**职责**：
- 扫描GitHub Issues发现技术痛点
- 分析Reddit和Hacker News讨论
- 监控Twitter技术趋势
- 追踪竞品动向
- 评估市场机会和收入潜力

**输出**：`opportunities.json` - 包含市场机会、痛点分析、潜在收入

### Product Designer AI（产品设计师）
**职责**：
- 将机会转化为产品概念
- 设计MVP功能集
- 制定定价策略
- 创建产品路线图

**输出**：`product_designs.json` - 产品设计文档、功能列表、定价模型

### Developer AI（开发专家）
**职责**：
- 实现产品功能
- 编写技术文档
- 创建自动化测试
- 修复bug和性能优化
- 管理代码仓库

**输出**：GitHub仓库、文档、测试套件

### Sales & Marketing AI（销售营销专家）
**职责**：
- 生成营销内容
- 管理社交媒体账号
- 回复客户咨询
- 跟进销售线索
- 维护客户关系

**输出**：营销活动、销售记录、客户数据库

### Customer Support AI（客服专家）
**职责**：
- 回答客户问题
- 解决技术问题
- 收集产品反馈
- 识别常见问题并改进FAQ

**输出**：支持工单、客户反馈、知识库更新

### Monitor AI（监控优化专家）
**职责**：
- 监控所有AI员工状态
- 检测性能异常
- 生成优化建议
- 触发人类告警

**输出**：健康报告、告警、优化建议

### Finance AI（财务专家）
**职责**：
- 追踪收入和支出
- 计算利润率
- 生成财务报告
- 建议定价调整

**输出**：财务报告、收入分析、趋势预测

## 技能结构 vs 项目结构

### 技能文件结构（当前）
```
ai-company/                 # 技能定义目录
├── SKILL.md                # 技能主文档
├── README.md               # 项目说明
├── LICENSE                 # 许可证
├── CONTRIBUTING.md         # 贡献指南
├── docs/                   # 详细文档
│   ├── design.md          # 设计文档
│   └── api.md             # API文档
└── examples/              # 示例代码
    ├── simple_ai_employee.py
    ├── simple_event_bus.py
    ├── simple_coordinator.py
    └── config.yaml
```

### 使用本技能创建的项目结构
```
my-ai-company/              # 使用技能创建的项目
├── employees/              # AI员工实现
│   ├── market_researcher.py
│   ├── product_designer.py
│   ├── developer.py
│   ├── sales_marketing.py
│   ├── customer_support.py
│   ├── monitor.py
│   └── finance.py
├── prompts/                # AI员工提示词（版本化）
│   ├── market_researcher/
│   │   ├── v1.0.md
│   │   └── v1.1.md
│   ├── sales_marketing/
│   │   ├── v1.0.md
│   │   ├── v2.0.md
│   │   └── v2.1.md
│   └── versions.json
├── shared/                 # 共享数据
│   ├── opportunities.json
│   ├── products.json
│   ├── customers.json
│   ├── sales.json
│   ├── state.json
│   └── metrics.json
├── workflows/              # 工作流定义
│   ├── discover_opportunities.yaml
│   ├── build_product.yaml
│   ├── make_sale.yaml
│   └── optimize_system.yaml
├── logs/                   # 日志文件
├── main.py                 # 主调度器
└── config.yaml             # 配置文件
```

## 快速开始

### 1. 安装依赖
```bash
pip install anthropic python-dotenv pyyaml requests
```

### 2. 创建AI公司项目
```bash
# 方法1：使用初始化脚本（推荐）
cd skills/ai-company/examples
python3 init_ai_company.py my-ai-company

# 方法2：手动创建
mkdir my-ai-company
cd my-ai-company
# 按照项目结构手动创建目录和文件
```

### 3. 配置API密钥
```bash
cd my-ai-company
cp .env.example .env
# 编辑.env，添加你的API密钥
nano .env
```

### 4. 运行示例测试
```bash
# 测试AI员工示例
python3 ../examples/simple_ai_employee.py

# 测试完整工作流示例
python3 ../examples/simple_coordinator.py
```

### 5. 启动你的AI公司
```bash
# 启动AI团队
python main.py start

# 查看状态
python main.py status

# 停止AI团队
python main.py stop
```

### 5. 设置定时任务
```bash
crontab -e
# 添加：
*/30 * * * * cd /path/to/my-ai-company && python main.py --task discover_opportunities
0 9 * * * cd /path/to/my-ai-company && python main.py --task daily_optimization
*/15 * * * * cd /path/to/my-ai-company && python main.py --task health_check
```

## 配置文件

### config.yaml
```yaml
company:
  name: "My AI Company"
  industry: "software_development"
  target_market: "individuals_small_business"

ai_employees:
  - name: market_researcher
    enabled: true
    version: "v1.1"
  - name: product_designer
    enabled: true
    version: "v1.0"
  - name: developer
    enabled: true
    version: "v1.0"
  - name: sales_marketing
    enabled: true
    version: "v2.1"
  - name: customer_support
    enabled: true
    version: "v1.0"
  - name: monitor
    enabled: true
    version: "v1.0"
  - name: finance
    enabled: true
    version: "v1.0"

apis:
  anthropic_api_key: "${ANTHROPIC_API_KEY}"
  github_token: "${GITHUB_TOKEN}"

schedule:
  opportunity_discovery: "*/30 * * * *"
  daily_optimization: "0 9 * * *"
  health_check: "*/15 * * * *"

monitoring:
  alert_email: "your-email@example.com"
  alert_threshold:
    error_rate: 0.1
    revenue_drop: 0.2
```

## 工作流程

### 1. 机会发现流程
```yaml
触发条件：每30分钟
流程：
  1. Market Research AI扫描多个平台
  2. 分析和评分每个机会
  3. 保存高价值机会到opportunities.json
  4. 发布opportunity.discovered事件
```

### 2. 产品开发流程
```yaml
触发条件：新机会发现
流程：
  1. Product Designer AI设计产品
  2. Developer AI实现MVP
  3. QA自动测试
  4. 部署到生产环境
  5. 发布product.ready事件
```

### 3. 销售流程
```yaml
触发条件：产品就绪
流程：
  1. Marketing AI创建营销内容
  2. 多渠道推广（Twitter、Reddit、邮件）
  3. Sales AI回复咨询
  4. 跟进线索
  5. 成交记录
```

### 4. 优化流程
```yaml
触发条件：每天早上9点
流程：
  1. 分析昨天的数据
  2. 识别问题和机会
  3. 优先级排序
  4. 执行改进：
     - 产品迭代
     - 营销优化
     - 定价调整
     - 客户挽回
  5. 学习和记录
```

## 版本控制和A/B测试

### AI员工版本管理
```bash
# 创建新版本
python main.py --new-version sales_agent v2.2

# A/B测试
python main.py --ab-test sales_agent v2.1 v2.2 --traffic 0.2

# 查看测试结果
python main.py --ab-test-results

# 回滚
python main.py --rollback sales_agent
```

### 提示词版本化
所有AI员工的提示词都纳入版本控制：

```bash
prompts/sales_marketing/
├── v1.0.md     # 初始版本
├── v2.0.md     # 重大更新
└── v2.1.md     # 当前版本
```

## 监控和告警

### 实时监控
```bash
# 查看所有AI员工状态
python main.py --status

# 查看特定AI的日志
tail -f logs/market_researcher.log

# 启动Web仪表板
python main.py --dashboard
# 访问 http://localhost:5000
```

### 告警级别
- **INFO**: 正常运行
- **WARNING**: 性能下降，需关注
- **ERROR**: 任务失败，自动重试中
- **CRITICAL**: 需要人类介入

### 告警触发条件
- 同一AI连续失败3次
- 收入下降超过20%
- 客户投诉率上升
- 系统资源使用超过90%
- AI检测到无法处理的异常

## 数据存储

### JSON数据结构

#### opportunities.json
```json
{
  "opportunities": [
    {
      "id": "opp_001",
      "source": "reddit/r/webdev",
      "pain_point": "缺少自动化测试工具",
      "potential_revenue": 500,
      "difficulty": "medium",
      "market_size": "large",
      "status": "validated"
    }
  ]
}
```

#### products.json
```json
{
  "products": [
    {
      "id": "prod_001",
      "name": "AutoTest Pro",
      "version": "2.3.0",
      "status": "active",
      "pricing": {"starter": 29, "pro": 99},
      "metrics": {
        "daily_sales": 15,
        "refund_rate": 0.02,
        "customer_satisfaction": 4.5
      }
    }
  ]
}
```

#### customers.json
```json
{
  "customers": [
    {
      "id": "cust_001",
      "name": "John Doe",
      "email": "john@example.com",
      "status": "active",
      "lifetime_value": 590,
      "health_score": 0.8
    }
  ]
}
```

## 最佳实践

### 1. 从小开始
- 先启动1-2个AI员工
- 验证工作流程
- 逐步扩展到完整的AI团队

### 2. 人工监督初期
- 前几周密切关注AI决策
- 定期审查AI输出
- 调整提示词和配置

### 3. 数据驱动优化
- 定期查看指标和报告
- 基于数据做决策
- A/B测试重大变更

### 4. 版本控制一切
- 所有提示词纳入Git
- 重大变更前打标签
- 保持快速回滚能力

### 5. 客户体验优先
- 快速响应客户咨询
- 主动收集反馈
- 持续改进产品质量

## 故障排查

### AI员工不工作
```bash
# 检查状态
python main.py --status

# 查看日志
tail -f logs/<employee_name>.log

# 重启AI员工
python main.py --restart <employee_name>
```

### 性能下降
```bash
# 查看优化建议
python main.py --optimizations

# 检查资源使用
python main.py --resources

# 回滚到上一版本
python main.py --rollback <employee_name>
```

### 收入异常
```bash
# 查看财务报告
python main.py --financial-report

# 分析销售数据
python main.py --analyze-sales

# 检查客户健康度
python main.py --customer-health
```

## 高级功能

### 自定义AI员工
```python
# employees/custom_ai.py
from ai_employee import AIEmployee

class CustomAI(AIEmployee):
    name = "custom_ai"
    role = "自定义专家"

    tools = [
        'custom_tool_1',
        'custom_tool_2'
    ]

    def process(self, task):
        # 自定义处理逻辑
        result = self.claude.process(task, self.tools)
        return result
```

### 自定义工作流
```yaml
# workflows/custom_workflow.yaml
name: 自定义工作流
triggers:
  - cron: "0 */2 * * *"
steps:
  - step_1:
      ai: custom_ai
      action: custom_action
  - step_2:
      ai: another_ai
      action: another_action
```

### 集成外部服务
```yaml
# config.yaml
integrations:
  slack:
    webhook_url: "https://hooks.slack.com/..."
  discord:
    bot_token: "your-bot-token"
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
```

## 扩展阅读

- [设计文档](docs/design.md) - 详细的系统设计
- [API文档](docs/api.md) - 完整的API参考
- [示例项目](https://github.com/sendwealth/claw-intelligence) - 实际运行的AI公司
- [社区讨论](https://github.com/sendwealth/claw-intelligence/discussions) - 分享经验和技巧

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**作者**: AI CEO Automation Team
**版本**: 2.0.0
**最后更新**: 2024-03-09

**开始构建你的AI公司吧！** 🚀
