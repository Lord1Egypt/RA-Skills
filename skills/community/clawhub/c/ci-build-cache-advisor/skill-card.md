## Description: <br>
Optimizes CI/CD build caching across GitHub Actions, GitLab CI, CircleCI, and Jenkins by analyzing cache hit rates, recommending cache keys, and reducing build times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to review CI pipeline cache behavior, diagnose cache misses, and draft platform-specific cache key and restore-key recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested cache paths or keys could accidentally include secrets, credentials, environment files, or unnecessarily broad directories in CI caches. <br>
Mitigation: Review cache paths and keys before applying recommendations, and exclude secret-bearing files, credential stores, environment files, and broad workspace directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/ci-build-cache-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, YAML examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory recommendations and projected CI time savings; users should review proposed cache paths and keys before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
