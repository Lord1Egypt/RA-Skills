# 开源词库来源说明

## 词库 1: konsheng/Sensitive-lexicon

- GitHub: <https://github.com/konsheng/Sensitive-lexicon>
- License: MIT
- 特点：持续维护，分类细，含 COVID/GFW 补充词

使用的文件：
- `Vocabulary/广告类型.txt`
- `Vocabulary/政治类型.txt`
- `Vocabulary/暴恐词库.txt`
- `Vocabulary/色情词库.txt`
- `Vocabulary/涉枪涉爆.txt`
- `Vocabulary/其他词库.txt`
- `Vocabulary/补充词库.txt`

## 词库 2: bigdata-labs/sensitive-stop-words

- GitHub: <https://github.com/bigdata-labs/sensitive-stop-words>
- License: 未注明（开源公开项目）
- 特点：常用互联网敏感词，含停止词

使用的文件：
- `广告.txt`
- `政治类.txt`
- `色情类.txt`
- `涉枪涉爆违法信息关键词.txt`

## 词库 3: jkiss/sensitive-words

- GitHub: <https://github.com/jkiss/sensitive-words>
- License: 未注明（开源公开项目）
- 特点：互联网常用敏感词，含停止词

使用的文件：
- `广告.txt`
- `政治类.txt`
- `色情类.txt`

## 合并策略

三个词库去重合并为 `data/sensitive_words.txt`，排序存储。
更新时全量替换，保持与上游同步。

## 抖音平台特有限流词（内置补充）

以下词汇不在上述词库中，但抖音平台已知会限流，直接内置在 `check.py` 的 `CATEGORY_PATTERNS`:

**平台限流词**: 推广、广告、营销、引流、私信、加微信、扫码、点链接、下单、购买、优惠券、福利、秒杀、限时

**广告极限词**: 最好、第一、唯一、顶级、极致、无敌、史上最、全网最、最强、最优、最大、最低、最高、最便宜、专家级、国家级
