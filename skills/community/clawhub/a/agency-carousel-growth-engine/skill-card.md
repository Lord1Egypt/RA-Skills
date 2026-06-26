## Description: <br>
Expert AI agent specializing in carousel growth engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouqkt](https://clawhub.ai/user/zhouqkt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and growth teams use this agent to research a website, generate six-slide TikTok and Instagram carousel content, publish it through Upload-Post, and adapt later posts from analytics feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to publish publicly to TikTok and Instagram and schedule future runs without asking first. <br>
Mitigation: Use draft or preview mode, require manual approval for every post and schedule, and test with non-production social accounts before enabling public publishing. <br>
Risk: The workflow requires credentials that can access publishing and analytics services. <br>
Mitigation: Store credentials in environment secrets, limit account scope, rotate tokens regularly, and revoke credentials when the skill is no longer in use. <br>
Risk: The workflow processes website content and analytics data. <br>
Mitigation: Run it only on websites, accounts, and analytics data the operator is authorized to process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouqkt/agency-carousel-growth-engine) <br>
- [Upload-Post API documentation](https://docs.upload-post.com) <br>
- [Google AI Studio API key setup](https://aistudio.google.com/app/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, image files] <br>
**Output Format:** [Markdown guidance plus generated JPG carousel slides, JSON analysis and learning files, captions, shell commands, and API requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment-provided Gemini and Upload-Post credentials; generated posts may be public if the publishing workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
