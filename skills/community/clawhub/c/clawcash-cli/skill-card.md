## Description: <br>
ClawCash helps agents use the ClawCash CLI to check USDC credit, proxy x402 calls on credit, and manage repayment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akshaydevh](https://clawhub.ai/user/akshaydevh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate the ClawCash CLI for credit-backed x402 requests, credit status checks, partner discovery, and repayment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate financial setup, credit activation, paid x402 calls, and repayment workflows. <br>
Mitigation: Require explicit user approval before package execution, token minting, credit activation, paid x402 calls, or repayment. <br>
Risk: Platform tokens and repayment URLs are sensitive credentials that can grant access or expose payment workflows. <br>
Mitigation: Keep tokens and repayment URLs out of logs, screenshots, committed files, and shared messages; prefer CLI-managed local storage. <br>
Risk: The install flow depends on identity onboarding and external CLI execution. <br>
Mitigation: Proceed only when the user intends to create or use ClawLens and ClawCash financial access, and stop for user-only verification or Terms acceptance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akshaydevh/clawcash-cli) <br>
- [ClawCash homepage](https://cash.clawlens.io) <br>
- [ClawCash SKILL.md](https://cash.clawlens.io/SKILL.md) <br>
- [ClawLens prerequisite skill](https://api.clawlens.io/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install packages, mint platform tokens, initialize local CLI state, make paid x402 requests, or generate repayment URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
