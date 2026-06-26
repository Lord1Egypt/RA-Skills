## Description: <br>
Search Geizhals.at (Austria) with HTTP-only autocomplete and detail-page parsing, without browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rolandkakonyi](https://clawhub.ai/user/rolandkakonyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run quick, best-effort Geizhals.at price checks for Austrian product listings and receive candidate detail URLs, prices, shops, offer counts, and confidence metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Geizhals.at and may store fetched public page content in a local cache. <br>
Mitigation: Use a dedicated cache directory when tighter control is needed and keep result limits small. <br>
Risk: Unofficial HTML parsing can miss prices, shops, or offer counts when Geizhals.at page structure changes or rate-limits requests. <br>
Mitigation: Treat results as best-effort, review the returned confidence and source fields, and verify important prices against the linked detail page. <br>


## Reference(s): <br>
- [Geizhals.at](https://geizhals.at) <br>
- [ClawHub skill page](https://clawhub.ai/rolandkakonyi/geizhals-at) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands] <br>
**Output Format:** [Plain text table or JSON records from a command-line search script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each result includes schema_version, name, detail_url, min_price_eur, shop, offer_count, price_confidence, price_source, and error fields.] <br>

## Skill Version(s): <br>
0.1.1 (source: pyproject.toml and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
