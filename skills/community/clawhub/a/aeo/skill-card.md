## Description: <br>
Run AEO audits, preview branch audits, changed-page sitemap audits, local/private preview audits with explicit opt-in, sitemap origin rewriting, static-output audits, regression comparisons, site fixes, schema validation, and llms.txt generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arberx](https://clawhub.ai/user/arberx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and marketing engineers use Aeo to audit websites for AI-answer visibility, schema quality, sitemap coverage, preview-branch regressions, and llms.txt readiness, then apply targeted site fixes when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external npm audit tool against websites or local build output, including local or private URLs when explicitly enabled. <br>
Mitigation: Use local/private URL auditing only for systems you control, keep private-target auditing explicit, and review command targets before execution. <br>
Risk: Fix and generation workflows may write AEO support files such as llms.txt, llms-full.txt, or robots.txt. <br>
Mitigation: Review generated file changes before committing or deploying them. <br>


## Reference(s): <br>
- [AEO homepage](https://ainyc.ai) <br>
- [ClawHub skill page](https://clawhub.ai/arberx/skills/aeo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands, JSON or agent-format audit reports from the npm tool, and generated support files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write llms.txt, llms-full.txt, or robots.txt only when the user asks for generation or fixes.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
