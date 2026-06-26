# Agent System 参考实现

> 本目录包含 Agent 系统的参考代码实现

## 文件说明

| 文件 | 说明 |
|------|------|
| `orchestrator-reference.md` | 本文件，代码架构参考 |
| `orchestrator.js` | Node.js 完整实现（约300行） |
| `test.js` | 测试脚本 |

## 核心模块

### Orchestrator (调度器)

```javascript
export async function dispatch(input) {
    // 1. Planner 复杂度评估
    const plan = await callAgent('planner', { text: input });
    
    // 2. 根据复杂度路由
    if (plan.complexity <= 3) {
        return await callAgent('executor', { task: plan.tasks[0], context: plan.raw });
    }
    
    // 3. 复杂任务：规划 → 执行 → 审查 → [自愈]
    // ... 完整逻辑见 orchestrator.js
}
```

### Planner Agent

```javascript
async function planner(input) {
    // 意图识别
    const intentKeywords = {
        'analysis': ['分析', '原因', '为什么'],
        'generation': ['写', '生成', '创建'],
        'coding': ['代码', '编程', '开发'],
        'decision': ['选择', '决定', '比较'],
        'planning': ['计划', '安排', '规划']
    };
    
    // 复杂度评估
    const complexIndicators = ['分析', '原因', '比较', '规划', '设计', '系统'];
    const count = complexIndicators.filter(w => text.includes(w)).length;
    const complexity = count >= 3 ? 8 : count >= 2 ? 6 : count >= 1 ? 4 : 3;
    
    // 任务拆解
    const tasks = complexity > 5 ? [
        { task_id: 't1', type: 'analysis', description: '收集并整理信息' },
        { task_id: 't2', type: 'analysis', description: '识别关键维度' },
        { task_id: 't3', type: 'generate', description: '生成最终结果' }
    ] : [
        { task_id: 't1', type: 'generate', description: '直接生成结果' }
    ];
    
    return { success: true, intent, complexity, tasks };
}
```

### Reviewer Agent

```javascript
async function reviewer(input) {
    const { content } = input;
    
    // 占位符检测
    const hasPlaceholder = /\{[^}]+\}/.test(content || '');
    const hasProhibited = /请提供|你可以告诉我|我需要更多信息/.test(content || '');
    
    // 评分
    let score = 85;
    if (hasPlaceholder) score -= 40;
    if (hasProhibited) score -= 30;
    if (!content || content.length < 10) score -= 50;
    
    return {
        success: true,
        score,
        is_valid: score >= 70,
        should_trigger_heal: score < 70 || hasPlaceholder
    };
}
```

### Self-Heal Engine

```javascript
async function selfHeal(input) {
    const { original_output, retry_count = 0 } = input;
    
    // 策略隔离
    const strategy = retry_count === 0 ? 'detailed_reasoning' : 'reverse_reasoning';
    
    return {
        success: true,
        content: `[已自愈 · 策略: ${strategy}] ${original_output}`,
        strategy,
        retry_count: retry_count + 1,
        degraded_mode: retry_count >= 2
    };
}
```

## 测试验证

```bash
node test.js
```

预期输出：
```
📝 测试: 复杂任务 - 销售分析
   Intent: analysis
   Complexity: 6
   Tasks: 3
   ✅ 通过
```
