// 周期化训练、肌群进展、多维度反馈模块
import * as fs from 'fs';
import * as path from 'path';
import { getWeekStart } from './templates.js';
const BASE_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/fitness-planner');
const PERIODIZATION_FILE = path.join(BASE_DIR, 'periodization_state.json');
const MUSCLE_PROGRESS_FILE = path.join(BASE_DIR, 'muscle_progress.json');
const FEEDBACK_FILE = path.join(BASE_DIR, 'feedback_state.json');
// ==================== 肌群映射 ====================
export const muscleGroupNames = {
    chest: '胸肌',
    back: '背部',
    shoulder: '肩部',
    biceps: '二头肌',
    triceps: '三头肌',
    leg: '腿部',
    core: '核心',
    cardio: '有氧'
};
// 动作到肌群的映射
const exerciseToMuscle = {
    // 胸肌
    '卧推': ['chest', 'triceps'],
    '哑铃卧推': ['chest', 'triceps'],
    '上斜哑铃卧推': ['chest', 'triceps'],
    '哑铃上斜卧推': ['chest', 'triceps'],
    '哑铃飞鸟': ['chest'],
    '俯卧撑': ['chest', 'triceps'],
    '下斜俯卧撑': ['chest', 'triceps'],
    '窄距俯卧撑': ['triceps', 'chest'],
    // 背部
    '引体向上': ['back', 'biceps'],
    '反手引体向上': ['biceps', 'back'],
    '正手引体向上': ['back', 'biceps'],
    '高位下拉': ['back', 'biceps'],
    '杠铃划船': ['back', 'biceps'],
    '哑铃划船': ['back', 'biceps'],
    // 肩部
    '肩推': ['shoulder', 'triceps'],
    '哑铃侧平举': ['shoulder'],
    '哑铃前平举': ['shoulder'],
    '俯身飞鸟': ['shoulder'],
    '面拉': ['shoulder', 'back'],
    // 二头肌
    '杠铃弯举': ['biceps'],
    '哑铃弯举': ['biceps'],
    '锤式弯举': ['biceps'],
    '集中弯举': ['biceps'],
    '21响礼炮': ['biceps'],
    '哑铃交替弯举': ['biceps'],
    // 三头肌
    '绳索下压': ['triceps'],
    '窄握卧推': ['triceps', 'chest'],
    '仰卧臂屈伸': ['triceps'],
    '哑铃颈后臂屈伸': ['triceps'],
    '双杠臂屈伸': ['triceps', 'chest'],
    // 腿部
    '深蹲': ['leg'],
    '高脚杯深蹲': ['leg'],
    '哑铃深蹲': ['leg'],
    '罗马尼亚硬拉': ['leg'],
    '腿举': ['leg'],
    '腿弯举': ['leg'],
    '弓步蹲': ['leg'],
    '臀桥': ['leg'],
    '提踵': ['leg'],
    // 核心
    '平板支撑': ['core'],
    '卷腹': ['core'],
    '悬垂举腿': ['core', 'back'],
    '俄罗斯转体': ['core'],
    '死虫': ['core'],
    // 有氧
    '跑步': ['cardio'],
    '开合跳': ['cardio'],
    '波比跳': ['cardio', 'core'],
    '登山跑': ['cardio', 'core'],
    '深蹲跳': ['leg', 'cardio'],
    '高抬腿': ['cardio']
};
// ==================== 周期化训练 ====================
const defaultPeriodizationState = {
    currentPhase: {
        type: 'hypertrophy',
        weekNumber: 1,
        totalWeeks: 4,
        startDate: new Date().toISOString().split('T')[0],
        endDate: '',
        intensity: 'medium',
        description: '肌肥大训练阶段'
    },
    phaseHistory: [],
    totalWeeksTrained: 0
};
function loadPeriodizationState() {
    try {
        if (fs.existsSync(PERIODIZATION_FILE)) {
            return JSON.parse(fs.readFileSync(PERIODIZATION_FILE, 'utf-8'));
        }
    }
    catch (e) {
        // ignore
    }
    // 初始化默认状态
    const state = { ...defaultPeriodizationState };
    state.currentPhase.endDate = calculatePhaseEndDate(state.currentPhase);
    savePeriodizationState(state);
    return state;
}
function savePeriodizationState(state) {
    fs.writeFileSync(PERIODIZATION_FILE, JSON.stringify(state, null, 2), 'utf-8');
}
function calculatePhaseEndDate(phase) {
    const start = new Date(phase.startDate);
    start.setDate(start.getDate() + phase.totalWeeks * 7 - 1);
    return start.toISOString().split('T')[0];
}
/**
 * 获取阶段描述
 */
