# Conclave Consensus Protocol v1.1

Chair-audited revision of the v0.1 architecture proposal, amended by external review (2026-08-14). Highest objective: **maximize decision quality per unit cost — never consensus, never model count, never debate length.**

Two orthogonal tag systems are used throughout:
- Implementation status: **[CORE]** current workflow · **[V1]** live now · **[L2]** deferred (needs data/infra)
- Rigor level: **[FORMAL]** standard statistical theory · **[ESTIMATOR]** needs data · **[HEURISTIC]** engineering proxy · **[POLICY]** human-set rule · **[EXPERIMENTAL]** unvalidated

Every soft number in any Conclave output must carry a rigor tag. Fake precision is the enemy.

---

## 0. What was rejected from v0.1 and why

| v0.1 item | Verdict | Reason |
|---|---|---|
| §13 w̃ᵢ = wᵢ/(1+λΣρᵢⱼwⱼ) | **REJECTED** | Ad hoc. The statistically principled aggregation of correlated estimators is inverse-covariance (GLS) weighting: w* ∝ Σ⁻¹1. Anything else needs empirical justification we don't have. |
| §17 Priority = I × D × U (product) | **REJECTED** | Product of three [0,1] terms collapses all priorities into noise. Replaced by decision-relevance-first ranking (§5 below). |
| §20 literal EVSI | **REPLACED** | True EVSI needs a likelihood model over what a new agent would say — intractable. Replaced by computable proxy: Decision-Flip Value (§6). |
| §3 fixed 7-model council | **BLOCKED** | Only 4 panelist CLIs exist (Claude, Codex, Gemini, Qwen) + Hermes + Manus. Seed/DeepSeek/Grok are not available. See §2. |
| §29C full calibration DB | **SCOPED** | Most strategic decisions never receive ground truth; Brier scores are uncomputable for them. Calibration tracking is restricted to *verifiable predictions* only (§9). |
| Multiplicative weight wᵢ = hᵢ·rᵢ·qᵢ | **[HEURISTIC]** kept with defaults | No calibration data yet. Default hᵢ = 1 for all; rᵢ, qᵢ set by chair per debate, logged, never presented as precise. |

## 1. Objective

a* = argmin_a E[L(a,θ) | E] + λ·Cost(process)

Consensus is an intermediate statistic, never the target. The chair optimizes the decision under a loss function the USER must supply or approve (default for investments: expected percentage drawdown of the account).

## 2. Modes (resource-constrained reality)

| Mode | Panelists | When | Manus |
|---|---|---|---|
| Quick | 2 CLIs + Hermes | low-risk, fast | off by default |
| Standard | 4 CLIs + Hermes | default (current implementation) | trigger-based (§7) |
| Deep | **BLOCKED** until additional panelist CLIs (DeepSeek/Grok/etc.) are installed and pass preflight | high-stakes | preferred |

Mode selection is declared by the chair in the brief; the user may override.

## 3. Round structure [CORE + V1]

- **R1 independence is absolute [CORE]**: no panelist sees another's output. Prompts identical except the explicit role-letter assignment (field lesson 13).
- **Structured R1 output [V1]**: each panelist must return JSON-ish blocks: position, claims[], evidence[], assumptions[], uncertainties[], disconfirming_conditions[], recommended_action, and self-rated confidence. Free-text reasoning follows the block. Confidence is self-reported and therefore **discounted, never trusted at face value**.
- R2+ cross-examination, constructive-opposition iron rule, anonymity, disconnection rules: unchanged [CORE].

## 4. Claim-based synthesis [V1]

The chair decomposes positions into atomic claims C₁…Cₙ (target 4–8 claims). For each claim the chair records: supporters, opponents, evidence sources cited, and **source overlap** (two agents citing the same URL/fact = one independent piece of evidence, not two). This replaces the v0.1 "evidence graph" with a flat table the chair can actually maintain in a verdict file.

## 5. Divergence triage [V1] — the Decision Reversal Test [FORMAL as a criterion]

