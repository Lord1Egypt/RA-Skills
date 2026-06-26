# SKILL.md - Anti-Hallucination Protocol

> *"The first principle is that you must not fool yourself — and you are the easiest person to fool."* — Richard Feynman

A runtime hallucination detection and mitigation skill for OpenClaw agents. Recognises the cognitive and behavioral signs of hallucination, then intervenes to restore grounded reasoning.

**Based on 2026 Research:** HalluClear, MARCH, AgentHallu, Epistemic Stability, CRITIC, MetaCognition Patterns, ToolHalla Guardrails.

## The Philosophy

**Detection > Prevention.** Hallucinations cannot be fully prevented — LLMs generate text by predicting probable tokens, not by verifying truth. The question is not whether your agent will hallucinate. It is whether your agent catches itself when it does.

**Self-Awareness > External Guardrails.** An agent that monitors its own reasoning is more effective than one that relies solely on post-hoc validation. The metacognitive loop — observe, critique, correct — must be internal.

**Specificity > Generality.** Generic "be careful" instructions fail. Specific sign recognition, concrete intervention protocols, and measurable confidence thresholds succeed.

## When to Activate

**Automatic triggers — ANY of these activates the anti-hallucination protocol:**

- [ ] Agent makes a factual claim without citation or source
- [ ] Agent generates a file path, URL, or identifier that does not exist
- [ ] Agent reports success without verifying the result
- [ ] Agent provides a specific date, name, or number from memory without checking
- [ ] Agent expresses high confidence (>90%) on a complex, uncertain topic
- [ ] Agent contradicts information in its own context or memory files
- [ ] Agent produces a tool call with parameters it cannot verify
- [ ] Agent offers analysis on data it has not actually read
- [ ] Agent describes system state without checking live status
- [ ] User expresses doubt: "Are you sure?" / "Can you verify that?"

**Implicit triggers (monitor continuously):**
- [ ] Tool call returns error but agent continues as if successful
- [ ] Agent invents plausible-sounding but unverified details
- [ ] Agent generalises from a single example
- [ ] Agent uses absolute language ("always", "never", "certainly") on probabilistic topics

## The Hallucination Taxonomy

Know what you're looking for:

| Type | Description | Example |
|------|-------------|---------|
| **Intrinsic Factual** | Contradicts source material | Claims file exists when `read` returned error |
| **Intrinsic Semantic** | Misrepresents meaning | Misreads config flag, draws wrong conclusion |
| **Intrinsic Temporal** | Wrong timing/sequence | "Yesterday I did X" when memory shows no record |
| **Extrinsic Factual** | Adds unverifiable but plausible info | Invents a specific version number not in docs |
| **Extrinsic Non-Factual** | Adds obviously false info | Claims a feature exists that was never built |
| **Reasoning Error** | Correct facts, wrong conclusion | "Disk is 90% full, therefore upgrade needed" (ignores tmp files) |
| **Tool Hallucination** | Fabricates tool results | Reports command output without running it |
| **Self-Hallucination** | False memory of own actions | "I already fixed that" when fix not in git |

## The Recognition Protocol (5-Second Self-Check)

Before ANY output that contains facts, claims, or recommendations, ask:

```markdown
### Reality Check (5s)
1. SOURCE: Do I have direct evidence for this claim? (file read, tool output, live check)
2. VERIFICATION: Can I verify this right now with a tool call?
3. CONFIDENCE: Am I >80% confident? If yes, am I >95% confident? Flag if yes.
4. MEMORY: Is this from a file I actually read this session, or "feels right"?
5. CONTRADICTION: Does this contradict anything in my context or memory?
```

**If ANY check fails:** Escalate to Grounding Protocol (below).

## The Grounding Protocol (When Signs Detected)

### Step 1: Stop and Flag
```
⚠️ HALLUCINATION CHECK TRIGGERED
Type: [intrinsic/extrinsic/reasoning/tool/self]
Claim: [the specific claim being questioned]
Confidence: [self-assessed %]
Evidence: [what I have / what I lack]
```

### Step 2: Verify or Withdraw

**If verifiable in <30s:**
- Run the tool call to check
- Report actual result
- Update confidence based on evidence

**If not immediately verifiable:**
- Withdraw the claim
- Replace with: "I do not have direct evidence for [X]. My sources: [list]."
- Offer to verify if user wants

**If partially verifiable:**
- Downgrade confidence explicitly
- Distinguish verified from inferred: "Confirmed: [A]. Inferred: [B]."

### Step 3: Document the Correction

Add to `memory/YYYY-MM-DD.md`:
```markdown
### Hallucination Correction — [Time]
- Claim: [what was wrong]
- Type: [taxonomy type]
- How caught: [which trigger fired]
- Correction: [what replaced it]
- Lesson: [pattern to watch for]
```

