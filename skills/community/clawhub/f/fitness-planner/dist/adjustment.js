// 自动调整模块
import * as fs from 'fs';
import * as path from 'path';
import { loadCurrentPlan, saveCurrentPlan } from './recorder.js';
import { loadStats } from './stats.js';
const BASE_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/fitness-planner');
const ADJUSTMENT_FILE = path.join(BASE_DIR, 'adjustment_state.json');
const defaultState = {
    consecutiveSkipped: 0,
    consecutiveTired: 0,
    consecutiveGreat: 0,
    lastAdjustment: null,
    adjustmentHistory: []
};
/**
 * 加载调整状态
 */
export function loadAdjustmentState() {
    if (!fs.existsSync(ADJUSTMENT_FILE)) {
        saveAdjustmentState(defaultState);
        return defaultState;
    }
    return JSON.parse(fs.readFileSync(ADJUSTMENT_FILE, 'utf-8'));
}
/**
 * 保存调整状态
 */
export function saveAdjustmentState(state) {
    fs.writeFileSync(ADJUSTMENT_FILE, JSON.stringify(state, null, 2), 'utf-8');
}
/**
 * 检测异常并返回调整建议
 */
export function detectAnomalies() {
    const state = loadAdjustmentState();
    const stats = loadStats();
    const plan = loadCurrentPlan();
    if (!plan) {
        return { hasAnomaly: false, type: '', message: '', action: 'none' };
    }
    // 检查连续跳过
    if (state.consecutiveSkipped >= 2) {
        return {
            hasAnomaly: true,
            type: 'skipped',
            message: `你已连续 ${state.consecutiveSkipped} 次跳过训练。是太忙了吗？我可以帮你调整计划强度，或者换到更合适的时间。`,
            action: 'inquire'
        };
    }
    // 检查连续太累
    if (state.consecutiveTired >= 3) {
        return {
            hasAnomaly: true,
            type: 'tired',
            message: `最近 ${state.consecutiveTired} 次训练都感觉太累，强度可能过高。我已自动将下周计划降低强度（减少1-2组）。`,
            action: 'reduce'
        };
    }
    // 检查连续状态好
    if (state.consecutiveGreat >= 4) {
        return {
            hasAnomaly: true,
            type: 'great',
            message: `连续 ${state.consecutiveGreat} 次训练状态很好！下周可以尝试增加强度（增加次数或组数）。`,
            action: 'increase'
        };
    }
    return { hasAnomaly: false, type: '', message: '', action: 'none' };
}
/**
 * 更新调整状态（打卡时调用）
 */
export function updateAdjustmentState(record) {
    const state = loadAdjustmentState();
    const today = new Date().toISOString().split('T')[0];
    // 重置计数
    if (record.feeling === 'tired') {
        state.consecutiveTired += 1;
        state.consecutiveGreat = 0;
        state.consecutiveSkipped = 0;
    }
    else if (record.feeling === 'great') {
        state.consecutiveGreat += 1;
        state.consecutiveTired = 0;
        state.consecutiveSkipped = 0;
    }
    else {
        state.consecutiveTired = 0;
        state.consecutiveGreat = 0;
        state.consecutiveSkipped = 0;
    }
    saveAdjustmentState(state);
}
/**
 * 记录跳过（未打卡时调用）
 */
export function recordSkip() {
    const state = loadAdjustmentState();
    state.consecutiveSkipped += 1;
    state.consecutiveGreat = 0;
    state.consecutiveTired = 0;
    saveAdjustmentState(state);
}
/**
 * 重置跳过计数（打卡成功后调用）
 */
export function resetSkipCount() {
    const state = loadAdjustmentState();
    state.consecutiveSkipped = 0;
    saveAdjustmentState(state);
}
/**
 * 调整计划强度
 */
