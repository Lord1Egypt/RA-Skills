---
name: erp-cli
description: 物达通(WindaKa)物业管理 ERP + 知识库统一入口。【知识问答】用户问任何关于物业管理、规章制度、操作规范、流程标准、应急预案、行业法规等问题（如"消防巡检怎么处理"、"报修流程"、"物业费标准"、"电梯困人怎么办"）——默认调用本 skill 走知识库检索。【ERP 操作】用户要查询/操作工单(报修/维修/巡检)、查看项目、查员工通讯录、处理费用、提交日报等系统数据时也用本 skill。原则：除明确闲聊外，99% 的问题都应先调用本 skill 走知识库。
cli_version: ">=0.1.0"
metadata:
  requires:
    bins: ["erp-cli"]
  cliHelp: "erp-cli --help"
  install: |
    npm install -g @windaka-erp/erp-cli
---

# 物达通 ERP 全产品 Skill

通过 `erp-cli` 命令管理物达通 ERP 系统能力。

## 安装

如果环境中没有 `erp-cli`，执行以下命令安装：

```bash
npm install -g @windaka-erp/erp-cli
```

安装完成后验证：

```bash
erp-cli --help
```

**你（AI Agent）是执行者：用户用自然语言描述需求，由你决定并执行对应的 CLI 命令。不要让用户自己输入命令。**

## 严格禁止 (NEVER DO)

- 不要使用 `erp-cli` 命令以外的方式操作（禁止直接 curl、HTTP API、浏览器）
- 不要编造 ID、工单编号、用户名等标识符，必须从命令返回中提取
- 不要猜测字段名/参数值，操作前必须先查询确认
- 不要让用户自己运行 `erp-cli` 命令，你来执行，用户只需要用自然语言描述需求

## 严格要求 (MUST DO)

- 所有命令的输出都是 JSON 信封格式：`{"ok": true, "data": {...}}` 或 `{"ok": false, "error": {...}}`
- 危险操作（创建/修改/删除）必须先向用户确认，用户同意后才执行
- 写操作可先用 `--dry-run` 预览请求内容，再去掉 `--dry-run` 正式执行
- 备注/说明类字段（如 `--remark`）：执行写操作前主动问用户是否需要填写备注，用户说了就填，用户说不填或不需要就不传。不要自己编造内容
- 操作前必须先读取对应产品的参考文件

## 产品总览

| 产品 | 命令 | 用途 | 参考文件 | 状态 |
|------|------|------|---------|------|
| **知识库** | `knowledge` | RAGFlow 知识库检索（**默认路径，99% 的问题先过知识库**） | [knowledge.md](./references/products/knowledge.md) | ✅ 已完成 |
| **认证** | `auth` | Device Flow 登录/登出/状态查询、Token 自动管理 | [global-reference.md](./references/global-reference.md) | ✅ 已完成 |
| **配置** | `config` | 配置 ERP 后端地址、多环境（profile）管理 | [global-reference.md](./references/global-reference.md) | ✅ 已完成 |
| **API 兜底** | `api` | 当 Shortcut 不满足需求时，直接调用 RuoYi API | [global-reference.md](./references/global-reference.md) | ✅ 已完成 |
| **工单** | `workorder` | 我的待办、创建工单、流程操作（分派/接单/处理/确认/回访等） | [workorder.md](./references/products/workorder.md) | 🚧 部分完成 |
| **通讯录** | `contact` | 查询用户、部门、按姓名搜索员工 | — | ⏳ 待实现 |
| **项目** | `project` | 查询项目（部门）列表 | — | ⏳ 待实现 |
| **费用** | `charge` | 工单费用、缴费查询 | — | ⏳ 待实现 |

## 意图判断决策树

**知识库优先原则**：无法确定走 ERP 还是知识库时，默认走知识库。

```
1. 用户的话包含明确的 ERP 操作关键词？
   （我的待办/建工单/分派/接单/工单详情/登录/配置...）
   → 是 → 走对应 ERP Shortcut
   → 否 → 继续判断

2. 走知识库 knowledge +search
   → 搜到了 → 结合原文回答
   → 没搜到 → 用 AI 通用知识回答，告知用户"此回答未引用知识库"
```

