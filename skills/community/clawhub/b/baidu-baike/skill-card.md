## Description: <br>
The Baidu Baike Component is a knowledge service tool designed to query authoritative encyclopedia explanations for various nouns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiduQianfanGroup](https://clawhub.ai/user/baiduQianfanGroup) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to look up Baidu Baike encyclopedia entries for objective nouns such as people, places, concepts, events, and other named things. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup terms are sent to Baidu when the skill queries Baidu Baike. <br>
Mitigation: Avoid searching secrets, confidential project names, private identifiers, or sensitive personal data unless disclosure to Baidu is acceptable. <br>
Risk: The skill requires a Baidu API key in the runtime environment. <br>
Mitigation: Store BAIDU_API_KEY in an approved secret store or environment configuration and avoid committing it to source files. <br>


## Reference(s): <br>
- [Baidu Baike](https://baike.baidu.com/) <br>
- [ClawHub skill page](https://clawhub.ai/baiduQianfanGroup/baidu-baike) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Text] <br>
**Output Format:** [JSON responses from Baidu Baike API calls, with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a BAIDU_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
