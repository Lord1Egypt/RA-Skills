## Description:

Aistore helps an agent navigate the AI STORE ecosystem, recommend AI STORE models, and manage marketplace skills through the gpushop CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangnan8791](https://clawhub.ai/user/wangnan8791)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Aistore to discover AI STORE skills, install or remove marketplace skills, view marketplace information, and configure AI STORE-hosted models for an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global package changes and persistent skill installation can modify the agent environment.

Mitigation: Require explicit user confirmation before installing npm packages or marketplace skills, and run the skill only in environments where persistent package changes are acceptable.

Risk: External browsing and marketplace access can disclose activity or depend on unverified remote content.

Mitigation: Avoid silent browsing; confirm network access with the user and rely on server-resolved provenance or trusted documentation when available.

Risk: Newly downloaded skills may introduce unreviewed instructions or unsafe behavior.

Mitigation: Review each downloaded skill's source, provenance, and security scan results before activating it in an agent workflow.

## Reference(s):

- [AI STORE Skill Page](https://clawhub.ai/wangnan8791/skills/aistore)
- [AI STORE Model Marketplace](https://gpushop.sh.189.cn/ModelService/onlineApi)
- [AI STORE Model API Documentation](https://gpushop.sh.189.cn/doc/guide/model-service/API-ref3.html)
- [Xiao Zhuren AI Office Platform](https://dx.mltai.cn/app-web/passport/login)
- [Xiao Lushi AI Legal Platform](https://dx.jurisai.cn/#/login?redirect=/index)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package-management commands, model configuration steps, marketplace lookups, and follow-on skill review actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
