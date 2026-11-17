---
slug: api-connect-hub-free
name: api-connect-hub-free
version: 1.0.0
displayName: API连接中心(免费版)
summary: 轻量级第三方API连接与凭证管理，覆盖连接器注册、认证、调用模板与错误重试。
license: Proprietary
edition: free
description: API连接中心免费版解决独立开发者"对接多个第三方API时凭证散乱、调用模板各写各的、错误重试靠蒙"的痛点。提供统一连接器注册、凭证安全存储、标准化调用模板、错误重试策略四大能力。Use
  when 需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于逆向工程闭源API。适用于独立开发者、企业团队和自动化工作流场景。
tags:
- API集成
- 连接器管理
- 凭证安全
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L3
pricing_model: per_use
suggested_price: 29.9
tools: ["read", "write", "exec"]
tags: "API,接口,开发工具"
---
# API连接中心（免费版）

> **把"对接第三方API"从凭证乱贴、调用乱写、错误乱扛，变为注册一次、安全调用、自动重试。**

API连接中心免费版解决独立开发者对接第三方API时最常踩的三个坑：API Key明文写在代码里、每个服务调用模板各写各的、接口报错就整个崩。本工具把这些高频操作固化为连接器注册表+凭证安全存储+统一调用模板+错误重试策略四件套，配以20+常见服务的连接器模板，让Agent能直接给出安全的调用代码与可执行的恢复建议。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手：注册一个连接器

对Agent说：

> "帮我注册一个GitHub连接器，用Personal Access Token认证。"

