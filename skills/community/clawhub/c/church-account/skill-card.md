## Description:

Automates account workflows on churchofjesuschrist.org and LCR (Leader & Clerk Resources), including login, session reuse, service URLs, and account-related lookup or management tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathan-deepmm](https://clawhub.ai/user/nathan-deepmm)

### License/Terms of Use:


## Use Case:

External users or agents operating with authorization use this skill to guide Church Account and LCR website login, session reuse, and navigation for membership, calling, directory, finance, and related account workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill addresses sensitive church account and LCR workflows involving personal, membership, finance, or access-controlled records.

Mitigation: Use only with accounts and church data the user is authorized to access, and confirm sensitive reads or changes before each action.

Risk: The artifact includes stealth browsing guidance and a no-sandbox browser launch flag.

Mitigation: Avoid stealth or detection-bypass techniques and remove the no-sandbox browser flag before use.

Risk: The artifact describes storing reusable browser session state in a shared temporary path.

Mitigation: Store session tokens only in user-controlled, access-restricted locations and delete them when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nathan-deepmm/skills/church-account)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline Python code blocks and reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include browser automation steps, credential handling notes, service URLs, and session reuse patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
