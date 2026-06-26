// src/core/context-injector.js

/**
 * ContextInjector: 经验注入器
 * 负责：将结构化的 AEIF 胶囊转化为华丽、易读的 Markdown 注入片段
 * 目标：在报错现场提供极具操作性的“专家建议”
 */
class ContextInjector {
    /**
     * 格式化检索到的经验 match
     * @param {Object} match - { capsule, score }
     * @returns {string} Markdown 注入字符串
     */
    format(match) {
        const { capsule, score } = match;
        const similarityPercent = (score * 100).toFixed(1);

        // 分步指南渲染
        const steps = capsule.actionSequence
            .map(a => `  - **[${a.type.toUpperCase()}]** ${a.instruction}\n    *Rationale: ${a.rationale}*`)
            .join('\n');

        // 反模式警告 (如果有)
        const warning = capsule.antipatternWarning 
            ? `\n> ⚠️ **[Warning]** ${capsule.antipatternWarning}\n` 
            : "";

        // 构建最终 Markdown
        return `
---
### 🧬 [EvoMap Advice] 已发现已知解决方案 (相似度: ${similarityPercent}%)
**Capsule ID:** \`${capsule.capsuleId}\` | **TrustScore:** \`${capsule.trustScore.toFixed(2)}\`

**诊断结论:** ${capsule.triggerSignature.taskIntent}

**[分步解法]:**
${steps}
${warning}
**[验证标准]:** ${capsule.verificationCriterion}
---
`;
    }

    /**
     * 插入到会话历史或系统流
     */
    inject(history, advice) {
        if (!advice) return history;
        return [
            ...history,
            { role: 'system', content: advice }
        ];
    }
}

module.exports = ContextInjector;
