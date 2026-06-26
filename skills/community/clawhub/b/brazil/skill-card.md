## Description: <br>
Plan Brazil trips with region-specific routing, visa and money clarity, season-aware logistics, and concrete city-nature playbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to build Brazil itineraries that account for entry requirements, regional routing, money and payment constraints, safety posture, weather, domestic transport, and destination-specific tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may retain personal trip preferences and constraints in ~/brazil/memory.md. <br>
Mitigation: Avoid storing passport numbers, full financial details, or unnecessary medical and accessibility specifics; review or delete the memory file when trip context should no longer be retained. <br>
Risk: Travel entry, health, customs, and payment rules can change after the skill's source material was checked. <br>
Mitigation: Verify current rules with official immigration, customs, health, and payment sources before booking non-refundable travel or relying on border-sensitive guidance. <br>


## Reference(s): <br>
- [ClawHub Brazil Skill](https://clawhub.ai/ivangdavila/brazil) <br>
- [Brazil Skill Homepage](https://clawic.com/skills/brazil) <br>
- [Brazil Skill Sources Map](artifact/sources.md) <br>
- [Brazil Federal Police Immigration Portal](https://www.gov.br/pf/pt-br/assuntos/imigracao) <br>
- [Receita Federal Travelers and Customs Guidance](https://www.gov.br/receitafederal/pt-br/assuntos/aduana-e-comercio-exterior/viajantes) <br>
- [Central Bank PIX Information Hub](https://www.bcb.gov.br/estabilidadefinanceira/pix) <br>
- [Ministry of Health Yellow Fever Guidance](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/f/febre-amarela) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown travel-planning guidance with occasional shell commands for local memory setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local trip context in ~/brazil/memory.md when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
