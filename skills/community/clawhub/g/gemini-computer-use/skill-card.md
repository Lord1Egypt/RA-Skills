## Description:

Build and run Gemini 2.5 Computer Use browser-control agents with Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[am-will](https://clawhub.ai/user/am-will)

### License/Terms of Use:


## Use Case:

Developers use this skill to build and run browser-control agents that send screenshots and URLs to Gemini, execute supported Playwright actions, and ask for confirmation before actions marked as risky by the model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends browser screenshots and current URLs to Gemini during browser automation.

Mitigation: Run it in an isolated browser or container, avoid authenticated or sensitive sites, and do not use it on private-network, payment, admin, or account-management tasks without additional review.

Risk: The model can execute broad browser actions through Playwright without strong local limits.

Mitigation: Use --exclude to block risky predefined actions and add local allowlists and explicit confirmations before high-impact actions.

## Reference(s):

- [Gemini Computer Use Notes](references/google-computer-use.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Playwright setup steps, Gemini API configuration, browser action exclusions, and operational safety guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
