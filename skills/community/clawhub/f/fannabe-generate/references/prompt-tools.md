# Prompt assistance

The same assist features as the studio's prompt box, usable standalone or inline on a generation.

## Standalone

```bash
fannabe prompt improve "girl on a beach" --media-type image --workflow <aiId>
fannabe prompt ai-edit "make it nighttime" --prompt "girl on a beach" --media-type image
fannabe prompt from-image ./inspo.jpg                  # describe a photo as a prompt
fannabe prompt tools list                              # JSON Prompt Generator, Video Prompter, ...
fannabe prompt tools run <toolId> "a beach scene"
```

## Inline on `generate create`

- `--enhance-prompt` — LLM rewrite/expansion pass (expert mode)
- `--from-image <path-or-url>` — derive the prompt from a photo via vision
- `--ai-edit "<instruction>"` — rewrite the current prompt per an instruction

They compose in that order: from-image, then prompt, then ai-edit.
