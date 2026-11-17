## Description:

Collects and maintains a Chinese anime, ACG, galgame, streamer, and gaming meme database from Bilibili, Zhihu, manual curation, and bundled keyword lists for trend-aware agent responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noblegasesgoo](https://clawhub.ai/user/noblegasesgoo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to maintain a Chinese anime, ACG, galgame, streamer, and gaming meme database for trend-aware agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The collector can be configured as a persistent scheduled job that runs local code with network and file-write access.

Mitigation: Enable scheduled collection only intentionally, run it from absolute paths under a low-privilege account, and document how to disable the job.

Risk: The collector disables HTTPS certificate verification for outbound requests.

Mitigation: Restore normal HTTPS certificate verification before relying on fetched content.

Risk: The skill fetches content from Bilibili and Zhihu and writes updates to the bundled JSON database.

Mitigation: Install only where outbound access to those services and local updates to the meme database are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/noblegasesgoo/skills/anime-meme-collector)
- [anime_memes_db.json](references/anime_memes_db.json)
- [anime_memes_manual.md](references/anime_memes_manual.md)
- [Bilibili ranking API](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all)
- [Bilibili hotword API](https://s.search.bilibili.com/main/hotword)
- [Zhihu hot list API](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and references to JSON and Markdown data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a local JSON meme database capped at 300 entries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
