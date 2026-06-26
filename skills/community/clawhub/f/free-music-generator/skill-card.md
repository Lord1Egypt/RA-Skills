## Description: <br>
Tunee AI music creation skill for lyric writing, vocal song generation, instrumental and BGM production, model selection, and Tunee credit checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuneeai](https://clawhub.ai/user/tuneeai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Music creators, enthusiasts, and agents use this skill to draft lyrics, construct music prompts, select Tunee models, and generate vocal or instrumental tracks through Tunee. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports an undisclosed non-Tunee callback URL in generation requests. <br>
Mitigation: Review or remove the callback URL in scripts/generate.py before use, confirm each generation before it runs, and use a revocable Tunee API key with limited account exposure. <br>
Risk: Prompts, titles, lyrics, and API credentials are sent to Tunee for music generation and account operations. <br>
Mitigation: Install only when Tunee processing is acceptable for the intended content, avoid sensitive lyrics or prompts, and keep the Tunee API key revocable. <br>


## Reference(s): <br>
- [Tunee AI](https://www.tunee.ai) <br>
- [Tunee Documentation](https://www.tunee.ai/docs) <br>
- [Tunee AI Publisher Profile](https://clawhub.ai/user/tuneeai) <br>
- [Free Music Generator on ClawHub](https://clawhub.ai/tuneeai/free-music-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and parsed Tunee result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tunee API key through TUNEE_API_KEY or an explicit --api-key argument.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
