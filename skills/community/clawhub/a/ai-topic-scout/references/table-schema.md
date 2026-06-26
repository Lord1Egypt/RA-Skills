# 数据表字段结构

## config.json 格式

初始化完成后，将所有 ID 保存到此文件（同目录下），后续操作直接读取：

```json
{
  "baseId": "xxx",
  "tables": {
    "youtube": {
      "tableId": "xxx",
      "fields": {
        "博主名称": "fld_xxx",
        "频道ID": "fld_xxx",
        "频道链接": "fld_xxx",
        "内容方向": "fld_xxx",
        "状态": "fld_xxx",
        "添加时间": "fld_xxx",
        "备注": "fld_xxx"
      },
      "options": {
        "状态": {
          "活跃": "opt_xxx",
          "暂停": "opt_xxx"
        }
      }
    },
    "twitter": {
      "tableId": "xxx",
      "fields": {
        "博主名称": "fld_xxx",
        "用户名": "fld_xxx",
        "主页链接": "fld_xxx",
        "内容方向": "fld_xxx",
        "状态": "fld_xxx",
        "添加时间": "fld_xxx",
        "备注": "fld_xxx"
      },
      "options": {
        "状态": {
          "活跃": "opt_xxx",
          "暂停": "opt_xxx"
        }
      }
    },
    "fetch": {
      "tableId": "xxx",
      "fields": {
        "来源": "fld_xxx",
        "博主名称": "fld_xxx",
        "标题": "fld_xxx",
        "内容摘要": "fld_xxx",
        "原文链接": "fld_xxx",
        "发布时间": "fld_xxx",
        "抓取时间": "fld_xxx",
        "内容类型": "fld_xxx",
        "关键词标签": "fld_xxx",
        "处理状态": "fld_xxx"
      },
      "options": {
        "来源": {
          "YouTube": "opt_xxx",
          "Twitter": "opt_xxx"
        },
        "内容类型": {
          "视频": "opt_xxx",
          "推文": "opt_xxx",
          "长推文": "opt_xxx",
          "转推评论": "opt_xxx"
        },
        "处理状态": {
          "待分析": "opt_xxx",
          "已分析": "opt_xxx",
          "已忽略": "opt_xxx"
        }
      }
    },
    "analysis": {
      "tableId": "xxx",
      "fields": {
        "主题": "fld_xxx",
        "热度评分": "fld_xxx",
        "相关内容数": "fld_xxx",
        "来源博主": "fld_xxx",
        "主题分类": "fld_xxx",
        "背景信息": "fld_xxx",
        "选题建议": "fld_xxx",
        "分析时间": "fld_xxx",
        "状态": "fld_xxx",
        "相关内容": "fld_xxx"
      },
      "options": {
        "主题分类": {
          "大模型": "opt_xxx",
          "AI应用": "opt_xxx",
          "AI编程": "opt_xxx",
          "AI硬件": "opt_xxx",
          "AI政策": "opt_xxx",
          "AI创业": "opt_xxx",
          "AI开源": "opt_xxx",
          "其他": "opt_xxx"
        },
        "状态": {
          "待审核": "opt_xxx",
          "已采纳": "opt_xxx",
          "已放弃": "opt_xxx"
        }
      }
    }
  }
}
```

## 字段说明

### YouTube博主表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 博主名称 | text | 频道名称 |
| 频道ID | text | YouTube频道ID（UC开头） |
| 频道链接 | text | `https://www.youtube.com/@handle` |
| 内容方向 | text | 简述该频道主要内容 |
| 状态 | singleSelect | 活跃/暂停 |
| 添加时间 | date | YYYY-MM-DD |
| 备注 | text | 补充信息 |

### Twitter博主表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 博主名称 | text | 显示名 |
| 用户名 | text | @handle 格式 |
| 主页链接 | text | `https://x.com/handle` |
| 内容方向 | text | 简述该博主主要内容 |
| 状态 | singleSelect | 活跃/暂停 |
| 添加时间 | date | YYYY-MM-DD |
| 备注 | text | 补充信息 |

### 抓取内容表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 来源 | singleSelect | YouTube / Twitter |
| 博主名称 | text | 内容作者 |
| 标题 | text | 视频标题 / 推文开头 |
| 内容摘要 | text | 200字以内摘要 |
| 原文链接 | text | 完整URL（用于去重） |
| 发布时间 | date | 内容原始发布时间 |
| 抓取时间 | date | 本系统抓取时间 |
| 内容类型 | singleSelect | 视频/推文/长推文/转推评论 |
| 关键词标签 | text | 逗号分隔的关键词 |
| 处理状态 | singleSelect | 待分析/已分析/已忽略 |

### 选题分析表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 主题 | text | emoji + 选题标题 |
| 热度评分 | number | 0-100 |
| 相关内容数 | number | 关联的 fetch 记录数 |
| 来源博主 | text | 逗号分隔的博主名 |
| 主题分类 | singleSelect | 8个分类 |
| 背景信息 | text | Tavily 搜索补充的背景 |
| 选题建议 | text | 目标受众+时长+结构+标题 |
| 分析时间 | date | 分析执行时间 |
| 状态 | singleSelect | 待审核/已采纳/已放弃 |
| 相关内容 | unidirectionalLink | 关联到抓取内容表的记录 |
