## Description:

Archive2Figure (a2f) converts PDF archives into digital character figures by extracting character features, generating images, and retrieving results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wadipapa](https://clawhub.ai/user/wadipapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to call the Wuji A2F API for extracting character details from PDFs, composing prompts, starting image-generation jobs, and polling for generated character images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected PDFs, extracted character details, and generation prompts to the Wuji A2F API.

Mitigation: Avoid confidential, regulated, copyrighted, or personal documents unless the provider's retention and privacy terms are understood.

Risk: A custom api_base value could redirect uploads, prompts, or API credentials to an untrusted service.

Mitigation: Use the default trusted API endpoint and do not accept api_base values from untrusted sources.

Risk: Dependency installation and examples may run in the user's local Python environment.

Mitigation: Install dependencies in an isolated environment and skip the unnecessary asyncio package.

## Reference(s):

- [ClawHub a2f Skill Page](https://clawhub.ai/wadipapa/skills/a2f)
- [wadipapa Publisher Profile](https://clawhub.ai/user/wadipapa)
- [Wuji A2F API Base](https://wuji.cyphy.com/api)
- [Examples Guide](artifact/README.md)
- [Complete A2F Client Example](artifact/a2f_example.py)
- [Quick Start Example](artifact/quick_start.py)
- [Batch Generation Example](artifact/batch_generation.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, configuration values, and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe PDF upload, prompt construction, asynchronous job polling, and result URL handling.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
