## Description: <br>
Short alias for content-search-summarization. Use this to search public content platforms, rank the top relevant items, and summarize them with links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allens0104](https://clawhub.ai/user/allens0104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content analysts use this skill to search public content platforms such as Bilibili and YouTube, rank relevant results, and produce concise summaries with links, capture context, confidence labels, and caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External public search and page retrieval can expose sensitive prompts, private URLs, or authenticated content if the user provides them. <br>
Mitigation: Use public topics and public URLs only; avoid private, authenticated, or sensitive inputs when invoking the skill. <br>
Risk: Summaries based on public page metadata may be incomplete or misleading if the full content was not inspected. <br>
Mitigation: Keep confidence labels and caveats in the output, and explicitly state when a summary is inferred from metadata. <br>
Risk: Platform search or scraping behavior may be subject to third-party platform rules. <br>
Mitigation: Confirm that source access and summarization comply with the relevant platform terms before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allens0104/content-summary) <br>
- [Publisher profile](https://clawhub.ai/user/allens0104) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with ranked links, capture scope, confidence labels, and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should state the search method, keyword scope, source links, per-item confidence, and when conclusions are inferred from metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
