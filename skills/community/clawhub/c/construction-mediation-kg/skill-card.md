## Description: <br>
Provides a construction commercial mediation knowledge graph for dispute diagnosis, mediation strategy, stakeholder analysis, BATNA/WATNA assessment, agreement drafting, and legal reference navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mediators, lawyers, construction cost engineers, and project managers use this skill to analyze construction disputes, plan commercial mediation workflows, evaluate negotiation alternatives, manage case evidence, and draft mediation documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive legal mediation facts and settlement positions. <br>
Mitigation: Use generic or redacted facts unless organizational policy approves the matter, provider, and data handling. <br>
Risk: Optional AI-backed functions may send case content to third-party providers. <br>
Mitigation: Configure API keys only for approved providers and avoid sending confidential, personal, or privileged materials without consent. <br>
Risk: Case and evidence management scripts write local JSON files that may contain sensitive matter data. <br>
Mitigation: Store generated files in a protected directory and define retention, deletion, and access-control practices before use. <br>
Risk: Generated legal analysis or agreement drafts may be incomplete or unsuitable for a specific matter. <br>
Mitigation: Have qualified legal professionals review legal advice, mediation strategies, and agreement drafts before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruiyongwang/construction-mediation-kg) <br>
- [Publisher profile](https://clawhub.ai/user/ruiyongwang) <br>
- [Construction dispute types](artifact/references/dispute-types.md) <br>
- [BATNA / WATNA framework](artifact/references/batna-framework.md) <br>
- [Mediation strategies](artifact/references/mediation-strategies.md) <br>
- [Legal basis quick reference](artifact/references/legal-basis.md) <br>
- [Mediation agreement template](artifact/references/agreement-template.md) <br>
- [Farui integration quickstart](artifact/scripts/farui_quickstart.md) <br>
- [Version 2 quickstart](artifact/scripts/v2_quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, document drafts, Python helper calls, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local reference files, local JSON case/evidence stores, and optional third-party legal AI API calls when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
