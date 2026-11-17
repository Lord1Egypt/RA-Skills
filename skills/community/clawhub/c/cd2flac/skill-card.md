## Description:

Converts CD audio archives and WAV/CUE pairs into organized per-track FLAC files, with optional synced lyric lookup and embedding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanshojin](https://clawhub.ai/user/hanshojin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and audio library maintainers use this skill to prepare and run conversion workflows for RAR archives or WAV/CUE album sources, split tracks into FLAC files, organize multi-disc albums, and optionally add synced lyrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion workflow can modify music files and delete source WAV, CUE, or RAR files when cleanup options are used.

Mitigation: Run on backed-up copies first, use --dry-run before conversion, keep source WAV/CUE files with --keep-wav --keep-cue, and avoid --delete-rar until outputs are verified.

Risk: Lyric lookup can send track metadata to Netease and Kugou, and the Kugou fallback uses insecure HTTP endpoints.

Mitigation: Use --lyrics or lyric.py only when sharing track metadata with those services is acceptable; skip lyric lookup for private libraries or sensitive metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanshojin/skills/cd2flac)
- [Netease Cloud Music lyric endpoint](https://music.163.com/api/linux/forward)
- [Kugou mobile search endpoint](http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={encoded}&page=1&pagesize=5)
- [Kugou lyric endpoint](http://m.kugou.com/app/i/krc.php?cmd=100&hash={song_hash}&timelength=999999)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown with inline bash commands; generated FLAC and lyric files when the scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can modify local music libraries and can call external lyric services when lyric lookup is enabled.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
