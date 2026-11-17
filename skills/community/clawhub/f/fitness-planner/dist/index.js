// 健身规划助手 - 主入口
import { loadConfig, saveConfig, isConfigComplete, getMissingFields, updateUserConfig, parseGender, parseGoal, parseLocation, parseExperience, parseNumber } from './config.js';
import { generateWeekPlan, getWeekStart } from './templates.js';
import { loadCurrentPlan, saveCurrentPlan, recordWorkout, getTodayPlan, isTodayCompleted, getTodayRecord, getWeekRecords, getHistoryRecords, updateFeeling } from './recorder.js';
import { loadStats, updateStats, generateWeeklySummary } from './stats.js';
import { detectAnomalies, updateAdjustmentState, resetSkipCount, adjustPlanIntensity, generateNextWeekPlan } from './adjustment.js';
import { formatWorkoutReminder, formatWorkoutReminderWithVideoLinks, formatCheckinSuccess, formatWeeklySummary, formatWeekProgress, formatStatsMessage, formatExerciseDetail, formatExerciseDetailWithVideo, formatAllExerciseBriefs, formatAllExerciseBriefsWithVideos } from './notifier.js';
// ==================== 主处理器 ====================
/**
 * 处理用户输入
 */
export function handleInput(input) {
    const trimmed = input.trim().toLowerCase();
    const config = loadConfig();
    // 如果配置不完整，优先尝试解析配置
    if (!isConfigComplete(config)) {
        // 检查是否是帮助命令
        if (trimmed.includes('帮助') || trimmed === 'help') {
            return handleHelp();
        }
        // 尝试解析为配置
        const result = parseConfigUpdate(input);
        if (result.success) {
            return result;
        }
        // 返回初始化提示
        return handleInit();
    }
    // 识别命令
    const command = recognizeCommand(trimmed);
    switch (command) {
        case 'init':
            return handleInit();
        case 'plan':
            return handlePlan();
        case 'today':
            return handleToday();
        case 'checkin':
            return handleCheckin();
        case 'feeling':
            return handleFeeling(input);
        case 'progress':
            return handleProgress();
        case 'stats':
            return handleStats();
        case 'summary':
            return handleSummary();
        case 'history':
            return handleHistory();
        case 'config':
            return handleConfig(input);
        case 'adjust':
            return handleAdjust(input);
        case 'nextweek':
            return handleNextWeek();
        case 'exercise':
            return handleExercise(input);
        case 'help':
            return handleHelp();
        default:
            return handleNaturalLanguage(input);
    }
}
/**
 * 识别命令
 */
function recognizeCommand(input) {
    if (input.includes('初始化') || input.includes('开始配置'))
        return 'init';
    if (input.includes('生成计划') || input.includes('安排计划') || input.includes('新计划'))
        return 'plan';
    if (input.includes('今天') || input.includes('今日'))
        return 'today';
    if (input.includes('打卡') || input.includes('完成') || input.includes('练完'))
        return 'checkin';
    if (input.includes('太累') || input.includes('一般') || input.includes('没练够') || input.includes('感觉'))
        return 'feeling';
    if (input.includes('本周') || input.includes('这周') || input.includes('进度'))
        return 'progress';
    if (input.includes('统计') || input.includes('数据'))
        return 'stats';
    if (input.includes('周报') || input.includes('总结'))
        return 'summary';
    if (input.includes('历史') || input.includes('记录'))
        return 'history';
    if (input.includes('配置') || input.includes('设置'))
        return 'config';
    if (input.includes('调整') || input.includes('降低强度') || input.includes('增加强度'))
        return 'adjust';
    if (input.includes('下周') || input.includes('生成下周'))
        return 'nextweek';
    if (input.includes('动作') || input.includes('讲解') || input.includes('教学'))
        return 'exercise';
    if (input.includes('帮助') || input.includes('help'))
        return 'help';
    return 'today';
}
// ==================== 命令处理器 ====================
/**
 * 初始化配置
 */
function handleInit() {
    const config = loadConfig();
    if (isConfigComplete(config)) {
        return {
            success: true,
            message: '你已完成初始化配置。回复「配置」可查看或修改。',
            data: config
        };
    }
    const missing = getMissingFields(config);
    return {
        success: false,
        message: `健身规划助手初始化\n==================\n\n请回答以下问题：\n\n缺失配置：${missing.join('、')}\n\n示例回复：\n「男，28岁，增肌，健身房，每周4天，每次60分钟，中级」`,
        data: config
    };
}
/**
 * 生成计划
 */
