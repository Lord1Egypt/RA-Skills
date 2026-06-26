// 打卡记录管理
import * as fs from 'fs';
import * as path from 'path';
const BASE_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/fitness-planner');
const PLANS_DIR = path.join(BASE_DIR, 'plans');
const RECORDS_DIR = path.join(BASE_DIR, 'records');
/**
 * 确保目录存在
 */
function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}
/**
 * 获取当前周计划文件路径
 */
export function getCurrentPlanPath() {
    return path.join(PLANS_DIR, 'current_week.json');
}
/**
 * 加载当前周计划
 */
export function loadCurrentPlan() {
    const planPath = getCurrentPlanPath();
    if (!fs.existsSync(planPath)) {
        return null;
    }
    const content = fs.readFileSync(planPath, 'utf-8');
    return JSON.parse(content);
}
/**
 * 保存当前周计划
 */
export function saveCurrentPlan(plan) {
    ensureDir(PLANS_DIR);
    const planPath = getCurrentPlanPath();
    fs.writeFileSync(planPath, JSON.stringify(plan, null, 2), 'utf-8');
}
/**
 * 获取记录文件路径
 */
function getRecordFilePath(yearMonth) {
    return path.join(RECORDS_DIR, `${yearMonth}.json`);
}
/**
 * 加载月度记录
 */
export function loadMonthRecords(yearMonth) {
    const recordPath = getRecordFilePath(yearMonth);
    if (!fs.existsSync(recordPath)) {
        return [];
    }
    const content = fs.readFileSync(recordPath, 'utf-8');
    return JSON.parse(content);
}
/**
 * 保存月度记录
 */
export function saveMonthRecords(yearMonth, records) {
    ensureDir(RECORDS_DIR);
    const recordPath = getRecordFilePath(yearMonth);
    fs.writeFileSync(recordPath, JSON.stringify(records, null, 2), 'utf-8');
}
/**
 * 获取年月字符串
 */
function getYearMonth(date = new Date()) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
}
/**
 * 记录打卡
 */
export function recordWorkout(date, dayName, durationMinutes, feeling = null, exercisesCompleted = 0, exercisesSkipped = 0, notes) {
    const yearMonth = date.substring(0, 7);
    const records = loadMonthRecords(yearMonth);
    // 检查是否已有当日记录
    const existingIndex = records.findIndex(r => r.date === date);
    const record = {
        date,
        dayName,
        completedAt: new Date().toISOString(),
        durationMinutes,
        feeling,
        exercisesCompleted,
        exercisesSkipped,
        notes
    };
    if (existingIndex >= 0) {
        records[existingIndex] = record;
    }
    else {
        records.push(record);
    }
    saveMonthRecords(yearMonth, records);
    return record;
}
/**
 * 获取当日计划
 */
export function getTodayPlan() {
    const plan = loadCurrentPlan();
    if (!plan)
        return null;
    const today = new Date().toISOString().split('T')[0];
    return plan.days.find(d => d.date === today) || null;
}
/**
 * 检查今日是否已打卡
 */
export function isTodayCompleted() {
    const today = new Date().toISOString().split('T')[0];
    const yearMonth = today.substring(0, 7);
    const records = loadMonthRecords(yearMonth);
    return records.some(r => r.date === today);
}
/**
 * 获取今日记录
 */
export function getTodayRecord() {
    const today = new Date().toISOString().split('T')[0];
    const yearMonth = today.substring(0, 7);
    const records = loadMonthRecords(yearMonth);
    return records.find(r => r.date === today) || null;
}
/**
 * 获取本周记录
 */
export function getWeekRecords(weekStart) {
    const records = [];
    for (let i = 0; i < 7; i++) {
        const date = addDays(weekStart, i);
        const yearMonth = date.substring(0, 7);
        const monthRecords = loadMonthRecords(yearMonth);
        const dayRecord = monthRecords.find(r => r.date === date);
        if (dayRecord) {
            records.push(dayRecord);
        }
    }
    return records;
}
/**
 * 获取历史记录
 */
export function getHistoryRecords(limit = 30) {
    const allRecords = [];
    // 读取最近 3 个月的记录
    const now = new Date();
    for (let i = 0; i < 3; i++) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const yearMonth = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
        const records = loadMonthRecords(yearMonth);
        allRecords.push(...records);
    }
    // 按日期排序，最新的在前
    allRecords.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    return allRecords.slice(0, limit);
}
/**
 * 更新记录的感受
 */
export function updateFeeling(date, feeling) {
    const yearMonth = date.substring(0, 7);
    const records = loadMonthRecords(yearMonth);
    const index = records.findIndex(r => r.date === date);
    if (index < 0)
        return null;
    records[index].feeling = feeling;
    saveMonthRecords(yearMonth, records);
    return records[index];
}
// 日期工具
function addDays(dateStr, days) {
    const date = new Date(dateStr);
    date.setDate(date.getDate() + days);
    return date.toISOString().split('T')[0];
}
