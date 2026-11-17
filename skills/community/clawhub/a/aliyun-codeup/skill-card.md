## Description:

Manages Aliyun Yunxiao Codeup repositories by querying projects, branches, commit history, branch activity, and repository statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to inspect Aliyun Yunxiao Codeup repositories, including branches, recent commits, branch activity, and basic repository statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Codeup personal access token may be exposed through token-bearing Git clone URLs, local process listings, or Git error output.

Mitigation: Use a least-privileged, short-lived token; avoid sharing command logs; and prefer API headers or a safer Git credential mechanism before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexmayanjun-collab/skills/aliyun-codeup)
- [Aliyun Yunxiao Codeup documentation](https://help.aliyun.com/product/44893.html)
- [GitLab API documentation](https://docs.gitlab.com/ee/api/)
- [Codeup personal access token management](https://codeup.aliyun.com/settings/tokens)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and Python CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YUNXIAO_PERSONAL_TOKEN environment variable with read_api and read_repository permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
