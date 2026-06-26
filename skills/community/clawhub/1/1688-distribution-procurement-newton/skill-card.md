## Description: <br>
Helps operators manage 1688 distribution procurement workflows, including shop binding, source linking, automatic supply switching, order tracking, purchasing, inventory synchronization, price monitoring, seller messages, and ISV-assisted Taobao/Douyin procurement tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External commerce operators and agent users use this skill to automate or assist 1688 distribution procurement after downstream orders are created. It is intended for workflows involving shop setup, supply-source association, replacement-source discovery, order queries, procurement actions, seller follow-up messages, and ISV-backed Taobao/Douyin order or after-sale operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive AKs and ISV tokens may grant access to real procurement, shop, order, seller-message, or after-sale workflows. <br>
Mitigation: Install only for intended live-commerce use, avoid broad token sharing, and limit credential access to trusted operators and environments. <br>
Risk: The skill can invoke other local ISV skills while carrying tokens. <br>
Mitigation: Restrict which local ISV skills and paths are trusted before enabling ISV-backed actions. <br>
Risk: High-impact commerce actions may include supply changes, automatic ordering, after-sale settings, publishing, and bulk seller messages. <br>
Mitigation: Require manual confirmation before executing those actions. <br>
Risk: Credential target mismatch could route actions through an unintended account or integration target. <br>
Mitigation: Confirm the AK and ISV tokens belong to the intended account and workflow before running live actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-distribution-procurement-newton) <br>
- [Publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [1688 ClawHub AK portal](https://clawhub.1688.com) <br>
- [1688 skills gateway](https://skills-gateway.1688.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese user-facing text and Markdown, with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require python3 and sensitive 1688 AK or ISV token configuration before live commerce actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, created 2026-06-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