function handlePlan() {
    const config = loadConfig();
    if (!isConfigComplete(config)) {
        const missing = getMissingFields(config);
        return {
            success: false,
            message: `请先完成配置。缺失：${missing.join('、')}\n\n示例：「男，28岁，增肌，健身房，每周4天，每次60分钟，中级」`
        };
    }
    const weekStart = getWeekStart();
    const plan = generateWeekPlan({
        experience: config.user.experience,
        goal: config.user.goal,
        location: config.user.location,
        weeklyDays: config.user.weeklyDays
    }, weekStart);
    saveCurrentPlan(plan);
    const lines = [
        `📋 本周训练计划（${weekStart} 起）`,
        '',
        `计划类型：${getPlanTypeName(plan.planType)}`,
        ''
    ];
    const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
    for (const day of plan.days) {
        const isWorkout = day.exercises.length > 0;
        lines.push(`${days[day.day - 1]} ${isWorkout ? `💪 ${day.name} (${day.focus})` : '🛌 休息'}`);
    }
    lines.push('');
    lines.push('回复「今天」查看今日详细计划');
    return { success: true, message: lines.join('\n'), data: plan };
}
/**
 * 今日计划
 */
function handleToday() {
    const config = loadConfig();
    if (!isConfigComplete(config)) {
        return handleInit();
    }
    // 检查是否有当前计划
    let plan = loadCurrentPlan();
    if (!plan) {
        // 自动生成计划
        const weekStart = getWeekStart();
        plan = generateWeekPlan({
            experience: config.user.experience,
            goal: config.user.goal,
            location: config.user.location,
            weeklyDays: config.user.weeklyDays
        }, weekStart);
        saveCurrentPlan(plan);
    }
    const todayPlan = getTodayPlan();
    const todayRecord = getTodayRecord();
    if (!todayPlan) {
        return {
            success: true,
            message: '📅 今日无训练计划，好好休息！'
        };
    }
    if (todayPlan.exercises.length === 0) {
        return {
            success: true,
            message: '🛌 今天是休息日，好好恢复！'
        };
    }
    // 已打卡
    if (todayRecord) {
        const feelingText = todayRecord.feeling
            ? { great: '💪 感觉不错', okay: '😐 一般', tired: '😫 有点累' }[todayRecord.feeling]
            : '';
        return {
            success: true,
            message: `✅ 今日已打卡\n\n${todayPlan.name} - ${todayPlan.focus}\n时长：${todayRecord.durationMinutes} 分钟\n${feelingText}`,
            data: { plan: todayPlan, record: todayRecord }
        };
    }
    // 未打卡，显示计划
    return {
        success: true,
        message: formatWorkoutReminder(todayPlan),
        data: todayPlan
    };
}
/**
 * 打卡
 */
function handleCheckin() {
    const todayPlan = getTodayPlan();
    if (!todayPlan || todayPlan.exercises.length === 0) {
        return {
            success: false,
            message: '今天没有训练计划，无需打卡'
        };
    }
    if (isTodayCompleted()) {
        return {
            success: false,
            message: '今天已经打过卡了'
        };
    }
    // 记录打卡
    const record = recordWorkout(new Date().toISOString().split('T')[0], todayPlan.name, todayPlan.estimatedDuration, null, todayPlan.exercises.length, 0);
    // 更新统计
    const stats = updateStats(record);
    // 重置跳过计数
    resetSkipCount();
    return {
        success: true,
        message: formatCheckinSuccess(todayPlan.name, todayPlan.estimatedDuration, null) +
            '\n\n训练感觉如何？回复「太累」「一般」「没练够」',
        data: { record, stats }
    };
}
/**
 * 记录感受
 */
