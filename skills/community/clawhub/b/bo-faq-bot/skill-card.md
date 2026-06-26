## Description: <br>
Build and query a local FAQ knowledge base from markdown files for business operations Q&A and Feishu bot responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imBing](https://clawhub.ai/user/imBing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, support teams, and business operations users use this skill to import FAQ markdown, add and manage FAQ entries, and answer common questions through a searchable local knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive business or customer data could be imported into FAQ answers that are later reused. <br>
Mitigation: Import only content intended for reuse in answers, and choose an approved storage location before creating the FAQ database. <br>
Risk: Write and delete commands can alter or remove entries from the local FAQ knowledge base. <br>
Mitigation: Export a backup before using remove or other maintenance commands, and run write/delete actions only when explicitly managing the knowledge base. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imBing/bo-faq-bot) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; FAQ search, export, and stats commands return plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local FAQ data is stored under ~/.faq-bot by default and can be redirected with FAQ_BOT_DIR.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
