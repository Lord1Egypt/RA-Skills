// 通知模块 - 企业微信通知
import { formatDuration } from './stats.js';
import { findExerciseDetail } from './exercise-detail.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
const execAsync = promisify(exec);
const VIDEO_CACHE_FILE = join(process.env.HOME || '', '.openclaw', 'workspace', 'fitness-planner', 'video-cache.json');
let videoCache = {};
// 加载视频缓存
function loadVideoCache() {
    try {
        if (existsSync(VIDEO_CACHE_FILE)) {
            return JSON.parse(readFileSync(VIDEO_CACHE_FILE, 'utf-8'));
        }
    }
    catch (e) {
        // ignore
    }
    return {};
}
// 保存视频缓存
function saveVideoCache() {
    try {
        videoCache = loadVideoCache();
        writeFileSync(VIDEO_CACHE_FILE, JSON.stringify(videoCache, null, 2));
    }
    catch (e) {
        // ignore
    }
}
/**
 * 搜索动作教学视频
 */
export async function searchExerciseVideo(exerciseName) {
    // 先检查缓存
    videoCache = loadVideoCache();
    const cached = videoCache[exerciseName];
    // 缓存有效期 30 天
    if (cached) {
        const cacheAge = Date.now() - new Date(cached.updatedAt).getTime();
        if (cacheAge < 30 * 24 * 60 * 60 * 1000) {
            return { url: cached.url, title: cached.title, author: cached.author };
        }
    }
    // 搜索视频
    const detail = findExerciseDetail(exerciseName);
    const searchKeyword = detail?.videoSearchKeywords || `${exerciseName}动作教学`;
    try {
        const { stdout } = await execAsync(`mcporter call 'exa.web_search_exa(query: "${searchKeyword} bilibili", numResults: 1)'`, { timeout: 30000 });
        // 解析结果
        const urlMatch = stdout.match(/URL:\s*(https:\/\/[^\s]+)/);
        const titleMatch = stdout.match(/Title:\s*(.+?)(?:\n|URL:)/s);
        const authorMatch = stdout.match(/Author:\s*(.+?)(?:\n|$)/);
        if (urlMatch) {
            const result = {
                url: urlMatch[1],
                title: titleMatch?.[1]?.trim() || '',
                author: authorMatch?.[1]?.trim() || ''
            };
            // 更新缓存
            videoCache[exerciseName] = {
                ...result,
                updatedAt: new Date().toISOString()
            };
            saveVideoCache();
            return result;
        }
    }
    catch (e) {
        console.error('搜索视频失败:', e);
    }
    return null;
}
/**
 * 批量搜索动作视频
 */
export async function searchExerciseVideos(exercises) {
    const results = new Map();
    // 并行搜索所有动作
    const promises = exercises.map(async (name) => {
        const video = await searchExerciseVideo(name);
        if (video) {
            results.set(name, video);
        }
    });
    await Promise.all(promises);
    return results;
}
/**
 * 发送消息到企业微信
 * 通过 OpenClaw 的 message 工具实现
 */
export async function sendWecomMessage(message) {
    // 这里需要通过 OpenClaw 的 message 工具发送
    // 实际调用在 index.ts 中通过 skill 指令完成
    console.log('[通知]', message);
    return true;
}
/**
 * 格式化训练提醒消息（包含动作讲解）
 */
export function formatWorkoutReminder(plan, includeDetails = true) {
    const lines = [
        '🏋️ 今日训练提醒',
        '',
        `📋 ${plan.name} - ${plan.focus}`,
        `⏱️ 预计 ${plan.estimatedDuration} 分钟`,
        '',
        '动作清单：'
    ];
    for (const ex of plan.exercises) {
        const detail = findExerciseDetail(ex.name);
        const brief = detail?.tips[0] || ex.notes || '';
        if (includeDetails && brief) {
            lines.push(`✓ ${ex.name} ${ex.sets}×${ex.reps}`);
            lines.push(`   💡 ${brief}`);
        }
        else {
            lines.push(`✓ ${ex.name} ${ex.sets}×${ex.reps}${ex.notes ? ` (${ex.notes})` : ''}`);
        }
    }
    lines.push('');
    lines.push('训练完成后回复「打卡」记录 ✅');
    lines.push('回复「动作讲解」查看详细步骤和视频');
    return lines.join('\n');
}
/**
 * 格式化带视频链接的完整训练计划（异步版本）
 */
