# DEPRECATED — dynamic-temperature

**Status:** Merged into SOUL.md
**Date:** 2026-04-02
**Reason:** Temperature logic is behavioral, not a skill. It belongs in the agent's core identity file, not a separate skill file. Having it as a skill meant it was only consulted when explicitly triggered — missing most cases.
**Lesson:** If a rule should apply to EVERY interaction, put it in SOUL.md. Skills are for triggered workflows, not universal behavioral rules.
**Moved to:** SOUL.md — Section "Temperature Guide"
