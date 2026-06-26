## Description: <br>
All-in-one RTO, challan, RC lookups and media downloader features for ChallanX. Accepts a single input - a URL, a free-text message, or an image - and returns concise, actionable results such as download links, summaries, or document analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rajniwebdeveloper](https://clawhub.ai/user/rajniwebdeveloper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to call or document the ChallanX OpenClaw API for media downloads, RTO/challan/RC-related lookups, and concise handling of URL, text, or image inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, text, images, and vehicle or document details submitted through this skill are sent to ChallanX. <br>
Mitigation: Install only if ChallanX is trusted with that data, and avoid sending private signed links, internal URLs, secrets, or highly sensitive documents unless disclosure is intended. <br>
Risk: The skill requires CHALLANX_API_KEY for authenticated API requests. <br>
Mitigation: Store CHALLANX_API_KEY as a runtime secret and do not hardcode it in the bundle, examples, or generated files. <br>


## Reference(s): <br>
- [ChallanX API Reference](references/api.md) <br>
- [ChallanX OpenClaw API](https://challanx.in/openclaw/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/rajniwebdeveloper/challanx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, OpenClaw hook configuration, and expected JSON or media response descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CHALLANX_API_KEY as a runtime secret for x-api-key authenticated requests.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
