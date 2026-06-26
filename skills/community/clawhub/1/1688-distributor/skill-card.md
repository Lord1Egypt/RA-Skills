## Description: <br>
Automate 1688.com product search, AI selection, batch distribution to your shop, and view distribution logs in one workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeppaura](https://clawhub.ai/user/zeppaura) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External sellers and shop operators use this skill to search 1688.com for products, select batches that match shop criteria, submit distribution to a target shop, and check distribution logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit bulk live shop distribution actions without a clear final approval step. <br>
Mitigation: Before execution, require the agent to show the logged-in account, target shop, selected products, item count, filters, and exact action, then wait for explicit approval before submitting distribution. <br>
Risk: An incorrect shop, product batch, or filter can create unwanted live listings. <br>
Mitigation: Start with a small test batch, review selected products before submission, and confirm how to remove unwanted listings before larger runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zeppaura/1688-distributor) <br>
- [1688 AI distribution workspace](https://air.1688.com/app/channel-fe/distribution-work/ai-assistant.html#/multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with JavaScript code blocks and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in 1688 distribution workspace plus a target shop and product selection criteria.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
