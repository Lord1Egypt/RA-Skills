## Description: <br>
Publish, create, and update Confluence pages from HTML content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeincx](https://clawhub.ai/user/aeincx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to publish HTML content to Atlassian Confluence, creating new pages or updating existing pages in a target space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A publish request can update an existing Confluence page when the title already exists in the target space. <br>
Mitigation: Verify the target space key and page title before publishing, and use a test or draft space when validating new workflows. <br>
Risk: The skill uses Atlassian credentials to create or update Confluence content. <br>
Mitigation: Use a least-privilege Atlassian API token scoped only to the spaces and actions required. <br>
Risk: Unpinned dependency ranges can make installs less reproducible over time. <br>
Mitigation: Use pinned dependency versions or a reviewed lock file for production deployments. <br>


## Reference(s): <br>
- [Confluence Publish release page](https://clawhub.ai/aeincx/confluence-publish) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text] <br>
**Output Format:** [JSON response containing status, operation, page metadata, page URL, or connection identity.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a new Confluence page or update an existing page with the same title in the target space.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
