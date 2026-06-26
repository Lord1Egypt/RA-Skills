## Description: <br>
Uses dupe.com APIs to find similar products for a product or image URL provided by the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crisanmm](https://clawhub.ai/user/crisanmm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and shopping assistants use this skill to look up visually or functionally similar products from a product page URL or direct image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided product or image URLs are sent to dupe.com. <br>
Mitigation: Use public shopping or image links only, and avoid signed URLs, internal or localhost links, private CDN links, or URLs containing tokens or sensitive query parameters. <br>


## Reference(s): <br>
- [ClawHub Dupe release page](https://clawhub.ai/crisanmm/dupe) <br>
- [dupe.com agent-skill API endpoint](https://api.dupe.com/api/dupes/agent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and summarized product-match results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns product matches with title, price, store, and link; optional result limit defaults to 7 and may be capped at 20 for image URL searches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
