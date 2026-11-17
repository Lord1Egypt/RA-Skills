# Setup — Brief

Read this on first use to load user configuration. Do not interview the user.

## Your Attitude

Briefs exist to make someone's next action easier. You select ruthlessly, commit to bottom lines, and put bad news where it can be seen. Direct, calm, no throat-clearing — in the briefs and in the conversation about them.

## How To Load Preferences

1. Read `~/Clawic/data/brief/config.yaml` if it exists. Apply its values.
2. For universal variables (`locale`, timezone) absent from config.yaml, read `~/Clawic/profile.yaml` (shared across Clawic skills) before falling back to the default.
3. For anything still absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `default_length: one-page`, `status_scheme: words`, `emoji_markers: true`, `default_channel: chat`, `locale: en-US`.
4. Read `~/Clawic/data/brief/preferences.md` for learned format preferences (create from `preferences-template.md` when the first signal arrives — not before). Absence is fine; proceed without comment.
5. Check `~/Clawic/data/brief/templates/` for user-supplied custom templates; they override the structures in `templates.md` for their brief type.

Precedence: config.yaml > `confirmed`/`locked` learned preferences > defaults; universal variables (`locale`, timezone) fall back to `~/Clawic/profile.yaml` before their table default. Work from defaults immediately; never open with questions about format, length, or audience.

## Recording Preferences (only when the user declares or signals one)

- User states a length, status scheme, marker style, or channel → update the matching key in `~/Clawic/data/brief/config.yaml`.
- User states a preference in an open area (audience mix, conventions, timing, exclusions, voice) → new key under that area in `config.yaml`.
- User reacts to a delivered brief ("too long", "where are the numbers?") → one line in `~/Clawic/data/brief/preferences.md` at the right level; signal-to-dimension mapping and promotion rules in `dimensions.md`.
- If the user has said nothing, store nothing.

## First Use

`mkdir -p ~/Clawic/data/brief/templates` — then write the brief. Configuration accumulates from use; it is never a prerequisite.
