## Description: <br>
Generate and deliver daily Agentic Payment news briefing for Visa Greater China VIC lead, covering Visa dynamics, China/APAC market activity, competitor protocols, and regulatory signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juncaijames](https://clawhub.ai/user/juncaijames) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up, edit, debug, or run a scheduled daily Agentic Payment briefing workflow that deduplicates recent items, writes an Obsidian Markdown report, generates a PDF, and sends it to WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is hardcoded to save business reports to a specific local Obsidian vault path and send PDFs to a fixed WeChat account on a schedule. <br>
Mitigation: Install only for the intended operator, replace path and recipient/account values before scheduling, and manually verify delivery. <br>
Risk: Scheduled delivery can send reports automatically without a dry-run or approval step. <br>
Mitigation: Add approval or dry-run controls before enabling the cron workflow. <br>
Risk: The PDF conversion script invokes shell commands with file paths. <br>
Mitigation: Harden the PDF conversion script to avoid shell interpolation before using it with untrusted paths or inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juncaijames/agentic-payment-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report text with Obsidian frontmatter, PDF generation command guidance, and delivery instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can create local Markdown and PDF files and can deliver the PDF through a configured WeChat message channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
