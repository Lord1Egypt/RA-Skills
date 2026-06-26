## Description: <br>
A thin proxy to the remote whylingxi.cn insurance-advisor chat for insurance planning, product comparison, budget allocation, and Q&A, preserving session continuity and returning the service's reply with minimal transformation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lpb123](https://clawhub.ai/user/lpb123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to forward China insurance-planning, product-comparison, budget-allocation, and insurance Q&A requests to a remote advisor while preserving multi-turn session continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Insurance messages may contain sensitive medical, financial, identity, or family details and are sent to a third-party chat service. <br>
Mitigation: Install only if comfortable with whylingxi.cn receiving the messages, and avoid sharing unnecessary sensitive details. <br>
Risk: Session continuity can link later messages to an earlier upstream conversation. <br>
Mitigation: Use --reset-session or clear the session mapping file when a fresh conversation is desired. <br>
Risk: The remote service can fail, time out, or change behavior. <br>
Mitigation: Report remote-service unavailability and do not fabricate product names, prices, or planning results. <br>


## Reference(s): <br>
- [Integration notes](artifact/integration-notes.md) <br>
- [Remote insurance advisor endpoint](https://whylingxi.cn/chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown-style upstream chat response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preserve upstream tables, product names, prices, links, and session continuity.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
