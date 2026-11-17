# BugDoctor: Diagnose the problem. Find the right fix.

Help your agent diagnose software failures, check existing remedies and make a scoped repair using its current model and tools.

## Use with OpenClaw

Copy this folder, including its references, into your workspace as `skills/bugdoctor`. Or give your OpenClaw the folder and ask it to install BugDoctor there while keeping your existing instructions and model settings. Start a new chat if the skill does not appear.

Then say:

> BugDoctor this error.

Paste the error or refer to the problem already in the conversation. Include what changed and the software version if you know. "Use BugDoctor on this" also works; `$bugdoctor` works where supported.

Use it for a broken deployment, recurring failure, intermittent bug or repeated unsuccessful fixes. Ask for a diagnosis or authorize a repair. It uses relevant code, logs and runtime evidence, plus current documentation and research when they can change the decision.

## Use as a prompt

Paste [BUGDOCTOR.md](BUGDOCTOR.md) into a chat followed by the problem and available evidence. The specialist guides are optional.

[Examples](EXAMPLES.md) · [References](REFERENCES.md) · Version 0.1.0 · [MIT-0 license](LICENSE)
