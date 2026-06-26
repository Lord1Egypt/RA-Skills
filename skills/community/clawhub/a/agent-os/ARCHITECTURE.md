# Agent OS Architecture

## Design Principles

1. **Persistence First** — All state survives restarts (JSON files, not memory)
2. **Sequential Simplicity** — Start with serial execution (parallel is v0.2)
3. **Template-Driven** — Task types use pre-defined templates (easy to extend)
4. **Agent-Centric** — Everything revolves around agent memory + state
5. **Observable** — Live dashboard shows exactly what's happening

## Core Abstractions

### Agent (agent.js)

**Purpose:** Persistent worker with memory and state

**Responsibilities:**
- Load/save memory on disk (lessons learned, capabilities)
- Load/save state on disk (current task, progress)
- Update progress during task execution
- Record errors and blockers
- Learn lessons for future tasks

**Key Methods:**
```javascript
startTask(task)      // Begin a task
updateProgress(%)    // Report progress
completeTask(output) // Mark done + save output
recordError(error)   // Log failure
learnLesson(category, lesson) // Capture insight
getStatus()          // Return status snapshot
```

**State Lifecycle:**
```
[idle] → startTask → [working] → updateProgress → [working] → completeTask → [done]
                                       ↓
                                   recordError → [blocked]
```

**Memory Structure:**
```json
{
  "id": "agent-research",
  "name": "🔍 Research",
  "capabilities": ["research", "planning"],
  "tasksCompleted": 4,
  "totalTokensBurned": 1250,
  "successRate": {
    "research": 0.95,
    "planning": 0.87
  },
  "lastActiveAt": "2026-02-24T16:32:51.846Z",
  "lessons": [
    {
      "category": "research",
      "lesson": "Web searches work best with 3-5 focused keywords"
    }
  ]
}
```

### TaskRouter (task-router.js)

**Purpose:** Decompose high-level goals into executable tasks

**Responsibilities:**
- Define task templates (planning, design, development, etc.)
- Decompose goals into task sequences
- Match tasks to agents based on capability fit
- Track task dependencies (sequential ordering)
- Calculate project progress

**Key Methods:**
```javascript
decompose(goal, taskTypes)      // Goal → [task, task, task]
matchAgent(taskType)            // Find best agent for task type
getNextTask(tasks)              // Get first executable task
completeTask(taskId, output)    // Mark task done
getProjectStatus(tasks)         // Return progress snapshot
```

**Task Template System:**
```javascript
taskTemplates = {
  planning: [
    { step: 1, name: 'Break down goal', estimatedMinutes: 20 },
    { step: 2, name: 'Identify risks', estimatedMinutes: 15 },
    ...
  ],
  design: [
    { step: 1, name: 'Analyze requirements', estimatedMinutes: 20 },
    ...
  ],
  development: [
    { step: 1, name: 'Setup project', estimatedMinutes: 15 },
    ...
  ]
}
```

**Task Structure:**
```json
{
  "id": 1,
  "type": "planning",
  "name": "Break down goal",
  "description": "planning: Break down goal",
  "estimatedMinutes": 20,
  "assignedAgent": "agent-research",
  "assignedAgentName": "🔍 Research",
  "status": "complete",
  "output": "Task completed successfully",
  "blockers": [],
  "dependsOn": null
}
```

**Dependency Model:**
```
Task 1 (planning) → Task 2 (planning) → Task 3 (planning) → Task 4 (planning)
                                              ↓
                                    Task 5 (design) → Task 6 (design) → ...
```

Currently: Sequential (each task waits for previous to complete)
Future: DAG-based (parallel where dependencies allow)

### Executor (executor.js)

**Purpose:** Run tasks sequentially, track progress, persist state

**Responsibilities:**
- Initialize project (create task list)
- Execute tasks one at a time
- Update agent progress during execution
- Persist project state after each task
- Handle completion and errors

