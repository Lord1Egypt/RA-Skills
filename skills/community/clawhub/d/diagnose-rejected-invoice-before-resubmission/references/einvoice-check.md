# E-Invoice Check reference

## Scope

E-Invoice Check runs the vendored Apache-2.0 KoSIT validator fully offline.
It checks UBL Invoice or CreditNote and UN/CEFACT CII CrossIndustryInvoice XML against the EN 16931 semantic model and the bundled national or Peppol Schematron rules.
The bundled configurations include validator-configuration-xrechnung and validator-configuration-bis scenario artifacts.
The check confirms the artifact by magic bytes and root element, detects syntax and profile, selects or applies a configuration, and reports evidence at rule and offending-element granularity.
It does not extract CII XML from a ZUGFeRD or Factur-X PDF container.

## Tools

- `powmcp-einvoice-check:einvoice_check` validates one safe invoice.
- `powmcp-einvoice-check:einvoice_compare` validates a baseline and revision and reports automated conformance changes.

## `einvoice_check` inputs requiring judgment

Supply exactly one input route:

- `url`: a direct public HTTP(S) sample invoice-XML URL.
- `body`: synthetic, public-sample, or safely redacted raw invoice XML, up to about 10 MB.

A URL cannot be a local path, data URL, authenticated URL, cloud-drive share, viewer page, or unhosted file.
Remove real party names, addresses, contact data, tax or registration IDs, invoice and customer identifiers, payment instructions, and bank or account identifiers before supplying a body.

Use `profile` as follows:

- `auto` is the default and detects from the customization or guideline identifier.
- `peppol` forces the Peppol configuration.
- `xrechnung` forces the XRechnung configuration.

Use the required profile when known. Confirm the reported profile and configuration after every run.
Set `maxFindings` from 1 through 1000. The default is 400.
The offline validation typically takes a few seconds and may take up to about 110 seconds.

## `einvoice_compare` inputs requiring judgment

Supply exactly two invoices total across `urls` and `bodies`, baseline first and revision second.
Use only public-sample, synthetic, or safely redacted invoices of the same lineage.
When two URLs are supplied, they must be distinct invoices.
Each array accepts at most two items.
Use the same `profile` selection for both validations.
Set `maxFindings` from 1 through 600 per invoice. The default is 300.
The validations run sequentially under one shared 115-second deadline.
Read comparability before interpreting changes.

## One-invoice output

Quote these fields without re-deriving them:

- `distinguishedStates`
- `detectedProfile`
- configuration and scenario
- `conforms`
- engine version and detected syntax
- severity counts
- rule ID, severity, rule text or message, and offending element
- structural inventory, including customization or profile identifier, invoice number, currency, line count, and totals presence when returned
- truncation state

Findings are returned most severe first and bounded by `maxFindings`.
Do not repeat invoice URL query strings or invoice line-item contents in narration.

## Comparison output

Quote the per-invoice identities, detected profiles, configurations, scenarios, conformance verdicts, and severity counts.
Then quote the comparability note, regressions, resolved findings, ranking, and any truncation state.
The ranking orders automated conformance first and then fewer error-level findings.
It does not mean one invoice is truer, tax-correct, or more likely to be accepted.

## What a pass proves

A conforming result means the checked bytes matched a bundled scenario and passed its XSD plus the applied EN 16931 and Schematron rules at the named engine and configuration.
The result is limited to the selected artifact, profile, scenario, configuration, and run date.
A comparable pair supports statements about returned regressions and resolutions between those two validations.

A pass does not establish legal validity, tax correctness, factual accuracy, or acceptance by a national platform or Peppol access point.
It does not assess arbitrary buyer-specific rules, routing failures, master-data failures, or platform rules outside the bundled scenarios.
Absence from the findings is not endorsement.

## Unassessable inputs and states

- A PDF container is unassessable because the tools require its embedded CII XML.
- An unhosted local file is unassessable because the URL route accepts public HTTP(S) invoice XML.
- Production data is outside the safe input policy; create a synthetic, public-sample, or safely redacted copy.
- A partial inventory or truncated report is incomplete because all structure or findings were not returned.
- A non-comparable pair does not support regression, resolution, or ranking conclusions.

## Distinguished absence and failure states

Use the returned state verbatim, then tell the user:

- `not-an-einvoice`: "The supplied bytes were not recognized as a supported UBL or CII e-invoice, so no clean conformance verdict is available."
- `schema-invalid`: "The invoice failed the applied schema check; use the returned schema evidence before business-rule remediation."
- `business-rule-failing`: "The invoice failed returned business-rule findings under the named profile and configuration."
- `profile-not-detected`: "The tool did not detect a profile, so this run does not support a clean profile-conformance verdict."
- `unsupported-profile`: "The detected or selected profile is not supported by the bundled scenarios, so this run is unassessable for that profile."
- `no-scenario-matched`: "No bundled scenario matched the artifact, so the run does not establish conformance."

If an invalid-arguments error names a field, say: "The call arguments were invalid for the named field; I will correct that field and call the same tool again."
Do not treat invalid arguments as a missing tool.

## Interpreting rules

A rule ID identifies a rule rather than supplying an independent diagnosis.
Open the cited location and apply the message as returned.
Preserve rule ID, severity, message, and offending element with the repair record.
Do not infer a legal, tax, factual, routing, or platform defect that the report did not produce.

## Non-PowMCP evidence path

Run the Apache-2.0 KoSIT validator directly with the applicable current EN 16931, national, or Peppol configuration.
This path covers XSD and Schematron execution, while its execution and report shape differ from the PowMCP service's bounded findings, distinguished states, and comparison summary.
The surrounding procedure remains the same: safe copy, correct profile, measured evidence, source correction, rerun, retransmission, and separate capture of the receiving platform response.

## Sources of truth

- Peppol BIS Billing 3.0 rules: https://docs.peppol.eu/poacc/billing/3.0/
- E-Invoice Check app and contract: https://powmcp.com/apps/einvoice-check/
