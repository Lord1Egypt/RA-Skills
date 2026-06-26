## Description: <br>
AetherLang Chef V3 provides Greek culinary consulting and recipe analysis with sections for food cost, HACCP, thermal curves, allergens, beverage pairing, plating, molecular gastronomy, and nutrition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contrario](https://clawhub.ai/user/contrario) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and culinary professionals use this skill to send natural-language food questions to an external culinary API for structured recipe consulting, molecular gastronomy guidance, flavor analysis, nutrition details, allergen notes, and plating plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts are sent to api.neurodoc.app for processing. <br>
Mitigation: Send only non-sensitive culinary query text, inform the user before the first API call, and do not include personal details, secrets, private documents, medical information, account data, credentials, files, environment variables, or conversation history. <br>
Risk: Provider identity or release provenance may matter for adoption decisions. <br>
Mitigation: Verify the third-party provider identity before use; server-resolved GitHub import provenance is unavailable for this version. <br>


## Reference(s): <br>
- [AetherLang Chef ClawHub page](https://clawhub.ai/contrario/aetherlang-chef) <br>
- [Publisher homepage](https://omnimusmind.com) <br>
- [AetherLang execution endpoint](https://api.neurodoc.app/aetherlang/execute) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Greek Markdown response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typical response is 4000-8000 characters; English queries are accepted and the primary output language is Greek.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