Rank claims by **decision relevance first**:

1. **Decision Reversal Test**: if Cₖ were proven false, would the optimal action change — a*(C) ≠ a*(¬C)? If a*(C) = a*(¬C), the claim is deprioritized no matter how loud the disagreement, how low the confidence, or how many agents are arguing.
2. Among decision-relevant claims, sort by divergence (spread of panelist positions).
3. Among those, sort by whether additional evidence is obtainable at all.

Only the top 1–2 claims enter the next round's prompt. Debate rounds are **information acquisition, not conversation**: each round must target a named uncertainty and end with a verdict on whether that uncertainty materially decreased; if not, the loop stops.

## 6. Stopping rule [V1] — Decision-Flip Value (DFV), the computable EVSI proxy

Continue only if there exists an open claim Cₖ such that:

P(resolving Cₖ flips the decision) × E[loss reduction if flipped] > Cost(next round)

Estimation is deliberately crude: chair assigns the flip probability from the divergence ledger; loss reduction from the user's loss function; round cost ≈ 4–6 CLI calls ≈ 20–40 min wall time. All three numbers are **[HEURISTIC]** and must be logged in the verdict. Hard floors/ceilings from the current convergence rules (floor 2/3, ceiling 8) remain as guardrails.

## 7. Manus external advisor [V1 — upgraded by field lesson 16]

Manus is External Advisor, never a voter. Retrieval via direct REST polling (POST/GET api.manus.im/v1/tasks), ~3 min turnaround.

**Two strictly separated modes** (independence rule, v1.1):
- **Blind Reality Check**: Manus receives ONLY the original question + constraints — never the council's outputs, summaries, or intermediate verdicts. Used when an independent evidence stream is needed. Requested output: facts, sources, counter-evidence, unknowns, and the mandatory field **"what would change the conclusion?"** (feeds directly into the Decision Reversal Test).
- **Draft Review**: Manus receives the versioned final draft (as in the nakedleg debate). Used only after sign-off. The two modes must never be merged in one task.

Trigger conditions (any one):
- T1: a decision-relevant claim depends on verifiable real-world facts the council cannot check;
- T2: R1 unanimity with suspected correlated training data (all four CLIs are LLMs — herding is the default failure mode);
- T3: critical minority dissent (§8);
- T4: the topic is time-sensitive (prices, regulation, news).

Manus output is treated as **evidence**, weighted by verifiability of its sources — not as an opinion. Chair audits: does each claim carry a checkable source? Unsourced Manus assertions get weight ≈ one self-rated LLM claim.

## 8. Dissent & critical minority [CORE + V1]

Existing sign-off rules (opposition requires an executable alternative; minority opinions archived verbatim) remain. Addition: dissent triage by expected loss Dᵢ = P(Fᵢ) × Impact(Fᵢ), where P(Fᵢ) is **discounted** because it is self-reported by the dissenter (default discount ×0.5, [HEURISTIC]). If Dᵢ > 10% of the decision's expected value at stake, the dissent forces one targeted follow-up round or a Manus reality check — never silently dropped.

## 9. Aggregation math [V1]

For binary/probability questions, until calibration data exists:

1. Convert each panelist's position on the claim to pᵢ (extracted from structured output; missing → claim excluded from pooling).
2. Normalize weights: ŵᵢ = wᵢ / Σw (prevents extremization).
3. Correlation discount: N_eff = (Σŵᵢ)² / ΣᵢΣⱼ ŵᵢŵⱼρᵢⱼ with default ρ = 0.6 same-family / 0.3 cross-family **[HEURISTIC]**; report N_eff alongside every pooled number.
4. Pool in log-odds with prior z₀ = logit(0.5) unless the user supplies a base rate: z* = z₀ + Σŵᵢ(zᵢ − z₀), then p* = σ(z*). Label output "uncalibrated pooled estimate".
5. **Phase gates [POLICY]** — no learned weighting before sufficient empirical data exists:
   - N < 30 resolved predictions: equal weights only.
   - 30 ≤ N < 100: correlation/calibration research may run offline, but must NOT affect live weights.
   - N ≥ 100: GLS / BMA / correlation-aware ensembles allowed ONLY after out-of-sample validation against the baselines in §9a. Any aggregation that cannot beat equal-weight out-of-sample does not ship.

