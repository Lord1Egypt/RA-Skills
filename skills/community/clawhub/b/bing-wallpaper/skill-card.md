## Description: <br>
Use when users need to fetch the daily Bing wallpaper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JaceyMarvin99](https://clawhub.ai/user/JaceyMarvin99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve the current Bing homepage wallpaper as a link, markdown, JSON, or image output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled shell script and makes an outbound request to the disclosed 60s.viki.moe wallpaper API. <br>
Mitigation: Install and run it only in environments where that outbound request is acceptable, and review the script before execution. <br>


## Reference(s): <br>
- [60s Bing wallpaper API](https://60s.viki.moe/v2/bing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Image data, Shell commands] <br>
**Output Format:** [stdout containing plain text, JSON, Markdown, or binary image data depending on the encoding option] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional encoding parameter: text, json, image, or markdown.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
