// src/core/gene-processor.js
const crypto = require('crypto');

/**
 * GeneProcessor: 经验提炼引擎
 * 负责：从原始对话流中抽象出“普适性”的 AEIF 经验胶囊
 * 核心策略：去变量化、逻辑抽象、结构化输出
 */
class GeneProcessor {
    constructor(llmClient, embeddingService) {
        this.llmClient = llmClient;
        this.embed = embeddingService;
    }

    /**
     * 核心方法：异步提炼经验
     * 遵循“去变量化”原则，剔除具体路径、URL、人名等噪音
     */
    async distill(sessionHistory) {
        const context = sessionHistory.slice(-12); // 取最近 12 轮对话
        const rawText = context.map(m => `[${m.role}]: ${m.content}`).join('\n');

        const prompt = `
你是一位资深软件架构师，负责将具体的调试经验“基因化（GeneDistillation）”。
请分析以下对话中的问题解决过程：

${rawText}

---
提炼任务要求：
1. **去变量化**：剔除具体的项目路径、服务器IP、用户名、具体的仓库URL（用 <PATH>, <URL>, <USER> 代替）。
2. **逻辑抽象**：描述问题的本质原因，而非表现。例如：“NPM权限错误”而非“安装 axios 报错”。
3. **步骤分解**：将方案分解为 diagnosis(诊断)、patch(修复)、config(配置) 或 workaround(临时规避)。
4. **反模式警告**：指出用户容易踩坑的错误尝试（如有）。

请严格按照以下 JSON 格式输出，不要包含任何 Markdown 标记：
{
  "category": "分类标签",
  "triggerPattern": "触发该场景的通用特征描述",
  "rootCause": "本质原因的抽象描述",
  "actionSequence": [
    { "step": 1, "type": "diagnosis/patch/config/workaround", "instruction": "明确的指令", "rationale": "为什么要这么做" }
  ],
  "verificationCriterion": "验证问题已解决的标准",
  "antipatternWarning": "可选的警告信息",
  "tags": ["标签1", "标签2"]
}
`;

        const response = await this.llmClient.ask(prompt);
        // 清理 LLM 可能输出的 Markdown 块
        const cleanJson = response.replace(/```json|```/g, '').trim();
        const distilled = JSON.parse(cleanJson);

        // 为“触发特征”生成向量索引
        const searchKey = `${distilled.triggerPattern} ${distilled.rootCause}`;
        const embedding = await this.embed.vectorize(searchKey);

        return { ...distilled, embedding };
    }

    /**
     * 构建完整的 AEIF Capsule 对象
     */
    createCapsule(distilled, envFingerprint) {
        return {
            capsuleId: `cap_${crypto.randomUUID().slice(0, 8)}`,
            schemaVersion: "1.0",
            category: distilled.category || "general",
            createdAt: new Date().toISOString(),
            trustScore: 0.5, // 初始分，待验证层异步更新
            useCount: 0,
            triggerSignature: {
                errorPattern: distilled.triggerPattern,
                taskIntent: distilled.rootCause,
                embedding: distilled.embedding
            },
            environment: envFingerprint,
            actionSequence: distilled.actionSequence,
            verificationCriterion: distilled.verificationCriterion,
            antipatternWarning: distilled.antipatternWarning || null,
            tags: distilled.tags || []
        };
    }
}

module.exports = GeneProcessor;
