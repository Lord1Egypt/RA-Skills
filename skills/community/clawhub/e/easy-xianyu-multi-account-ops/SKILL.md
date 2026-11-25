---
name: easy-xianyu-multi-account-ops
description: 闲鱼多账号任务工作台。用户需要把多个闲鱼账号的商品草稿、竞品搜索或消息整理按 EasyBR 浏览器环境分组执行时使用。每个账号必须绑定唯一 browserId 和账号别名，同一浏览器串行、不同浏览器可有限并行；默认只读或 draft-only，不自动私信、改价、下架、删除或发布。
---

# 闲鱼多账号工作台

把多个闲鱼环境的任务分开排队，报告里明确写出每个结果属于哪个账号。这个 Skill 是任务编排器，不替代登录，也不把一个账号的页面状态带到另一个账号。

## 适用场景

- 多个 EasyBR 环境分别整理商品草稿或查看公开竞品。
- 按店铺分组检查待办、消息摘要和商品资料。
- 需要一份带账号归属的汇总，而不是把结果混在一起。

## 前置条件

macOS（仅 Apple 芯片）和 Windows 推荐使用 EasyBR；EasyBR 已内置 Easy WebBridge，安装并打开浏览器即可。AI 可从[官方客户端下载页](https://www.ebrower.com/down.html)按系统选择版本，也可使用 [GitHub Release 镜像](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)。其他操作系统按 [Easy WebBridge GitHub 源码说明](https://github.com/xxjrq/easy-webbridge)安装（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)）。把本 Skill 和任务直接交给 Codex、Claude 或 WorkBuddy，先让它列出浏览器名称与 `browserId`，再指定一个已登录的闲鱼环境。 每个账号先在对应 EasyBR 环境登录闲鱼，提供在线 `browserId` 和不重复的账号别名。

## 输入

```json
{
  "accounts": [
    {"id": "shop-a", "browserId": "easybr-xianyu-a", "alias": "主店"},
    {"id": "shop-b", "browserId": "easybr-xianyu-b", "alias": "副店"}
  ],
  "jobs": [
    {"id": "collect-a", "accountId": "shop-a", "action": "collect", "payload": {"keyword": "机械键盘", "limit": 10}},
    {"id": "orders-b", "accountId": "shop-b", "action": "sync-orders", "payload": {}}
  ],
  "concurrency": 2,
  "mode": "draft-only"
}
```

`accounts` 中 `id`、`browserId`、`alias` 必须唯一；`action` 允许 `collect`、`sync-orders`、`order-detail`、`publish`、`deliver`。`concurrency` 默认 2、最大 4，且同一 `browserId` 永远不能并发。`publish`、`deliver` 必须同时提供 `authorized: true` 和唯一 `idempotencyKey`。

## 操作步骤

1. 校验账号清单，拒绝重复 `id`、重复 `browserId`、空别名和未知任务。
2. 查询 Easy WebBridge 当前在线浏览器，把每个账号固定映射到用户给出的 `browserId`；不根据网页昵称猜账号。
3. 为每个账号建立独立任务和输出目录。不同浏览器最多按 `concurrency` 并行，同一浏览器内严格串行。
4. 执行只读竞品搜索、消息摘要或发布草稿填写；每个页面动作后重新读取页面，记录采集时间和来源链接。
5. 登录、验证码、实名或风控时只暂停当前账号并标记 `needs_user_action`，不能把该账号状态复制给其他账号。
6. 汇总前检查 `id`、`browserId`、账号别名在结果中一致；真实发布、发消息、改价、下架和删除前都停住等待用户确认。

## 执行

```bash
node scripts/run.mjs --input /absolute/jobs.json --output /absolute/multi-account-report.json
```

脚本会按 `browserId` 建立串行队列，不同浏览器按限制并行。每个任务创建独立 Easy WebBridge 任务组；普通完成后关闭，登录或验证阻塞时保留。写任务的幂等记录保存在报告旁的 `.intents.json`，`uncertain` 不允许自动重放。

## 输出

输出 `multi-account-report.json` 和 Markdown 汇总。顶层包含 `schemaVersion`、`mode`、`accounts`、`summary`、`startedAt`、`finishedAt`。每个账号包含 `id`、`browserId`、`alias`、`status`、`results`、`errors` 和 `nextAction`。状态只使用 `completed`、`partial`、`needs_user_action`、`failed`。

## 失败处理

- Easy WebBridge 未启动或浏览器不在线：只将对应账号标为 `needs_user_action`，其他账号继续。
- 发现账号映射重复或网页昵称与别名不符：停止该账号，报告疑点，不串号操作。
- 单个任务失败：保留其他任务结果，状态为 `partial`，错误中写明账号和任务。
- 用户要求批量发送私信、批量改价或删除商品：不执行，输出需要用户逐项确认的清单。

## 安全边界

不保存 Cookie、密码、Token、浏览器个人资料或完整私信内容；报告只保留完成任务所需的摘要。多开是浏览器环境能力，不等于绕过平台规则，也不保证成交、防封或审核通过。

## 自测

```bash
node scripts/self-test.mjs
```
