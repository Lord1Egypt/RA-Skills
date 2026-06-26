// 配置管理
import * as fs from 'fs';
import * as path from 'path';
const BASE_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/fitness-planner');
const CONFIG_FILE = path.join(BASE_DIR, 'config.json');
const defaultConfig = {
    user: {
        gender: null,
        age: null,
        goal: null,
        location: null,
        weeklyDays: null,
        sessionDuration: null,
        experience: null,
        limitations: []
    },
    notification: {
        channel: 'wecom',
        advanceMinutes: 30,
        morningSummary: true,
        weeklySummaryDay: 'sunday',
        weeklySummaryTime: '20:00'
    },
    createdAt: null,
    updatedAt: null
};
/**
 * 确保配置目录存在
 */
function ensureDir() {
    if (!fs.existsSync(BASE_DIR)) {
        fs.mkdirSync(BASE_DIR, { recursive: true });
    }
}
/**
 * 加载配置
 */
export function loadConfig() {
    ensureDir();
    if (!fs.existsSync(CONFIG_FILE)) {
        saveConfig(defaultConfig);
        return defaultConfig;
    }
    const content = fs.readFileSync(CONFIG_FILE, 'utf-8');
    return JSON.parse(content);
}
/**
 * 保存配置
 */
export function saveConfig(config) {
    ensureDir();
    config.updatedAt = new Date().toISOString();
    if (!config.createdAt) {
        config.createdAt = config.updatedAt;
    }
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}
/**
 * 检查配置是否完整
 */
export function isConfigComplete(config) {
    const { user } = config;
    return !!(user.gender &&
        user.age &&
        user.goal &&
        user.location &&
        user.weeklyDays &&
        user.sessionDuration &&
        user.experience);
}
/**
 * 更新用户配置
 */
export function updateUserConfig(updates) {
    const config = loadConfig();
    config.user = { ...config.user, ...updates };
    saveConfig(config);
    return config;
}
/**
 * 获取缺失的配置项
 */
export function getMissingFields(config) {
    const missing = [];
    const { user } = config;
    if (!user.gender)
        missing.push('性别');
    if (!user.age)
        missing.push('年龄');
    if (!user.goal)
        missing.push('训练目标');
    if (!user.location)
        missing.push('训练场地');
    if (!user.weeklyDays)
        missing.push('每周训练天数');
    if (!user.sessionDuration)
        missing.push('每次训练时长');
    if (!user.experience)
        missing.push('健身经验');
    return missing;
}
/**
 * 解析用户输入
 */
export function parseGender(input) {
    const lower = input.toLowerCase();
    if (lower === '男' || lower === 'male' || lower === 'm')
        return 'male';
    if (lower === '女' || lower === 'female' || lower === 'f')
        return 'female';
    return null;
}
export function parseGoal(input) {
    const goals = {
        '增肌': 'build_muscle',
        '长肌肉': 'build_muscle',
        '减脂': 'lose_fat',
        '减肥': 'lose_fat',
        '塑形': 'shape',
        '塑型': 'shape',
        '保持': 'maintain',
        '维持': 'maintain',
        '体能': 'endurance',
        '耐力': 'endurance'
    };
    return goals[input] || null;
}
export function parseLocation(input) {
    const locations = {
        '健身房': 'gym',
        '健身房器械': 'gym',
        '居家': 'home',
        '居家徒手': 'home',
        '家里': 'home',
        '户外': 'outdoor',
        '户外跑步': 'outdoor',
        '跑步': 'outdoor'
    };
    return locations[input] || null;
}
export function parseExperience(input) {
    const lower = input.toLowerCase();
    if (lower.includes('新') || lower.includes('beginner') || lower.includes('<6'))
        return 'beginner';
    if (lower.includes('高级') || lower.includes('advanced') || lower.includes('>24'))
        return 'advanced';
    if (lower.includes('中级') || lower.includes('intermediate') || lower.includes('6-24'))
        return 'intermediate';
    return null;
}
export function parseNumber(input) {
    const num = parseInt(input, 10);
    return isNaN(num) ? null : num;
}
