## 5. Anti-Pattern Quick Reference

Weak → Strong transformations for common situations.
For structured correction workflows, see also `references/templates.md` (Section 4.3 Correct).

| Situation | Weak Prompt | Strong Prompt |
|-----------|-------------|---------------|
| Code too complex | `Simplify this` | `Strip to core functionality. Remove all unused code. No over-abstraction.` |
| AI went off track | `That's wrong, redo` | `Stop. Direction is wrong — I want X, not Y. Re-understand the requirement. Don't keep previous code.` |
| AI changed too much | `Be careful` | `Only modify <file/function>. Don't touch other files. Report what changed.` |
| Output too verbose | *(implicit)* | `Code only. No explanation unless a key decision needs confirmation.` |
| Error stuck | *(implicit)* | `On error, log it and continue. Report all issues at the end.` |
| Naming/collision risk | `Implement X` | `When designing <rule>, construct boundary collision cases: special chars, equivalent inputs, edge cases. Fix risks before moving on.` |
| Improvement idea | `Do X instead` | `I have an idea: <X>. Evaluate first: Is it logical? Side effects? Implementation notes? Don't change code until I confirm.` |
| Clean old code | `Remove X` | `<Feature> is fully removed. Search entire codebase for residual code, imports, comments, doc references. List cleanup checklist before deleting.` |
| Pre-release audit | `Check for bugs` | `Assume I'm a brand new user. Audit: hardcoded paths? Environment assumptions? Step-order dependencies? Error message friendliness? Can it run end-to-end on a fresh machine?` |
| AI says "done" | `Great` | `Show evidence: run it and show output, or tell me which file/function implements this.` |
| Stub/placeholder delivered | *(missed)* | `This is a skeleton, not an implementation. Replace all TODO/pass/placeholder/hardcoded sample data with real logic. No stubs.` |
| Rule-based when LLM is better | `Improve accuracy` | `This must be LLM-native. No hardcoded rules, keyword lists, or scoring algorithms. The LLM's understanding is sufficient for this task.` |
| Local optimization trap | `Tweak X more` | `We've revised <X> multiple times. Stop — is the <approach/architecture> itself wrong? Re-analyze from <usage scenario/user perspective>. No more patches on the current approach.` |
| Start new feature | `Implement X` | `My daily scenario: <how I actually use it>. Design from this usage scenario, not from technical implementation.` |
