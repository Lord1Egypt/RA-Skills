## Description: <br>
Convert CD audio archives and WAV+CUE pairs into organized FLAC tracks, with support for RAR extraction, CUE-based splitting, Chinese filename encoding fixes, multi-CD organization, and optional synced lyric lookup from Netease Cloud Music with Kugou fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanshojin](https://clawhub.ai/user/hanshojin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and audio library maintainers use this skill to convert CD-quality archive releases into per-track FLAC files, organize multi-disc albums, and optionally enrich FLAC or DSF files with synced lyrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversion cleanup can delete source WAV and CUE files, and --delete-rar can remove archive files. <br>
Mitigation: Run with --dry-run first, use --keep-wav and --keep-cue when preservation matters, and enable --delete-rar only when backups exist. <br>
Risk: Lyric lookup sends track metadata to Netease Cloud Music or Kugou. <br>
Mitigation: Avoid --lyrics and --lyrics-only for private libraries when sharing track metadata with those services is unacceptable. <br>
Risk: The skill runs local audio conversion tools over user-selected folders and modifies media tags or writes lyric files. <br>
Mitigation: Install and run it only in trusted local music directories, review the target path before execution, and keep source files until conversion results are verified. <br>


## Reference(s): <br>
- [ClawHub Cd2flac release page](https://clawhub.ai/hanshojin/cd2flac) <br>
- [Netease Cloud Music Linux API endpoint](https://music.163.com/api/linux/forward) <br>
- [Kugou mobile lyric endpoint](http://m.kugou.com/app/i/krc.php?cmd=100&hash={song_hash}&timelength=999999) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Code] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that create, rename, convert, tag, or delete local audio files depending on selected options.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
