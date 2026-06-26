# 画像格式规范

画像数据存储在SQLite，按需加载字段。以下定义profile_json完整结构。

## 核心字段

| 字段 | 类型 | 说明 | 加载时机 |
|------|------|------|---------|
| profile_version | string | "2.0" | 始终 |
| lecturer_id | string | 讲师标识 | 始终 |
| lecturer_name | string | 显示名称 | 始终 |
| qualitative | object | 定性分析 | 文案生成 |
| persona_mapping | object | 人设映射 | 文案生成 |
| style_dimensions | object | 文风五维 | 文案生成 |
| reference_scripts | array | 参考示例索引 | 文案生成 |
| sample_excerpts | object | 精彩片段 | 文案生成 |
| quantitative | object | 定量分析 | 增量合并 |
| sample_stats | object | 样本统计 | 管理 |
| merge_history | array | 合并历史 | 管理 |
| created_at | string | 创建时间 | 管理 |
| updated_at | string | 更新时间 | 管理 |

## Token优化对比

| 场景 | 全量加载 | 按需加载 | 节省 |
|------|----|----|------|
| 文案生成（加载画像） | ~2500 tokens | ~400 tokens | 84% |
| 增量合并（加载定量） | ~2500 tokens | ~1500 tokens(单独) | 40% |
| 知识检索(1产品5文档) | ~1500 tokens | ~300-500 tokens | 67-80% |
| 系列连续性(10集) | ~3200 tokens | ~600 tokens(摘要) | 81% |

## quantitative字段合并策略

| 字段 | 策略 | 说明 |
|------|------|------|
| basic_stats | 计数型累加 | total_chinese_chars等直接相加 |
| sentence_length | 数值型加权平均 | avg/median/stdev按权重合并 |
| word_frequency | 列表型合并去重 | 同词累加count，取Top50 |
| bigrams | 列表型合并去重 | 同上 |
| punctuation | 计数型累加+比率加权 | counts累加，ratios加权 |
| vocabulary_diversity | 数值型加权平均 | ttr按权重合并 |
| rhetorical_patterns | 计数型累加+比率加权 | 同punctuation |
| connector_patterns | 计数型累加 | 各类别count累加 |
| opening/closing_patterns | 列表保留最新5条 | 新数据覆盖旧数据 |
