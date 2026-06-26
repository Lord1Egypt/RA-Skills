# catfee-feishu-recorder

飞书群聊总结技能。

## 触发关键词

总结群聊 | 拉取聊天记录 | 最近一周 | 最近一个月 | 帮我看看这几天

## 功能说明

1. 拉取群聊消息（默认7天，可自定义时间范围）
2. 生成摘要统计（活跃成员Top10、消息分布等）
3. 生成完整聊天记录（含发送者ID、昵称、时间、内容）
4. 创建飞书文档保存记录

## 凭证配置（必须）

在运行前设置环境变量：

```
FEISHU_APP_ID=cli_xxxxxxxxxx
FEISHU_APP_SECRET=your_secret_here
```

获取方式：飞书开放平台 → 应用凭证

## 必选权限

- im:message:readonly（读取群消息）
- docx:document:create（创建云文档）

## 调用示例

```
python scripts/summarize.py <chat_id> <时间范围>

python scripts/summarize.py oc_281d2d2dcec5e1fcd29d7ac809e75111 "最近7天"
python scripts/summarize.py oc_281d2d2dcec5e1fcd29d7ac809e75111 "2026-04-01"
```

## 时间范围输入格式

| 输入 | 范围 |
|------|------|
| 今天/昨天 | 1天 |
| 最近几天/这周 | 7天 |
| 最近两周 | 14天 |
| 最近一个月 | 30天 |
| 2026-04-01 | 指定日期至今 |

## 飞书文档内容

生成的文档包含两部分：

**摘要部分：**
- 时间范围、总消息数
- 活跃成员Top10排行（昵称 + ID + 消息数）
- 最近20条消息预览

**完整记录部分：**
- 所有文本消息列表
- 每条记录包含：时间、发送者ID、发送者昵称、消息内容
