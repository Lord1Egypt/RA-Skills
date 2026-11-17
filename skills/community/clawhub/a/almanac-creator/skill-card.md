## Description:

Daily Chinese Almanac Image Generator - Create traditional Huangli calendar images with zodiac fortune, fengshui tips, auspicious timing, and dressing advice for social media publishing (Toutiao/Douyin/Xiaohongshu).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangj85](https://clawhub.ai/user/zhangj85)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to generate daily Chinese Huangli image sets with lunar calendar details, zodiac guidance, auspicious timing, fengshui direction, wellness content, and posting copy for Toutiao, Douyin, and Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages 2 and 3 include a built-in like, comment, and follow footer that may not fit every publishing policy or audience.

Mitigation: Review generated images before posting and adjust the footer or publication workflow when the engagement prompt is inappropriate.

Risk: Optional third-party API examples may send date or query metadata to external almanac services.

Mitigation: Use local/default data generation unless external API use has been reviewed and approved for the intended environment.

Risk: Almanac, fortune, and fengshui content can be culturally contextual and should not be treated as authoritative advice.

Mitigation: Keep the traditional-culture disclaimer visible and review generated text for accuracy before publication.

## Reference(s):

- [Almanac Image Standard](references/almanac-image-standard.md)
- [lunar-python API Guide](references/lunar-python-api-guide.md)
- [Usage Examples](references/usage-examples.md)
- [Qingyunke Almanac API](https://api.qingyunke.com/api.php?key=free&appid=01&msg=%E4%BB%8A%E6%97%A5%E9%BB%84%E5%8E%86)
- [Qingyunke API Endpoint](https://api.qingyunke.com/api.php)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash and Python snippets, configuration YAML, and generated PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generator creates up to three 1080x1400 PNG pages per date, supports batch generation, writes to a local output directory, and can be configured without external API calls.]

## Skill Version(s):

3.0.5 (source: server release metadata; artifact frontmatter reports 3.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
