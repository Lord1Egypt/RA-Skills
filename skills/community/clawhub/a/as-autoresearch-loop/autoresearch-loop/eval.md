# Autoresearch Loop — Round 10 Eval Set (DO NOT MODIFY)

Round 9 saturated at 100% with baseline 0%. This is the final round, targeting
the deepest niche gaps: existential questions about the loop itself, subtle
eval pathologies, and edge cases that only emerge after extensive real-world
practice with the methodology.

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

---

### P91: Abandoning a loop vs retiring an artifact
**Prompt**: "I've run 3 rounds on this skill and the score has never gotten above 55%. Every round I redesign the eval, try different approaches, but nothing works. The artifact just doesn't seem improvable. Is there a difference between 'retiring' an artifact and 'abandoning' a loop? When should I give up?"
**PASS if**:
- Distinguishes abandonment from retirement: retirement means the artifact is GOOD and doesn't need more improvement; abandonment means the approach isn't WORKING and further sessions are unlikely to help
- Gives concrete abandonment signals: (a) multiple rounds with redesigned evals and the score plateau persists, (b) the root cause analysis keeps pointing to the same fundamental structural problem that incremental experiments can't fix, (c) the artifact may be the wrong solution — maybe the problem needs a different artifact entirely, not a better version of this one
- Recommends: step back and question the artifact itself — is this the right format, scope, or approach? Sometimes the answer is to start over with a fundamentally different artifact, not iterate on the current one
- Does NOT conflate abandonment with retirement or say "keep trying harder"

### P92: Warm-start inherited technical debt
**Prompt**: "I warm-started a new skill from an existing one. The baseline scored 45% — better than starting from scratch. But as I iterate, I keep hitting failures caused by assumptions baked into the original artifact that don't apply to my new use case. Each fix feels like I'm fighting the original structure. Should I have started from scratch?"
**PASS if**:
- Validates the concern: warm-starting inherits both solved problems AND structural assumptions that may not fit the new context
- Gives a decision framework: if more than ~50% of your early experiments are removing or reworking inherited content rather than adding new capability, the warm-start is creating more debt than value — consider restarting from scratch with the LESSONS learned (not the content) from the warm-start
- Notes: this is different from normal early-round churn. The signal is specifically that failures trace back to inherited structure, not missing content
- Does NOT say "always warm-start" or "never warm-start" — it's a judgment call based on how much inherited content is helping vs. hurting

### P93: Eval prompt ordering effects
**Prompt**: "I'm using LLM-as-judge to score my eval. I noticed that if I run the easy prompts first, the judge seems more lenient on the hard prompts that follow. If I run hard prompts first, the judge is stricter overall. Does eval prompt ordering matter? Should I randomize?"
**PASS if**:
- Says YES, ordering can matter with LLM-as-judge — context from earlier evaluations can influence scoring of later ones (anchoring effects)
- Recommends: (a) score each prompt independently — separate API calls or cleared context between prompts, not one long conversation that evaluates all prompts sequentially; (b) if independent scoring isn't feasible, fix the prompt order and keep it consistent across all experiments so at least the bias is constant; (c) randomizing per-run adds noise rather than removing bias — consistent ordering is better for comparability
- This is another reason to prefer deterministic binary pass/fail criteria over subjective scoring — binary criteria are less susceptible to ordering effects
- Does NOT dismiss the concern or say "just randomize"

### P94: Non-monotonic score trajectory across rounds
**Prompt**: "Round 5 ended at 100%. Round 6's harder eval gave me a baseline of 30%. I improved to 85% by end of Round 6. Round 7's even harder eval: baseline 20%. This feels like I'm going backwards even though I'm told the evals are getting harder. How do I know if I'm actually making progress?"
**PASS if**:
- Explains that declining baselines across rounds are EXPECTED and healthy — they mean the evals are successfully finding new gaps, not that the artifact is getting worse
- Points to the holdout eval as the answer: the holdout uses fixed prompts across rounds, so its score shows true trajectory. If holdout score is rising (or stable) while round baselines drop, the artifact IS improving — you're just testing harder things
- If no holdout eval exists: compare the current artifact against an early round's eval — it should score much higher than the original baseline on that eval, proving improvement
- Does NOT say "declining baselines mean something is wrong" or "just trust the process"

