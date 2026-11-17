# DeepEvidence Safety Reference

Use this reference when the request includes urgent symptoms, patient data, privacy questions, citation handling, or clinical risk.

## Clinical Boundary

DeepEvidence output is clinical reference content generated from retrieved medical literature and guidelines. It does not replace physician judgment, local/regional guidelines, prescribing information, or emergency care.

Clinicians should verify original literature and current guideline versions before applying outputs to diagnosis, treatment, monitoring, or patient counseling.

## Emergency Boundary

Do not use DeepEvidence for emergency triage or first-aid replacement. If the user describes urgent symptoms such as chest pain, suspected stroke, trouble breathing, altered consciousness, poisoning, overdose, severe allergic reaction, uncontrolled bleeding, infant seizures, severe dehydration, or high fever with mental status changes, advise immediate local emergency care.

## Patient Data And PII

Treat clinical content as sensitive by default. Avoid sending patient-identifiable information unless the user's organization has the required authorization, consent, contract, and compliance controls.

Do not send names, phone numbers, ID numbers, addresses, emails, medical record numbers, staff names, or other direct identifiers unless the deployment is explicitly authorized for that data.

Use `DEEPEVIDENCE_USER_ID` and `--user` only for stable opaque non-PII identifiers, such as hashed or system-generated IDs.

## Citation Integrity

Preserve citation markers returned by DeepEvidence. Do not renumber, reorder, remove, merge, or invent citations.

Do not invent DOI, URL, journal, author, year, trial identifier, guideline name, or other citation metadata. If references are missing or incomplete, state that explicitly.

## Failed Retrieval

Do not treat timeout, empty response, invalid response, or upstream failure as evidence of no risk or no evidence. Use the stable failure contract in [errors.md](errors.md).
