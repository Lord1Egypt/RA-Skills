---
name: agent-architecture-patterns
description: AI Agent architecture patterns library with 10 patterns for single and multi-agent systems
---

# Agent Architecture Patterns

This skill provides a comprehensive library of AI Agent architecture patterns to help developers:
- Design single-agent architectures (ReAct, Reflection, Self-Critique, Plan-and-Solve, Tree of Thoughts)
- Design multi-agent collaboration systems (Manager-Worker, Peer-to-Peer, Hierarchical, Market-Based, Pipeline)
- Apply system design principles (separation of concerns, fault tolerance, scalability)
- Implement best practices based on OpenClaw

---

## Patterns

### Single-Agent Patterns (5)

1. **ReAct** - Reasoning + Acting alternation
2. **Reflection** - Self-reflection and iterative improvement
3. **Self-Critique** - Self-criticism and error correction
4. **Plan-and-Solve** - Plan first, then execute
5. **Tree of Thoughts** - Multi-path exploration

### Multi-Agent Patterns (5)

1. **Manager-Worker** - 1 manager coordinates multiple workers
2. **Peer-to-Peer** - Equal agents collaborate
3. **Hierarchical** - Multi-level management structure
4. **Market-Based** - Task bidding and allocation
5. **Pipeline** - Sequential multi-stage processing

---

## Usage

### Option 1: Consult AI-Agent

Ask questions like:
- "Design a multi-agent code review system"
- "How to implement ReAct pattern?"
- "Which agent collaboration pattern should I use?"

### Option 2: Reference Documentation

Browse `patterns/` directory for detailed pattern docs.

### Option 3: Use Code Examples

Run example code from `examples/` directory.

---

## Examples

### ReAct Pattern Example

```javascript
const agent = new ReActAgent({
  tools: [search, calculate],
  maxSteps: 10
});

const answer = await agent.execute("What's the temperature in Beijing today?");
```

### Manager-Worker Pattern Example

```javascript
const workers = [
  new WorkerAgent('worker-1', ['javascript'], { codeReview: true }),
  new WorkerAgent('worker-2', ['python'], { dataAnalysis: true })
];

const manager = new ManagerAgent(workers);
const result = await manager.coordinate("Review this codebase");
```

---

## Installation

```bash
clawhub install agent-architecture-patterns
```

---

## Testing

```bash
npm test
# Runs 30 test cases for ReAct and Manager-Worker implementations
```

---

## License

MIT

---

## Author

AI-Agent
