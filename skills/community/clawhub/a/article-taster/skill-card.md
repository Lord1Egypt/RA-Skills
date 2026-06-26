## Description: <br>
Analyzes Chinese articles for quality, genre, originality, AI-generation signals, and reading value. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, writers, and editors use Article Taster to assess article quality, classify technical articles, essays, novels, or other writing, and receive concise reading recommendations. It is especially oriented toward Chinese-language content and spoiler-aware novel analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-generation and originality scores are heuristic and may be overconfident or use wording that readers find inappropriate. <br>
Mitigation: Treat scores as advisory, review conclusions before relying on them, and replace insulting labels before broader production use. <br>
Risk: Python dependencies are declared with broad version ranges. <br>
Mitigation: Install in an isolated environment and pin dependency versions for repeatable production deployments. <br>
Risk: Future remote LLM-assisted modes could expose private drafts if enabled without clear consent. <br>
Mitigation: Use local analysis for sensitive text and enable any remote LLM assistance only after confirming where article content is sent. <br>


## Reference(s): <br>
- [Article Taster on ClawHub](https://clawhub.ai/forealmy/article-taster) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [JSON report and Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scores, article-type classification, AI-generation heuristics, originality signals, and reading advice for user-selected article content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
