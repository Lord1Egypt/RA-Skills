# api-doc-gen — API 文档自动生成器

## 痛点
- 手写 API 文档费时费力，格式不统一
- 前后端接口对接时，文档经常滞后于代码
- 不同项目文档风格不一致，维护成本高
- Swagger/OpenAPI 写起来复杂，容易出错

## 场景
- 写好一个 Flask/Django/FastAPI 接口，直接生成完整 API 文档
- 根据代码注释自动推断参数类型和返回值
- 导出 OpenAPI 3.0 (Swagger) JSON/YAML 格式
- 导出 Markdown 格式给非技术团队查看
- 导出 Postman Collection 方便调试

## 定价
- **免费**：基础文档生成（Markdown 格式，单文件）
- **Pro 19元**：OpenAPI 3.0 + Postman Collection + 多端点支持
- **Team 49元**：批量处理 + HTML 文档站 + 自定义模板

## 支持框架
- FastAPI
- Flask
- Django DRF
- Express.js
- 通用函数/类（基于注释推断）

## 输出格式
- `--format markdown` — Markdown 格式 API 文档
- `--format openapi` — OpenAPI 3.0 JSON
- `--format openapi-yaml` — OpenAPI 3.0 YAML
- `--format postman` — Postman Collection JSON

## 指令格式

### 基本用法
```
api-doc-gen analyze <file_or_code> [选项]
```

### 示例
```bash
# 分析 Python Flask 文件
api-doc-gen analyze app.py --framework flask --format markdown

# 分析 FastAPI 代码
api-doc-gen analyze main.py --framework fastapi --format openapi

# 分析 Express.js 文件
api-doc-gen analyze routes.js --framework express --format postman

# 从代码字符串生成
api-doc-gen analyze "def hello(name: str) -> str: ..." --language python --format markdown

# 批量处理目录
api-doc-gen batch ./api/ --framework fastapi --format openapi -o docs/
```

## 字段推断规则

基于 Python type hints / JSDoc / 代码注释自动推断：
- 参数类型：string, integer, number, boolean, array, object
- 是否必填：默认必填，有默认值则可选
- 描述：优先使用注释，其次参数名
- 格式：email, phone, url, date, datetime 等

## 内置响应模板

| 场景 | 状态码 | 响应结构 |
|:---|:---|:---|
| 成功 | 200 | `{code: 0, data: {}, message: "success"}` |
| 创建成功 | 201 | `{code: 0, data: {id}, message: "created"}` |
| 参数错误 | 400 | `{code: 400, data: null, message: "参数错误"}` |
| 未授权 | 401 | `{code: 401, data: null, message: "未授权"}` |
| 服务器错误 | 500 | `{code: 500, data: null, message: "服务器错误"}` |

## 技术细节

- **语言**：Python 3.8+
- **依赖**：仅标准库（无外部依赖）
- **安装**：pip install -r requirements.txt
- **CLI**：基于 argparse
