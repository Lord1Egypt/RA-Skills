## Description: <br>
AI news aggregation and heat-ranking helper that collects current AI product launches, research papers, industry updates, funding news, open-source project updates, community viral events, and popular AI tool or agent projects, then outputs Chinese summaries with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenxcomp](https://clawhub.ai/user/kenxcomp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to gather recent AI news across newsletters, media, forums, research sources, funding coverage, and policy sources. It helps produce a ranked Chinese digest with links for readers who want a quick view of notable AI developments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on public web searches and external pages, so prompts may be exposed through search queries or page retrieval. <br>
Mitigation: Avoid including private details in news prompts and use public-interest queries only. <br>
Risk: Current-news summaries can contain incorrect or outdated claims from source material. <br>
Mitigation: Verify important claims through the source links included in the output. <br>


## Reference(s): <br>
- [AI news source recommendations](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/kenxcomp/ai-news-collectors) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Chinese Markdown summary list with ranked news items and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks 15-25 news items by heat and includes collection count, search count, covered dimensions, and update time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
