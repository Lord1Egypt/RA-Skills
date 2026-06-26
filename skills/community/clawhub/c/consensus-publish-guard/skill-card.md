## Description: <br>
Persona-weighted governance for outbound publishing across blog, social, and announcement drafts that prevents unsafe public claims via hard-block checks, weighted consensus, rewrite paths, and board-native audit artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and publishing workflow owners use this skill to review outward-facing drafts before release, classify publish risk, and receive an allow, block, or rewrite decision with audit artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit artifacts may contain submitted drafts, votes, decision details, or confidential content. <br>
Mitigation: Configure the consensus state path in an access-controlled location and avoid submitting secrets or confidential account data unless those details should be stored locally for audit. <br>
Risk: Installation depends on the npm dependency chain used by the guard runtime. <br>
Mitigation: Review the dependency chain before installing or deploying the skill in a managed environment. <br>
Risk: A guard decision can reduce publishing risk but may not replace human legal, policy, or brand review for high-impact content. <br>
Mitigation: Use the decision and rewrite guidance as a pre-publication control and keep human review in the release process when content has elevated risk. <br>


## Reference(s): <br>
- [Consensus Publish Guard ClawHub listing](https://clawhub.ai/kaicianflone/consensus-publish-guard) <br>
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [consensus-guard-core repository](https://github.com/kaicianflone/consensus-guard-core) <br>
- [consensus-tools repository](https://github.com/kaicianflone/consensus-tools) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance, configuration, files] <br>
**Output Format:** [JSON decision object and local JSON audit artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decision values include ALLOW, BLOCK, or REQUIRE_REWRITE/REWRITE-style revision guidance depending on the guard path.] <br>

## Skill Version(s): <br>
1.1.17 (source: server release metadata, package.json, metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
