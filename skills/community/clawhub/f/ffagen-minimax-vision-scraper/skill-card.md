## Description: <br>
Uses Playwright to capture rendered webpage screenshots and MiniMax vision understanding to extract visible page content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ffagen](https://clawhub.ai/user/ffagen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can capture rendered webpages and ask MiniMax VLM to extract visible content such as news, finance data, or product details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured webpage screenshots and prompts are sent to MiniMax. <br>
Mitigation: Use only on pages where external processing is acceptable, and avoid logged-in, internal, personal, or confidential content unless provider handling has been reviewed. <br>
Risk: The artifact ships with a bundled API key fallback. <br>
Mitigation: Remove the bundled key and require users to provide their own MINIMAX_API_KEY through the environment. <br>
Risk: Screenshot-based automation may interact with pages that prohibit automation or scraping. <br>
Mitigation: Use the skill only on sites the operator is authorized to automate and run it in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ffagen/ffagen-minimax-vision-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/ffagen) <br>
- [Referenced Playwright scraper skill](https://clawhub.ai/skills/scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text analysis printed to stdout from a Node.js command, configured with environment variables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Captures a PNG screenshot temporarily and sends the image plus prompt to MiniMax for analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
