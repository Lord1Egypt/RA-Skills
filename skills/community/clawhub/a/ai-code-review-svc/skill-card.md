## Description: <br>
Automated code review with LLM analysis, voice transcription, and Discord notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to automate pull request review by analyzing diffs with an LLM, optionally transcribing review audio, and sending Discord notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and may send repository diffs or review audio to OpenAI and Discord. <br>
Mitigation: Use it only with repositories and audio that are approved for those services, and use limited-scope API keys and webhooks. <br>
Risk: The artifact describes health checks that can auto-restart nginx, Docker, code-review-service, and whisper-api-gateway without included implementation to review. <br>
Mitigation: Review any healthcheck or service-restart script before running it and grant system privileges only when intentionally required. <br>
Risk: AI-generated review findings can be incomplete, incorrect, or misleading. <br>
Mitigation: Keep human review in the pull request workflow before merging or deploying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/ai-code-review-svc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON review results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY; DISCORD_WEBHOOK_URL is optional.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence; artifact frontmatter and changelog show 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
