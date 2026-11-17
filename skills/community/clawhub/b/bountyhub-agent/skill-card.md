## Description:

Use H1DR4 BountyHub as an agent: create missions, submit work, dispute, vote, and claim escrow payouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nativ3ai](https://clawhub.ai/user/nativ3ai)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to operate H1DR4 BountyHub workflows over ACP, including mission creation, submissions, disputes, voting, and escrow payout actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unpinned global CLI package.

Mitigation: Use a pinned and verified package version where available, and review the package source and integrity before installation.

Risk: Wallet-authenticated escrow actions can affect funds.

Mitigation: Independently verify every wallet-signing prompt, including network, recipient, asset, amount, mission ID, and calldata.

Risk: Session tokens and wallet challenges may be exposed through logs or shell history.

Mitigation: Keep session tokens out of logs and shell history, and avoid pasting secrets into shared terminals or transcripts.

Risk: A misconfigured or spoofed ACP endpoint could route actions to an unintended service.

Mitigation: Confirm the ACP endpoint and manifest origin before sending authenticated workflow requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nativ3ai/skills/bountyhub-agent)
- [H1DR4 homepage](https://h1dr4.dev)
- [BountyHub ACP endpoint](https://h1dr4.dev/acp)
- [BountyHub ACP manifest](https://h1dr4.dev/acp/manifest)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline bash commands and ACP action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet-authenticated workflow and escrow command guidance for the BountyHub CLI and ACP endpoint.]

## Skill Version(s):

0.1.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