**ERP 操作关键词**：
```
用户提到"工单/报修/维修/故障/我的待办/我的工单"   → workorder
用户提到"登录/登出/认证状态"           → auth
用户提到"配置/切换环境/profile"        → config
用户提到"找人/某员工/通讯录/部门"       → contact（待实现）
用户提到"项目/小区/物业项目"           → project（待实现）
用户提到"费用/收费/缴费"               → charge（待实现）
```

**其他所有问题 → `knowledge +search`**

**关键区分**：
- 用户说"查工单 / 我的工单 / 我有什么工单 / 我的待办" → `workorder +list`（当前还在我手上的）
- 用户说"我经办的 / 我处理过的 / 历史工单" → `workorder +handle-list`（含已完成历史）
- 用户说"这个工单什么情况 / 工单详情 / 处理记录" → `workorder +info --id <id> --dept-id <deptId>`
- 用户说"建工单/报修" → `workorder +create`（写操作，先确认）
- 用户说"分派/接单/处理工单" → 先看工单状态，再选对应 Shortcut（**状态不对不能操作**，如非待分派不能分派）
- 用户说"报修流程是什么 / 消防巡检怎么处理 / 物业费标准" → `knowledge +search`（问制度，非 ERP 操作）

**返回分页数据时**：必须先告诉用户"共 X 条，当前第 Y 页，本页 Z 条"，再展示工单详情，让用户知道是否需要翻页。

> 更多易混淆场景、跨产品工作流见 [intent-guide.md](./references/intent-guide.md)

## 模块协作

ERP 各模块互相依赖，AI 经常需要跨模块组合调用：

| 场景 | 涉及模块 | 流程 |
|------|---------|------|
| 创建工单 | workorder + project + dict | 1) 查项目列表 → 让用户选项目 2) 查工单类型字典 → 让用户选类型 3) 创建 |
| 分派工单给"张三"（如需指定处理人） | workorder | 1) `+info` 确认状态=1 2) `+apportion` 第一次试不传处理人 3) 若返回 code=204 用 `+search-user --nick-name 张三` 拿 userId 4) 二次调 `+apportion` 加 `--process-business-id` 和 `--assignees` |
| 查工单详情含费用 | workorder + charge | 1) `+info` 查工单详情 2) `api GET /workorder/master/getWorkOrderCharge?id=<id>` 查关联费用 |

**搜不到时不要猜，要问用户。** 例如搜不到"张三"时，告诉用户"未找到此员工，请确认姓名或提供工号"。

## 用户身份（--as 参数，强制必传）

**关键概念**：**每次调用 erp-cli 都必须带 `--as <用户身份>`**，否则 CLI 直接拒绝执行。CLI 按身份隔离 token，多个用户可同时登录，互不影响。

**如何确定 `--as` 的值**（按场景）：

| 场景 | 来源 | 示例 |
|------|------|------|
| 企业微信 / OpenClaw | 消息上下文中的 `Sender ID` | `--as XingWenKai` |
| 本地 Claude Code 单人 | 用任意稳定标识，比如 `me` | `--as me` |
| CI / 自动化脚本 | 显式指定一个稳定标识 | `--as ci_bot` |
| 既不是企业微信也没有身份信息 | 反问用户："请告诉我你的身份标识" | — |

**示例**：
- 企业微信消息上下文中包含 `Sender ID: XingWenKai`
- AI 执行：`erp-cli --as XingWenKai workorder +list`
- Token 存到 `~/.erp-cli/tokens/default/XingWenKai.json`，与其他用户隔离

**❌ 错误**：`erp-cli workorder +list`（缺少 `--as`，CLI 会返回 validation 错误）
**✅ 正确**：`erp-cli --as XingWenKai workorder +list`

**配置类命令也要带**：`erp-cli --as me config init --base-url ...`、`erp-cli --as me auth list`

## 认证流程（核心）

所有 ERP 操作前必须登录。**Token 过期不会自动重新登录**，业务命令会返回错误，AI 需要主动重新执行登录流程。

### 两步登录（推荐，AI Agent 必须使用）