**Key Methods:**
```javascript
initializeProject(goal, taskTypes)  // Setup project
execute()                           // Run all tasks to completion
executeTask(task)                   // Run one task
getStatus()                         // Return live status
```

**Execution Loop:**
```
1. Initialize project
   ├── Create task list (decompose goal)
   ├── Save project state
   └── Print task plan

2. Execute tasks
   └── while (nextTask = getNextTask()):
       ├── Find assigned agent
       ├── agent.startTask(task)
       ├── while (progress < 100):
       │   ├── agent.updateProgress(progress)
       │   └── await sleep(500)  // Simulate work
       ├── agent.completeTask(output)
       ├── task.status = "complete"
       └── saveProject()

3. Mark complete
   ├── project.status = "complete"
   ├── project.completedAt = now
   └── saveProject()
```

**Project State:**
```json
{
  "projectId": "my-project",
  "createdAt": "2026-02-24T16:32:00.000Z",
  "goal": "Build AI-powered trial follow-up system",
  "taskTypes": ["planning", "design", "development"],
  "tasks": [...],
  "status": "executing",
  "startedAt": "2026-02-24T16:32:00.000Z",
  "completedAt": null,
  "notes": []
}
```

### AgentOS (index.js)

**Purpose:** Top-level orchestration

**Responsibilities:**
- Register agents
- Initialize components
- Expose high-level API
- Delegate to sub-components

**Key Methods:**
```javascript
registerAgent(id, name, capabilities)
initialize()
runProject(goal, taskTypes)
getStatus()
getAgentStatus(agentId)
```

**Initialization Flow:**
```
AgentOS()
├── registerAgent('research', ...) → agents.push(Agent)
├── registerAgent('design', ...) → agents.push(Agent)
├── registerAgent('dev', ...) → agents.push(Agent)
└── initialize()
    ├── new TaskRouter(agents)
    └── new Executor(projectId, agents, taskRouter)
```

## Data Flow

### Typical Project Execution

```
User: os.runProject('Build feature', ['planning', 'design', 'dev'])
  ↓
Executor.initializeProject()
  ├── TaskRouter.decompose() → [12 tasks]
  ├── Assign agents to tasks based on capability
  ├── Save project state: data/[projectId]-project.json
  └── Print task plan
  ↓
Executor.execute()
  └── while (getNextTask()):
      ├── Get assigned agent
      ├── agent.startTask(task)
      │  ├── Load agent memory
      │  ├── Update agent state
      │  └── Save agent state: data/agent-[id]-state.json
      ├── for (i = 0; i <= 100; i += 25):
      │  ├── agent.updateProgress(i)
      │  └── Save agent state
      ├── agent.completeTask(output)
      │  ├── memory.tasksCompleted++
      │  ├── Save memory: data/agent-[id]-memory.json
      │  └── Save state
      ├── task.status = "complete"
      └── Save project state
  ↓
Project complete
  ├── Executor.getStatus() → summary report
  └── All state persisted to disk
```

### File I/O

**Reading:**
```
Agent(id) constructor:
  ├── Read data/agent-[id]-memory.json (if exists)
  └── Read data/agent-[id]-state.json (if exists)
```

**Writing (after every state change):**
```
agent.saveMemory()
  └── Write data/agent-[id]-memory.json (atomic: tmp → mv)

agent.saveState()
  └── Write data/agent-[id]-state.json (atomic: tmp → mv)

executor.saveProject()
  └── Write data/[projectId]-project.json (atomic: tmp → mv)
```

## Design Decisions

### Why Sequential Execution (Not Parallel)?

**v0.1:** Start simple, serial. Easier to debug, understand, persist.

**v0.2+:** Add parallel execution with dependency graph:
```javascript
const tasks = [
  { id: 1, name: 'Plan', dependsOn: null },
  { id: 2, name: 'Design A', dependsOn: 1 },
  { id: 3, name: 'Design B', dependsOn: 1 },  // Can run with Design A
  { id: 4, name: 'Dev A', dependsOn: 2 },      // Waits for Design A
  { id: 5, name: 'Dev B', dependsOn: 3 }       // Waits for Design B
]
```

