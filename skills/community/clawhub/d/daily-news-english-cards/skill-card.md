## Description: <br>
Generates daily bilingual English learning cards with vocabulary, summaries, and AI-created comic illustrations from recent news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonruan](https://clawhub.ai/user/jasonruan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, educators, and agents use this skill to create news-based English study cards with simple bilingual summaries, vocabulary, and comic-style illustrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses paid external APIs and requires API keys. <br>
Mitigation: Use dedicated low-privilege keys with spending limits and avoid sharing keys in prompts, logs, or generated files. <br>
Risk: The generator can install Python packages at runtime. <br>
Mitigation: Run it in an isolated virtual environment and review dependencies before allowing installation. <br>
Risk: News-derived prompts and generated text are sent to external providers. <br>
Mitigation: Avoid using sensitive personal or proprietary text as input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonruan/daily-news-english-cards) <br>
- [Publisher profile](https://clawhub.ai/user/jasonruan) <br>
- [Tavily Search](https://tavily.com) <br>
- [DeepSeek API](https://platform.deepseek.com) <br>
- [OpenRouter](https://openrouter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with bash commands; runtime outputs include PNG learning cards, PNG comic images, and JSON content data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tavily, DeepSeek, and OpenRouter API keys; supports custom categories and output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
