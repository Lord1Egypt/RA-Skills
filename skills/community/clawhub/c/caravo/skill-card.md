## Description: <br>
Caravo Service Marketplace helps agents discover and execute paid external services through the Caravo CLI across AI media generation, search, data, finance, communication, file conversion, and infrastructure tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Azure-Vision](https://clawhub.ai/user/Azure-Vision) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to route tasks that require external data, paid APIs, media generation, web or academic search, communication, file upload, or market data through Caravo's CLI-based service marketplace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad authority to broker paid external-service calls. <br>
Mitigation: Use a limited API key or low-balance dedicated wallet, pin the CLI version where possible, and require explicit approval before any paid call. <br>
Risk: The skill can send email or SMS, upload local files, publish files to public links, scrape websites, and process confidential or personal data through external services. <br>
Mitigation: Require explicit user approval before communication, upload, scraping, or confidential-data actions, and avoid providing sensitive data unless the user has confirmed the destination and purpose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Azure-Vision/caravo) <br>
- [Caravo homepage](https://caravo.ai) <br>
- [Agent-Skills repository from metadata](https://github.com/Caravo-AI/Agent-Skills) <br>
- [Caravo CLI repository](https://github.com/Caravo-AI/Caravo-CLI) <br>
- [@caravo/cli package](https://www.npmjs.com/package/@caravo/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Caravo tool results vary by selected service and may include text, JSON, URLs for generated media, uploaded files, timestamps, execution IDs, pricing, and review metadata.] <br>

## Skill Version(s): <br>
0.4.22 (source: server release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
