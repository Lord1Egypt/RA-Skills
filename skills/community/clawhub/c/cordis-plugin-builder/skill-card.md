## Description:

A Chinese-language guide and reference set for building Cordis plugins for DeepSeek Harness, covering core concepts, plugin forms, runtime lifecycle, capability mounting, deployment options, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifruit13](https://clawhub.ai/user/kiwifruit13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, test, package, publish, and troubleshoot Cordis plugins for DeepSeek Harness. It supports plugin development guidance, instructional Q&A, and diagnosis of plugin loading states such as PENDING and FAILED.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples or generated plugin code may introduce incorrect, unsafe, or unsuitable behavior if used without review.

Mitigation: Review generated code, run tests, and scan the plugin before deployment.

Risk: The guide includes examples involving unpinned command execution.

Mitigation: Pin exact package versions and avoid running npx -y on sensitive machines.

Risk: HTTP endpoint examples may lack authentication or session checks.

Mitigation: Add authentication and session validation before using endpoint patterns in a deployed plugin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiwifruit13/skills/cordis-plugin-builder)
- [API/interface conventions for plugin development](references/00-understanding/api-contract.md)
- [DeepSeek Harness platform overview](references/00-understanding/dsh-platform.md)
- [Plugin system mental models](references/00-understanding/mental-models.md)
- [Cordis core philosophy and DSH customization](references/00-understanding/philosophy.md)
- [Plugin forms and templates](references/00-understanding/plugin-forms.md)
- [Environment setup and installation](references/10-setup/environment.md)
- [Cordis inspect workflow](references/10-setup/inspect-workflow.md)
- [Project scaffolding and initialization](references/10-setup/scaffolding.md)
- [Agent loop lifecycle and event flow](references/20-develop/agent-lifecycle.md)
- [DSH event catalog](references/20-develop/events-catalog.md)
- [Event dispatch modes and waterfall semantics](references/20-develop/events.md)
- [Hook and tool data flow](references/20-develop/hook-tool-data-flow.md)
- [Hook and tool identity seam](references/20-develop/identity-seam.md)
- [Fiber, effects, and lifecycle](references/20-develop/lifecycle.md)
- [Capability seams and replaceable providers](references/20-develop/seams.md)
- [Client UI slots, themes, and styles](references/30-capability/client-ui.md)
- [Dynamic Cordis plugins](references/30-capability/dynamic-plugins.md)
- [Harness capability integration](references/30-capability/harness-integration.md)
- [Tool execution pipeline](references/30-capability/tool-pipeline.md)
- [Cordis plugin testing methodology](references/40-test/testing.md)
- [DSH plugin deployment overview](references/50-ship/deployment-overview.md)
- [Packaging, cordis.yml, deployment, and diagnostics](references/50-ship/packaging.md)
- [Practical pitfalls and mitigations](references/90-experience/traps.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language technical guidance for Cordis and DeepSeek Harness plugin development.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
