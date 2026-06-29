## Description: <br>
Cynefin helps an agent classify ambiguous decisions into Clear, Complicated, Complex, Chaotic, or Confused domains and match the decision method to the situation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill when familiar playbooks fail, experts disagree, or a crisis needs domain diagnosis before action. It guides the agent to elicit the situation, diagnose cause-effect structure, choose the matching Cynefin method, and produce a boundary-watch plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides advisory judgment for ambiguous situations, and its recommendations may be inappropriate if applied without human review. <br>
Mitigation: Require explicit confirmation before acting on any real-world, destructive, financial, or account-changing recommendation. <br>
Risk: A domain diagnosis can be wrong when the user provides incomplete facts or when conditions shift during a crisis. <br>
Mitigation: Use the skill's boundary-watch and re-diagnosis steps, and involve domain experts before committing to high-stakes actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/cynefin) <br>
- [Publisher profile](https://clawhub.ai/user/deciqai) <br>
- [Sources - cynefin](references/sources.md) <br>
- [Method in Action: Snowden at IBM (1999) and the HBR Synthesis (2007)](examples/snowden-at-ibm-1999-and-the-hbr-synthesis-2007.md) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured diagnosis fields and step-by-step coaching prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user input at explicit WAIT checkpoints during novice coaching.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
