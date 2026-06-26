## Description: <br>
Use this skill when an agent needs to install, update, authenticate, or operate the FactuCat CLI to create Mexican CFDI 4.0 invoice drafts, assign customers or receiver data, add concepts, preview invoices, stamp them, send them through customer contact channels, or download XML/PDF artifacts on factucat.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ocruzv](https://clawhub.ai/user/ocruzv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to install, authenticate, and operate the FactuCat CLI for Mexican CFDI 4.0 invoice workflows. It supports draft creation, receiver and concept entry, preview before timbrado, stamping, delivery through customer contact channels, and XML/PDF artifact download. <br>

### Deployment Geography for Use: <br>
Mexico <br>

## Known Risks and Mitigations: <br>
Risk: Unattended commands can stamp or send real Mexican CFDI invoices without a clear approval checkpoint. <br>
Mitigation: Require `factucat invoice show` preview and explicit human approval before any `factucat invoice stamp` command or customer delivery flag. <br>
Risk: The FactuCat API key can be exposed through logs, shell history, screenshots, or shared terminals. <br>
Mitigation: Keep `FACTUCAT_API_KEY` and direct API key values out of logs and shared sessions; prefer secure secret handling for automation. <br>
Risk: The skill depends on the third-party `@factucat/cli` npm package and FactuCat service. <br>
Mitigation: Install and run it only in environments where the publisher and package are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ocruzv/factucat-cli) <br>
- [FactuCat CLI homepage](https://github.com/factucat/ai-skills/tree/main/factucat-cli) <br>
- [FactuCat production service](https://factucat.com) <br>
- [Install and authenticate](references/install-and-auth.md) <br>
- [Interactive flows](references/interactive-flows.md) <br>
- [Mexican CFDI 4.0 context](references/mexico-cfdi-context.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Unattended flows](references/unattended-flows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce XML, PDF, and JSON invoice artifacts through the FactuCat CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
