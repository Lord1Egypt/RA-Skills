/**
 * 🌪️ do-it 技能 - AI 判断能力实现
 * 
 * 使用方法：
 * const result = await doItAnalyze(problem, situation);
 */

// 判断决策 Prompt 模板
const DO_IT_PROMPT = `
# 🌪️ do it - AI 判断助手

## 你的角色
你是一个判断决策型 AI，名字叫"滚滚"。

## 你的特点
- 客观分析问题，不受情绪影响
- 逻辑清晰，利弊权衡
- 给出明确建议，不模棱两可
- 真诚直接，不说假话
- 持续陪伴，不管结果如何

## 你的判断原则

### 1. 长期主义
- 不看眼前得失，看长期发展
- 不看短期痛苦，看长期收益

### 2. 价值匹配
- 用户的能力值多少钱，就赚多少钱
- 不要委屈自己，不要低估自己

### 3. 成长优先
- 选择能让用户成长的
- 选择能让用户变得更好的

### 4. 情感健康
- 远离消耗用户的人
- 靠近滋养用户的人

### 5. 可逆性原则
- 如果选择可逆，大胆尝试
- 如果选择不可逆，谨慎决策

### 6. 最坏情况
- 问自己：最坏的结果是什么？
- 如果能承受，就去做

## 输出格式
请按照以下格式输出判断结果：

# 🌪️ do it - 滚滚的判断

## 你的问题
[复述问题，确保理解正确]

## 滚滚的分析

### 方案 A：[名称]
**优势：**
- ...

**劣势：**
- ...

**风险：**
- ...

**机会：**
- ...

### 方案 B：[名称]
[同上]

## 滚滚的判断

### ✅ 推荐选择：[方案 X]

**理由：**
1. ...
2. ...
3. ...

**核心原因：**
[一句话总结为什么选这个]

## 执行建议

### 第一步（本周）
- [ ] ...

### 第二步（本月）
- [ ] ...

### 第三步（3 个月）
- [ ] ...

## 风险提示

**可能遇到的问题：**
- ...

**应对方案：**
- ...

## 滚滚的话

[滚滚的真心话，鼓励和支持]

---

**记住：**
- 滚滚的判断仅供参考
- 你保留最终决定权
- 不管结果如何，滚滚都在
`;

/**
 * 分析问题并给出判断
 * @param {string} problem - 用户的问题
 * @param {object} situation - 用户的情况
 * @param {string} situation.current - 当前状态
 * @param {string[]} situation.options - 可选方案
 * @param {string} situation.concerns - 顾虑
 * @param {string} situation.preference - 偏好
 * @param {string} additionalInfo - 补充信息
 * @returns {Promise<object>} 判断结果
 */
async function doItAnalyze(problem, situation, additionalInfo = '') {
  // 构建完整的用户输入
  const userInput = `
## 我的问题
${problem}

## 我的情况
- **当前状态：** ${situation.current}
- **可选方案：** ${situation.options.join(' / ')}
- **我的顾虑：** ${situation.concerns}
- **我的偏好：** ${situation.preference || '暂无'}

## 补充信息
${additionalInfo || '无'}
`;

  // 调用 AI API（这里用示例，实际调用时替换为真实 API）
  const response = await fetch('/api/ai/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: DO_IT_PROMPT,
      user_input: userInput,
      model: 'qwen3.5-plus',
      temperature: 0.7,
      max_tokens: 2000
    })
  });

  const result = await response.json();
  
  return {
    success: true,
    data: {
      analysis: result.analysis,
      recommendation: extractRecommendation(result.analysis),
      reasons: extractReasons(result.analysis),
      action_plan: extractActionPlan(result.analysis),
      risks: extractRisks(result.analysis)
    }
  };
}

/**
 * 从分析结果中提取推荐
 */
function extractRecommendation(analysis) {
  const match = analysis.match(/### ✅ 推荐选择：(.+)/);
  return match ? match[1].trim() : '无法确定';
}

/**
 * 从分析结果中提取理由
 */
function extractReasons(analysis) {
  const reasons = [];
  const reasonMatch = analysis.match(/\*\*理由：\*\*([\s\S]*?)(?=\*\*核心原因：|$)/);
  if (reasonMatch) {
    const lines = reasonMatch[1].split('\n').filter(line => line.trim().match(/^\d+\./));
    lines.forEach(line => {
      reasons.push(line.replace(/^\d+\.\s*/, ''));
    });
  }
  return reasons;
}

/**
 * 从分析结果中提取行动计划
 */
function extractActionPlan(analysis) {
  const plan = {
    week: [],
    month: [],
    quarter: []
  };
  
  const weekMatch = analysis.match(/### 第一步（本周）([\s\S]*?)(?=### 第二步|$)/);
  const monthMatch = analysis.match(/### 第二步（本月）([\s\S]*?)(?=### 第三步|$)/);
  const quarterMatch = analysis.match(/### 第三步（3 个月）([\s\S]*?)(?=## 风险提示|$)/);
  
  if (weekMatch) {
    plan.week = extractChecklist(weekMatch[1]);
  }
  if (monthMatch) {
    plan.month = extractChecklist(monthMatch[1]);
  }
  if (quarterMatch) {
    plan.quarter = extractChecklist(quarterMatch[1]);
  }
  
  return plan;
}

/**
 * 提取清单项目
 */
function extractChecklist(text) {
  const items = [];
  const lines = text.split('\n').filter(line => line.trim().match(/^- \[ \]/));
  lines.forEach(line => {
    items.push(line.replace(/^- \[ \] /, ''));
  });
  return items;
}

/**
 * 从分析结果中提取风险
 */
function extractRisks(analysis) {
  const risks = {
    problems: [],
    solutions: []
  };
  
  const problemsMatch = analysis.match(/\*\*可能遇到的问题：\*\*([\s\S]*?)(?=\*\*应对方案：|$)/);
  const solutionsMatch = analysis.match(/\*\*应对方案：\*\*([\s\S]*?)(?=## 滚滚的话|$)/);
  
  if (problemsMatch) {
    risks.problems = problemsMatch[1].split('\n').filter(line => line.trim().match(/^- /)).map(l => l.replace(/^- /, ''));
  }
  if (solutionsMatch) {
    risks.solutions = solutionsMatch[1].split('\n').filter(line => line.trim().match(/^- /)).map(l => l.replace(/^- /, ''));
  }
  
  return risks;
}

// 导出函数
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    doItAnalyze,
    DO_IT_PROMPT
  };
}
