# 首次初始化指南

## 1. 创建钉钉AI表格 Base

```bash
mcporter call dingtalk-ai-table create_base \
  --args '{"baseName":"AI短视频选题","description":"AI内容追踪与短视频选题分析"}' \
  --output json
```

记下返回的 `baseId`。

## 2. 创建 YouTube博主 表

```bash
mcporter call dingtalk-ai-table create_table --args '{
  "baseId":"<baseId>",
  "tableName":"YouTube博主",
  "fields":[
    {"fieldName":"博主名称","type":"text"},
    {"fieldName":"频道ID","type":"text"},
    {"fieldName":"频道链接","type":"text"},
    {"fieldName":"内容方向","type":"text"},
    {"fieldName":"状态","type":"singleSelect","config":{"options":[{"name":"活跃"},{"name":"暂停"}]}},
    {"fieldName":"添加时间","type":"date","config":{"formatter":"YYYY-MM-DD"}},
    {"fieldName":"备注","type":"text"}
  ]
}' --output json
```

## 3. 创建 Twitter博主 表

```bash
mcporter call dingtalk-ai-table create_table --args '{
  "baseId":"<baseId>",
  "tableName":"Twitter博主",
  "fields":[
    {"fieldName":"博主名称","type":"text"},
    {"fieldName":"用户名","type":"text"},
    {"fieldName":"主页链接","type":"text"},
    {"fieldName":"内容方向","type":"text"},
    {"fieldName":"状态","type":"singleSelect","config":{"options":[{"name":"活跃"},{"name":"暂停"}]}},
    {"fieldName":"添加时间","type":"date","config":{"formatter":"YYYY-MM-DD"}},
    {"fieldName":"备注","type":"text"}
  ]
}' --output json
```

## 4. 创建 抓取内容 表

```bash
mcporter call dingtalk-ai-table create_table --args '{
  "baseId":"<baseId>",
  "tableName":"抓取内容",
  "fields":[
    {"fieldName":"来源","type":"singleSelect","config":{"options":[{"name":"YouTube"},{"name":"Twitter"}]}},
    {"fieldName":"博主名称","type":"text"},
    {"fieldName":"标题","type":"text"},
    {"fieldName":"内容摘要","type":"text"},
    {"fieldName":"原文链接","type":"text"},
    {"fieldName":"发布时间","type":"date","config":{"formatter":"YYYY-MM-DD HH:mm"}},
    {"fieldName":"抓取时间","type":"date","config":{"formatter":"YYYY-MM-DD HH:mm"}},
    {"fieldName":"内容类型","type":"singleSelect","config":{"options":[{"name":"视频"},{"name":"推文"},{"name":"长推文"},{"name":"转推评论"}]}},
    {"fieldName":"关键词标签","type":"text"},
    {"fieldName":"处理状态","type":"singleSelect","config":{"options":[{"name":"待分析"},{"name":"已分析"},{"name":"已忽略"}]}}
  ]
}' --output json
```

## 5. 创建 选题分析 表

```bash
mcporter call dingtalk-ai-table create_table --args '{
  "baseId":"<baseId>",
  "tableName":"选题分析",
  "fields":[
    {"fieldName":"主题","type":"text"},
    {"fieldName":"热度评分","type":"number"},
    {"fieldName":"相关内容数","type":"number"},
    {"fieldName":"来源博主","type":"text"},
    {"fieldName":"主题分类","type":"singleSelect","config":{"options":[{"name":"大模型"},{"name":"AI应用"},{"name":"AI编程"},{"name":"AI硬件"},{"name":"AI政策"},{"name":"AI创业"},{"name":"AI开源"},{"name":"其他"}]}},
    {"fieldName":"背景信息","type":"text"},
    {"fieldName":"选题建议","type":"text"},
    {"fieldName":"分析时间","type":"date","config":{"formatter":"YYYY-MM-DD HH:mm"}},
    {"fieldName":"状态","type":"singleSelect","config":{"options":[{"name":"待审核"},{"name":"已采纳"},{"name":"已放弃"}]}}
  ]
}' --output json
```

## 6. 创建关联字段

在选题分析表中添加指向抓取内容表的关联字段：

```bash
mcporter call dingtalk-ai-table create_fields --args '{
  "baseId":"<baseId>",
  "tableId":"<选题分析tableId>",
  "fields":[{
    "fieldName":"相关内容",
    "type":"unidirectionalLink",
    "config":{"linkedSheetId":"<抓取内容tableId>","multiple":true}
  }]
}' --output json
```

> ⚠️ 必须用 `unidirectionalLink`，不要用 `bidirectionalLink`。后者在 API 写入关联时行为一致，但单向关联更简单可靠。

## 7. 获取所有 fieldId

建表后必须读取每张表的字段ID，后续所有读写操作都依赖 fieldId：

```bash
mcporter call dingtalk-ai-table get_tables \
  --args '{"baseId":"<baseId>","tableIds":["<tableId1>","<tableId2>"]}' \
  --output json
```

对 singleSelect 字段还需获取 option ID：

```bash
mcporter call dingtalk-ai-table get_fields \
  --args '{"baseId":"<baseId>","tableId":"<tableId>","fieldIds":["<selectFieldId>"]}' \
  --output json
```

## 8. 保存配置

将所有 ID 写入 `references/config.json`，格式见 `table-schema.md`。

## 9. 填入初始博主

### 推荐 YouTube 博主（AI方向）

| 博主名称 | 频道链接 | 内容方向 |
|----------|---------|---------|
| Two Minute Papers | @TwoMinutePapers | AI研究论文速览 |
| AI Explained | @aiexplained-official | AI新闻深度解析 |
| Yannic Kilcher | @YannicKilcher | AI论文精读 |
| Matt Wolfe | @maboroshi | AI工具测评 |
| Fireship | @Fireship | AI与编程快讯 |
| DeepLearning.AI | @Deeplearningai | AI教程、行业洞察 |
| Matthew Berman | @matthew_berman | AI模型评测 |
| TheAIGRID | @TheAiGrid | AI突破新闻 |
| Sentdex | @sentdex | Python AI编程 |
| Wes Roth | @WesRoth | AGI进展分析 |

### 推荐 Twitter 博主（AI方向）

| 博主名称 | 用户名 | 内容方向 |
|----------|--------|---------|
| Sam Altman | @sama | OpenAI CEO |
| Yann LeCun | @ylecun | Meta首席AI科学家 |
| Jim Fan | @DrJimFan | NVIDIA机器人研究 |
| Andrej Karpathy | @karpathy | AI教育、LLM解析 |
| Emad Mostaque | @EMostaque | 开源AI |
| Swyx | @swyx | AI工程、Latent Space |
| Elvis Saravia | @omarsar0 | Prompt Engineering |
| Ethan Mollick | @emollick | AI实际应用研究 |
| Harrison Chase | @hwchase17 | LangChain/AI Agent |
| Rowan Cheung | @rowancheung | AI新闻速报 |

写入时 singleSelect 字段可以直接传 option name（如 `"活跃"`），不必传 option ID。
