## Description: <br>
Use when looking up digital movie/TV show prices, deals, charts, or recommendations across iTunes, Amazon, Vudu, and Google Play. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tracerman](https://clawhub.ai/user/tracerman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find digital movie and TV deals, compare prices across supported stores, inspect charts, and check whether current sale prices are at an all-time low. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web requests to CheapCharts and optional enrichment sites can expose the titles, stores, or deal topics being queried. <br>
Mitigation: Use the skill for non-sensitive price research and avoid submitting confidential viewing, purchasing, or business intent. <br>
Risk: Deal, price, and gift-card information may be stale or incomplete by the time a purchase decision is made. <br>
Mitigation: Treat outputs as informational and verify current prices, store availability, and checkout terms before spending money. <br>
Risk: All-time-low enrichment depends on CheapCharts DetailData behavior, including an internal endpoint described by the artifact. <br>
Mitigation: Check API status fields, handle endpoint errors, and verify important ATL claims against visible CheapCharts or store pages. <br>
Risk: Non-iTunes store coverage is described as sparser and less reliable for batch deal checks. <br>
Mitigation: Prefer title-specific lookups for non-iTunes stores and avoid claiming complete cross-store coverage unless each store result was verified. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/tracerman/cheapcharts-skill/tree/main/skills/cheapcharts) <br>
- [ClawHub skill page](https://clawhub.ai/tracerman/skills/cheapcharts) <br>
- [CheapCharts AI agent documentation](https://www.cheapcharts.com/us/ai) <br>
- [CheapCharts website](https://www.cheapcharts.com) <br>
- [CheapCharts GPT API base](https://buster.cheapcharts.de/v1/gptapi/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional curl commands, Python snippets, JSON output, and concise deal reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make public HTTP requests to CheapCharts and optional enrichment sites; no credentials are required.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata); skill documentation version 2.2.0 (source: SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
