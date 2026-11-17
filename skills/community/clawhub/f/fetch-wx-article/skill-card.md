## Description:

Fetches WeChat public article content from mp.weixin.qq.com links and converts the HTML content to Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomjamescn](https://clawhub.ai/user/tomjamescn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflows use this skill to extract text, title, author, and body content from shared WeChat public article URLs for downstream processing or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch script can retrieve any user-supplied URL rather than enforcing the documented WeChat article scope.

Mitigation: Run it in an isolated, low-privilege environment and add URL allowlisting for mp.weixin.qq.com before routine use.

Risk: The skill fetches remote web content and depends on external Python packages.

Mitigation: Review the target URL before execution and pin dependency versions during installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomjamescn/skills/fetch-wx-article)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ignores links and images by default when converting fetched HTML content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
