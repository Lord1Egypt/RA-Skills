"use strict";
/**
 * 统一记忆系统 - 核心模块
 * 五层记忆架构：L0闪存/L1工作/L2经验/L3知识/L4智慧
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.UnifiedMemorySystem = void 0;
const crypto = __importStar(require("crypto"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
// ========== 统一记忆系统核心类 ==========
class UnifiedMemorySystem {
    constructor(skillName = 'ai_system', baseDir = 'memory', config) {
        this.L0Variables = new Map();
        this.L0Context = '';
        this.L1Content = '';
        this.L2Entries = [];
        this.L3Data = { worldviews: [], methodologies: [], capabilityModels: [], personalProfile: [] };
        this.L4Data = { insights: [], coreValues: [], longTermPredictions: [], inheritableAssets: [] };
        this.skillName = skillName;
        this.baseDir = baseDir;
        this.config = {
            L0_MAX_ITEMS: 10,
            L1_MAX_LINES: 50,
            L2_MAX_ENTRIES: 200,
            L3_MAX_ENTRIES: 1000,
            AUTO_ARCHIVE_THRESHOLD: 0.8,
            ...config
        };
        this.initialize();
    }
    initialize() {
        this.createDirectories();
        this.loadMemories();
    }
    createDirectories() {
        const dirs = ['L0_flash', 'L1_working', 'L2_experience', 'L3_knowledge', 'L4_wisdom', 'shared', 'logs'];
        for (const dir of dirs) {
            const fullPath = path.join(this.baseDir, this.skillName, dir);
            if (!fs.existsSync(fullPath)) {
                fs.mkdirSync(fullPath, { recursive: true });
            }
        }
    }
    loadMemories() {
        this.loadL1();
        this.loadL2();
        this.loadL3();
        this.loadL4();
    }
    loadL1() {
        const filePath = path.join(this.baseDir, this.skillName, 'L1_working', 'WORKING_MEMORY.md');
        if (fs.existsSync(filePath)) {
            this.L1Content = fs.readFileSync(filePath, 'utf-8');
        }
    }
    loadL2() {
        const filePath = path.join(this.baseDir, this.skillName, 'L2_experience', 'EXPERIENCE_MEMORY.json');
        if (fs.existsSync(filePath)) {
            try {
                const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
                this.L2Entries = data.entries || [];
            }
            catch (e) {
                this.L2Entries = [];
            }
        }
    }
    loadL3() {
        const filePath = path.join(this.baseDir, this.skillName, 'L3_knowledge', 'KNOWLEDGE_MEMORY.json');
        if (fs.existsSync(filePath)) {
            try {
                const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
                this.L3Data = { ...this.L3Data, ...data };
            }
            catch (e) { }
        }
    }
    loadL4() {
        const filePath = path.join(this.baseDir, this.skillName, 'L4_wisdom', 'WISDOM_MEMORY.json');
        if (fs.existsSync(filePath)) {
            try {
                const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
                this.L4Data = { ...this.L4Data, ...data };
            }
            catch (e) { }
        }
    }
    // L0 闪存
    setContext(context) { this.L0Context = context; }
    getContext() { return this.L0Context; }
    setVariable(key, value) {
        this.L0Variables.set(key, value);
        if (this.L0Variables.size > this.config.L0_MAX_ITEMS)
            this.flushL0toL1();
    }
    getVariable(key) { return this.L0Variables.get(key); }
    getAllVariables() {
        const result = {};
        this.L0Variables.forEach((v, k) => { result[k] = v; });
        return result;
    }
    flushL0toL1() {
        const entries = [];
        this.L0Variables.forEach((v, k) => { entries.push(`- ${k}: ${JSON.stringify(v)}`); });
        this.addToL1('L0闪存转存', entries.join('\n'), 'task', 3);
        this.L0Variables.clear();
    }
    // L1 工作记忆
    addToL1(key, value, category, importance = 3) {
        const timestamp = new Date().toISOString();
        const entry = `\n### [${category}] ${key} - ${timestamp}\n${value}\n---\n`;
        this.L1Content += entry;
        if (this.L1Content.split('\n').length > this.config.L1_MAX_LINES)
            this.archiveL1toL2();
        this.saveL1();
    }
    saveL1() {
        fs.writeFileSync(path.join(this.baseDir, this.skillName, 'L1_working', 'WORKING_MEMORY.md'), this.L1Content, 'utf-8');
    }
    archiveL1toL2() {
        const lines = this.L1Content.split('\n');
        const archiveLines = lines.slice(0, Math.floor(lines.length * 0.5));
        this.addToL2('L1自动归档', archiveLines.join('\n'), 'task', 2, [], 'shared');
        this.L1Content = lines.slice(Math.floor(lines.length * 0.5)).join('\n');
    }
    queryL1(pattern) {
        const results = [];
        for (const entry of this.L1Content.split('\n---\n')) {
            if (entry.toLowerCase().includes(pattern.toLowerCase())) {
                results.push({
                    id: this.generateId(), level: 'L1', category: 'task', key: pattern, value: entry,
                    tags: [], importance: 3, system: 'shared',
                    createdAt: new Date().toISOString(), accessedAt: new Date().toISOString(), accessCount: 1
                });
            }
        }
        return results;
    }
    getL1Content() { return this.L1Content; }
    // L2 经验记忆
    addToL2(key, value, category, importance, tags = [], system = 'shared') {
        const timestamp = new Date().toISOString();
        this.L2Entries.push({
            id: this.generateId(), level: 'L2', category, key, value, tags, importance, system,
            createdAt: timestamp, accessedAt: timestamp, accessCount: 0
        });
        if (this.L2Entries.length > this.config.L2_MAX_ENTRIES)
            this.archiveL2toL3();
        this.saveL2();
    }
    saveL2() {
        fs.writeFileSync(path.join(this.baseDir, this.skillName, 'L2_experience', 'EXPERIENCE_MEMORY.json'), JSON.stringify({ entries: this.L2Entries }, null, 2), 'utf-8');
    }
    archiveL2toL3() {
        const sorted = [...this.L2Entries].sort((a, b) => (b.importance * 10 + b.accessCount) - (a.importance * 10 + a.accessCount));
        for (const entry of sorted.slice(Math.floor(this.config.L2_MAX_ENTRIES * 0.7))) {
            this.addToL3Direct(entry);
        }
        this.L2Entries = sorted.slice(0, Math.floor(this.config.L2_MAX_ENTRIES * 0.7));
        this.saveL2();
    }
    queryL2(query, tagFilter, importanceMin = 0) {
        const results = [];
        for (const entry of this.L2Entries) {
            if (entry.importance < importanceMin)
                continue;
            if (tagFilter && !entry.tags.includes(tagFilter))
                continue;
            const content = `${entry.key} ${JSON.stringify(entry.value)} ${entry.tags.join(' ')}`.toLowerCase();
            if (content.includes(query.toLowerCase())) {
                entry.accessCount++;
                entry.accessedAt = new Date().toISOString();
                results.push(entry);
            }
        }
        this.saveL2();
        return results.sort((a, b) => b.importance - a.importance);
    }
    getL2Entries() { return this.L2Entries; }
    // L3 知识记忆
    addToL3(entry) { entry.level = 'L3'; this.addToL3Direct(entry); }
    addToL3Direct(entry) {
        if (entry.category === 'worldview')
            this.L3Data.worldviews.push(entry);
        else if (entry.category === 'methodology')
            this.L3Data.methodologies.push(entry);
        else if (entry.category === 'pattern')
            this.L3Data.capabilityModels.push(entry);
        else if (entry.category === 'goal' || entry.category === 'value')
            this.L3Data.personalProfile.push(entry);
        else
            this.L3Data.methodologies.push(entry);
        this.saveL3();
    }
    saveL3() {
        fs.writeFileSync(path.join(this.baseDir, this.skillName, 'L3_knowledge', 'KNOWLEDGE_MEMORY.json'), JSON.stringify(this.L3Data, null, 2), 'utf-8');
    }
    queryL3(category) {
        if (category === 'worldview')
            return this.L3Data.worldviews;
        if (category === 'methodology')
            return this.L3Data.methodologies;
        if (category === 'pattern')
            return this.L3Data.capabilityModels;
        if (category === 'goal' || category === 'value')
            return this.L3Data.personalProfile;
        return [...this.L3Data.worldviews, ...this.L3Data.methodologies, ...this.L3Data.capabilityModels, ...this.L3Data.personalProfile];
    }
    getL3Data() { return this.L3Data; }
    // L4 智慧记忆
    addToL4(entry) {
        entry.level = 'L4';
        if (entry.category === 'insight')
            this.L4Data.insights.push(entry);
        else if (entry.category === 'value')
            this.L4Data.coreValues.push(entry);
        else if (entry.category === 'wisdom')
            this.L4Data.longTermPredictions.push(entry);
        else
            this.L4Data.inheritableAssets.push(entry);
        this.saveL4();
    }
    saveL4() {
        fs.writeFileSync(path.join(this.baseDir, this.skillName, 'L4_wisdom', 'WISDOM_MEMORY.json'), JSON.stringify(this.L4Data, null, 2), 'utf-8');
    }
    queryL4(category) {
        if (category === 'insight')
            return this.L4Data.insights;
        if (category === 'value')
            return this.L4Data.coreValues;
        if (category === 'wisdom')
            return this.L4Data.longTermPredictions;
        return [...this.L4Data.insights, ...this.L4Data.coreValues, ...this.L4Data.longTermPredictions, ...this.L4Data.inheritableAssets];
    }
    getL4Data() { return this.L4Data; }
    // 统一查询
    queryAll(query) {
        return {
            L0: [], L1: this.queryL1(query), L2: this.queryL2(query),
            L3: this.queryL3().filter(e => JSON.stringify(e.value).toLowerCase().includes(query.toLowerCase())),
            L4: this.queryL4().filter(e => JSON.stringify(e.value).toLowerCase().includes(query.toLowerCase()))
        };
    }
    // 跨系统共享
    syncToSystem(targetSystem, entries) {
        fs.writeFileSync(path.join(this.baseDir, this.skillName, 'shared', `${targetSystem}_sync.json`), JSON.stringify({ timestamp: new Date().toISOString(), entries }, null, 2), 'utf-8');
    }
    syncFromSystem(sourceSystem) {
        const filePath = path.join(this.baseDir, this.skillName, 'shared', `${sourceSystem}_sync.json`);
        if (fs.existsSync(filePath))
            return JSON.parse(fs.readFileSync(filePath, 'utf-8')).entries || [];
        return [];
    }
    // AI镜像
    generateMirrorInsight() {
        const recent = this.L2Entries.slice(-10);
        const patterns = this.analyzePatterns(recent);
        const blindSpot = this.discoverBlindSpot(recent, this.L3Data.worldviews);
        return {
            observation: `我观察到你在${patterns.domain}领域有持续投入`,
            pattern: patterns.description,
            blindSpot: blindSpot.description,
            suggestion: this.generateSuggestion(patterns, blindSpot),
            prediction: this.predictFuture(recent, this.L3Data.methodologies)
        };
    }
    analyzePatterns(entries) {
        const counts = {};
        for (const e of entries)
            counts[e.category] = (counts[e.category] || 0) + 1;
        const top = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || 'general';
        return { domain: top, description: `在${top}方面有${entries.length}条记录` };
    }
    discoverBlindSpot(entries, worldviews) {
        if (worldviews.length > 0 && entries.length < 5)
            return { description: '有世界观但缺乏具体行动记录' };
        if (entries.filter(e => e.tags.includes('error')).length > 3)
            return { description: '有重复的错误模式，建议深入分析根因' };
        return { description: '暂未发现明显盲点' };
    }
    generateSuggestion(p, b) {
        if (b.description.includes('缺乏具体行动'))
            return '建议将世界观转化为具体行动，并记录执行过程';
        if (b.description.includes('重复的错误'))
            return '建议对错误进行根因分析，形成避免重复的方法论';
        return '继续保持当前的学习和行动节奏';
    }
    predictFuture(entries, methodologies) {
        if (methodologies.length > 3)
            return '基于已沉淀的方法论，未来能力将持续复利增长';
        if (entries.length > 10)
            return '经验积累丰富，建议提炼方法论以实现能力复利';
        return '继续积累经验，未来可期';
    }
    // 健康检查
    healthCheck() {
        const L1Lines = this.L1Content.split('\n').length;
        const L2Count = this.L2Entries.length;
        const L3Count = this.L3Data.worldviews.length + this.L3Data.methodologies.length + this.L3Data.capabilityModels.length + this.L3Data.personalProfile.length;
        const L4Count = this.L4Data.insights.length + this.L4Data.coreValues.length + this.L4Data.longTermPredictions.length + this.L4Data.inheritableAssets.length;
        const recommendations = [];
        if (L1Lines > this.config.L1_MAX_LINES * this.config.AUTO_ARCHIVE_THRESHOLD)
            recommendations.push('L1工作记忆接近上限');
        if (L2Count > this.config.L2_MAX_ENTRIES * this.config.AUTO_ARCHIVE_THRESHOLD)
            recommendations.push('L2经验记忆接近上限');
        const sharedDir = path.join(this.baseDir, this.skillName, 'shared');
        const files = fs.existsSync(sharedDir) ? fs.readdirSync(sharedDir) : [];
        return {
            timestamp: new Date().toISOString(),
            levels: {
                L0: { usage: `${this.L0Variables.size}/${this.config.L0_MAX_ITEMS}`, status: 'OK' },
                L1: { usage: `${L1Lines}/${this.config.L1_MAX_LINES}`, status: L1Lines > this.config.L1_MAX_LINES * 0.8 ? 'WARNING' : 'OK' },
                L2: { usage: `${L2Count}/${this.config.L2_MAX_ENTRIES}`, status: L2Count > this.config.L2_MAX_ENTRIES * 0.8 ? 'WARNING' : 'OK' },
                L3: { usage: `${L3Count}/${this.config.L3_MAX_ENTRIES}`, status: 'OK' },
                L4: { usage: `${L4Count}`, status: 'OK' }
            },
            recommendations,
            crossSystemSync: { signal: files.includes('signal_sync.json'), workflow: files.includes('workflow_sync.json'), goal: files.includes('goal_sync.json') }
        };
    }
    getSummary() {
        const h = this.healthCheck();
        return `=== 统一记忆系统摘要 ===
技能名称: ${this.skillName}
最后更新: ${h.timestamp}
【L0闪存】变量数: ${h.levels.L0.usage}
【L1工作记忆】行数: ${h.levels.L1.usage}
【L2经验记忆】条目数: ${h.levels.L2.usage}
【L3知识记忆】世界观${this.L3Data.worldviews.length}条, 方法论${this.L3Data.methodologies.length}条
【L4智慧记忆】洞察${this.L4Data.insights.length}条, 核心价值${this.L4Data.coreValues.length}条
跨系统同步: 信号${h.crossSystemSync.signal ? '✅' : '❌'} 工作流${h.crossSystemSync.workflow ? '✅' : '❌'} 目标${h.crossSystemSync.goal ? '✅' : '❌'}`;
    }
    generateId() {
        return crypto.createHash('md5').update(`${Date.now()}_${Math.random()}`).digest('hex').slice(0, 12);
    }
    getConfig() { return { ...this.config }; }
    updateConfig(newConfig) { this.config = { ...this.config, ...newConfig }; }
}
exports.UnifiedMemorySystem = UnifiedMemorySystem;
//# sourceMappingURL=memory.js.map