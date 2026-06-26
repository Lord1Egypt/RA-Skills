// src/hooks/exception-hook.js

/**
 * ExceptionHook: 运行时异常拦截器
 * 核心策略：混合搜索 (Hybrid Search) = 语义相似度 + 正则硬匹配奖励
 */
class ExceptionHook {
    constructor(store, embedding, injector) {
        this.store = store;
        this.embedding = embedding;
        this.injector = injector;
        
        // 核心信号正则：增强版本，涵盖了 SSL、Git 拒绝等更多报错特征
        this.ERROR_SIGNALS = /(error|failed|exception|timeout|stack trace|not found|404|500|permission denied|EACCES|heap out of memory|ssl|certificate|refused|rejected|fatal)/i;
        
        this.SIMILARITY_THRESHOLD = 0.7; // 进一步放宽基础阈值
        this.MIN_TRUST_SCORE = 0.4;
    }

    async scanAndIntercept(content, taskIntent = '') {
        // 1. 正则预扫
        if (!this.ERROR_SIGNALS.test(content)) return null;

        console.log(`[EvoMap-Hook] Error signal detected, performing hybrid search...`);

        const query = `${content} ${taskIntent}`.slice(0, 500);
        const queryVector = await this.embedding.vectorize(query);

        const matches = await this.store.findSimilar(queryVector, {
            k: 3,
            threshold: 0.1 // 拿到候选集，我们后面自己算 Boosting
        });

        if (matches.length === 0) return null;

        // --- 核心算法升级：Hybrid Boosting ---
        const boostedMatches = matches.map(m => {
            let finalScore = m.score;
            
            // 策略：如果搜索词中包含存储的 errorPattern 关键字，给予显著加分
            // 这解决了路径干扰导致的向量稀释问题
            const pattern = m.capsule.triggerSignature.errorPattern;
            if (pattern && content.toLowerCase().includes(pattern.toLowerCase())) {
                finalScore += 0.35; // 进一步增强强匹配奖励
                console.log(`[EvoMap-Hook] Pattern match boosting applied (+0.35) for ${m.capsule.capsuleId}`);
            }
            
            return { ...m, finalScore };
        });

        // 重新按最终得分排序
        const best = boostedMatches.sort((a,b) => b.finalScore - a.finalScore)[0];

        if (best.finalScore < this.SIMILARITY_THRESHOLD || best.capsule.trustScore < this.MIN_TRUST_SCORE) {
            console.log(`[EvoMap-Hook] Best match ${best.capsule.capsuleId} failed threshold (Final: ${best.finalScore.toFixed(2)}, Trust: ${best.capsule.trustScore.toFixed(2)})`);
            return null;
        }

        return this.injector.format(best);
    }
}

module.exports = ExceptionHook;
