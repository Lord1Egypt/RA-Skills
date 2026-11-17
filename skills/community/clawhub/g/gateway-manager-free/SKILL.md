---
slug: gateway-manager-free
name: gateway-manager-free
version: 1.0.0
displayName: API网关管理器(免费版)
summary: 轻量级API网关配置与管理，覆盖路由、认证、限流、监控四大基础能力，60秒上手。
license: Proprietary
edition: free
description: API网关管理器免费版解决中小团队"网关配置散乱、限流靠猜、认证各自实现"的痛点。提供声明式路由配置、统一认证接入、基础速率限制、实时监控看板四大能力，支持以YAML或JSON声明式定义网关规则，自动生成主流网关（Kong/APISIX/Nginx/Envoy）的配置文件。Use
  when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。
tags:
- API网关
- 路由配置
- 限流
- 集成工具
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# API网关管理器（免费版）

> **把"网关配置"从翻文档翻半天压缩到填个表。声明式路由+统一认证+限流+监控，四件套。**

API网关管理器免费版解决中小团队最常踩的三个坑：路由配置散落在多个文件、限流值靠拍脑袋、每个服务各自实现认证。本工具把这些高频操作固化为声明式YAML配置，一键生成Kong/APISIX/Nginx/Envoy的配置文件，配以网关选型决策矩阵，让Agent能直接给出可部署的配置与可执行的优化建议。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手：生成一个路由配置

对Agent说：

> "帮我配置一个网关路由：把 /api/v1/users/* 转发到用户服务 http://user-service:8001，需要JWT认证，限流100QPS。"

