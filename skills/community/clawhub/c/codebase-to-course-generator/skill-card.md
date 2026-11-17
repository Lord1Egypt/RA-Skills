## Description:

Turns a target codebase into an interactive, browser-openable HTML course that explains how the code works for non-technical learners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaki6](https://clawhub.ai/user/yaki6)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI-assisted builders use this skill to turn a local or GitHub codebase into an educational walkthrough. The generated course explains architecture, data flow, code snippets, debugging points, and practical engineering vocabulary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted repository content may be turned into browser-executed HTML or JavaScript without clear sanitization safeguards.

Mitigation: Use the skill only on trusted codebases until generated HTML escaping and sanitization are reviewed, and inspect the generated course before opening it in a browser.

Risk: The skill can read a target codebase, write a generated course directory, optionally clone a GitHub repository, and open generated HTML in a browser.

Mitigation: Run it in a workspace that exposes only the intended project, verify any GitHub URL before cloning, and review the output directory path before execution.

## Reference(s):

- [Codebase to Course ClawHub Listing](https://clawhub.ai/yaki6/skills/codebase-to-course-generator)
- [README](README.md)
- [Content Philosophy](references/content-philosophy.md)
- [Design System Reference](references/design-system.md)
- [Interactive Elements Reference](references/interactive-elements.md)
- [Gotchas](references/gotchas.md)
- [Module Brief Template](references/module-brief-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Directory of HTML, CSS, JavaScript, optional Markdown briefs, and an assembled index.html course]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally clone a user-provided GitHub repository, read a target codebase, write a generated course directory, and open the generated HTML in a browser.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
