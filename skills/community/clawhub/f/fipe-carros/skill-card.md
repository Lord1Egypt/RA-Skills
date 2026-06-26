## Description: <br>
Consulta preços médios de carros, motos e caminhões na Tabela FIPE brasileira para compra, venda, seguro e financiamento. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People evaluating Brazilian vehicle values use this skill to list brands, models, years, and FIPE reference prices for cars, motorcycles, and trucks. It supports buying, selling, insurance, financing, and other vehicle-price checks. <br>

### Deployment Geography for Use: <br>
Brazil <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle lookup terms and selected vehicle codes are sent to the disclosed public FIPE API. <br>
Mitigation: Use the skill for vehicle make, model, and year lookups only; avoid entering private or sensitive information in search terms. <br>
Risk: Public API availability and changing FIPE data can affect result freshness or completeness. <br>
Mitigation: Verify important vehicle prices against an authoritative FIPE source before relying on them for purchases, insurance, financing, or tax decisions. <br>


## Reference(s): <br>
- [Parallelum FIPE API](https://parallelum.com.br/fipe/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the public FIPE API; search behavior in the artifact focuses on cars and limits brand scanning for performance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
