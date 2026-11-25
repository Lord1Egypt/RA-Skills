## Description:

Direcciones argentinas para agentes con el callejero oficial (georef, INDEC/IGN): normalizar y geocodificar una dirección escrita a mano, geocodificación inversa lat/lon → provincia/partido/municipio, buscar calles y localidades, resolver provincias/departamentos/municipios con ids oficiales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torlettijoaquin](https://clawhub.ai/user/torlettijoaquin)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to validate, normalize, and geocode Argentine addresses, search streets and localities, and identify official provincial and municipal divisions.

### Deployment Geography for Use:

Argentina

## Known Risks and Mitigations:

Risk: Address queries are processed by a remote service and may include sensitive location or customer details.

Mitigation: Submit only addresses the user is authorized to share; remove unnecessary customer identifiers and apartment details, and review the service's privacy and retention terms before sensitive batches.

Risk: The service uses an API key and prepaid credits, so key exposure or repeated checkout attempts could create security or cost issues.

Mitigation: Protect the API key, review charges before checkout, show the returned checkout link to the user, and do not retry in a loop when credits are insufficient.

## Reference(s):

- [Direcciones AR on ClawHub](https://clawhub.ai/torlettijoaquin/skills/direcciones-ar)
- [Direcciones AR API](https://direcciones-ar-api-103907796853.us-east1.run.app)
- [OpenAPI specification](https://direcciones-ar-api-103907796853.us-east1.run.app/openapi.json)
- [Remote MCP endpoint](https://direcciones-ar-api-103907796853.us-east1.run.app/mcp)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured address, geocoding, and locality lookup results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include official names and identifiers, coordinates, candidate matches, and ambiguity information.]

## Skill Version(s):

0.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