function handleFeeling(input) {
    const todayRecord = getTodayRecord();
    if (!todayRecord) {
        return {
            success: false,
            message: '今天还没有打卡，请先回复「打卡」'
        };
    }
    let feeling;
    const lower = input.toLowerCase();
    if (lower.includes('累') || lower.includes('tired') || lower.includes('😫')) {
        feeling = 'tired';
    }
    else if (lower.includes('没练够') || lower.includes('不够') || lower.includes('💪')) {
        feeling = 'great';
    }
    else {
        feeling = 'okay';
    }
    const updated = updateFeeling(todayRecord.date, feeling);
    const stats = loadStats();
    // 更新本月感受统计
    const month = todayRecord.date.substring(0, 7);
    const currentMonth = new Date().toISOString().split('T')[0].substring(0, 7);
    if (month === currentMonth) {
        stats.thisMonth.feelingDistribution[feeling] += 1;
    }
    // 更新调整状态
    updateAdjustmentState(todayRecord);
    // 检测异常
    const anomaly = detectAnomalies();
    let extraMessage = '';
    if (anomaly.hasAnomaly && anomaly.action !== 'none') {
        extraMessage = '\n\n💡 ' + anomaly.message;
        if (anomaly.action === 'reduce') {
            extraMessage += '\n\n回复「降低强度」确认调整';
        }
        else if (anomaly.action === 'increase') {
            extraMessage += '\n\n回复「增加强度」确认调整';
        }
    }
    return {
        success: true,
        message: formatCheckinSuccess(todayRecord.dayName, todayRecord.durationMinutes, feeling) + extraMessage
    };
}
/**
 * 本周进度
 */
function handleProgress() {
    const plan = loadCurrentPlan();
    if (!plan) {
        return {
            success: false,
            message: '还没有本周计划，回复「生成计划」创建'
        };
    }
    const records = getWeekRecords(plan.weekStart);
    const completedDates = records.map(r => r.date);
    const recordsMap = new Map(records.map(r => [r.date, { feeling: r.feeling, duration: r.durationMinutes }]));
    return {
        success: true,
        message: formatWeekProgress(plan, completedDates, recordsMap),
        data: { plan, records }
    };
}
/**
 * 统计数据
 */
function handleStats() {
    const stats = loadStats();
    return {
        success: true,
        message: formatStatsMessage(stats),
        data: stats
    };
}
/**
 * 周总结
 */
function handleSummary() {
    const plan = loadCurrentPlan();
    if (!plan) {
        return {
            success: false,
            message: '还没有本周计划'
        };
    }
    const summary = generateWeeklySummary(plan.weekStart);
    return {
        success: true,
        message: formatWeeklySummary(summary),
        data: summary
    };
}
/**
 * 历史记录
 */
function handleHistory() {
    const records = getHistoryRecords(10);
    if (records.length === 0) {
        return {
            success: true,
            message: '还没有训练记录'
        };
    }
    const lines = ['📅 最近训练记录', ''];
    for (const r of records) {
        const feelingEmoji = r.feeling
            ? { great: '💪', okay: '😐', tired: '😫' }[r.feeling]
            : '';
        lines.push(`${r.date} ${r.dayName} - ${r.durationMinutes}分钟 ${feelingEmoji}`);
    }
    return {
        success: true,
        message: lines.join('\n'),
        data: records
    };
}
/**
 * 配置管理
 */
function handleConfig(input) {
    const config = loadConfig();
    // 如果只是查看配置
    if (input.trim() === '配置' || input.trim() === '设置') {
        const user = config.user;
        return {
            success: true,
            message: [
                '⚙️ 当前配置',
                '',
                `性别：${user.gender === 'male' ? '男' : user.gender === 'female' ? '女' : '未设置'}`,
                `年龄：${user.age || '未设置'}`,
                `目标：${getGoalName(user.goal)}`,
                `场地：${getLocationName(user.location)}`,
                `每周：${user.weeklyDays ? user.weeklyDays + '天' : '未设置'}`,
                `时长：${user.sessionDuration ? user.sessionDuration + '分钟' : '未设置'}`,
                `经验：${getExperienceName(user.experience)}`,
                '',
                '修改配置示例：「年龄改成30」或「目标改为减脂」'
            ].join('\n'),
            data: config
        };
    }
    // 尝试解析配置更新
    return parseConfigUpdate(input);
}
/**
 * 解析配置更新
 */
