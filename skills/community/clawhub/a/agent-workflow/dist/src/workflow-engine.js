// src/workflow-engine.ts
// Core FSM logic: transitions, guards, fork/join, and response building.
import { WORKFLOW_GRAPH, getNode, getMissingPrevious, getMainFlowOrder, } from "./workflow-graph.js";
import crypto from "node:crypto";
// ─── Engine ────────────────────────────────────────────────────────────────────
export class WorkflowEngine {
    store;
    skillLoader;
    maxForks;
    constructor(store, skillLoader, maxForks = 3) {
        this.store = store;
        this.skillLoader = skillLoader;
        this.maxForks = maxForks;
    }
    // ── start ──────────────────────────────────────────────────────────────────
    start(projectName) {
        const entryNode = WORKFLOW_GRAPH.entryNode;
        const state = this.store.createWorkflow(projectName, entryNode);
        return this.buildResponse(state, `Workflow started. Beginning with ${entryNode}.`);
    }
    // ── status ─────────────────────────────────────────────────────────────────
    // Returns a lightweight summary list when no workflowId is given,
    // or full WorkflowResponse for a specific workflow.
    // Always returns WorkflowResponse for consistent Agent consumption.
    status(workflowId) {
        if (!workflowId) {
            // Return all active workflows as a structured list inside WorkflowResponse
            const summaries = this.listSummaries("active");
            return {
                ok: true,
                message: summaries.length === 0
                    ? "No active workflows. Use start() to begin one."
                    : `${summaries.length} active workflow(s).`,
                // Embed summaries in a dedicated field
                allWorkflows: summaries,
            };
        }
        const state = this.store.loadWorkflow(workflowId);
        if (!state)
            return this.notFound(workflowId);
        return this.buildResponse(state, "Current workflow status.");
    }
    // ── list ───────────────────────────────────────────────────────────────────
    list(statusFilter) {
        const validStatus = ["active", "paused", "completed", "abandoned"];
        const filter = validStatus.includes(statusFilter)
            ? statusFilter
            : undefined;
        const summaries = this.listSummaries(filter);
        return {
            ok: true,
            allWorkflows: summaries,
            message: `Found ${summaries.length} workflow(s)${filter ? ` with status "${filter}"` : ""}.`,
        };
    }
    // ── next ───────────────────────────────────────────────────────────────────
    next(workflowId, branch) {
        const state = this.store.loadWorkflow(workflowId);
        if (!state)
            return this.notFound(workflowId);
        if (state.status !== "active") {
            return this.error("WORKFLOW_ENDED", `Workflow is ${state.status}.`);
        }
        const currentNode = getNode(state.currentNode);
        // Branch point: require branch selection
        if (currentNode.branches && currentNode.branches.length > 0 && !branch) {
            return {
                ok: false,
                workflowId,
                projectName: state.projectName,
                current: this.currentNodeInfo(state.currentNode),
                next: currentNode.branches.map(b => ({
                    node: b.target,
                    label: b.label,
                    condition: b.condition,
                })),
                error: {
                    code: "BRANCH_REQUIRED",
                    message: `Node "${state.currentNode}" is a branch point. Specify a branch.`,
                    suggestion: `Call next with branch: one of [${currentNode.branches.map(b => b.id).join(", ")}]`,
                },
                message: `Branch required. Choose: ${currentNode.branches.map(b => `"${b.id}" (${b.label})`).join(" | ")}`,
            };
        }
        // Determine target node
        let targetId;
        if (branch && currentNode.branches) {
            const chosen = currentNode.branches.find(b => b.id === branch);
            if (!chosen) {
                return this.error("INVALID_TRANSITION", `Unknown branch "${branch}" for node "${state.currentNode}".`, `Valid branches: ${currentNode.branches.map(b => b.id).join(", ")}`);
            }
            targetId = chosen.target;
        }
        else if (currentNode.next.length === 1) {
            targetId = currentNode.next[0];
        }
        else if (currentNode.next.length === 0) {
            return this.error("WORKFLOW_ENDED", "No further nodes. Use complete() to finish.");
        }
        else {
            return this.error("BRANCH_REQUIRED", `Multiple next nodes available. Specify a branch.`, `Options: ${currentNode.next.join(", ")}`);
        }
        return this.transitionTo(state, targetId, branch);
    }
    // ── goto ───────────────────────────────────────────────────────────────────
    // Moves currentNode without marking the previous node as completed.
    // This allows "jumping" to any node without corrupting history/progress.
    goto(workflowId, step) {
        const state = this.store.loadWorkflow(workflowId);
        if (!state)
            return this.notFound(workflowId);
        if (state.status !== "active") {
            return this.error("WORKFLOW_ENDED", `Workflow is ${state.status}.`);
        }
        if (!WORKFLOW_GRAPH.nodes[step]) {
            return this.error("UNKNOWN_NODE", `Node "${step}" does not exist.`);
        }
        // Soft guard: warn about missing previous nodes
        const completed = Object.entries(state.nodes)
            .filter(([, s]) => s === "completed")
            .map(([id]) => id);
        const missing = getMissingPrevious(step, completed);
        // Move to target without completing the current node
        const updated = this.moveToNode(state, step);
        const response = this.buildResponse(updated, `Jumped to "${step}".`);
        if (missing.length > 0) {
            response.warnings = [
                `Skipped recommended steps: ${missing.join(", ")}. ` +
                    `This may affect quality — consider completing them first.`,
            ];
        }
        return response;
    }
    // ── complete ───────────────────────────────────────────────────────────────
    complete(workflowId, note, output) {
        const state = this.store.loadWorkflow(workflowId);
        if (!state)
            return this.notFound(workflowId);
        if (state.status !== "active") {
            return this.error("WORKFLOW_ENDED", `Workflow is ${state.status}.`);
        }
        const now = new Date().toISOString();
        const newNodes = { ...state.nodes, [state.currentNode]: "completed" };
        // Close the LAST open history entry for current node, attach note/output
        const history = this.closeLastOpenEntry(state.history, state.currentNode, now)
            .map(h => h.node === state.currentNode && h.completedAt === now
            ? { ...h, note, output }
            : h);
        // Check if workflow is done (no more next nodes)
        const currentNode = getNode(state.currentNode);
        const isEnd = currentNode.next.length === 0;
        const updated = this.store.saveWorkflow({
            ...state,
            nodes: newNodes,
            status: isEnd ? "completed" : "active",
            history,
        }, state.stateVersion);
        if (isEnd) {
            return this.buildResponse(updated, `Workflow completed! All steps done.`);
        }
        return this.buildResponse(updated, `"${state.currentNode}" marked complete. Call next() to proceed.`);
    }
    // ── fork ───────────────────────────────────────────────────────────────────
    fork(workflowId, plugin) {
        const state = this.store.loadWorkflow(workflowId);
        if (!state)
            return this.notFound(workflowId);
        if (state.status !== "active") {
            return this.error("WORKFLOW_ENDED", `Workflow is ${state.status}.`);
        }
        if (!WORKFLOW_GRAPH.contextPlugins.includes(plugin)) {
            return this.error("UNKNOWN_NODE", `"${plugin}" is not a context-plugin. Available: ${WORKFLOW_GRAPH.contextPlugins.join(", ")}`);
        }
        const activeForks = Object.values(state.forks).filter(f => f.status === "active");
        if (activeForks.length >= this.maxForks) {
            return this.error("FORK_LIMIT_EXCEEDED", `Maximum ${this.maxForks} concurrent forks reached.`, `Complete an existing fork with join() before starting a new one.`);
        }
        const forkId = crypto.randomUUID();
        const now = new Date().toISOString();
        const fork = {
            forkId,
            plugin,
            status: "active",
            startedAt: now,
            joinTarget: state.currentNode,
        };
        const updated = this.store.saveWorkflow({ ...state, forks: { ...state.forks, [forkId]: fork } }, state.stateVersion);
        const skillInfo = this.currentNodeInfo(plugin);
        return {
            ok: true,
            workflowId,
            projectName: state.projectName,
            current: skillInfo,
            activeForks: this.activeForksSummary(updated),
            message: `Fork "${forkId}" started for "${plugin}". Use join("${forkId}") when done.`,
        };
    }
    // ── join ───────────────────────────────────────────────────────────────────
    join(workflowId, forkId, note) {
        const state = this.store.loadWorkflow(workflowId);
        if (!state)
            return this.notFound(workflowId);
        const fork = state.forks[forkId];
        if (!fork) {
            return this.error("NOT_FOUND", `Fork "${forkId}" not found.`);
        }
        if (fork.status === "completed") {
            return this.error("INVALID_TRANSITION", `Fork "${forkId}" is already completed.`);
        }
        const now = new Date().toISOString();
        const updatedFork = { ...fork, status: "completed", completedAt: now, note };
        const updated = this.store.saveWorkflow({ ...state, forks: { ...state.forks, [forkId]: updatedFork } }, state.stateVersion);
        return this.buildResponse(updated, `Fork "${forkId}" (${fork.plugin}) completed. Returned to "${fork.joinTarget}".`);
    }
    // ── getSkill ───────────────────────────────────────────────────────────────
    getSkill(node) {
        const nodeInfo = WORKFLOW_GRAPH.nodes[node];
        if (!nodeInfo) {
            return { ...this.error("UNKNOWN_NODE", `Node "${node}" does not exist.`), skillContent: "" };
        }
        const body = this.skillLoader.getBody(nodeInfo.skillFile);
        return {
            ok: true,
            current: {
                node,
                title: nodeInfo.title,
                type: nodeInfo.type,
                summary: nodeInfo.summary,
                needsFullContent: false,
            },
            skillContent: body, // dedicated field — keeps message clean
            message: `Full content loaded for "${nodeInfo.title}". Follow the instructions in skillContent.`,
        };
    }
    // ── abandon ────────────────────────────────────────────────────────────────
    abandon(workflowId) {
        const state = this.store.loadWorkflow(workflowId);
        if (!state)
            return this.notFound(workflowId);
        const updated = this.store.saveWorkflow({ ...state, status: "abandoned" }, state.stateVersion);
        return {
            ok: true,
            workflowId,
            projectName: state.projectName,
            message: `Workflow "${state.projectName}" abandoned.`,
        };
    }
    // ─── Private helpers ────────────────────────────────────────────────────────
    // Shared summary builder used by status() and list()
    listSummaries(filter) {
        const entries = this.store.listWorkflows(filter);
        const mainOrder = getMainFlowOrder();
        return entries.map(e => {
            const node = WORKFLOW_GRAPH.nodes[e.currentNode];
            const state = this.store.loadWorkflow(e.workflowId);
            const completed = state
                ? Object.entries(state.nodes)
                    .filter(([, s]) => s === "completed")
                    .map(([id]) => id)
                    .filter(id => mainOrder.includes(id))
                : [];
            return {
                workflowId: e.workflowId,
                projectName: e.projectName,
                status: e.status,
                currentNode: e.currentNode,
                currentNodeTitle: node?.title ?? e.currentNode,
                percentDone: mainOrder.length > 0
                    ? Math.round((completed.length / mainOrder.length) * 100)
                    : 0,
                activeForks: state
                    ? Object.values(state.forks).filter(f => f.status === "active").length
                    : 0,
                updatedAt: e.updatedAt,
            };
        });
    }
    // transitionTo: used by next() — marks current node completed and moves forward
    transitionTo(state, targetId, branch) {
        const now = new Date().toISOString();
        const newNodes = {
            ...state.nodes,
            [state.currentNode]: "completed",
            [targetId]: "active",
        };
        const branchChoices = branch
            ? { ...state.branchChoices, [state.currentNode]: branch }
            : state.branchChoices;
        // Close the LAST open history entry for current node (handles re-visits)
        const history = this.closeLastOpenEntry(state.history, state.currentNode, now);
        history.push({ node: targetId, enteredAt: now });
        const updated = this.store.saveWorkflow({
            ...state,
            nodes: newNodes,
            currentNode: targetId,
            branchChoices,
            history,
        }, state.stateVersion);
        return this.buildResponse(updated, `Moved to "${targetId}".`);
    }
    // moveToNode: used by goto() — only changes currentNode, does NOT complete the old node
    moveToNode(state, targetId) {
        const now = new Date().toISOString();
        const newNodes = {
            ...state.nodes,
            // Do NOT mark currentNode as completed — goto is navigation, not progression
            [targetId]: state.nodes[targetId] === "completed" ? "completed" : "active",
        };
        // Add a new history entry for the target (don't close the current one)
        const history = [...state.history, { node: targetId, enteredAt: now }];
        return this.store.saveWorkflow({ ...state, nodes: newNodes, currentNode: targetId, history }, state.stateVersion);
    }
    // closeLastOpenEntry: closes only the most recent uncompleted entry for a node
    // Prevents leaking multiple open entries when a node is visited more than once
    closeLastOpenEntry(history, nodeId, completedAt) {
        let closedOne = false;
        // Traverse in reverse to find the LAST open entry for this node
        const result = [...history];
        for (let i = result.length - 1; i >= 0; i--) {
            if (result[i].node === nodeId && !result[i].completedAt) {
                result[i] = { ...result[i], completedAt };
                closedOne = true;
                break;
            }
        }
        if (!closedOne) {
            // No open entry found — add a synthetic completed entry
            result.push({ node: nodeId, enteredAt: completedAt, completedAt });
        }
        return result;
    }
    buildResponse(state, message) {
        const mainOrder = getMainFlowOrder();
        const completed = mainOrder.filter(id => state.nodes[id] === "completed");
        const remaining = mainOrder.filter(id => state.nodes[id] !== "completed" && state.nodes[id] !== "skipped");
        const percentDone = mainOrder.length > 0
            ? Math.round((completed.length / mainOrder.length) * 100)
            : 0;
        const currentNodeInfo = this.currentNodeInfo(state.currentNode);
        const node = getNode(state.currentNode);
        const next = node.branches
            ? node.branches.map(b => ({
                node: b.target,
                label: b.label,
                condition: b.condition,
            }))
            : node.next.map(id => {
                const n = WORKFLOW_GRAPH.nodes[id];
                return { node: id, label: n?.title ?? id };
            });
        return {
            ok: true,
            workflowId: state.workflowId,
            projectName: state.projectName,
            current: currentNodeInfo,
            next,
            activeForks: this.activeForksSummary(state),
            progress: { completed, remaining, percentDone },
            message,
        };
    }
    currentNodeInfo(nodeId) {
        const node = WORKFLOW_GRAPH.nodes[nodeId];
        if (!node)
            return undefined;
        const summary = node.summary || this.skillLoader.getSummary(node.skillFile);
        return {
            node: nodeId,
            title: node.title,
            type: node.type,
            summary,
            needsFullContent: true, // always suggest loading full content on navigation
        };
    }
    activeForksSummary(state) {
        return Object.values(state.forks)
            .filter(f => f.status === "active")
            .map(f => ({
            forkId: f.forkId,
            plugin: f.plugin,
            status: f.status,
            startedAt: f.startedAt,
        }));
    }
    notFound(workflowId) {
        return this.error("NOT_FOUND", `Workflow "${workflowId}" not found.`, `Use list() to see all workflows, or start() to create a new one.`);
    }
    error(code, message, suggestion) {
        return { ok: false, error: { code, message, suggestion }, message };
    }
}
//# sourceMappingURL=workflow-engine.js.map