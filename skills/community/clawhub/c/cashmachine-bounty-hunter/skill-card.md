## Description: <br>
Automates multi-repo GitHub bounty searches, estimates bounty values, generates fixes with a coding agent, opens pull requests, and monitors payout progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergeysolovyev](https://clawhub.ai/user/sergeysolovyev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to search GitHub issues for bounty opportunities, prepare candidate fixes, open pull requests, handle review follow-up, and draft payout claim notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes autonomous GitHub activity, including forks, pull requests, comments, review responses, and payout-related claims. <br>
Mitigation: Require manual approval before every public GitHub action or payout claim. <br>
Risk: Generated fixes may be incorrect, incomplete, or unsafe if published without review. <br>
Mitigation: Run generated changes in a sandboxed temporary clone and require human review before publication. <br>
Risk: Broad GitHub credentials could expose repositories or accounts beyond the intended bounty workflow. <br>
Mitigation: Use a narrowly scoped GitHub token or a dedicated test account. <br>


## Reference(s): <br>
- [CashMachine Bounty Hunter on ClawHub](https://clawhub.ai/sergeysolovyev/cashmachine-bounty-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code changes, pull request text, review responses, and payout claim drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub search results, bounty estimates, temporary clone instructions, and human-review checkpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
