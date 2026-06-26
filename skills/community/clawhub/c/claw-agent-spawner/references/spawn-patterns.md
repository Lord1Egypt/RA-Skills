# Spawn Patterns — Reference Guide

## Pattern A: Parallel Research (Data Collection)

**Best for:** Tasks requiring research across multiple independent sources.
**Speed gain:** 3-5x over sequential research.

### Template
```
Task: "Research X across N sources"
→ Split: source_1, source_2, ..., source_N
→ Each agent: "Research [specific source] for [topic]"
→ Collect: all findings
→ Synthesize: unified report with comparisons
```

### Example: Market Research
```
Spawn 3 agents:
  1. "Research the current state of AI automation tools in EU market. Focus on pricing, features, and adoption trends. Find at least 5 specific examples."
  2. "Analyze the Czech automation market. Identify top 3 competitors, their pricing, and market position. Focus on local companies."
  3. "Research emerging trends in AI automation for 2026. Focus on open-source tools, no-code platforms, and integration capabilities."
```

### Anti-pattern
```
❌ Don't: Ask each agent to summarize the other agents' work
❌ Don't: Create dependencies between subtasks
✅ Do: Give each agent full context to work independently
```

---

## Pattern B: Build + Test + Document (Parallel Delivery)

**Best for:** Software deliverables that need code, tests, and docs.
**Speed gain:** 2-3x over sequential build.

### Template
```
Task: "Build [deliverable] with tests and documentation"
→ Split: builder, tester, writer
→ Each agent works on their part in isolation
→ Collect: source files, test results, documentation
→ Synthesize: complete deliverable
```

### Example: Skill Development
```
Spawn 3 agents:
  1. "Build a Python CLI tool that converts CSV to JSON with validation. Include error handling for malformed data."
  2. "Write 8 unit tests for a CSV-to-JSON converter. Test edge cases: empty files, encoding errors, large files, mixed types."
  3. "Write documentation for a CSV-to-JSON CLI tool. Include usage examples, options reference, and troubleshooting guide."
```

---

## Pattern C: Analyze → Summarize → Format (Pipeline)

**Best for:** Data processing where analysis, summary, and presentation are distinct.
**Speed gain:** 1.5-2x (partial parallelism).

### Template
```
Task: "Create [deliverable] from [data source]"
→ Split: analyst (find patterns), summarizer (extract insights), formatter (presentation)
→ Order: analyst → summarizer → formatter (can partially parallelize)
```

### Example: Competitive Analysis
```
Spawn 3 agents:
  1. "Analyze the feature sets of these 6 CRM tools. Create a comparison table with 15 dimensions."
  2. "Based on the feature comparison, identify which CRM is best for startups, which for enterprise, and which is the overall winner. Justify each choice."
  3. "Format a competitive analysis report. Use markdown with headers, tables, bullet points, and a clear executive summary."
```

---

## Pattern D: Review → Fix → Verify (Quality Gate)

**Best for:** Code quality improvement, security audits, compliance checks.
**Speed gain:** 2-3x over single-agent review.

### Template
```
Task: "Improve [codebase] [criteria]"
→ Split: reviewer (find issues), fixer (apply patches), verifier (confirm fixes)
→ Order: reviewer → fixer → verifier (sequential pipeline)
```

### Example: Security Review
```
Spawn 3 agents:
  1. "Review this Python codebase for security vulnerabilities. List each issue with file, line, severity, and suggested fix."
  2. "Apply security fixes to the following files based on these findings: [reviewer output]"
  3. "Verify that these security fixes are correct and haven't introduced regressions. Run tests and check the patched code."
```

---

## Pattern E: Multi-Format Output

**Best for:** Deliverables needed in multiple formats.
**Speed gain:** 2x (independent format generation).

### Template
```
Task: "Create [content] in multiple formats"
→ Split: format_1, format_2, ..., format_N
→ Each agent produces one format from shared source
→ Collect: all formats
→ Synthesize: complete multi-format deliverable
```

### Example: Report Package
```
Spawn 3 agents:
  1. "Create a markdown report about [topic]. Include executive summary, analysis, and recommendations."
  2. "Create a structured JSON report about [topic] with fields: title, summary, sections[], recommendations[], date."
  3. "Create a bulleted outline version of [topic] suitable for a presentation. Max 10 slides with 3-5 bullet points each."
```

---

## Pattern F: ACP Code Generation

**Best for:** Heavy coding tasks that benefit from specialized coding agents.
**Speed gain:** Variable (depends on coding agent capabilities).

### Template
```
Task: "Build [complex software component]"
→ Split: ACP agent (heavy code generation)
→ Orchestrate: spawn ACP with specific task
→ Collect: code from ACP session
→ Verify: test and review the output
```

---

## Common Mistakes

1. **Over-segmentation** — splitting into too many tiny tasks creates coordination overhead
2. **Under-segmentation** — keeping subtasks too large defeats the parallelism benefit
3. **Circular dependencies** — subtask A needs B's output and vice versa (impossible)
4. **Lossy synthesis** — pasting outputs without adding coherence, context, or polish
5. **Ignoring context** — each agent starts fresh; don't assume shared context unless explicitly passed

## Optimal Subtask Size

- **Small:** 1-3 subtasks — simple parallel work
- **Medium:** 4-8 subtasks — standard multi-part deliverables
- **Large:** 9+ subtasks — consider splitting into phases

## When NOT to Use

- Simple single-step tasks (overhead > benefit)
- Tasks with hard sequential dependencies
- Tasks requiring real-time collaboration between agents
- When total task time < 5 minutes (sequential is faster)