export function adjustPlanIntensity(action) {
    const plan = loadCurrentPlan();
    if (!plan) {
        return { success: false, message: '没有当前计划可调整' };
    }
    const adjustment = action === 'reduce' ? -1 : 1;
    const factor = action === 'reduce' ? 0.8 : 1.2;
    // 调整每天的训练
    const adjustedDays = plan.days.map(day => {
        if (day.exercises.length === 0)
            return day;
        return {
            ...day,
            exercises: day.exercises.map(ex => {
                // 调整组数
                const newSets = Math.max(2, Math.min(6, ex.sets + adjustment));
                // 调整次数范围
                let newReps = ex.reps;
                if (action === 'reduce') {
                    // 降低次数：取范围的下限
                    const match = ex.reps.match(/(\d+)-?(\d+)?/);
                    if (match) {
                        const min = parseInt(match[1]);
                        const max = match[2] ? parseInt(match[2]) : min;
                        newReps = `${Math.max(6, min - 2)}-${max - 2}`;
                    }
                }
                else {
                    // 增加次数：取范围的上限
                    const match = ex.reps.match(/(\d+)-?(\d+)?/);
                    if (match) {
                        const min = parseInt(match[1]);
                        const max = match[2] ? parseInt(match[2]) : min;
                        newReps = `${min + 2}-${Math.min(25, max + 3)}`;
                    }
                }
                return {
                    ...ex,
                    sets: newSets,
                    reps: newReps
                };
            })
        };
    });
    const adjustedPlan = {
        ...plan,
        days: adjustedDays
    };
    saveCurrentPlan(adjustedPlan);
    // 记录调整历史
    const state = loadAdjustmentState();
    state.lastAdjustment = new Date().toISOString();
    state.adjustmentHistory.push({
        date: new Date().toISOString().split('T')[0],
        type: action,
        reason: action === 'reduce' ? '连续疲劳反馈' : '连续状态良好'
    });
    saveAdjustmentState(state);
    // 重置计数
    if (action === 'reduce') {
        state.consecutiveTired = 0;
    }
    else {
        state.consecutiveGreat = 0;
    }
    saveAdjustmentState(state);
    const actionText = action === 'reduce' ? '降低' : '提高';
    return {
        success: true,
        message: `✅ 已${actionText}计划强度\n\n主要调整：\n- 组数 ${action === 'reduce' ? '减少' : '增加'} 1 组\n- 次数范围 ${action === 'reduce' ? '降低' : '提高'} 2-3 次`,
        plan: adjustedPlan
    };
}
/**
 * 生成下周计划（带调整）
 */
export function generateNextWeekPlan() {
    const state = loadAdjustmentState();
    const stats = loadStats();
    const currentPlan = loadCurrentPlan();
    // 获取下周一
    const nextMonday = getNextMonday();
    // 基础计划
    let newPlan;
    if (currentPlan) {
        // 复制当前计划，更新日期
        newPlan = {
            ...currentPlan,
            weekStart: nextMonday,
            days: currentPlan.days.map((day, i) => ({
                ...day,
                date: addDays(nextMonday, i)
            }))
        };
        // 根据状态自动调整
        if (state.consecutiveTired >= 2) {
            // 降低强度
            newPlan.days = newPlan.days.map(day => ({
                ...day,
                exercises: day.exercises.map(ex => ({
                    ...ex,
                    sets: Math.max(2, ex.sets - 1)
                }))
            }));
        }
        else if (state.consecutiveGreat >= 3) {
            // 提高强度
            newPlan.days = newPlan.days.map(day => ({
                ...day,
                exercises: day.exercises.map(ex => ({
                    ...ex,
                    sets: Math.min(6, ex.sets + 1)
                }))
            }));
        }
    }
    else {
        return { success: false, message: '没有当前计划，请先生成' };
    }
    saveCurrentPlan(newPlan);
    // 重置状态
    state.consecutiveSkipped = 0;
    state.consecutiveTired = 0;
    state.consecutiveGreat = 0;
    saveAdjustmentState(state);
    return {
        success: true,
        message: `📋 下周计划已生成（${nextMonday} 起）\n\n已根据本周反馈自动调整强度。`,
        plan: newPlan
    };
}
/**
 * 检查是否需要主动询问
 */
export function checkProactiveInquiry() {
    const state = loadAdjustmentState();
    const plan = loadCurrentPlan();
    if (!plan)
        return null;
    // 连续跳过 2 次
    if (state.consecutiveSkipped >= 2) {
        return `注意到你最近跳过了 ${state.consecutiveSkipped} 次训练。是不是太忙了？要不要调整计划？`;
    }
    // 连续太累 2 次
    if (state.consecutiveTired >= 2) {
        return `最近训练感觉比较累，需要我帮你降低强度吗？回复「降低强度」即可。`;
    }
    return null;
}
// 辅助函数
function getNextMonday() {
    const today = new Date();
    const dayOfWeek = today.getDay();
    const daysUntilMonday = dayOfWeek === 0 ? 1 : 8 - dayOfWeek;
    const nextMonday = new Date(today);
    nextMonday.setDate(today.getDate() + daysUntilMonday);
    return nextMonday.toISOString().split('T')[0];
}
function addDays(dateStr, days) {
    const date = new Date(dateStr);
    date.setDate(date.getDate() + days);
    return date.toISOString().split('T')[0];
}
