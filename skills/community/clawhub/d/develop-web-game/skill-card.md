## Description:

Use when Codex is building or iterating on a web game (HTML/JS) and needs a reliable development and testing loop: implement small changes, run a Playwright-based test script with short input bursts and intentional pauses, inspect screenshots and text state, and review console errors with render_game_to_text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tbeard602](https://clawhub.ai/user/tbeard602)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to build, iterate, and test browser-based HTML/JavaScript games with a Playwright-driven loop. It helps agents validate controls, canvas rendering, deterministic time stepping, screenshots, console errors, and concise text-state output while maintaining a progress handoff log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags guidance to use an unpinned global npm install fallback for Playwright-related tooling.

Mitigation: Prefer an existing local Playwright dependency or install a pinned local version before using any global fallback.

Risk: The security guidance notes that progress.md can contain prompts or other sensitive working context.

Mitigation: Avoid writing secrets, credentials, sensitive prompts, or private project details into progress.md.

Risk: The skill runs browser automation against local game builds and writes local test artifacts.

Mitigation: Run it only in workspaces where browser automation and local artifact creation are expected, and review generated screenshots and logs before sharing.

## Reference(s):

- [Action payload examples](artifact/references/action_payloads.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and local artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, console logs, text-state JSON, and progress.md notes during the game testing loop.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