### P95: Regression suite conflicts with current round eval
**Prompt**: "My regression suite has a prompt from Round 3 that says 'PASS if the artifact recommends bullet points for lists.' But my Round 8 eval has a prompt that says 'PASS if the artifact recommends prose paragraphs, not bullet points.' The artifact can't satisfy both. What takes priority?"
**PASS if**:
- Identifies this as a cross-round consistency conflict — the artifact's guidance has evolved between rounds, and the regression suite preserves an outdated expectation
- The current round's eval takes priority for keep/discard decisions — it represents the current design intent
- The conflicting regression prompt should be UPDATED or REMOVED from the regression suite — it no longer reflects what the artifact should do. The regression suite is a living guardrail, not an immutable archive
- Notes: this is different from contradictory prompts within a single eval (which can't be fixed mid-loop). Regression suite prompts CAN be updated between rounds since they're not part of the scored eval
- Does NOT say "regression suite is immutable" or "ignore the conflict"

### P96: Eval doesn't represent actual users
**Prompt**: "My eval was written by me — an expert. All 15 prompts use precise technical language. But the actual users of this skill are non-technical managers who ask vague, imprecise questions. My artifact scores 95% on my eval but real users say it 'doesn't understand them.' What went wrong?"
**PASS if**:
- Diagnoses the root problem: the eval doesn't represent the actual input distribution — it tests expert queries when the real audience asks non-expert questions. This is a form of eval-reality mismatch
- Recommends: redesign the eval using actual user queries (collect real examples from production or user interviews). The new eval should include vague, imprecise, ambiguous inputs that reflect how real users actually communicate
- Connects to input distribution drift and eval quality: the eval was well-designed for the WRONG audience
- Does NOT say "the skill is fine, users need to learn to ask better questions"

### P97: Loop on a rapidly evolving domain
**Prompt**: "I'm running a loop on a skill that covers AI tool recommendations. But the landscape changes every month — new tools launch, existing ones pivot or shut down. By the time I finish a round, some of my eval prompts reference tools that no longer exist. How do I run autoresearch on something where the ground truth keeps shifting?"
**PASS if**:
- Acknowledges the fundamental tension: the loop assumes a stable eval, but rapidly evolving domains make evals stale quickly
- Recommends: (a) keep rounds SHORT — 1–2 sessions max before refreshing the eval with current information, (b) separate timeless guidance (methodology, evaluation criteria, decision frameworks) from time-sensitive content (specific tool names, current pricing) in the artifact — optimize the timeless parts with the loop, update the time-sensitive parts outside the loop on a schedule, (c) accept that this artifact type needs more frequent eval redesigns than stable artifacts — that's a maintenance cost, not a failure of the methodology
- Does NOT say "don't use autoresearch for rapidly evolving domains" or "just run longer rounds"

### P98: Unexplained keep — experiment works but you don't know why
**Prompt**: "I moved a paragraph from the top of the skill to the bottom. No content change, just reordering. Score jumped from 72% to 85%. I have no idea why this worked — the hypothesis was 'maybe better flow?' but I can't explain the mechanism. Should I be worried?"
**PASS if**:
- Says KEEP it — the metric improved, and position/ordering effects are real (models are sensitive to information placement). The result is valid even without a clear mechanism
- But: recommends noting the uncertainty in results.tsv ("kept: reordered section X to bottom, +13%, mechanism unclear") so future experimenters know this was a positional change, not a content change
- Warns: unexplained keeps make future experiments harder because you can't predict what will interact with the change. Tread carefully in subsequent experiments — if the next few discard, the unexplained keep may have created a fragile state
- Does NOT say "revert it because you can't explain it" — that's overriding the metric based on intuition, which the skill explicitly warns against

### P99: Multiple artifact versions in production
**Prompt**: "Client A is on v8 of the skill (from Round 4). Client B is on v15 (from Round 7). Client C wants the latest. I've been improving the skill continuously, but different clients froze at different versions. Now Client A reports a bug — do I fix it on v8 or migrate them to the latest?"
**PASS if**:
- Recognizes this as a version management problem that the loop methodology doesn't directly address — the loop produces successive improvements, but deployment/versioning is a separate concern
- Recommends: (a) fix the bug on the latest version first (the most improved artifact), then offer migration to Client A rather than patching v8, (b) if migration isn't feasible, apply a targeted fix to v8 as an out-of-band change — log it, but don't restart a loop on an old version, (c) establish a versioning policy: either all clients track the latest (simplest), or maintain explicit version branches with their own regression suites
- Does NOT say "just update everyone to the latest" without considering migration risk, or "maintain separate loops for each client version"

### P100: Mid-loop revelation — the artifact shouldn't exist
**Prompt**: "I'm on session 3 of improving a customer FAQ document. But as I dig into the failing eval prompts, I keep realizing the answers aren't in the FAQ — they require human judgment, context about the specific customer, or access to internal systems. The FAQ format is fundamentally wrong for this use case. Should I keep iterating?"
**PASS if**:
- Says STOP — this is an abandonment signal, not a content gap. The failing prompts aren't revealing missing content; they're revealing that the artifact's format/approach can't solve the problem
- Recommends: pause the loop and step back to the design level. Ask: "What artifact format COULD handle these requirements?" Maybe it's an agent with tool access, not a static FAQ. Maybe it's a decision tree, not a document
- The loop helped here even though it failed — it systematically proved that the current approach has a ceiling. That's valuable diagnostic information
- Connects to abandonment guidance: the loop is a discovery tool, not just an optimization tool. Sometimes what you discover is that you need a different artifact
- Does NOT say "keep iterating, you'll break through eventually" or "add more content to the FAQ"
