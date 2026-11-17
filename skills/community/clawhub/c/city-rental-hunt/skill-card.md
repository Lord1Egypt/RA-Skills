## Description:

Search and triage rental listings from Chinese social platforms, especially Xiaohongshu via TikHub and optionally Douyin, for apartment hunting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dario-github](https://clawhub.ai/user/dario-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn apartment-hunting requirements for Chinese cities into zone-specific search keywords, social-platform listing triage, a shortlist, and a contact-first brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on TikHub or other social-media tooling whose permissions and account access are managed outside this skill.

Mitigation: Review those tool permissions and credentials separately before use, and keep this skill scoped to search planning, listing triage, and reporting.

Risk: Social-platform posts may be stale, spam-like, incomplete, or no longer available as real rental inventory.

Mitigation: Rank leads by freshness, constraint fit, contactability, and red flags, then verify availability, price, fees, landlord or agent status, pet policy, building age, and elevator status before acting.

Risk: Rental searches can expose personal location preferences, commute patterns, or private contact details.

Mitigation: De-identify reusable outputs by removing personal names, exact home or work identities, and private note identifiers unless the user explicitly intends to share them.

## Reference(s):

- [City Rental Hunt Playbook](references/playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown briefs with keyword lists and structured lead notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include YAML-style requirement snapshots and shell command examples.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
