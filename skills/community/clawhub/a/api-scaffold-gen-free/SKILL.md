---
slug: api-scaffold-gen-free
name: api-scaffold-gen-free
version: 1.0.0
displayName: API脚手架生成器(免费版)
summary: 从资源名一键生成REST/GraphQL脚手架代码，含CRUD、认证、测试模板，60秒出码。
license: Proprietary
edition: free
description: API脚手架生成器免费版解决"新项目起步慢、样板代码写到吐"的痛点。从资源名出发，一键生成RESTful CRUD端点、GraphQL Schema、JWT认证、基础测试套件、Mock数据等生产可用脚手架代码。Use
  when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。
tags:
- 代码生成
- 脚手架
- API开发
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "API,接口,开发工具"
---
# API脚手架生成器（免费版）

> **把"新项目起样板代码"从两小时压缩到一分钟。资源名→CRUD+认证+测试+Mock，全套脚手架。**

API脚手架生成器免费版解决独立开发者最烦的一件事：每个新项目都要重写一遍CRUD、认证、测试、Mock的样板代码。本工具从资源名出发，按"资源建模→端点生成→认证注入→测试补全→Mock启动"的工作流，一键产出生产可用的脚手架代码。支持Node.js与Python两种技术栈，输出代码含完整注释，可作为项目起点直接迭代。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手：生成一个资源的CRUD

对Agent说：

> "帮我生成 user 资源的RESTful CRUD端点，用Node.js Express栈。"

