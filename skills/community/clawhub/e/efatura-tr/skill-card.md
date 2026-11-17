## Description:

A Turkish e-invoicing assistant that provides e-fatura and e-arşiv guidance, taxpayer lookup support, GİB regulatory references, integrator comparisons, and obligation timing for SMEs and accountants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayhanagirgol](https://clawhub.ai/user/ayhanagirgol)

### License/Terms of Use:

MIT-0

## Use Case:

External businesses, accountants, and developers use this skill to answer Turkish e-fatura, e-arşiv, e-irsaliye, GİB portal, and electronic invoicing obligation questions. It can also propose shell commands for checking e-fatura taxpayer status by VKN, Turkish ID number, or company name.

### Deployment Geography for Use:

Turkey

## Known Risks and Mitigations:

Risk: The skill may run a local Bash lookup script that uses curl, unzip, and grep and caches a public GİB taxpayer CSV in the user's home cache directory.

Mitigation: Review the script before execution, ensure network access to GİB endpoints is acceptable, and remove or manage the local cache according to the user's data-handling expectations.

Risk: Taxpayer lookup results and regulatory thresholds may be advisory or become outdated as GİB and Hazine ve Maliye Bakanlığı guidance changes.

Mitigation: Confirm material decisions against official GİB sources and current mevzuat before relying on the output.

Risk: The security guidance notes a bundled script function-order bug that can prevent normal lookup execution until fixed.

Mitigation: Test the script in a controlled shell before operational use and fix execution ordering before depending on automated lookups.

Risk: The skill includes Finhouse promotional mentions.

Mitigation: Review responses for commercial bias and prefer official GİB sources for compliance conclusions.

## Reference(s):

- [E-Fatura ve E-Arşiv Rehberi](references/efatura_rehber.md)
- [GİB e-Belge Portal](https://ebelge.gib.gov.tr)
- [GİB e-Belge Mevzuat](https://ebelge.gib.gov.tr/mevzuat.html)
- [GİB E-Fatura Portal](https://efatura.gib.gov.tr)
- [GİB E-Fatura Taxpayer List](https://efatura.gib.gov.tr/listeleri/efatura_mf.zip)
- [ClawHub Skill Page](https://clawhub.ai/ayhanagirgol/skills/efatura-tr)
- [Publisher Profile](https://clawhub.ai/user/ayhanagirgol)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite Turkish GİB sources and may suggest a bundled Bash lookup script.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
