# ClawHub Plugin Packager

`clawhub-plugin-packager` is a ClawHub skill for generating, repairing, and auditing **native OpenClaw / ClawHub plugin packages**.

Version `1.1.0` sharpens the package around explicit **plugin modes** rather than treating plugins as a light extension of skill-packaging logic.

## What it does

The skill accepts rough notes, partial requirements, existing plugin code, mixed drafts, or incomplete manifests and turns them into:

1. a **publish-ready native plugin package zip**
2. a **separate plain-text critique file** outside the plugin zip

The critique file records assumptions, repairs, simplifications, and review points for a stronger second pass.

## Supported modes

- `native-tool-plugin` — default fallback mode
- `native-provider-plugin`
- `native-channel-plugin`
- `plugin-audit-only`
- `repair-existing-plugin`

## v1.1 improvements

- Adds explicit plugin-mode selection rules.
- Tightens the minimum publishable contract.
- Strengthens critique-file structure.
- Improves repair behavior for existing plugin drafts.
- Keeps the default output conservative: minimal native tool plugin in TypeScript + ESM unless the request clearly indicates a different runtime role.

## Core delivery rule

For plugin-generation jobs, the skill must keep:

- the **plugin package zip**
- the **critique file**

as two separate outputs.

The critique file must not be embedded inside the generated plugin zip unless the user explicitly asks for that.

## Included support files

- `SKILL.md` — operating instructions for the skill
- `PLUGIN-SPEC-TEMPLATE.yaml` — structured intake template
- `REVIEW-CHECKLIST.txt` — pre-delivery review checklist
- `REVIEW-RECORD-TEMPLATE.txt` — critique output template
- `PORTABILITY.md` — notes for adapting the skill outside ClawHub
- `examples/` — example specs for tool/provider/channel plugin jobs
- `templates/` — starter reference templates for common native plugin types

## Notes

This skill package is the **skill release artifact itself**.

The “plugin zip + separate critique file” rule applies to the plugin jobs generated **by** the skill, not to the distribution of the skill package.
