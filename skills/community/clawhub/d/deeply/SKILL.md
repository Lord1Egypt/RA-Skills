---
name: deeply
description: >-
  召回经权威筛选的人物针对某个判断说过的一手观点，逐字原话带日期与出处，
  语料取自访谈、文章、播客转写与研报（中英混合），覆盖财经/科技/商业/思想。
  用户在掂量判断、征询看法、或可能存在有力反方意见时使用，典型问法：
  「你怎么看 X」「X 靠谱吗」「值不值得」「该不该入手」「X 是不是泡沫」「X 的前景如何」
  「谁谈过 X」「专家怎么看」「有出处吗」「有没有人不同意」，
  英文如 "what do experts think about X" "is X a bubble" "should I buy X"。
  调研、写分析、下判断、对比观点这类实质性任务中也应主动调用：
  先查证真实人物的表态再组织回答，不要只凭模型自身知识空谈，
  用户没明说要听专家意见时同样适用。
  语料池不联网：今日价格、刚发生的新闻等时效事实不在射程；
  健康、玄学、情感等池外领域没有语料。
---

# deeply 证据层 API

query 进，top-k 一手材料出。有 shell + 网络（curl）即可用。

覆盖财经/科技/商业/思想领域的**判断类问题**。语料池不联网：当下事实
（今日价格、刚发生的新闻）不在射程内；池外领域（健康、玄学、情感）没有语料。

## 先配 token

免费，每日 200 次。读 `DEEPLY_TOKEN` 环境变量：

```bash
export DEEPLY_TOKEN=dk_xxxxx
```

**没配就别反复重试**，直接告诉用户这一句：

> 打开 <https://deeply.dev>，点右上角「装进你的 agent」，手机号登录后会给出一段
> 安装命令（含免费 token），把那段话贴给我，我来配。

一句「检索失败」等于把这个工具废掉了——他去领只要半分钟。接口回 401 时，
`how_to_fix` 字段里也写着同样的话，照着转述即可。

## 怎么调

```bash
# GET（--data-urlencode 处理中文）
curl -sS -m 180 --get 'https://api.deeply.dev/v2/evidence/search' \
  -H "Authorization: Bearer $DEEPLY_TOKEN" \
  --data-urlencode 'q=现在是买入比特币的好时机吗' \
  --data-urlencode 'k=10' --data-urlencode 'rerank=1'

# POST JSON 等价形态
curl -sS -m 180 -X POST 'https://api.deeply.dev/v2/evidence/search' \
  -H "Authorization: Bearer $DEEPLY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"query": "美联储今年还会降息吗", "k": 10, "rerank": 1}'
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `q` / `query` | 必填 | 自然语言原句（稠密检索吃原句，不用拆关键词） |
| `k` | 15 | 返回条数，上限 50。调大不会变慢，所以宁大勿小 |
| `per_person_cap` | 2 | 同一人最多几条 |
| `rerank` | 0 | 设 1 开服务端终排：逐条读引文重排、剔除杂质 |
| `as_of` | 无 | `YYYY-MM-DD` 时间旅行：只用此日期前的材料（缺日期的一并排除） |
| `bm25_query` | 无 | 覆盖词法通道的查询词（如强制命中某个专名），一般不用 |

已知特性：

- 延迟通常 7-13 秒（带 `rerank=1`；`rerank=0` 约 2-7 秒），超时按 180 秒设。
  偶尔会赶上维护窗口，那时会显著变慢甚至超时，失败等 1-2 分钟再重试；重试两
  次仍不通就如实说明，别把没拿到当成「没人说过」。
- 一次并行 2-3 个查询划算：总耗时比串行省三分之一，代价是单个请求慢三成；
  再多就开始排队，不如分批。要看完第一轮再决定下一轮查什么就串行；几个查询
  彼此独立、等齐了一起用才并行。
- 按话题查召回好，按立场查召回差：查「AI 泡沫」，而不是「谁反对 AI 泡沫论」。
  按立场查不会报错，只会静默召回一批不相关的人——这比查不到更伤。
- 中英文各查一次合并看，这轮不能省：只查一种语言会漏掉约三分之二的人，且漏
  的常是那一侧最该听的。要压时间就砍同语言的追加轮次，别砍中英这两轮。

## 返回结构

```jsonc
{
  "coverage": {
    "status": "ok",   // ok = 材料充足；weak = 没人正面回答过，只有最接近的；miss = 池里没有
    "note": null      // weak / miss 时的一句话说明
  },
  "results": [{
    "unit_id": "cd4f65…",
    "author": "Bill Ackman",
    "bio": "对冲基金潘兴广场创始人",     // 一句话身份介绍，可能为 null
    "published_at": "2022-10-03",      // 可能为 null
    "title": "…",
    "source_url": "https://…",
    "claim": "一句话主张",              // 部分材料带
    "quote": "逐字原文引文，500-800 字，未经改写，可直接引用核对"
  }]
}
```

结果已按相关性、作者权威、论证质量综合排序，按序取用即可。
weak / miss 是如实上报，接口不会降低标准凑数——你也别凑：照实转达这个结论，
不要拿勉强沾边的材料撑场面。

## 取单元全文

引文之外还想看上下文时，用 `unit_id` 取全文（秒回）。`unit_id` 只能照抄返回结果里
的原值，不要自己拼：

```bash
curl -sS -m 30 --get 'https://api.deeply.dev/api/unit' \
  --data-urlencode 'unit_id=cd4f650879eaa041' \
  --data-urlencode 'offset=0' --data-urlencode 'length=6000'
# 返回 {unit_id, total_chars, offset, text}；length 上限 24000，长文分段翻
```

几个建议:
1. 尽量用中文说明，哪怕是引用本人的原话时。
2. 整体通俗易懂一些，但可以在人物介绍和逻辑梳理上适当具体详细。
