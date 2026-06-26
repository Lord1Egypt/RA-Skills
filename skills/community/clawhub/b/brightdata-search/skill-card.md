## Description: <br>
Search the web via the Bright Data CLI using keyword SERP commands or intent-ranked discovery with optional page content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Bright Data web search and discovery workflows, collect SERP or semantic result URLs, and optionally retrieve page content for later analysis or scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Bright Data credentials and may process sensitive search queries. <br>
Mitigation: Use the intended Bright Data account or API key, authenticate through the documented CLI flow, and avoid sensitive queries unless their use has been approved. <br>
Risk: Search and discovery results may include untrusted external page content, including block pages or misleading content. <br>
Mitigation: Validate JSON output, confirm non-empty result arrays and expected fields, check included content for block-page signatures, and review privacy, copyright, and retention needs before using fetched bodies. <br>
Risk: SERP order and localization can vary by geography, language, and device. <br>
Mitigation: Set country, language, and device flags explicitly when reproducible or region-specific search results are required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/meirk-brd/brightdata-search) <br>
- [Flag Reference](references/flags.md) <br>
- [Search Patterns](references/patterns.md) <br>
- [Worked Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and Bright Data JSON result artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce URL lists and optional markdown page bodies from Bright Data discovery results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
