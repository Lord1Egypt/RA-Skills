## Description: <br>
Extracts structured product details from public e-commerce product pages, including price, currency, brand, images, identifiers, availability, ratings, variants, and seller information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect product information from publicly accessible e-commerce pages by URL, keyword, SKU, ASIN, EAN, UPC, or similar identifier. It is suited for product research, catalog enrichment, price checks, and availability checks where the user can manually access the same page in a browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encounter CAPTCHA, bot-check, login, or other access-control barriers while browsing e-commerce sites. <br>
Mitigation: Use only on pages the user can manually access, avoid sites presenting access-control challenges, and stop rather than attempting to bypass restricted content. <br>
Risk: Local memory notes may retain sensitive product URLs, browsing details, or site-specific observations. <br>
Mitigation: Review, redact, disable, or delete the local memory file when URLs or browsing details are sensitive. <br>
Risk: Extracted product data can be incomplete or stale when pages render dynamically, require login for prices, or omit full variant markup. <br>
Mitigation: Wait for page stability before extraction, test a small sample before batch runs, and verify important price, availability, and variant fields against the source page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/ecommerce-product-detail-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON product data with shell command snippets and concise execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product URLs, image URLs, identifiers, availability, ratings, variants, seller details, error messages, and local execution notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
