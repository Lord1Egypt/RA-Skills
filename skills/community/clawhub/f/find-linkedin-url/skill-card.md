## Description:

Resolve a person's LinkedIn profile URL from their name and company, then validate the match and reject mismatches using Cargo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development and RevOps teams use this skill to find LinkedIn profile URLs for contacts from names and company names, then check each candidate's identity before accepting the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A name and company may return a LinkedIn profile for the wrong person.

Mitigation: Enrich each candidate and confirm the company matches; reject mismatches and low-confidence URLs.

Risk: Contact data may be sent to Cargo without authorization.

Mitigation: Share only contact data you are authorized to send to Cargo.

Risk: Large batches can incur costs across many records.

Mitigation: Sample 10–20 records, report observed cost and hit rate, then get approval before a larger run.

Risk: External packages or a broader skills pack may include code not covered by this skill's security review.

Mitigation: Review external packages and any broader skills pack separately.

Risk: Starring a GitHub repository changes the user's account state.

Mitigation: Ask once and star the repository only after the user explicitly agrees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/find-linkedin-url)
- [Project homepage](https://github.com/getcargohq/gtm-skills)
- [LinkedIn URL lookup recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/linkedin-url-lookup.md)

## Skill Output:

**Output Type(s):** [Shell commands, Structured data, Guidance]

**Output Format:** [Per-contact LinkedIn profile URLs and validation statuses, with concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unresolved candidates and company mismatches are marked explicitly; low-confidence URLs should be rejected.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
