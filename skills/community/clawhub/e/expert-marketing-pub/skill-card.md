## Description:

广告与营销合规专家 routes pasted marketing materials to its bundled viral-video script analyzer and returns line-grounded structural diagnostics when the input is sufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and content reviewers use this skill to triage pasted script material into the available viral-script analyzer and receive structural findings about hooks, retention rhythm, speakability, CTA strength, and missing script segments. It is not a full advertising-compliance checker and should not be treated as authoritative legal or platform-policy review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is described as an advertising and marketing compliance expert, but server security evidence says it behaves as a local video-script structural analysis tool rather than a full compliance checker.

Mitigation: Present conclusions as script diagnostics only and require human review for legal, advertising, and platform-policy compliance decisions.

Risk: The tool keeps a local persistent usage counter that can block use after the free trial threshold and lead to a subscription prompt.

Mitigation: Disclose the local counter and trial limit before installation or execution, and run only in an environment where writing to the user home directory is acceptable.

Risk: Materials outside the bundled viral-script analyzer scope may be unmatched or only partially checked.

Mitigation: Review the returned scope and checks_not_run fields, and do not treat a lack of findings as proof that all marketing risks were checked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-marketing-pub)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [SKILL.md](artifact/SKILL.md)
- [Expert manifest](artifact/scripts/engine/expert-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON diagnostics with status, scope, findings, summary, and checks not run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local analysis; may write a small local usage counter and block after the free-use threshold.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
