/**
 * 工作流资产沉淀系统
 */
import { UnifiedMemorySystem } from '../core/memory';
type KnowledgeLevel = 'operation' | 'experience' | 'decision' | 'thinking' | 'value';
export interface TacitKnowledge {
    level: KnowledgeLevel;
    content: string;
    discoveryMethod: string;
    outputForm: string;
}
export interface CapabilityGene {
    name: string;
    category: string;
    description: string;
    manifestation: string;
    transferableScenarios: string[];
    strength: 'high' | 'medium' | 'low';
}
export interface Methodology {
    name: string;
    levels: {
        philosophy: string;
        principles: string[];
        methods: string[];
        processes: string[];
        tools: string[];
    };
    validation: string;
}
export declare class WorkflowAssetSystem {
    private memory;
    private systemName;
    constructor(memory: UnifiedMemorySystem);
    explicitizeTacitKnowledge(task: string, userResponses: Record<KnowledgeLevel, string>): TacitKnowledge[];
    identifyCapabilityGenes(task: string, result: string, tacitKnowledge: TacitKnowledge[]): CapabilityGene[];
    buildMethodology(tacitKnowledge: TacitKnowledge[], capabilityGenes: CapabilityGene[]): Methodology;
    generateDailyWorkflowReport(date: string, tasks: string[], userResponses: Record<KnowledgeLevel, string>[]): {
        date: string;
        tasks: string[];
        tacitKnowledge: TacitKnowledge[];
        capabilityGenes: CapabilityGene[];
        methodologies: Methodology[];
    };
    queryMethodologies(): Methodology[];
    syncToOtherSystems(): void;
}
export {};
//# sourceMappingURL=workflow.d.ts.map