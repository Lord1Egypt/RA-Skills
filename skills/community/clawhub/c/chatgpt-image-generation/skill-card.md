## Description: <br>
Generate images from ChatGPT using Playwright browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Amian](https://clawhub.ai/user/Amian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative automation users can use this skill to batch-submit image prompts to ChatGPT and save the generated images with a per-prompt results log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt files are submitted to ChatGPT under the user's logged-in account. <br>
Mitigation: Do not include secrets, private personal data, or confidential business material unless that use is acceptable for the account and organization. <br>
Risk: The results log stores prompt text alongside generation outcomes. <br>
Mitigation: Protect or delete the output directory when prompt contents or generated images are sensitive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [image files, JSONL logs, shell commands, guidance] <br>
**Output Format:** [PNG image files with a JSONL results log and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Playwright/Chromium and a ChatGPT account session; generated outputs and prompt logs are written to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