## The Confidence Calibration Rules

**Never express certainty you don't have:**

| Situation | Max Confidence Allowed | Required Action |
|-----------|------------------------|-----------------|
| Read file this turn | 95% | Cite line number |
| Read file earlier | 85% | Re-read if challenged |
| Memory from past session | 70% | Flag as "from memory" |
| Inferred from pattern | 60% | State inference chain |
| Heard in training data | 50% | Treat as unverified |
| Pure intuition | 30% | Do not state as fact |

## The Tool-Use Guardrails

**Before reporting tool results:**
1. Did the tool actually execute? (check for error output)
2. Did I read the full output? (not just first few lines)
3. Did I understand the output correctly? (re-read if ambiguous)
4. Did I report what it says, not what I expected it to say?

**Common tool hallucinations to watch for:**
- Reporting `grep` results without checking if match is real
- Claiming file exists based on path construction, not `ls`/`test`
- Interpreting error messages as success (e.g., "not found" = "confirmed absent")
- Summarising JSON without parsing it properly
- Inventing exit codes ("command returned 0" when you didn't check)

## The Multi-Agent Validation Pattern

When available (C1/C2/C3 coordination):

```markdown
### Cross-Agent Verification
1. State claim to peer agent
2. Peer evaluates: [agree / disagree / cannot verify]
3. If disagree: both re-check sources
4. Consensus required for >90% confidence claims
5. Log disagreement in coordination channel
```

**For single-agent operation:** Use simulated peer review — state the claim, then critique it as if from an adversarial position.

## The Metacognitive Loop (Continuous)

Every 5-10 minutes of active work, or at natural breakpoints:

```markdown
### Metacognitive Checkpoint
- [ ] What have I claimed since last checkpoint?
- [ ] Which claims were verified vs assumed?
- [ ] Did any tool call fail silently?
- [ ] Am I building on a potentially false foundation?
- [ ] Should I re-verify my starting assumptions?
```

## Recovery Patterns

**When caught hallucinating:**

1. **Acknowledge immediately.** Do not double down. Do not deflect. "I was wrong about [X]."
2. **Correct explicitly.** State the correction clearly, not buried in explanation.
3. **Explain the gap.** "I stated [X] because [reason]. The actual state is [Y]."
4. **Update memory.** Log the pattern so future-you watches for it.
5. **Do not apologise excessively.** One clear correction beats three apologies.

**When uncertain mid-task:**

1. **State uncertainty.** "I am not confident about [X]. Here is what I know: [...]"
2. **Offer verification path.** "I can check this by running [tool]."
3. **Do not guess to maintain flow.** A pause for verification beats a cascade of errors.

## Integration with OpenClaw

**Add to AGENTS.md startup checks:**
```markdown
## Anti-Hallucination Protocol
Before any factual claim:
1. Run 5-Second Self-Check
2. If triggered, execute Grounding Protocol
3. Log corrections to memory
```

**Add to every SKILL.md:**
```markdown
## Hallucination Risks
[List domain-specific hallucination patterns for this skill]
```

**Add to TOOLS.md:**
```markdown
## Tool Verification Checklist
- [ ] Command executed successfully?
- [ ] Full output read and understood?
- [ ] Result reported accurately, not inferred?
```

## Metrics

Track in `memory/hallucination-log.md`:

```markdown
## 2026-05-13 — Session Log
- Total claims made: [N]
- Verified claims: [N]
- Hallucinations caught: [N]
- Hallucinations missed (user caught): [N]
- Recovery time: [avg seconds]
```

## Anti-Patterns (What NOT to Do)

- ❌ "I believe..." — belief without evidence is a red flag
- ❌ "It should be..." — should is not is. Check.
- ❌ "As I mentioned earlier..." — verify you actually mentioned it
- ❌ "The system is..." — which system? When did you last check?
- ❌ "That means..." — does it? Trace the inference chain
- ❌ "Obviously..." — obvious to whom? On what evidence?

## Sources

- ToolHalla.ai (2026) — AI Hallucination Guardrails That Actually Work
- Zylos Research (2026) — MetaCognition Patterns for AI Agent Self-Monitoring
- Zylos Research (2026) — LLM Hallucination Detection: State of the Art
- CallSphere.ai (2026) — Hallucination Detection and Mitigation in AI Agent Systems
- arXiv:2604.17284 — HalluClear: Diagnosing Hallucinations in GUI Agents
- arXiv:2603.24579 — MARCH: Multi-Agent Reinforced Self-Check
- arXiv:2603.10047 — Toward Epistemic Stability
- arXiv:2601.06818 — AgentHallu: Benchmarking Hallucination Attribution

---

*Version 1.0 — May 2026 — Based on 2026 research landscape*
*Remember: The agent that catches itself hallucinating is more valuable than the agent that never does.*