function getPhaseDescription(type) {
    const descriptions = {
        strength: '力量训练阶段 - 大重量低次数，提升最大力量',
        hypertrophy: '肌肥大训练阶段 - 中等重量中等次数，促进肌肉生长',
        endurance: '耐力训练阶段 - 轻重量高次数，提升肌肉耐力',
        deload: '减载周 - 降低训练量，促进恢复'
    };
    return descriptions[type];
}
/**
 * 获取阶段强度参数
 */
function getPhaseParameters(type) {
    const params = {
        strength: { setsMultiplier: 0.8, repsRange: { min: 4, max: 6 }, restMultiplier: 1.5 },
        hypertrophy: { setsMultiplier: 1.0, repsRange: { min: 8, max: 12 }, restMultiplier: 1.0 },
        endurance: { setsMultiplier: 1.2, repsRange: { min: 15, max: 20 }, restMultiplier: 0.8 },
        deload: { setsMultiplier: 0.6, repsRange: { min: 10, max: 15 }, restMultiplier: 1.2 }
    };
    return params[type];
}
/**
 * 根据阶段调整训练计划
 */
export function adjustPlanForPhase(plan, phase) {
    const params = getPhaseParameters(phase.type);
    const adjustedDays = plan.days.map(day => ({
        ...day,
        exercises: day.exercises.map(ex => {
            // 调整组数
            const newSets = Math.max(2, Math.round(ex.sets * params.setsMultiplier));
            // 调整次数范围
            let newReps = ex.reps;
            if (phase.type === 'strength') {
                newReps = `${params.repsRange.min}-${params.repsRange.max}`;
            }
            else if (phase.type === 'endurance') {
                newReps = `${params.repsRange.min}-${params.repsRange.max}`;
            }
            else if (phase.type === 'deload') {
                newReps = `${params.repsRange.min}-${params.repsRange.max}`;
            }
            // 调整休息时间
            let newRest = ex.rest;
            if (phase.type === 'strength') {
                newRest = '120-180s';
            }
            else if (phase.type === 'endurance') {
                newRest = '45s';
            }
            else if (phase.type === 'deload') {
                newRest = '90s';
            }
            return {
                ...ex,
                sets: newSets,
                reps: newReps,
                rest: newRest
            };
        })
    }));
    return { ...plan, days: adjustedDays };
}
/**
 * 推进到下一阶段
 */
export function advancePhase() {
    const state = loadPeriodizationState();
    // 保存当前阶段到历史
    state.phaseHistory.push(state.currentPhase);
    state.totalWeeksTrained += state.currentPhase.weekNumber;
    // 决定下一阶段
    const nextType = getNextPhaseType(state.currentPhase.type, state.phaseHistory);
    // 创建新阶段
    const newPhase = {
        type: nextType,
        weekNumber: 1,
        totalWeeks: nextType === 'deload' ? 1 : 4,
        startDate: getWeekStart(),
        endDate: '',
        intensity: nextType === 'deload' ? 'low' : nextType === 'strength' ? 'high' : 'medium',
        description: getPhaseDescription(nextType)
    };
    newPhase.endDate = calculatePhaseEndDate(newPhase);
    state.currentPhase = newPhase;
    savePeriodizationState(state);
    const phaseNames = {
        strength: '力量期',
        hypertrophy: '肌肥大期',
        endurance: '耐力期',
        deload: '减载周'
    };
    return {
        message: `🔄 进入新的训练阶段：${phaseNames[newPhase.type]}\n\n${newPhase.description}\n\n时长：${newPhase.totalWeeks} 周`,
        newPhase
    };
}
function getNextPhaseType(current, history) {
    // 标准周期：力量 → 肌肥大 → 力量 → 减载
    const cycle = ['strength', 'hypertrophy', 'endurance', 'deload'];
    const currentIndex = cycle.indexOf(current);
    // 如果刚完成减载周，根据目标选择下一阶段
    if (current === 'deload') {
        // 检查之前的训练历史，选择最需要的阶段
        return 'hypertrophy'; // 默认从肌肥大开始
    }
    return cycle[(currentIndex + 1) % cycle.length];
}
/**
 * 获取当前阶段信息
 */
