## Description:

Uses an existing Baijiahao login state to open the Baijiahao publishing page, fill a title and body, optionally convert Markdown to rich text, choose a cover, and save a draft or publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilisidu1210-ui](https://clawhub.ai/user/lilisidu1210-ui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Baijiahao posts from text or Markdown using an existing login state, with options to open the editor, save a draft, or publish after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use stored Baijiahao login data to operate a real publishing account.

Mitigation: Use a dedicated or least-privileged account where possible, keep auth files local, and avoid sharing cookie or storage-state files.

Risk: Automated draft or publish actions may save or post unintended content without a strong confirmation or reliable success check.

Mitigation: Run open-only or draft flows first, keep the browser visible when possible, and require explicit human confirmation before using publish mode.

Risk: Broad local auth or content paths may expose sensitive files to the automation flow.

Mitigation: Pass only narrow, trusted auth and content paths from a reviewed working directory.

Risk: Dependency updates for Playwright, Chromium, or markdown may change browser automation behavior or supply-chain reproducibility.

Mitigation: Install in an isolated environment and pin dependency versions when reproducible operation matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilisidu1210-ui/skills/baijiahao-publish)
- [Baijiahao publishing page](https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples; the script emits a text result line such as [RESULT] success or [RESULT] failed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Playwright with Chromium, the markdown package, and a user-supplied Baijiahao auth state.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
