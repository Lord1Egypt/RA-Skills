/**
 * OpenClaw Agent System - Planner Kernel v3
 * 基于 Planner Kernel 协议
 * 
 * ============================================
 * GLOBAL RULES (系统级总控)
 * ============================================
 * 1. All outputs must be JSON
 * 2. No agent executes tasks outside its role
 * 3. All tasks go through:
 *    Planner → Dispatch → Executor → Reviewer
 * 4. Token Control is mandatory
 * 5. Failed tasks must trigger Self-Heal
 * 6. Logs must be recorded for Evolve
 * 
 * Violation = system failure
 * ============================================
 */

const LOG = [];

function log(level, event, details = {}) {
    LOG.push({ timestamp: new Date().toISOString(), level, event, details });
}

// ==================== 意图识别 ====================

function recognizeIntent(text) {
    const patterns = {
        'analysis': ['分析', '原因', '为什么'],
        'generation': ['写', '生成', '创建', '编写'],
        'coding': ['代码', '编程', '开发'],
        'decision': ['选择', '决定', '比较'],
        'planning': ['计划', '规划', '安排']
    };
    for (const [intent, keywords] of Object.entries(patterns)) {
        if (keywords.some(k => text.includes(k))) return intent;
    }
    return 'unknown';
}

// ==================== 复杂度评估 ====================

function assessComplexity(text) {
    const weights = {
        // 核心分析词 - 高权重
        '分析': 3, '原因': 3, '为什么': 3,
        // 复杂任务词
        '比较': 2, '规划': 2, '设计': 2, '系统': 2,
        '复杂': 3, '全面': 2, '详细': 2, '深入': 2,
        // 执行类词
        '执行': 1, '处理': 1, '完成': 1
    };
    
    let score = 1; // 基础分
    for (const [word, weight] of Object.entries(weights)) {
        if (text.includes(word)) score += weight;
    }
    
    // 阈值调整
    if (score >= 7) return 'high';
    if (score >= 3) return 'medium';
    return 'low';
}

// ==================== Token 估算 ====================

function estimateTokens(text) {
    return Math.ceil(text.length / 2);
}

// ==================== Planner Kernel ====================

export function planner(input) {
    log('INFO', 'planner_start', {});
    
    const text = String(input || '');
    const intent = recognizeIntent(text);
    const complexity = assessComplexity(text);
    const estimatedTokens = estimateTokens(text) * 3; // 任务数 × 平均
    
    let tasks = [];
    
    if (complexity === 'high') {
        tasks = [
            { id: 'T1', description: '收集并整理相关信息', parallel: false },
            { id: 'T2', description: '识别关键维度和模式', parallel: false },
            { id: 'T3', description: '生成最终结果和建议', parallel: false }
        ];
    } else if (complexity === 'medium') {
        tasks = [
            { id: 'T1', description: '处理任务请求', parallel: false },
            { id: 'T2', description: '验证和优化结果', parallel: true }
        ];
    } else {
        tasks = [
            { id: 'T1', description: '直接执行任务', parallel: false }
        ];
    }
    
    const result = {
        goal: `${intent}: ${text.substring(0, 50)}`,
        intent,
        complexity,
        tasks,
        estimated_tokens: Math.min(estimatedTokens, 2000)
    };
    
    log('INFO', 'planner_complete', { task_count: tasks.length });
    
    return JSON.stringify(result, null, 2);
}

// ==================== Executor Agent ====================

export function executor(taskInput) {
    log('INFO', 'executor_start', {});
    
    const input = taskInput?.description || taskInput || '';
    
    const result = {
        task_id: `exec_${Date.now()}`,
        status: 'success',
        result: `[EXEC] ${input}`,
        error: null
    };
    
    log('INFO', 'executor_complete', {});
    return JSON.stringify(result, null, 2);
}

// ==================== Reviewer Agent ====================

export function reviewer(reviewInput) {
    log('INFO', 'reviewer_start', {});
    
    const content = reviewInput?.result || '';
    let score = 85;
    const issues = [];
    
    if (/\{[^}]+\}/.test(content)) { score -= 40; issues.push('占位符未填充'); }
    if (/请提供|我需要更多信息/.test(content)) { score -= 30; issues.push('包含禁止提问语句'); }
    if (!content || content.length < 10) { score -= 50; issues.push('内容为空'); }
    
    const result = {
        task_id: `review_${Date.now()}`,
        score,
        issues,
        suggestion: score < 70 ? 'needs_retry' : 'approved',
        needs_retry: score < 70
    };
    
    log('INFO', 'reviewer_complete', { score });
    return JSON.stringify(result, null, 2);
}

