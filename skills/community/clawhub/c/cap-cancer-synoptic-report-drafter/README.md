# CAP Cancer Synoptic Report Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Pathology / Surgical Pathology / Anatomic Pathology / Cancer Reporting

## Purpose

Converts a specimen profile (specimen type, laterality, procedure, prior treatment), the gross description, the microscopic findings, and the ancillary-study results into a DRAFT surgical pathology cancer report whose synoptic block follows the applicable College of American Pathologists (CAP) Cancer Protocol — Required Data Elements only, in the listed order, all responses listed together in one location — with WHO Blue Book histologic typing, AJCC 8th Edition pTNM staging (with the "y" / "r" / "a" prefixes where applicable), margin and lymph-node-yield accounting, treatment-effect / tumor-regression-grade fields for neoadjuvant cases, biomarker fields per the protocol (HER2, ER, PR, Ki-67, MMR / MSI, PD-L1, NTRK, BRAF, KRAS, EGFR, ALK, ROS1), a comment block for nonsynoptic information, a final diagnosis line, an unsigned attending-pathologist sign-out block, an open-questions list, and an evidence index — for attending pathologist review and electronic sign-out in the LIS.

## When to Use

- A surgical pathologist needs to draft a CAP-conformant synoptic cancer report for a resection / biopsy / re-excision / lymph-node specimen
- A pathology assistant needs to pre-populate the gross-to-synoptic shell before sign-out
- A pathology resident or fellow needs an RDE checklist to ensure no required data element is missing for CAP LAP / CoC / NAPBC / NAPRC accreditation
- A laboratory information system (LIS) report-builder needs a structured synoptic block to import into PowerPath, CoPath, Epic Beaker AP, or Cerner CoPathPlus
- A cancer registrar needs a draft synoptic that will populate the NAACCR file and the Commission on Cancer (CoC) submission cleanly
- A subspecialty consultant needs to draft an addendum with the synoptic block separated from the consultative opinion

## What It Does

**Phase 1: Case Intake and Protocol Selection**
1. Captures the requesting role (attending pathologist / fellow / resident / PA / LIS builder / consultant), the case posture (in-house resection, in-house biopsy, outside consult, re-excision, addendum), the accreditation surface (CAP LAP, Commission on Cancer, NAPBC, NAPRC, state-mandated), the case identifier (using accession number only — never patient name or MRN in the working draft), and the specimen list with laterality, procedure, and prior-treatment status
2. Selects the applicable CAP Cancer Protocol by anatomic site, procedure, and tumor type (e.g. Breast — Invasive Carcinoma — Resection; Colon and Rectum — Resection; Prostate — Radical Prostatectomy; Lung — Resection; Skin — Melanoma — Excision; Kidney — Nephrectomy; Endometrium — Hysterectomy) and confirms the protocol version (CAP releases protocol updates periodically; the April 2026 release affected 11 protocols and retired two — the user must confirm the version their LIS is configured for)

**Phase 2: Required Data Element (RDE) Checklist**
3. Walks the Required Data Element list for the selected protocol, in the protocol-listed order, asking only for the fields the user has not supplied — never re-orders RDEs and never silently combines two RDEs into one line
4. Enforces the synoptic-block format rule: every Required Data Element is rendered as `Data element : Response` and all RDEs are listed together in one location (diagnosis section, end of report, or separate synoptic section, per institutional convention)
5. Flags missing RDEs as `[OPEN — required by protocol]` rather than silently omitting; the LIS sign-out cannot release a synoptic with `[OPEN]` placeholders

