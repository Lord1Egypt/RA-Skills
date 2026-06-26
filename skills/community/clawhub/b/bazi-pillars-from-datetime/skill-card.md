## Description: <br>
Derives Bazi chart data from Gregorian datetime and timezone inputs, or generates grounded user-language analysis from an existing chart JSON and local knowledge files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vastaq](https://clawhub.ai/user/vastaq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to convert Gregorian datetime, timezone, and optional location inputs into reproducible Bazi four-pillar chart JSON. They can also use it to draft a concise Markdown analysis from an existing chart and the bundled knowledge material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth-location names may be resolved through geocoding or cached locally, creating privacy considerations. <br>
Mitigation: Provide longitude and latitude directly when possible, prefer local lookup, avoid unnecessary geocoding API keys, and clear or relocate city_cache.json if cached locations are sensitive. <br>
Risk: Bazi analysis can be overread as deterministic personal, health, or relationship advice. <br>
Mitigation: Keep analysis grounded in the chart JSON and knowledge file, use probabilistic language, disclose missing inputs, and avoid medical diagnoses, legal advice, or fear-based claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vastaq/bazi-pillars-from-datetime) <br>
- [Skill instructions](SKILL.md) <br>
- [Analysis prompt](prompt.md) <br>
- [Bazi knowledge base](knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Guidance] <br>
**Output Format:** [JSON for chart mode and Markdown for analysis mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chart output includes four pillars, optional luck cycles, flow data, solar terms, metadata, and structured errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
