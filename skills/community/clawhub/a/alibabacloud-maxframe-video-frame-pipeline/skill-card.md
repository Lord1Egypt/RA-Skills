## Description: <br>
Generates MaxFrame scaffolds for Alibaba Cloud OSS and ODPS video frame extraction, image labeling, and image embedding workflows using ffmpeg UDFs and AI FUNC models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to generate customer-neutral MaxFrame job code, schema guidance, and walkthroughs for OSS video manifests, frame extraction, clip/keyframe labeling, image labeling, and image embeddings on ODPS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated pipelines require OSS and ODPS credentials, including OSS access keys for AI FUNC image fetches. <br>
Mitigation: Use least-privilege or temporary credentials, keep secrets in environment variables or a secret manager, and avoid hardcoded credential literals. <br>
Risk: Example jobs can overwrite ODPS output tables when writing manifests, frame tables, or final labeling outputs. <br>
Mitigation: Verify output table names before execution and prefer versioned, partitioned, or temporary output tables when data loss would matter. <br>
Risk: Path-based video and clip workflows can process unintended OSS locations if roots or prefixes are misconfigured. <br>
Mitigation: Require declared OSS roots, reject paths outside the configured root, block traversal, and keep write-back paths under an approved output prefix. <br>
Risk: Generated code or configuration may be incorrect for a customer's MaxFrame, ODPS, model, or runtime environment. <br>
Mitigation: Review generated scaffolds before deployment, confirm model names and runtime settings, and test against non-production data first. <br>


## Reference(s): <br>
- [AI FUNC Multi-Modal Call Shapes](references/ai_func_calls.md) <br>
- [Build Video Meta Table](references/build_video_meta.md) <br>
- [Frame Extraction](references/frame_extraction.md) <br>
- [Output Contracts](references/output_contracts.md) <br>
- [Video Runtime Config](references/runtime_config.md) <br>
- [Video Safety Rules](references/safety.md) <br>
- [Alibaba Cloud OSS Python SDK v2 developer guide](https://github.com/aliyun/alibabacloud-oss-python-sdk-v2/blob/master/DEVGUIDE-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code, SQL/schema guidance, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Customer-neutral scaffolds externalize runtime settings and include row-level status, error_stage, and error_msg semantics.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
