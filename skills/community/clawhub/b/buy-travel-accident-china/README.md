# 旅游意外险，适合旅行社代客出单 Agent API / Travel Accident Insurance Agent API

单一 Skill 入口：**仓库根目录 [`SKILL.md`](./SKILL.md)**（版本 2.0.4；ClawHub slug：`buy-travel-accident-china`，展示名：旅游意外险。）

---

## 文档结构

| 章节（均在 `SKILL.md` 内） | 说明 |
|---------------------------|------|
| **能力路由** | 用户意图 → 对应章节 |
| **发票 API 路径选择** | 路径 A：`/policies/.../invoice`；路径 B：`/broker/invoice` 等 |
| **鉴权与状态管理** | Base URL、Token、`.agent-state.json`、Schema 缓存、错误处理 |
| **咨询** | 产品列表、计划、保障对比、`POST /quote` |
| **投保** | 下单、支付、单证下载、路径 A 发票、智能填表、ASCII 支付二维码 |
| **退保** | 单张/批量退保、退费、broker 查询 |
| **开票经纪侧** | 路径 B：`/broker/invoice`、`invoiceQuery`、`redInvoice` |

鉴权、状态与 Schema 缓存已写在 **`SKILL.md`** 的「鉴权与状态管理」一节，无需其他附录文件。

---

## 中文说明

让 Agent 能够调用旅游意外险接口，完成从咨询报价到投保、退保、开票的完整业务流程，支持中国身份证智能填表。

### 前置条件

- Agent 具备 HTTP 请求能力（调用 `https://prod.uzyun.cn/api/agent/v1`）。
- 用户需拥有该平台账号（注册/登录后获得 token）。

### 安装与启用

**从 ClawHub 安装（推荐）**

- Slug：`buy-travel-accident-china`，展示名：**旅游意外险**
- 命令：`clawhub install buy-travel-accident-china`

**本地目录安装**

将本技能目录放入 OpenClaw 技能目录（如 `~/.openclaw/skills/` 或项目 `.openclaw/skills/`），**确保宿主加载根目录 `SKILL.md`**，重启 OpenClaw 或执行 `/reload-skills` 热加载。

### 权限说明

本技能仅描述如何调用外部 API，不包含额外系统权限。Agent 需能发起 HTTPS 请求并读写工作区内的 `.agent-state.json` 以持久化登录状态与常用人员信息；**短信验证码不写入状态文件**（登录为手机号 + 验证码，见 `SKILL.md`「鉴权」）。

---

## English

This skill enables the Agent to call the travel accident insurance API for the full flow: consultation and quoting, purchasing, surrender, and invoicing (policy-path and broker-path), with smart form-fill for Chinese ID cards.

### Single entrypoint

Use **[`SKILL.md`](./SKILL.md)** at the repository root as the only canonical skill document.

### Requirements

- Agent can make HTTP requests to `https://prod.uzyun.cn/api/agent/v1`
- User must have an account on the platform (token after register/login)

### Install and enable

**From ClawHub:** `clawhub install buy-travel-accident-china` (slug `buy-travel-accident-china`, display name **旅游意外险**).

**From a local copy:** place this folder in your OpenClaw skills directory and ensure the host loads the root **`SKILL.md`**, then restart or `/reload-skills`.