function parseConfigUpdate(input) {
    const config = loadConfig();
    const updates = {};
    // 尝试解析完整配置
    const parts = input.split(/[，,\s]+/);
    for (const part of parts) {
        const lower = part.toLowerCase();
        // 性别
        const gender = parseGender(part);
        if (gender) {
            updates.gender = gender;
            continue;
        }
        // 目标
        const goal = parseGoal(part);
        if (goal) {
            updates.goal = goal;
            continue;
        }
        // 场地
        const location = parseLocation(part);
        if (location) {
            updates.location = location;
            continue;
        }
        // 经验
        const experience = parseExperience(part);
        if (experience) {
            updates.experience = experience;
            continue;
        }
        // 每周天数 - 支持 "每周4天"、"4天"、"每周四天"
        if (part.includes('每周') || part.includes('天')) {
            const match = part.match(/(\d+)/);
            if (match) {
                const num = parseInt(match[1], 10);
                if (num >= 1 && num <= 7) {
                    updates.weeklyDays = num;
                    continue;
                }
            }
        }
        // 每次时长 - 支持 "每次60分钟"、"60分钟"、"60min"
        if (part.includes('分钟') || part.includes('min')) {
            const match = part.match(/(\d+)/);
            if (match) {
                const num = parseInt(match[1], 10);
                if (num >= 10 && num <= 180) {
                    updates.sessionDuration = num;
                    continue;
                }
            }
        }
        // 纯数字
        const num = parseNumber(part);
        if (num) {
            if (num >= 10 && num <= 80 && !updates.age) {
                updates.age = num;
            }
            else if (num >= 1 && num <= 7 && !updates.weeklyDays) {
                updates.weeklyDays = num;
            }
            else if (num >= 20 && num <= 120 && !updates.sessionDuration) {
                updates.sessionDuration = num;
            }
        }
    }
    if (Object.keys(updates).length > 0) {
        const newConfig = updateUserConfig(updates);
        const lines = ['✅ 配置已更新', ''];
        for (const key of Object.keys(updates)) {
            lines.push(`${key}: ${updates[key]}`);
        }
        // 检查是否还需要更多信息
        if (!isConfigComplete(newConfig)) {
            const missing = getMissingFields(newConfig);
            lines.push('', `还需要：${missing.join('、')}`);
        }
        return {
            success: true,
            message: lines.join('\n'),
            data: newConfig
        };
    }
    return {
        success: false,
        message: '无法识别的配置项。示例：「男，28岁，增肌，健身房，每周4天，每次60分钟，中级」'
    };
}
/**
 * 自然语言处理
 */
function handleNaturalLanguage(input) {
    // 尝试解析为配置更新
    const config = loadConfig();
    if (!isConfigComplete(config)) {
        // 可能是配置信息
        return parseConfigUpdate(input);
    }
    // 默认返回今日计划
    return handleToday();
}
/**
 * 帮助
 */
function handleHelp() {
    return {
        success: true,
        message: [
            '🏋️ 健身规划助手',
            '',
            '可用命令：',
            '• 初始化 - 开始配置',
            '• 计划 - 生成本周计划',
            '• 今天 - 查看今日训练',
            '• 打卡 - 记录完成',
            '• 进度 - 本周进度',
            '• 统计 - 训练数据',
            '• 周报 - 周总结',
            '• 历史 - 训练记录',
            '• 配置 - 查看/修改配置',
            '• 调整强度 - 自动调整计划',
            '• 下周 - 生成下周计划',
            '• 动作讲解 [动作名] - 查看详细讲解'
        ].join('\n')
    };
}
/**
 * 动作讲解
 */
function handleExercise(input) {
    const todayPlan = getTodayPlan();
    // 提取动作名称
    const exerciseName = input
        .replace(/动作|讲解|教学|的|详细/g, '')
        .trim();
    // 如果没有指定动作名，显示今日所有动作的讲解
    if (!exerciseName && todayPlan && todayPlan.exercises.length > 0) {
        return {
            success: true,
            message: formatAllExerciseBriefs(todayPlan)
        };
    }
    // 查找指定动作
    if (exerciseName) {
        const detail = formatExerciseDetail(exerciseName);
        return {
            success: true,
            message: detail
        };
    }
    return {
        success: false,
        message: '请指定要查看的动作名称，例如「动作讲解 卧推」，或先生成今日计划。'
    };
}
/**
 * 调整强度
 */
function handleAdjust(input) {
    const lower = input.toLowerCase();
    let action;
    if (lower.includes('降低') || lower.includes('减少')) {
        action = 'reduce';
    }
    else if (lower.includes('增加') || lower.includes('提高')) {
        action = 'increase';
    }
    else {
        return {
            success: false,
            message: '请明确调整方向：\n• 「降低强度」- 减少组数和次数\n• 「增加强度」- 增加组数和次数'
        };
    }
    return adjustPlanIntensity(action);
}
/**
 * 生成下周计划
 */
