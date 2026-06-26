## Description: <br>
Daily news briefing generator that produces a conversational radio-host-style audio briefing and DOCX document covering weather, X/Twitter trends, web trends, world news, politics, tech, local news, sports, markets, and crypto; macOS only, using Apple TTS and afplay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matusvojtek](https://clawhub.ai/user/matusvojtek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users ask their agent for a daily or morning briefing, and the skill gathers public weather, trend, news, market, and crypto information to produce a spoken briefing plus a formatted document. It is intended for configurable personal news briefings on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends configured weather location and trend regions to public services while gathering briefing data. <br>
Mitigation: Review the configured location and trend regions before use, and avoid entering sensitive locations if that disclosure is not acceptable. <br>
Risk: The skill creates local configuration and briefing files and includes a clean helper that permanently removes old date-named briefing folders under the configured output folder. <br>
Mitigation: Review output.folder before running cleanup; version 1.0.3 validates output.folder against safe directories such as Documents, Desktop, Downloads, .briefing-room, and /tmp. <br>
Risk: The skill may run a short background task to gather data, compose the briefing, and generate audio and document outputs. <br>
Mitigation: Run it only when background network access and local file generation are expected, and inspect the generated briefing before relying on it. <br>


## Reference(s): <br>
- [Briefing Room on ClawHub](https://clawhub.ai/matusvojtek/briefing-room) <br>
- [Publisher profile: matusvojtek](https://clawhub.ai/user/matusvojtek) <br>
- [MLX-Audio Kokoro](https://github.com/ml-explore/mlx-audio) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [Coinbase Spot Price API](https://api.coinbase.com/v2/prices/BTC-USD/spot) <br>
- [GetDayTrends](https://getdaytrends.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Agent response plus generated Markdown working text, DOCX document, and MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local configuration for location, language, sections, voices, and output folder; normal output is saved under a date-named briefing folder.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and changelog, released 2026-02-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
