# AI Company

**完全自主的AI公司运营系统** - 7×24小时自动化发现需求、设计、开发、销售、运维，实现盈利

> **注意**：这是一个技能定义和示例代码库。使用本技能创建您的AI公司项目，而不是直接使用这些文件。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude](https://img.shields.io/badge/Claude-API-orange.svg)](https://www.anthropic.com/)

## 🚀 核心功能

### 完全自动化的公司运营

- **🔍 自主发现需求** - 扫描GitHub、Reddit、Twitter发现市场机会
- **🎨 智能设计开发** - AI产品设计师和开发者团队协作
- **💬 自动化销售** - AI销售和营销自动获取客户
- **🔧 持续交付支持** - AI客服和DevOps自动运维
- **📊 数据驱动优化** - 基于反馈持续迭代产品和流程
- **🔐 版本化管理** - 所有AI员工可版本控制和快速回滚

### 轻量级技术栈

```
Python 3.10+ + Claude Agent SDK + JSON文件
```

无需复杂的基础设施，几分钟即可启动！

## 📋 目录

- [快速开始](#快速开始)
- [AI员工角色](#ai员工角色)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [工作流程](#工作流程)
- [示例代码](#示例代码)
- [文档](#文档)
- [贡献](#贡献)
- [许可证](#许可证)

## 🎯 快速开始

### 1. 安装依赖

```bash
pip install anthropic python-dotenv pyyaml requests
```

### 2. 创建你的AI公司项目

```bash
# 使用初始化脚本创建项目（推荐）
cd ai-company/examples
python3 init_ai_company.py my-ai-company

# 或手动创建项目结构
mkdir my-ai-company
cd my-ai-company
```

### 3. 配置和测试

```bash
# 配置环境变量
cd my-ai-company
cp .env.example .env
# 编辑 .env 文件，添加你的API密钥

# 运行示例测试
python3 ../examples/simple_ai_employee.py
python3 ../examples/simple_coordinator.py

# 启动你的AI公司
python main.py start
```

## 👥 AI员工角色

### 核心团队

| AI员工 | 角色 | 主要功能 |
|--------|------|----------|
| **Market Research AI** | 市场研究专家 | 扫描平台发现机会，分析市场趋势 |
| **Product Designer AI** | 产品设计师 | 设计产品功能和定价策略 |
| **Developer AI** | 开发专家 | 编写代码、文档和测试 |
| **Sales & Marketing AI** | 销售营销 | 生成营销内容，回复客户咨询 |
| **Customer Support AI** | 客服专家 | 回答问题，收集反馈 |
| **Monitor AI** | 监控专家 | 监控系统状态，生成告警 |
| **Finance AI** | 财务专家 | 追踪收支，生成财务报告 |

## 📁 技能文件 vs 创建的项目

### 技能文件结构（当前目录）
```
ai-company/                 # 技能定义
├── SKILL.md               # 技能主文档
├── README.md              # 项目说明
├── LICENSE                # 许可证
├── CONTRIBUTING.md        # 贡献指南
├── docs/                  # 详细文档
│   ├── design.md         # 设计文档
│   └── api.md            # API文档
└── examples/             # 示例代码
    ├── simple_ai_employee.py
    ├── simple_event_bus.py
    ├── simple_coordinator.py
    └── config.yaml
```

### 使用本技能创建的项目结构
```
my-ai-company/              # 您创建的AI公司
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
│   └── versions.json
├── shared/                 # 共享数据
│   ├── opportunities.json
│   ├── products.json
│   ├── customers.json
│   └── state.json
├── workflows/              # 工作流定义
│   ├── discover_opportunities.yaml
│   ├── build_product.yaml
│   └── make_sale.yaml
├── main.py                 # 主调度器
├── config.yaml             # 配置文件
└── README.md
```

## ⚙️ 配置说明

### 基本配置

```yaml
# config.yaml
company:
  name: "My AI Company"
  industry: "software_development"

ai_employees:
  - name: market_researcher
    enabled: true
    version: "v1.0"

apis:
  anthropic_api_key: "${ANTHROPIC_API_KEY}"
  github_token: "${GITHUB_TOKEN}"
```

### 环境变量

```bash
# .env
ANTHROPIC_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
```

## 🔄 工作流程

### 完整的自动化循环

```
1. 机会发现 → Market Research AI扫描平台
2. 产品设计 → Product Designer AI创建设计
3. 产品开发 → Developer AI实现MVP
4. 营销销售 → Sales & Marketing AI获取客户
5. 客户支持 → Customer Support AI维护关系
6. 数据分析 → Monitor AI生成优化建议
7. 产品迭代 → 基于反馈持续改进
```

### 示例：从发现机会到销售

```python
# 1. 发现机会
opportunity = market_researcher.scan_github(["automation", "tool"])

# 2. 设计产品
design = product_designer.create_design(opportunity)

# 3. 开发产品
product = developer.build(design)

# 4. 营销推广
sales_marketing.promote(product)

# 5. 跟进销售
sale = sales_marketing.close_sale(customer, product)

# 6. 记录收入
finance.record_revenue(sale)
```

## 💡 示例代码

### 创建自定义AI员工

```python
from simple_ai_employee import SimpleAIEmployee

class CustomAI(SimpleAIEmployee):
    def __init__(self):
        super().__init__(
            name="custom_ai",
            role="自定义专家",
            version="v1.0"
        )

# 使用
ai = CustomAI()
result = ai.work({
    "description": "执行任务"
})
```

### 事件驱动通信

```python
from simple_event_bus import SimpleEventBus

bus = SimpleEventBus()

# 订阅事件
def handler(data):
    print(f"收到: {data}")

bus.subscribe("custom.event", handler)

# 发布事件
bus.publish("custom.event", {"message": "Hello"})
```

## 📚 文档

- [设计文档](docs/design.md) - 详细的系统设计
- [API文档](docs/api.md) - 完整的API参考
- [示例代码](examples/) - 实用示例
- [贡献指南](CONTRIBUTING.md) - 如何贡献

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)

### 贡献方式

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🌟 特性

### ✅ 优势

- **简单易用** - 只需Python和JSON文件
- **完全自动化** - 7×24小时自动运营
- **持续优化** - 基于反馈不断改进
- **版本控制** - 所有AI员工可回滚
- **人类监督** - 异常时自动告警
- **可扩展** - 轻松添加新的AI员工

### 🎯 适用场景

- 软件开发服务
- SaaS产品开发
- 数字产品销售
- 技术咨询服务
- 自动化客服

## 🔗 相关资源

- [Claude API](https://www.anthropic.com/)
- [GitHub示例项目](https://github.com/sendwealth/claw-intelligence)
- [社区讨论](https://github.com/sendwealth/claw-intelligence/discussions)

## 📞 支持

- GitHub Issues: 技术问题
- GitHub Discussions: 一般讨论
- Email: support@ai-company.com

---

**开始构建你的AI公司吧！** 🚀
