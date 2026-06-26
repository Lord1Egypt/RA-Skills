# Eight-Dimension Analysis — Evaluation Criteria, Self-Check Lists & Pattern Library

Reference manual for retrospective analysis. Loaded in Step 2 to provide self-check lists, evaluation criteria, and recommendation templates for each dimension.

**Core requirement**: Every dimension must go through its self-check list item by item. A dimension can only be skipped when ALL self-check items are answered "no."

---

## Dimension 1: AI Self-Reflection ⭐ (Highest Priority — Must Be Analyzed First)

### Self-Check List (answer each item)

- [ ] Did the AI give a wrong judgment or conclusion at any point? (e.g., "this is expected behavior" when it wasn't)
- [ ] Did the AI miss something it should have checked? (e.g., modified serialization code but didn't check input boundary cases)
- [ ] Did the AI jump to conclusions prematurely without investigating deeper? (e.g., said "no problem" based on surface symptoms)
- [ ] Did the AI only discover an issue after the user asked, when it should have found it proactively?
- [ ] Did the AI miss critical technical constraints or edge cases during planning/design?
- [ ] Did the AI fail to anticipate foreseeable side effects? (e.g., changed output format but didn't consider parser compatibility)
- [ ] Did the AI's code introduce bugs that required post-fix? Analyze root cause for each bug separately

### Analysis Method

For each "yes" answer:
1. **Locate event**: Which specific conversation turn did this happen?
2. **Quantify impact**: How many extra turns of conversation/debugging did this cause?
3. **Counterfactual reasoning**: If the AI had done X at that point, what could have been avoided?
4. **Root cause classification**:
   - Cognitive blind spot (didn't know a technical fact)
   - Insufficient analysis (only looked at surface, didn't trace root cause)
   - Check omission (changed A but didn't check related B)
   - Over-optimism (declared "no problem" too early)

### Recommendation Template

```
**AI Self-Reflection** [Priority: X]
- Event: Turn N, AI did/didn't do XXX
- Impact: Caused M extra turns / introduced bug / delayed discovery
- Counterfactual: If XXX had been done, YYY could have been saved
- Root cause: Cognitive blind spot / Insufficient analysis / Check omission / Over-optimism
- Improvement: In similar future scenarios, should ZZZ
```

---

## Dimension 2: Verification Strategy

### Self-Check List

- [ ] Did the AI define clear verification criteria before starting implementation? (e.g., "verification passes when X appears in Y")
- [ ] Did the AI proactively provide verification steps/checklists to the user? Or passively wait for "take a look"?
- [ ] After each verification round, did the AI check all core metrics? Or did it only look at some before concluding?
- [ ] When verification failed, did the AI provide clear troubleshooting direction? Or did it take multiple rounds to locate the issue?
- [ ] Could verification rounds have been fewer? If the AI had given a complete checklist upfront, could the user have verified in one pass?

### Common Problem Patterns

| Pattern | Problem | Improvement |
|---------|---------|-------------|
| Passive verification | Waiting for user to say "I ran it, take a look" | AI should proactively output verification checklist with expected results |
| Partial verification | Only checked new feature, not core objectives | Verify against requirements item by item |
| Missing edge cases | Didn't verify boundary conditions/error paths | Checklist should include happy path + boundary + error cases |
| Multi-round verification | User had to run tests repeatedly | Give complete verification plan upfront to minimize round-trips |

### Recommendation Template

```
**Verification Strategy** [Priority: X]
- Event: <specific verification scenario>
- Problem: <efficiency loss during verification>
- Counterfactual: If AI had provided verification checklist [item1, item2, ...] at turn N, M round-trips could have been saved
- Recommendation: <improved verification strategy>
```

---

## Dimension 3: Automation Opportunities

This dimension identifies repetitive workflows or hand-written scripts that could be encapsulated into reusable automations — regardless of the specific tool ecosystem.

### Self-Check List

- [ ] Was any operation executed 2+ times during the session? (e.g., hand-written analysis scripts, formatted output)
- [ ] Was there a fixed multi-step process (3+ steps) that followed the same pattern?
- [ ] Did the AI hand-write scripts that could be templatized or tool-ized? (especially one-off Python/shell scripts)
- [ ] Are there operations that would likely recur in future sessions?

### Common Signal Patterns

| Signal | Example |
|--------|---------|
| Hand-written one-off script ≥2 times | Multiple Python scripts analyzing similar data files |
| Multi-step fixed process | "Every time: first X, then Y, finally Z" |
| Domain-specific knowledge | Operations involving specific APIs, framework conventions, business rules |
| Repeated instructions | User giving same guidance across different sessions |

### What "automation" means per tool

| AI Tool | Automation Mechanism |
|---------|---------------------|
| WorkBuddy | Skills (SKILL.md + directory structure) |
| Cursor | .cursor/rules, custom instructions, notepads |
| Claude Code | CLAUDE.md, project instructions, slash commands |
| GitHub Copilot | .github/copilot-instructions.md, custom instructions |
| Windsurf | .windsurfrules, Cascade workflows |
| Cline | .clinerules, custom instructions |
| Generic | Prompt templates, checklists, runbooks stored in project |

### Recommendation Template

```
**Automation Opportunity** [Priority: X]
- Suggested name: <descriptive-name>
- Trigger scenario: <when should this be used>
- Core workflow: <main steps overview>
- Repetition count this session: N times
- Estimated benefit: <what it saves or improves>
- Implementation hint: <which automation mechanism fits your tool>
```

---

## Dimension 4: Existing Automation Tuning

This dimension evaluates any pre-existing automations, templates, rules, or custom instructions that were active during the session.

### Self-Check List

- [ ] Were any automations/skills/rules/custom instructions triggered during this session? If so, did the AI follow them completely?
- [ ] Was the automation's output corrected or supplemented by the user?
- [ ] Were there scenarios where an automation should have triggered but didn't?
- [ ] Did the automation's output conform to project conventions (paths, naming, format)?

### Common Signal Patterns

| Signal | Possible Problem |
|--------|-----------------|
| AI skipped a step from the automation | Instructions unclear or step description ambiguous |
| Output doesn't match project conventions | Automation not adapted to project-specific rules |
| User manually corrected output | Quality criteria not specific enough |
| Automation didn't trigger when it should have | Trigger conditions not accurately described |

### Recommendation Template

```
**Automation Tuning** [Priority: X]
- Target: <automation/skill/rule name>
- Problem found: <specific issue description>
- Suggested fix: <which part to modify and how>
- Expected improvement: <effect after modification>
```

---

## Dimension 5: Tool Integration Opportunities

This dimension identifies operations that would benefit from dedicated tool integrations, plugins, or API connections — beyond what the AI assistant provides out of the box.

### Self-Check List

- [ ] Did the session involve repeated calls to external APIs or services?
- [ ] Were there operations requiring specific tool capabilities the AI currently lacks?
- [ ] Were there multi-step operations that could be encapsulated into a single tool call?

### Evaluation Criteria

| Characteristic | Suitable For |
|---------------|-------------|
| Needs independent conversation context | Custom agent/sub-agent |
| Needs multi-step reasoning | Custom agent/sub-agent |
| Single function call | Tool plugin / MCP server / API integration |
| Needs external service connection | Tool plugin / MCP server / API integration |

### Tool integration mechanisms per AI tool

| AI Tool | Integration Options |
|---------|-------------------|
| WorkBuddy | MCP servers, custom Agents, Skills with scripts |
| Cursor | MCP servers, custom tools |
| Claude Code | MCP servers, custom slash commands |
| GitHub Copilot | Extensions, MCP servers (preview) |
| Windsurf | MCP servers, tool integrations |
| Generic | Shell scripts, API wrappers, CLI tools |

### Recommendation Template

```
**Tool Integration Opportunity** [Priority: X]
- Type: Agent / Plugin / MCP / API wrapper / CLI tool
- Name: <suggested-name>
- Function: <what it does>
- Current pain point: <the problem without it>
- Implementation hint: <which mechanism fits your tool>
```

---

## Dimension 6: Knowledge Persistence

### Self-Check List

- [ ] Were important technical facts established during the session? (e.g., a module's internal call chain, an API's behavioral characteristics)
- [ ] Did the user correct the AI's behavior and indicate the right approach?
- [ ] Were there significant architecture/design decisions and their rationale?
- [ ] Did the user express clear preferences or conventions?

### Knowledge Categories

| Type | Where to Persist | Examples |
|------|-----------------|---------|
| Global preferences | Tool's memory/persistent config | "I prefer concise output", "Reply in Chinese" |
| Project conventions | Project config or docs | "Callback chain for module X is..." |
| Technical decisions | Project docs or decision log | "Used approach A because..." |

### Persistence mechanisms per tool

| AI Tool | Persistence Options |
|---------|-------------------|
| WorkBuddy | `update_memory`, working memory files, MEMORY.md |
| Cursor | .cursor/rules, notepads, project instructions |
| Claude Code | CLAUDE.md, project-level memory |
| GitHub Copilot | .github/copilot-instructions.md |
| Windsurf | .windsurfrules, memories |
| Cline | .clinerules, custom instructions |
| Generic | README notes, project docs, config files |

### Recommendation Template

```
**Knowledge Persistence** [Auto-execute if possible]
- Type: Global preference / Project convention / Technical decision
- Content: <specific information to persist>
- Suggested location: <where to store, adapted to your tool>
- Reason: <why this is worth persisting>
```

---

## Dimension 7: Documentation Updates

### Self-Check List

- [ ] Did this session's changes involve architecture modifications? Do architecture docs need updating?
- [ ] Are there new coding standards/conventions that should be documented?
- [ ] Are there new tools/scripts that need usage instructions?

### Recommendation Template

```
**Documentation Update** [Priority: X]
- Target document: <file path or document name>
- Update content: <what to add/modify>
- Update reason: <why the update is needed>
```

---

## Dimension 8: Workflow Efficiency

### Self-Check List

- [ ] Were multiple independent steps executed sequentially? (Could have been parallelized)
- [ ] Was the same code/script hand-written multiple times? (Should be reused or tool-ized)
- [ ] Were suboptimal tools or methods used? (Better alternatives exist)
- [ ] Did the AI do unnecessary work? (Over-analysis, redundant verification)
- [ ] How many conversation turns were wasted? What percentage of total turns?

### Common Patterns

| Pattern | Efficiency Loss | Improvement Direction |
|---------|----------------|----------------------|
| Sequential search | Searching files one by one | Use global/project-wide search |
| Trial and error | Multiple modifications to the same spot | Analyze root cause before modifying |
| Hand-written one-off scripts | Rewriting analysis scripts for each verification | Encapsulate into reusable automation |
| Missing verification | No verification after modification | Verify immediately after changes |
| Plan gaps | Plan didn't cover critical constraints | Add technical constraint review step to planning |

### Recommendation Template

```
**Workflow Efficiency** [Priority: X]
- Scenario: <specific efficiency bottleneck>
- Waste quantified: ~N conversation turns / M repeated operations
- Counterfactual: If XXX, could have saved YYY
- Improvement: <more efficient approach>
- Applicability: This session only / General recommendation
```

---

## Priority Scoring Rules

| Priority | Criteria |
|----------|---------|
| **High** | High frequency (encountered in almost every session) OR high impact (≥3 wasted turns) |
| **Medium** | Occasional but with clear improvement path (1-2 wasted turns) |
| **Low** | Nice-to-have improvement, not essential but worth considering |

Prioritize high-priority findings in output. No limit on findings per dimension, but each finding must have a specific event reference and quantified analysis.
