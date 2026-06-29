# Claude Code patterns worth borrowing

This note distills transferable ideas from `/Users/kokwind/project/claude-code-src-main`.

## 1. Planning is a first-class mode, not a vibe

**What Claude Code does**
- Treats planning as an explicit mode switch instead of mixing planning and editing in one blurry loop.
- Uses a dedicated tool to enter plan mode and pushes the model into read-only exploration before implementation.
- Has a stronger remote planning path (`/ultraplan`) for large jobs.

**Key files**
- `src/tools/EnterPlanModeTool/EnterPlanModeTool.ts`
- `src/commands/ultraplan.tsx`

**Why it matters**
- Prevents premature edits.
- Makes complex work easier to review.
- Creates a natural approval boundary.

**Local takeaway**
- For complex work, separate discovery/plan/execution/verification.
- Encode the behavior in workflow docs and future skills.

---

## 2. Task state is persistent and visible

**What Claude Code does**
- Uses task create/update/list tools.
- Keeps a persistent task list with watcher-backed UI updates.
- Auto-hides completed work after a grace period instead of leaving stale clutter forever.

**Key files**
- `src/tools/TaskCreateTool/TaskCreateTool.ts`
- `src/tools/TaskUpdateTool/TaskUpdateTool.ts`
- `src/hooks/useTasksV2.ts`

**Why it matters**
- Long jobs stay legible.
- Multi-step execution becomes inspectable.
- Verification and blocking relationships can be expressed explicitly.

**Local takeaway**
- Prefer explicit checklists for large tasks.
- Preserve task state across long sessions instead of relying on conversational memory alone.

---

## 3. Context usage is observable

**What Claude Code does**
- Surfaces context consumption by category.
- Exposes collapse/autocompact status instead of hiding context rewriting.
- Separates system prompt, user context, and system context assembly.

**Key files**
- `src/components/ContextVisualization.tsx`
- `src/utils/queryContext.ts`

**Why it matters**
- Makes context pressure visible before quality degrades.
- Helps explain why the model may lose detail.
- Encourages disciplined prompt assembly.

**Local takeaway**
- Be proactive about memory flushes and concise context.
- Prefer explicit summaries and daily memory updates on long jobs.

---

## 4. Memory is selective, typed, and bounded

**What Claude Code does**
- Treats memory as a directory-backed system, not one giant blob.
- Truncates the memory entrypoint aggressively.
- Selects only a few relevant memories for a query.

**Key files**
- `src/memdir/memdir.ts`
- `src/memdir/findRelevantMemories.ts`

**Why it matters**
- Memory remains usable as it grows.
- Retrieval focuses on relevance, not volume.
- The model is less likely to drown in stale notes.

**Local takeaway**
- Keep long-term memory curated.
- Use index + topic-file patterns when knowledge grows.
- Retrieve surgically instead of reading everything.

---

## 5. Tool discovery is deferred instead of front-loading everything

**What Claude Code does**
- Supports a dedicated tool-search path for deferred tools.
- Searches tool names and descriptions only when needed.

**Key files**
- `src/tools/ToolSearchTool/ToolSearchTool.ts`
- `src/tools.ts`

**Why it matters**
- Keeps default context lean.
- Preserves discoverability without paying full prompt cost up front.
- Works well with expanding MCP/plugin ecosystems.

**Local takeaway**
- Prefer skill descriptions and modular skill directories over dumping all process knowledge into the main prompt.
- Keep skills discoverable, but load detail only on trigger.

---

## 6. Multi-agent work is treated as orchestration, not chaos

**What Claude Code does**
- Has a coordinator mode with explicit worker rules.
- Distinguishes research, synthesis, implementation, and verification.
- Encourages parallel read work and serialized overlapping writes.

**Key files**
- `src/coordinator/coordinatorMode.ts`
- `src/tools.ts`

**Why it matters**
- Parallelism becomes safe and legible.
- The coordinator stays focused on synthesis.
- Workers are guided by clear boundaries.

**Local takeaway**
- For large tasks, fan out discovery where possible.
- Serialize writes on the same file set.
- Treat worker outputs as inputs to synthesize, not as final user-facing prose.

---

## 7. Observability includes cost, diffs, and history

**What Claude Code does**
- Tracks cost and model usage across sessions.
- Extracts per-turn file diffs from tool results.
- Keeps session-aware history and searchable prompt recall.

**Key files**
- `src/cost-tracker.ts`
- `src/hooks/useTurnDiffs.ts`
- `src/history.ts`
- `src/components/HistorySearchDialog.tsx`

**Why it matters**
- Users can see what changed, what it cost, and how they got there.
- Long-running work becomes reviewable.
- Repeated prompts and workflows are easier to recover.

**Local takeaway**
- Report changed files and verification status explicitly.
- Keep better short summaries of important turns.
- Preserve reusable workflows in skills/docs instead of depending on memory alone.

---

## 8. Skills and plugins are hot-reloadable operating surfaces

**What Claude Code does**
- Reloads skill/command state on file changes.
- Separates plugin load, command exposure, agents, hooks, MCP, and LSP integration.
- Uses feature flags to keep optional systems modular.

**Key files**
- `src/hooks/useSkillsChange.ts`
- `src/hooks/useManagePlugins.ts`
- `src/tools.ts`

**Why it matters**
- Extensibility does not require monolithic redesign.
- Experimental features can be added safely.
- Operational surfaces can evolve without restarting the whole mental model.

**Local takeaway**
- Prefer skills for reusable behavior upgrades.
- Keep new capabilities modular and documented.
- Avoid bloating core workspace instructions with niche procedures.

---

## 9. Startup and loading are optimized around user-perceived latency

**What Claude Code does**
- Uses startup prefetch and lazy loading.
- Keeps heavy systems behind dynamic imports and feature gates.

**Key files**
- `README.md`
- `src/tools.ts`
- `src/hooks/useMainLoopModel.ts`

**Why it matters**
- Faster time-to-first-use.
- Optional features do not tax every session.

**Local takeaway**
- Keep startup context lean.
- Prefer on-demand references over giant always-loaded instructions.

---

## 10. The biggest meta-lesson: productize good operator habits

Claude Code’s strongest ideas are not magical model tricks. They are workflow productization:

- planning becomes a mode
- tasks become objects
- context becomes visible
- memory becomes typed and selective
- tool sprawl becomes searchable
- parallel work gets guardrails
- diffs/cost/history become inspectable

That is the main pattern to borrow: take a fuzzy best practice and make it a concrete operating surface.

## Best local adaptations for OpenClaw

### Adopt now
- Create skills for reusable upgrade workflows.
- Use explicit phase-based execution on larger technical tasks.
- Keep better task/checklist discipline.
- Write durable notes for repeatable patterns.

### Prototype later
- A local task cockpit for long technical work.
- A context budget / compaction dashboard.
- Automatic changed-file summaries after edit-heavy turns.
- A lightweight tool/skill finder spanning workspace skills.

### Avoid copying directly
- Anthropic-specific remote web flows.
- Internal telemetry/product experiments.
- Vendor-only policy and bridge details without a local analogue.
