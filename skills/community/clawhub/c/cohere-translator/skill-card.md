## Description: <br>
Neural machine translation supporting 23 languages using Cohere's Command A Translate model, optimized for file-based input to minimize agent context usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lykeion-dev](https://clawhub.ai/user/lykeion-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to translate short text, stdin, or files between supported languages through Cohere's hosted translation model. It is especially suited to file translation workflows where the agent should issue a command without reading the source document into its own context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translated text and selected files are sent to Cohere's external API. <br>
Mitigation: Do not use the skill for secrets, credentials, regulated data, or confidential documents unless the organization has approved that data flow. <br>
Risk: Passing an API key on the command line can expose it through shared shell history or process listings. <br>
Mitigation: Prefer setting COHERE_API_KEY in the environment rather than using the --api-key argument. <br>
Risk: The skill can incur Cohere API usage and depends on account limits or billing terms. <br>
Mitigation: Confirm Cohere account limits and production billing before using it in automated or high-volume workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lykeion-dev/cohere-translator) <br>
- [Cohere API keys](https://dashboard.cohere.com/api-keys) <br>
- [Cohere Labs CC-BY-NC license](https://cohere.com/cohere-labs-cc-by-nc-license) <br>
- [Research notes](RESEARCH.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, json, shell commands, configuration] <br>
**Output Format:** [Translated text, translated output files, or optional JSON with token counts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COHERE_API_KEY or an explicit API key argument; file mode can write translations to stdout or an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
