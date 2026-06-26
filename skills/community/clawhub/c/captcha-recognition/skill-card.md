## Description: <br>
Recognizes CAPTCHA images using ddddocr library. Invoke when user needs to recognize/decode CAPTCHA images or mentions captcha verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to recognize text in CAPTCHA images supplied as local files, image bytes, PIL images, or HTTP/HTTPS image URLs when they are authorized to process those images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary HTTP/HTTPS URLs supplied as image inputs. <br>
Mitigation: Use it only with URLs the user is authorized to process, and avoid untrusted or internal URLs unless the execution environment can safely make those requests. <br>
Risk: The skill has broad CAPTCHA/OCR activation scope and could be misused to bypass third-party verification systems. <br>
Mitigation: Limit use to authorized CAPTCHA images and do not use it to circumvent third-party access controls or verification flows. <br>
Risk: Sensitive local paths or private image contents may be exposed to the OCR workflow when passed as inputs. <br>
Mitigation: Do not provide sensitive local paths or images unless the environment and dependencies are trusted for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Moxin1044/captcha-recognition) <br>
- [Publisher profile](https://clawhub.ai/user/Moxin1044) <br>
- [ddddocr project](https://github.com/sml2h3/ddddocr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Guidance] <br>
**Output Format:** [Plain text recognition result, with optional Markdown code examples for API or command-line use] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process local files, HTTP/HTTPS URLs, bytes, or PIL images; Blob URLs require browser-side download or resolution before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
