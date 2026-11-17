---
name: dependency-license-scanner
description: >
  Summarize declared licenses from a package manifest snippet. Use when
  checking OSS license risk before adding a dependency.
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":["python3"]}}}
---

# Dependency License Scanner

## Purpose / Overview
Parses a simple `name==version` list and prints license field if provided
alongside each line as `name | license`.

## When to Use
Vendoring decisions; SBOM draft from a hand-built list.

## Usage / Instructions
1. Save lines as `name==version|LicenseName` or bare `name==version`.
2. Run `python3 scripts/scan_licenses.py <file>`.
3. Highlight unknown licenses as `UNKNOWN`.

## Examples
```bash
python3 scripts/scan_licenses.py ./deps.txt
```

## Requirements / Dependencies
python3.

## Limitations / Caveats
Does not download packages or call package registries.

## Security / Permissions
Reads only the list file path given. No network.

## Attribution / License
MIT-0

## Description

Summarize declared licenses from a package manifest snippet.

## Use case

Intended for practitioners who need help with: Summarize declared licenses from a package manifest snippet.

## Risks and mitigations

## References

- SPDX License List: https://spdx.org/licenses/

## Ethical considerations

Illegal use is not allowed. Activity that violates national statutes or international norms is unacceptable; The publisher will not be accountable for illegal use. Do not use this skill for stalking, doxxing, or other privacy invasions that break the law. Do not use outputs to commit fraud or deceive regulated processes.
