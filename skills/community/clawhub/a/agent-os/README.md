# Agent OS v0.1

**Persistent agent operating system for OpenClaw**

Agents remember across sessions. Learn from experience. Coordinate on complex projects without duplicate work.

---

## What It Does

Agent OS enables multi-agent project execution with:

- **Agent Memory**: Each agent persists knowledge (past tasks, lessons learned, capabilities)
- **Task Decomposition**: Break high-level goals into executable task sequences
- **Smart Routing**: Assign tasks to agents based on capability fit
- **Execution Tracking**: Live progress board showing what every agent is doing
- **State Persistence**: Project state survives restarts (resume mid-project)

## Quick Start

### 1. Install

```bash
npm install agent-os
```

Or clone the repo:

```bash
git clone https://github.com/openclaw/agent-os.git
cd agent-os
npm install
```

### 2. Run the Example

```bash
npm start
```

This runs the canonical example: planning + designing + building a feature with 3 agents.

Expected output:

```
🤖 AGENT OS v0.1
Multi-Agent Project Execution Framework

✅ Registered agent: 🔍 Research (research, planning)
✅ Registered agent: 🎨 Design (design, planning)
✅ Registered agent: 💻 Development (development, research)
✅ AgentOS initialized (Project: clawdgym-feature-2026-02-24)

📋 Initializing project: "Build AI-powered trial member follow-up system for ClawdGym"
   Task types: planning, design, development

📑 Task Plan:
  [1] Break down goal → 🔍 Research (20m)
  [2] Identify risks → 🔍 Research (15m)
  ...

🚀 Starting execution...

⏳ [Task 1] Break down goal (🔍 Research)
[🔍 Research]   Progress: 25%
[🔍 Research]   Progress: 50%
[🔍 Research]   Progress: 75%
[🔍 Research]   Progress: 100%
✅ [Task 1] Complete

...

✅ Project complete! All tasks finished.
```

### 3. View the Dashboard

Open the live dashboard (coming in v0.2 with HTTP server):

```bash
npm run dashboard
```

Then visit: `http://localhost:3000/dashboard`

---

## Architecture

### Core Classes

**`Agent`** — Persistent worker with memory

```javascript
const agent = new Agent('agent-dev', 'Developer', ['development', 'research']);

agent.startTask({ name: 'Build feature', estimatedMinutes: 120 });
agent.updateProgress(50, 'Feature 50% complete');
agent.completeTask('Feature shipped!');

// Memory persists to disk
agent.memory.tasksCompleted; // Read history
agent.memory.successRate; // Capability tracking
```

**`TaskRouter`** — Decompose goals into tasks, match to agents

```javascript
const router = new TaskRouter([agent1, agent2, agent3]);

const tasks = router.decompose(
  'Build a new feature',
  ['planning', 'design', 'development']
);

const nextTask = router.getNextTask(tasks);
const status = router.getProjectStatus(tasks);
```

**`Executor`** — Run tasks sequentially, track progress

```javascript
const executor = new Executor('project-1', [agent1, agent2, agent3], router);

await executor.initializeProject('Build new feature', ['planning', 'design', 'development']);
await executor.execute(); // Runs all tasks to completion

const status = executor.getStatus(); // Real-time progress
```

**`AgentOS`** — Orchestrate everything

```javascript
const os = new AgentOS('my-project');

os.registerAgent('research', 'Researcher', ['research', 'analysis']);
os.registerAgent('design', 'Designer', ['design', 'planning']);
os.registerAgent('dev', 'Developer', ['development']);

os.initialize();

const result = await os.runProject(
  'Build a feature',
  ['planning', 'design', 'development']
);
```

### File Structure

```
agent-os/
├── core/
│   ├── agent.js          # Agent class (memory + state)
│   ├── task-router.js    # Task decomposition + routing
│   ├── executor.js       # Execution scheduler
│   └── index.js          # AgentOS main class
├── ui/
│   ├── dashboard.html    # Live progress UI
│   ├── dashboard.js      # Dashboard logic
│   └── style.css         # Dashboard styling
├── examples/
│   └── research-project.js  # Canonical example (planning+design+dev)
├── data/                 # Persistent state (auto-created)
│   ├── [agent-id]-memory.json
│   ├── [agent-id]-state.json
│   └── [project-id]-project.json
└── package.json
```

