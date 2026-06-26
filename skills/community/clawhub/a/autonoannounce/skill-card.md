## Description: <br>
Build, operate, and troubleshoot Autonoannounce local speaker text-to-speech using the queued pipeline from enqueue to worker to ElevenLabs to local playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironystock](https://clawhub.ai/user/ironystock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure, run, tune, and troubleshoot low-latency local speaker TTS backed by ElevenLabs synthesis and a queued playback worker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local configuration can affect file writes and playback program selection. <br>
Mitigation: Keep config/tts-queue.json writable only by trusted users, set playback.backend to a known player such as mpv or ffplay, avoid custom backend names, and keep earcons.libraryPath under .openclaw. <br>
Risk: Preflight response files may briefly remain in /tmp on shared machines. <br>
Mitigation: Run preflight only on trusted systems and avoid exposing temporary directories to untrusted local users. <br>
Risk: Network synthesis requires an ElevenLabs API key and sends synthesis requests to ElevenLabs endpoints. <br>
Mitigation: Install only when ElevenLabs-backed local speaker TTS is needed, protect ELEVENLABS_API_KEY, and follow local policy for text that may be sent to the synthesis service. <br>


## Reference(s): <br>
- [Autonoannounce homepage](https://github.com/ironystock/autonoannounce) <br>
- [Runbook](references/runbook.md) <br>
- [Config contract](references/config-contract.md) <br>
- [Performance SLOs](references/perf-slos.md) <br>
- [Foreground path optimization](references/front-path-optimization.md) <br>
- [Earcon library](references/earcon-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local runtime state, local playback backends, ElevenLabs environment variables, and queue performance measurements.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
