## Description:

agent-eval-harness helps developers run repeatable agent regression tests, measure pass rates, and flag capability regressions against historical baselines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define regression test cases for agents, run them against callable agent functions, summarize pass rates, and detect regressions after skill, prompt, or model changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learner memory may store user preferences, notes, error labels, and recent operation details in local JSON files.

Mitigation: Do not record secrets, personal data, or sensitive customer context in learner notes or preferences; review and prune learned_patterns.json before sharing or packaging.

Risk: Stored learner output may influence future behavior or proposed instruction changes.

Mitigation: Treat learner insights as advisory and review exact proposed changes before applying them to skill instructions or agent behavior.

Risk: Regression baselines are persisted locally, so stale or manipulated baseline files can affect later regression judgments.

Mitigation: Keep baseline JSONL files under review, reset them intentionally when test suites change, and compare results against trusted CI artifacts where possible.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples; runtime helpers emit JSON-compatible summaries and local JSON/JSONL state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pass-rate summaries, regression flags, baseline history, and learner memory insights.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