**Phase 3: Histologic Typing, Grade, Margins, Lymph Nodes, and pTNM**
6. Assigns histologic type per the current WHO Classification of Tumours (Blue Book) for that site, with the controlled-vocabulary term (e.g. "Invasive carcinoma of no special type" rather than "ductal carcinoma NOS"), and the histologic grade per the protocol-specified grading system (Nottingham for breast; ISUP / Gleason ISUP grade group for prostate; FNCLCC for soft tissue sarcoma; WHO grade for CNS; FIGO for endometrium)
7. Reconciles margin status (negative, positive, close — with the protocol's "close" threshold and the millimeter measurement of the closest margin), the anatomic margin name (peripheral, deep, radial, circumferential, mucosal, serosal, perineural — per site), and the method of margin assessment (en face / shave vs perpendicular / radial)
8. Reports lymph-node yield as (positive / total examined), with the location of nodes (level for breast / neck dissection; station for lung / mediastinal; basin for melanoma / sentinel), extranodal extension status, and matted-nodes status — and flags lymph-node yields below the protocol's quality threshold (e.g. <12 for colon cancer per NCCN / CoC)
9. Assigns pTNM strictly per the AJCC 8th Edition Cancer Staging Manual for that site, with the correct prefixes (`y` for post-neoadjuvant, `r` for recurrent, `a` for autopsy), and prefixes the T, N, and M categories with `p` for pathologic staging; never substitutes a clinical TNM (cT, cN, cM) into the pathology synoptic, and never assigns a stage group when any of T, N, or M is `X` (unless the protocol explicitly permits)

**Phase 4: Treatment Effect, Biomarkers, Ancillary Studies**
10. For neoadjuvant cases, populates the treatment-effect / tumor-regression-grade RDE per the protocol's grading system (Ryan / Mandard / CAP tumor regression grade 0–3 for GI; RCB / MD Anderson Residual Cancer Burden for breast; Salzer-Kuntschik for sarcoma) and prefixes the pTNM with `y`
11. Populates the biomarker block per the protocol's required panel (Breast: ER, PR, HER2, Ki-67 where reported; Colon: MMR / MSI, BRAF, KRAS / NRAS, HER2 where reported; Lung NSCLC: PD-L1, EGFR, ALK, ROS1, BRAF, NTRK, KRAS, MET, RET, HER2 per the protocol; Melanoma: BRAF; Endometrium: MMR / MSI, p53, POLE per the molecular classification) and flags pending biomarkers as `[PENDING — to be issued by addendum]` with a stated turnaround commitment
12. Cross-checks IHC and molecular results against the morphologic diagnosis: if the IHC or molecular result is discordant (e.g. HER2 IHC 3+ but ISH-negative; ER 0 in a low-grade luminal-pattern carcinoma; CK7−/CK20− in a colorectal-pattern tumor), flags `[DISCORDANT — attending to reconcile]` rather than silently picking one result

**Phase 5: Synoptic Assembly, Comment, Diagnosis Line, and Sign-out**
13. Assembles the synoptic block with every Required Data Element in the protocol-listed order, each `Data element : Response` on its own line, all listed together in one location, with the protocol name and version cited at the head of the block
14. Drafts the comment block for any nonsynoptic information that does not fit a Required Data Element (e.g. unusual stromal pattern, immunohistochemistry rationale, communication-with-treating-team note, deferred items, addendum-promise) — never moves protocol RDEs into the comment block to "shorten" the synoptic
15. Writes the final diagnosis line in standard institutional format (specimen, procedure, diagnosis) referencing the synoptic block for staging and biomarker detail
16. Appends an unsigned attending-pathologist sign-out block, an evidence index that cross-references gross dictation, slide accession numbers and stain panels, ancillary-study report numbers, prior pathology and outside consultation, and an open-questions list for any RDE marked `[OPEN]` or `[DISCORDANT]` or `[PENDING]`

## Output

A draft synoptic pathology packet consisting of (a) the synoptic block in CAP `Data element : Response` format, all RDEs in protocol-listed order, all listed together in one location, with the protocol name and version cited at the head; (b) the comment block for nonsynoptic information; (c) the final diagnosis line; (d) an unsigned attending-pathologist sign-out block; (e) a numbered evidence index; (f) an open-questions list for `[OPEN]` / `[DISCORDANT]` / `[PENDING]` items — all marked **DRAFT — FOR ATTENDING PATHOLOGIST REVIEW AND ELECTRONIC SIGN-OUT IN THE LIS**.

## Notes

This skill **drafts** a CAP-conformant synoptic cancer report to support — never replace — the attending pathologist's diagnosis, sign-out, and electronic release in the laboratory information system. The skill does not assign a diagnosis the attending has not made, does not stage cases the attending has not staged, does not release biomarker results before the attending has reviewed the ancillary-study report, does not sign out a case, and does not communicate critical findings to the treating clinician — those are attending-pathologist responsibilities. The skill uses the **accession number only** in the working draft; patient name, MRN, date of birth, and other PHI are never placed into the working draft and are added only at sign-out in the LIS. The skill stages strictly per the **AJCC 8th Edition Cancer Staging Manual**; clinical (cTNM) staging is out of scope, and the skill never substitutes cTNM for pTNM. The skill follows the protocol version the user confirms — if the user cannot confirm the version their LIS is configured for, the skill stops and asks rather than guessing.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
