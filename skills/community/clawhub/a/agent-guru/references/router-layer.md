# Router Layer

## Rationale

A single generalist agent accumulates too many tools, grows an unwieldy system prompt, and makes routing decisions on every turn instead of once. **Route early, route cheaply, route at the boundary.** The router's job is narrow: classify intent and dispatch. It must not perform the task itself.

## Routing Strategies

| Strategy | When to use | Cost | Latency |
|----------|------------|------|---------|
| **Regex / keyword** | Structured inputs (commands, IDs) | Near zero | ~0ms |
| **Embedding similarity** | Semantic routing across many intents | Low | ~50ms |
| **Structured LLM output** | Ambiguous natural language | Medium | ~500ms |
| **Supervisor agent** | Context needed to decide | High | ~1-2s |

Use the cheapest strategy that maintains acceptable accuracy. Reserve LLM-based routing for genuinely ambiguous inputs.

## Failure Modes to Design For

- **Misrouting** → add confidence threshold; route low-confidence to clarification
- **Ambiguous intent** → route to a clarification node, not a random specialist
- **Unknown intent** → always have a catch-all that asks or gracefully rejects

## Real-World Example

Customer support triage: *"my invoice is wrong"* → billing agent, *"the app crashes"* → technical agent, *"I want to cancel"* → cancellation agent, *"help me"* → clarification. A misroute is costly — wrong agent, wrong tone, wrong tools.

## Core Pattern (LangGraph)

```python
from typing import Literal
from pydantic import BaseModel
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, END
from typing import TypedDict

# --- State ---
class RouterState(TypedDict):
    user_message: str
    route: str
    confidence: float
    messages: list

# --- Structured output schema ---
class RouteDecision(BaseModel):
    route: Literal["billing", "technical", "cancellation", "clarification"]
    confidence: float  # 0.0 - 1.0
    reason: str

# --- Router node ---
# llm = your LLM instance (any provider)
router_llm = llm.with_structured_output(RouteDecision)

ROUTER_PROMPT = """You are a support triage router. Classify the user's intent.

Routes:
- billing: invoice, payment, charge, refund, pricing
- technical: bug, crash, error, not working, broken
- cancellation: cancel, unsubscribe, quit, close account
- clarification: unclear, could be multiple things, needs more info

Be conservative with confidence — if unsure, route to clarification."""

def router_node(state: RouterState) -> RouterState:
    decision = router_llm.invoke([
        {"role": "system", "content": ROUTER_PROMPT},
        {"role": "user", "content": state["user_message"]}
    ])
    return {
        **state,
        # Confidence threshold (0.7) — below it, always clarify
        "route": decision.route if decision.confidence >= 0.7 else "clarification",
        "confidence": decision.confidence
    }

def route_decision(state: RouterState) -> str:
    return state["route"]

# --- Build graph ---
graph = StateGraph(RouterState)
graph.add_node("router",        router_node)
graph.add_node("billing",       billing_agent_node)
graph.add_node("technical",     technical_agent_node)
graph.add_node("cancellation",  cancellation_agent_node)
graph.add_node("clarification", clarification_node)

graph.set_entry_point("router")
graph.add_conditional_edges("router", route_decision, {
    "billing":       "billing",
    "technical":     "technical",
    "cancellation":  "cancellation",
    "clarification": "clarification",
})
for node in ["billing", "technical", "cancellation", "clarification"]:
    graph.add_edge(node, END)

app = graph.compile()
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Router also performs the task | Router classifies only — delegate execution to specialist nodes |
| No confidence threshold | Low-confidence routes → always route to clarification |
| No catch-all route | Add `"clarification"` or `"fallback"` as the default |
| Router holds conversation history | Router is stateless — it reads the current message only |
| Hallucinated routes | Use structured output with `Literal` type — invalid routes become validation errors |
