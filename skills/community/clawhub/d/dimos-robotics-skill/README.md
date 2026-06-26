# DimOS Robotics Dev Skill

This ZIP contains a ChatGPT/agent skill package for working with the DimensionalOS `dimos` repository, plus templates for creating DimOS runtime `@skill` containers.

It is designed for:

- writing DimOS `Module` classes and `@skill` methods;
- wiring skills into MCP-enabled `Blueprint`s;
- testing with `dimos --replay` or `dimos --simulation` before real hardware;
- avoiding hallucinated robot capabilities by checking `dimos mcp list-tools`;
- generating safe, conservative robot-control wrappers.

## Files

- `SKILL.md` — the skill instructions.
- `resources/` — quick references and safety/testing notes.
- `templates/` — Python and prompt templates for DimOS work.
- `scripts/scaffold_dimos_skill.py` — creates a starter DimOS skill container.

## Example scaffold command

```bash
python scripts/scaffold_dimos_skill.py \
  --class-name RoomReporterSkill \
  --skill-name report_room_status \
  --out room_reporter_skill.py
```

Then add the generated skill container to a DimOS blueprint and test it with an MCP-enabled replay or simulation stack.
