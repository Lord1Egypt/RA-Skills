## Description: <br>
Find Alibaba suppliers via LaunchFast, draft optimized outreach messages, check replies, and manage negotiations for Amazon FBA sourcing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlockchainHB](https://clawhub.ai/user/BlockchainHB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amazon FBA sellers and sourcing operators use this skill to research verified Alibaba suppliers, prepare outreach, monitor replies, and negotiate supplier terms with user approval before messages are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can use a logged-in Alibaba session and prepare supplier messages. <br>
Mitigation: Require user approval before sending any outreach or negotiation message, and confirm the recipient and message content with screenshots before submission. <br>
Risk: Supplier conversations and negotiation details are stored as local plaintext Markdown files. <br>
Mitigation: Treat ~/.claude/supplier-conversations as sensitive, restrict local access, and delete the files when supplier data is no longer needed. <br>
Risk: Browser automation may target the wrong supplier if Alibaba page layout or search results shift. <br>
Mitigation: Verify the Alibaba contact form's To field and take screenshots before and after each form interaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BlockchainHB/alibaba-supplier-outreach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, supplier comparison tables, drafted outreach messages, browser automation steps, and local Markdown negotiation logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the user to be logged in to Alibaba, uses LaunchFast supplier research and Chrome automation tools, and stores negotiation logs under ~/.claude/supplier-conversations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
