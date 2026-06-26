## Description: <br>
Fetches Amazon product data such as title, price, currency, rating, review count, availability, main image, and product URL from a public Amazon URL or ASIN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mysmth2003](https://clawhub.ai/user/mysmth2003) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to look up individual public Amazon product pages and return structured product details without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Amazon product pages and may be blocked by CAPTCHA, HTTP 503 responses, or Amazon anti-scraping controls. <br>
Mitigation: Use it for individual public product lookups, retry later when blocked, and avoid bulk scraping workflows. <br>
Risk: The optional marketplace setting can redirect requests away from the default Amazon host if set to a non-Amazon or untrusted domain. <br>
Mitigation: Keep AMAZON_MARKETPLACE or --marketplace restricted to trusted Amazon marketplace domains. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text table or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns product fields including asin, title, price, currency, rating, reviews, availability, image_url, and product_url.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
