## Description: <br>
Use when managing a self-hosted Dify instance, checking feature feasibility, or orchestrating apps, prompts, datasets, and knowledge-base operations via the dify-manager MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arn0ld87](https://clawhub.ai/user/arn0ld87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer self-hosted Dify instances, including app, prompt, dataset, upload, retrieval, health-check, and feature-feasibility workflows. It emphasizes preflight checks, explicit confirmation for destructive actions, and post-change verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and delete operations can modify apps, datasets, prompts, uploads, and knowledge-base state in a self-hosted Dify instance. <br>
Mitigation: Confirm the target API surface, app or dataset IDs, file paths, and explicit user approval before write or delete operations; run read-back or smoke checks afterward. <br>
Risk: Dify management, runtime, and console credentials could be exposed if copied into prompts, logs, examples, or generated content. <br>
Mitigation: Keep Dify secrets in local configuration or a secret store and avoid embedding API keys or passwords in prompts, logs, examples, or skill content. <br>
Risk: Version-sensitive Dify features such as plugins, triggers, OAuth behavior, and workflow behavior may differ across self-hosted deployments. <br>
Mitigation: Verify official Dify documentation, release notes, and the target instance version before advising or executing feature-dependent changes. <br>


## Reference(s): <br>
- [Dify Docs](https://docs.dify.ai/) <br>
- [Dify GitHub Repository](https://github.com/langgenius/dify) <br>
- [Dify Releases](https://github.com/langgenius/dify/releases) <br>
- [Dify Official Plugins](https://github.com/langgenius/dify-official-plugins) <br>
- [App Types](references/app_types.md) <br>
- [App Type Decision Guide](references/app_type_decision_guide.md) <br>
- [Knowledge Retrieval](references/knowledge_retrieval.md) <br>
- [Plugins And Providers](references/plugins_and_providers.md) <br>
- [Plugin Integration Patterns](references/plugin_integration_patterns.md) <br>
- [Self-Hosted Operations](references/self_hosted_operations.md) <br>
- [Version Notes](references/version_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and structured operational steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool-call sequences, Dify configuration examples, preflight checks, and smoke-check recommendations.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
