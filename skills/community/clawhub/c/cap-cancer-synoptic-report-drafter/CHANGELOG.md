# Changelog

## [0.1.1] - 2026-05-28
Rewrote frontmatter description to concise 200–500 character format for improved agent-trigger clarity.

## [0.1.0] - 2026-05-25
Initial release. Five-phase workflow that converts a specimen profile (specimen type, laterality, procedure, prior treatment), the gross description, the microscopic findings, and the ancillary-study results into a DRAFT surgical pathology cancer report — covering CAP Cancer Protocol selection (case type, applicable protocol version, accreditation requirement: CAP LAP / CoC / NAPBC / NAPRC), Required Data Element (RDE) checklist enforcement in the protocol-listed order, WHO Blue Book histologic typing with grade where applicable, margin and lymph-node-yield accounting (with method-of-measurement note), pTNM staging strictly per AJCC 8th Edition with "y" / "r" / "a" prefixes where applicable, treatment-effect / regression-grade fields for neoadjuvant cases, biomarker block (HER2, ER, PR, Ki-67, MMR / MSI, PD-L1, NTRK, BRAF, KRAS, EGFR, ALK, ROS1 — per the protocol), synoptic-block-only format (Required Data Element : Response, one location, in the listed order), comment block for nonsynoptic information, final diagnosis line, an unsigned attending-pathologist sign-out block, an open-questions list, and an evidence index — for attending review and electronic sign-out in the LIS.
