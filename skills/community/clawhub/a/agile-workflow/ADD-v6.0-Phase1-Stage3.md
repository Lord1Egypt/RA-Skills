# ADD - 敏捷工作流 v6.0 Phase 1 阶段 3: 创造性评分优化

**版本**: v6.0-Phase1-Stage3  
**状态**: 设计完成 → 实施中  
**原则**: 效率优先，保质保量（无时间计划）

---

## 1. 架构概述

### 1.1 设计目标

**核心目标**：实现创造性自动评分，与人工评分相关性>0.8

**创造性维度**：
```
创造性评分 = 新颖性 (25%) + 复杂性 (25%) + 深度 (25%) + 原创性 (25%)
```

### 1.2 质量标准

- 创造性评分准确率：> 85%
- 与人工评分相关性：> 0.8
- 质量评分：≥85 分
- 测试覆盖率：100%

---

## 2. 核心算法

### 2.1 新颖性检测 (25%)

**情节转折检测**：
```javascript
detectPlotTwists(content) {
  // 检测转折关键词
  const twistKeywords = ['然而', '却', '没想到', '突然', '意外', '转折'];
  
  // 检测转折密度
  const twistCount = countKeywords(content, twistKeywords);
  const density = twistCount / content.length * 1000;
  
  // 评分：0-100
  return Math.min(100, density * 10);
}
```

**设定创新检测**：
```javascript
detectSettingInnovation(content, baseline) {
  // 对比基准设定
  const uniqueElements = compareWithBaseline(content, baseline);
  
  // 创新元素数量评分
  return Math.min(100, uniqueElements.length * 10);
}
```

**表达方式创新**：
```javascript
detectExpressionInnovation(content) {
  // 检测修辞手法
  const rhetoricDevices = ['比喻', '拟人', '排比', '对比'];
  
  // 检测句式变化
  const sentenceVariety = analyzeSentenceVariety(content);
  
  // 综合评分
  return (rhetoricScore + sentenceVariety) / 2;
}
```

### 2.2 复杂性检测 (25%)

**多线叙事检测**：
```javascript
detectMultiThread(content) {
  // 检测视角切换
  const povChanges = detectPOVChanges(content);
  
  // 检测时间线
  const timelineChanges = detectTimelineChanges(content);
  
  // 检测场景切换
  const sceneChanges = detectSceneChanges(content);
  
  // 综合评分
  return (povChanges + timelineChanges + sceneChanges) / 3;
}
```

**人物关系复杂度**：
```javascript
detectCharacterRelations(content) {
  // 提取人物
  const characters = extractCharacters(content);
  
  // 提取关系
  const relations = extractRelations(content);
  
  // 关系图密度
  const density = relations.length / (characters.length * (characters.length - 1) / 2);
  
  return Math.min(100, density * 100);
}
```

**情节复杂度**：
```javascript
detectPlotComplexity(content) {
  // 检测情节点数量
  const plotPoints = extractPlotPoints(content);
  
  // 检测因果链长度
  const causeEffectChains = detectCauseEffectChains(content);
  
  // 检测冲突数量
  const conflicts = detectConflicts(content);
  
  // 综合评分
  return (plotPoints.length + causeEffectChains.length + conflicts.length) / 3;
}
```

### 2.3 深度检测 (25%)

**心理描写深度**：
```javascript
detectPsychologicalDepth(content) {
  // 检测心理描写关键词
  const心理Keywords = ['心想', '思考', '回忆', '感受', '内心', '情感'];
  
  // 检测心理描写密度
  const density = countKeywords(content, 心理 Keywords) / content.length * 1000;
  
  // 检测内心独白
  const monologues = detectMonologues(content);
  
  // 综合评分
  return Math.min(100, density * 10 + monologues.length * 5);
}
```

**主题深度**：
```javascript
detectThemeDepth(content) {
  // 检测主题关键词
  const themeKeywords = ['生命', '死亡', '爱', '恨', '自由', '命运', '人性'];
  
  // 检测主题讨论深度
  const themeDiscussions = detectThemeDiscussions(content, themeKeywords);
  
  // 检测哲学思考
  const philosophicalThoughts = detectPhilosophicalThoughts(content);
  
  // 综合评分
  return Math.min(100, themeDiscussions * 10 + philosophicalThoughts * 20);
}
```

**情感深度**：
```javascript
detectEmotionalDepth(content) {
  // 检测情感词汇
  const emotionWords = extractEmotionWords(content);
  
  // 检测情感变化
  const emotionChanges = detectEmotionChanges(content);
  
  // 检测情感层次
  const emotionLayers = detectEmotionLayers(content);
  
  // 综合评分
  return (emotionWords.length + emotionChanges * 10 + emotionLayers * 20) / 3;
}
```

### 2.4 原创性检测 (25%)

**套路识别**：
```javascript
detectCliches(content) {
  // 常见套路库
  const cliches = [
    '从此过上了幸福的生活',
    '这是一个美好的结局',
    '他们永远在一起了',
    '天降横财',
    '一见钟情',
    '失散多年的亲人'
  ];
  
  // 检测套路出现
  const detectedCliches = cliches.filter(c => content.includes(c));
  
  // 评分：每出现一个套路减 20 分
  return Math.max(0, 100 - detectedCliches.length * 20);
}
```

**陈词滥调检测**：
```javascript
detectOverusedPhrases(content) {
  // 陈词滥调库
  const overusedPhrases = [
    '阳光明媚',
    '心情愉快',
    '非常高兴',
    '十分惊讶'
  ];
  
  // 检测出现频率
  const frequency = countPhrases(content, overusedPhrases);
  
  // 评分：频率越高分数越低
  return Math.max(0, 100 - frequency * 5);
}
```

