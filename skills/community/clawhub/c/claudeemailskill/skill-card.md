## Description: <br>
Helps agents plan, draft, critique, and QA Claude-oriented email prompts and campaign copy with review gates before live email-system changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and email operations teams use this skill through an agent to structure Claude prompts, draft or critique campaign copy, generate variants, and prepare approval-ready email handoffs while keeping live-system actions behind approval gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts or critiques could introduce unsupported claims, overpromising, or compliance-sensitive language. <br>
Mitigation: Trace major claims to supplied source material and require human, legal, product, or deliverability review where the artifact marks approval needs. <br>
Risk: Email-system recommendations could be mistaken for permission to perform live operational changes. <br>
Mitigation: Separate recommendations from execution and require explicit approval before live sends, contact imports, suppression edits, DNS/authentication changes, production automation changes, provider migrations, or destructive cleanup. <br>
Risk: Prompts may expose unnecessary private or customer data during email drafting or critique. <br>
Mitigation: Use bounded source material and avoid exposing unnecessary private data in prompts. <br>


## Reference(s): <br>
- [Claude Email Skill Operating Checklist](references/operating-checklist.md) <br>
- [Claude Email Skill on ClawHub](https://clawhub.ai/polnikale/claudeemailskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text with prompts, drafts, critique rubrics, rewrite instructions, variant sets, and approval-ready copy packets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human approval before live sends, contact imports, DNS/authentication changes, suppression edits, production automation changes, or provider migrations.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
