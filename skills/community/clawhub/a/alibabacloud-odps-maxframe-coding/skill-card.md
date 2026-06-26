## Description: <br>
Guides agents through MaxFrame SDK development and documentation navigation for Alibaba Cloud MaxCompute (ODPS), including API questions, data processing code, debugging, and custom DPE runtime images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to answer MaxFrame and MaxCompute questions, create or modify MaxFrame data pipelines, debug local or remote jobs, and prepare custom DPE runtime images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MaxFrame examples can include high-impact table writes, deletes, overwrite=True operations, broad cloud permissions, or UDF network allowlists. <br>
Mitigation: Review generated code before execution, use test tables first, require explicit confirmation for remote writes or permission changes, and apply least-privilege roles. <br>
Risk: The skill requires MaxCompute credentials and includes .env-based setup examples. <br>
Mitigation: Use approved secret handling, avoid exposing credential files, and verify environment variables without printing secret values. <br>
Risk: LLM-assisted data processing or generated debugging guidance can be incorrect or unsafe for production data. <br>
Mitigation: Validate code and data handling with project owners, run small controlled tests, and follow organizational review before production deployment. <br>


## Reference(s): <br>
- [MaxFrame Documentation](https://maxframe.readthedocs.io/en/latest/) <br>
- [MaxFrame Examples](https://maxframe.readthedocs.io/en/latest/examples/index.html) <br>
- [MaxCompute Endpoints](https://www.alibabacloud.com/help/zh/maxcompute/user-guide/endpoints?spm=a2c63.p38356.help-menu-search-27797.d_0) <br>
- [MaxFrame Installation Guide](references/installation.md) <br>
- [MaxFrame Common Workflow](references/common-workflow.md) <br>
- [MaxFrame Remote Debug Guide](references/remote-debug-guide.md) <br>
- [MaxFrame Local Debug Mode Guide](references/local-debug-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MaxFrame API references, example programs, debugging steps, runtime image guidance, and source citations requested by the skill.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
