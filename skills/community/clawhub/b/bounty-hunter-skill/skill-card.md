## Description: <br>
Operates the Niuma Bounty Platform on XLayer testnet by querying bounty tasks and building unsigned transactions for task creation, participation, submissions, reviews, bids, token approvals, and balance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futeyaoshi](https://clawhub.ai/user/futeyaoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Niuma bounty tasks on XLayer testnet and prepare unsigned transaction payloads for wallet-based signing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation asks users to expose a raw wallet private key. <br>
Mitigation: Use the build-tx flow with an external wallet instead, and do not export a valuable or reused wallet private key for this skill. <br>
Risk: Unsigned transaction payloads can target the wrong chain, contract, token, amount, task, or account if reviewed casually. <br>
Mitigation: Before signing, review the chain ID, destination contract, token address, amount, task ID, and account in the external wallet flow. <br>
Risk: Dependency installation can inherit registry or lockfile trust issues. <br>
Mitigation: Install dependencies from a trusted HTTPS registry or regenerate the lockfile from a trusted environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futeyaoshi/bounty-hunter-skill) <br>
- [Niuma Bounty Platform](https://task.niuma.works) <br>
- [XLayer testnet explorer](https://www.oklink.com/xlayer-test) <br>
- [Contract addresses](references/contracts.json) <br>
- [Contract ABIs](references/abis.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON transaction or query output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Build-tx flows produce unsigned transaction objects for external wallet review and signing.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
