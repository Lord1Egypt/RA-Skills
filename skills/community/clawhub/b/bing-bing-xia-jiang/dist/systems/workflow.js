"use strict";
/**
 * 工作流资产沉淀系统
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.WorkflowAssetSystem = void 0;
class WorkflowAssetSystem {
    constructor(memory) {
        this.systemName = 'workflow';
        this.memory = memory;
    }
    explicitizeTacitKnowledge(task, userResponses) {
        const knowledge = [];
        const discoveryMethods = {
            operation: '直接记录', experience: '提问引导：为什么这样做？',
            decision: '提问引导：如果...会怎样？', thinking: '深度对话：你是怎么想的？', value: '深度对话：这对你意味着什么？'
        };
        const outputForms = {
            operation: '流程文档', experience: '技巧清单', decision: '决策树', thinking: '思维模型', value: '价值宣言'
        };
        for (const level of ['operation', 'experience', 'decision', 'thinking', 'value']) {
            if (userResponses[level]) {
                knowledge.push({ level, content: userResponses[level], discoveryMethod: discoveryMethods[level], outputForm: outputForms[level] });
            }
        }
        for (const k of knowledge) {
            this.memory.addToL2(`${task}_${k.level}`, k, 'insight', k.level === 'value' ? 5 : k.level === 'thinking' ? 4 : 3, [k.level, 'tacit-knowledge'], this.systemName);
        }
        return knowledge;
    }
    identifyCapabilityGenes(task, result, tacitKnowledge) {
        const genes = [];
        for (const knowledge of tacitKnowledge) {
            if (knowledge.level === 'decision') {
                genes.push({ name: '判断能力', category: 'decision', description: knowledge.content, manifestation: `在${task}中体现`, transferableScenarios: ['类似决策场景'], strength: 'medium' });
            }
            if (knowledge.level === 'thinking') {
                genes.push({ name: '思维能力', category: 'information', description: knowledge.content, manifestation: `在${task}中体现`, transferableScenarios: ['需要思考的场景'], strength: 'medium' });
            }
        }
        for (const gene of genes) {
            this.memory.addToL2(`能力基因_${gene.name}`, gene, 'pattern', 4, ['capability-gene', gene.category], this.systemName);
        }
        return genes;
    }
    buildMethodology(tacitKnowledge, capabilityGenes) {
        const methodology = {
            name: '工作方法论',
            levels: {
                philosophy: tacitKnowledge.find(k => k.level === 'value')?.content || '',
                principles: tacitKnowledge.filter(k => k.level === 'thinking').map(k => k.content),
                methods: tacitKnowledge.filter(k => k.level === 'decision').map(k => k.content),
                processes: tacitKnowledge.filter(k => k.level === 'experience').map(k => k.content),
                tools: tacitKnowledge.filter(k => k.level === 'operation').map(k => k.content)
            },
            validation: '待验证'
        };
        this.memory.addToL3({
            id: '', level: 'L3', category: 'methodology', key: `方法论_${new Date().toISOString().split('T')[0]}`,
            value: methodology, tags: ['methodology', 'workflow'], importance: 5, system: this.systemName,
            createdAt: new Date().toISOString(), accessedAt: new Date().toISOString(), accessCount: 0
        });
        return methodology;
    }
    generateDailyWorkflowReport(date, tasks, userResponses) {
        const allTacitKnowledge = [];
        const allCapabilityGenes = [];
        const methodologies = [];
        for (let i = 0; i < tasks.length; i++) {
            const knowledge = this.explicitizeTacitKnowledge(tasks[i], userResponses[i] || {});
            allTacitKnowledge.push(...knowledge);
            const genes = this.identifyCapabilityGenes(tasks[i], '完成', knowledge);
            allCapabilityGenes.push(...genes);
        }
        if (allTacitKnowledge.length > 0) {
            methodologies.push(this.buildMethodology(allTacitKnowledge, allCapabilityGenes));
        }
        return { date, tasks, tacitKnowledge: allTacitKnowledge, capabilityGenes: allCapabilityGenes, methodologies };
    }
    queryMethodologies() {
        const entries = this.memory.queryL3('methodology');
        return entries.filter(e => e.system === this.systemName).map(e => e.value);
    }
    syncToOtherSystems() {
        const methodologies = this.memory.queryL3('methodology');
        this.memory.syncToSystem('signal', methodologies);
        this.memory.syncToSystem('goal', methodologies);
    }
}
exports.WorkflowAssetSystem = WorkflowAssetSystem;
//# sourceMappingURL=workflow.js.map