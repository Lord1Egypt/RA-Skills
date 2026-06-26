// src/core/verification-engine.js

/**
 * VerificationEngine: 经验验证与信任评分引擎
 * 核心策略：LLM 自反思 (Self-Reflection) + 动态评分算法
 * 目标：拦截幻觉、低质方案与反模式
 */
class VerificationEngine {
    constructor(llmClient) {
        this.llmClient = llmClient;
    }

    /**
     * 对经验胶囊进行深度自反思
     * @param {Object} capsule - 待验证的 AEIF 胶囊
     * @returns {Promise<Object>} 评分结果
     */
    async selfReflect(capsule) {
        const prompt = `
你是一位严苛的代码审查专家。请评估以下经验胶囊的质量：

[经验描述]
触发特征：${capsule.triggerSignature.errorPattern}
本质原因：${capsule.triggerSignature.taskIntent}

[解决方案]
${JSON.stringify(capsule.actionSequence, null, 2)}

---
请按以下标准打分（0-10分）：
1. **普适性**：该方案是否适用于大多数同类场景，而非特定项目的 Hack？
2. **副作用**：方案是否会引入安全隐患或严重的性能损耗？
3. **优雅度**：是否为根本解决，而非头痛医头的 Workaround？
4. **反模式**：是否包含已知的错误实践（如：滥用 sudo, 禁用安全检查）？

请严格按照以下 JSON 格式输出，不要包含任何 Markdown 标记：
{
  "score": 0-10,
  "concerns": ["问题1", "问题2"],
  "isAntipattern": boolean,
  "suggestion": "改进建议"
}
`;

        const response = await this.llmClient.ask(prompt);
        const cleanJson = response.replace(/```json|```/g, '').trim();
        return JSON.parse(cleanJson);
    }

    /**
     * 动态 TrustScore 计算公式
     * @param {Object} reflection - 自反思结果
     * @param {Object} useHistory - 使用历史 (success/fail)
     * @returns {number} 0.0 - 1.0 之间的分数
     */
    computeTrustScore(reflection, useHistory = { successCount: 0, failCount: 0 }) {
        // 1. 基础分 (0-1)
        let score = reflection.score / 10;

        // 2. 反模式强制降权 (打 3 折)
        if (reflection.isAntipattern) {
            score *= 0.3;
        }

        // 3. 历史加权 (成功 +2%, 失败 -5%)
        score += useHistory.successCount * 0.02;
        score -= useHistory.failCount * 0.05;

        // 4. 边界约束
        return Math.max(0, Math.min(1, score));
    }
}

module.exports = VerificationEngine;
