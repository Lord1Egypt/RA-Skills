## Description:

Confidant helps AI agents request, receive, and save user-provided secrets through a human-in-the-loop handoff instead of chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsantos](https://clawhub.ai/user/ericsantos)

### License/Terms of Use:


## Use Case:

Developers and AI agent operators use Confidant to collect API keys, passwords, and tokens from users through a web handoff, then save them to configured files or environment setup without exposing secrets in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handoff can involve local services or public tunnel URLs.

Mitigation: Use the skill only in a trusted, clean environment and avoid public tunneling unless the user is remote and remote submission is necessary.

Risk: Direct secret, get, or stdout flows can expose credentials outside the intended save path.

Mitigation: Prefer the documented request workflow with a service or explicit save path, and avoid stdout or direct secret flows for real credentials.

Risk: Setup and fallback execution can install or run unpinned npm packages.

Mitigation: Review and pin the Confidant and localtunnel dependencies before use in managed or production environments.

Risk: The request workflow can block while waiting for a human to submit a secret.

Mitigation: Run long-lived polling in a persistent session such as tmux so execution timeouts do not interrupt credential receipt.

## Reference(s):

- [Confidant ClawHub Skill Page](https://clawhub.ai/ericsantos/skills/confidant)
- [Localtunnel Documentation](https://theboroer.github.io/localtunnel-www/)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files, guidance]

**Output Format:** [Plain text or JSON status output with URLs, request identifiers, save paths, and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local credential files and environment setup through the Confidant CLI.]

## Skill Version(s):

1.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
