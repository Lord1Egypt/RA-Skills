---
name: API-design-doc
description: 标准化API接口设计文档生成工具。根据需求文档、数据库DDL等输入，进行API的标准化、规范化设计，输出完整的API接口设计文档，包括错误码规范、接口格式规范、入参出参定义、JSON示例等，指导后续的代码开发和前后端联调。使用场景包括：(1) 根据业务需求设计RESTful API接口，(2) 基于数据库DDL生成对应的CRUD接口文档，(3) 规范化现有API接口文档，(4) 为前后端联调提供标准化的接口规范文档
---

# API Design Doc

根据需求文档、数据库DDL等输入，生成标准化的API接口设计文档。

## 工作流程

1. **收集输入信息**
   - 获取需求文档或业务需求描述
   - 获取数据库DDL（如果适用）
   - 明确接口的业务场景和功能需求

2. **页面功能与API接口关系**
   - 明确页面功能与API接口的对应关系


3. **设计API接口**
   - 确定接口的RESTful风格（GET/POST/PUT/DELETE）
   - 定义接口URL路径
   - 设计入参和出参结构
   - 选择合适的错误码

4. **生成接口文档**
   - 使用标准模板生成每个接口的详细文档
   - 包含功能描述、入参、出参、URL、请求方式、JSON示例

5. **输出完整文档**
   - 页面功能与API接口关系
   - 汇总所有接口文档
   - 包含错误码规范总表
   - 提供接口格式规范说明

## 参考资料

### 错误码规范
参见 [error-codes.md](references/error-codes.md) - 完整的错误码列表和说明

### 接口文档模板
参见 [api-spec-template.md](references/api-spec-template.md) - 标准的API接口文档格式

### 命名规范
参见 [naming-conventions.md](references/naming-conventions.md) - API命名和参数命名规范

### 最佳实践
参见 [best-practices.md](references/best-practices.md) - API设计最佳实践

## 模板文件

### API文档模板
使用 [templates/api-doc-template.md](assets/templates/api-doc-template.md) 作为单个接口文档的模板

### API响应模板
使用 [templates/api-response-template.json](assets/templates/api-response-template.json) 作为标准响应格式参考

## 使用指南

当用户请求设计API接口时：

1. 首先读取 [error-codes.md](references/error-codes.md) 了解错误码规范
2. 根据业务需求设计接口，参考 [best-practices.md](references/best-practices.md)
3. 使用 [api-spec-template.md](references/api-spec-template.md) 的格式生成每个接口文档
4. 确保命名符合 [naming-conventions.md](references/naming-conventions.md) 的规范
5. 输出完整的API设计文档，包含所有接口和错误码总表

## 输出格式

接口文档必须包含以下部分：

1. 错误码规范总表
2. 接口格式规范说明
3. 页面功能与API接口关系表，包含以下内容：
   - **页面名称**：前端页面或功能模块的名称
   - **页面功能描述**：页面或功能模块的简要说明
   - **关联API接口**：该页面调用的API接口列表（API-Id）
   - **操作类型**：GET/POST/PUT/DELETE等HTTP方法
   - **接口URL**：完整的API路径
4. 接口清单与详细定义，详细定义的规范如下：

- **接口编号（API-Id）**：顺序生成，格式为 API001-接口名称，如 API001-用户登录, API002-获取用户列表, ...
- **功能描述**：详细描述接口的功能和用途
- **入参**：参数类型和说明（标注必填/可选）
- **返回参数**：返回值类型和说明
- **URL地址**：完整的API路径
- **请求方式**：GET/POST/PUT/DELETE
- **接口 JSON 示例**：完整的请求和响应JSON示例



## 输出位置

- 仅生成一份API文档，保存在项目根目录下的 `doc/` 目录。
- 若 `doc/` 目录不存在，应自动创建该目录后再写入文档。
- 文档文件名固定为：`API接口设计文档.md`，内容包含：
- 错误码总表（来自 references/error-codes.md）
- 接口格式规范（来自 references/api-spec-template.md 的说明部分）
- 页面功能与API接口关系表（按页面或功能模块归类）
- 接口清单与详细定义（按模块归类的所有接口条目）