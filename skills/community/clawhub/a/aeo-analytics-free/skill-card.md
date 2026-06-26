## Description: <br>
Tracks AI visibility by scanning target prompts to measure whether AI assistants mention and cite a brand, then reports mention and citation trends and content opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketers, SEO/AEO teams, and developers use this skill to monitor brand visibility in AI-generated answers, compare mention and citation rates over time, and prioritize content improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, brand names, and domain information may be sent to Gemini or search providers during scans. <br>
Mitigation: Use non-confidential prompts and brand data unless sharing that information with the selected provider is acceptable. <br>
Risk: The skill stores scan history locally, which may include response excerpts, citation URLs, competitors, and trend data. <br>
Mitigation: Store the history file in an approved location and review or delete it when it is no longer needed. <br>
Risk: A Gemini API key may be used for grounded scans. <br>
Mitigation: Store GEMINI_API_KEY in an environment variable or keychain instead of writing it into prompts, files, or reports. <br>


## Reference(s): <br>
- [AEO Analytics Data Schema](references/data-schema.md) <br>
- [Using Gemini API with Grounding for AEO Analytics](references/gemini-grounding.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/psyduckler/aeo-analytics-free) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, API calls, guidance] <br>
**Output Format:** [Markdown reports and JSON scan-history files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target domain, brand names, and tracked prompts; may use GEMINI_API_KEY for grounded Gemini scans or web search as a fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
