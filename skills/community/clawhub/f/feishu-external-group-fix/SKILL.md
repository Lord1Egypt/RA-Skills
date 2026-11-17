---
name: feishu-external-group-fix
description: 诊断并修复飞书自建应用/智能体机器人无法加入外部群的问题。报错「不支持加入外部群」或群里搜不到机器人时：先用 API 自检（tenant_access_token→机器人能力→列群→发消息）定位缺什么，再走开放平台「创建版本→对外共享→允许被添加到外部群→申请发布（需管理员审核）」修复，或改用零审核的内部群快捷路径。Use when a Feishu custom app bot fails to join a group, shows "不支持加入外部群", is unsearchable in group bot list, or when configuring 对外共享/availability/publish version on the Feishu open platform.
---

# feishu-external-group-fix：飞书机器人加入外部群 · 排查与修复

适用症状：往群里添加自建应用机器人时报 **「添加群成员失败：XXX 不支持加入外部群」**；或群机器人列表里**搜不到**你的应用。

## 根因速查

| 症状 | 根因 | 修复 |
|---|---|---|
| 报错「不支持加入外部群」 | 群是**外部群**（含外部联系人），应用「对外共享」未开启 | 走下面的主修复路径 |
| 群里搜不到机器人 | 应用**未发布版本** / **可用范围**不含你 / 机器人能力未开 / 客户端缓存 | 见「其他排查点」 |
| 报错缺权限 99991672 | 应用缺 scope | 按报错里的直链开通后**重发版本** |

## 第一步：API 自检（2 分钟，先搞清缺什么）

```bash
# 1. 换取租户凭证（app_id/app_secret 来自开放平台「凭证与基础信息」页）
curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}'
# → {"code":0, "tenant_access_token":"t-...", "expire":7200}

TOKEN=t-xxxx
# 2. 机器人能力 + 启用状态（失败=没开机器人能力）
curl -s -H "Authorization: Bearer $TOKEN" https://open.feishu.cn/open-apis/bot/v3/info

# 3. 列出机器人在哪些群（code=0 说明有 im:chat 类权限；群数量=0 说明还没进任何群）
curl -s -H "Authorization: Bearer $TOKEN" "https://open.feishu.cn/open-apis/im/v1/chats?page_size=20"

# 4. 发消息权限验证（先建个测试群拿到 chat_id 再发；230001=content 不是 JSON 字符串，用程序 json.dumps 二次编码）
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"test\"}"}' \
  "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
```

经验：错误信息很具体——`99991672 Access denied` 会直接给出开通 scope 的直链（`https://open.feishu.cn/app/{app_id}/auth?q=...`）；`40004` = 通讯录类权限缺失。

## 第二步：主修复路径（开放平台网页操作）

> 入口 `https://open.feishu.cn/app/{app_id}/version`，登录用二维码（豆包/飞书 App 扫）。

1. **创建版本**（版本号自动递增，如 1.0.0 → 1.0.1）
2. 找到 **「对外共享」** 区块 → 勾选 **「允许机器人被添加到外部群中使用」**（按需决定是否勾「允许外部用户与机器人单聊」，一般不勾）
3. 勾选后会出现 **「申请理由」** 必填框——写清用途（如：个人 RSS 推送机器人，需推送到自己所在的外部群）
4. **保存** → 弹窗 **「申请线上发布」** 提交
5. ⚠️ **对外共享不免审**：必须等 **企业管理员** 在管理后台/客户端审批通过后才生效（普通修改在可用范围≤5人时免审，开了对外共享就要审）
6. 生效后客户端**完全退出重开**再重试拉群（配置有缓存）

## 快捷替代：内部群（零审核、立即可用）

如果推送场景不强制要求外部群（RSS 提醒、个人通知类基本都不需要）：

**建一个普通群（只拉本组织成员）→ 群设置 → 群机器人 → 添加机器人 → 搜应用名**。

内部群只要「已发布 + 可用范围包含你 + 机器人能力已开」就能加，**不需要对外共享、不需要审核**。

## 其他排查点（搜不到机器人时逐项过）

- **应用能力** 页：是否有「机器人」能力
- **版本管理与发布** 页：是否存在状态为「已发布」的版本（光保存不发布=不生效）
- 可用范围：部分成员模式下，你自己要在成员列表里
- 可用范围是空的/被清空：重新编辑成员，保存后**重新发布一版**
- 客户端缓存：完全退出飞书客户端重开（刚发布的配置几分钟内可能搜不到）
- 想强制刷新配置：原样重发一个新版本（小租户免审秒生效）

## 浏览器自动化操作开放平台的坑

用 agent 控制浏览器操作 open.feishu.cn 时：

- **Playwright locator 点击大量超时**（按钮/复选框即使 snapshot 里存在也点不动）→ 改用 **截图定位 + CUA 坐标点击**，点完截图确认状态
- 创建版本页很长，对外共享区块要往下滚
- 提交发布有两次确认弹窗，第二次弹窗出现时页面状态可能滞后，等 2~3 秒再判断
