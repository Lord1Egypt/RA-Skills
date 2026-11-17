## Description:

1688 Scraper helps an agent collect product details, images, SKU data, shop details, sales data, attributes, and reviews from 1688 product detail pages and save them as local assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howerlin0329](https://clawhub.ai/user/howerlin0329)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to archive or analyze 1688 product listings by collecting product media and structured detail data from a specific product URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says URL validation is too loose and could direct the browser to non-1688 or internal hosts.

Mitigation: Review before installing and use only intended 1688 product URLs, preferably exact https://detail.1688.com/offer/<id>.html links.

Risk: The security guidance notes that the skill creates a local image folder and JSON file that may consume disk space or be picked up by desktop backup or sync tools.

Mitigation: Choose an appropriate save location, monitor generated file size, and avoid collecting sensitive listings into synced desktop folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howerlin0329/skills/1688-scraper)
- [README.md](artifact/README.md)
- [USAGE.md](artifact/USAGE.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files, JSON]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; generated local image files and a JSON data package.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local image folder and JSON file for each product ID; downloaded media can consume disk space.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
