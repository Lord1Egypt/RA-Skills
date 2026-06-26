---
name: football-prediction-optimized
version: 1.0.0
description: 使用优化后的提示词对足球比赛进行预测，支持批量筛选(stage1)和单场比赛预测(stage2)
disable-model-invocation: false
---

# 足球预测优化技能

这个技能使用经过自我优化系统优化的最佳提示词，对足球比赛进行专业预测。包含两个阶段：

1. **Stage1 批量筛选**：对同一比赛日的多场比赛进行横向比较，筛选出最适合预测的高质量场次。
2. **Stage2 单场比赛预测**：对单场比赛进行深入分析，预测胜平负结果，并计算CLV收益预估。

## 功能特性

### Stage1 批量筛选
- **多维评估**：从数据完整性、市场清晰度、基本面优势、预测潜力、风险等级5个维度评分
- **智能筛选**：根据综合评分自动筛选评分>6.0的比赛，数量控制在3-8场
- **结构化输出**：JSON格式的筛选结果，包含详细评分和筛选理由

### Stage2 单场比赛预测
- **综合分析**：结合基本面分析、市场分析、数据质量评估、风险因素识别
- **CLV收益预估**：预测主胜、平局、客胜三个选项的CLV值（收盘赔率变化值）
- **置信度评估**：提供0-1的置信度评分
- **风险提示**：列出主要风险因素

## 使用方法

### 方法1：通过OpenClaw技能调用
当用户需要足球比赛预测时，技能会自动触发：
- "批量筛选今天的所有比赛"
- "预测这场比赛的结果"
- "分析这场比赛并给出CLV预估"

### 方法2：直接使用Python脚本
```bash
# Stage1 批量筛选
python3 /Users/cjy/.openclaw/workspace/skills/football-prediction-optimized/football_prediction.py stage1 --input batch_fet_txt.txt

# Stage2 单场比赛预测
python3 /Users/cjy/.openclaw/workspace/skills/football-prediction-optimized/football_prediction.py stage2 --input single_fet_txt.txt
```

### 方法3：与lota-football技能配合使用
```bash
# 1. 使用lota-football获取比赛特征文本
# 2. 将特征文本保存到文件
# 3. 使用本技能进行预测
python3 football_prediction.py stage2 --input fet_txt.txt
```

## 输入格式

### Stage1 输入
多场比赛的特征文本，每场比赛的特征文本用`===`分隔：
```
{第一场比赛的特征文本}
===
{第二场比赛的特征文本}
===
...
```

### Stage2 输入
单场比赛的特征文本（完整fet_txt格式）

## 输出格式

### Stage1 输出
```json
{
  "date": "比赛日期",
  "total_matches": 总比赛数量,
  "selected_matches": [
    {
      "lota_id": "比赛唯一ID",
      "home_team": "主队名称",
      "away_team": "客队名称",
      "league": "所属联赛",
      "score": 综合评分,
      "data_completeness": 数据完整性得分,
      "market_clarity": 市场清晰度得分,
      "fundamental_strength": 基本面优势得分,
      "prediction_potential": 预测潜力得分,
      "risk_level": 风险等级得分,
      "decision": "KEEP",
      "reason": "筛选理由"
    }
  ],
  "summary": {
    "total_selected": 选中比赛数量,
    "average_score": 平均综合评分,
    "selection_rate": 选中比例
  }
}
```

### Stage2 输出
```json
{
  "lota_id": "比赛唯一ID",
  "prediction": "H/D/A",
  "confidence": 0.85,
  "reasoning": [
    "理由1：...",
    "理由2：...",
    "理由3：..."
  ],
  "clv_estimates": {
    "home": 0.02,
    "draw": -0.01,
    "away": 0.03
  },
  "risk_factors": [
    "风险因素1",
    "风险因素2"
  ],
  "timestamp": "2026-03-28 10:30:00"
}
```

## 环境变量

- `DEEPSEEK_API_KEY`: DeepSeek API密钥（必需）
- `DEEPSEEK_BASE_URL`: DeepSeek API基础URL（可选，默认：https://api.deepseek.com）

## 技术实现

1. **模型调用**：使用DeepSeek API（deepseek-chat模型）
2. **提示词优化**：使用自我优化系统得到的最佳提示词
3. **错误处理**：网络重试、格式验证、异常捕获
4. **性能优化**：异步调用、缓存机制

## 与现有技能集成

### 与lota-football技能集成
1. 使用lota-football技能获取比赛列表和特征文本
2. 将特征文本传递给本技能进行预测
3. 结合两个技能的结果进行综合决策

### 与odds-plotter技能集成
1. 使用odds-plotter技能绘制赔率走势图
2. 使用本技能进行预测分析
3. 结合图表和预测结果进行深度分析

## 示例用例

### 用例1：每日比赛筛选
```
用户：筛选今天所有竞彩比赛，推荐3-8场高质量比赛
流程：
1. lota-football获取今日比赛特征文本
2. Stage1批量筛选
3. 输出推荐比赛列表
```

### 用例2：单场比赛深度分析
```
用户：深度分析曼联对切尔西这场比赛
流程：
1. lota-football获取该场比赛特征文本
2. Stage2单场比赛预测
3. 输出预测结果和CLV预估
```

### 用例3：批量预测与筛选
```
用户：批量预测今天所有比赛，并筛选出最有价值的比赛
流程：
1. lota-football获取今日所有比赛特征文本
2. Stage2逐个预测每场比赛
3. 根据置信度和CLV值进行排序筛选
```

## 错误处理

1. **API调用失败**：自动重试3次，使用指数退避
2. **输入格式错误**：提示正确的输入格式示例
3. **模型输出格式错误**：尝试解析或使用备用提示词
4. **环境变量缺失**：提示设置必要的环境变量

## 性能考虑

- 批量处理时限制并发数，避免API限制
- 使用本地缓存存储频繁查询的比赛数据
- 支持断点续传，避免重复处理

## 更新日志

### v1.0.0 (2026-03-28)
- 初始版本，基于自我优化系统的最佳提示词
- 支持Stage1批量筛选和Stage2单场比赛预测
- 与lota-football技能无缝集成