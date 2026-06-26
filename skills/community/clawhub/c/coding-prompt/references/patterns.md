## 3. Communication Patterns

Patterns that improve AI communication efficiency but are often overlooked.

### 3.1 Context Anchoring

AI's recall of conversation context degrades after ~10 turns. Key constraints agreed upon early may be forgotten.

**Rule**: When a conversation exceeds 10 turns and you reference a prior decision/constraint, restate it explicitly — never say "as discussed before" or "like we agreed."

### 3.2 Failure Recovery

When AI produces clearly wrong output, "wrong, redo" is inefficient — AI loses the useful parts of the previous attempt.

**Rule**: When correcting, provide an anchor point:
1. Identify specifically what's wrong
2. State the correct direction or principle
3. Optionally reference an analogy: `Similar to how X handles this`

**Pattern**: `The <specific part> is wrong because <reason>. The correct approach is <direction>. Keep everything else as-is.`

### 3.3 Priority Declaration

When a prompt contains multiple requirements, AI treats them equally. Important things may get the same effort as minor things.

**Rule**: For prompts with 3+ requirements, explicitly prioritize:
- `P0: <must-complete> | P1: <should-complete> | P2: <nice-to-have>`
- Or: `Focus on X first. Y is secondary. Z only if time permits.`

### 3.4 Output Control

AI defaults to verbose explanations. Users often just need code, or a specific format.

**Rule**: Explicitly control output when the default verbosity isn't desired:
- `Code only, no explanation`
- `Conclusion first, then reasoning`
- `Use a table, not paragraphs`
- `Be concise — skip what I didn't ask for`

### 3.5 Dependency Declaration

Tasks often depend on unfinished work. AI may assume dependencies are ready and start implementing against a non-existent foundation.

**Rule**: When a task has prerequisites, declare them:
- `Prerequisite: <X> must be completed first. If not done, do X first.`
- `This depends on <module/feature>. Check its current state before proceeding.`
