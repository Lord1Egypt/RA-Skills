"use strict";
/**
 * AI协作操作系统 - 主入口
 * 一站式集成：统一记忆系统 + 信息信号识别 + 工作流资产沉淀 + 个人目标追踪
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.AICollaborationSystem = exports.PersonalGoalSystem = exports.WorkflowAssetSystem = exports.SignalRecognitionSystem = exports.UnifiedMemorySystem = void 0;
// 导出核心模块
var memory_1 = require("./core/memory");
Object.defineProperty(exports, "UnifiedMemorySystem", { enumerable: true, get: function () { return memory_1.UnifiedMemorySystem; } });
// 导出三个子系统
var signal_1 = require("./systems/signal");
Object.defineProperty(exports, "SignalRecognitionSystem", { enumerable: true, get: function () { return signal_1.SignalRecognitionSystem; } });
var workflow_1 = require("./systems/workflow");
Object.defineProperty(exports, "WorkflowAssetSystem", { enumerable: true, get: function () { return workflow_1.WorkflowAssetSystem; } });
var goal_1 = require("./systems/goal");
Object.defineProperty(exports, "PersonalGoalSystem", { enumerable: true, get: function () { return goal_1.PersonalGoalSystem; } });
// 导入
const memory_2 = require("./core/memory");
const signal_2 = require("./systems/signal");
const workflow_2 = require("./systems/workflow");
const goal_2 = require("./systems/goal");
/**
 * AI协作操作系统 - 完整集成类
 *
 * 一行代码创建，自动关联所有系统：
 * const ai = new AICollaborationSystem('my_system');
 */
class AICollaborationSystem {
    constructor(skillName = 'ai_system', baseDir = 'memory', config) {
        // 初始化统一记忆系统
        this.memory = new memory_2.UnifiedMemorySystem(skillName, baseDir, config);
        // 初始化三个子系统，共享同一个记忆实例
        this.signal = new signal_2.SignalRecognitionSystem(this.memory);
        this.workflow = new workflow_2.WorkflowAssetSystem(this.memory);
        this.goal = new goal_2.PersonalGoalSystem(this.memory);
        // 记录初始化
        this.memory.addToL1('系统初始化', 'AI协作操作系统启动完成', 'rule', 5);
    }
    // ========== 便捷方法 ==========
    getSummary() { return this.memory.getSummary(); }
    healthCheck() { return this.memory.healthCheck(); }
    generateInsight() { return this.memory.generateMirrorInsight(); }
    syncAllSystems() {
        this.signal.syncToOtherSystems();
        this.workflow.syncToOtherSystems();
        this.goal.syncToOtherSystems();
    }
    queryAll(query) { return this.memory.queryAll(query); }
    // ========== 每日工作流 ==========
    dailyScan(rawSignals) {
        const date = new Date().toISOString().split('T')[0];
        return this.signal.generateDailyScanReport(date, rawSignals);
    }
    dailyWorkflow(tasks, responses) {
        const date = new Date().toISOString().split('T')[0];
        return this.workflow.generateDailyWorkflowReport(date, tasks, responses);
    }
    dailyGoalTracking(goals, timeLog, ideal) {
        return this.goal.analyzeEnergyAllocation(timeLog, ideal);
    }
    // ========== 每周工作流 ==========
    weeklyReview(goals, timeLog, ideal, priorities) {
        const period = `${new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]} - ${new Date().toISOString().split('T')[0]}`;
        return this.goal.generateWeeklySelfAwarenessReport(period, goals, timeLog, ideal, priorities);
    }
}
exports.AICollaborationSystem = AICollaborationSystem;
exports.default = AICollaborationSystem;
//# sourceMappingURL=index.js.map