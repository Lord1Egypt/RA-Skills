## Description: <br>
Run local agent-first SEO scoring, search-intent classification, and opportunity prioritization before content changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and AI agents use this skill to install and configure Agent SEO Engine, run local SEO scoring, classify search intent, rank GSC-style opportunities, and check privacy boundaries before content changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may involve OAuth tokens, API keys, service-account files, customer content, or search-console exports. <br>
Mitigation: Keep credentials and private data scoped and redacted, and avoid printing tokens, service-account JSON, local token files, or private user data. <br>
Risk: The runnable code is supplied by a linked GitHub CLI rather than executable files in the artifact. <br>
Mitigation: Review or trust the linked CLI before installing, and prefer doctor, manifest, privacy audit, connection-status, and dry-run checks before live provider calls or writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidmosiah/agent-seo-engine) <br>
- [Agent SEO Engine repository (declared by artifact)](https://github.com/davidmosiah/agent-seo-engine) <br>
- [Agent SEO Engine docs/site (declared by artifact)](https://github.com/davidmosiah/agent-seo-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup steps, privacy checks, troubleshooting guidance, and safe-use boundaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
