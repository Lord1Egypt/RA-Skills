## Description:

Compare two texts and get a unified diff with a similarity score (0-1), line-level additions/deletions, and individual change records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Diffgate to compare LLM outputs, documents, configuration files, and skill versions for line-level changes and similarity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Uvicorn service could be exposed beyond the host if bound publicly.

Mitigation: Keep it bound to localhost unless authentication, rate limits, and resource controls are added.

Risk: Compared text may contain secrets or sensitive content handled by the local service process.

Mitigation: Avoid submitting secrets unless the runtime environment is approved to process that text.

Risk: Installing current PyPI dependencies can introduce dependency drift.

Mitigation: Install in an environment where resolving current packages is acceptable and pin dependencies for controlled deployments.

## Reference(s):

- [Diffgate ClawHub listing](https://clawhub.ai/mirni/skills/diffgate)
- [mirni publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [text, analysis]

**Output Format:** [JSON response with similarity, addition and deletion counts, and per-line change records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stateless local FastAPI endpoint; request text fields are limited to 500,000 characters each.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