export function getCurrentPhase() {
    const state = loadPeriodizationState();
    return state.currentPhase;
}
/**
 * 更新阶段周数
 */
export function incrementPhaseWeek() {
    const state = loadPeriodizationState();
    state.currentPhase.weekNumber += 1;
    // 检查是否需要进入下一阶段
    if (state.currentPhase.weekNumber > state.currentPhase.totalWeeks) {
        advancePhase();
    }
    else {
        savePeriodizationState(state);
    }
}
// ==================== 肌群进展追踪 ====================
function getDefaultMuscleProgress() {
    const muscles = {};
    const groups = ['chest', 'back', 'shoulder', 'biceps', 'triceps', 'leg', 'core', 'cardio'];
    for (const muscle of groups) {
        muscles[muscle] = {
            muscle,
            totalSets: 0,
            totalReps: 0,
            lastTrained: null,
            weeklyFrequency: 0,
            strengthProgress: 0,
            hypertrophyProgress: 0,
            sorenessLevel: 0,
            lastSoreness: null,
            personalRecords: []
        };
    }
    return {
        muscles,
        lastUpdated: new Date().toISOString()
    };
}
export function loadMuscleProgress() {
    try {
        if (fs.existsSync(MUSCLE_PROGRESS_FILE)) {
            return JSON.parse(fs.readFileSync(MUSCLE_PROGRESS_FILE, 'utf-8'));
        }
    }
    catch (e) {
        // ignore
    }
    const state = getDefaultMuscleProgress();
    saveMuscleProgress(state);
    return state;
}
function saveMuscleProgress(state) {
    state.lastUpdated = new Date().toISOString();
    fs.writeFileSync(MUSCLE_PROGRESS_FILE, JSON.stringify(state, null, 2), 'utf-8');
}
/**
 * 获取动作涉及的目标肌群
 */
export function getExerciseMuscles(exerciseName) {
    for (const [name, muscles] of Object.entries(exerciseToMuscle)) {
        if (exerciseName.includes(name) || name.includes(exerciseName)) {
            return muscles;
        }
    }
    return ['chest']; // 默认胸肌
}
/**
 * 记录肌群训练
 */
export function recordMuscleTraining(exercises) {
    const state = loadMuscleProgress();
    const today = new Date().toISOString().split('T')[0];
    for (const ex of exercises) {
        const muscles = getExerciseMuscles(ex.name);
        const reps = parseReps(ex.reps);
        for (const muscle of muscles) {
            const progress = state.muscles[muscle];
            progress.totalSets += ex.sets;
            progress.totalReps += ex.sets * reps;
            progress.lastTrained = today;
        }
    }
    saveMuscleProgress(state);
}
function parseReps(repsStr) {
    const match = repsStr.match(/(\d+)/);
    return match ? parseInt(match[1]) : 10;
}
/**
 * 记录肌群酸痛
 */
export function recordSoreness(muscles, level) {
    const state = loadMuscleProgress();
    const today = new Date().toISOString().split('T')[0];
    for (const muscle of muscles) {
        state.muscles[muscle].sorenessLevel = level;
        state.muscles[muscle].lastSoreness = today;
    }
    saveMuscleProgress(state);
}
/**
 * 分析肌群训练不平衡
 */