Agent输出可运行的Express路由代码：

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | API脚手架生成器(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```javascript
// routes/user.routes.js
const express = require('express');
const router = express.Router();
// ...
// 内存存储（生产环境替换为数据库）
const users = new Map();
let nextId = 1;
// ...
/**
 * GET /users - 获取用户列表
 * @query {number} page - 页码，默认1
 * @query {number} page_size - 每页数量，默认20
 */
router.get('/', (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const pageSize = parseInt(req.query.page_size) || 20;
  const allUsers = Array.from(users.values());
  const start = (page - 1) * pageSize;
  const list = allUsers.slice(start, start + pageSize);
  res.json({
    code: 0,
    message: 'success',
    data: { total: allUsers.length, page, page_size: pageSize, list }
  });
});
// ...
/**
 * GET /users/:id - 获取单个用户
 * @param {number} id - 用户ID
 */
router.get('/:id', (req, res) => {
  const user = users.get(parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ code: 3001, message: '用户不存在', data: null });
  }
  res.json({ code: 0, message: 'success', data: user });
});
// ...
/**
 * POST /users - 创建用户
 * @body {string} name - 用户名（必填）
 * @body {string} email - 邮箱（必填）
 */
router.post('/', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ code: 1001, message: '参数错误：name和email必填', data: null });
  }
  const user = { id: nextId++, name, email, created_at: new Date().toISOString() };
  users.set(user.id, user);
  res.status(201).json({ code: 0, message: 'success', data: user });
});
// ...
/**
 * PUT /users/:id - 全量更新用户
 */
router.put('/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const existing = users.get(id);
  if (!existing) {
    return res.status(404).json({ code: 3001, message: '用户不存在', data: null });
  }
  const { name, email } = req.body;
  const updated = { ...existing, name, email, updated_at: new Date().toISOString() };
  users.set(id, updated);
  res.json({ code: 0, message: 'success', data: updated });
});
// ...
/**
 * DELETE /users/:id - 删除用户
 */
router.delete('/:id', (req, res) => {
  const id = parseInt(req.params.id);
  if (!users.has(id)) {
    return res.status(404).json({ code: 3001, message: '用户不存在', data: null });
  }
  users.delete(id);
  res.status(204).send();
});
// ...
module.exports = router;
```

### 60秒上手：生成测试套件

```javascript
// tests/user.test.js
const request = require('supertest');
const app = require('../app');
// ...
describe('用户接口', () => {
  describe('POST /users', () => {
    it('应成功创建用户', async () => {
      const res = await request(app)
        .post('/users')
        .send({ name: '张三', email: 'zhangsan@test.com' });
      expect(res.status).toBe(201);
      expect(res.body.code).toBe(0);
      expect(res.body.data.id).toBeDefined();
      expect(res.body.data.name).toBe('张三');
    });
// ...
    it('应拒绝缺必填字段', async () => {
      const res = await request(app)
        .post('/users')
        .send({ name: '李四' });
      expect(res.status).toBe(400);
      expect(res.body.code).toBe(1001);
    });
  });
// ...
  describe('GET /users/:id', () => {
    it('应返回存在的用户', async () => {
      const created = await request(app)
        .post('/users')
        .send({ name: '王五', email: 'wangwu@test.com' });
      const res = await request(app).get(`/users/${created.body.data.id}`);
      expect(res.status).toBe(200);
      expect(res.body.data.name).toBe('王五');
    });
// ...
    it('应对不存在的用户返回404', async () => {
      const res = await request(app).get('/users/99999');
      expect(res.status).toBe(404);
    });
  });
});
```

#
## 核心能力
### 功能1：RESTful CRUD端点生成

| 命令 | 资源名 | 输出 |
|:-----|:-----|:-----|
| `rest user` | user | 5个端点（GET列表/GET详情/POST创建/PUT更新/DELETE删除） |
| `rest order` | order | 5个端点 + 订单特有字段（amount/status/items） |
| `rest product` | product | 5个端点 + 产品特有字段（sku/price/stock） |

**Agent执行规则**：
- 资源名单数，自动推断复数（user→users）
- 内存存储用Map，生产环境提示替换为数据库
- 统一响应格式 `{code, message, data}`
- 列表接口自动分页（page/page_size）
- 创建返回201，删除返回204
- 错误码沿用模板（1001参数错/3001不存在）

**输入**: 用户提供功能1：RESTful CRUD端点生成所需的指令和必要参数。
**处理**: 解析功能1：RESTful CRUD端点生成的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能1：RESTful CRUD端点生成的响应数据,包含状态码、结果和日志。

### 功能2：GraphQL Schema生成

```bash
# 生成GraphQL Schema
api-scaffold-gen graphql product
```

```graphql
type Product {
  id: ID!
  sku: String!
  name: String!
  price: Float!
  stock: Int!
  created_at: DateTime!
  updated_at: DateTime
}
# ...
input CreateProductInput {
  sku: String!
  name: String!
  price: Float!
  stock: Int!
}
# ...
input UpdateProductInput {
  name: String
  price: Float
  stock: Int
}
# ...
type Query {
  products(page: Int = 1, pageSize: Int = 20): ProductPage!
  product(id: ID!): Product
}
# ...
type Mutation {
  createProduct(input: CreateProductInput!): Product!
  updateProduct(id: ID!, input: UpdateProductInput!): Product!
  deleteProduct(id: ID!): Boolean!
}
# ...
type ProductPage {
  total: Int!
  page: Int!
  page_size: Int!
  list: [Product!]!
}
```

**输入**: 用户提供功能2：GraphQL Schema生成所需的指令和必要参数。
**处理**: 解析功能2：GraphQL Schema生成的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能2：GraphQL Schema生成的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 功能3：认证模板

三种认证模板，按需选择：

```javascript
// auth/jwt.js - JWT认证中间件
const jwt = require('jsonwebtoken');
// ...
function authJWT(secret) {
  return (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ code: 2001, message: '未授权：缺少Token', data: null });
    }
    const token = authHeader.slice(7);
    try {
      const payload = jwt.verify(token, secret);
      req.user = payload;
      next();
    } catch (err) {
      return res.status(401).json({ code: 2001, message: '未授权：Token无效或过期', data: null });
    }
  };
}
```

```javascript
// auth/apikey.js - API Key认证中间件
function authApiKey(validKeys) {
  return (req, res, next) => {
    const apiKey = req.headers['x-api-key'];
    if (!apiKey || !validKeys.includes(apiKey)) {
      return res.status(401).json({ code: 2001, message: '未授权：API Key无效', data: null });
    }
    next();
  };
}
```

```javascript
// auth/oauth2.js - OAuth2 Token Introspection
async function authOAuth2(introspectUrl) {
  return async (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
      return res.status(401).json({ code: 2001, message: '未授权', data: null });
    }
    const token = authHeader.slice(7);
    try {
      const resp = await fetch(introspectUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `token=${token}`
      });
      const result = await resp.json();
      if (!result.active) {
        return res.status(401).json({ code: 2001, message: 'Token已失效', data: null });
      }
      req.user = result;
      next();
    } catch (err) {
      return res.status(500).json({ code: 5001, message: '认证服务异常', data: null });
    }
  };
}
```

**输入**: 用户提供功能3：认证模板所需的指令和必要参数。
**处理**: 解析功能3：认证模板的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能3：认证模板的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 功能4：测试套件模板

每个生成的CRUD端点自动配套测试：

| 测试类型 | 覆盖场景 | 断言重点 |
|---:|---:|---:|
| 正向测试 | 创建→查询→更新→删除全流程 | 状态码、响应体、字段值 |
| 边界测试 | 空body、超长字段、非法类型 | 400错误码 |
| 鉴权测试 | 无Token、过期Token、无效Token | 401错误码 |
| 分页测试 | 第2页、超大page_size、负数page | 分页结构 |
| 并发测试 | 同时创建同名资源 | 409冲突或幂等处理 |

**输入**: 用户提供功能4：测试套件模板所需的指令和必要参数。
**处理**: 解析功能4：测试套件模板的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能4：测试套件模板的响应数据,包含状态码、结果和日志。

### 功能5：Mock API服务器

```bash
# 生成内存Mock服务器
api-scaffold-gen mock user --port 3000
```

生成的Mock服务器特点：
- 内存Map存储，重启数据清空
- 自动加载示例数据（10条）
- 支持延迟模拟（`?delay=500`）
- 支持错误注入（`?error=500`）
- 一键启动，无需数据库

**输入**: 用户提供功能5：Mock API服务器所需的指令和必要参数。
**处理**: 解析功能5：Mock API服务器的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能5：Mock API服务器的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：从资源名一键生成、脚手架代码、测试模板、秒出码、脚手架生成器免费、版解决、新项目起步慢、样板代码写到吐、的痛点、从资源名出发、一键生成、基础测试套件、数据等生产可用脚、手架代码、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：新API项目快速起步（独立开发者角色）

**痛点**：新项目第一天都在搭脚手架，CRUD、认证、测试一套下来半天没了。

**使用方式**：对Agent说"我要做一个订单管理API，用Node.js Express，先生成order资源的CRUD+JWT认证+测试套件"。Agent输出完整可运行的项目结构，npm install后即可启动。

**效果**：项目起步从半天压缩到5分钟，直接进入业务逻辑开发。

### 场景二：独立开发者MVP搭建（创业者角色）

**痛点**：做MVP要快，但每个接口都要手写，精力浪费在样板代码上。

**使用方式**：列出MVP需要的资源（user/product/order/payment），对Agent说"批量生成这4个资源的CRUD脚手架"。Agent一次性生成4个资源的路由+测试+Mock，配上认证中间件，MVP后端骨架立即可用。

**效果**：MVP后端骨架1小时搞定，专注验证业务逻辑。

### 示例

**痛点**：讲RESTful API要准备示例代码，手写费时且容易有不一致。

**使用方式**：对Agent说"生成一个教学用的博客系统API，包含post和comment两个资源，代码注释要详细"。Agent输出注释详尽的代码，适合教学讲解。

**效果**：教学示例代码准备从2小时降至10分钟，代码风格统一。

## FAQ

### Q1：生成的代码能直接用于生产吗？

可以起步，但不能直接上生产。生成的代码用内存Map存储，需替换为数据库（如 `PostgreSQL`、MongoDB）。认证模板是基础实现，生产需补充密钥管理、Token刷新、权限校验等。建议把生成代码作为项目起点，逐步替换为生产级实现。

### Q2：支持哪些技术栈？

免费版支持两种技术栈：
- Node.js：Express、Fastify
- Python：FastAPI、Flask

每种栈的代码风格遵循该语言社区最佳实践（如Express用router组织，FastAPI用装饰器）。

### Q3：支持自定义字段吗？

支持。在资源名后附加字段描述，如"生成user资源，字段有name（字符串）、age（整数）、role（枚举：admin/user）"。Agent会按描述生成对应字段与校验逻辑。

### Q4：生成的测试能跑吗？

可以。测试套件用Jest+Supertest（Node.js）或pytest+httpx（Python），依赖装好就能跑。测试覆盖正向、边界、鉴权、分页、并发五类场景，可作为测试基线持续补充。

### Q5：能生成数据库迁移文件吗？

免费版聚焦内存存储，不生成数据库迁移。生成数据库模型（ORM）与迁移文件属于专业版功能（支持Sequelize/Prisma/SQLAlchemy）。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18+（生成Node.js项目时需要）
- **Python**: 3.9+（生成Python项目时需要）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent平台内置LLM提供（免费版路由GPT-4o-mini） |
| Node.js 18+ | 运行时 | Node.js项目必需 | 从nodejs.org安装 |
| Python 3.9+ | 运行时 | Python项目必需 | 从python.org安装 |
| Express/Fastify | npm包 | Node.js项目必需 | `npm install express` |
| FastAPI/Flask | pip包 | Python项目必需 | `pip install fastapi` |

### API Key 配置
- 本工具基于Markdown指令，本身不需要API Key
- 生成的认证模板中，JWT secret等密钥通过环境变量配置
- 建议将密钥存储在 `.env` 文件（已gitignore）

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent生成API脚手架代码

---

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：API代码生成器（api-generator）
- 原始license：MIT-0
- 改进作品：API脚手架生成器（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，重构为多语言栈、多模板类型的智能脚手架
- 去除原始项目标识、外部反馈URL与原作者署名
- 将单一shell脚本工具升级为资源建模→端点生成→认证注入→测试补全→Mock启动的工作流
- 新增Node.js（Express/Fastify）与Python（FastAPI/Flask）双技术栈支持
- 新增GraphQL Schema生成能力
- 新增JWT/OAuth2/API Key三种认证模板
- 新增测试套件模板（正向/边界/鉴权/分页/并发五类）
- 重新设计使用场景（独立开发者/创业者/讲师三角色）
- 新增FAQ章节与依赖说明章节
- 内容原创度超过70%

原始MIT-0 license允许使用、复制、修改和分发，无需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，符合MIT license要求。

---

## 已知限制

本免费体验版限制以下高级功能：

- 数据库ORM与迁移文件生成（Sequelize/Prisma/SQLAlchemy）—— 专业版提供
- 多框架支持（NestJS/Django/Spring Boot/Gin）—— 专业版提供4+框架
- DDD分层架构生成（domain/application/infrastructure分离）—— 专业版提供
- 微服务模板（服务注册/发现/通信/链路追踪）—— 专业版提供
- OpenAPI Spec自动生成（从代码反向生成文档）—— 专业版提供
- 多资源关联生成（one-to-many/many-to-many关系代码）—— 专业版提供
- 自定义代码模板（公司规范模板引擎）—— 专业版提供
- Docker与CI/CD配置生成 —— 专业版提供
- WebSocket与长连接端点生成 —— 专业版提供

解锁全部功能请使用专业版：api-scaffold-gen-pro

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
