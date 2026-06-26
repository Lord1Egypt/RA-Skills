## Description: <br>
Analyze music audio files to extract chord progressions, key signature, tempo, and song structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctwww](https://clawhub.ai/user/ctwww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, musicians, and music-analysis users use this skill to analyze local audio files for key signature, tempo, chord progression, chord frequency, and basic song structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analyzer runs local Python code and installs third-party audio-processing dependencies. <br>
Mitigation: Install dependencies in a virtual environment and review package names before running pip. <br>
Risk: The script analyzes a configured local audio path, so an unchanged path may target the wrong file or fail. <br>
Mitigation: Edit the audio path before execution and confirm it points only to the intended audio file. <br>
Risk: Chord and structure detection are approximate and can be less reliable for distorted, layered, or complex music. <br>
Mitigation: Treat results as analysis guidance and use specialized transcription tools when professional accuracy is required. <br>


## Reference(s): <br>
- [Chord Analyzer ClawHub Release](https://clawhub.ai/ctwww/chord-analyzer) <br>
- [ctwww Publisher Profile](https://clawhub.ai/user/ctwww) <br>
- [librosa Project](https://github.com/librosa/librosa) <br>
- [Chordify](https://chordify.net) <br>
- [Hookpad](https://www.hooktheory.com/hookpad) <br>
- [MuseScore](https://musescore.org) <br>
- [Capo](https://capoapp.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the analyzer script prints text reports and returns Python dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and local audio files; analysis quality depends on source audio clarity and musical complexity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
