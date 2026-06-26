## Description: <br>
Fetches and formats the latest flash-news items from Futu's public news endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loveni](https://clawhub.ai/user/loveni) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve the latest Futu flash-news updates, up to 10 items, and present each item with Beijing time and source text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts news.futunn.com to retrieve public flash-news data. <br>
Mitigation: Install and use it only when outbound access to that public endpoint is acceptable. <br>
Risk: The helper script depends on Python requests and includes an environment-specific shebang. <br>
Mitigation: Run it with an appropriate Python interpreter and ensure requests is installed in the target environment. <br>
Risk: News content can be unavailable, malformed, or limited to 10 items by the endpoint. <br>
Mitigation: Report fetch failures or empty results transparently and do not invent missing flash-news content. <br>


## Reference(s): <br>
- [Futu flash-news API endpoint](https://news.futunn.com/news-site-api/main/get-flash-list) <br>
- [Futu live news page](https://news.futunn.com/main/live) <br>
- [ClawHub skill page](https://clawhub.ai/loveni/futu-flash) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary or JSON results from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns at most 10 flash-news items; timestamps are converted to Beijing time (UTC+8).] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
