## Description: <br>
Aeo helps agents run AEO audits, preview and sitemap checks, schema validation, llms.txt generation, regression comparisons, and related site fixes through the published @ainyc/aeo-audit package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arberx](https://clawhub.ai/user/arberx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and marketing or SEO engineers use Aeo to evaluate answer-engine optimization signals for public, staging, local, or static websites; compare regressions; and generate focused fixes or AI-readable files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the published @ainyc/aeo-audit npm package against websites or local build output. <br>
Mitigation: Use it only for websites and build outputs you are authorized to audit, and install it only if you are comfortable with that package. <br>
Risk: Local or private preview auditing can reach non-public systems when explicitly enabled. <br>
Mitigation: Use local/private auditing only for systems you control and require explicit opt-in before allowing local or private targets. <br>
Risk: Fix and llms modes can affect public-facing files such as robots.txt, llms.txt, llms-full.txt, schema, or page content. <br>
Mitigation: Review proposed changes before accepting them and verify generated files before deployment. <br>


## Reference(s): <br>
- [Aeo ClawHub listing](https://clawhub.ai/arberx/skills/aeo) <br>
- [AINYC homepage](https://ainyc.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON or agent audit reports, shell commands, and targeted file changes when fix or llms modes are requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write llms.txt, llms-full.txt, or robots.txt and may propose website fixes after user confirmation.] <br>

## Skill Version(s): <br>
4.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
