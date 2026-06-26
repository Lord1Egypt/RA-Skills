## Description: <br>
Find anime releases from raw Chinese or English requests, normalize episode, season, and download intent, verify likely titles, search releases, and return a best result, magnet fallback, or download/status payload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiggy-chan](https://clawhub.ai/user/tiggy-chan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to resolve anime-release requests that may include aliases, latest-season or latest-episode wording, subtitle preferences, magnet-only requests, direct downloads, or follow-up download status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically queue torrents and start a persistent Transmission daemon from natural-language requests without a clear confirmation gate. <br>
Mitigation: Prefer search-only or cli-only magnet mode unless the user explicitly wants downloading, and review or disable high-confidence auto-download behavior before use. <br>
Risk: The skill can contact Bangumi and Nyaa and write local preference or download-status files. <br>
Mitigation: Use it only in environments where those network calls and local state changes are acceptable, especially when legal, bandwidth, or disk side effects matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tiggy-chan/anime-finder) <br>
- [Publisher profile](https://clawhub.ai/user/tiggy-chan) <br>
- [README](README.md) <br>
- [Intent Examples](references/intent_examples.md) <br>
- [Bangumi API](https://api.bgm.tv) <br>
- [Nyaa.si](https://nyaa.si) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON workflow output with optional human-readable text, shell commands, magnet links, torrent URLs, and download status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local preference and last-download state, contact Bangumi and Nyaa, and queue torrents through Transmission when explicitly used in download mode.] <br>

## Skill Version(s): <br>
1.4.0 (source: evidence release metadata and artifact changelog, released 2026-04-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
