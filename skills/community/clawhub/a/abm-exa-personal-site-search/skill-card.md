## Description: <br>
Find personal websites, blogs, and portfolios for specific people using Exa's personal site category search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find and verify a named person's personal website, blog, portfolio, or speaking page using Exa search results and fetched page content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and context are sent to an external Exa search service. <br>
Mitigation: Only include names, affiliations, and context that are appropriate to send to an external search provider. <br>
Risk: Local product marketing context may influence the search plan if present. <br>
Mitigation: Review `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md` before use and confirm it is relevant to the task. <br>
Risk: Common names or sparse affiliation details can produce results for the wrong person. <br>
Mitigation: Add role, organization, university, location, or other disambiguating context and cross-check the result before presenting it as the person's site. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariokarras/abm-exa-personal-site-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include person name, site URL, site type, content summary, and visible last-updated information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
