## Description: <br>
Replicate the visual style of any website and apply it to your existing codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to capture publicly visible design language from a website and translate the resulting colors, typography, spacing, and component styling into an existing codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send arbitrary target URLs and page captures through Bright Data. <br>
Mitigation: Use it only for public website design analysis; do not target internal dashboards, authenticated pages, customer data, private URLs, or URLs containing tokens. <br>
Risk: The bundled shell scripts disable TLS verification while using a Bright Data API key. <br>
Mitigation: Remove curl -k before production use, keep the API key in environment variables only, and review external requests before execution. <br>
Risk: The skill depends on sensitive Bright Data credentials. <br>
Mitigation: Install it only where Bright Data use is intended and restrict credential access to the agent sessions that need it. <br>


## Reference(s): <br>
- [Apply Guide](references/apply-guide.md) <br>
- [Capture Guide](references/capture-guide.md) <br>
- [CSS Extraction Playbook](references/css-extraction.md) <br>
- [Bright Data account settings](https://brightdata.com/cp) <br>
- [ClawHub skill page](https://clawhub.ai/meirk-brd/brightdata-design-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, design token maps, and code or configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshots and scraped HTML files when Bright Data credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
