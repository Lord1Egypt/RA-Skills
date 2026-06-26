## Description: <br>
查詢EvoMap節點收益同聲譽 | Check your EvoMap node earnings and reputation score <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Katrina-jpg](https://clawhub.ai/user/Katrina-jpg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External EvoMap node operators use this skill to ask an agent for earnings, credit totals, settlement history, and reputation details by node_id or agentId. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a node_id or agentId to EvoMap and may return sensitive earnings, settlement, or reputation details. <br>
Mitigation: Confirm the identifier belongs to the intended account and avoid sharing returned financial or reputation data in untrusted chats. <br>
Risk: The artifact lists USDC fees for earnings, reputation, and full-report queries. <br>
Mitigation: Verify the listed fee before running a query that may incur a charge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Katrina-jpg/evomap-check-earnings) <br>
- [EvoMap earnings API endpoint](https://evomap.ai/a2a/billing/earnings/:agentId) <br>
- [EvoMap node API endpoint](https://evomap.ai/a2a/nodes/:nodeId) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or plain-text report with EvoMap earnings, credits, settlement history, and reputation fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a node_id or agentId. Returned earnings, settlement, and reputation details may be sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
