## Description: <br>
Bundle size and dependency bloat analyzer that scans JavaScript and TypeScript projects for oversized dependencies, duplicate packages, tree-shaking failures, and bundle configuration issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect JavaScript and TypeScript projects for bundle bloat, dependency duplication, tree-shaking problems, and bundler configuration issues. It can also generate reports, enforce bundle budgets, and install commit-time checks when licensed features are enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted or untrusted BundlePhobia license key can trigger unsafe behavior during license parsing. <br>
Mitigation: Use license keys only from trusted sources, treat them as sensitive credentials, and avoid pasting unknown tokens into configuration. <br>
Risk: Installing hooks adds persistent pre-commit behavior that can block commits in a repository. <br>
Mitigation: Review the generated lefthook.yml configuration before relying on installed hooks and remove the hooks if they are not wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/bundlephobia) <br>
- [BundlePhobia homepage](https://bundlephobia.pages.dev) <br>
- [BundlePhobia hooks documentation](https://bundlephobia.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text, with optional SARIF JSON for CI workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local scan findings, bundle health reports, hook setup guidance, and CI-oriented output depending on the invoked command.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