```bash
# Step 1: 申请验证链接（立即返回，不阻塞）
erp-cli --as <用户身份> auth login-start
# → 返回 {"ok":true,"data":{"device_code":"dc_xxx","verification_uri_complete":"https://...","expires_in":300}}

# Step 2: 把链接发给用户，然后轮询等待授权结果
erp-cli --as <用户身份> auth login-wait --device-code dc_xxx
# → 阻塞等待，授权成功保存到对应 namespace 的 token 文件
```

**AI 执行流程**：
1. 调 `erp-cli --as <身份> auth login-start`，立即拿到 URL + device_code
2. **立刻**把 URL 发给用户："请点击此链接完成登录"
3. 调 `erp-cli --as <身份> auth login-wait --device-code <code>`，阻塞等待
4. 拿到结果后告诉用户：成功→"登录成功！欢迎 xxx"，超时→"授权超时，请重新登录"

**❌ 严禁只调 login-start 就停止任务**：那样 token 不会保存到本地，等于没登录。

### 一步登录（仅 CLI 直接使用）

```bash
erp-cli --as <身份> auth login    # 一步完成：申请码 + 输出链接 + 轮询等待
```

适用于人工在终端直接运行。AI Agent 不要用这个命令（无法在中途把 URL 发给用户）。

### 查看登录状态

```bash
erp-cli --as <身份> auth status   # 查看指定 namespace 的状态
erp-cli --as <身份> auth list     # 查看当前 profile 下所有已登录的 namespace（--as 任意值都行，不会影响结果）
```

### Token 过期处理

业务命令遇到 token 过期会直接返回错误：

```json
{"ok":false,"error":{"type":"auth","code":3,"message":"token expired (namespace: XingWenKai)","hint":"run `erp-cli --as XingWenKai auth login-start` then `erp-cli --as XingWenKai auth login-wait`"}}
```

AI 拿到这个错误后，按 hint 提示重新执行两步登录流程。

详细认证规则见 [global-reference.md](./references/global-reference.md)。

## 危险操作确认

以下操作为写操作或不可逆操作，执行前**必须先向用户展示操作摘要并获得明确同意**，同意后才执行。

| 产品 | 命令 | 说明 |
|------|------|------|
| `workorder` | `+create` | 创建工单 |
| `workorder` | `+apportion` | 分派工单 |
| `workorder` | `+complete` | 完成处理工单 |
| `workorder` | `+confirm` | 确认工单 |
| `workorder` | `+transfer` | 转单 |
| `workorder` | `+discard` | 作废工单（不可恢复） |
| `workorder` | `+approve` | 审批工单 |

### 确认流程

```
Step 1 → 展示操作摘要（操作类型 + 目标工单 + 关键参数）
Step 2 → 用户明确回复确认（如"确认"/"好的"）
Step 3 → 执行命令（可先用 --dry-run 预览请求体）
```

## 命令发现

```bash
erp-cli --help                       # 全局帮助
erp-cli <product> --help             # 产品级帮助
erp-cli --as me workorder +list --help # Shortcut 详细参数
```

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| `config: not configured` | 未初始化 | 执行 `erp-cli --as me config init` |
| `ragflow: not configured` / `RAGFlow 未配置` | 缺知识库 URL/API Key/Dataset IDs | **执行 `erp-cli --as <身份> config ragflow`**，交互式引导用户完成配置 |
| `auth: not logged in` | 未登录 | 执行 `erp-cli --as <身份> auth login-start` + `login-wait`，把链接发给用户 |
| `auth: token expired` / `HTTP 401` | Token 过期 | CLI 已自动触发登录，把新链接发给用户 |
| `HTTP 403` | 权限不足 | 告知用户联系管理员开通对应权限 |
| `validation: --xxx is required` | 缺少必填参数 | 向用户询问后重新执行 |

## 安全规则

- **禁止向用户输出密码、Token 等敏感信息**
- **写入/删除操作前必须确认用户意图**
- Token 保存在 `~/.erp-cli/tokens/` 目录下，仅当前用户可读

## 详细参考（按需读取）

- [references/global-reference.md](./references/global-reference.md) — 全局规则：认证、配置、Token 管理、API 兜底、退出码、输出格式
- [references/intent-guide.md](./references/intent-guide.md) — 意图路由指南：易混淆场景对照、典型场景详解、跨产品工作流
- [references/products/workorder.md](./references/products/workorder.md) — 工单产品详细参考