// ==================== Token Controller ====================

const MAX_TOKENS = 2000;

export function tokenControl(content) {
    if (!content) return { final_text: '', tokens_used: 0, truncated: false };
    
    // 估算 token（1 token ≈ 2 字符）
    const tokens_used = Math.ceil(content.length / 2);
    
    if (tokens_used <= MAX_TOKENS) {
        return { final_text: content, tokens_used, truncated: false };
    }
    
    // 优先级保留：结论 > 关键结果 > 推理过程 > 示例
    // 截断策略：保留开头和结尾的关键部分
    const preservedLength = MAX_TOKENS * 2;
    const truncated = content.substring(0, preservedLength) + '\n...[已截断]\n\n[部分内容因超过Token限制被省略]...';
    
    return { final_text: truncated, tokens_used: MAX_TOKENS, truncated: true };
}

// ==================== Evolve Agent ====================

// 全局学习状态
const LEARNING_STATE = {
    failure_log: [],
    success_log: [],
    thresholds: {
        failure_count: 3,
        retry_weight: 1.0,
        decomposition_granularity: 'medium'
    }
};

export function evolve(input) {
    log('INFO', 'evolve_start', {});
    
    const { failure_log = [], success_log = [] } = input || {};
    
    // 合并日志
    const allFailures = [...LEARNING_STATE.failure_log, ...failure_log];
    const allSuccess = [...LEARNING_STATE.success_log, ...success_log];
    
    // 统计失败模式
    const failurePatterns = {};
    for (const f of allFailures) {
        const pattern = f.pattern || f.error || 'unknown';
        failurePatterns[pattern] = (failurePatterns[pattern] || 0) + 1;
    }
    
    // 识别高频失败
    const patterns = Object.entries(failurePatterns)
        .filter(([_, count]) => count >= 2)
        .map(([pattern, count]) => ({ pattern, count }));
    
    // 根因分析
    const rootCauses = [];
    for (const [pattern, count] of Object.entries(failurePatterns)) {
        if (count >= LEARNING_STATE.thresholds.failure_count) {
            rootCauses.push({
                cause: pattern,
                frequency: count,
                severity: count >= 5 ? 'high' : 'medium'
            });
        }
    }
    
    // 优化建议
    const optimizations = [];
    
    // 基于失败模式生成优化
    if (patterns.some(p => p.pattern.includes('timeout'))) {
        optimizations.push({
            target: 'executor',
            action: '增加超时时间或添加重试逻辑',
            priority: 'high'
        });
    }
    
    if (patterns.some(p => p.pattern.includes('占位符'))) {
        optimizations.push({
            target: 'planner',
            action: '加强输入验证，拒绝未填充占位符的请求',
            priority: 'high'
        });
    }
    
    if (rootCauses.length > 0) {
        optimizations.push({
            target: 'dispatch',
            action: `增加重试权重 x1.2`,
            priority: 'medium'
        });
    }
    
    // 检查是否需要自动学习
    const shouldAutoLearn = allFailures.length > LEARNING_STATE.thresholds.failure_count;
    
    if (shouldAutoLearn) {
        log('WARNING', 'auto_learning_triggered', { 
            failures: allFailures.length,
            optimizations: optimizations.length
        });
        
        // 自动调整阈值
        LEARNING_STATE.thresholds.retry_weight *= 1.1;
        
        // 调整任务分解粒度
        if (allFailures.length >= 10) {
            LEARNING_STATE.thresholds.decomposition_granularity = 'fine';
        }
    }
    
    // 更新学习状态
    LEARNING_STATE.failure_log = allFailures.slice(-100); // 保留最近100条
    LEARNING_STATE.success_log = allSuccess.slice(-100);
    
    const result = {
        patterns,
        root_causes: rootCauses,
        optimizations,
        learning_state: {
            total_failures: allFailures.length,
            total_successes: allSuccess.length,
            retry_weight: LEARNING_STATE.thresholds.retry_weight,
            decomposition_granularity: LEARNING_STATE.thresholds.decomposition_granularity,
            auto_learning_triggered: shouldAutoLearn
        }
    };
    
    log('INFO', 'evolve_complete', { 
        patterns: patterns.length,
        optimizations: optimizations.length 
    });
    
    return JSON.stringify(result, null, 2);
}

// ==================== 主调度流程 ====================