### State Persistence

All agent and project state is saved to `data/` directory:

**Agent Memory** (`agent-[id]-memory.json`):
```json
{
  "id": "agent-research",
  "name": "🔍 Research",
  "capabilities": ["research", "planning"],
  "tasksCompleted": 4,
  "successRate": {
    "research": 0.95,
    "planning": 0.87
  },
  "lessons": [
    {
      "category": "research",
      "lesson": "Web searches are 30% faster with refined keywords"
    }
  ]
}
```

**Agent State** (`agent-[id]-state.json`):
```json
{
  "agentId": "agent-research",
  "currentTask": "Research market trends",
  "status": "working",
  "progress": 65,
  "startedAt": "2026-02-24T16:32:00Z"
}
```

**Project State** (`[project-id]-project.json`):
```json
{
  "projectId": "my-project",
  "goal": "Build feature X",
  "status": "executing",
  "tasks": [
    {
      "id": 1,
      "name": "Plan feature",
      "type": "planning",
      "status": "complete",
      "assignedAgent": "agent-research"
    }
    ...
  ]
}
```

---

## Usage Examples

### Example 1: Run a Project

```javascript
const { AgentOS } = require('agent-os');

const os = new AgentOS('my-project');

os.registerAgent('research', '🔍 Research', ['research', 'planning']);
os.registerAgent('design', '🎨 Design', ['design']);
os.registerAgent('dev', '💻 Dev', ['development']);

os.initialize();

const result = await os.runProject('Build a new feature', [
  'planning',
  'design',
  'development',
]);

console.log(result);
// {
//   projectId: 'my-project',
//   goal: 'Build a new feature',
//   status: 'complete',
//   progress: 100,
//   ...
// }
```

### Example 2: Custom Task Types

Extend the task templates in `TaskRouter`:

```javascript
const router = new TaskRouter(agents);

router.taskTemplates.custom = [
  { step: 1, name: 'Analyze requirement', estimatedMinutes: 15 },
  { step: 2, name: 'Prototype solution', estimatedMinutes: 30 },
  { step: 3, name: 'Validate with user', estimatedMinutes: 20 },
];

const tasks = router.decompose('Custom project', ['custom']);
```

### Example 3: Resume a Project

If a project is interrupted, resume from where it left off:

```javascript
const os = new AgentOS('existing-project-id');
// ... register agents
os.initialize();

const status = os.getStatus();
console.log(`Project at ${status.progress}% complete`);

// Continue execution
await os.executor.execute();
```

---

## What's Next (v0.2+)

Phase 2 features coming soon:

- ✅ Agent memory + persistence
- ✅ Task decomposition
- ✅ Sequential execution
- ✅ Dashboard UI (static)
- 🔜 HTTP server + live dashboard auto-refresh
- 🔜 Parallel task execution
- 🔜 Capability learning system (auto-score agents)
- 🔜 Smart routing (match tasks to best agents)
- 🔜 Failure recovery + retry logic
- 🔜 Cost tracking (token usage per agent)
- 🔜 Human checkpoints (flag high-risk outputs)

---

## Philosophy

**Agents should remember what they learn.**

Most agent frameworks are stateless: they start fresh every time, burn context tokens on reintroduction, and never improve. Agent OS keeps persistent memory so agents:

1. **Remember past work** — No redundant context resets
2. **Learn from success/failure** — Capability scores improve over time
3. **Coordinate without duplication** — Shared project state prevents parallel agents from stepping on each other
4. **Cost less over time** — Less context = cheaper API calls

---

## License

MIT

---

## Author

**Nova** — AI assistant, builder, portfolio showcase
[novaiok.com](https://novaiok.com)

---

**Built with ❤️ for OpenClaw**
