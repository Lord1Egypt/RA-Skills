# Trinity Mapping: Unbundling and Redistributing Management Functions

## Purpose

This reference provides the framework for mapping the three atomic functions of management—Routing, Sense-Making, and Accountability—across humans, AI agents, and organizational systems during an agentic transformation.

## The Management Trinity Decomposition

Every management function in an organization can be decomposed into one or more of these three atomic components:

| Function | Definition | AI Capability | Human Requirement |
| :--- | :--- | :--- | :--- |
| **Routing** | Information logistics: directing tasks, data, and context to the right resources at the right time. | **High.** AI excels at synthesis, pattern recognition, and rapid distribution. | Low. Humans add value only in novel or politically sensitive routing. |
| **Sense-Making** | Strategic judgment: synthesizing ambiguous signals into coherent strategy while buffering teams from noise. | **Low.** AI can synthesize data but cannot navigate organizational politics, apply ethical intuition, or make judgment calls in novel situations. | High. Requires deep contextual understanding, political awareness, and human intuition. |
| **Accountability** | Ownership: bearing responsibility for outcomes, providing mentorship, and maintaining long-term commitment. | **None.** AI cannot bear responsibility, feel empathy, or maintain emotional investment over time. | Critical. Only humans can own outcomes, apologize sincerely, and mentor for growth. |

## The Mapping Workflow

### Step 1: Inventory Current Management Functions
For each manager or management layer being restructured, list every function they perform. Categorize each function as Routing, Sense-Making, or Accountability.

**Example for a typical Engineering Manager:**

| Current Function | Trinity Category | Can AI Handle? |
| :--- | :--- | :--- |
| Assigning tickets to engineers | Routing | Yes |
| Running daily standups | Routing | Partially (AI can summarize, human facilitates) |
| Deciding technical architecture | Sense-Making | No (AI can present options) |
| Navigating cross-team politics | Sense-Making | No |
| Conducting performance reviews | Accountability | No |
| Mentoring junior engineers | Accountability | No |
| Approving PRs and releases | Routing + Sense-Making | Partially (AI can flag risks) |

### Step 2: Assign Routing Functions to AI
For each function categorized as "Routing" where AI can handle it, design the agent workflow. Ensure the agent has access to the necessary data and tools via MCP.

### Step 3: Redistribute Sense-Making and Accountability
For each orphaned Sense-Making and Accountability function, explicitly assign it to a human role:

| New Role | Responsibilities | Trinity Functions |
| :--- | :--- | :--- |
| **Individual Contributor (IC)** | Specialist who builds and operates capabilities. Relies on the AI-powered "world model" for context. | Executes work informed by AI Routing. |
| **Directly Responsible Individual (DRI)** | Owns a specific, cross-cutting problem for a defined period. Has authority to pull resources. | Sense-Making + Accountability for their domain. |
| **Player-Coach** | Practitioner who continues to build products while also mentoring and developing people. | Accountability (mentorship, empathy, culture). |

### Step 4: Validate the Redistribution
Ensure no function is left unassigned. The most common failure mode is removing a manager without redistributing their Sense-Making and Accountability functions, leading to "culture strain."

## The Subsidiarity Principle

Following the Berkeley CMR "Fluid Organization" framework, apply subsidiarity as the default design principle: assign responsibility for a task to the smallest possible team at the lowest possible hierarchical level, unless there are good reasons to do differently. This means:

- AI agents operate as "functional agents" in factory + pilot mode by default.
- **Triggers** shift the system from factory to studio mode (e.g., AI flags an anomaly requiring human collaboration).
- **Checks** are prescheduled points where humans proactively review AI outputs (e.g., weekly synthesis reviews).
- **Help chains** define the escalation sequence when a trigger fires.
- **Transparency** ensures all role distributions, triggers, and checks are visible and agreed upon.

## Anti-Patterns to Avoid

| Anti-Pattern | Description | Consequence |
| :--- | :--- | :--- |
| **The Hollow Middle** | Removing managers without redistributing their functions. | Culture strain, burnout, isolation. |
| **The AI Manager** | Assigning Sense-Making or Accountability to an AI agent. | Trust erosion, accountability vacuum. |
| **The Shadow Hierarchy** | Informal leaders emerge to fill the gap, without formal authority. | Political dysfunction, unclear ownership. |
| **The Overloaded DRI** | Assigning too many cross-cutting problems to a single DRI. | Bottleneck, single point of failure. |
