## Description: <br>
Design and manage OpenClaw GEO content operations including knowledge sources, topic clusters, content tasks, publish targets, LLM-friendly artifacts, receipts, AI crawler visibility, and GEO analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, SEO/GEO teams, and developers use this skill to plan, audit, and improve an auditable GEO content operating loop across sources, tasks, publishing targets, receipts, artifacts, and analytics. It is not a single-article writing layer and requires receipts before claiming production publishing, indexing, crawler visits, rankings, or AI citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public content could be posted, updated, deleted, or unpublished without enough review if the workflow is connected to real publishing systems. <br>
Mitigation: Require explicit human review and durable receipts before any publishing, update, delete, or unpublish action. <br>
Risk: API tokens or provider secrets could be exposed if receipts or logs capture raw integration details. <br>
Mitigation: Keep secrets out of receipts and redact provider credentials from logs and artifacts. <br>
Risk: Teams could overstate live publishing, indexing, crawler visits, ranking, or AI citation outcomes without proof. <br>
Mitigation: Require receipts and evidence checks before making production, indexing, crawler, ranking, or citation claims. <br>


## Reference(s): <br>
- [OpenClaw GEO Content Ops release page](https://clawhub.ai/x-rayluan/geo-content-ops) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [GEOFlow Patterns](references/geoflow-patterns.md) <br>
- [English README](docs/readme/README_en.md) <br>
- [GitHub source reference](https://github.com/X-RayLuan/openclaw-geo-content-ops.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with JSON task and receipt structures where useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning, audit, and operating-model guidance; does not perform hidden execution or credential handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
