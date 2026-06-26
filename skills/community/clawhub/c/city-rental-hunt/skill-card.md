## Description: <br>
Search and triage rental listings from Chinese social platforms, especially Xiaohongshu via TikHub and optionally Douyin, for apartment hunting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dario-github](https://clawhub.ai/user/dario-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn apartment-hunting requirements into zone-specific searches, listing triage, shortlists, and contact briefs for rentals on Chinese social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can depend on a separate TikHub or social-media integration that may require credentials and platform access. <br>
Mitigation: Use only trusted integrations, keep API keys scoped, and follow the target platform rules. <br>
Risk: Rental searches may expose personal names, private addresses, commute details, or private note identifiers. <br>
Mitigation: De-identify private search details and avoid publishing personal names, exact private addresses, or private note IDs. <br>
Risk: Social posts may be stale, incomplete, or promotional rather than active rental inventory. <br>
Mitigation: Classify leads as keep, maybe, or discard, prioritize freshness, and verify price, availability, landlord status, pet policy, building age, and elevator details before acting. <br>


## Reference(s): <br>
- [City Rental Hunt Playbook](references/playbook.md) <br>
- [City Rental Hunt on ClawHub](https://clawhub.ai/dario-github/city-rental-hunt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefs with optional shell command examples and structured listing records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces keyword plans, keep/maybe/discard classifications, shortlists, and contact-first briefs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
