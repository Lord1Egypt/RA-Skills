## Description:

Processes document and image scans through Baidu Netdisk's scan service to remove handwriting, watermarks, shadows, screen artifacts, enhance clarity, improve ID or receipt images, convert backgrounds, correct perspective, or apply general scan enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidunetdiskaibot](https://clawhub.ai/user/baidunetdiskaibot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to route a single supported image to Baidu Netdisk scan processing and return the resulting JSON response or saved processed image path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented local-file execution can run shell commands from crafted file paths.

Mitigation: Do not process attacker-supplied local file paths until the documented sh -c path is replaced with direct stdin or file handling.

Risk: Images are uploaded to the Baidu scan endpoint for processing.

Mitigation: Use only when the operator trusts the endpoint and is comfortable sending the specific image content to that service.

Risk: Processed images may be written to /tmp and remain there after the skill returns.

Mitigation: Manually remove /tmp/scan_*.png outputs after use, especially for IDs, invoices, bank cards, contracts, or other sensitive images.

Risk: BDPAN_API_KEY is required for service access.

Mitigation: Restrict access to the key, avoid exposing it in command history or logs, and rotate it if leakage is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baidunetdiskaibot/skills/baidu-drive-scan)
- [Baidu Netdisk scan skill API key page](https://aiconvert.baidu.com/simple/embed/scanSkill)
- [Baidu Netdisk scan filter endpoint](https://pan.baidu.com/apaas/scan/filter)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command snippets and JSON command results; successful image processing may return a local /tmp/scan_*.png file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BDPAN_API_KEY and a single jpg, png, gif, bmp, or webp image of 5 MB or less.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
