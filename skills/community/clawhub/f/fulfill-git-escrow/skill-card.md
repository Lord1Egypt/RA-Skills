## Description:

Fulfill a git escrow bounty by writing a solution or submitting an existing one. Use when the user wants to solve a test suite challenge, write code to pass tests, and claim a token reward. Requires the git-escrows CLI (npm i -g git-escrows).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlegls](https://clawhub.ai/user/mlegls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fulfill git escrow bounties by either writing a solution that passes a test suite or submitting an existing solution repository and commit for reward collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run git-escrows commands that use a wallet private key and submit blockchain escrow actions.

Mitigation: Use a dedicated low-value wallet and require explicit user confirmation before fulfillment or collection commands are run.

Risk: Private-key setup guidance may lead users to paste secrets into command lines or chat.

Mitigation: Avoid sharing private keys in chat or shell history; use a local .env or wallet setup process that keeps secrets out of prompts and logs.

Risk: Using an unpinned git-escrows executable can change the behavior of escrow submission commands.

Mitigation: Prefer a pinned, preinstalled git-escrows version and verify the CLI before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mlegls/skills/fulfill-git-escrow)
- [Project homepage](https://github.com/arkhai-io/git-commit-trading)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify solution files, prepare git commits, and propose git-escrows fulfillment and collection commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
