# Quality Checklist — Full Specification

Moved from main SKILL.md §12.

## 12.1 Statistics

- [ ] All statistics from user input
- [ ] No missing df / p / CI / effect size
- [ ] p-value format consistent
- [ ] Non-significant results correctly reported
- [ ] No fabricated post-hoc / simple effects
- [ ] Each statistical value in revision from current round's user input or explicitly authorized carry-over
- [ ] No context-carryover hallucination (previous test data leaking in)
- [ ] 【Meta-analysis】No "significant" written for adjusted effect without p-value
- [ ] 【Meta-analysis】No "robust/stable" written when I² ≥ 50%
- [ ] 【Meta-analysis】No "Q-test significant, therefore random-effects"
- [ ] 【LMM/Regression】Lower-order coefficients correctly interpreted per reference level/coding
- [ ] 【LMM/Regression】No "predicted/as expected" when hypothesis not provided

## 12.2 Writing

- [ ] Clear results organization
- [ ] Main before auxiliary
- [ ] No laundry list
- [ ] Clear figure/table narrative
- [ ] Restrained tone
- [ ] Matches target journal
- [ ] No compressed omnibus statistics (e.g., "Fs > 6.4") when exact values available
- [ ] No private marginal mean calculation without annotation
- [ ] No SD/SE/CI confusion (error bar type matches caption)
- [ ] Error bar type not assumed when caption doesn't specify
- [ ] Bootstrap count from user input; not auto-filled as 5000/10000
- [ ] No proportion/magnitude wording when proportion mediated not provided
- [ ] Variable translations accurate and consistent throughout
- [ ] p-value format consistent (not mixing p = .021 and p = 0.021)
- [ ] No "sleep-enhanced memory" wording without sleep control design
- [ ] No visual judgment language without actual image
- [ ] EEG–behavior correlation not written as "only appears in/absent from"

## 12.3 Boundary

- [ ] No unsolicited citations (including alternative phrasings)
- [ ] No Discussion content in Results
- [ ] Correlation not written as causation
- [ ] Exploratory not written as main conclusion
- [ ] Non-significant not written as "proven no effect"
- [ ] No overuse of "显著提高/显著降低"

## 12.4 Target-Paper Style Adaptation (full list: see §19 in main SKILL)
- 40+ checklist items covering: style extraction, source integrity, design match, derived statistics, placeholder rules, translation rules, statistical-effect prefix, extraction coverage, test-context carryover, file-output completeness, Module H bridge usage, and design-incompatible fallback.

Full checklist: see main SKILL.md §12.4 or `docs/target-paper-adaptation.md`.
