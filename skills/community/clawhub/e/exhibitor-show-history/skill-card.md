## Description: <br>
Finds a company's trade show exhibitor history using Lensmor, including dates, locations, booth context, and recurring patterns for competitive intelligence or account research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business, sales, marketing, and event teams use this skill to research where a company has exhibited, map competitors' show circuits, and plan outreach or partner discovery around trade shows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, domains, and research intent are sent to Lensmor when the skill looks up exhibitor history. <br>
Mitigation: Use the skill only when Lensmor is approved for the data being queried and avoid submitting confidential account details beyond the company identifier needed for lookup. <br>
Risk: The skill depends on LENSMOR_API_KEY and could expose paid API access if the key is mishandled. <br>
Mitigation: Keep LENSMOR_API_KEY in the agent environment, never paste or display it in outputs, and monitor key usage. <br>
Risk: Show-history results can be incomplete, ambiguous, or mismatched for common company names. <br>
Mitigation: Confirm the resolved company name and domain, ask for clarification on ambiguous matches, and avoid inferring patterns unless multiple returned records support them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weilun88313/exhibitor-show-history) <br>
- [Skill homepage](https://github.com/LensmorOfficial/trade-show-skills/tree/main/exhibitor-show-history) <br>
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=exhibitor-show-history) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown company summary, show-history table, pattern summary, and follow-up suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; accepts company name or URL with optional year and pagination inputs; does not output API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence, release metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
