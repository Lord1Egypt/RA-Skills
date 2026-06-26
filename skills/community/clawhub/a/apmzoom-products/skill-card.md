## Description: <br>
Provides public APM product-library search API guidance for natural-language text search and image similarity search, returning lightweight product results without price, stock, rating, or sales fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apmzoom](https://clawhub.ai/user/apmzoom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to search an APM product library by natural-language description or public image URL, then return candidate products for recommendation, discovery, or style-matching workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image search sends the submitted image URL to worker.apmzoom.ai. <br>
Mitigation: Use public, non-sensitive image URLs and avoid signed CDN links, intranet URLs, private storage links, or URLs that reveal account, customer, or proprietary inventory information. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/apmzoom-ai/apm-skills) <br>
- [ClawHub skill page](https://clawhub.ai/apmzoom/apmzoom-products) <br>
- [Text search lite API documentation](products_search_by_text_lite.md) <br>
- [Image search lite API documentation](products_search_by_image_lite.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and JSON request/response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls the public worker.apmzoom.ai API; image search sends the provided image URL to that service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
