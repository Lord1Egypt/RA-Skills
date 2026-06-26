# dida365-openapi

基于滴答清单官方 OpenAPI 和 OAuth2 的任务管理 Skill，直连 dida365.com，不经过任何第三方服务，你的数据只在本地和滴答清单服务器之间传输。零第三方依赖，纯 Python 标准库实现。完整覆盖项目与任务的增删改查、完成、移动、筛选，支持标签、提醒、重复规则等丰富功能，并内置输入验证和灰色区域防护，确保每次 API 调用都安全可靠。

## 功能概览

告诉你的 agent 一句话，剩下的它来搞定：

- "看看我有哪些项目" — 列出所有项目
- "看看我有哪些任务" — 列出所有任务
- "帮我建个任务：买牛奶" — 在收集箱快速创建任务
- "把买牛奶标记为完成" — 完成任务
- "看看收集箱里有什么任务" — 查看任务列表
- "帮我查一下这周完成了哪些任务" — 已完成任务回顾
- "把这个任务优先级设为高" — 更新任务属性
- "给这个任务加上「工作」标签" — 标签管理
- "把这个任务移到工作项目里" — 跨项目移动
- "这个任务设成每天重复" — 重复规则
- "提前 30 分钟提醒我" — 任务提醒
- "帮我建个新项目叫读书计划" — 项目创建
- "帮我删掉这个任务" — 任务删除
- "找一下标签是「工作」的任务" — 任务筛选
- ……

## 与 ClawHub 现有 Skill 的对比

ClawHub 上目前有 6 个同类 skill，以下是核心差异对比：

| 维度 | dida365-openapi（本 Skill） | dida-cli | dida365 (MCP) | dida365-cli | dida-coach | dida365-ticktick-agent | ticktick-official-cli |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **认证方式** | 官方 OAuth2 | OAuth PKCE | 依赖 MCP 服务端 | 浏览器 Cookie | 依赖 MCP 服务端 | 浏览器 Cookie | 官方 OAuth2 |
| **API 来源** | 官方 OpenAPI | 官方 OpenAPI | 未明确 | 私有 API | 依赖 MCP | 私有 API | 官方 OpenAPI |
| **标签写入** | 支持 | 不支持 | 仅筛选 | 支持（私有 API） | 仅筛选 | 支持（私有 API） | 不明确 |
| **提醒模式** | 完整支持 + 模式验证 | 不支持 | 不明确 | 支持 | 支持 | 支持 | 支持 |
| **重复规则** | RRULE 完整支持 + 模式验证 | 不支持 | 部分 | 支持 | 支持 | 支持 | 支持 |
| **输入验证** | 日期/优先级/提醒/重复规则全面验证 | 基础 flag 验证 | 字段级 | Zod 验证 | 语义级 | 无 | Pydantic 验证 |
| **灰色区域防护** | 主动屏蔽不安全的 API 行为 | 无 | 无 | 无 | 无 | 无 | 无 |
| **外部依赖** | 零依赖（纯 Python 标准库） | Node.js + npm | MCP 服务端 | Node.js + npm | Python + MCP 服务端 | Node.js + npm | Python + httpx/typer/pydantic |
| **参考文档** | 3 份完整文档（API 参考 + 认证 + 示例） | README | SKILL.md | README | 11 份提示词 + 3 份参考 | 无 | API 文档 |
| **API 稳定性** | 高（官方 API） | 高 | 未知 | 低（私有 API 随时可能变更） | 取决于 MCP 服务端 | 低（私有 API） | 高 |

> 以上对比基于各 skill 在本 skill 提交时的版本，各 skill 后续可能会有更新。

### 核心优势总结

1. **官方 API + 零依赖**：使用官方 OAuth2 认证和官方 OpenAPI，不依赖私有接口或第三方 MCP 服务端，纯 Python 标准库实现，无需 `npm install` 或 `pip install`
2. **全面的输入验证**：日期格式、优先级值、提醒触发器、重复规则在发送到 API 前全部本地验证，防止静默失败
3. **灰色区域防护**：滴答清单 API 存在一些未文档化的边界行为，例如某些提醒值会被静默忽略、无日期任务设置重复规则会被清除。本 skill 在 CLI 层主动拦截这些已知的不可靠操作，避免看似成功实则无效的调用，这是其他 skill 都没有的能力
4. **丰富的功能覆盖**：支持标签写入、任务类型设置、提醒模式、重复规则等能力，覆盖日常任务管理的全部场景

## 快速开始

### 1. 安装 Skill

```bash
clawhub install dida365-openapi
```

### 2. 确认 Python 版本

需要 Python 3.9 或更高版本：

```bash
python --version
```

### 3. 注册滴答清单 OAuth 应用

前往[滴答清单开发者平台](https://developer.dida365.com)，创建一个 OAuth 应用，获取 `client_id` 和 `client_secret`。

将 redirect_uri 设置为：`http://127.0.0.1:36500/callback`

### 4. 登录认证

```bash
cd ~/.openclaw/skills/dida365-openapi
python scripts/dida365.py auth login-local \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

在浏览器中打开 stderr 输出的 URL，完成授权后令牌会自动保存。

### 5. 验证连接

```bash
python scripts/dida365.py project data --project-id inbox
```

看到收集箱数据即表示配置成功。之后就可以直接让 agent 帮你操作滴答清单了。

## Agent 调用示例

你只需用自然语言和 agent 对话，agent 会在后台自动转换为以下 CLI 命令执行：

```bash
# "看看我有哪些项目"
python scripts/dida365.py project list

# "帮我建个任务：买菜"
python scripts/dida365.py task create --project-id inbox --title "买菜"

# "帮我查一下这周完成了哪些任务"
python scripts/dida365.py task completed \
  --start-date "2026-03-16T00:00:00+0800" \
  --end-date "2026-03-22T23:59:59+0800"

# "找一下标签是「工作」的任务"
python scripts/dida365.py task filter --tag-json '["工作"]'
```

## Skill 结构

```
dida365-openapi/
  SKILL.md                       # Skill 定义（OpenClaw frontmatter + agent 指令）
  scripts/
    dida365.py                   # CLI 入口
    dida365_lib/
      __init__.py
      cli.py                     # 命令解析、输入验证、所有端点处理
      client.py                  # API 客户端封装
      auth.py                    # OAuth2 认证流程
      http.py                    # HTTP 请求层（基于 urllib）
      config.py                  # 配置加载与持久化
      common.py                  # 通用工具函数
      errors.py                  # 结构化错误定义
  references/
    api-reference.md             # 字段定义、枚举值、已确认的模式
    auth-and-config.md           # OAuth 流程、配置优先级、环境变量
    examples.md                  # 常见工作流的命令示例
```

## 工作原理

这个 skill 是纯 API 封装，不包含业务逻辑。Agent 读取 `SKILL.md` 中的指令，通过 `python scripts/dida365.py <resource> <action> [flags]` 调用滴答清单 API。所有命令以结构化 JSON 输出到 stdout，错误输出到 stderr。

CLI 会在本地验证输入（日期格式、优先级值、提醒模式），并屏蔽已知的灰色区域 API 行为，确保操作可预期。
