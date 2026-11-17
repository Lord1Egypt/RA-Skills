## Description:

FL Studio Python scripting reference for MIDI controller development, piano roll manipulation, Edison audio editing, workflow automation, and FLP file parsing with PyFLP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delorenj](https://clawhub.ai/user/delorenj)

### License/Terms of Use:


## Use Case:

Developers and music-technology engineers use this skill to create, review, and troubleshoot FL Studio Python scripts for MIDI controllers, piano roll and Edison automation, and FLP project parsing. It supports code, workflow guidance, and API lookup for agents helping with DAW automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent guidance may lead to project-changing FL Studio actions, including edits to .flp files, mixer state, notes, recording state, or undo history.

Mitigation: Inspect projects read-only by default, make backups before editing .flp files, save modified projects under a new name, and require confirmation before running project-changing scripts.

Risk: MIDI controller scripts may affect live DAW behavior when callbacks handle transport, mixer, channel, or hardware-feedback events.

Mitigation: Review generated scripts before use, test with the intended controller and FL Studio project, and confirm device assignment and event handling before live operation.

## Reference(s):

- [FL Studio Scripting Skill](artifact/SKILL.md)
- [Official FL Studio Python Scripting API](https://www.image-line.com/fl-studio/modules/python-scripting/)
- [PyFLP GitHub](https://github.com/demberto/PyFLP)
- [Arrangement & Patterns Module API Reference](artifact/references/api-arrangement-patterns.md)
- [Callbacks & FlMidiMsg Reference](artifact/references/api-callbacks.md)
- [Channels Module API Reference](artifact/references/api-channels.md)
- [Device Module API Reference](artifact/references/api-device.md)
- [Mixer Module API Reference](artifact/references/api-mixer.md)
- [Playlist Module API Reference](artifact/references/api-playlist.md)
- [Plugins Module API Reference](artifact/references/api-plugins.md)
- [Screen & LaunchMapPages Module API Reference](artifact/references/api-screen-launchmap.md)
- [Transport Module API Reference](artifact/references/api-transport.md)
- [UI & General Module API Reference](artifact/references/api-ui-general.md)
- [Utils, Constants & MIDI Reference](artifact/references/api-utils-constants.md)
- [Examples, Patterns & Templates](artifact/references/examples-patterns.md)
- [Piano Roll & Edison Audio Scripting API](artifact/references/piano-roll-edison.md)
- [FLP File Parsing with PyFLP](artifact/references/pyflp.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose DAW automation scripts or FLP parsing steps that require user review before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
