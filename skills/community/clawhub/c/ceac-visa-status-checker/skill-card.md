## Description: <br>
Automatically check U.S. visa application status in CEAC (NIV), solve CEAC captcha with Zhipu vision model, and return structured status JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xavierjiezou](https://clawhub.ai/user/xavierjiezou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check CEAC NIV visa application status with supplied location, case, passport, surname, and Zhipu API key inputs. It is intended for running a local CEAC status query and returning structured success or error JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles CEAC identifiers, passport-related inputs, surname data, and a Zhipu API key in a local environment file. <br>
Mitigation: Keep the .env file private, avoid hardcoding secrets, and use a dedicated Zhipu API key where practical. <br>
Risk: The workflow sends visa-status form data to CEAC and captcha images to Zhipu for OCR. <br>
Mitigation: Run the skill only when the user is comfortable with those purpose-aligned external data transfers. <br>
Risk: Captcha recognition and CEAC location matching can fail, which may produce retries or error JSON instead of a status result. <br>
Mitigation: Use the exact CEAC location text where possible, review returned errors, and avoid excessive automated checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xavierjiezou/ceac-visa-status-checker) <br>
- [LOCATION.md](references/LOCATION.md) <br>
- [CEAC status tracker](https://ceac.state.gov) <br>
- [Zhipu AI](https://open.bigmodel.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and structured JSON output from the script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints a JSON object containing CEAC status fields on success or error details on failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
