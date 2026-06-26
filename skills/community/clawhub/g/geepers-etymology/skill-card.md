## Description: <br>
Look up word etymology, historical sound changes, language family trees, and word evolution through the dr.eamer.dev etymology and diachronic linguistics API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukeslp](https://clawhub.ai/user/lukeslp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, writers, researchers, and developers use this skill to query etymology and diachronic linguistics data for word origins, historical forms, cognates, sound changes, and language-family context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukeslp/geepers-etymology) <br>
- [dr.eamer.dev API base](https://api.dr.eamer.dev) <br>
- [Word etymology endpoint example](https://api.dr.eamer.dev/v1/etymology/word?word=serendipity) <br>
- [Word history endpoint example](https://api.dr.eamer.dev/v1/etymology/explore?word=knight&lang=en) <br>
- [Sound changes endpoint example](https://api.dr.eamer.dev/v1/etymology/sound-changes?from=proto-indo-european&to=english) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMER_API_KEY and sends lookup terms to api.dr.eamer.dev; avoid secrets and sensitive research topics in queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
