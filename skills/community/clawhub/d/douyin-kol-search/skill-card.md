## Description: <br>
抖音最具商业价值意见领袖（KOL） helps creators, operators, marketers, and brands search for Douyin creators and KOL benchmark accounts using keywords and optional content-category filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketing teams, operators, and brand teams use this skill to identify Douyin KOL candidates, benchmark accounts, and cooperation or competitor-research leads from a search keyword and optional category filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive API key for the external AI Skills service. <br>
Mitigation: Store AISKILLS_API_KEY in environment variables or a secrets manager, rotate it if exposed, and avoid committing it to source files or prompts. <br>
Risk: Search terms and strategy context are sent to an external service. <br>
Mitigation: Avoid using confidential campaign strategy, private personal data, or regulated information as search inputs. <br>
Risk: AISKILLS_BASE_URL can redirect execution to a configured external endpoint. <br>
Mitigation: Use the default service URL or another trusted endpoint, and review environment configuration before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/douyin-kol-search) <br>
- [form-schema.json](references/form-schema.json) <br>
- [skill.json](references/skill.json) <br>
- [AI Skills service](https://ai-skills.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API response with creator candidates, commercial-value signals, benchmark-account references, and execution metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISKILLS_API_KEY and calls an external AI Skills API; responses depend on the configured AISKILLS_BASE_URL and available Douyin creator data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
