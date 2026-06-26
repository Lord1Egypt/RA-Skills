## Description: <br>
Extracts main webpage content with the Defuddle library and converts it to Markdown for content scraping, text processing, and automation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeholdon](https://clawhub.ai/user/yeholdon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to extract readable article content from URLs or local HTML files, convert the result to Markdown or JSON, and optionally route extracted text into messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional send scripts transmit extracted page text to WeChat or Telegram. <br>
Mitigation: Use those scripts only with trusted pages and destinations, and avoid sensitive or internal URLs. <br>
Risk: The WeChat send helper path is hardcoded to a local user path. <br>
Mitigation: Inspect or replace the helper path before running the script. <br>
Risk: Extraction commands invoke the npm defuddle package. <br>
Mitigation: Verify the npm package source before use. <br>


## Reference(s): <br>
- [Defuddle ClawHub page](https://clawhub.ai/yeholdon/defuddle-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JavaScript examples, plus extracted Markdown or JSON content from the Defuddle CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional scripts can print extracted content locally or send it to WeChat or Telegram.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
