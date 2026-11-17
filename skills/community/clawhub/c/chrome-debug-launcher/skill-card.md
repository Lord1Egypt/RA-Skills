## Description:

Launches two independent Chrome browser instances, one normal and one with remote debugging enabled on local port 9222.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengzongxin](https://clawhub.ai/user/chengzongxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to open a regular Chrome session alongside an isolated remote-debugging Chrome profile for Selenium or Playwright work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can close all existing Chrome windows, which may interrupt tabs, downloads, or unsaved browser work.

Mitigation: Review before installing and confirm the browser can be closed before running the commands.

Risk: The debug Chrome instance opens a powerful browser-control interface on port 9222.

Mitigation: Keep port 9222 local, avoid signing into sensitive accounts in the debug profile, and close the debug browser when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengzongxin/skills/chrome-debug-launcher)
- [Publisher profile](https://clawhub.ai/user/chengzongxin)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific Chrome launch commands and a localhost debugging endpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
