# Artifact storage

Schema version: `2.0`.

Persist nothing for `locate`. A report directory may contain only:

```text
artifacts/<report-id>/
├── extracted.json
└── <verified-source-name>.pdf   # only after an explicit download request
```

`extract` writes or updates only `extracted.json`. For PDF extraction without explicit download, download into a task-temporary directory and remove it after success or failure. For HTML extraction, do not save the HTML, DOM, snapshot, images, or browser state.

Use the deterministic report ID from `report-schema.md`. Resolve the default Artifact root to `<skill-root>/artifacts`; a user-supplied absolute root may override it. Return `artifact_store_unavailable` when the selected root is not writable.

Write `extracted.json` through a temporary sibling and atomic replacement. Treat existing Artifact directories as user data during Skill upgrades.
