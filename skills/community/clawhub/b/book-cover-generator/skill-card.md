## Description: <br>
AI book cover generator for indie authors and self-publishers — create stunning KDP book covers, novel cover art, ebook covers, and Kindle cover designs using AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors, self-publishers, and developers use this skill to generate genre-specific book cover image URLs from text prompts via the Neta/TalesOfAI image generation API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated-image workflow data are sent to the external Neta/TalesOfAI API. <br>
Mitigation: Use the skill only when that provider is acceptable for the intended content, and avoid submitting confidential manuscript material, private data, or secrets in prompts. <br>
Risk: The skill requires a Neta API token for authenticated requests. <br>
Mitigation: Use a dedicated low-privilege token where possible and pass it through environment-variable expansion instead of typing raw secrets into shell history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/book-cover-generator) <br>
- [Neta API Token Setup](https://www.neta.art/open/) <br>
- [TalesOfAI Image Generation API](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls] <br>
**Output Format:** [Plain text URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct generated-image URL after polling the external API; requires a Neta API token and accepts optional size and reference-image UUID inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
