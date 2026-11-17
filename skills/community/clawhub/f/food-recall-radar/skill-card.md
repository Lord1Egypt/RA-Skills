## Description:

Food Recall Radar helps agents maintain a local pantry inventory, query openFDA food-enforcement recalls, fuzzy-match stored food items against ongoing Class I/II/III recalls, extract lot-code hints, and produce a risk-ranked action list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and household caregivers use this skill to record pantry items and run recall checks after grocery trips, recall news, or weekly audits. It helps prioritize package checks, discard decisions, and refund returns while directing users to confirm each hit against the FDA notice.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The local pantry file can contain purchase and household details in plaintext.

Mitigation: Use an appropriate local file location, protect the user account and device, and avoid storing unnecessary household notes.

Risk: Verbose logging can expose an optional openFDA API key in logs or transcripts.

Mitigation: Run without an API key for normal household use when possible, avoid verbose mode when a key is configured, and rotate any key that has already been exposed.

Risk: Recall matching is intentionally conservative and can produce false positives or miss lot-specific nuance.

Mitigation: Treat MATCH and VERIFY results as prompts to inspect the package and read the FDA notice before discarding food or seeking a refund.

## Reference(s):

- [Food Recall Matching Problem Reference](references/recall-matching.md)
- [Sample cached recalls](references/sample-recalls.json)
- [openFDA food enforcement endpoint](https://api.openfda.gov/food/enforcement.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and text reports from the recall checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON pantry data and cached recall data when the user runs the bundled script.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
