# Intake fields

## Minimum metadata

- `title`: human-readable name
- `description`: one to three sentences
- `resource_type`: file | link | template | dataset | document | script | image | component | other
- `owner`: person, team, or source
- `license`: license name or `internal-only`
- `version`: semantic version, date, or `unversioned`
- `keywords`: three to eight search terms
- `location`: path, URL, or registry slug

## Common follow-ups

- Missing license: mark `license: unknown` and do not publish externally.
- Sensitive data: mark `classification: restricted` and avoid public sync.
- Duplicate candidate: compare title, hash/path, and version before replacing.
- External publication: confirm redistribution rights first.
