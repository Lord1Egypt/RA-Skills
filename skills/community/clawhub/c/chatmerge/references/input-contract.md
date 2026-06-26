# Input Contract

当用户没有给规范数据，先接收原始聊天内容，再尽量归一化到一个稳定结构。这个文件只在需要处理原始导出、OCR 文本或结构化消息对象时阅读。

## Accepted Inputs

- 用户直接粘贴的群聊文本
- 平台导出的聊天记录
- OCR 后的截图文本
- 已经抓取好的 JSON、YAML 或 CSV 消息数据
- 混合来源的手工整理内容

## Preferred Normalized Shape

```yaml
messages:
  - platform: telegram
    channel_id: "-1001234567890"
    channel_label: "Project Alpha"
    thread_id: "thread_42"
    message_id: "12345"
    author_id: "u_001"
    author_name: "张三"
    timestamp: "2026-03-22T09:15:00+08:00"
    timezone: "Asia/Shanghai"
    text: "今天先修支付崩溃，晚上前给回归结果。"
    reply_to: "12340"
    mentions: ["李四"]
    attachments: []
    links: []
    reactions: []
    is_bot: false
    language: "zh-CN"
```

## Minimum Required Fields

最少保留这些字段：

- `platform`
- `channel_label` 或 `channel_id`
- `author_name`
- `timestamp` 或可靠的相对顺序
- `text`

缺字段时可以为 `null`，但不要臆造。

## Normalization Rules

- 时间统一成 ISO 8601；如果原始数据没有时区，就保留原文并标注时区不确定
- 作者名尽量统一同一人的多个显示名，但没有证据时不要强合并
- 频道名称优先保留人类可读标签，同时保存原始 ID
- OCR 噪声只做轻量修正，避免改坏原意
- 链接、附件、Bug 编号、工单号、金额、日期要尽量保留

## Noise Filtering

默认可过滤：

- 入群退群、系统通知
- 纯广告、明显无关转发
- 纯表情或无语义短消息

这些内容要谨慎保留：

- `收到`、`OK`、`同意`、`先别发`、`明天上线`
- 很短但会改变决策、优先级或状态的回复

## Dedup Heuristics

跨平台或跨群去重时，至少满足下列多数条件：

- 归一化文本高度一致
- 发送时间接近
- 作者或转发来源一致
- 链接、附件、工单号一致

不要去重这些情况：

- 同一句话在不同上下文里表达不同态度
- 一个是原始消息，另一个是带补充信息的转述
- 同主题但不同执行人、截止时间或风险等级

## Thread Reconstruction

优先级从高到低：

1. 显式 `reply_to`
2. 平台线程 ID
3. 同一主题关键词或工单号
4. 相近时间内的连续追问和回应
5. 明确的 @提及

如果只能弱推断，结果里要写成“可能属于同一讨论”。
