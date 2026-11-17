## Description:

Searches and displays recipes from the open-source Gar-b-age/CookLikeHOC repository for CookLikeHOC dish requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxiangxie](https://clawhub.ai/user/xiaoxiangxie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and cooking assistants use this skill to find matching CookLikeHOC recipes and present the selected recipe instructions as clean Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe lookup script may send an existing GITHUB_TOKEN environment variable to GitHub while refreshing the public recipe index.

Mitigation: Review before installing, run without ambient GitHub credentials when possible, or update the script to avoid automatically attaching credentials for public recipe lookup.

Risk: Recipe Markdown is fetched from a remote repository and may change independently of this skill release.

Mitigation: Treat fetched recipe content as untrusted user-facing text and review it before relying on it for cooking, safety, or dietary decisions.

## Reference(s):

- [CookLikeHOC repository](https://github.com/Gar-b-age/CookLikeHOC)
- [Cook Like Hoc ClawHub page](https://clawhub.ai/xiaoxiangxie/skills/cook-like-hoc)
- [Publisher profile](https://clawhub.ai/user/xiaoxiangxie)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown recipe text with optional shell command execution by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fuzzy recipe matching may return the closest available recipe or a short list of examples when no match is found.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
