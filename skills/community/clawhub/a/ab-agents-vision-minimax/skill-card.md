## Description: <br>
Image analysis via the MiniMax VL API for describing images, extracting text from screenshots, and analyzing photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexburrstudio](https://clawhub.ai/user/alexburrstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to send a local image path or image URL with an optional prompt to MiniMax for visual description, OCR-style text extraction, and photo analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images may include private screenshots, documents, corporate files, or personal photos that are sent to MiniMax for processing. <br>
Mitigation: Review image sensitivity before use and avoid submitting sensitive images unless MiniMax processing is acceptable for the deployment context. <br>
Risk: The launcher may use a fallback API key file if MINIMAX_API_KEY is not set explicitly. <br>
Mitigation: Set MINIMAX_API_KEY explicitly and verify credential sourcing before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexburrstudio/ab-agents-vision-minimax) <br>
- [Project homepage](https://github.com/alexburrstudio/ab-agents-vision) <br>
- [MiniMax platform](https://platform.minimax.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text returned by the MiniMax vision tool, with shell usage examples in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and sends submitted images or image URLs to MiniMax for processing.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
