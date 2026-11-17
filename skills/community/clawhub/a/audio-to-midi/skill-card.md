## Description:

Transcribes audio recordings into MIDI and MusicXML files and reports tempo, key, chords, dynamics, and instrument hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Musicians, arrangers, and audio developers use this skill to turn recordings into editable MIDI or MusicXML and review a basic music analysis. It also supports piano-focused transcription and optional separation of vocals, drums, bass, and other stems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script automatically installs missing Python packages, and the piano engine may download a large model checkpoint.

Mitigation: Run it in a dedicated Python environment and allow for the model download when selecting the piano engine.

Risk: Generated files are written locally and may replace files with the same names in the output folder.

Mitigation: Choose a separate output folder to keep existing files from being replaced.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catsmansion/skills/audio-to-midi)
- [Piano transcription model checkpoint](https://zenodo.org/record/4034264/files/CRNN_note_F1%3D0.9677_pedal_F1%3D0.9186.pth?download=1)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [MIDI and MusicXML files, a JSON analysis file, and a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional stem-separated outputs; analysis and MusicXML generation can be skipped.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
