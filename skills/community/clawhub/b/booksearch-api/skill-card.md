## Description: <br>
Search Amazon KDP books on the BeyondBSR API, retrieve BSR history for individual books, and explore Amazon category taxonomy for supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramius88](https://clawhub.ai/user/ramius88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for KDP niche research, competitor analysis, BSR history checks, sales and royalty estimation, and Amazon category lookup through the BeyondBSR private beta API. <br>

### Deployment Geography for Use: <br>
Global; current BeyondBSR data coverage is limited to the United States and France Amazon marketplaces. <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends book research queries to the BeyondBSR private beta API using a sensitive API key. <br>
Mitigation: Store the key only in BOOKSEARCH_API_KEY, never paste or log it, and use the skill only if comfortable sending those queries to BeyondBSR. <br>
Risk: Returned market estimates are third-party data and may be unsuitable as guaranteed financial advice. <br>
Mitigation: Treat sales, royalty, revenue, and market estimates as directional research inputs and verify them before making business decisions. <br>
Risk: The documented API data coverage is currently limited to United States and France Amazon marketplaces. <br>
Mitigation: Ask for a supported marketplace when intent is ambiguous and do not invent domain IDs for unsupported countries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ramius88/booksearch-api) <br>
- [BeyondBSR book search API](https://api.beyondbsr.com/api/v1/books/search) <br>
- [BeyondBSR BSR history API](https://api.beyondbsr.com/api/v1/books/{domainId}/{asin}/bsr-history?days={1..365}) <br>
- [BeyondBSR category search API](https://api.beyondbsr.com/api/v1/categories/search?domainId={..}&q={..}&limit={1..200}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON request examples and optional cURL commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOOKSEARCH_API_KEY; BeyondBSR API responses are JSON.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
