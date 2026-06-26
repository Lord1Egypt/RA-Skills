---
name: football-predict
description: >
  足球赛事预测神器。自动采集 titan007.com 数据（亚盘、大小球、欧赔、基本面、阵容、角球、半全场），
  5 步量化分析框架，输出投注建议与预测比分。Football match betting prediction system. Auto-scrapes data from m.nowscore.com (Asian handicap,
  over/under, European odds, fundamentals, lineups, corners, half-time goals), runs a 5-step
  quantitative analysis framework, and outputs betting recommendations with predicted scores.
  Supports concise/visual dual output modes, post-match review, and auto weight optimization.
  Triggers: (1) match ID like "2908467" or match description, (2) requests to predict/analyze
  football matches (e.g. "predict", "analyze this match"), (3) match results for post-match review
  (e.g. "review", "result was 2-1"), (4) handicap/over-under analysis.
---

# 足球博彩预测 / Football Betting Prediction

三大工作流：数据采集 → 预测分析 → 赛后复盘

## 输出模式选择

用户请求预测时，询问或推断偏好的输出格式：

- **简洁模式 (Concise)**: 快速结果 - 最佳推荐、概率、EV、预测比分
- **可视化模式 (Visual/Detailed)**: 完整 HTML 报告，含数据表格、公式、图表

未指定时：默认使用可视化模式以获得最佳用户体验。

---

## 工作流一：赛前数据采集

用户提供比赛 ID 或比赛描述时，从 m.nowscore.com 采集数据。

1. 构建 URL: `https://m.nowscore.com/Analy/Analysis/{match_id}.htm`
2. 使用 `browser navigate` 打开页面
3. 使用新球体育数据提取数据。详见 [references/data-collection.md](references/data-collection.md)

**关于首发阵容**：首发阵容通常在开赛前30-60分钟公布。提前收集时标注"阵容待公布"，使用现有阵容深度信息。接近开球时如有需要可重新检查。

**需采集数据点：**
- 比赛信息（球队、联赛、时间、场地、天气）
- 亚盘（让球盘）："即"和"早"行，所有机构
- 大小球盘："即"和"早"行，所有机构
- 欧赔（胜平负）："即"和"早"行，前10+机构
- 球队基本面（近期战绩、主客场、历史交锋、联赛排名）
- 大小球增强数据：半场进球、角球
- 首发阵容（如比赛前30-60分钟内可用）

采集完成后，立即进入工作流二。

**⚠️ 存档规则（强制）**：预测完成后，必须将比赛ID、联赛、盘口、推荐、预测比分写入 `~/.hermes/workspace/memory/football-match-history.md`。格式参照已有条目，状态标记为"待确认"。不存档=不完整。

---

## 工作流二：预测分析

对收集的数据运行五步预测框架。详见 [references/prediction-framework.md](references/prediction-framework.md)

**输出模式决定呈现方式：**
- **简洁**：基于文本的快速摘要，关键数字
- **可视化**：完整 HTML 报告，数据表格、概率条、公式展示

**步骤概述：**
1. **数据整理** - 将所有收集的数据分类整理
2. **基本面分析** - 盘口合理性、走势追踪、机构意图、欧亚转换
3. **盘口概率计算** - 计算亚盘和大小球的真实隐含概率
4. **模型预测** - 两个逻辑回归模型：亚盘模型（权重：盘口0.35 > 基本面0.20+0.20 > 阵容0.15 > 战意0.10）和大小球模型（含xG、联赛因子、半场进球、角球等）
5. **EV 计算与推荐** - 计算每个投注选项的期望值，输出最佳推荐和预测比分

**默认初始权重**：基于 AI 概率判断设置，通过赛后复盘自动优化。

**输出格式：**
- 亚盘分析及其赢盘概率
- 大小球分析及其赢盘概率
- 所有选项的 EV 值
- 最佳投注推荐
- 预测比分

---

## 工作流三：赛后复盘

用户提供比赛结果或请求复盘时触发。详见 [references/review-framework.md](references/review-framework.md)

**流程：**
1. 回顾本场比赛的所有赛前数据和预测分析
2. 运行偏差分析，比较预测与实际结果
3. 识别预测错误的根本原因
4. **自动优化**：根据预测误差调整特征权重
5. 将更新后的框架保存到内存文件以持久化
6. 输出所有已分析比赛的累计准确率统计

**持久化**：将框架更新和比赛历史保存到内存文件，以便跨会话学习。

**目标**：亚盘和大小球预测准确率均达到 70% 以上。

---

## 参考文档

- [data-collection.md](references/data-collection.md) - 数据采集指南
- [prediction-framework.md](references/prediction-framework.md) - 预测分析框架
- [review-framework.md](references/review-framework.md) - 赛后复盘与学习框架
