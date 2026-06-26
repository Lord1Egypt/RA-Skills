---
name: feishu-recall-message
description: 撤回飞书群消息。以用户身份撤回（recall）飞书群聊或单聊中的消息。群主/管理员可撤回任意成员消息，普通成员只能撤回自己的消息。支持单条撤回、批量撤回、按时间范围撤回。触发词：撤回消息、recall message、删除群消息、recall、撤回。
---

# 飞书群消息撤回

使用 `feishu_im_user_message` 工具的 `delete` action 以用户身份撤回消息。

## 前置条件

- 已完成飞书用户 OAuth 授权（撤回操作需要用户身份）
- 应用已开通 `im:message` scope
- 群主/管理员可撤回群内任意消息；普通成员只能撤回自己的消息

## 撤回单条消息

```
feishu_im_user_message(action="delete", message_id="om_xxx")
```

可选参数 `need_notification`：设为 `true` 则群内显示"xxx 撤回了一条消息"通知。默认 `false`（静默撤回）。

## 撤回引用的消息

当用户引用某条消息说"撤回"时，从引用上下文获取 `message_id`，直接调用 delete。

## 批量撤回

1. 用 `feishu_im_user_get_messages` 获取目标消息列表（支持 `start_time`/`end_time` 时间范围过滤，`chat_id` 指定群）
2. 过滤掉 `deleted: true` 的消息
3. 逐条调用 `feishu_im_user_message(action="delete", message_id="om_xxx")`
4. 汇报结果：成功数 / 失败数

## 按时间范围撤回

```
# 获取指定时间范围的消息
feishu_im_user_get_messages(
  chat_id="oc_xxx",
  start_time="2026-03-27T00:00:00+08:00",
  end_time="2026-03-27T23:59:59+08:00",
  page_size=50
)

# 逐条撤回未删除的消息
for msg in messages:
  if not msg.deleted:
    feishu_im_user_message(action="delete", message_id=msg.message_id)
```

注意：单次 `get_messages` 最多返回 50 条。如消息量大，需分页（用 `page_token`）。

## 注意事项

- 飞书限制：不支持撤回发出时间超过 1 天的消息
- 已删除的消息返回 `deleted: true`，跳过即可
- 撤回机器人消息也可用 `message` 系统工具的 `delete` action（无需用户授权）
- 撤回用户消息必须用 `feishu_im_user_message` 的 `delete`（需要用户 OAuth token）
