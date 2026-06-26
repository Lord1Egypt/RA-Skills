# Evaluation Checklist

Use this to audit a research run or improve the skill after real use.

## Coverage

- [ ] The question, scope, exclusions, and deliverable are explicit.
- [ ] The run used an appropriate effort level.
- [ ] The aspect map covered definitions, primary evidence, implementation or empirical evidence, limitations, and counterevidence.
- [ ] Source classes were diverse enough for the task.
- [ ] The search did not overfit to one phrasing, one domain, or one vendor/project.

## Accuracy

- [ ] High-impact claims have evidence IDs.
- [ ] Evidence locators are specific enough to re-check.
- [ ] Current/version-sensitive claims include dates or versions.
- [ ] Primary sources are preferred for factual claims.
- [ ] Secondary sources are not used to override primary sources without explanation.
- [ ] Conflicting evidence is represented fairly.

## Source quality

- [ ] Evidence rows include `source_type`, `quality_score`, `stance`, and `claim`.
- [ ] At least one primary or near-primary source supports the central claim when available.
- [ ] Source independence is assessed for central claims.
- [ ] Bias, incentives, and possible staleness are noted.
- [ ] GitHub popularity metrics are not treated as proof.

## Verification

- [ ] At least one counterevidence route was searched for nontrivial topics.
- [ ] False premises were checked.
- [ ] Known limitations, failures, deprecations, and security issues were considered where relevant.
- [ ] The final answer labels `weak`, `single-source`, `stale`, `contested`, or `unknown` claims.

## Synthesis quality

- [ ] The final answer begins with the answer, not just process.
- [ ] The structure matches the user's requested deliverable.
- [ ] Tables clarify comparisons instead of adding noise.
- [ ] The method appendix is concise and useful.
- [ ] Next steps are concrete and only included when useful.

## Ledger lint interpretation

`research_ledger.py lint` returns errors for structural problems and warnings for research-quality risks. Warnings are not always failures; they tell the agent what to disclose or fix.

Common warnings:

- too few independent source families: find more corroboration or label uncertainty;
- too few source classes: broaden sources or explain why a source class is irrelevant;
- no counterevidence: run an adversarial search for contested topics;
- no evidence IDs in final report: add evidence IDs for high-impact claims;
- exceeded hop target: either prune or explain why the extra search mattered.

## Regression tests for the skill

Test the skill on these prompts:

1. `Research whether a GitHub project is production-ready.` Expected: checks README, code/docs, releases, issues, license, risks.
2. `Write a literature review of a current AI method.` Expected: papers, code/data, limitations, related work, citation graph.
3. `Verify a current claim that may be false.` Expected: freshness check, counterevidence, direct uncertainty if unresolved.
4. `Compare three tools for a build decision.` Expected: matrix, evidence IDs, recommendation, validation plan.
5. `Summarize a user-provided PDF plus web updates.` Expected: local locators plus current web verification.