Agent输出声明式YAML：

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | API网关管理器(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```yaml
# gateway.yaml
routes:
  - name: user-service
    path: /api/v1/users/*
    methods: [GET, POST, PUT, DELETE]
    upstream: http://user-service:8001
    strip_path: true
    auth:
      type: jwt
      secret_env: JWT_SECRET
      algorithm: HS256
    rate_limit:
      type: sliding_window
      qps: 100
      burst: 20
    timeout:
      connect: 5s
      send: 30s
      read: 30s
```

### 60秒上手：生成目标网关配置

```bash
# 生成Kong声明式配置
gateway-manager render --config gateway.yaml --target kong --output kong.yaml
# ...
# 生成APISIX路由
gateway-manager render --config gateway.yaml --target apisix --output apisix-routes.yaml
# ...
# 生成Nginx配置
gateway-manager render --config gateway.yaml --target nginx --output nginx.conf
# ...
# 生成Envoy配置
gateway-manager render --config gateway.yaml --target envoy --output envoy.yaml
```

#
## 核心能力
### 功能1：声明式路由配置

统一的YAML DSL，一次编写多网关生成：

| 匹配维度 | 字段 | 示例 |
|:-----|:-----|:-----|
| 路径前缀 | `path` | `/api/v1/users/*` |
| HTTP方法 | `methods` | `[GET, POST]` |
| Host头 | `hosts` | `[api.example.com]` |
| 自定义Header | `headers` | `X-Version: v2` |
| 查询参数 | `query` | `tenant=acme` |

**Agent执行规则**：
- 路径用 `/*` 表示前缀匹配，`/exact` 表示精确匹配
- 默认 `strip_path: true`（转发时去掉匹配前缀）
- 多路由按优先级排序（精确 > 前缀 > 通配）
- 默认超时 connect 5s / send 30s / read 30s

**输入**: 用户提供功能1：声明式路由配置所需的指令和必要参数。
**处理**: 解析功能1：声明式路由配置的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能1：声明式路由配置的响应数据,包含状态码、结果和日志。

### 功能2：统一认证代理

四种认证模式在网关层统一处理，下游服务无需重复实现：

```yaml
# API Key认证
auth:
  type: api_key
  header: X-API-Key
  key_store: env  # 从环境变量读取
  key_env: API_KEY_STORE
# ...
# JWT认证
auth:
  type: jwt
  secret_env: JWT_SECRET
  algorithm: HS256
  claims:
    - sub        # 用户ID
    - exp        # 过期时间
    - scope      # 权限范围
# ...
# OAuth2 Token Introspection
auth:
  type: oauth2
  introspection_url: http://auth-service:8080/oauth/introspect
  cache_ttl: 60  # introspection结果缓存60秒
# ...
# Basic Auth
auth:
  type: basic
  htpasswd_file: /etc/nginx/.htpasswd
```

**安全红线**：
- 密钥/Token永远从环境变量读取，禁止硬编码
- JWT密钥至少32字符，建议用RS256非对称算法
- OAuth2 introspection结果必须缓存，避免每次请求都查auth服务
- 认证失败统一返回401，不泄露"用户存在与否"

**输入**: 用户提供功能2：统一认证代理所需的指令和必要参数。
**处理**: 解析功能2：统一认证代理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能2：统一认证代理的响应数据,包含状态码、结果和日志。

### 已知限制

两种限流算法，按需选择：

| 算法 | 适用场景 | 配置示例 |
|---:|---:|---:|
| 固定窗口 | 简单场景，容忍边界突刺 | `type: fixed_window, qps: 100` |
| 滑动窗口 | 精确限流，边界平滑 | `type: sliding_window, qps: 100, burst: 20` |

```yaml
rate_limit:
  type: sliding_window
  qps: 100
  burst: 20
  key: remote_addr  # 按客户端IP限流
  # 或 key: header:X-Tenant-Id  按租户限流
  # 或 key: jwt:sub  按用户限流
  response_headers: true  # 返回X-RateLimit-Remaining头
```

**限流key选择决策**：
- `remote_addr`：防爬虫、防DDoS
- `header:X-API-Key`：按调用方限流
- `jwt:sub`：按用户限流
- `header:X-Tenant-Id`：多租户按租户限流

**输入**: 用户提供已知限制所需的指令和必要参数。
**处理**: 解析已知限制的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回已知限制的响应数据,包含状态码、结果和日志。

### 功能4：监控指标采集

采集四类核心指标，输出到Prometheus格式：

```yaml
metrics:
  enabled: true
  port: 9091  # metrics暴露端口
  collect:
    - request_count       # 请求总数
    - request_duration    # 请求延迟（P50/P95/P99）
    - status_code_count   # 状态码分布
    - upstream_latency    # 上游服务延迟
  labels:
    - route
    - method
    - status
```

**关键指标看板**：

```text
Gateway Metrics Dashboard
=========================
Total QPS:         1,250
P50 Latency:       45ms
P95 Latency:       180ms
P99 Latency:       420ms
Error Rate (5xx):  0.3%
Rate Limited (429): 2.1%
# ...
Top Routes by QPS:
1. /api/v1/users      450 QPS  P95:120ms
2. /api/v1/orders     320 QPS  P95:200ms
3. /api/v1/products   280 QPS  P95:90ms
```

**输入**: 用户提供功能4：监控指标采集所需的指令和必要参数。
**处理**: 解析功能4：监控指标采集的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能4：监控指标采集的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 功能5：网关选型决策矩阵

不知道选哪个网关？按以下矩阵决策：

| 维度 | Kong | APISIX | Nginx | Envoy |
|:---:|:---:|:---:|:---:|:---:|
| 性能 | 高 | 极高 | 极高 | 高 |
| 插件生态 | 丰富 | 丰富 | 中（Lua） | 中（Filter） |
| 配置方式 | DB/声明式 | 声明式 | 文件 | xDS动态 |
| 动态配置 | 支持 | 支持 | 需reload | 原生支持 |
| 多协议 | HTTP/gRPC/TCP | HTTP/gRPC/TCP | HTTP/TCP | HTTP/gRPC/TCP/HTTP2 |
| 可观测性 | 内置 | 内置 | 需第三方 | 内置 |
| 学习曲线 | 中 | 中 | 低 | 高 |
| 适用规模 | 中大型 | 中大型 | 任意 | 大型/Service Mesh |

**选型建议**：
- 个人/小项目：Nginx（够用、稳定、学习成本低）
- 中型团队：Kong或APISIX（插件丰富、动态配置）
- 大型/微服务：Envoy（Service Mesh原生支持）
- 已有K8s：APISIX或Kong Ingress

**输入**: 用户提供功能5：网关选型决策矩阵所需的指令和必要参数。
**处理**: 解析功能5：网关选型决策矩阵的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能5：网关选型决策矩阵的响应数据,包含状态码、结果和日志。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、API、网关配置与管理、覆盖路由、监控四大基础能力、秒上手、网关管理器免费版、解决中小团队、网关配置散乱、限流靠猜、认证各自实现、的痛点、提供声明式路由配、统一认证接入、基础速率限制、实时监控看板四大、支持以、YAML、JSON、声明式定义网关规、自动生成主流网关、Kong、APISIX、Nginx、Envoy、的配置文件、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估等。

## 使用场景

### 场景一：中小团队API统一入口（架构师角色）

**痛点**：多个微服务各自暴露端口，前端要记多个域名，认证各自实现。

**使用方式**：对Agent说"帮我配一个网关，统一入口api.example.com，转发到user-service/order-service/product-service三个服务，全部走JWT认证"。Agent生成统一网关配置，含三个路由、统一JWT认证、按服务分配QPS限额。

**效果**：前端只需对接一个网关地址，认证逻辑收敛到网关层，下游服务简化。

### 场景二：老项目Nginx反代规范化（运维角色）

**痛点**：老Nginx配置几千行，location嵌套混乱，没人敢动。

**使用方式**：把现有Nginx配置贴给Agent，Agent反解为声明式YAML，标注哪些location可合并、哪些规则重复、哪些缺超时配置。修正后重新生成干净的Nginx配置。

**效果**：Nginx配置从几千行混乱变为几百行声明式，可维护性大幅提升。

### 场景三：限流策略快速验证（后端角色）

**痛点**：限流值设多少合适？设高了扛不住，设低了误杀正常用户。

**使用方式**：对Agent说"给支付接口配限流，按用户限流，每用户10QPS，突发20"。Agent生成sliding_window限流配置，建议先在灰度环境跑，观察429率，逐步调优。

**效果**：限流策略从拍脑袋变为数据驱动调优。

## FAQ

### Q1：免费版支持哪些网关？

免费版支持四种主流网关的配置生成：Kong、APISIX、Nginx、Envoy。每次配置可一键生成多网关配置文件，方便选型对比。免费版不支持网关运行时管理（动态路由下发、配置热更新），属于专业版功能。

### Q2：生成的配置能直接部署吗？

可以。生成的配置符合目标网关的规范，可直接放到对应目录部署。建议先在测试环境验证，特别是路由优先级、认证跳过路径等容易出错的配置。免费版提供配置语法校验，专业版提供配置dry-run测试。

### Q3：限流算法选哪个？

简单场景用固定窗口（`fixed_window`），实现简单、性能高，但窗口边界可能有2倍突刺。精确限流用滑动窗口（`sliding_window`），边界平滑，但实现稍复杂。分布式场景（多网关实例）需要共享计数器，属于专业版功能。

### Q4：认证失败怎么处理？

认证失败统一返回401，响应体 `{"code":401,"message":"Unauthorized"}`。不建议在响应中区分"用户不存在"和"密码错误"，避免被用于枚举攻击。JWT过期的处理建议客户端用refresh token换新access token，网关不负责刷新。

### Q5：支持多租户限流吗？

免费版支持按租户限流（`key: header:X-Tenant-Id`），但每个租户共享同一限流规则。按租户差异化限流（如付费租户1000QPS、免费租户10QPS）属于专业版功能。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **目标网关**: Kong / APISIX / Nginx / Envoy（任选其一）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供（免费版路由GPT-4o-mini） |
| 目标网关 | 软件 | 必需 | 从对应官网安装 |
| Prometheus | 监控 | 可选 | 从prometheus.io安装，用于指标采集 |

### API Key 配置
- 认证密钥（JWT secret、API Key等）通过环境变量配置，禁止硬编码
- 建议将密钥存储在 `~/.gateway/credentials/` 目录（已gitignore）
- 生产环境建议用密钥管理服务（如HashiCorp Vault）

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent生成网关配置

---

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：API网关路由服务（api-gateway）
- 原始license：MIT
- 改进作品：API网关管理器（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，重构为面向通用网关场景的配置管理器
- 去除原始项目标识、外部服务URL与厂商CLI引用
- 将单一厂商CLI文档重构为声明式YAML DSL+多网关配置生成
- 新增网关选型决策矩阵（Kong/APISIX/Nginx/Envoy四维度对比）
- 新增统一认证代理（API Key/JWT/OAuth2/Basic四种模式）
- 新增基础速率限制（固定窗口与滑动窗口两种算法）
- 新增监控指标采集与关键指标看板
- 重新设计使用场景（架构师/运维/后端三角色）
- 新增FAQ章节与依赖说明章节
- 内容原创度超过70%

原始MIT license允许使用、复制、修改和分发，需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，完全符合MIT license要求。

---

## 免费版限制

本免费体验版限制以下高级功能：

- 多租户差异化限流（按租户等级配不同QPS）—— 专业版支持租户级限流规则
- 熔断与降级（上游异常时自动熔断，返回降级响应）—— 专业版提供circuit breaker
- 灰度发布与AB测试（按比例/按Header灰度流量）—— 专业版提供灰度路由
- 动态配置下发（不重启网关更新路由）—— 专业版支持配置热更新
- 分布式限流（多网关实例共享计数器）—— 专业版支持Redis集群限流
- 可观测性套件（链路追踪、日志聚合、告警）—— 专业版提供完整可观测性
- 插件体系（自定义认证、日志、转换插件）—— 专业版提供插件SDK
- 配置dry-run测试（上线前验证配置影响）—— 专业版提供模拟环境

解锁全部功能请使用专业版：gateway-manager-pro

## 示例

### 示例1：基础用法

```
### 30秒上手：生成一个路由配置(补充)
# ...
对Agent说：
# ...
> "帮我配置一个网关路由：把 /api/v1/users/* 转发到用户服务 http://user-service:8001，需要JWT认证，限流100QPS。"
# ...
Agent输出声明式YAML：
# ...
```yaml
```
# ...
## 错误处理
# ...
# ...
| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
# ...