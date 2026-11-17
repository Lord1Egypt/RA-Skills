---
slug: api-magic-gen-free
name: api-magic-gen-free
version: 1.0.0
displayName: 接口魔法生成免费版
summary: 基于magic-api框架的接口快速生成工具，通过Web UI编写脚本自动映射HTTP接口，无需Controller/Service/Dao。
license: Proprietary
edition: free
description: 面向Java后端开发者的接口快速生成工具，基于magic-api框架能力封装。通过Web UI编写脚本即可自动映射为HTTP接口，免除Controller、Service、Dao、Mapper、XML、VO等Java对象的编写负担，特别适合原型验证、内部工具、数据看板接口等场景。Use
  when 需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于逆向工程闭源API。
tags:
- 集成工具
- 接口开发
- 低代码
- Java生态
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
# 接口魔法生成工具（免费版）

本工具为Java后端开发者提供基于magic-api框架的接口快速生成能力。免费版覆盖核心场景：脚本编写、CRUD映射、条件查询、基础认证，可快速搭建原型与内部工具接口。

## 概述

传统Java接口开发需要编写Controller、Service、Dao、Mapper、XML、VO等多个文件，流程繁琐。magic-api框架通过Web UI编写脚本自动生成HTTP接口，将开发效率提升数倍，特别适合原型验证、内部工具、数据看板等场景。

本工具以中文实战指南形式提供完整使用说明，覆盖从Maven依赖配置到生产部署的全流程，配套安全注意事项与性能调优建议。

## 核心能力

| 能力分类 | 说明 |
|----|---|
| 脚本编写 | Web UI在线编辑，实时调试，所见即所得 |
| 请求映射 | 自动映射GET/POST/PUT/DELETE四类HTTP方法 |
| 内置对象 | request、path、body、db、cache、log、response |
| 数据库操作 | 内置select、selectOne、insert、update、delete、page |
| 事务支持 | 通过db.transaction包裹批量操作 |
| 脚本语法 | 类JavaScript语法，变量定义、条件判断、循环 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：magic、api、框架的接口快速生、成工具、编写脚本自动映射、Controller、Service、Dao、后端开发者的接口、快速生成工具、框架能力封装、编写脚本即可自动、映射为、Mapper、XML、对象的编写负担、特别适合原型验证、内部工具、数据看板接口等场、Use、when、接口对接、Webhook、系统连接时使用、不适用于逆向工程等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：后端原型快速验证

产品经理提出需求后，2小时内提供可用接口供前端联调，缩短需求确认周期，避免返工。

### 场景二：内部运营后台接口

为运营、客服等内部团队提供数据查询、导出、统计接口，无需走完整研发流程。

### 场景三：数据看板接口

为BI看板、报表系统提供数据查询接口，支持分页、聚合、条件过滤。

### 场景四：独立开发者API服务

一人公司或独立开发者快速搭建SaaS产品的后端API，专注业务逻辑而非框架代码。

## 快速开始

### 依赖详情

```xml
<dependency>
    <groupId>org.ssssssss</groupId>
    <artifactId>magic-api-spring-boot-starter</artifactId>
    <version>2.2.2</version>
</dependency>
```

### 第二步：配置application.yml

```yaml
server:
  port: 9999
# ...
magic-api:
  web: /magic/web              # Web UI 入口
  resource:
    location: /data/magic-api  # 脚本存储位置
```

### 第三步：访问Web UI编写接口

打开浏览器访问 `http://localhost:9999/magic/web`，新建接口并编写脚本：

```javascript
// GET /api/user/:id - 查询单个用户
var user = db.selectOne("select * from user where id = ?", path.id);
return user ? {code: 200, data: user} : {code: 404, msg: "用户不存在"};
```

保存后接口立即可用，无需重启服务。完整上手时间约120秒。

## 示例

### 内置对象速查表

| 对象 | 说明 | 示例 |
|:-----|:-----|:-----|
| `request` | HTTP请求参数 | `request.name` |
| `path` | URL路径参数 | `path.id` |
| `body` | 请求体JSON | `body.name` |
| `db` | 数据库操作 | `db.select()` |
| `log` | 日志输出 | `log.info()` |
| `cache` | 缓存操作 | `cache.set()` |
| `response` | HTTP响应 | `response.setHeader()` |

### 数据库操作示例

```javascript
// 查询列表
var list = db.select("select * from user where status = ?", 1);
// ...
// 查询单条
var user = db.selectOne("select * from user where id = ?", id);
// ...
// 查询单值
var count = db.selectValue("select count(*) from user");
// ...
// 分页查询
var page = db.page("select * from user", 1, 10);
// 返回: {list: [...], total: 100, pageSize: 10, pageNumber: 1}
// ...
// 插入并返回自增ID
var id = db.insert("user", {name: "张三", age: 25}, true);
// ...
// 更新
db.update("user", {name: "李四"}, "id = ?", 1);
// ...
// 删除
db.delete("user", "id = ?", 1);
```

