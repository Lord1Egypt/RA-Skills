# Declutter Coach（整理教练）

## Overview
帮助用户对特定空间（衣柜、书架、抽屉等）进行整理，提供分步计划、断舍离原则和变现渠道。

## Trigger
- 整理衣柜/房间
- 断舍离
- 东西太多
- 收纳建议

## Workflow
1. 识别整理目标区域
2. 给出断舍离分类原则
3. 提供分步执行计划（含时间估算）
4. 给出闲置变现渠道

## Output
JSON: {targetArea, declutterPlan{steps[], category_rules[], time_estimate}, tips[], donationChannels[]}
