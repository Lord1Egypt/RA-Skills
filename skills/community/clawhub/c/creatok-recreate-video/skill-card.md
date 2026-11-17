## Description:

Use when recreating, rewriting, or remixing a TikTok reference video into a new product-fit version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newt0n](https://clawhub.ai/user/newt0n)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, sellers, and their agents use this skill to analyze a TikTok reference video and draft a differentiated, product-fit remake or remix. It helps carry the result toward a script, storyboard, shot list, visual direction, and optional handoff to video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe run ID handling can allow saved analysis artifacts to be written outside the intended .artifacts directory.

Mitigation: Constrain or sanitize run IDs before execution and review file paths before installing in workspaces with sensitive files.

Risk: The skill sends TikTok URLs to CreatOK and stores returned analysis locally.

Mitigation: Use only references appropriate to share with CreatOK and handle generated artifact files according to workspace data policies.

## Reference(s):

- [CreatOK Recreate Video Skill Page](https://clawhub.ai/newt0n/skills/creatok-recreate-video)
- [Publisher Profile: newt0n](https://clawhub.ai/user/newt0n)
- [Common Rules](references/common-rules.md)
- [CreatOK API Keys](https://www.creatok.ai/app/workspace/api-keys)
- [CreatOK](https://www.creatok.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional shell commands and JSON artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CREATOK_API_KEY and writes analysis and recreation artifacts under the skill artifact directory.]

## Skill Version(s):

0.1.4 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
