## Description: <br>
腾讯云对象存储（COS）上传工具。将本地文件上传至腾讯云 COS，生成下载链接和图片预览。适用于备份文件、生成公开分享链接、存储静态资源。跨平台支持（macOS/Linux/Windows），支持 CLI 和 Python 两种方式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realorange1994](https://clawhub.ai/user/realorange1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Tencent Cloud Object Storage uploads, choose CLI or Python upload paths across macOS, Linux, and Windows, and produce download or preview links for uploaded files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generic request to share or back up content could cause an unintended Tencent COS upload. <br>
Mitigation: Require explicit confirmation of Tencent COS use, local file or folder, bucket, region, object key, and sharing behavior before running upload commands. <br>
Risk: Tencent COS credentials or public bucket settings could expose sensitive files. <br>
Mitigation: Use least-privileged COS credentials, avoid public-read buckets for sensitive files, and prefer short-lived presigned links for private content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realorange1994/cloud-upload-tencent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include upload result summaries, COS paths, bucket and region details, and download or preview link formats.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
