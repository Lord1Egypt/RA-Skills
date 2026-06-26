## Description: <br>
Publish and manage Facebook Page content through a preconfigured MyBrandMetrics API connection, including Page connection, account and Page listing, post and media publishing, feed and comment management, and Page or post insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbus](https://clawhub.ai/user/clawbus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, social media operators, and developers use this skill to publish Facebook Page posts, photos, and videos, read feeds and comments, moderate comments, and fetch insights through MyBrandMetrics. It is intended for workflows where the agent is authorized to use the user's MyBrandMetrics credentials and manage real Facebook Page content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real Facebook Page changes when used with the user's MyBrandMetrics credentials. <br>
Mitigation: Install only if the publisher and MyBrandMetrics connection are trusted, use least-privilege credentials, and verify the target Page, content, post IDs, comment IDs, and intended visibility before publishing or moderating. <br>
Risk: Access tokens, API keys, Page IDs, account IDs, and connection IDs are sensitive operational data. <br>
Mitigation: Provide credentials through runtime arguments, environment variables, or a local config file, avoid committing them, and avoid echoing secrets in logs or terminal output. <br>
Risk: Overriding the API base URL can send credentials and Page operations to an unintended service. <br>
Mitigation: Use the default MyBrandMetrics API host unless a trusted alternate environment is explicitly required. <br>


## Reference(s): <br>
- [Facebook Pages Skill Page](https://clawhub.ai/clawbus/clawbus-facebook-pages) <br>
- [Configuration](references/configuration.md) <br>
- [Examples](references/examples.md) <br>
- [MyBrandMetrics](https://mybrandmetrics.com/) <br>
- [Clawbus](https://www.clawbus.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and structured JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token or API-key authentication and returns the real MyBrandMetrics API response for script calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
