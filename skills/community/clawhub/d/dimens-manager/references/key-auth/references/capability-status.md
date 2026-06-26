# dimens-manager Key 鉴权章节 能力状态说明

## 1. 文档目标

这份文档专门回答：

`dimens-manager/references/key-auth/overview.md` 里哪些能力已经有 CLI 命令，哪些仍然只是 server 或 web 侧能力。

如果不把这层写清楚，Skill 很容易把“接口存在”误写成“CLI 已完全封装”。

---

## 2. 三种状态口径

| 状态 | 含义 | 输出要求 |
| --- | --- | --- |
| `已封装` | 当前已有 CLI 命令 | 可以直接给命令案例 |
| `server-only` | 当前只有后端接口或服务入口 | 只能给接口案例，不能伪装成 CLI 能力 |
| `部分对齐` | CLI 有上游或下游能力，但不能等同于完整 Key 管理能力 | 必须提示边界 |

---

## 3. 当前 Key 鉴权能力状态

### 3.1 已封装

当前最明确、且已经由 `dimens-cli` 封装的能力是：

| 能力 | CLI 命令 | 说明 |
| --- | --- | --- |
| API Key 登录换 token | `dimens-cli auth api-key-login` | 当前最稳定的 CLI 入口 |

### 3.2 server-only

下面这些能力目前仍主要是 server 或 web 侧能力：

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 创建 API Key | `server-only` | CLI 尚未完整封装 Key 管理命令 |
| 查询 Key 列表 | `server-only` | 主要仍由 web / 接口提供 |
| 启用 / 禁用 Key | `server-only` | 仍以接口方式为主 |
| 删除 Key | `server-only` | 仍以接口方式为主 |
| 重置 Secret | `server-only` | 明文 secret 仍主要在接口返回中处理 |
| 登录日志审计 | `server-only` | 主要用于管理界面和排查 |

### 3.3 部分对齐

下面这些现象最容易被误判：

| 现象 | 为什么只是部分对齐 |
| --- | --- |
| `api-key-login` 成功，就以为完整 Key 管理能力都 CLI 化了 | 目前 CLI 主要只收了“登录换 token”这一条 |
| 登录后能访问 `/app/*`，就以为 API Key 有独立权限体系 | 实际仍然复用现有用户权限，不是新平台 |

---

## 4. Skill 输出要求

当用户问“这个 Key 能力 CLI 有没有”时，建议固定按下面顺序回答：

1. 先说明当前属于 `已封装 / server-only / 部分对齐` 哪一类。
2. 如果没有 CLI，就给真实接口案例，不要伪装成命令能力。
3. 如果只是部分对齐，要明确这是“登录链路已命令化”，不是“Key 管理平台已命令化”。

---

## 5. 与其他 references 的关系

建议按下面顺序组合使用：

1. 先看 `examples.md`，确认真实接口和命令入口。
2. 再看本文件，确认当前能力状态。
3. 如果问题涉及边界和对接方式，再看 `integration-boundaries.md`。
