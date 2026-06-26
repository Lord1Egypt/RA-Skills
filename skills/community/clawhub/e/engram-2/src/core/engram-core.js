// src/core/evomap-core.js
const CapsuleStore = require('../storage/capsule-store');
const EmbeddingService = require('./embedding-service');
const GeneProcessor = require('./gene-processor');
const VerificationEngine = require('./verification-engine');
const DistillManager = require('./distill-manager');
const ExceptionHook = require('../hooks/exception-hook');
const ContextInjector = require('./context-injector');

/**
 * EvoMapCore: 系统总控中心
 * 负责：模块初始化、任务调度、指令路由
 * 目标：为 Agent 提供一站式的长期记忆管理能力
 */
class EvoMapCore {
    constructor(config = {}) {
        this.store = new CapsuleStore(config.dbPath);
        this.embedding = new EmbeddingService();
        this.injector = new ContextInjector();
        
        // 核心引擎
        this.verifier = new VerificationEngine(config.llmClient);
        this.processor = new GeneProcessor(config.llmClient, this.embedding);
        
        // 异步管理器与拦截器
        this.distillManager = new DistillManager(this.processor, this.store, this.verifier);
        this.hook = new ExceptionHook(this.store, this.embedding, this.injector);
        
        this.initialized = false;
    }

    /**
     * 异步初始化 (模型加载)
     */
    async init() {
        if (this.initialized) return;
        await this.embedding.init();
        this.initialized = true;
        console.log("🧬 [EvoMap-Core] System initialized and ready.");
    }

    /**
     * !exp consult 指令处理
     */
    async consult(query, taskIntent = '') {
        const advice = await this.hook.scanAndIntercept(query, taskIntent);
        return advice || "[EvoMap] 未找到高度匹配的既有经验。";
    }

    /**
     * !exp commit 指令处理
     */
    async commit(history) {
        return await this.distillManager.enqueue(history);
    }

    /**
     * !exp list 指令处理
     */
    async list() {
        const stats = this.store.db.prepare('SELECT COUNT(*) as count, AVG(trustScore) as avgTrust FROM engram_capsules').get();
        const recent = this.store.db.prepare('SELECT capsuleId, category, trustScore FROM engram_capsules ORDER BY createdAt DESC LIMIT 5').all();
        
        let output = `### 🧬 [EvoMap Stats] 记忆库概览
`;
        output += `- **经验总数:** ${stats.count}
`;
        output += `- **平均信任分:** ${stats.avgTrust ? stats.avgTrust.toFixed(2) : 'N/A'}

`;
        output += `**[最近存入]:**
`;
        recent.forEach(c => {
            output += `- \`${c.capsuleId}\` [${c.category}] (Score: ${c.trustScore.toFixed(2)})\n`;
        });
        
        return output;
    }

    /**
     * 评价反馈 (用于动态调分)
     */
    async rate(capsuleId, isGood) {
        const row = this.store.db.prepare('SELECT trustScore, useCount FROM engram_capsules WHERE capsuleId = ?').get(capsuleId);
        if (!row) return `[EvoMap] 错误：找不到 ID 为 ${capsuleId} 的胶囊。`;

        const adjustment = isGood ? 0.05 : -0.15; // 差评扣分更狠
        const newScore = Math.max(0, Math.min(1, row.trustScore + adjustment));
        
        this.store.updateTrustScore(capsuleId, newScore);
        return `[EvoMap] 反馈已收到。胶囊 ${capsuleId} 的信任分已更新为 ${newScore.toFixed(2)}。`;
    }

    async terminate() {
        await this.embedding.terminate();
    }
}

module.exports = EvoMapCore;
