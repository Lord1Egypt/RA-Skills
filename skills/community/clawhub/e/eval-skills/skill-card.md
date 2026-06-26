## Description: <br>
Eval Skills is a framework-agnostic toolkit for discovering, scaffolding, selecting, evaluating, and reporting on AI agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isLinXu](https://clawhub.ai/user/isLinXu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate individual AI skills, compare candidates on shared benchmarks, enforce CI/CD quality gates, and generate human-readable evaluation reports before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use can execute local or remote skill code and custom scorer code with under-scoped trust boundaries. <br>
Mitigation: Run evaluations in an isolated workspace, prefer Docker sandboxing with controlled network egress, and review skill entrypoints and custom scorer paths before execution. <br>
Risk: HTTP, MCP, or LLM endpoints used during evaluation may receive benchmark data or other local inputs. <br>
Mitigation: Avoid exposing broad API keys or secrets and treat configured endpoints as external data recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/isLinXu/eval-skills) <br>
- [README](artifact/README.md) <br>
- [CI/CD integration guide](artifact/docs/guides/ci-cd-integration.md) <br>
- [Quick start guide](artifact/docs/guides/quickstart.md) <br>
- [Custom benchmark guide](artifact/docs/guides/custom-benchmark.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and configuration snippets; evaluation reports can be JSON, Markdown, HTML, CSV, or diff output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports benchmark selection, evaluation thresholds, report output directories, and optional persistent result storage.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter/package metadata says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