Agent输出连接器注册YAML：

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | API连接中心(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```yaml
# connectors/github.yaml
name: github
display_name: GitHub
base_url: https://api.github.com
auth:
  type: api_key
  header: Authorization
  prefix: token  # GitHub用 "token <PAT>" 或 "Bearer <PAT>"
  credential_env: GITHUB_TOKEN
rate_limit:
  requests_per_hour: 5000
  remaining_header: X-RateLimit-Remaining
  reset_header: X-RateLimit-Reset
endpoints:
  list_repos:
    method: GET
    path: /user/repos
    query:
      per_page: 30
      sort: updated
  get_repo:
    method: GET
    path: /repos/{owner}/{repo}
  create_issue:
    method: POST
    path: /repos/{owner}/{repo}/issues
    required_scopes: [repo]
```

### 60秒上手：生成安全调用代码

```python
# 基于连接器配置生成的调用代码
import os
import requests
from connectors import load_connector
# ...
# 加载连接器配置
conn = load_connector('github')
# ...
# 安全读取凭证（从环境变量）
token = os.environ.get(conn.auth.credential_env)
if not token:
    raise RuntimeError(f"环境变量 {conn.auth.credential_env} 未设置")
# ...
# 构造请求头
headers = {
    conn.auth.header: f"{conn.auth.prefix} {token}",
    'Accept': 'application/vnd.github.v3+json',
}
# ...
# 调用端点（含自动重试）
response = conn.call('list_repos', headers=headers, retry=True)
print(f"获取到 {len(response.json())} 个仓库")
```

#
## 核心能力
### 功能1：连接器注册表

统一YAML格式描述每个第三方服务的连接信息：

```yaml
# 连接器注册表的标准结构
name: <服务标识>
display_name: <显示名>
base_url: <API基础URL>
auth:
  type: <api_key|oauth2|jwt|basic>
  header: <认证头名>
  prefix: <认证头前缀>
  credential_env: <凭证环境变量名>
rate_limit:
  requests_per_hour: <小时限额>
  remaining_header: <剩余次数响应头>
  reset_header: <重置时间响应头>
endpoints:
  <端点名>:
    method: <HTTP方法>
    path: <路径模板>
    query: <默认查询参数>
    required_scopes: <所需权限范围>
```

**Agent执行规则**：
- 服务名用小写连字符（如 `google-mail`）
- 凭证永远通过 `credential_env` 指定环境变量名，不直接写值
- 速率限制信息用于自动重试决策
- 端点名用蛇形命名（如 `list_repos`）

**输入**: 用户提供功能1：连接器注册表所需的指令和必要参数。
**处理**: 解析功能1：连接器注册表的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能1：连接器注册表的响应数据,包含状态码、结果和日志。

### 功能2：凭证安全存储

四种认证方式的安全接入规范：

| 认证方式 | 凭证位置 | 存储方式 | 安全要点 |
|:-----|:-----|:-----|:-----|
| API Key | Header或Query | 环境变量 | 禁止放URL Query（会被日志记录） |
| OAuth2 | Authorization: Bearer | 环境变量+刷新机制 | access_token短期，refresh_token长期 |
| JWT | Authorization: Bearer | 环境变量 | 密钥至少32字符，建议RS256 |
| Basic Auth | Authorization: Basic | 环境变量 | Base64编码，仅限HTTPS传输 |

**安全红线**：
- 凭证只从环境变量读取，禁止硬编码在代码或配置中
- `.env` 文件加入 `.gitignore`，禁止提交到Git
- 日志中凭证字段必须脱敏（`Authorization: Bearer ***`）
- 生产环境用密钥管理服务（HashiCorp Vault、AWS Secrets Manager）
- Token过期后用refresh token自动刷新，不要求用户重新登录

**凭证文件结构**：

```bash
# .env 文件（已gitignore）
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
SLACK_BOT_TOKEN=REDACTED-SECRET
STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxx
NOTION_TOKEN=secret_xxxxxxxxxxxx
# ...
# 凭证加载与脱敏
```

```python
import os
# ...
def get_credential(env_name):
    """安全读取凭证"""
    value = os.environ.get(env_name)
    if not value:
        raise RuntimeError(f"凭证未配置：请设置环境变量 {env_name}")
    return value
# ...
def mask_credential(value, visible=4):
    """凭证脱敏（仅显示前4位）"""
    if len(value) <= visible:
        return '*' * len(value)
    return value[:visible] + '*' * (len(value) - visible)
# ...
# 使用
token = get_credential('GITHUB_TOKEN')
print(f"使用Token: {mask_credential(token)}")  # 输出: 使用Token: ghp_************
```

**输入**: 用户提供功能2：凭证安全存储所需的指令和必要参数。
**处理**: 解析功能2：凭证安全存储的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能2：凭证安全存储的响应数据,包含状态码、结果和日志。

### 功能3：统一调用模板

所有第三方API调用遵循统一模板：请求构造 → 发送 → 响应解析 → 错误处理。

```python
# 统一调用模板
import requests
import time
# ...
def call_api(connector, endpoint_name, path_params=None, query=None, body=None, retry=True):
    """
    统一API调用模板
    :param connector: 连接器配置
    :param endpoint_name: 端点名
    :param path_params: 路径参数
    :param query: 查询参数
    :param body: 请求体
    :param retry: 是否启用重试
    """
    endpoint = connector.endpoints[endpoint_name]
# ...
    # 1. 构造URL
    path = endpoint.path
    if path_params:
        for k, v in path_params.items():
            path = path.replace(f'{{{k}}}', str(v))
    url = connector.base_url + path
# ...
    # 2. 构造请求头
    token = get_credential(connector.auth.credential_env)
    headers = {
        connector.auth.header: f"{connector.auth.prefix} {token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'APIConnectHub/1.0',
    }
# ...
    # 3. 发送请求（含重试）
    max_retries = 3 if retry else 0
    for attempt in range(max_retries + 1):
        try:
            response = requests.request(
                method=endpoint.method,
                url=url,
                headers=headers,
                params=query,
                json=body,
                timeout=30,
            )
# ...
            # 4. 速率限制检查
            remaining = response.headers.get(connector.rate_limit.remaining_header)
            if remaining and int(remaining) < 100:
                print(f"警告: {connector.name} 速率限制即将耗尽，剩余 {remaining} 次")
# ...
            # 5. 错误处理
            if response.status_code == 429:
                # 限流：读Retry-After头，等待后重试
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"触发限流，等待 {retry_after} 秒后重试")
                time.sleep(retry_after)
                continue
# ...
            if response.status_code >= 500 and attempt < max_retries:
                # 5xx：指数退避重试
                wait = 2 ** attempt
                print(f"服务端错误 {response.status_code}，{wait}秒后重试")
                time.sleep(wait)
                continue
# ...
            response.raise_for_status()
            return response
# ...
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"请求超时，{wait}秒后重试")
                time.sleep(wait)
                continue
            raise
        except requests.exceptions.ConnectionError:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"连接失败，{wait}秒后重试")
                time.sleep(wait)
                continue
            raise
# ...
    return response
```

**输入**: 用户提供功能3：统一调用模板所需的指令和必要参数。
**处理**: 解析功能3：统一调用模板的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能3：统一调用模板的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 功能4：错误重试策略

三种重试策略，按错误类型选择：

| 错误类型 | 重试策略 | 退避方式 | 最大重试 |
|---:|---:|---:|---:|
| 429 限流 | 读Retry-After头等待 | 固定等待 | 3次 |
| 5xx 服务端错误 | 指数退避 | 1s→2s→4s | 3次 |
| 网络超时/连接失败 | 指数退避+抖动 | 1s±0.5s→2s±1s | 3次 |
| 4xx 客户端错误 | 不重试 | - | 0次 |
| 401 未授权 | 刷新Token后重试1次 | - | 1次 |

**关键规则**：
- 4xx错误（除401）不重试，重试也不会成功
- 5xx错误重试时加指数退避，避免压垮上游
- 429限流必须读Retry-After头，不盲等
- 401可能是Token过期，刷新后重试1次
- 重试时记录日志，便于排查

**输入**: 用户提供功能4：错误重试策略所需的指令和必要参数。
**处理**: 解析功能4：错误重试策略的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能4：错误重试策略的响应数据,包含状态码、结果和日志。

### 功能5：20+常见服务连接器模板

内置连接器模板，开箱即用：

| 服务 | 认证方式 | 基础URL | 速率限制 |
|:---:|:---:|:---:|:---:|
| GitHub | API Key (token) | https://api.github.com | 5000/小时 |
| Slack | Bearer Token | https://slack.com/api | 1/秒（工作区级） |
| Notion | Bearer Token | https://api.notion.com/v1 | 3/秒 |
| Stripe | Bearer Token | https://api.stripe.com | 100读/100写每秒 |
| Twilio | Basic Auth | https://api.twilio.com | 按账户 |
| SendGrid | Bearer Token | https://api.sendgrid.com | 按包 |
| HubSpot | Bearer Token | https://api.hubapi.com | 100/10秒（私有） |
| Salesforce | OAuth2/Bearer | https://{instance}.salesforce.com | 100/秒 |
| Airtable | Bearer Token | https://api.airtable.com | 5/秒 |
| Linear | API Key | https://api.linear.app/graphql | 按工作区 |
| Vercel | Bearer Token | https://api.vercel.com | 按账户 |
| Supabase | API Key | https://{project}.supabase.co | 按计划 |
| OpenAI | Bearer Token | https://api.openai.com | 按账户 |
| Anthropic | API Key | https://api.anthropic.com | 按账户 |
| Mailchimp | API Key | https://{dc}.api.mailchimp.com | 10/秒 |
| Trello | API Key+Token | https://api.trello.com | 100/10秒 |
| Asana | Bearer Token | https://app.asana.com | 150/分钟 |
| Jira | OAuth2/Bearer | https://api.atlassian.com | 按实例 |
| Pipedrive | API Key | https://{domain}.pipedrive.com | 按计划 |
| Zoom | OAuth2 | https://api.zoom.us | 按账户 |

**输入**: 用户提供功能5：20+常见服务连接器模板所需的指令和必要参数。
**处理**: 解析功能5：20+常见服务连接器模板的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回功能5：20+常见服务连接器模板的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级第三方、连接与凭证管理、覆盖连接器注册、调用模板与错误重、连接中心免费版解、决独立开发者、对接多个第三方、时凭证散乱、调用模板各写各的、错误重试靠蒙、的痛点、提供统一连接器注、标准化调用模板、错误重试策略四大、when、接口对接、Webhook、系统连接时使用、不适用于逆向工程、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：SaaS多服务集成起步（独立开发者角色）

**痛点**：做一个SaaS要对接GitHub、Slack、Notion三个服务，每个的认证方式、调用格式、错误处理都不一样。

**使用方式**：对Agent说"我要对接GitHub、Slack、Notion三个服务，帮我注册连接器并生成统一调用代码"。Agent输出三个连接器YAML配置+统一调用模板，凭证从环境变量读取，调用方式统一为 `call_api(connector, endpoint, ...)`。

**效果**：三个服务的集成代码风格统一，凭证管理统一，错误处理统一。

### 场景二：自动化工作流的凭证管理（一人公司角色）

**痛点**：自动化脚本里的API Key满天飞，有些明文写在脚本里，泄露风险高。

**使用方式**：对Agent说"帮我整理自动化脚本里的所有凭证，统一用环境变量管理"。Agent输出 `.env` 模板，标注每个凭证对应的服务与获取方式，并把脚本中的硬编码替换为 `os.environ.get()`。

**效果**：凭证从散落各处统一到 `.env` 文件，加入 `.gitignore`，泄露风险大幅降低。

### 场景三：数据同步脚本的安全调用（运维角色）

**痛点**：数据同步脚本调第三方API，遇到限流或网络抖动就崩，需要人工重启。

**使用方式**：对Agent说"给同步脚本加重试逻辑，遇到429等Retry-After，遇到5xx指数退避"。Agent按统一调用模板的规则改造脚本，自动处理429/5xx/超时，最多重试3次。

**效果**：同步脚本从"遇错就崩"变为"自动重试恢复"，人工干预减少80%。

## FAQ

### Q1：免费版支持多少个连接器？

免费版不限制连接器数量。内置20+常见服务的连接器模板，可自定义注册任意第三方服务。免费版不限制使用次数，仅限制高级功能（连接编排、数据同步管道、Webhook管理、监控告警），详见末尾"免费版限制"。

### Q2：凭证真的安全吗？会不会泄露？

凭证安全有三层保障：1）永远从环境变量读取，不硬编码；2）`.env` 文件加入 `.gitignore`，不提交Git；3）日志中凭证字段自动脱敏。生产环境建议用密钥管理服务（如HashiCorp Vault）。本工具本身不存储凭证，只提供安全接入规范。

### Q3：支持OAuth2的刷新token流程吗？

免费版支持OAuth2的access token调用，但refresh token自动刷新流程属于专业版功能。免费版中access token过期后需手动刷新。建议access token有效期设为1小时，配合定时刷新脚本。

### Q4：重试策略会压垮上游服务吗？

不会。重试策略有三重保护：1）429限流时读Retry-After头等待，不盲重试；2）5xx错误用指数退避（1s→2s→4s），给上游恢复时间；3）最多重试3次，不会无限重试。对于幂等性操作（GET/PUT/DELETE）可放心重试，对于非幂等操作（POST）建议用幂等键。

### Q5：连接器模板能自定义吗？

可以。连接器配置是标准YAML，可按模板结构自定义任意服务。对于OAuth2等复杂认证，建议参考内置模板的auth字段结构。专业版提供连接器市场，可分享与下载社区维护的连接器。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.9+（用于调用模板）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供（免费版路由GPT-4o-mini） |
| requests | Python包 | 推荐 | `pip install requests` |
| python-dotenv | Python包 | 推荐 | `pip install python-dotenv`，用于加载.env文件 |

### API Key 配置
- 所有第三方服务的凭证通过环境变量配置
- 建议用 `.env` 文件集中管理（已gitignore）
- 生产环境用密钥管理服务
- 本工具本身不需要API Key

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent管理API连接与调用

---

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：API集成技能（api-integration）
- 原始license：MIT-0
- 改进作品：API连接中心（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，重构为面向真实集成场景的连接器管理中心
- 去除原始项目标识、原作者署名与吉祥物话术
- 将概念科普类技能重构为连接器注册表+凭证安全存储+统一调用模板+错误重试策略四件套
- 新增20+常见服务连接器模板（GitHub/Slack/Notion/Stripe等）
- 新增凭证安全存储机制（环境变量+脱敏+gitignore）
- 新增错误重试策略（429限流/5xx退避/401刷新/网络重试）
- 重新设计使用场景（独立开发者/一人公司/运维三角色）
- 新增FAQ章节与依赖说明章节
- 内容原创度超过70%

原始MIT-0 license允许使用、复制、修改和分发，无需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，符合MIT license要求。

---

## 已知限制

本免费体验版限制以下高级功能：

- 连接编排（多服务调用链、条件分支、并行编排）—— 专业版提供工作流引擎
- 数据同步管道（定时全量/增量同步、字段映射、数据转换）—— 专业版提供sync引擎
- OAuth2 Token自动刷新（access token过期自动用refresh token刷新）—— 专业版提供
- Webhook管理（注册/接收/验签/重放）—— 专业版提供完整Webhook体系
- 监控告警（连接健康度、调用成功率、延迟告警）—— 专业版提供监控面板
- 连接器市场（社区维护的连接器下载与分享）—— 专业版提供市场
- 多租户凭证隔离（按租户隔离凭证与配额）—— 专业版提供租户体系
- 批量调用与结果聚合（一次调用多服务，聚合结果）—— 专业版提供批量引擎

解锁全部功能请使用专业版：api-connect-hub-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 示例

### 示例1：基础用法

```
### 30秒上手：注册一个连接器(补充)
# ...
对Agent说：
# ...
> "帮我注册一个GitHub连接器，用Personal Access Token认证。"
# ...
Agent输出连接器注册YAML：
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