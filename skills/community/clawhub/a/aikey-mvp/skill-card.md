## Description:

Turns a creator’s rough topic idea into a plain-text X post, records it for testing, and uses real engagement to guide whether to develop or drop the topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Independent knowledge creators use the skill to test uncertain content ideas on X before investing time in a video. It drafts a post, records the test, and interprets engagement to guide next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected vault files and post-history CSV contents enter the agent’s context.

Mitigation: Select only the intended vault and post-history CSV.

Risk: The workflow may create drafts, update the testing pipeline or saved preferences, and replace clipboard contents.

Mitigation: Review local changes and clipboard contents before using them.

Risk: A drafted post may be published before its claims and wording are checked.

Mitigation: Review the draft before manually publishing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-text X post with Markdown draft and testing-pipeline records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local drafts and pipeline records and replace clipboard contents; publishing remains manual.]

## Skill Version(s):

0.2.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
