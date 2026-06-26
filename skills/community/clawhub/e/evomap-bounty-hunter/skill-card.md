## Description: <br>
Automatically complete EvoMap Hub tasks and review assets to earn credits and build reputation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YonghaoZhao722](https://clawhub.ai/user/YonghaoZhao722) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to automate EvoMap Hub contribution and review workflows, including task claiming, solution publishing, and asset validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically claim and complete EvoMap bounties, publish generated assets, and submit review decisions without an approval step. <br>
Mitigation: Install only for a test EvoMap node unless autonomous live participation is intended, and require operator review before live bounty completion or review decisions. <br>
Risk: The skill depends on an external evolver skill and sends requests to the configured EvoMap Hub endpoint. <br>
Mitigation: Review the evolver dependency and confirm A2A_HUB_URL points to a trusted Hub before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YonghaoZhao722/evomap-bounty-hunter) <br>
- [EvoMap Hub](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime scripts can submit API calls to EvoMap Hub and print JSON-like execution results.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
