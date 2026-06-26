## Description: <br>
The Baidu Baike Component is a knowledge service tool that queries Baidu Baike for authoritative encyclopedia explanations of nouns such as objects, people, locations, concepts, and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ide-rea](https://clawhub.ai/user/ide-rea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to look up Baidu Baike entries by title or entry ID, including ambiguous terms that need homonym resolution before returning the selected encyclopedia result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends lookup terms to Baidu and uses a Baidu API key. <br>
Mitigation: Use a dedicated, revocable API key, monitor quota or billing, and avoid querying confidential internal terms. <br>
Risk: The Python script depends on the requests package being available in the runtime environment. <br>
Mitigation: Confirm the runtime has the required Python dependency before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ide-rea/baidu-baike-data) <br>
- [Publisher profile](https://clawhub.ai/user/ide-rea) <br>
- [Baidu Baike](https://baike.baidu.com/) <br>
- [Baidu Baike API endpoint](https://appbuilder.baidu.com/v2/baike) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON returned by a Python command-line script, with agent-facing guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; sends lookup terms to Baidu.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
