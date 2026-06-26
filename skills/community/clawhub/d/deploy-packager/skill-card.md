## Description: <br>
Executes backup optimizer packaging plans for deployment workflows, recording selected files, checksums, package names, and target shared-storage paths for CI/CD use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to run packaging plans from a backup optimizer, inspect which files would be included, and produce deployment manifest data for CI/CD pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plan-selected files can be read and included in deployment metadata without an additional content audit. <br>
Mitigation: Use only trusted packaging plans with path allowlists, upstream audit results, and secret scanning before execution. <br>
Risk: Live mode reports uploaded archive paths while the artifact behavior does not itself create real archive files. <br>
Mitigation: Require a separate verification step that expected archives exist and were copied before any deployment treats them as published. <br>
Risk: Live mode can write deployment metadata and target paths for shared CI/CD storage. <br>
Mitigation: Run only in a controlled CI/CD environment with least-privilege filesystem access and monitored shared-storage permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ink5725/deploy-packager) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Console text plus a JSON deployment_manifest.json file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run; live mode targets shared deployment storage and should be used only after plan, path, and artifact verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
