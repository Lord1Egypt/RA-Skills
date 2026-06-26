## Description: <br>
Turn client briefs, emails, or chat notes into motion design/VFX production plans, estimates, invoice drafts, and optional project folder scaffolds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wiseape11](https://clawhub.ai/user/Wiseape11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creative operations professionals, producers, and motion/VFX freelancers use this skill to convert unstructured client briefs into client-ready production plans, scoped estimates, invoice draft data, and repeatable project documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice draft pushes can send client and project billing data to a configured invoicing API. <br>
Mitigation: Use --push-invoice only intentionally, keep the API URL local or otherwise trusted, and configure a narrowly scoped API key when authentication is used. <br>
Risk: Generated estimates and production plans may contain incorrect assumptions when a brief is incomplete. <br>
Mitigation: Review the generated plan, estimate, and open questions before sharing them with a client or using them for billing. <br>


## Reference(s): <br>
- [Creative Ops Copilot on ClawHub](https://clawhub.ai/Wiseape11/creative-ops-copilot) <br>
- [Configuration example](references/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown planning documents, JSON estimate and invoice draft files, optional folder structure, and optional invoice API request result text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes docs/creative-ops/plan.md, estimate.json, and invoice-draft.json; can optionally create a project skeleton and push invoice data when explicitly requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
