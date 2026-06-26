---
name: dimens-manager-key-auth
slug: dimens-manager-key-auth
description: 用于维表智联 API Key / API Secret 登录换取 token、第三方接入边界和 Key 权限链路排查。
version: 1.0.0
author: 方块智联工作室
tags: [auth, api-key, token, integration, dimens-cli]
---

# dimens-manager Key 鉴权章节

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 这是登录方式扩展，不是新开放平台
- ✅ API Key 登录成功后返回的是现有用户 token，不是新权限体系
- ✅ 第三方系统换到 token 后，调用的仍是现有 `/app/*` 接口
- ✅ `apiSecret` 只会在创建成功或重置成功时返回一次，不能从列表接口反查
- ✅ API Key 的可见权限仍然继承其绑定用户本身的权限
- ✅ 处理 API Key 问题时，必须区分“Key 本身是否有效”和“用户是否本来就有权限”

## 命令维护表

| 命令 | 作用 | 必填参数 | 常用可选 | 细节说明 |
| --- | --- | --- | --- | --- |
| `dimens-cli auth api-key-login` | 使用 API Key / Secret 换取登录 token | `apiKey`, `apiSecret` | `baseUrl` | 这是最关键的 CLI 登录链路，成功后复用的仍是现有用户 token |
| `api_key_create` | 创建 API Key | `name` | `expireTime`, `remark`, `ipWhiteList` | 创建成功后只返回一次明文 `apiSecret`，要立即保存 |
| `api_key_list` | 查询 API Key 列表 | `token` | `status`, `page`, `size` | 列表不返回明文 secret，只用于查看状态和元数据 |
| `api_key_status` | 启用或停用 API Key | `id`, `status` | - | 状态变化会直接影响登录是否成功 |
| `api_key_delete` | 删除 API Key | `id` | - | 删除后不能继续登录，属于不可逆的使用中止 |
| `api_key_reset_secret` | 重置 Secret | `id` | - | 成功后会返回新的明文 secret，旧 secret 即失效 |
| `api_key_log_page` | 查询 API Key 登录日志 | `id` 或 `apiKey` | `page`, `size` | 用于审计和排查登录失败原因 |

### 强调细节

- Key 登录成功只说明换 token 成功，不代表这个用户对目标团队、项目、表格、报表天然有权限。
- `apiSecret` 只会在创建或重置时返回一次，列表接口拿不回来，不要误判为数据丢失。
- 处理 Key 问题时先区分“Key 是否有效”和“用户本身是否有权限”，这两层不要混。
- 这个技能主要是认证入口，不是资源更新链；真正进入项目、表格、报表更新时，仍要遵循“拿数据 -> 改数据 -> 更新数据”的业务更新流程。

## 核心约束

### 1. 定位边界

- API Key 能力是现有登录体系的扩展
- 不新增新的权限平台
- 不新增新的开放资源模型
- 不绕开现有用户权限

### 2. 安全边界

- 服务端不明文存储 `apiSecret`
- `apiSecret` 使用哈希保存
- 列表接口不返回明文 `apiSecret`
- 明文只在创建和重置时出现一次

### 3. 登录校验边界

登录时至少会校验：

1. API Key 是否存在
2. 是否启用
3. 是否过期
4. 绑定用户是否存在且启用
5. Secret 是否匹配
6. 如果配置了 IP 白名单，当前 IP 是否允许

### 4. 权限边界

- API Key 没有独立权限集
- 换出的 token 权限完全继承所属用户
- 如果第三方系统拿到 token 后访问受限，优先查用户原始权限，而不是先怀疑 Key 体系

### 5. 数量边界

- 当前规则是同一用户最多创建 10 个 API Key
- 该限制按 `userId` 计算，不绑定团队和项目

## 必查文档

| Skill / references | 作用 | 什么时候必须看 |
| --- | --- | --- |
| `dimens-manager/references/team/overview.md` | 团队与项目权限的上游隔离模型 | 分析换 token 后访问受限时建议看 |
| `dimens-manager/references/permission/overview.md` | 为什么换 token 成功后仍然可能没有资源权限 | 解释访问受限时建议看 |
| `references/login-flow.md` | Key 登录链路与 token 复用方式 | 处理 Key 登录时必须看 |
| `references/integration-boundaries.md` | 第三方调用边界 | 解释对接方式时必须看 |
| `references/capability-status.md` | 当前 Key 能力范围 | 判断当前支持范围时建议看 |
| `references/examples.md` | Key 登录和管理案例 | 需要直接举例时看 |

## 使用场景示例

### 场景 1：使用 API Key 登录

```bash
dimens-cli auth api-key-login \
  --api-key ak_xxx \
  --api-secret sk_xxx
```

执行成功后通常意味着：

- 本地 profile 写入 `token`
- 如果服务端返回 `refreshToken` 也会同步写入
- 后续 `project`、`sheet`、`row`、`ai` 等命令可以直接复用

### 场景 2：创建一个给第三方同步脚本使用的 API Key

```json
{
  "name": "同步脚本 Key",
  "expireTime": "2026-12-31 23:59:59",
  "remark": "用于报表同步"
}
```

注意：

- 创建成功后要立即保存返回的 `apiSecret`
- 列表接口无法再次取回明文

### 场景 3：解释“为什么登录成功了但接口还是没权限”

标准结论：

1. API Key 登录成功只说明换 token 成功
2. 不代表这个用户对目标团队、项目、表格、工作流天然有权限
3. 需要继续排查该用户本身的角色和资源授权

## 常见错误与排查

| 错误现象 | 根本原因 | 解决方案 |
| --- | --- | --- |
| `api-key-login` 失败 | Key 不存在、被禁用、已过期或 secret 不匹配 | 依次检查状态、过期时间、secret 与白名单 |
| 登录成功但访问 `/app/*` 仍然报无权限 | 用户本身没有对应资源权限 | 检查用户角色、团队成员关系、项目授权 |
| 创建后找不到 `apiSecret` | `apiSecret` 只返回一次 | 需要重置 Secret 才能拿到新的明文 |
| 第三方环境可用，本地不可用 | IP 白名单限制或 baseUrl 不一致 | 检查 IP 白名单和当前环境地址 |
| 一个用户创建不了新的 Key | 达到单用户 10 个上限 | 清理旧 Key 或停用不再使用的 Key |

## 参考文档

- `references/login-flow.md`
- `references/integration-boundaries.md`
- `references/capability-status.md`
- `references/examples.md`
- 如需查看整个 Skill 体系的能力总览，请返回 `dimens-cli/skills/README.md`
