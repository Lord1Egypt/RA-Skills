## Description: <br>
Plan Colombia trips with region-specific routing, verified entry rules, weather-aware logistics, and practical tourist safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to design Colombia itineraries with entry, health, region, transport, budget, weather, safety, and local trip-memory context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain local trip context in ~/colombia/memory.md, which may include sensitive travel, health, mobility, child-travel, or itinerary details if the user saves them. <br>
Mitigation: Review ~/colombia/memory.md periodically and avoid storing passport, health, mobility, child-travel, or exact itinerary details that should not be retained. <br>


## Reference(s): <br>
- [Colombia Skill Homepage](https://clawic.com/skills/colombia) <br>
- [Sources - Colombia Skill](artifact/sources.md) <br>
- [Cancilleria Visa Requirements](https://www.cancilleria.gov.co/tramites_servicios/visa/requisitos) <br>
- [Migracion Colombia Check-Mig](https://apps.migracioncolombia.gov.co/pre-registro/en/) <br>
- [Colombia Travel Practical Information](https://colombia.travel/en/practical-information) <br>
- [Minsalud Yellow Fever Guidance](https://www.minsalud.gov.co/salud/publica/PET/Paginas/fiebre-amarilla.aspx) <br>
- [IDEAM Forecasts and Alerts](https://www.ideam.gov.co/pronosticos-y-alertas) <br>
- [Parques Nacionales Ecotourism](https://www.parquesnacionales.gov.co/entidad/ecoturismo/) <br>
- [INVIAS Road Information System](https://hermes2.invias.gov.co/SIV/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown travel-planning guidance with itineraries, checklists, route tradeoffs, and local memory updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local trip context in ~/colombia/memory.md when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
