## Description: <br>
Generates vertical WeryAI videos that show an artwork moving from sketch through color and detail to a final reveal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to prepare and submit WeryAI text-to-video or image-to-video jobs for art-process reels. It expands short briefs into production prompts, confirms generation parameters, and returns playable video URLs or clear failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WERYAI_API_KEY for paid WeryAI network generation, and successful wait runs can consume credits. <br>
Mitigation: Keep the API key secret and rotatable, review the confirmation table, and run generation only after explicit user confirmation. <br>
Risk: URL override environment variables could send prompts, image URLs, or bearer tokens to an unintended service if misconfigured. <br>
Mitigation: Leave WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL unset unless the endpoints are trusted; review the environment before production use. <br>
Risk: Image-to-video inputs must be public HTTPS URLs and may be sent to WeryAI for processing. <br>
Mitigation: Use only intended public HTTPS image URLs and avoid submitting private or sensitive source images. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zoucdr/art-process-video) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI API host](https://api.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, JSON, Text] <br>
**Output Format:** [Markdown guidance with confirmation tables, inline shell commands, and JSON command results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and WERYAI_API_KEY; image inputs must be public HTTPS URLs; successful wait runs may consume paid WeryAI credits.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
