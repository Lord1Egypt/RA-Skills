## Description: <br>
Daily curiosity feed from AIgneous Million Whys - query "why" questions by topic or semantic search, delivered as quizzes, articles, or podcast scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyc11776611](https://clawhub.ai/user/lyc11776611) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to receive personalized science and culture curiosity prompts from Million Whys as quizzes, short articles, podcast scripts, or flashcards. It also helps users submit question ideas and suggestions to the Million Whys community with explicit consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a Million Whys API key in chat. <br>
Mitigation: Use a revocable key, store it through a platform secret store when available, and avoid pasting long-lived secrets into ordinary chat history. <br>
Risk: The skill asks the agent to maintain a long-term curiosity profile, including shown question IDs, interests, language preferences, and format preferences. <br>
Mitigation: Install only if persistent personalization is acceptable, and prefer deployments that let users view, reset, or disable saved memory. <br>


## Reference(s): <br>
- [Clawriosity ClawHub page](https://clawhub.ai/lyc11776611/clawriosity) <br>
- [Publisher profile](https://clawhub.ai/user/lyc11776611) <br>
- [Million Whys](https://millionwhys.com) <br>
- [Million Whys OpenClaw API](https://millionwhys.com/api/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional inline images, quiz cards, article cards, podcast scripts, flashcards, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use MILLIONWHYS_API_KEY for registered access and may ask the agent to maintain a long-term curiosity profile for personalization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
