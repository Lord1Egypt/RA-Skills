## Description:

Read and update Teambition test plans and individual test cases through an Ego Lite browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to inspect Teambition test plans and cases, then create or update individual cases and their statuses through an authenticated Ego Lite session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A write could target the wrong Teambition plan or case, or change a case-library record reused elsewhere.

Mitigation: Use the intended account and verify the plan, case number, and title before creating or changing case content.

Risk: Archiving a case could move the wrong item to the recycle bin.

Mitigation: Confirm the case number and title before archiving, and describe the action as moving the case to the recycle bin.

Risk: The external Ego Lite runtime and live Teambition behavior were not tested in the supplied security review.

Mitigation: Run the login check first and inspect the returned result after each write.

## Reference(s):

- [Login instructions](references/login.md)
- [Test case API guide](references/testcase-api.md)
- [Test case pitfalls](references/pitfalls.md)
- [Teambition](https://www.teambition.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text or JSON test plan and test case results, with concise action summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update an individual case, change its status, or move it to the recycle bin when explicitly requested.]

## Skill Version(s):

0.2.2 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
