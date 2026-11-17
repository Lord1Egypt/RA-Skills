## Description:

APM 상품 라이브러리 검색 API provides public, unauthenticated text and image similarity search for APM product listings through lite endpoints that omit price, inventory, and sales fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apmzoom](https://clawhub.ai/user/apmzoom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce agents use this skill to search APM product listings by natural-language text or public image URL, returning similar products for recommendation, discovery, and style-matching workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search queries and image URLs are sent to the public APMZoom API.

Mitigation: Use only public, non-sensitive text queries and publicly accessible image URLs; do not submit private, signed, internal, customer-sensitive, or secret-bearing URLs.

## Reference(s):

- [APM Skills Repository Homepage](https://github.com/apmzoom-ai/apm-skills)
- [Text Search Lite Endpoint Reference](products_search_by_text_lite.md)
- [Image Search Lite Endpoint Reference](products_search_by_image_lite.md)
- [APMZoom Products Skill Page](https://clawhub.ai/apmzoom/skills/apmzoom-products)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public API access; text search accepts text, limit, and category_l1_id; image search accepts image_url, limit, category_l1_id, and embedding.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
