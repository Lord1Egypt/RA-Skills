# Integration Checklist

- [ ] Identify the planner entry point.
- [ ] Identify the tool runner entry point.
- [ ] Identify any existing memory module.
- [ ] Load the latest task state at session start.
- [ ] Load the latest structured summary at session start.
- [ ] Rebuild the working bundle before each major model call.
- [ ] Update task state after each planner step.
- [ ] Update task state after each file write or code patch.
- [ ] Write a checkpoint before any destructive action.
- [ ] Write a checkpoint when context pressure enters warning/compress/critical levels.
- [ ] Stop autonomous execution at critical pressure unconditionally.
- [ ] Ask for confirmation instead of improvising when recovery confidence is low or state recovery is ambiguous.
- [ ] If the host exposes a helper CLI, make it accept a stable workspace root through a session-level default (for example an environment variable) so weak models do not depend on fragile global-option ordering.
- [ ] Prefer a stable summary alias such as `summaries/latest-summary.md` for runtime reads, even if timestamped summaries also exist.
- [ ] If legacy task-state shapes may already exist in the host, detect them safely before mutation and require explicit archival/reinitialization instead of silent overwrite.
- [ ] Append an event log entry after each major action.
- [ ] Keep configuration and filesystem paths configurable.
- [ ] Keep the module framework-agnostic.