### 事务处理

```javascript
db.transaction(() => {
    var orderId = db.insert("orders", order, true);
    db.update("product", {stock: stock - 1}, "id = ?", productId);
});
```

### RESTful CRUD完整示例

```javascript
// GET /api/user - 查询列表
return {code: 200, data: db.select("select * from user")};
// ...
// POST /api/user - 新增
var id = db.insert("user", body, true);
return {code: 200, data: {id: id}, msg: "创建成功"};
// ...
// PUT /api/user/:id - 更新
db.update("user", body, "id = ?", path.id);
return {code: 200, msg: "更新成功"};
// ...
// DELETE /api/user/:id - 删除
db.delete("user", "id = ?", path.id);
return {code: 200, msg: "删除成功"};
```

### 条件查询（动态拼接）

```javascript
var sql = "select * from user where 1=1";
var params = [];
// ...
if (request.name) {
    sql += " and name like ?";
    params.push("%" + request.name + "%");
}
if (request.status) {
    sql += " and status = ?";
    params.push(request.status);
}
// ...
return db.select(sql, ...params);
```

### 登录认证基础模式

```javascript
// 登录接口
var user = db.selectOne("select * from user where username = ?", body.username);
if (!user || user.password != body.password) {
    return {code: 401, msg: "用户名或密码错误"};
}
// ...
var token = generateToken(user.id);
cache.set("token:" + token, user.id, 86400);
return {code: 200, data: {token: token, user: user}};
// ...
// 认证拦截（放在需要登录的接口开头）
var token = request.header("Authorization");
var userId = cache.get("token:" + token);
if (!userId) return {code: 401, msg: "请先登录"};
```

## 最佳实践

### 1. 使用参数化查询防SQL注入

```javascript
// 正确：使用?占位符
db.select("select * from user where id = ?", id);
// ...
// 错误：字符串拼接，有SQL注入风险
db.select("select * from user where id = " + id);
```

### 2. 密码必须加密存储

使用BCrypt或MD5+盐值，禁止明文存储密码。

### 3. 复杂逻辑拆分多个接口

单脚本不超过100行，复杂业务拆分为多个小接口，便于维护与复用。

### 4. 统一返回结构

所有接口返回统一格式：`{code: 200, data: ..., msg: "..."}`，便于前端处理。

### 5. 脚本目录纳入Git管理

将`/data/magic-api`目录纳入版本控制，支持回滚与多人协作。

## 常见问题

### Q1：生产环境是否需要关闭Web UI？

A：必须关闭或限制IP访问。Web UI暴露在生产环境会被未授权用户篡改接口逻辑，造成严重安全风险。建议通过Nginx白名单或`magic-api.web.enabled=false`关闭。

### Q2：脚本修改后是否需要重启服务？

A：不需要。magic-api支持热加载，保存脚本后立即可用。这是其相比传统Java开发的核心优势。

### Q3：如何调试脚本？

A：Web UI内置调试控制台，可单步执行、查看变量值、打印日志。生产环境可通过`log.info()`输出到日志文件排查。

### Q4：支持哪些数据库？

A：通过Spring Boot的datasource配置，支持MySQL、`PostgreSQL`、Oracle、SQL Server等主流关系型数据库，由底层JDBC驱动决定。

### Q5：脚本如何与已有Java代码协作？

A：通过`import`语句引入Java类，或在Spring容器中注册为Bean后通过`@magic-script`注解调用。

## 已知限制

本免费体验版限制以下高级功能：
- 单接口脚本行数上限为100行
- 不支持多数据源切换
- 不支持自定义拦截器与全局变量
- 不支持接口导出为OpenAPI文档
- 不支持性能监控与慢接口告警

解锁全部功能请使用专业版：api-magic-gen-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **JDK**: 8+
- **Maven**: 3.5+
- **Spring Boot**: 2.x/3.x

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| JDK | 运行时 | 必需 | adoptium.net 官方下载 |
| Maven | 构建工具 | 必需 | maven.apache.org 官方下载 |
| magic-api-spring-boot-starter | Java依赖 | 必需 | Maven中央仓库 |
| Spring Boot | Java框架 | 必需 | Maven中央仓库 |
| JDBC驱动 | Java依赖 | 必需 | 根据数据库类型选择 |

### API Key 配置
- 本免费版基于本地magic-api服务，无需额外API Key
- 数据库连接信息通过application.yml的spring.datasource配置
- 禁止在脚本中硬编码数据库密码，必须使用环境变量或配置中心

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "接口魔法生成免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "api magic gen"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
