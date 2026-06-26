# Changelog

## 1.1.0

- Added explicit plugin-native operating modes: `native-tool-plugin`, `native-provider-plugin`, `native-channel-plugin`, `plugin-audit-only`, and `repair-existing-plugin`.
- Added mode-selection rules that default to the narrowest valid plugin class instead of treating all plugin jobs as the same packaging flow.
- Added a tighter minimum publishable contract covering manifest, config schema, runtime entrypoint, package metadata, README, and output separation.
- Added stronger inference, repair, and self-audit rules for incomplete or inconsistent plugin requests.
- Added expanded example specs and refreshed reference templates for tool, provider, and channel plugin generation.

## 1.0.0

- Initial release of `clawhub-plugin-packager`.
- Added generation of publish-ready native OpenClaw/ClawHub plugin package zips from rough, partial, or incomplete requirements.
- Added separate plain-text critique output for assumptions, inferences, repairs, and review notes.
- Added inference and repair handling for missing or inconsistent plugin specification details.
- Added enforced separation between plugin package output and critique output.
- Added default generation of minimal native tool plugins in TypeScript + ESM unless otherwise specified.
