## Description: <br>
Professional SEO/GEO website auditor skill evaluating LLM citation readiness, technical accessibility, and semantic authority. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, SEO, and web teams use this skill to audit target domains for AI search visibility, crawler accessibility, semantic structure, and citation readiness. It produces scored findings and optimization roadmaps for agent-first and human-first websites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local audit script makes outbound requests to target websites and, with --e2e, to search providers using the provided domain and prompt. <br>
Mitigation: Run audits only for domains and prompts that can be shared with those services, and avoid --e2e for sensitive targets. <br>
Risk: The audit script may retry failed HTTPS fetches without certificate verification, so results from sites with broken TLS can be less trustworthy. <br>
Mitigation: Treat findings from sites with TLS errors as preliminary and confirm them manually before relying on the report. <br>


## Reference(s): <br>
- [Emergence SEO GEO Homepage](https://emergence.science/skills/emergence-seo-geo) <br>
- [Emergence Science SEO-GEO Audit Tool](https://emergence.science/en/tools/seo-geo) <br>
- [OpenAPI Description](https://api.emergence.science/openapi.json) <br>
- [Content Index](https://api.emergence.science/content/index.json) <br>
- [Bundled Audit Report Example](examples/emergence_science_analysis_en.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with scored audit findings, JSON script output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform outbound website fetches and optional live search index checks when the audit script is run with --e2e.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
