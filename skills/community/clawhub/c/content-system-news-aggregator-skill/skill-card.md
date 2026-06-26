## Description: <br>
Comprehensive news aggregator that fetches, filters, and analyzes real-time content from 28 sources including Hacker News, GitHub Trending, Hugging Face Papers, AI newsletters, WallStreetCN, Weibo, essays, and podcasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch current news, run preconfigured daily briefing profiles, and produce Simplified Chinese Markdown reports with links, timing, heat signals, summaries, and deeper analysis from the fetched JSON data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags anti-bot scraping behavior and unsafe network defaults. <br>
Mitigation: Install and run in an isolated environment; review or disable Playwright and deep-fetch paths before use. <br>
Risk: Automated scraping reaches many third-party sites and can run concurrent fetches. <br>
Mitigation: Limit sources and item counts, respect site policies, and review fetched URLs before enabling broad or repeated scans. <br>
Risk: Saved reports can persist local records of user interests and fetched content. <br>
Mitigation: Use --no-save when persistence is not needed, choose a controlled output directory, and periodically remove reports/YYYY-MM-DD/ files. <br>
Risk: Artifact planning material references cron/background scheduling for unattended recurring runs. <br>
Mitigation: Do not approve cron or background scheduling unless recurring unattended scans are intended, and verify installed schedules afterward. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abigale-cyber/content-system-news-aggregator-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [templates.md](artifact/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Simplified Chinese Markdown reports, JSON source data, and shell commands for local Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved under reports/YYYY-MM-DD/ unless --no-save or a custom output directory is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