export async function dispatch(input) {
    log('INFO', 'dispatch_start', {});
    
    // Step 1: Planner 生成计划
    const planStr = planner(input);
    const plan = JSON.parse(planStr);
    
    const results = {};
    
    // Step 2: 按顺序执行任务
    for (const task of plan.tasks) {
        const execStr = executor({ description: task.description });
        const exec = JSON.parse(execStr);
        results[task.id] = exec.result;
        
        // 审查
        const reviewStr = reviewer({ result: exec.result });
        const review = JSON.parse(reviewStr);
        
        if (review.needs_retry) {
            for (let i = 0; i < 2; i++) {
                const retry = executor({ description: task.description });
                const retryReview = reviewer({ result: JSON.parse(retry).result });
                if (!retryReview.needs_retry) break;
            }
        }
    }
    
    // Step 3: 合并结果
    const finalContent = Object.values(results).join('\n---\n');
    const tokenized = tokenControl(finalContent);
    
    log('INFO', 'dispatch_complete', {});
    
    // ✅ Runtime Hook: 始终通过 Token Controller
    const final = tokenControl(finalContent);
    
    return JSON.stringify({
        success: true,
        plan,
        content: final.final_text,
        metrics: {
            tokens_used: final.tokens_used,
            truncated: final.truncated,
            quality_score: 85
        }
    }, null, 2);
}

export function getLogs() { return LOG; }
export function clearLogs() { LOG.length = 0; }
export function getLearningState() { return LEARNING_STATE; }

// ==================== Metrics Aggregator ====================

export function metricsAggregator(logs) {
    log('INFO', 'metrics_start', {});
    
    const executions = logs || LOG;
    
    let success = 0, total = 0;
    let totalScore = 0;
    let retries = 0;
    let totalTokens = 0;
    
    for (const entry of executions) {
        if (entry.event === 'dispatch_complete') {
            total++;
            if (entry.details?.success !== false) success++;
            if (entry.details?.retry) retries++;
            totalTokens += entry.details?.tokens || 0;
            totalScore += entry.details?.quality_score || 0;
        }
    }
    
    const result = {
        success_rate: total > 0 ? success / total : 0,
        avg_score: total > 0 ? Math.round(totalScore / total) : 0,
        retry_rate: total > 0 ? retries / total : 0,
        token_avg: total > 0 ? Math.round(totalTokens / total) : 0,
        total_executions: total
    };
    
    log('INFO', 'metrics_complete', result);
    return JSON.stringify(result, null, 2);
}

// ==================== Self-Heal Agent (扩展) ====================

export function selfHeal(input) {
    log('INFO', 'selfheal_start', {});
    
    const { failed_task, error_message } = input || {};
    
    // 错误分类
    let errorType = 'unknown';
    if (/timeout|timed?out|超时/.test(error_message || '')) {
        errorType = 'rate_limit';
    } else if (/undefined|null|cannot read|找不到/.test(error_message || '')) {
        errorType = 'logic_error';
    } else if (/api|service|服务/.test(error_message || '')) {
        errorType = 'tool_error';
    }
    
    // 策略选择
    let action = 'retry';
    let newTask = failed_task;
    let reason = '';
    
    switch (errorType) {
        case 'rate_limit':
            action = 'retry';
            reason = '限流，等待后重试';
            break;
        case 'logic_error':
            action = 'replan';
            reason = '逻辑错误，重新规划任务';
            break;
        case 'tool_error':
            action = 'simplify';
            reason = '工具错误，简化任务';
            newTask = `简化版：${failed_task}`;
            break;
        default:
            action = 'retry';
            reason = '未知错误，重试';
    }
    
    const result = {
        action,
        new_task: newTask,
        reason,
        error_type: errorType
    };
    
    log('INFO', 'selfheal_complete', result);
    return JSON.stringify(result, null, 2);
}

// ==================== 统一类型封装 ====================

export function wrapResponse(type, data) {
    return JSON.stringify({ type, data, timestamp: new Date().toISOString() });
}

// ==================== 统一异常处理 ====================

export function withErrorHandling(fn, name = 'unknown') {
    return function(...args) {
        try {
            return fn(...args);
        } catch (error) {
            log('ERROR', `${name}_error`, { message: error.message });
            return JSON.stringify({
                status: 'fail',
                error_type: error.name || 'Error',
                message: error.message
            });
        }
    };
}

export default { planner, executor, reviewer, evolve, tokenControl, dispatch, getLogs, clearLogs, getLearningState, metricsAggregator, selfHeal, wrapResponse, withErrorHandling };