**创新点评分**：
```javascript
detectInnovations(content, baseline) {
  // 对比基准，找出创新点
  const innovations = findInnovations(content, baseline);
  
  // 评估创新点质量
  const qualityScore = evaluateInnovationQuality(innovations);
  
  // 综合评分
  return Math.min(100, innovations.length * 10 + qualityScore);
}
```

---

## 3. 综合评分算法

### 3.1 权重配置

```javascript
const weights = {
  novelty: 0.25,      // 新颖性 25%
  complexity: 0.25,   // 复杂性 25%
  depth: 0.25,        // 深度 25%
  originality: 0.25   // 原创性 25%
};
```

### 3.2 评分计算

```javascript
function calculateCreativityScore(content, baseline) {
  const scores = {
    novelty: detectNovelty(content, baseline),
    complexity: detectComplexity(content),
    depth: detectDepth(content),
    originality: detectOriginality(content, baseline)
  };
  
  const totalScore = 
    scores.novelty * weights.novelty +
    scores.complexity * weights.complexity +
    scores.depth * weights.depth +
    scores.originality * weights.originality;
  
  return {
    total: Math.round(totalScore),
    scores,
    level: getCreativityLevel(totalScore),
    suggestions: generateCreativitySuggestions(scores)
  };
}

function getCreativityLevel(score) {
  if (score >= 90) return 'S'; // 卓越
  if (score >= 80) return 'A'; // 优秀
  if (score >= 70) return 'B'; // 良好
  if (score >= 60) return 'C'; // 合格
  return 'D'; // 需改进
}
```

### 3.3 优化建议生成

```javascript
function generateCreativitySuggestions(scores) {
  const suggestions = [];
  
  if (scores.novelty < 70) {
    suggestions.push('增加情节转折，提升新颖性');
    suggestions.push('尝试创新的设定和表达方式');
  }
  
  if (scores.complexity < 70) {
    suggestions.push('增加多线叙事，提升复杂性');
    suggestions.push('丰富人物关系和情节层次');
  }
  
  if (scores.depth < 70) {
    suggestions.push('深化心理描写和情感表达');
    suggestions.push('探讨更深刻的主题');
  }
  
  if (scores.originality < 70) {
    suggestions.push('避免使用常见套路和陈词滥调');
    suggestions.push('寻找独特的创新点');
  }
  
  return suggestions;
}
```

---

## 4. 人工校准

### 4.1 校准流程

```
准备测试样本 (50+)
    ↓
人工评分 (3 人独立评分)
    ↓
算法评分
    ↓
相关性分析
    ↓
权重调整
    ↓
验证效果
```

### 4.2 相关性计算

```javascript
function calculateCorrelation(humanScores, aiScores) {
  // Pearson 相关系数
  const n = humanScores.length;
  const sumX = sum(humanScores);
  const sumY = sum(aiScores);
  const sumXY = sum(humanScores.map((x, i) => x * aiScores[i]));
  const sumX2 = sum(humanScores.map(x => x * x));
  const sumY2 = sum(aiScores.map(y => y * y));
  
  const numerator = n * sumXY - sumX * sumY;
  const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
  
  return numerator / denominator;
}
```

### 4.3 权重优化

```javascript
function optimizeWeights(humanScores, aiScores, initialWeights) {
  // 梯度下降优化权重
  let weights = { ...initialWeights };
  const learningRate = 0.01;
  const epochs = 1000;
  
  for (let epoch = 0; epoch < epochs; epoch++) {
    const aiScores = calculateScores(samples, weights);
    const correlation = calculateCorrelation(humanScores, aiScores);
    const gradient = calculateGradient(weights, humanScores, aiScores);
    
    // 更新权重
    weights.novelty -= learningRate * gradient.novelty;
    weights.complexity -= learningRate * gradient.complexity;
    weights.depth -= learningRate * gradient.depth;
    weights.originality -= learningRate * gradient.originality;
    
    // 归一化
    weights = normalizeWeights(weights);
  }
  
  return weights;
}
```

---

## 5. 验收标准

### 5.1 功能验收

- [ ] 新颖性检测准确率 > 85%
- [ ] 复杂性检测准确率 > 85%
- [ ] 深度检测准确率 > 85%
- [ ] 原创性检测准确率 > 85%
- [ ] 综合评分与人工相关性 > 0.8

### 5.2 质量验收

- [ ] 质量评分 ≥ 85 分
- [ ] 测试覆盖率 100%
- [ ] 无严重问题
- [ ] 文档完整度 100%

### 5.3 性能验收

- [ ] 评分速度 < 1 秒/任务
- [ ] 内存占用 < 100MB
- [ ] 并发支持 > 10 任务

---

## 6. 交付物

### 6.1 代码

- [ ] creativity-scorer.js (核心算法)
- [ ] creativity-rules.js (规则库)
- [ ] creativity-calibrator.js (校准工具)
- [ ] test-creativity.js (测试用例)

### 6.2 文档

- [ ] API 文档
- [ ] 使用文档
- [ ] 校准报告
- [ ] 测试报告

### 6.3 数据

- [ ] 测试样本集 (50+)
- [ ] 人工评分数据
- [ ] 算法评分数据
- [ ] 相关性分析报告

---

**ADD 设计完成，开始实施阶段 3！** 🚀

**原则**: 效率优先，保质保量  
**时间计划**: ❌ 禁止  
**质量标准**: ✅ ≥85 分  
**验证机制**: ✅ 自动验证
