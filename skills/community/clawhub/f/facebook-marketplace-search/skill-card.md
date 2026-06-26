## Description: <br>
Search Facebook Marketplace listings near a specified location with filters for radius, price range, limit, and pickup-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexanderhe88](https://clawhub.ai/user/alexanderhe88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to query a local or configured Marketplace-compatible service for nearby listings and receive normalized result data. It is useful when an agent needs structured listing fields such as title, price, seller, image URL, and listing URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search terms and location to a local or configured Marketplace API service. <br>
Mitigation: Keep the endpoint on localhost or another service you control, and review the configured MARKETPLACE_API_BASE_URL before use. <br>
Risk: Dependency hygiene issues can make installs less reproducible. <br>
Mitigation: Use a virtual environment, remove unused Flask if it is not needed, and pin dependencies for reproducible installs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexanderhe88/facebook-marketplace-search) <br>
- [Publisher Profile](https://clawhub.ai/user/alexanderhe88) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normalized Marketplace search results with query, location, count, and listing fields; errors are returned as JSON on stderr.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