function handleNextWeek() {
    return generateNextWeekPlan();
}
// ==================== 辅助函数 ====================
function getPlanTypeName(type) {
    const names = {
        'beginner-fullbody': '新手全身训练',
        'push-pull-legs': '推拉腿分化',
        'upper-lower': '上肢下肢分化',
        'home-bodyweight': '居家徒手',
        'running': '跑步计划',
        'hiit': 'HIIT 燃脂'
    };
    return names[type] || type;
}
function getGoalName(goal) {
    if (!goal)
        return '未设置';
    const names = {
        'build_muscle': '增肌',
        'lose_fat': '减脂',
        'shape': '塑形',
        'maintain': '保持',
        'endurance': '体能'
    };
    return names[goal];
}
function getLocationName(location) {
    if (!location)
        return '未设置';
    const names = {
        'gym': '健身房',
        'home': '居家',
        'outdoor': '户外'
    };
    return names[location];
}
function getExperienceName(exp) {
    if (!exp)
        return '未设置';
    const names = {
        'beginner': '新手（<6个月）',
        'intermediate': '中级（6-24个月）',
        'advanced': '高级（>24个月）'
    };
    return names[exp];
}
// ==================== 导出 ====================
export { loadConfig, saveConfig, loadCurrentPlan, saveCurrentPlan, loadStats, generateWeekPlan, getWeekStart };
export { findExerciseDetail, getExerciseBrief, getExerciseFullDescription, exerciseDetails } from './exercise-detail.js';
export { formatWorkoutReminder, formatWorkoutReminderWithVideos, formatWorkoutReminderWithVideoLinks, formatExerciseDetail, formatExerciseDetailWithVideo, formatAllExerciseBriefs, formatAllExerciseBriefsWithVideos } from './notifier.js';
// ==================== 异步版本（支持视频搜索） ====================
/**
 * 异步处理用户输入（支持视频搜索）
 */
export async function handleInputAsync(input) {
    const trimmed = input.trim().toLowerCase();
    const config = loadConfig();
    // 如果配置不完整，优先尝试解析配置
    if (!isConfigComplete(config)) {
        if (trimmed.includes('帮助') || trimmed === 'help') {
            return handleHelp();
        }
        const result = parseConfigUpdate(input);
        if (result.success) {
            return result;
        }
        return handleInit();
    }
    const command = recognizeCommand(trimmed);
    switch (command) {
        case 'today':
            return handleTodayAsync();
        case 'exercise':
            return handleExerciseAsync(input);
        default:
            return handleInput(input);
    }
}
/**
 * 今日计划（异步，包含视频）
 */
async function handleTodayAsync() {
    const config = loadConfig();
    if (!isConfigComplete(config)) {
        return handleInit();
    }
    let plan = loadCurrentPlan();
    if (!plan) {
        const weekStart = getWeekStart();
        plan = generateWeekPlan({
            experience: config.user.experience,
            goal: config.user.goal,
            location: config.user.location,
            weeklyDays: config.user.weeklyDays
        }, weekStart);
        saveCurrentPlan(plan);
    }
    const todayPlan = getTodayPlan();
    const todayRecord = getTodayRecord();
    if (!todayPlan || todayPlan.exercises.length === 0) {
        return handleToday();
    }
    if (todayRecord) {
        return handleToday();
    }
    // 未打卡，显示带视频的计划
    const message = await formatWorkoutReminderWithVideoLinks(todayPlan);
    return {
        success: true,
        message,
        data: todayPlan
    };
}
/**
 * 动作讲解（异步，包含视频）
 */
async function handleExerciseAsync(input) {
    const todayPlan = getTodayPlan();
    const exerciseName = input
        .replace(/动作|讲解|教学|的|详细/g, '')
        .trim();
    // 没有指定动作名，显示今日所有动作的讲解
    if (!exerciseName && todayPlan && todayPlan.exercises.length > 0) {
        const message = await formatAllExerciseBriefsWithVideos(todayPlan);
        return {
            success: true,
            message
        };
    }
    // 查找指定动作
    if (exerciseName) {
        const detail = await formatExerciseDetailWithVideo(exerciseName);
        return {
            success: true,
            message: detail
        };
    }
    return {
        success: false,
        message: '请指定要查看的动作名称，例如「动作讲解 卧推」，或先生成今日计划。'
    };
}
