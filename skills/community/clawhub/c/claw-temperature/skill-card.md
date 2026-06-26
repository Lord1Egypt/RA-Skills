## Description: <br>
Adds occasional GIF reactions after OpenClaw's main reply, with automatic API key registration and free Beta access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangych](https://clawhub.ai/user/wangych) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to add occasional GIF reactions after main chat replies when a turn clearly signals task success, blockage, frustration, or delight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and may display a generated service API key. <br>
Mitigation: Treat the generated API key as a secret and mask it before sharing recharge, debug, or support output. <br>
Risk: Reaction requests are sent to the publisher's hosted GIF API. <br>
Mitigation: Install only if the publisher-hosted API is acceptable, and keep metadata summaries short, non-sensitive, and free of secrets. <br>
Risk: Hosted API failures or recharge-related paths could interrupt or confuse the reaction flow. <br>
Mitigation: Keep fail-open behavior so the main reply continues without a GIF, and avoid sharing recharge output until any key exposure is removed or masked. <br>


## Reference(s): <br>
- [OpenClaw Temperature ClawHub Listing](https://clawhub.ai/wangych/claw-temperature) <br>
- [OpenClaw Temperature Manifest](https://claw-temp.nydhfc.cn/openclaw-skill/manifest.json) <br>
- [Hosted API](https://claw-temp.nydhfc.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown image output plus JSON-like initialization and reaction status objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores one generated API key locally and sends short reaction-event metadata to the hosted API for selected moments.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata, manifest.json, package.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
