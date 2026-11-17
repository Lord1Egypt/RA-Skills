# ClawHub review — 2026-11-07

Fixed lifecycle bypass: card, promote and eval-fixture require accepted, unexpired lessons. A card binds lesson content and note as well as the destination hash. Fixed lexical-only target validation by resolving the project root and rejecting symlink components, including dangling links and missing eval destinations beneath symlinked parents.

The CLI assumes its local project is not concurrently modified by a hostile process; it is not an OS sandbox. Local lessons remain editable by their owner. Explicit fix/remember commands deliberately create accepted local lessons; they do not silently persist ordinary conversation. `/ber report` reads only the current project store. Demo cleanup is limited to its own mktemp directory. Scanner inability to inspect a referenced artifact is not evidence of evasion.
