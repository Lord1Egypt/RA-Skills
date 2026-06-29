## Description: <br>
Extracts structured product listings from public e-commerce category, search results, or keyword-search pages, including pagination and common filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to collect visible product-listing data from public shopping pages, category pages, and keyword searches. It is suited for product discovery, comparison workflows, catalog extraction, and paginated listing review where no login is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public e-commerce sites can block automated browsing or impose terms that limit scraping. <br>
Mitigation: Use only public pages the user is allowed to access, avoid login-only content, test one page first, and pace pagination as the skill recommends. <br>
Risk: DOM variation, SPA behavior, site-specific filters, and anti-bot pages can produce incomplete or inaccurate product data. <br>
Mitigation: Validate extracted rows against the visible page, prefer direct site search when generic search is unreliable, and stop or adjust strategy when counts or fields look wrong. <br>
Risk: The skill may keep a local memory file of scraping issues in the working directory. <br>
Mitigation: Review or delete the memory file when it may contain sensitive target-site notes, investigation details, or operational context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/ecommerce-listing-skill) <br>
- [Publisher profile](https://clawhub.ai/user/browseract-cli) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON product-listing and pagination objects, with Markdown guidance and bash snippets for execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Items may include URL, name, price, currency, image, rating, review count, ASIN, condition, shipping, next-page URL, and pagination method when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
