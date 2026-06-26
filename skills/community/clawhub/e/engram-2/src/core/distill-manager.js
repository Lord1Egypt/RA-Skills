// src/core/distill-manager.js
const EnvChecker = require('./env-checker');

/**
 * DistillManager: 异步提炼与验证管理器
 * 负责：异步调度 GeneProcessor, 协同入库, 触发异步验证
 * 核心策略：Lazy Distillation + Lazy Verification (响应先行, 异步完善)
 */
class DistillManager {
    constructor(processor, store, verifier) {
        this.processor = processor;
        this.store = store;
        this.verifier = verifier;
    }

    /**
     * 接收提炼请求
     * @param {Array} history - 会话历史
     * @returns {string} 任务确认信息
     */
    async enqueue(history) {
        const taskId = `task_${Date.now().toString(36)}`;
        
        // 立即确认并开始后台计算
        this._processTask(history, taskId); 
        
        return `[EvoMap] 任务已受理 (ID: ${taskId})。经验正在后台进行提炼与基因化，完成后将通过 LLM 进行质量反思并激活。`;
    }

    /**
     * 内部异步处理逻辑 (管道模式)
     * @private
     */
    async _processTask(history, taskId) {
        try {
            console.log(`[EvoMap-Distill] Starting task ${taskId}...`);
            
            // 1. 提炼并生成向量 (LLM 1次消耗)
            const distilled = await this.processor.distill(history);
            const env = EnvChecker.getFingerprint();
            const capsule = this.processor.createCapsule(distilled, env);
            
            // 2. 初始 Draft 入库 (TrustScore = 0.5)
            this.store.save(capsule);
            console.log(`[EvoMap-Distill] Draft stored: ${capsule.capsuleId}`);

            // 3. 延迟反思 (LLM 2次消耗 - 后台非阻塞)
            console.log(`[EvoMap-Verify] Starting lazy verification for ${capsule.capsuleId}...`);
            const reflection = await this.verifier.selfReflect(capsule);
            
            // 4. 计算并更新 TrustScore
            const finalScore = this.verifier.computeTrustScore(reflection);
            this.store.updateTrustScore(capsule.capsuleId, finalScore);
            
            console.log(`[EvoMap-Verify] Verification complete. Final TrustScore: ${finalScore.toFixed(2)} (Reflect Score: ${reflection.score})`);

        } catch (err) {
            console.error(`[EvoMap-Distill] Task ${taskId} failed:`, err.message);
        }
    }
}

module.exports = DistillManager;
