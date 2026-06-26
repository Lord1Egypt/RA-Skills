## Description: <br>
Runs a review-first autoresearch growth loop that reads analytics snapshots, preserves product truth, generates and critiques experiment variants, ranks them with Borda scoring, and outputs two review-ready A/B test variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and growth teams use this skill to turn analytics snapshots or project briefs into review-ready copy and experiment variants for landing pages, onboarding, pricing, CTAs, signup, checkout, and activation surfaces. The default workflow produces artifacts for human review before any production implementation or experiment wiring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics snapshots or event payloads may contain sensitive project data or PII. <br>
Mitigation: Use scoped analytics access, review saved snapshots before sharing, and avoid storing PII or temporary metric values in project context. <br>
Risk: Generated experiment variants could introduce misleading claims, product drift, or unsupported conversion language. <br>
Mitigation: Review final_variants.md against the product truth, data limitations, and guardrails before approving any implementation. <br>
Risk: The outer experiment loop can lead to production copy or experiment setup changes after approval. <br>
Mitigation: Keep the default workflow review-only and require explicit human approval before editing product code, wiring experiments, or launching measurement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dannyshmueli/agent-analytics-autoresearch) <br>
- [Agent Analytics homepage](https://agentanalytics.sh) <br>
- [Agent Analytics skills repository](https://github.com/Agent-Analytics/skills) <br>
- [Autoresearch Growth template](https://github.com/Agent-Analytics/autoresearch-growth) <br>
- [Regular Agent Analytics skill](https://github.com/Agent-Analytics/skills/tree/main/skills/agent-analytics) <br>
- [Autoresearch Growth Loop](references/program.md) <br>
- [Growth Loop Brief template](references/brief-template.md) <br>
- [Final Variants template](references/final-variants-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and TSV files with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local run artifacts such as brief.md, results.tsv, final_variants.md, and data snapshots; production changes require explicit human approval.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
