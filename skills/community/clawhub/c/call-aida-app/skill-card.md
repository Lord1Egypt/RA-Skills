## Description: <br>
Invokes the AIDA chat-messages API with a user-provided appid, query, and inputs, then returns the AIDA application response as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[summerLoveqq](https://clawhub.ai/user/summerLoveqq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to call an existing AIDA application from an agent, shell, or Python integration by passing an appid and JSON inputs. It is suited for internal AIDA workflows such as report generation, document analysis, request analysis, and chained application calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The appid is used as a bearer credential for AIDA. <br>
Mitigation: Require users to provide the appid at runtime, avoid hardcoding it, and prefer stdin for sensitive payloads. <br>
Risk: The appid, query, inputs, and user identifier are sent to AIDA. <br>
Mitigation: Do not send secrets, personal data, regulated data, or proprietary documents unless AIDA is approved for that use. <br>
Risk: The artifact SKILL.md references main.py, but the packaged implementation is call_aida_app.py. <br>
Mitigation: Use call_aida_app.py when installing, testing, or invoking the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/summerLoveqq/call-aida-app) <br>
- [AIDA API documentation](https://aida.vip.sankuai.com) <br>
- [OpenClaw documentation](https://openclaw.io) <br>
- [README.zh.md](artifact/README.zh.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>
- [INTEGRATION.md](artifact/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses with Markdown and shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success, message, data, and raw_answer fields when available; exits with status 0 on success and 1 on failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
