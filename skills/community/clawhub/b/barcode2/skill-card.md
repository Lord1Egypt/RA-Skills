## Description: <br>
Generates barcode images as base64 content from barcode type and parameters, or recognizes barcode type and number from a barcode image URL or base64 image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate common barcode formats or recognize barcode contents through JisuAPI. It is suited for workflows that need barcode images, barcode type detection, or barcode number extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JisuAPI AppKey. <br>
Mitigation: Treat JISU_API_KEY as a secret and avoid committing or logging it. <br>
Risk: Barcode values, barcode image URLs, or base64 barcode images are sent to JisuAPI for processing. <br>
Mitigation: Avoid submitting sensitive internal labels or regulated data unless JisuAPI's privacy and retention terms are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/barcode2) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI barcode generation and recognition API](https://www.jisuapi.com/api/barcode/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation returns barcode image base64 content; recognition returns barcode type and number records.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
