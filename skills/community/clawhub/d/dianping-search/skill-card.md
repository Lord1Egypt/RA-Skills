## Description: <br>
Dianping API skill for searching restaurants and local businesses, viewing shop details, checking deals and coupons, and reading recommended dishes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FJSAND](https://clawhub.ai/user/FJSAND) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to query Dianping for Chinese-city restaurant and local-business search results, shop details, recommended dishes, prices, ratings, addresses, and deal information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Dianping session cookies in ~/.dianping/cookies.json and can print cookie values through login helper commands. <br>
Mitigation: Treat the cookie file and terminal output as sensitive account material, avoid using --export, avoid sharing logs or screenshots, and delete the cookie file when finished. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/FJSAND/dianping-search) <br>
- [Dianping website](https://www.dianping.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [JSON responses and Markdown usage guidance with shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Dianping session cookies and uses curl-based HTTP requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
