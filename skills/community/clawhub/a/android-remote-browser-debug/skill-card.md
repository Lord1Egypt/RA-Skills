## Description:

Guides agents through remote debugging Android Chromium-based browsers such as Edge and Chrome by using ADB port forwarding and the Chrome DevTools Protocol to inspect console logs, network requests, DOM snapshots, JavaScript evaluation, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sougannkyou](https://clawhub.ai/user/sougannkyou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an authorized Android device to a local debugging session, inspect browser state, run diagnostic JavaScript, capture page data, and troubleshoot mobile web issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote debugging can expose sensitive live browser state, including console logs, DOM content, network data, screenshots, and evaluated JavaScript results.

Mitigation: Use only with owned or explicitly authorized Android browser sessions, treat captured data as sensitive, and keep temporary outputs in a private per-run directory.

Risk: JavaScript evaluation through the Chrome DevTools Protocol can change page state or trigger unintended actions.

Mitigation: Prefer read-only diagnostic expressions and review any state-changing JavaScript before execution.

Risk: ADB port forwarding can leave a local debugging endpoint available after the task is complete.

Mitigation: Remove the specific forwarded port or all ADB forwards after debugging and delete temporary debug scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sougannkyou/skills/android-remote-browser-debug)
- [Publisher profile](https://clawhub.ai/user/sougannkyou)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands and scripts that expose live browser state through local ADB and Chrome DevTools Protocol sessions.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
