## Description:

Analyzes short drama scripts, dialogue, or subtitles for copyright similarity, age-rating risks, and adaptation deviation, then produces an advisory risk map and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaalenwow](https://clawhub.ai/user/aaalenwow)

### License/Terms of Use:

MIT-0

## Use Case:

Content review teams, creators, and agent workflows use this skill to scan short drama text for possible copyright overlap, age-rating concerns, and adaptation drift before publication decisions. The output supports triage and remediation planning, not legal conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional deep-analysis mode may send script excerpts to configured OpenAI or Anthropic APIs.

Mitigation: Use local-only mode for confidential or unpublished scripts unless the organization has approved sending excerpts to those providers.

Risk: Environment diagnostics can make outbound network probes.

Mitigation: Avoid running diagnostics in restricted environments unless that network traffic is acceptable.

Risk: Compliance reports can be incomplete or incorrect and do not provide legal advice.

Mitigation: Manually review high-impact copyright, age-rating, and adaptation decisions with qualified reviewers or legal counsel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaalenwow/skills/ai-drama-review)
- [Copyright Detection Guide](artifact/references/copyright_detection_guide.md)
- [Age Rating Standards](artifact/references/age_rating_standards.md)
- [Adaptation Analysis](artifact/references/adaptation_analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance, shell commands]

**Output Format:** [Structured JSON reports, Markdown reports, and concise text warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and may include risk levels, matched locations, remediation suggestions, and excerpts from analyzed scripts.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
