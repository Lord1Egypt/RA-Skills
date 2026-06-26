## Description: <br>
Generate images via OpenRouter API (text-to-image) with automation-ready local scripts and a queue-first workflow for single images or batched variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironystock](https://clawhub.ai/user/ironystock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Banana Claws to generate image files from text prompts through OpenRouter, including posters, thumbnails, illustrations, concept art, and iterative variants. It is especially suited to workflows that enqueue work quickly, process batches asynchronously, and return consolidated completion records with attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and baseline images can be sent to OpenRouter, and provider metadata may be retained locally. <br>
Mitigation: Use a private workspace, avoid sensitive prompts or images unless external transmission is approved, and delete generated queue/provider records when they are no longer needed. <br>
Risk: Queue mode can terminate local processes based on editable queue metadata. <br>
Mitigation: Review queue mode before installation and disable or patch stale-worker cleanup so it only terminates verified worker processes. <br>
Risk: The skill requires an OpenRouter API key and network access. <br>
Mitigation: Scope and protect OPENROUTER_API_KEY, run the preflight check before use, and avoid exposing logs or generated metadata containing request details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ironystock/banana-claws) <br>
- [Declared skill homepage](https://github.com/ironystock/banana-claws) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Generated image files, JSON status/provider records, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENROUTER_API_KEY, supports queued batch generation, writes outputs and queue records to workspace paths, and may persist provider metadata for debugging.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
