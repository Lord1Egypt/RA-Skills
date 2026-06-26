## Description: <br>
Build, modify, and debug feapder 1.9.2 spiders and projects with the framework's native patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fqxue](https://clawhub.ai/user/fqxue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, modify, and debug feapder 1.9.2 crawlers, including AirSpider, Spider, TaskSpider, BatchSpider, request parsing, persistence, render settings, and project scaffolding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vendored upstream reference files include unsafe Redis parsing examples. <br>
Mitigation: Treat Redis task and cache data as untrusted, validate or sanitize inputs before use, and isolate debug Redis keys from production systems. <br>
Risk: Examples may show credential-handling patterns that could expose real cookies, passwords, or database credentials if copied directly. <br>
Mitigation: Use placeholder secrets in examples, keep real credentials in environment-specific configuration or secret storage, and avoid pasting production credentials into generated code or prompts. <br>
Risk: Generated crawler debugging or persistence guidance can write test data to shared Redis or database resources. <br>
Mitigation: Run debugging workflows against isolated development resources and review database writes before enabling production pipelines. <br>


## Reference(s): <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Spider Types and Scaffolding](artifact/references/spider-types-and-scaffolding.md) <br>
- [Code Patterns](artifact/references/code-patterns.md) <br>
- [Settings, Debugging, and Source Anchors](artifact/references/settings-debugging-and-sources.md) <br>
- [feapder 1.9.2 README](artifact/references/vendor/feapder-1.9.2/README.md) <br>
- [feapder CLI documentation](artifact/references/vendor/feapder-1.9.2/docs/command/cmdline.md) <br>
- [AirSpider usage](artifact/references/vendor/feapder-1.9.2/docs/usage/AirSpider.md) <br>
- [Spider usage](artifact/references/vendor/feapder-1.9.2/docs/usage/Spider.md) <br>
- [TaskSpider usage](artifact/references/vendor/feapder-1.9.2/docs/usage/TaskSpider.md) <br>
- [BatchSpider usage](artifact/references/vendor/feapder-1.9.2/docs/usage/BatchSpider.md) <br>
- [ClawHub skill page](https://clawhub.ai/fqxue/feapder) <br>
- [Publisher profile](https://clawhub.ai/user/fqxue) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with code blocks and inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include feapder spider files, project scaffolding instructions, settings guidance, and debugging steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
