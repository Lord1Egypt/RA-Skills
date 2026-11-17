## Description:

AlphaClaw is a SkillHub CLI helper for searching, installing, publishing, and managing Claude Code skills with AK/SK login, skill search, installation, publishing, favorites, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use AlphaClaw to discover SkillHub skills, install them locally, and publish skill packages from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable global npm package.

Mitigation: Install only a trusted, pinned, reviewed version of the AlphaClaw npm package and avoid privileged installation patterns such as sudo.

Risk: AK/SK credentials are stored locally in ~/.alphaclaw/auth.json.

Mitigation: Protect the credential file, use a non-shared or isolated environment, and rotate credentials if exposure is suspected.

Risk: Force, yes, API override, or debug options can change what is installed, published, or exposed.

Mitigation: Review downloaded or published skill contents before using --force, --yes, --api, or --debug.

## Reference(s):

- [AlphaClaw Skill Page](https://clawhub.ai/1688aiinfra/skills/alphaclaw)
- [SkillHub Website](https://skill.alphashop.cn/)
- [AlphaShop API Key Management](https://www.alphashop.cn/seller-center/apikey-management)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local credential storage and command-line options for AlphaClaw workflows.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
