## Description: <br>
Fetches current Baidu hot-search topics from Baidu's public ranking endpoint and prints a ranked terminal list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piaomiao123](https://clawhub.ai/user/piaomiao123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check Baidu trending search topics during market, news, or content research without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Baidu to retrieve public trending-search data. <br>
Mitigation: Install only in environments where outbound requests to top.baidu.com are acceptable. <br>
Risk: The documentation describes options such as output files and history that the script does not implement. <br>
Mitigation: Rely on the current script behavior for ranked terminal output, and review documentation before advertising additional features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piaomiao123/baidu-hot) <br>
- [Baidu hot-search API endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with ranked hot-search topics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and outbound network access to top.baidu.com; no API key is required.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
