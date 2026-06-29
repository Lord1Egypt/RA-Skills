## Description: <br>
Automates bookkeeping workflows for accounting agencies, including invoice OCR, accounting entries, financial reports, tax calculations, Golden Tax Phase IV filing support, risk checks, and dashboard output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and accounting teams use this skill to run or guide an automated bookkeeping cycle for small-business clients, from receipt capture through vouchers, reports, tax estimates, filing-package generation, and review dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive invoices, company records, tax identifiers, and filing data. <br>
Mitigation: Use trusted environments, protect generated files and credentials, and limit access to financial data handled by the workflow. <br>
Risk: Live OCR and tax-provider integrations may transmit financial data to external services. <br>
Mitigation: Keep default or simulated modes until provider credentials, destination URLs, and data-sharing approvals are verified. <br>
Risk: Automated accounting, tax, and filing outputs may be incomplete or incorrect for a real taxpayer. <br>
Mitigation: Review calculations, vouchers, reports, risk findings, and filing payloads with qualified accounting or tax personnel before submission. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/bettermen/agent-accounting) <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/agent-accounting) <br>
- [Baidu OCR finance documentation](https://ai.baidu.com/tech/ocr/finance) <br>
- [Baidu OCR API reference](https://ai.baidu.com/ai-doc/OCR/Zk3h7xz52) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; invoked workflows can produce text summaries, XML filing payloads, and HTML dashboards.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and optional environment variables for Baidu OCR and tax-provider integrations.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
