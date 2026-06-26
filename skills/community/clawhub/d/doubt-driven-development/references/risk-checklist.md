# Risk Checklist

Use this checklist for high-risk work.

## Release Risk

- Version, tag, changelog, and registry publish version match.
- The package contents are the intended directory.
- CI is green on the pushed commit or tag.

## Permission Risk

- No broad sandbox, approval, or filesystem weakening is introduced.
- Exceptions are narrow and tied to a specific workflow.
- Denied actions are not retried through indirect paths.
- Auto-review is treated as a reviewer for boundary-crossing requests, not as permission expansion.
- High-volume approval noise is reduced with narrow writable roots or precise command prefixes, not broad allow rules.

## Data Risk

- No private data, local secrets, or machine-specific paths are shipped.
- Logs and generated artifacts were checked before publication.
- Rollback or unpublish path is understood when available.