## 9a. Permanent baselines [V1, POLICY]

Every debate records two free baselines in the final report: (a) simple majority vote; (b) equal-weight pooled probability. The protocol's value is measured as Performance(Conclave) − Performance(Baseline). If the gap is not positive over time, added complexity is unjustified and must be removed.

## 10. Verdict schema [V1]

final.md keeps its current mandatory structure (dry conclusion first, consensus list, divergence & adjudication, minority verbatim, advisor handling). Added fields:

- **Decision State block** — five separate lines, never merged: Belief (pooled P, tagged uncalibrated) / Consensus (level) / Confidence (evidence quality) / Decision (action) / Decision Robustness (§10a).
- Mode used; N_eff [ESTIMATOR with heuristic priors]; claim table with per-claim status (resolved / open / accepted-risk); dissent expected-loss triage results; both baselines (§9a); every soft number carries a rigor tag.
- **Why-stopped block** [POLICY]: one of the enumerated reasons — (1) critical claims decision-stable; (2) remaining disagreement cannot change the action; (3) external evidence does not contradict; (4) DFV < cost; (5) required evidence unavailable → recommendation DO NOT DECIDE YET; (6) hard ceiling reached.

## 10a. Terminal states and Decision Robustness [V1]

Terminal states (v0.1 §28 extended): STRONG CONSENSUS / CONDITIONAL CONSENSUS / MAJORITY + CRITICAL DISSENT / UNRESOLVED / REJECT / **NO CONSENSUS — INSUFFICIENT EVIDENCE** / **DEBATE_FAILED** (agents disagree because required evidence is unavailable, not because reasoning is insufficient). Emitting NO CONSENSUS or DEBATE_FAILED when it prevents a bad decision is a success, not a failure.

**Decision Robustness** [HEURISTIC]: a small sensitivity table — flip the 2-3 load-bearing assumptions across their plausible ranges (e.g., CAPEX +10%/+20%, demand −10%/−20%) and record where the decision flips. Report HIGH / MEDIUM / LOW robustness with the flip points named. Far more useful than a naked confidence number.

## 11. Calibration logging [V1]

Every debate appends one JSONL record per **verifiable** prediction to `~/.hermes/debates/calibration.jsonl` with fields: prediction_id, question, timestamp, agent, role, probability, resolution_date, ground_truth (filled at resolution), brier_score, log_loss. Only predictions with a defined check date and an observable outcome are recorded. A cron job (or the chair at the next debate) resolves due predictions.

**Dual-track rule [POLICY]**: Track A = verifiable predictions → scored. Track B = strategic judgments ("this strategy is good") → never auto-scored; only post-hoc qualitative review. The system must never refuse hard strategic questions just because they are unscoreable.

## 11a. Research definitions (do NOT implement) [EXPERIMENTAL]

- Marginal Agent Value: MAVᵢ = Q(Council + i) − Q(Council − i). Answers "who adds marginal value" rather than "who is most accurate" (a correlated strong model may be worth less than a weaker but independent one). Research-only until the calibration log can support it.
- Risk-sensitive decisions (CVaR-style, for P(catastrophe) small-but-unacceptable cases): [L2]. For now, final.md only carries risk metadata (worst-case loss, tail probability) without CVaR machinery.
- Evidence provenance full schema: keep the lightweight version (source + source_type + date + independently_verified flag); the full schema is deferred.

## 12. What this protocol deliberately does NOT do

- No dynamic expansion mid-debate [L2].
- No learned ρᵢⱼ [L2].
- No Bayesian Model Averaging / hierarchical Bayes [L2 — unjustifiable without calibration data; would be fake precision].
- No claim that any pooled probability is calibrated before the log has data.
