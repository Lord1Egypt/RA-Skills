## Description: <br>
Türkiye e-fatura ve e-arşiv bilgi asistanı for e-fatura mükellefiyeti checks, GİB mevzuatı, entegratör comparisons, zorunluluk timelines, and Turkish electronic invoicing questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayhanagirgol](https://clawhub.ai/user/ayhanagirgol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, accountants, and small businesses use this skill to understand Turkish e-fatura and e-arşiv obligations, compare GİB portal and integrator options, and run local checks for e-fatura taxpayer status by VKN, TCKN, or company name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup commands can process VKN, TCKN, or company names and contact GİB services. <br>
Mitigation: Run lookups only when authorized to process the submitted identifier or company name, and verify results against official GİB sources. <br>
Risk: The lookup script can download a public GİB taxpayer list and create a local cache under the user's home directory. <br>
Mitigation: Review the shell command before execution and clear the local cache if retaining downloaded taxpayer data is not appropriate. <br>
Risk: Turkish e-invoicing thresholds and obligations change over time. <br>
Mitigation: Confirm tax obligations against current GİB and Hazine ve Maliye Bakanlığı sources before making compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayhanagirgol/efatura-tr) <br>
- [E-Fatura ve E-Arşiv Rehberi](references/efatura_rehber.md) <br>
- [GİB e-Belge Portal](https://ebelge.gib.gov.tr) <br>
- [GİB E-Fatura Portal](https://efatura.gib.gov.tr) <br>
- [Finhouse](https://finhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest running a local shell script that contacts GİB and caches a downloaded taxpayer list under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
