## Description:

Davos helps agents create vertical HTML poster templates and capture them with a browser screenshot for social sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhsongchao](https://clawhub.ai/user/zhsongchao)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use Davos to draft 800x1200 Chinese-language posters for social channels, especially agriculture, livestock, legal, and consulting layouts. The skill guides creation of an HTML file, browser preview, screenshot capture, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preview workflow can expose the user's entire Desktop over an unauthenticated local web server.

Mitigation: Serve only a temporary folder containing the poster, bind the server to 127.0.0.1, stop the exact server process after screenshotting, and avoid storing sensitive files in the served directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhsongchao/skills/easy-html-poster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with HTML/CSS and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshot-ready HTML poster files and local preview commands when an agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
