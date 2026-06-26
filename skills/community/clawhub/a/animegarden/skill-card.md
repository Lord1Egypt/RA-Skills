## Description: <br>
Anime Garden helps agents search anime torrent resources through the Anime Garden API, a third-party mirror of 動漫花園, 萌番组, and ANi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjl9903](https://clawhub.ai/user/yjl9903) <br>

### License/Terms of Use: <br>
GNU Affero General Public License v3.0 <br>


## Use Case: <br>
External users and developers use this skill to find anime torrent resources, build precise Anime Garden API filters, fetch resource details, and normalize returned metadata for follow-up workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the third-party api.animes.garden service. <br>
Mitigation: Do not include personal, confidential, or sensitive information in Anime Garden queries. <br>
Risk: Returned torrent or magnet resources may have legal, trust, or content-safety implications. <br>
Mitigation: Review results for legality and trustworthiness before using or sharing any torrent or magnet link. <br>
Risk: The skill depends on a third-party API and upstream resource providers. <br>
Mitigation: Check service status and handle empty, unavailable, or error responses before relying on results. <br>


## Reference(s): <br>
- [Anime Garden HTTP API Reference](artifact/references/api.md) <br>
- [Anime Garden API](https://api.animes.garden) <br>
- [動漫花園](https://share.dmhy.org/) <br>
- [萌番组](https://bangumi.moe/) <br>
- [ClawHub skill page](https://clawhub.ai/yjl9903/animegarden) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown with endpoint guidance, curl examples, and JSON request or response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider and providerId fields so agents can fetch resource details later.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
