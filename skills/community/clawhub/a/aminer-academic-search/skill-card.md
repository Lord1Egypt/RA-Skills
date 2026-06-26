## Description: <br>
Academic data search and analysis using AMiner Open Platform APIs for scholars, papers, institutions, journals, patents, composite workflows, and individual API routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ye4wzp](https://clawhub.ai/user/ye4wzp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to plan AMiner Open Platform queries for academic profiles, paper discovery, citation analysis, institution analysis, venue monitoring, patent lookup, and natural-language paper Q&A. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic queries, names, identifiers, and token-authenticated requests may be sent to AMiner. <br>
Mitigation: Use the skill only for data you are comfortable sharing with AMiner and follow the AMiner Open Platform terms for submitted queries. <br>
Risk: The skill requires an AMiner API token. <br>
Mitigation: Store the token in a secret or environment variable and avoid pasting it into shared prompts, logs, or committed files. <br>
Risk: Several documented endpoints have per-call costs, so repeated or bulk use can create charges. <br>
Mitigation: Review endpoint costs before high-volume workflows and prefer free or lower-cost routes when they satisfy the task. <br>
Risk: Example commands reference an external aminer_client.py helper that is not packaged with this release. <br>
Mitigation: Inspect and trust any external client script before running it, and treat generated commands as proposals to review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ye4wzp/aminer-academic-search) <br>
- [AMiner Open Platform Documentation](https://open.aminer.cn/open/doc) <br>
- [AMiner Token Console](https://open.aminer.cn/open/board?tab=control) <br>
- [AMiner Platform](https://aminer.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API-routing notes and example shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include AMiner API paths, token setup guidance, endpoint-cost notes, and workflow-specific command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
