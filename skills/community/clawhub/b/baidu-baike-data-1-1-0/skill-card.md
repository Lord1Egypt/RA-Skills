## Description: <br>
The Baidu Baike Component is a knowledge service tool that queries Baidu Baike for standardized encyclopedia explanations of nouns such as objects, people, locations, concepts, and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Baidu Baike encyclopedia entries for queried nouns, including direct title lookup and homonym disambiguation before selecting a specific entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup terms are sent to Baidu's API. <br>
Mitigation: Avoid submitting sensitive or confidential terms unless that data sharing is acceptable for the deployment. <br>
Risk: The skill requires a Baidu API key. <br>
Mitigation: Use a scoped key where possible and keep it out of shared logs and transcripts. <br>
Risk: The query script depends on the Python requests package. <br>
Mitigation: Confirm the runtime includes requests before using the skill. <br>


## Reference(s): <br>
- [Baidu Baike](https://baike.baidu.com/) <br>
- [Baidu Baike API endpoint](https://appbuilder.baidu.com/v2/baike) <br>
- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/baidu-baike-data-1-1-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON returned by the Baidu Baike query script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the Python requests package, and BAIDU_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
