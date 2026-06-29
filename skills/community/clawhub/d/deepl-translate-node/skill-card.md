## Description: <br>
Use DeepL's neural MT API as a fallback when you are NOT confident in your own translation -- proper nouns, ambiguous phrasing, domain/legal/medical terminology, idioms, low-resource languages, or any text where a mistranslation carries real cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockbenben](https://clawhub.ai/user/rockbenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill when translation quality matters enough to call DeepL instead of relying on the agent's own translation. It is intended for uncertain, high-stakes, specialized, idiomatic, or explicitly DeepL-requested translation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for translation is sent to DeepL using the configured API host. <br>
Mitigation: Do not translate secrets, regulated data, or confidential material unless external transfer to DeepL is intended and approved. <br>
Risk: Changing DEEPL_API_HOST could send translation text and API credentials to a non-official endpoint. <br>
Mitigation: Keep DEEPL_API_HOST unset for DeepL Free or set it only to DeepL's official Pro endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rockbenben/deepl-translate-node) <br>
- [DeepL Supported Languages](https://developers.deepl.com/docs/getting-started/supported-languages) <br>
- [DeepL Languages API](https://api-free.deepl.com/v3/languages?resource=translate_text) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain translated text from the Node helper, with Markdown guidance and shell commands in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and a DEEPL_API_KEY environment variable; optional source language, target language, API host, and glossary arguments affect the translation request.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
