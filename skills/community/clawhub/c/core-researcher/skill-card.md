## Description: <br>
Core Researcher helps agents search CORE, analyze academic papers, build literature reviews, format citations, and draft scholarly research content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bivex](https://clawhub.ai/user/bivex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and developer agents use this skill to conduct literature searches through the CORE API, summarize papers, analyze methods and findings, identify research gaps, and prepare citation-formatted scholarly writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and paper metadata requests may be sent to CORE with the user's API key. <br>
Mitigation: Provide the API key through an environment variable or secrets manager and avoid including unrelated private data in research queries. <br>
Risk: Academic summaries, citations, or research-gap claims may be incomplete or inaccurate. <br>
Mitigation: Review generated research outputs against the source papers and citation requirements before relying on them. <br>


## Reference(s): <br>
- [Core Researcher on ClawHub](https://clawhub.ai/bivex/core-researcher) <br>
- [CORE API v3](https://api.core.ac.uk/v3/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API guidance, configuration] <br>
**Output Format:** [Markdown with structured summaries, citation examples, and CORE API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON response fields returned by the CORE API; requires a user-provided CORE API key at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
