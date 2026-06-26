## Description: <br>
Claw Web Fetch converts web pages, GitHub READMEs, and Reddit threads into normalized Markdown with metadata for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ernestyu](https://clawhub.ai/user/ernestyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch a single public HTTP or HTTPS URL and turn the page content into predictable Markdown for local knowledge-base ingestion, indexing, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and executes the published clawfetch npm package and its dependency tree. <br>
Mitigation: Install only when the package and dependencies are trusted, and review the bootstrap step before deployment. <br>
Risk: Fetched URLs can expose sensitive, authenticated, internal, or tokenized resources to the scraping process or optional backend. <br>
Mitigation: Use the skill only for URLs the agent is intended to fetch, and avoid sensitive or internal URLs. <br>
Risk: An optional FlareSolverr endpoint receives target URL content when configured. <br>
Mitigation: Set FLARESOLVERR_URL only to a local or otherwise trusted service. <br>


## Reference(s): <br>
- [clawfetch homepage](https://github.com/ernestyu/clawfetch) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/ernestyu/clawfetch) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text] <br>
**Output Format:** [Markdown with a metadata header] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes one HTTP or HTTPS URL per invocation; Reddit output can be limited with max-comments, and Cloudflare-challenge handling can use a trusted FlareSolverr endpoint.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata, SKILL.md frontmatter, and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
