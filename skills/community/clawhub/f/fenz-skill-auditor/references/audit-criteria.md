# Skill Audit Criteria

Rubrics for evaluating Claude skills across six categories. Each criterion is rated **Pass**, **Partial**, or **Fail**.

---

## 1. Effectiveness

How well the skill achieves its stated purpose and guides Claude's behavior.

| Criterion | Pass | Partial | Fail |
|-----------|------|---------|------|
| **Description quality** | Clear WHAT + WHEN in frontmatter; Claude can reliably trigger on relevant user requests | Has description but missing WHEN triggers or too vague | Missing, generic, or misleading description |
| **Trigger clarity** | Description covers natural language variations users would actually say | Covers some triggers but misses obvious phrasings | Too narrow or too broad — false negatives or false positives |
| **Workflow definition** | Clear step-by-step instructions; Claude knows what to do at each stage | Steps exist but some are ambiguous or missing details | No clear workflow; Claude must guess at process |
| **Examples provided** | Includes concrete examples for complex or ambiguous steps | Some examples but not for the trickiest parts | No examples where they would clearly help |
| **Error handling** | Addresses likely failure modes with specific recovery actions | Mentions some errors but without clear recovery steps | No error handling guidance |

### Scoring
- **Strong**: 4-5 criteria Pass
- **Adequate**: 3 criteria Pass, rest Partial
- **Weak**: 2+ criteria Fail

---

## 2. Token Usage

How efficiently the skill uses context window tokens.

| Criterion | Pass | Partial | Fail |
|-----------|------|---------|------|
| **SKILL.md length** | Under 500 lines; concise instructions | 500-800 lines; some bloat but manageable | Over 800 lines; excessive inline content |
| **Progressive disclosure** | References external files for details; SKILL.md is a router | Some external references but key content still inline | Everything in SKILL.md; no external file usage |
| **Reference efficiency** | Reference files are focused and relevant; no redundancy | Some redundancy across files | Large reference files with much irrelevant content |
| **Total token footprint** | Under 2,000 estimated tokens | 2,000-5,000 tokens | Over 5,000 tokens |
| **Conditional loading** | Loads files only when needed (e.g., "if user asks about X, read Y") | Some conditional logic | All files loaded upfront regardless of need |

### Scoring
- Use `scripts/analyze_tokens.py` output for quantitative data
- **Low** (good): <2,000 tokens with progressive disclosure
- **Medium**: 2,000-5,000 tokens
- **High** (concern): >5,000 tokens or no progressive disclosure

---

## 3. Time Spending

Expected time/complexity for skill execution.

| Criterion | Pass | Partial | Fail |
|-----------|------|---------|------|
| **Workflow complexity** | Linear flow with clear decision points | Some branching but manageable | Complex branching with unclear conditions |
| **External tool calls** | Minimal necessary tool calls; batched where possible | Moderate tool usage; some could be combined | Excessive tool calls; many unnecessary steps |
| **User interaction** | Asks user only when genuinely needed | Some unnecessary confirmations | Too many interruptions or none when needed |
| **Scope clarity** | Clear boundaries on what the skill does and doesn't do | Mostly clear with some ambiguous edges | Unbounded scope; could run indefinitely |

### Rating
- **Quick**: Simple workflow, few tool calls, minimal interaction
- **Moderate**: Multi-step workflow, several tool calls, some interaction
- **Extended**: Complex workflow, many tool calls, significant interaction

---

## 4. Permissions

Tool access requested and their justification.

| Criterion | Pass | Partial | Fail |
|-----------|------|---------|------|
| **Minimal permissions** | Only requests tools actually needed | Requests some unnecessary tools | Broad tool access beyond what's needed |
| **Justification** | Each tool's purpose is clear from the workflow | Most tool usage is clear | Tool usage unclear or unjustified |
| **Destructive tools** | No destructive tools, or clearly justified with safeguards | Destructive tools with some safeguards | Destructive tools without safeguards |
| **Network access** | No network, or clearly justified (e.g., git clone for a specific purpose) | Network access with partial justification | Unexplained network access |
| **File scope** | Reads/writes limited to specific directories | Mostly scoped but some broad access | Unrestricted file system access |

### Red Flags
- `Bash` without scope restrictions
- File operations outside the skill's working directory
- Network access without clear justification
- `Write` or `Edit` to system files

---

## 5. Safety

Risk assessment for the skill's behavior.

| Criterion | Pass | Partial | Fail |
|-----------|------|---------|------|
| **Description-behavior consistency** | Skill does exactly what description says | Mostly consistent with minor extras | Description doesn't match actual behavior |
| **Network access scope** | No network, or limited to stated URLs/domains | Network access broader than stated | Unrestricted or hidden network access |
| **File scope** | Operates only within expected directories | Mostly scoped with minor overreach | Reads/writes unexpected locations |
| **Sensitive data handling** | No access to secrets/credentials, or explicitly handles them safely | Touches sensitive data with some precautions | Accesses secrets without safeguards |
| **Injection resistance** | User inputs are validated/sanitized before use in commands | Some validation but gaps exist | User input passed directly to shell/commands |

### Risk Levels
- **Low**: All Pass, no concerning patterns
- **Medium**: Mostly Pass with 1-2 Partial
- **High**: Any Fail, or multiple concerning patterns

---

## 6. Recommendations

Best-practice compliance and improvement opportunities.

| Category | Check |
|----------|-------|
| **Structure** | Follows recommended directory layout (scripts/, references/, assets/) |
| **Naming** | SKILL.md (exact case), kebab-case directories, clear file names |
| **Documentation** | Skill purpose is clear to both Claude and human readers |
| **Maintainability** | Easy to update; no hardcoded values that should be configurable |
| **Reusability** | Components could be reused in other skills where appropriate |
| **Testing** | Can be tested in isolation; expected outputs are verifiable |

### Priority Levels
- **High**: Issues that affect safety, correctness, or major effectiveness
- **Medium**: Issues that affect efficiency or maintainability
- **Low**: Style and convention suggestions
