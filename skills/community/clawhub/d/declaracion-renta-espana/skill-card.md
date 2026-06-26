## Description: <br>
Assists Spanish taxpayers with reviewing, optimizing, or preparing their 2025 IRPF income tax return using guided workflows and official national, regional, and foral reference material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joseconti](https://clawhub.ai/user/joseconti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a Spanish personal tax assistant to review AEAT or foral draft returns, identify potentially missed deductions, or prepare an orientative Renta WEB package from source documents. It is intended as a supplementary checklist and calculation aid, not as a substitute for professional tax advice. <br>

### Deployment Geography for Use: <br>
Spain <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal tax documents and may expose unnecessary identifiers or financial details if users upload complete records. <br>
Mitigation: Redact unnecessary NIF/NIE details, bank account numbers, addresses, QR or verification codes, signatures, and third-party data before upload when possible. <br>
Risk: Tax deductions and calculated results may be incomplete, approximate, or outdated for a user's specific facts. <br>
Mitigation: Verify recommendations and calculations against official AEAT or foral sources and consult a qualified tax professional before filing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joseconti/declaracion-renta-espana) <br>
- [README](artifact/README.md) <br>
- [Skill workflow](artifact/SKILL.md) <br>
- [National IRPF reference](artifact/references/nacional.md) <br>
- [Preparation mode reference](artifact/references/modo-preparacion.md) <br>
- [Self-employed taxpayer reference](artifact/references/autonomos.md) <br>
- [Special cases reference](artifact/references/casos-especiales.md) <br>
- [Regional reference index](artifact/references/regiones/indice-regiones.md) <br>
- [AEAT Renta 2025 practical manual](https://sede.agenciatributaria.gob.es/Sede/Ayuda/25Manual/100.html) <br>
- [AEAT 2025 autonomous deduction guide](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025-deducciones-autonomicas/guia-deducciones-autonomicas.html) <br>
- [BOE Order HAC/277/2026](https://www.boe.es/buscar/act.php?id=BOE-A-2026-7041) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance, summaries, checklists, tables, and orientative tax calculations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May analyze sensitive tax documents supplied by the user; outputs require verification against official AEAT or foral sources and, when appropriate, a qualified tax professional.] <br>

## Skill Version(s): <br>
2025.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