export function analyzeMuscleBalance() {
    const state = loadMuscleProgress();
    const today = new Date();
    const undertrained = [];
    const overtrained = [];
    const recovered = [];
    const recommendations = [];
    for (const [muscle, progress] of Object.entries(state.muscles)) {
        // 检查是否很久没训练
        if (progress.lastTrained) {
            const lastTrainedDate = new Date(progress.lastTrained);
            const daysSinceLastTrained = Math.floor((today.getTime() - lastTrainedDate.getTime()) / (1000 * 60 * 60 * 24));
            if (daysSinceLastTrained > 7 && muscle !== 'cardio') {
                undertrained.push(muscle);
                recommendations.push(`${muscleGroupNames[muscle]}已 ${daysSinceLastTrained} 天未训练，建议安排训练`);
            }
        }
        else {
            undertrained.push(muscle);
        }
        // 检查是否酸痛未恢复
        if (progress.sorenessLevel >= 7 && progress.lastSoreness) {
            const lastSorenessDate = new Date(progress.lastSoreness);
            const daysSinceSoreness = Math.floor((today.getTime() - lastSorenessDate.getTime()) / (1000 * 60 * 60 * 24));
            if (daysSinceSoreness < 3) {
                overtrained.push(muscle);
                recommendations.push(`${muscleGroupNames[muscle]}酸痛较重，建议再休息 ${3 - daysSinceSoreness} 天`);
            }
        }
        // 检查是否已恢复
        if (progress.sorenessLevel <= 3 && progress.lastTrained) {
            recovered.push(muscle);
        }
    }
    return { undertrained, overtrained, recovered, recommendations };
}
/**
 * 根据肌群进展推荐动作调整
 */
export function recommendExerciseAdjustments(plan) {
    const analysis = analyzeMuscleBalance();
    const addExercises = [];
    const removeExercises = [];
    const notes = [];
    // 检查今日计划的肌群是否适合训练
    for (const ex of plan.exercises) {
        const muscles = getExerciseMuscles(ex.name);
        for (const muscle of muscles) {
            if (analysis.overtrained.includes(muscle)) {
                removeExercises.push(ex.name);
                notes.push(`⚠️ ${ex.name} 涉及的 ${muscleGroupNames[muscle]} 尚未恢复，建议跳过或降低强度`);
            }
        }
    }
    // 建议添加弱势肌群训练
    const targetMuscles = plan.focus.includes('胸') ? ['chest'] :
        plan.focus.includes('背') ? ['back'] :
            plan.focus.includes('肩') ? ['shoulder'] :
                plan.focus.includes('二头') ? ['biceps'] :
                    plan.focus.includes('三头') ? ['triceps'] :
                        plan.focus.includes('腿') ? ['leg'] : [];
    for (const undertrained of analysis.undertrained) {
        if (targetMuscles.includes(undertrained)) {
            notes.push(`💡 可增加 ${muscleGroupNames[undertrained]} 训练量`);
        }
    }
    return { addExercises, removeExercises, notes };
}
// ==================== 多维度反馈 ====================
function getDefaultFeedbackState() {
    return {
        recentFeedback: [],
        averageSleep: 7,
        averageEnergy: 5,
        averageStress: 3,
        recoveryScore: 70
    };
}
export function loadFeedbackState() {
    try {
        if (fs.existsSync(FEEDBACK_FILE)) {
            return JSON.parse(fs.readFileSync(FEEDBACK_FILE, 'utf-8'));
        }
    }
    catch (e) {
        // ignore
    }
    const state = getDefaultFeedbackState();
    saveFeedbackState(state);
    return state;
}
function saveFeedbackState(state) {
    fs.writeFileSync(FEEDBACK_FILE, JSON.stringify(state, null, 2), 'utf-8');
}
/**
 * 记录多维度反馈
 */