export async function formatWorkoutReminderWithVideoLinks(plan) {
    const lines = [
        '🏋️ 今日训练提醒',
        '',
        `📋 ${plan.name} - ${plan.focus}`,
        `⏱️ 预计 ${plan.estimatedDuration} 分钟`,
        '',
        '动作清单：'
    ];
    // 搜索所有动作的视频
    const exerciseNames = plan.exercises.map(ex => ex.name);
    const videos = await searchExerciseVideos(exerciseNames);
    for (const ex of plan.exercises) {
        const detail = findExerciseDetail(ex.name);
        const brief = detail?.tips[0] || ex.notes || '';
        const video = videos.get(ex.name);
        lines.push(`✓ ${ex.name} ${ex.sets}×${ex.reps}`);
        if (brief) {
            lines.push(`   💡 ${brief}`);
        }
        if (video) {
            lines.push(`   📺 ${video.url}`);
        }
    }
    lines.push('');
    lines.push('训练完成后回复「打卡」记录 ✅');
    return lines.join('\n');
}
/**
 * 格式化带视频链接的训练计划
 */
export function formatWorkoutReminderWithVideos(plan, videoLinks) {
    const lines = [
        '🏋️ 今日训练提醒',
        '',
        `📋 ${plan.name} - ${plan.focus}`,
        `⏱️ 预计 ${plan.estimatedDuration} 分钟`,
        '',
        '动作清单：'
    ];
    for (const ex of plan.exercises) {
        const detail = findExerciseDetail(ex.name);
        const brief = detail?.tips[0] || ex.notes || '';
        const videoUrl = videoLinks.get(ex.name);
        lines.push(`✓ ${ex.name} ${ex.sets}×${ex.reps}`);
        if (brief) {
            lines.push(`   💡 ${brief}`);
        }
        if (videoUrl) {
            lines.push(`   📺 ${videoUrl}`);
        }
    }
    lines.push('');
    lines.push('训练完成后回复「打卡」记录 ✅');
    return lines.join('\n');
}
/**
 * 格式化单个动作的详细讲解
 */
export function formatExerciseDetail(name) {
    const detail = findExerciseDetail(name);
    if (!detail) {
        return `未找到「${name}」的讲解，请尝试搜索视频教程。`;
    }
    const lines = [
        `📌 ${detail.name}`,
        '',
        '动作步骤：',
        ...detail.steps.map((s, i) => `${i + 1}. ${s}`),
        '',
        '要点：',
        ...detail.tips.map(t => `• ${t}`),
        '',
        '常见错误：',
        ...detail.commonErrors.map(e => `✗ ${e}`),
        '',
        `🔍 搜索关键词：${detail.videoSearchKeywords}`
    ];
    return lines.join('\n');
}
/**
 * 格式化单个动作的详细讲解（包含视频链接）
 */
export async function formatExerciseDetailWithVideo(name) {
    const detail = findExerciseDetail(name);
    if (!detail) {
        // 尝试搜索视频
        const video = await searchExerciseVideo(name);
        if (video) {
            return `未找到「${name}」的本地讲解，但找到视频教程：\n\n📺 ${video.url}\n> ${video.author}`;
        }
        return `未找到「${name}」的讲解。`;
    }
    const video = await searchExerciseVideo(name);
    const lines = [
        `📌 ${detail.name}`,
        ''
    ];
    if (video) {
        lines.push(`📺 ${video.url}`);
        if (video.author) {
            lines.push(`   > ${video.author}`);
        }
        lines.push('');
    }
    lines.push('动作步骤：', ...detail.steps.map((s, i) => `${i + 1}. ${s}`), '', '要点：', ...detail.tips.map(t => `• ${t}`), '', '常见错误：', ...detail.commonErrors.map(e => `✗ ${e}`));
    return lines.join('\n');
}
/**
 * 格式化所有动作的简要讲解
 */
export function formatAllExerciseBriefs(plan) {
    const lines = [
        `📖 ${plan.name} - 动作讲解`,
        ''
    ];
    for (const ex of plan.exercises) {
        const detail = findExerciseDetail(ex.name);
        lines.push(`【${ex.name}】${ex.sets}×${ex.reps}`);
        if (detail) {
            lines.push('');
            lines.push('步骤：');
            detail.steps.forEach((s, i) => lines.push(`  ${i + 1}. ${s}`));
            lines.push('');
            lines.push('要点：');
            detail.tips.forEach(t => lines.push(`  • ${t}`));
        }
        else if (ex.notes) {
            lines.push(`要点：${ex.notes}`);
        }
        lines.push('');
    }
    return lines.join('\n');
}
/**
 * 格式化所有动作的完整讲解（包含视频链接）
 */
