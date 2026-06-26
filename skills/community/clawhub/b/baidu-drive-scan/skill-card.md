## Description: <br>
百度网盘智能图像扫描处理工具，支持去手写、去水印、去阴影、去屏纹、清晰化、证件票据增强、黑白处理、检测矫正和扫描增强。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidunetdiskaibot](https://clawhub.ai/user/baidunetdiskaibot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route a single document or image through Baidu Drive scan processing for cleanup, enhancement, perspective correction, or document-style output. It requires a BDPAN_API_KEY and returns either the service JSON response or a local path to the processed image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to Baidu's scan service for processing. <br>
Mitigation: Use the skill only for images appropriate for that service, and avoid highly sensitive IDs, receipts, or private documents unless the data handling is acceptable. <br>
Risk: The BDPAN_API_KEY is a sensitive credential required for service access. <br>
Mitigation: Store the key in the BDPAN_API_KEY environment variable, keep it out of command arguments and shared logs, and revoke or rotate it if exposed. <br>
Risk: Processed images may remain as local files in /tmp after a successful run. <br>
Mitigation: Periodically delete generated /tmp/scan_*.png files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidunetdiskaibot/baidu-drive-scan) <br>
- [Baidu scan skill API key page](https://aiconvert.baidu.com/simple/embed/scanSkill) <br>
- [Baidu scan filter endpoint](https://pan.baidu.com/apaas/scan/filter) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON response with optional local image file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes one jpg, png, gif, bmp, or webp image up to 5MB per invocation; successful processed images may be saved under /tmp.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
