## Description:

Search and get details for POI (points of interest) using Baidu Maps API. Use for searching places, restaurants, hotels, attractions, and retrieving detailed POI information by UID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archimondecy](https://clawhub.ai/user/archimondecy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Baidu Maps points of interest by name, address, category, or natural-language attributes, then retrieve POI details such as location, address, ratings, prices, hours, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can expose the Baidu Maps API key and private search terms in request logs.

Mitigation: Use a restricted Baidu Maps API key, prefer BAIDU_AK over passing keys in JSON, and redact or remove stderr request logging in shared terminals, CI, or agent environments.

Risk: Location searches may include sensitive place queries.

Mitigation: Avoid sensitive location queries and review query content before sending requests to the Baidu Maps API.

## Reference(s):

- [Baidu Maps POI Region Search API](https://api.map.baidu.com/api_place_pro/v1/region)
- [Baidu Maps Multidimensional Place Search Documentation](https://api.map.baidu.com/place/v3/multidimensional)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON API results with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Baidu Maps API key supplied through BAIDU_AK or the request JSON.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
