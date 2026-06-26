# Orchestrator Layer

## Rationale

Complex tasks decompose into subtasks. The orchestrator understands the full goal, breaks it apart, delegates to specialists, and synthesizes results. It must not perform detailed work itself. The critical insight: **subagents receive isolated message history and scoped tool sets** — the orchestrator passes only what the subagent needs. This prevents context pollution, reduces token waste, and makes subagent behavior predictable.

## Task Decomposition Patterns

```
Sequential:     A → B → C → D          (each step depends on previous output)
Parallel:       A, B, C → aggregate    (independent subtasks — run concurrently)
Hierarchical:   A → (B → (D, E)), C    (nested delegation)
Plan-Execute:   Plan phase → Execute   (separate reasoning from action)
```

- **Sequential**: when subtask B needs subtask A's output
- **Parallel**: when subtasks are independent — major latency reduction
- **Plan-Execute**: when mistakes are costly or irreversible

## Plan-Then-Execute Pattern

1. **Plan phase** — agent has read-only tools. Inspects, reasons, produces a structured plan. No side effects.
2. **Execute phase** — agent has full tool access. Human can review the plan before execution proceeds.

This is the single most impactful safety pattern for production agents. It separates *understanding* from *action*.

## Real-World Example

PR review: orchestrator spawns three parallel subagents — code agent (logic/security), test agent (coverage/quality), doc agent (changelog gaps). Each gets only the tools it needs. Orchestrator aggregates into a final review comment.

## Core Pattern (LangGraph Supervisor)

```python
from langgraph.graph import StateGraph, END
# pip install langgraph-supervisor
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from typing import TypedDict

# --- Scoped subagents — each gets ONLY the tools it needs ---
code_agent = create_react_agent(
    model=llm,
    tools=[read_file, grep_codebase, list_files],   # read-only
    state_modifier="You are a code review specialist. Focus on logic, correctness, and security."
)

test_agent = create_react_agent(
    model=llm,
    tools=[read_file, run_tests, check_coverage],
    state_modifier="You are a test review specialist. Check coverage and quality."
)

doc_agent = create_react_agent(
    model=llm,
    tools=[read_file, list_files],
    state_modifier="You are a documentation specialist. Check if docs need updating."
)

# --- Orchestrator delegates to specialists ---
supervisor = create_supervisor(
    agents=[code_agent, test_agent, doc_agent],
    model=llm,
    prompt="""You are a PR review orchestrator.
    Delegate to: code_agent (logic), test_agent (coverage), doc_agent (docs).
    Run code_agent and test_agent in parallel.
    Synthesize all findings into a final review comment with line numbers and file paths."""
)
```

## Plan-Then-Execute Variant

```python
class PlanExecuteState(TypedDict):
    task: str
    plan: str
    mode: str   # "plan" | "execute"
    results: list

def plan_node(state: PlanExecuteState) -> PlanExecuteState:
    """Read-only phase: inspect and produce a plan. No side effects."""
    response = llm.invoke([
        {"role": "system", "content":
         "You are planning. List each step you will perform. Do NOT make any changes."},
        {"role": "user", "content": f"Plan for:\n{state['task']}"}
    ])
    return {**state, "plan": response.content, "mode": "execute"}

def execute_node(state: PlanExecuteState) -> PlanExecuteState:
    """Full tool access: execute the plan step by step."""
    result = supervisor.invoke({"messages": [
        {"role": "user", "content": f"Execute this plan:\n{state['plan']}"}
    ]})
    return {**state, "results": result["messages"]}

graph = StateGraph(PlanExecuteState)
graph.add_node("plan",    plan_node)
graph.add_node("execute", execute_node)
graph.set_entry_point("plan")
graph.add_edge("plan",    "execute")
graph.add_edge("execute", END)
```

## Passing Context to Subagents

```python
# BAD: subagent drowns in irrelevant history
subagent.invoke({"messages": all_parent_messages})

# GOOD: isolated, focused context — pass only what the subagent needs
subagent.invoke({"messages": [
    {"role": "user", "content": f"""
    Task: {specific_subtask}
    Relevant context: {only_what_subagent_needs}
    Return: {expected_output_format}
    """}
]})
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Orchestrator also executes detailed work | Delegate to specialists; orchestrator synthesizes only |
| Subagent receives full parent message history | Pass only the specific task + relevant data |
| All subagents share the same tool set | Scope tools per agent — limits blast radius |
| No aggregation for partial failures | Handle case where one subagent fails; others may succeed |
| Plan-execute skipped for risky workflows | Any irreversible step needs plan-execute + HITL |
