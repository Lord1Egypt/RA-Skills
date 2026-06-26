---
name: consumer-research
description: 消费者调研能力；支持目标人群画像分析、核心需求挖掘、问卷设计与数据处理；当需要进行消费者洞察、产品定位或用户研究时使用
dependency:
  python:
    - pandas==1.5.0
  system:
    - mkdir -p data/consumer_data
---

# 消费者调研

## 任务目标
- 本技能用于：了解目标消费者特征、需求与偏好，指导产品定位
- 核心能力：人群画像、需求分析、问卷调研
- 触发条件：新品开发立项、用户研究、产品优化方向确定

## 数据来源

### 在线数据源

| 来源 | 网址 | 内容 |
|------|------|------|
| CBNData | https://www.cbndata.com | 消费人群画像、行业趋势 |
| QuestMobile | https://www.questmobile.com | 移动互联网用户洞察 |
| TalkingData | https://www.talkingdata.com | 消费者行为分析 |
| 艾瑞咨询 | https://www.iresearch.cn | 用户研究报告 |

### 数据获取方式

使用 `web_search` 搜索消费者洞察：

```
# 人群特征研究
web_search(query="健身人群 消费者画像 行为特征")
web_search(query="Z世代 食品消费 偏好 趋势")

# 需求洞察
web_search(query="减脂人群 食品需求 痛点")
web_search(query="老年人 健康食品 消费趋势")

# 市场报告
web_search(query="2024年 食品消费者洞察 报告")
web_search(query="无糖食品 消费者接受度 调研")
```

## 数据存储

采集的数据保存在工作区 `data/consumer_data/` 目录：
- `profile_data.json` - 人群画像数据
- `needs_analysis.json` - 需求分析数据
- `questionnaire_results.csv` - 问卷调查结果

## 操作步骤

### 1. 确定目标人群
1. 使用 `web_search` 搜索目标人群特征
2. 分析人口统计特征（年龄、性别、收入、地域）
3. 分析心理特征（价值观、生活方式）

### 2. 挖掘核心需求
1. 整理目标人群的核心痛点
2. 搜索相关调研报告获取数据支撑
3. 识别高机会需求

### 3. 设计调研问卷
1. 根据人群画像设计问卷结构
2. 参考问卷模板（见附件）
3. 确定调研渠道和样本量

### 4. 数据分析与输出
1. 收集问卷数据
2. 生成人群画像报告
3. 输出产品定位建议

## 资源索引
- 调研脚本：见 [scripts/consumer_research.py](scripts/consumer_research.py)
- 问卷模板：见 [assets/questionnaire_template.md](assets/questionnaire_template.md)
- 调研规范：见 [references/research_guidelines.md](references/research_guidelines.md)

## 注意事项
- 保护消费者隐私数据
- 样本量需满足统计显著性
- 问卷设计需遵循专业规范
