## Description: <br>
从 YouTube 或本地音频文件分离人声和伴奏，生成纯伴奏音乐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gycdsj](https://clawhub.ai/user/gycdsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create karaoke-style accompaniment by separating vocals from YouTube audio, a direct video URL, or a local audio file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill defaults to using the user's local Chrome/Google session cookies for YouTube downloads. <br>
Mitigation: Install only when this access is acceptable; prefer local-file mode or an explicitly provided limited cookies file. <br>
Risk: The skill depends on command-line audio tools and Python packages that execute locally. <br>
Mitigation: Use a virtual environment, review dependency installation commands, and inspect optional installer commands before running them. <br>
Risk: Downloaded or generated audio files are written to a local output directory. <br>
Mitigation: Review the configured output directory and remove sensitive intermediate or cookie files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gycdsj/accompaniment-generator) <br>
- [Spleeter project referenced by artifact README](https://github.com/deezer/spleeter) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Audio files with optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs accompaniment and optional vocal tracks to the configured local output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
