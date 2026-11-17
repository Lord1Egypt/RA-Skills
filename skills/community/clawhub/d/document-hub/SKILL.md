# Document Hub - PRD 模板系统

飞书文档 PRD 模板系统，支持多种产品类型的标准化文档生成。

## 功能特性

- 📝 **多种模板类型**: 基础 PRD、AI 功能 PRD、API 设计 PRD、数据产品 PRD、平台产品 PRD
- 🎨 **Jinja2 模板引擎**: 灵活的变量替换和条件渲染
- 🚀 **飞书集成**: 一键生成并上传到飞书文档
- 🔧 **可扩展**: 支持自定义模板和扩展

## 模板类型

| 模板 | 文件 | 适用场景 |
|------|------|----------|
| 基础 PRD | `base.md` | 通用产品需求文档 |
| AI 功能 PRD | `ai-feature-prd.md` | AI/LLM 功能产品 |
| API 设计 PRD | `api-prd.md` | 接口/API 设计 |
| 数据产品 PRD | `data-product-prd.md` | 数据报表/服务 |
| 平台产品 PRD | `platform-prd.md` | 平台/开发者产品 |

## 快速开始

### 1. 使用 Python 脚本生成

```python
from scripts.template_engine import PRDGenerator

# 创建生成器
generator = PRDGenerator()

# 定义产品信息
product_info = {
    'product_name': '智能客服系统',
    'version': '1.0.0',
    'author': '产品经理',
    'business_background': '当前客服团队面临大量重复性问题...',
    'current_pain_points': '人工回复慢、成本高...'
}

# 生成 AI 功能 PRD
prd_content = generator.create_ai_feature_prd(product_info)

# 或保存到文件
generator.create_ai_feature_prd(
    product_info,
    output_path='./智能客服系统_PRD.md'
)
```

### 2. 使用命令行工具

```bash
# 交互式生成
python scripts/generate_prd.py --interactive

# 从 JSON 文件生成
python scripts/generate_prd.py --template ai-feature --input product.json --output PRD.md

# 生成并创建飞书文档
python scripts/generate_prd.py --template base --input product.json --feishu
```

### 3. 在 OpenClaw 中使用

```python
# 读取模板引擎
read ~/.openclaw/workspace/skills/document-hub/scripts/template_engine.py

# 生成 PRD 内容
prd_content = engine.render('ai-feature', {
    'product_name': '新产品',
    'version': '1.0.0'
})

# 创建飞书文档
feishu_create_doc(title='新产品 PRD', markdown=prd_content)
```

## 模板变量

### 基础 PRD 变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `product_name` | 产品名称 | 智能客服系统 |
| `version` | 版本号 | 1.0.0 |
| `author` | 作者 | 产品经理 |
| `status` | 文档状态 | 草稿/评审中/已批准 |
| `business_background` | 业务背景 | 当前客服团队... |
| `current_pain_points` | 当前痛点 | 人工回复慢... |

### AI 功能 PRD 特有变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ai_capability_type` | AI 能力类型 | LLM/VLM/Agent |
| `selected_model` | 选定模型 | GPT-4/Claude |
| `system_prompt` | System Prompt | 你是一个助手... |
| `accuracy_threshold` | 准确率阈值 | 85 |

### API PRD 特有变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `api_name` | API 名称 | 用户服务 API |
| `base_url` | 基础 URL | https://api.example.com |
| `protocol` | 协议 | HTTPS |
| `auth_method` | 认证方式 | OAuth 2.0 |

## 目录结构

```
document-hub/
├── SKILL.md                    # 本文件
├── templates/
│   └── prd/
│       ├── base.md            # 基础 PRD 模板
│       ├── ai-feature-prd.md  # AI 功能 PRD 模板
│       ├── api-prd.md         # API 设计 PRD 模板
│       ├── data-product-prd.md # 数据产品 PRD 模板
│       └── platform-prd.md    # 平台产品 PRD 模板
├── scripts/
│   ├── template_engine.py     # 模板渲染引擎
│   └── generate_prd.py        # PRD 生成工作流
└── tests/
    └── test_templates.py      # 模板测试
```

## 创建自定义模板

1. 在 `templates/prd/` 目录创建新的 `.md` 文件
2. 使用 Jinja2 语法添加变量 `{{ variable_name }}`
3. 在 `template_engine.py` 的 `TEMPLATE_TYPES` 中注册

示例:
```markdown
# {{product_name}} - 自定义 PRD

## 1. 概述
{{overview}}
```

## 集成飞书

生成 PRD 后，可直接创建飞书文档:

```python
from feishu_create_doc import feishu_create_doc

# 生成 PRD 内容
prd_content = generator.create_prd(product_info, 'base')

# 创建飞书文档
result = feishu_create_doc(
    title=f"{product_info['product_name']} - PRD",
    markdown=prd_content
)

print(f"文档链接: {result.get('url')}")
```

## 注意事项

1. 模板使用 Jinja2 语法，变量使用 `{{ variable }}` 格式
2. 条件渲染使用 `{% if condition %}...{% endif %}`
3. 循环使用 `{% for item in items %}...{% endfor %}`
4. 所有模板文件必须使用 UTF-8 编码

## 许可证

MIT License
