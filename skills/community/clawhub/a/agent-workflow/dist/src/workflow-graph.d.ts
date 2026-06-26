export type NodeType = "main-flow" | "context-plugin" | "utility" | "meta";
export interface RequiredPrevious {
    all?: string[];
    any?: string[];
}
export interface WorkflowNode {
    id: string;
    title: string;
    type: NodeType;
    summary: string;
    skillFile: string;
    next: string[];
    branches?: BranchOption[];
    requiredPrevious?: RequiredPrevious;
}
export interface BranchOption {
    id: string;
    label: string;
    target: string;
    condition: string;
}
export interface WorkflowGraph {
    entryNode: string;
    nodes: Record<string, WorkflowNode>;
    contextPlugins: string[];
    utilityNodes: string[];
}
export declare const WORKFLOW_GRAPH: WorkflowGraph;
export declare function getNode(nodeId: string): WorkflowNode;
export declare function getNextNodes(nodeId: string): WorkflowNode[];
export declare function getMissingPrevious(nodeId: string, completedNodes: string[]): string[];
export declare function getMainFlowOrder(): string[];
//# sourceMappingURL=workflow-graph.d.ts.map