DAG solver would detect 2 & 3 can run in parallel, 4 & 5 can run in parallel.

### Why Task Templates (Not AI Decomposition)?

**Templates:** Deterministic, fast, easy to extend, no hallucinations.

**AI Decomposition (future):** Could use Claude to decompose custom goals, but risky for v0.1.

### Why JSON Files (Not Database)?

**JSON:**
- ✅ Human-readable (easy debugging)
- ✅ Git-friendly (can version control state)
- ✅ No dependencies (no database server)
- ✅ Atomic writes (tmp → mv pattern)

**SQLite (future):** Once we need complex queries (e.g., "find all tasks where agent failed").

### Why Memory-Only Progress Updates?

In `executeTask()`, we simulate progress with:
```javascript
for (let i = 0; i <= 100; i += 25) {
  agent.updateProgress(i);
  await sleep(500);
}
```

**v0.2:** Real progress comes from agent execution hooks:
```javascript
// Agent actually reports progress during work
class Agent {
  executeWith(callback) {
    callback(progress => this.updateProgress(progress));
  }
}
```

## Extension Points

### Add a New Task Type

```javascript
const router = new TaskRouter(agents);

router.taskTemplates.quality_assurance = [
  { step: 1, name: 'Setup test environment', estimatedMinutes: 15 },
  { step: 2, name: 'Write tests', estimatedMinutes: 60 },
  { step: 3, name: 'Run test suite', estimatedMinutes: 20 },
  { step: 4, name: 'Report coverage', estimatedMinutes: 10 }
];

const tasks = router.decompose('Build feature', ['planning', 'design', 'development', 'quality_assurance']);
```

### Track Custom Capability

```javascript
agent.memory.successRate.copywriting = 0.72;
agent.learnLesson('copywriting', 'Headlines with numbers perform 40% better');
```

### Custom Agent Routing

```javascript
const router = new TaskRouter(agents);
router.matchAgent = (taskType) => {
  // Custom logic: route all "critical" tasks to best agent
  if (taskType === 'critical_review') {
    return agents.reduce((best, a) => 
      a.memory.successRate[taskType] > (best.memory.successRate[taskType] || 0) 
        ? a 
        : best
    );
  }
  return agents.find(a => a.capabilities.includes(taskType));
};
```

## Performance Considerations

### Token Usage

**Current:** ~100-200 tokens per project (just logging, no actual AI calls)

**With real agents:** Depends on OpenClaw integration:
- Each agent spawn = fresh context
- Memory file pre-loaded = no redundant context
- Streaming progress updates = stay within window

### Disk I/O

**Writes:** After every task complete + progress update
- Total: ~200-300 file writes per 12-task project
- Size: ~1-5KB per file

**Optimization (v0.2):** Batch writes (flush state every N seconds)

### Execution Time

**Current:** ~30 seconds for 12-task project (25% simulated wait per task)

**With real agents:** Depends on task complexity
- Planning: 5-15 minutes
- Design: 10-30 minutes
- Development: 30-120 minutes

## Future Roadmap

**v0.1** (current)
- ✅ Agent memory + state
- ✅ Task decomposition
- ✅ Sequential execution
- ✅ Basic dashboard

**v0.2**
- Parallel execution + DAG solver
- Capability learning (auto-score agents)
- Smart routing (match tasks to best agents)
- HTTP server + live dashboard

**v0.3**
- Failure recovery + retry strategies
- Cost tracking (tokens, API calls)
- Human checkpoints (flag high-risk outputs)

**v0.4+**
- Multi-project coordination
- Agent specialization (focus agents on specific domains)
- Knowledge base sharing (agents learn from each other)
- Real-time collaboration UI
