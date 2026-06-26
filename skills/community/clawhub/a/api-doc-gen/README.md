# API Doc Generator

> **AI驱动的 API 文档自动生成工具** — 从 Flask/FastAPI/Express 代码自动推断 API 结构，3秒生成专业 Markdown / OpenAPI 3.0 / Postman 文档。

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ⚡ 痛点解决

| 过去 | 现在 |
|:---|:---|
| ❌ 手写 API 文档，1小时只能写3个接口 | ✅ 一行命令，3秒生成完整文档 |
| ❌ 文档与代码不同步，维护成本高 | ✅ 代码即文档，永远保持同步 |
| ❌ OpenAPI 格式写起来复杂容易出错 | ✅ 自动推断类型和参数格式 |
| ❌ 每个项目文档风格不一致 | ✅ 标准化输出，统一风格 |

---

## 🚀 快速开始

```bash
# 安装
pip install -r requirements.txt

# 或直接运行（无需安装）
python cli.py analyze app.py --framework flask --format markdown
```

---

## 📦 支持的框架

| 框架 | 支持状态 | 说明 |
|:---|:---:|:---|
| FastAPI | ✅ | 自动识别 @app.get/post 等装饰器 |
| Flask | ✅ | 自动识别 @app.route, @app.get/post |
| Django DRF | ✅ | 自动识别视图函数 |
| Express.js | ✅ | 自动识别 router.get/post |
| NestJS | ✅ | 自动识别 @Get/@Post 装饰器 |
| 通用代码 | ✅ | 基于函数签名和注释推断 |

---

## 📋 输出格式

### 1. Markdown 文档（免费）
适合团队内部使用，非技术人员也能阅读：

```bash
python cli.py analyze app.py --framework flask --format markdown
```

### 2. OpenAPI 3.0 JSON（Pro）
标准 API 描述格式，可导入 Apifox、Swagger UI、Postman：

```bash
python cli.py analyze app.py --framework fastapi --format openapi -o openapi.json
```

### 3. OpenAPI 3.0 YAML（Pro）
更适合 Git 管理的 YAML 格式：

```bash
python cli.py analyze app.py --framework fastapi --format openapi-yaml -o openapi.yaml
```

### 4. Postman Collection（Pro）
直接导入 Postman 开始调试接口：

```bash
python cli.py analyze app.py --framework express --format postman -o collection.json
```

---

## 📁 使用示例

### 示例 1：分析 Flask 文件

```python
# app.py
from flask import Flask, request
app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表"""
    return {'code': 0, 'data': []}

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建新用户
    Args:
        name (str): 用户名
        email (str): 邮箱地址
    """
    data = request.json
    return {'code': 0, 'data': {'id': 1}}, 201
```

生成文档：
```bash
python cli.py analyze app.py --framework flask --format markdown
```

输出示例：
```markdown
# API Documentation

## /api/users

### 🔵 POST /api/users
**Description:** 创建新用户

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `name` | string | ✅ | - | 用户名 |
| `email` | string | ✅ | - | 邮箱地址 |

**Responses:**
| Status | Description |
|--------|-------------|
| 200 | 成功响应 |
| 400 | 参数错误 |
| 500 | 服务器错误 |
```

### 示例 2：分析 Express.js 文件

```bash
python cli.py analyze routes.js --framework express --format postman
```

### 示例 3：批量处理整个项目

```bash
python cli.py batch ./api/ --extension py --framework fastapi --format openapi -o ./docs/
```

### 示例 4：预览检测到的端点

```bash
python cli.py preview app.py
# 🔍 Found 5 endpoint(s):
#   [1] GET    /api/users
#   [2] POST   /api/users
#   [3] GET    /api/users/:id
#   [4] PUT    /api/users/:id
#   [5] DELETE /api/users/:id
```

### 示例 5：直接从代码字符串生成

```bash
python cli.py analyze --code "def hello(name: str) -> str: return f'Hello {name}'" --language python --format markdown
```

---

## 🔧 高级用法

### 作为 Python 模块使用

```python
from generator import generate_docs, analyze_code

# 分析代码
endpoints = analyze_code(code, language="python", framework="flask")

# 生成文档
md = generate_docs(code, output_format="markdown", title="My API")
openapi_json = generate_docs(code, output_format="openapi", title="My API")
postman = generate_docs(code, output_format="postman", title="My API")
```

---

## 🧠 智能推断

### 类型推断
| 参数名关键词 | 推断类型 | 格式 |
|:---|:---|:---|
| `email` | string | email |
| `phone` / `mobile` | string | tel |
| `url` / `link` | string | url |
| `date` / `time` | string | date-time |
| `price` / `amount` | number | - |
| `is_*` / `has_*` | boolean | - |
| `*_id` | integer | - |
| `count` / `page` | integer | - |

### 参数必填推断
- **必填**：无默认值
- **可选**：有默认值（如 `page=1`）

---

## 📈 为什么选择 API Doc Generator？

| 特性 | API Doc Generator | 手写文档 | Swagger |
|:---|:---|:---|:---|
| 零配置生成 | ✅ | ❌ | ⚠️ 需要写YAML/JSON |
| 代码即文档 | ✅ | ❌ | ⚠️ 需要额外标注 |
| 中国项目适配 | ✅ 符合国内API风格 | ❌ | ❌ |
| 多框架支持 | ✅ 5种主流框架 | N/A | ⚠️ 仅规范层面 |
| CLI工具 | ✅ 开箱即用 | ❌ | ❌ |
| Postman导出 | ✅ 一键生成 | ❌ | ⚠️ 需手动转换 |

---

## 📁 项目结构

```
api-doc-gen/
├── SKILL.md          # OpenClaw 技能描述
├── generator.py      # 核心文档生成引擎
├── cli.py            # 命令行入口
├── README.md         # 本文件
├── requirements.txt  # 依赖列表
└── tests/
    └── test_generator.py  # 单元测试
```

---

## ✅ 运行测试

```bash
pip install pytest pyyaml
pytest tests/ -v
```

---

## 📄 License

MIT License
