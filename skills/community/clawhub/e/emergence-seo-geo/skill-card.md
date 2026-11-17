## Description:

Professional GEO/SEO website auditor skill evaluating LLM citation readiness, technical accessibility, and semantic authority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, developer relations, and website teams use this skill to audit public domains for AI search readiness. It produces prioritized GEO/SEO findings, score breakdowns, and optimization roadmaps for agent-first and human-first sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled auditor can make unrestricted network requests from the user's machine.

Mitigation: Use it only for approved public websites you intend to audit, and avoid private, internal, or sensitive URLs.

Risk: E2E mode may send target domains or prompts to external search providers through local tools.

Mitigation: Enable E2E checks only for non-sensitive public targets and prompts, and review local Brave Search or Tavily CLI configuration before use.

Risk: The script can accept unauthenticated HTTPS content after a failed verified request.

Mitigation: Treat audit results as advisory and manually verify surprising findings through trusted browser or webmaster tooling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emergencescience/skills/emergence-seo-geo)
- [Emergence SEO GEO Homepage](https://emergence.science/skills/emergence-seo-geo)
- [Emergence Science SEO-GEO Audit Tool](https://emergence.science/en/tools/seo-geo)
- [Bundled Audit Report Example](artifact/examples/emergence_science_analysis_en.md)
- [Emergence Science API Specification](https://api.emergence.science/openapi.json)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON audit output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional E2E checks may add live search indexation details; audit findings should be treated as advisory.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
