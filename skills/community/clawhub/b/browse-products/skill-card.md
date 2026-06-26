## Description: <br>
Semantic product search API using vector embeddings for natural language product queries with price filtering, pagination, and relevance scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gzipped](https://clawhub.ai/user/gzipped) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search and browse product catalogs from natural language requests, including optional price filters, pagination, and bulk product search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product search terms are sent to the disclosed external API at pbs-search-api-fp45p.ondigitalocean.app. <br>
Mitigation: Avoid sending confidential, personal, medical, financial, or proprietary details unless the user trusts that service's data handling. <br>


## Reference(s): <br>
- [Products Browse Skill API Reference](artifact/reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gzipped/browse-products) <br>
- [Product Search API](https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search) <br>
- [Bulk Product Search API](https://pbs-search-api-fp45p.ondigitalocean.app/api/v1/products/search/bulk) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with HTTP examples, curl commands, and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search query text is limited to 500 characters; bulk search supports up to 50 queries per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
