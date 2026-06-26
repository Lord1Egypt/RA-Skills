## Description: <br>
Perform deep, concurrent web research using the Perplexity Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HolyGrass](https://clawhub.ai/user/HolyGrass) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and agent users use this skill to break complex research requests into targeted search queries, fetch Perplexity Search API results concurrently, and synthesize sourced findings into a Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user research queries to the Perplexity API and may automatically install an unpinned third-party Python package at runtime. <br>
Mitigation: Review SKILL.md before deployment, avoid sensitive queries unless external API sharing is intended, and prefer preinstalling or pinning the dependency in the execution environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HolyGrass/echo-openclaw-perplexity-ultimate-async-deep-researcher) <br>
- [Publisher profile](https://clawhub.ai/user/HolyGrass) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with inline hyperlink citations, supported by JSON search results from the Perplexity Search API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PERPLEXITY_API_KEY and python3; may install the unpinned perplexityai Python package at runtime; requests up to five search results per query with 2048 tokens per page.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
