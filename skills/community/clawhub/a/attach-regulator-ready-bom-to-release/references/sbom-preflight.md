# SBOM Check reference

Load this reference when preparing or interpreting `powmcp-sbom-preflight:sbom_check` or `powmcp-sbom-preflight:sbom_compare`.

## Scope

SBOM Check version 0.4.5 validates document conformance for CycloneDX and SPDX SBOMs.

For CycloneDX JSON and SPDX JSON, it detects the format and specification version, validates against the applicable bundled official versioned JSON schema, checks every package URL against PURL syntax, checks every declared license against the full SPDX license-id list, and reports document-located defects and a required-field summary.

For CycloneDX XML and SPDX tag-value, it parses and structurally checks the document, detects the format and specification version, and checks required fields, PURLs, and SPDX license identifiers. It does not perform full versioned-schema validation.

The measurement is per fetched or attached document. Comparison applies identical limits to exactly two distinct builds.

## Input decisions

### `powmcp-sbom-preflight:sbom_check`

Choose exactly one source kind:

- `url`: one publicly fetchable HTTP(S) document.
- `file`: one SBOM file attached in the conversation.

Do not provide both. The source limit is 10 MB.

The supported document forms are CycloneDX JSON or XML and SPDX JSON or tag-value. Local paths, pasted document bodies, data URLs, FTP or SFTP, cloud-drive links, and URLs requiring credentials or headers are unsupported.

`maxDefects` caps returned findings per category. Its default is 300, and its allowed range is 1 to 1000.

### `powmcp-sbom-preflight:sbom_compare`

Choose exactly one source kind:

- `urls`: exactly two distinct public SBOM URLs.
- `files`: exactly two distinct attached SBOM files.

Order them as baseline then candidate. Do not provide both source kinds, and do not compare a build with itself.

`maxDefects` caps returned findings per category per build. Its default is 200, and its allowed range is 1 to 500.

Fetching and validating either one live document or two live documents can take up to 60 seconds. Tell the user before the call.

## Result fields to quote

For `powmcp-sbom-preflight:sbom_check`, quote:

- `pass` together with `schema.applied`.
- `schema.reason` when no schema was applied.
- Detected format and specification version.
- The most severe returned defect.
- Schema findings.
- Invalid PURL findings.
- Invalid SPDX license-id findings.
- Required-field summary.
- Any truncation marker.

For `powmcp-sbom-preflight:sbom_compare`, quote:

- Each build's pass state and conformance-defect counts.
- Introduced and resolved schema, PURL, and license findings.
- Added, removed, and version-changed components.
- Added and removed licenses.
- The returned conformance ranking when the measured findings support a distinction.

Quote figures verbatim. Do not recalculate, round, or infer a value omitted from the result.

## Meaning of pass and fail

A pass proves that a supported CycloneDX or SPDX JSON document passed the bundled versioned schema and the scanned PURL and SPDX license checks for the fetched bytes.

A pass does not prove:

- Absence of CVEs or vulnerabilities.
- Acceptable supply-chain risk.
- Complete component coverage.
- Supplier coverage or recursive component resolution.
- Completion of conformity-assessment work.
- Compliance with the BSI version floor unless the detected version is compared separately.

CycloneDX XML and SPDX tag-value cannot return pass true because no JSON schema is applied. Read `schema.reason` and report conformance as not machine-checked rather than diagnosing the document as invalid from `pass: false` alone.

A truncation marker means the returned findings are incomplete evidence. Absence from the findings is not endorsement.

The comparison ranking concerns automated conformance only. Fewer defects do not establish lower supply-chain risk, better security, or more complete coverage.

## Error handling and user lines

The bundled contract does not name failure codes. Do not invent one. For an invalid argument, name the failing field, correct it, and retry. Tell the user:
> The check rejected the `[field]` argument. I corrected that field and retried; the argument error is not evidence about the SBOM.

For duplicate comparison inputs, tell the user:
> SBOM compare failed because the two inputs must be distinct builds. Provide a baseline and a different candidate.

For XML or tag-value, tell the user:
> Conformance was not machine-checked because no JSON schema was applied. The structural, required-field, PURL, and SPDX license-id findings remain reportable.

For a source larger than 10 MB, tell the user:
> The source exceeds the 10 MB limit, so this check did not run.

Do not treat an invalid argument as a missing tool. Do not repeat URL query strings, credentials, or secrets in any error explanation.

## Fix and rerun

Fix document-located schema, PURL, SPDX license-id, or required-field findings in the release artifact. Rerun `powmcp-sbom-preflight:sbom_check` against that same corrected artifact.

Use `powmcp-sbom-preflight:sbom_compare` when before-and-after evidence is the deliverable. It compares exactly two distinct builds under identical limits.

A rule id is not a diagnosis. Open the returned location and apply the returned message without supplying an unstated interpretation.

## Non-PowMCP path

Run sbomqs and the applicable SPDX NTIA conformance checker in CI, validate the document against the relevant official schema, and manually apply the BSI format-version floor. Review supplier and identifier coverage plus recursive component resolution, keep vulnerability statements in a separate CSAF or VEX workflow, and complete the required conformity work.

This path does not produce a `powmcp-sbom-preflight` result. Record which validator and schema supplied the evidence rather than attributing it to PowMCP.

## Source of truth

- SBOM Check app: https://powmcp.com/apps/sbom-preflight/
- BSI TR-03183-2 version 2.1.0: https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf
