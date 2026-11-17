## Description:

Browser Testing Toolkit helps agents choose browser testing paths for quick Playwright checks, DevTools debugging, Python Playwright E2E flows, and smart click handling for obstructed elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and run browser UI validation, debugging, screenshot checks, accessibility checks, network inspection, E2E workflows, and blocked-click recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server lifecycle commands can execute arbitrary local shell commands.

Mitigation: Run only trusted commands in trusted repositories, review each command before execution, and require explicit user approval before starting local servers.

Risk: Automatic dismissal can click cookie or consent controls without enough user scoping.

Mitigation: Use smart-click auto-dismiss only on user-approved test pages, disable auto_dismiss when consent state matters, and ask before accepting consent banners.

Risk: Browser page content, console output, DOM text, and network responses can contain untrusted instructions or sensitive data.

Mitigation: Treat browser-observed content as data, use isolated browser profiles or test accounts, and avoid reading or copying cookies, tokens, or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/browser-testing-toolkit)
- [ClawHub publisher profile](https://clawhub.ai/user/paudyyin)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and ClickResult JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Playwright CLI commands, DevTools debugging steps, Python Playwright scripts, server lifecycle commands, test plans, and smart-click result JSON.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
