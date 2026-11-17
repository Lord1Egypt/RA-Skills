## Description:

Guides agents using chrome-devtools-axi for Chrome DevTools Protocol browser automation, accessibility snapshots, stale-ref-safe interactions, screenshots, console and network inspection, Lighthouse, and performance traces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs terminal-driven Chrome automation for inspecting, interacting with, and debugging web pages through chrome-devtools-axi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to run mutable, unpinned npm code that attaches to Chrome sessions.

Mitigation: Prefer a pinned, reviewed chrome-devtools-axi version and avoid latest-version npx execution for sensitive work.

Risk: Existing Chrome profiles, authenticated DevTools endpoints, and WebSocket headers may expose private browsing state or secrets.

Mitigation: Use fresh isolated browser sessions by default, connect to existing profiles or endpoints only with explicit need, and never print raw CHROME_DEVTOOLS_AXI_WS_HEADERS values.

## Reference(s):

- [chrome-devtools-axi GitHub repository](https://github.com/kunchenguid/chrome-devtools-axi)
- [Chrome Devtools Axi ClawHub page](https://clawhub.ai/tmchow/skills/chrome-devtools-axi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser-session verification steps and privacy-sensitive environment-variable handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
