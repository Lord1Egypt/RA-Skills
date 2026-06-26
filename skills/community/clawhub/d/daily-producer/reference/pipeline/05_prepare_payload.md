# 05 去噪打分

## 脚本

```bash
python3 scripts/prepare_payload.py --date {date}
```

## 作用

从 detail.txt 中解析所有候选条目，基于 profile 关键词过滤噪音、打分排序，输出结构化 JSON 供 AI 生成日报。

## 输入

- `output/raw/{date}_detail.txt` — 由 collect_detail.py 生成
- `config/profile.yaml` — 关键词和排除话题

## 输出

- `output/raw/{date}_candidates.json` — 结构化候选列表

## 去噪逻辑

**不使用硬编码黑名单，完全基于 profile 关键词匹配，通用于任何用户画像。**

### 噪音判断规则

| 条目类型 | 判断 | 保留条件 |
|---------|------|---------|
| 标题为空 | → 噪音 | — |
| 命中 exclude_topics | → 噪音 | — |
| 网站类（region=website） | → 直接保留 | Google site: 搜索自带相关性 |
| 平台搜索结果（有 keyword） | → 宽松 | 搜索词在内容中出现 **或** 命中 ≥1 个 profile 关键词 |
| 热门/趋势类（无 keyword） | → 严格 | 命中 ≥1 个具体关键词 **或** 命中 ≥2 个任意关键词 |

### 「具体关键词」vs「泛义关键词」

- **具体关键词**：含中文的词（"智能体"）、含大写的品牌名（"OpenAI"）、多词短语（"AI coding"）
- **泛义关键词**：短的常见英文单词（agent、model、tool、product、release 等）

泛义关键词单独命中不够可靠（"agent" 可能指经纪人/特工），需要配合其他关键词才算有效。

## 打分逻辑

```
得分 = 热度分(0-50) + 关键词匹配分(0-30) + 来源可信度分(0-5)
```

- **热度分**：`min(50, log10(hot+1) * 10)`，热度越高分越高但有上限
- **关键词匹配分**：每命中 1 个 profile 关键词 +5，最高 30
- **来源可信度**：tier-1 来源（Twitter、微博、量子位等）+5

## 输出格式

```json
{
  "meta": {
    "date": "2026-04-06",
    "total_parsed": 91,
    "after_noise_filter": 69,
    "top_n": 69
  },
  "candidates": [
    {
      "rank": 1,
      "score": 57.4,
      "title": "...",
      "platform": "Twitter/X",
      "author": "...",
      "time": "...",
      "url": "...",
      "hot": "17386",
      "keyword": "...",
      "ai_summary": {"what_happened": "", "why_it_matters": ""},
      "ai_relevance": "",
      "ai_priority": "",
      "ai_tags": []
    }
  ],
  "ai_todo": {
    "instruction": "请为每条候选填写 ai_summary、ai_relevance、ai_priority、ai_tags...",
    "target_items": 15
  }
}
```

`ai_*` 字段为空，留给下一步 AI 填写。

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--date` | 今天 | 目标日期 |
| `--top` | 0 | 保留前 N 条，0=全部保留 |
| `--no-save` | false | 不保存到文件 |

## 多行正文处理

Twitter 推文等多行内容在 detail.txt 中以续行形式存在。解析器将这些续行追加到 `fields["text"]` 字段中（换行拼接），用于关键词匹配和去噪判断。
