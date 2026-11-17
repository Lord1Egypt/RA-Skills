## Description:

Quickly view and analyze Android device page stacks, including the current page, Activity history, Fragment stack, recent tasks, and page-switch monitoring via ADB commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[githubzyq](https://clawhub.ai/user/githubzyq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, testers, and Android reverse-engineering practitioners use this skill to inspect foreground Activity state, Activity back stacks, Fragment information, recent tasks, and page transitions on Android devices they are authorized to debug.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ADB inspection can expose sensitive device, app, process, recent-task, property, or log data.

Mitigation: Use the skill only with Android devices you own or are authorized to inspect, and redact or package-scope results before sharing them.

Risk: Raw dumpsys and monitoring output may be misleading when Android versions, vendor builds, WebViews, dialogs, or disabled dumpsys fields change the reported state.

Mitigation: Confirm findings with package-scoped commands, raw output review, and Android-version-aware field checks before acting on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/githubzyq/skills/android-stack-analyzer)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline ADB command examples and shell script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume Android SDK Platform Tools, an authorized ADB connection, and device output that may vary by Android version and vendor build.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