export async function formatAllExerciseBriefsWithVideos(plan) {
    const lines = [
        `📖 ${plan.name} - 动作讲解`,
        ''
    ];
    // 搜索所有动作的视频
    const exerciseNames = plan.exercises.map(ex => ex.name);
    const videos = await searchExerciseVideos(exerciseNames);
    for (const ex of plan.exercises) {
        const detail = findExerciseDetail(ex.name);
        const video = videos.get(ex.name);
        lines.push(`【${ex.name}】${ex.sets}×${ex.reps}`);
        if (video) {
            lines.push(`📺 ${video.url}`);
            if (video.author) {
                lines.push(`   > ${video.author}`);
            }
            lines.push('');
        }
        if (detail) {
            lines.push('步骤：');
            detail.steps.forEach((s, i) => lines.push(`  ${i + 1}. ${s}`));
            lines.push('');
            lines.push('要点：');
            detail.tips.forEach(t => lines.push(`  • ${t}`));
            lines.push('');
            lines.push('常见错误：');
            detail.commonErrors.forEach(e => lines.push(`  ✗ ${e}`));
        }
        else if (ex.notes) {
            lines.push(`要点：${ex.notes}`);
        }
        lines.push('');
        lines.push('---');
        lines.push('');
    }
    return lines.join('\n');
}
/**
 * 格式化早间总结消息
 */
export function formatMorningSummary(plan) {
    if (!plan || plan.exercises.length === 0) {
        return '🌅 早上好！今天是休息日，好好放松 💪';
    }
    return [
        '🌅 早上好！',
        '',
        `今日训练：${plan.name} (${plan.focus})`,
        `预计时长：${plan.estimatedDuration} 分钟`,
        '',
        '准备好就开始吧！'
    ].join('\n');
}
/**
 * 格式化打卡成功消息
 */
export function formatCheckinSuccess(dayName, duration, feeling) {
    const feelingEmoji = {
        great: '💪',
        okay: '😐',
        tired: '😫'
    };
    const lines = [
        '✅ 打卡成功！',
        '',
        `📊 ${dayName} - ${duration} 分钟`
    ];
    if (feeling) {
        lines.push(`感受：${feelingEmoji[feeling]}`);
    }
    lines.push('');
    lines.push('继续保持！');
    return lines.join('\n');
}
/**
 * 格式化周总结消息
 */
export function formatWeeklySummary(summary) {
    const feelingEmoji = {
        great: '💪',
        okay: '😐',
        tired: '😫'
    };
    const lines = [
        '📊 本周训练总结',
        '',
        `📅 ${summary.weekStart} - ${summary.weekEnd}`,
        '',
        `打卡：${summary.completedDays}/${summary.totalDays} 天`,
        `总时长：${formatDuration(summary.totalMinutes)}`,
        `感受分布：${feelingEmoji.great} ${summary.feelingDistribution.great}次 ${feelingEmoji.okay} ${summary.feelingDistribution.okay}次 ${feelingEmoji.tired} ${summary.feelingDistribution.tired}次`,
        '',
        '💡 建议：'
    ];
    for (const rec of summary.recommendations) {
        lines.push(`   - ${rec}`);
    }
    lines.push('');
    lines.push('回复「调整计划」重新安排下周');
    return lines.join('\n');
}
/**
 * 格式化本周进度消息
 */
export function formatWeekProgress(plan, completedDates, records) {
    const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
    const statusEmoji = {
        completed: '✅',
        skipped: '❌',
        pending: '⏳',
        rest: '🛌'
    };
    const feelingEmoji = {
        great: '💪',
        okay: '😐',
        tired: '😫'
    };
    const lines = [
        `📅 本周训练进度（${plan.weekStart} 起）`,
        ''
    ];
    let completedCount = 0;
    let totalCount = 0;
    for (const day of plan.days) {
        const isWorkoutDay = day.exercises.length > 0;
        const isCompleted = completedDates.includes(day.date);
        const record = records.get(day.date);
        let status;
        let extra = '';
        if (!isWorkoutDay) {
            status = statusEmoji.rest;
        }
        else {
            totalCount += 1;
            if (isCompleted) {
                status = statusEmoji.completed;
                completedCount += 1;
                if (record?.feeling) {
                    extra = ` - ${feelingEmoji[record.feeling]}`;
                }
            }
            else {
                const today = new Date().toISOString().split('T')[0];
                status = day.date < today ? statusEmoji.skipped : statusEmoji.pending;
            }
        }
        lines.push(`${days[day.day - 1]} ${status} ${day.name}${extra}`);
    }
    lines.push('');
    lines.push(`完成率：${completedCount}/${totalCount} (${Math.round(completedCount / totalCount * 100)}%)`);
    return lines.join('\n');
}
/**
 * 格式化统计消息
 */
export function formatStatsMessage(stats) {
    return [
        '📈 训练统计',
        '',
        `总训练次数：${stats.totalWorkouts} 次`,
        `总训练时长：${formatDuration(stats.totalMinutes)}`,
        `当前连续：${stats.currentStreak} 天`,
        `最长连续：${stats.longestStreak} 天`,
        '',
        `本月：${stats.thisMonth.workouts} 次 / ${formatDuration(stats.thisMonth.minutes)}`
    ].join('\n');
}
