## Description:

Generates bilingual English learning cards with vocabulary, summaries, and AI-created comic illustrations from recent news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonruan](https://clawhub.ai/user/jasonruan)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and developers use this skill to generate news-based English study cards with simple bilingual summaries, vocabulary, and illustrations. It is suited for creating daily English-learning materials from selected news categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install mutable Python dependencies at runtime.

Mitigation: Preinstall pinned dependencies in an isolated environment before running the script.

Risk: The script can load API keys from .env files in nearby directories.

Mitigation: Run it from a clean workspace and provide only trusted API keys through the intended environment.

Risk: Model-supplied image URLs are fetched during generation.

Mitigation: Run with network controls appropriate for untrusted remote media and review generated files before sharing.

Risk: Generated cards include fixed branding not disclosed in the public instructions.

Mitigation: Review outputs and modify the code or branding before use in external materials.

## Reference(s):

- [Daily News English Cards on ClawHub](https://clawhub.ai/jasonruan/skills/daily-news-english-cards)
- [Tavily Search API](https://tavily.com)
- [DeepSeek Platform](https://platform.deepseek.com)
- [OpenRouter](https://openrouter.ai)

## Skill Output:

**Output Type(s):** [Image files, JSON, Files]

**Output Format:** [PNG learning-card images, PNG comic illustrations, and structured JSON content files written to an output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tavily, DeepSeek, and OpenRouter API keys; categories and output directory can be customized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