export function recordFeedback(feedback) {
    const state = loadFeedbackState();
    // 添加到最近反馈列表
    state.recentFeedback.push(feedback);
    // 只保留最近 30 天的反馈
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    state.recentFeedback = state.recentFeedback.filter(f => new Date(f.date) >= thirtyDaysAgo);
    // 计算平均值
    if (state.recentFeedback.length > 0) {
        state.averageSleep = state.recentFeedback.reduce((sum, f) => sum + f.sleep.hours, 0) / state.recentFeedback.length;
        const energyMap = { low: 3, medium: 5, high: 8 };
        state.averageEnergy = state.recentFeedback.reduce((sum, f) => sum + energyMap[f.energy], 0) / state.recentFeedback.length;
        const stressMap = { low: 2, medium: 5, high: 8 };
        state.averageStress = state.recentFeedback.reduce((sum, f) => sum + stressMap[f.stress], 0) / state.recentFeedback.length;
    }
    // 计算恢复指数
    state.recoveryScore = calculateRecoveryScore(state);
    saveFeedbackState(state);
}
/**
 * 计算恢复指数
 */
function calculateRecoveryScore(state) {
    // 睡眠权重 40%
    const sleepScore = Math.min(100, (state.averageSleep / 8) * 100);
    // 能量权重 30%
    const energyScore = (state.averageEnergy / 10) * 100;
    // 压力权重 30%（反向）
    const stressScore = 100 - (state.averageStress / 10) * 100;
    return Math.round(sleepScore * 0.4 + energyScore * 0.3 + stressScore * 0.3);
}
/**
 * 快速反馈记录
 */
export function recordQuickFeedback(sleepHours, sleepQuality, energy, stress) {
    const feedback = {
        date: new Date().toISOString().split('T')[0],
        sleep: {
            quality: sleepQuality,
            hours: sleepHours
        },
        stress,
        diet: 'fair',
        energy,
        soreness: [],
        motivation: energy === 'high' ? 8 : energy === 'medium' ? 5 : 3
    };
    recordFeedback(feedback);
    return feedback;
}
/**
 * 分析恢复状态并给出建议
 */
export function analyzeRecoveryStatus() {
    const state = loadFeedbackState();
    const score = state.recoveryScore;
    let status;
    const recommendations = [];
    let shouldReduceIntensity = false;
    if (score < 40) {
        status = 'poor';
        shouldReduceIntensity = true;
        recommendations.push('⚠️ 恢复状态较差，建议今天休息或只做轻度活动');
        recommendations.push('确保充足睡眠（7-9小时）');
        if (state.averageStress > 6) {
            recommendations.push('压力较大，可尝试冥想或放松活动');
        }
    }
    else if (score < 60) {
        status = 'fair';
        recommendations.push('💡 恢复状态一般，建议降低训练强度');
        if (state.averageSleep < 7) {
            recommendations.push('睡眠不足，建议早睡');
        }
    }
    else if (score < 80) {
        status = 'good';
        recommendations.push('✅ 恢复状态良好，可以正常训练');
    }
    else {
        status = 'excellent';
        recommendations.push('🌟 状态极佳，可以挑战更高强度');
    }
    return { score, status, recommendations, shouldReduceIntensity };
}
/**
 * 综合分析 - 用于训练前决策
 */
export function getPreWorkoutAnalysis() {
    const phase = getCurrentPhase();
    const recovery = analyzeRecoveryStatus();
    const muscleBalance = analyzeMuscleBalance();
    let overallRecommendation = '';
    // 综合判断
    if (recovery.shouldReduceIntensity) {
        overallRecommendation = `⚠️ 今日建议降低训练强度或休息。原因：${recovery.recommendations[0]}`;
    }
    else if (muscleBalance.overtrained.length > 0) {
        overallRecommendation = `💡 注意：${muscleBalance.overtrained.map(m => muscleGroupNames[m]).join('、')} 尚未完全恢复`;
    }
    else if (recovery.status === 'excellent') {
        overallRecommendation = `🌟 状态很好！今天是挑战 ${phase.type === 'strength' ? '大重量' : phase.type === 'hypertrophy' ? '中等重量' : '高次数'} 的好日子`;
    }
    else {
        overallRecommendation = `✅ 可以正常训练，当前阶段：${phase.description}`;
    }
    return {
        phase,
        recovery,
        muscleBalance,
        overallRecommendation
    };
}
// ==================== 导出辅助函数 ====================
export { loadPeriodizationState, savePeriodizationState };
