## Description: <br>
Collects and manages anime and ACG memes and trending phrases from Chinese internet sources to help agents understand current otaku culture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Noblegasesgoo](https://clawhub.ai/user/Noblegasesgoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to keep an agent's anime and ACG meme context current, especially for Chinese internet trends, Bilibili hot terms, galgame references, and streamer or gaming culture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The collection script weakens HTTPS verification while contacting public Chinese web platforms. <br>
Mitigation: Do not enable scheduled updates until TLS verification is restored; review network behavior before running the script. <br>
Risk: Public web content is automatically persisted into a local meme database and may later be used as agent context. <br>
Mitigation: Treat the generated database as untrusted trend context rather than authoritative facts or instructions, and review entries before user-facing use. <br>


## Reference(s): <br>
- [Anime Meme Collector on ClawHub](https://clawhub.ai/Noblegasesgoo/anime-meme-collector) <br>
- [anime_memes_db.json](references/anime_memes_db.json) <br>
- [anime_memes_manual.md](references/anime_memes_manual.md) <br>
- [Bilibili ranking API](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all) <br>
- [Bilibili hotword API](https://s.search.bilibili.com/main/hotword) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON reference data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates a local meme database capped at 300 entries when the collection script is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
