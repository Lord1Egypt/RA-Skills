## Description:

AirShelf helps agents search, compare, and initiate checkout for products from verified merchants using structured product data and Decision Packs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evoleinik](https://clawhub.ai/user/evoleinik)

### License/Terms of Use:


## Use Case:

External users and commerce agents use this skill to find products, compare structured recommendations, check details such as pricing and allergens, and prepare merchant checkout links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product searches may send sensitive health, family, or preference details to AirShelf.

Mitigation: Ask before sending sensitive queries and avoid including unnecessary personal details.

Risk: Raw shell substitution in example curl URLs can mishandle spaces, punctuation, or special characters in user search text.

Mitigation: URL-encode query parameters or use a structured HTTP client when constructing requests.

Risk: Checkout requests and optional email fields can initiate purchase flows or share contact information.

Mitigation: Ask before checkout and before sending an optional email address.

## Reference(s):

- [AirShelf Skill on ClawHub](https://clawhub.ai/evoleinik/skills/airshelf)
- [AirShelf API Base](https://dashboard.airshelf.ai)
- [AirShelf Merchant Directory API](https://dashboard.airshelf.ai/api/directory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; checkout redirects users to merchant sites for payment.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
