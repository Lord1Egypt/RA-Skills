## Description: <br>
Query Czech ARES business registry by ICO or name with human/JSON/raw outputs, retries, and legal-form decoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PGhostek](https://clawhub.ai/user/PGhostek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to look up Czech business entities by ICO, name, city, or CZ-NACE filters and return human-readable or JSON registry results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business lookup terms such as ICO, name, city, or NACE filters are sent to the Czech ARES service. <br>
Mitigation: Use the skill only with lookup terms that are acceptable to disclose to ARES. <br>
Risk: A custom --base URL can redirect registry queries to a non-default service. <br>
Mitigation: Use the default ARES endpoint unless the custom endpoint is intentionally trusted. <br>
Risk: The skill creates a small local cache for legal-form names. <br>
Mitigation: Account for the .cache/pravni_forma.json file in local data handling and clear it when needed. <br>
Risk: City filtering is best-effort and ARES matching may return records outside the expected municipality. <br>
Mitigation: Review returned entity details before using results for business decisions. <br>


## Reference(s): <br>
- [ARES links](references/ares-links.md) <br>
- [ARES Swagger UI](https://ares.gov.cz/swagger-ui/#/) <br>
- [ARES technical documentation catalog of public services](https://mf.gov.cz/assets/attachments/2024-02-16_ARES-Technical-documentation-Catalog-of-public-services_v02.pdf) <br>
- [CZ-NACE classification](https://www.czso.cz/csu/czso/klasifikace_ekonomickych_cinnosti_cz_nace) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands] <br>
**Output Format:** [Human-readable text, normalized JSON, raw JSON payloads, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ARES network calls, retry/backoff behavior, and a small 24-hour local legal-form cache.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
