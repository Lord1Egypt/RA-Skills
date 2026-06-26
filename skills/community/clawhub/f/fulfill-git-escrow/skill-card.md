## Description: <br>
Fulfill a git escrow bounty by writing a solution or submitting an existing one. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlegls](https://clawhub.ai/user/mlegls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to fulfill git escrow bounties by understanding test suites, writing or submitting solution commits, and preparing fulfillment and collection commands for token rewards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an Ethereum private key and submit wallet-backed fulfillment or collection actions. <br>
Mitigation: Use a dedicated low-value wallet and require explicit confirmation before any command that signs, submits, collects, or uses the private key. <br>
Risk: The workflow can stage and commit broad repository changes while preparing a solution. <br>
Mitigation: Run in a clean branch or disposable repository and inspect diffs before staging or committing changes. <br>
Risk: The workflow depends on the external git-escrows CLI for token-related actions. <br>
Mitigation: Verify the git-escrows package source and version before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mlegls/fulfill-git-escrow) <br>
- [Project homepage](https://github.com/arkhai-io/git-commit-trading) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository changes, git commit details, fulfillment identifiers, and follow-up status or collection commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
