## Description: <br>
Build a reusable brand knowledge package from uploaded brand documents and/or a filled intake form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, developers, and brand operators use this skill to turn company materials or intake forms into a reusable brand single source of truth for downstream agents, RAG, FAQ, sales support, content generation, and AI search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected brand documents and intake content are sent to the configured OpenAI-compatible provider. <br>
Mitigation: Use only an approved provider, review OPENAI_BASE_URL before use, and exclude confidential, regulated, customer-sensitive, or secret-containing documents unless that provider is approved for them. <br>
Risk: The output directory may include a local source_bundle.md copy of submitted materials. <br>
Mitigation: Store generated outputs in an approved location, review files before sharing, and remove source bundles when they are no longer needed. <br>
Risk: Generated brand knowledge may contain missing fields, assumptions, or unverified claims. <br>
Mitigation: Review the analysis report, resolve follow-up questions, and confirm all marked fields before publishing or loading outputs into production systems. <br>
Risk: The skill requires OPENAI_API_KEY for the configured LLM provider. <br>
Mitigation: Provide credentials through environment management and avoid committing API keys or local .env files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ljseeking/brand-knowledge-base) <br>
- [Publisher profile](https://clawhub.ai/user/ljseeking) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Manifest](artifact/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, YAML, Markdown, llms.txt, FAQ, glossary, standard messaging, analysis report, and intake templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Missing or weakly supported brand fields are marked for confirmation and paired with follow-up questions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
