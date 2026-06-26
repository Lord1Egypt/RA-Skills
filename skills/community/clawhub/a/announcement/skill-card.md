## Description: <br>
Query BingX official announcements by module type, including latest announcements, promotions, product updates, maintenance notices, listing and delisting notices, funding rate updates, and crypto scout notices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Julian-L](https://clawhub.ai/user/Julian-L) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to retrieve and summarize BingX public announcement data by module type, language, and page. It supports read-only access to announcements, promotions, maintenance notices, listings, delistings, funding rate updates, and crypto scout content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned announcements are external financial information and may be incomplete, delayed, or unsuitable as the sole basis for trading or account decisions. <br>
Mitigation: Verify important announcements against official BingX pages and other appropriate sources before acting on them. <br>
Risk: Using the skill makes read-only requests to BingX public API domains and sends a static source-identification header. <br>
Mitigation: Install and enable the skill only where outbound requests to BingX public API domains and the X-SOURCE-KEY header are acceptable. <br>


## Reference(s): <br>
- [BingX Announcement API Reference](artifact/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Julian-L/announcement) <br>
- [BingX Announcement Endpoint](https://open-api.bingx.com/openApi/content/v1/announcement?contentType=LatestAnnouncements&language=en-us&page=1) <br>
- [BingX Open API Base URL](https://open-api.bingx.com) <br>
- [BingX Open API Fallback Base URL](https://open-api.bingx.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with API request examples, TypeScript helper code, shell commands, and summarized announcement results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API requests; no authentication or signature required; sends the static X-SOURCE-KEY header.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
