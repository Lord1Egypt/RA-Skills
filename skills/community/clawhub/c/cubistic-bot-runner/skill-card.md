## Description:

Run a polite Cubistic painter bot for public participation using the Cubistic HTTP API with proof-of-work challenge handling and once-or-loop execution modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreasnordenadler](https://clawhub.ai/user/andreasnordenadler)

### License/Terms of Use:


## Use Case:

External developers and Cubistic participants use this skill to run a Node.js bot that paints only Void pixels, solves Cubistic proof-of-work challenges, and backs off on failed writes or rate limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot API key can appear in runtime logs.

Mitigation: Run with a low-privilege Cubistic bot key, avoid retaining loop-mode logs, and rotate the key if it has appeared in terminal, CI, or service logs.

Risk: The backend URL is user-controlled and the scripts do not enforce that the API key is sent only to a trusted HTTPS backend.

Mitigation: Set BACKEND_URL manually to the intended HTTPS Cubistic backend and do not send the bot key to any other service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreasnordenadler/skills/cubistic-bot-runner)
- [ClawHub publisher profile](https://clawhub.ai/user/andreasnordenadler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, BACKEND_URL, API_KEY, and optional COLOR_INDEX, MAX_ATTEMPTS, and MAX_SUCCESSES environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
