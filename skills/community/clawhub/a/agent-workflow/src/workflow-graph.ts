// src/workflow-graph.ts
// Defines the workflow graph: nodes, edges, transition rules, and guard conditions.

export type NodeType = "main-flow" | "context-plugin" | "utility" | "meta";

export interface RequiredPrevious {
  all?: string[];   // AND semantics: ALL must be completed
  any?: string[];   // OR semantics: AT LEAST ONE must be completed
}

export interface WorkflowNode {
  id: string;
  title: string;
  type: NodeType;
  summary: string;         // one-line description surfaced to Agent
  skillFile: string;       // relative path to SKILL.md within skills/
  next: string[];          // valid next nodes (for main-flow)
  branches?: BranchOption[]; // defined when node is a branch point
  requiredPrevious?: RequiredPrevious; // soft-guard: warn if prerequisites unmet
}

export interface BranchOption {
  id: string;
  label: string;
  target: string;
  condition: string;       // human-readable condition description
}

export interface WorkflowGraph {
  entryNode: string;
  nodes: Record<string, WorkflowNode>;
  contextPlugins: string[];  // nodes that can be forked at any time
  utilityNodes: string[];    // nodes available anytime, not part of state machine
}

export const WORKFLOW_GRAPH: WorkflowGraph = {
  entryNode: "brainstorming",

  nodes: {
    "brainstorming": {
      id: "brainstorming",
      title: "Brainstorming",
      type: "main-flow",
      summary: "Turn ideas into fully formed designs through collaborative dialogue. Produces an approved spec document.",
      skillFile: "brainstorming/SKILL.md",
      next: ["writing-plans"],
    },

    "writing-plans": {
      id: "writing-plans",
      title: "Writing Plans",
      type: "main-flow",
      summary: "Break an approved spec into bite-sized, actionable execution tasks with explicit acceptance criteria.",
      skillFile: "writing-plans/SKILL.md",
      next: ["subagent-driven-execution", "executing-plans"],
      requiredPrevious: { all: ["brainstorming"] },
      branches: [
        {
          id: "subagent",
          label: "Subagent-Driven (recommended)",
          target: "subagent-driven-execution",
          condition: "Subagents are available and tasks are mostly independent",
        },
        {
          id: "sequential",
          label: "Sequential Execution",
          target: "executing-plans",
          condition: "No subagent support, or tasks are tightly coupled",
        },
      ],
    },

    "subagent-driven-execution": {
      id: "subagent-driven-execution",
      title: "Subagent-Driven Execution",
      type: "main-flow",
      summary: "Dispatch one fresh subagent per task with two-stage review (spec + quality) after each.",
      skillFile: "subagent-driven-execution/SKILL.md",
      next: ["verification-before-completion"],
      requiredPrevious: { all: ["writing-plans"] },
    },

    "executing-plans": {
      id: "executing-plans",
      title: "Executing Plans",
      type: "main-flow",
      summary: "Execute the plan sequentially in the current session with checkpoints.",
      skillFile: "executing-plans/SKILL.md",
      next: ["verification-before-completion"],
      requiredPrevious: { all: ["writing-plans"] },
    },

    "verification-before-completion": {
      id: "verification-before-completion",
      title: "Verification Before Completion",
      type: "main-flow",
      summary: "Verify all work against acceptance criteria before claiming completion. Evidence before assertions.",
      skillFile: "verification-before-completion/SKILL.md",
      next: ["finishing-work"],
      // OR semantics: user will have completed exactly one of the two execution branches
      requiredPrevious: { any: ["subagent-driven-execution", "executing-plans"] },
    },

    "finishing-work": {
      id: "finishing-work",
      title: "Finishing Work",
      type: "main-flow",
      summary: "Present delivery options (integrate / submit / keep / discard) and execute the chosen path.",
      skillFile: "finishing-work/SKILL.md",
      next: [],
      requiredPrevious: { all: ["verification-before-completion"] },
    },

    // --- Context plugins (can be forked at any time) ---

    "dispatching-parallel-agents": {
      id: "dispatching-parallel-agents",
      title: "Dispatching Parallel Agents",
      type: "context-plugin",
      summary: "Split 2+ independent tasks across parallel agents for concurrent execution.",
      skillFile: "dispatching-parallel-agents/SKILL.md",
      next: [],
    },

    "requesting-review": {
      id: "requesting-review",
      title: "Requesting Review",
      type: "context-plugin",
      summary: "Dispatch a reviewer subagent to verify work meets requirements before delivery.",
      skillFile: "requesting-review/SKILL.md",
      // context-plugins have no next: they are forked and joined, not chained
      // receiving-review is a separate context-plugin, fork it independently if needed
      next: [],
    },

    "receiving-review": {
      id: "receiving-review",
      title: "Receiving Review",
      type: "context-plugin",
      summary: "Evaluate review feedback with technical rigor — verify before implementing suggestions.",
      skillFile: "receiving-review/SKILL.md",
      next: [],
    },

    // --- Utility nodes (always available, no state machine effect) ---

    "systematic-problem-solving": {
      id: "systematic-problem-solving",
      title: "Systematic Problem Solving",
      type: "utility",
      summary: "Diagnose any problem using root-cause investigation before proposing fixes.",
      skillFile: "systematic-problem-solving/SKILL.md",
      next: [],
    },

    "writing-skills": {
      id: "writing-skills",
      title: "Writing Skills",
      type: "utility",
      summary: "Create or improve skill documents using TDD applied to process documentation.",
      skillFile: "writing-skills/SKILL.md",
      next: [],
    },
  },

  contextPlugins: [
    "dispatching-parallel-agents",
    "requesting-review",
    "receiving-review",
  ],

  utilityNodes: [
    "systematic-problem-solving",
    "writing-skills",
  ],
};

// Returns the node or throws if not found
export function getNode(nodeId: string): WorkflowNode {
  const node = WORKFLOW_GRAPH.nodes[nodeId];
  if (!node) throw new Error(`Unknown node: ${nodeId}`);
  return node;
}

// Returns all nodes that can follow the given node in main-flow
export function getNextNodes(nodeId: string): WorkflowNode[] {
  const node = getNode(nodeId);
  return node.next.map(id => getNode(id));
}

// Returns missing required-previous nodes (for soft guard)
// Supports both AND (all) and OR (any) semantics via RequiredPrevious struct.
export function getMissingPrevious(
  nodeId: string,
  completedNodes: string[]
): string[] {
  const node = getNode(nodeId);
  if (!node.requiredPrevious) return [];

  const missing: string[] = [];

  // AND semantics: every listed node must be completed
  if (node.requiredPrevious.all) {
    for (const req of node.requiredPrevious.all) {
      if (!completedNodes.includes(req)) missing.push(req);
    }
  }

  // OR semantics: at least one listed node must be completed
  if (node.requiredPrevious.any) {
    const anyCompleted = node.requiredPrevious.any.some(req =>
      completedNodes.includes(req)
    );
    if (!anyCompleted) {
      missing.push(`one of [${node.requiredPrevious.any.join(", ")}]`);
    }
  }

  return missing;
}

// Resolves the active main-flow node (first "active" in main-flow chain)
export function getMainFlowOrder(): string[] {
  const order: string[] = [];
  const visited = new Set<string>();
  const queue = [WORKFLOW_GRAPH.entryNode];
  while (queue.length > 0) {
    const id = queue.shift()!;
    if (visited.has(id)) continue;
    visited.add(id);
    const node = WORKFLOW_GRAPH.nodes[id];
    if (node.type === "main-flow") {
      order.push(id);
      node.next.forEach(n => queue.push(n));
    }
  }
  return order;
}
