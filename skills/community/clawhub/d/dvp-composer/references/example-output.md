# Example DVP Output

## Example Study Context

- Protocol: XYZ-2024-001
- Phase: III
- Indication: Non-Small Cell Lung Cancer (NSCLC)
- Design: Randomized, double-blind, placebo-controlled

## Example Check Rules

### AE Module

| Check ID | Category | Description | Logic | Query Wording | Severity | Method |
|----------|----------|-------------|-------|---------------|----------|--------|
| AE-001 | Completeness | AE start date missing | If AE term is filled but start date is empty | Adverse event term is reported but start date is missing. Please provide the start date. | Major | System |
| AE-002 | Consistency | AE start date before informed consent | If AE start date < informed consent date | The start date of adverse event is before the date of informed consent. Please verify. | Major | SAS |
| AE-003 | Consistency | SAE without SAE form | If AE seriousness = Yes but no corresponding SAE narrative exists | Serious adverse event is reported but the SAE narrative form is not completed. Please complete the SAE form. | Critical | System |
| AE-004 | Timeline | AE end date before start date | If AE end date is not null and AE end date < AE start date | The end date of adverse event is before the start date. Please verify both dates. | Major | System |
| AE-005 | Cross-Module | AE without corresponding visit | If AE reported but no visit record within ±3 days of AE start date | Adverse event is reported but there is no corresponding visit record. Please confirm if the visit was conducted. | Minor | SAS |

### Visit Module

| Check ID | Category | Description | Logic | Query Wording | Severity | Method |
|----------|----------|-------------|-------|---------------|----------|--------|
| VS-001 | Timeline | Visit outside window | If actual visit date outside protocol-defined window (±3 days) | Visit date is outside the protocol-defined visit window. Please provide reason for out-of-window visit. | Minor | SAS |
| VS-002 | Completeness | Missing scheduled visit | If expected visit per schedule has no corresponding visit record | Expected visit [Visit Name] has no corresponding visit record. Please confirm if the visit was conducted or missed. | Major | Listing |

### Lab Module

| Check ID | Category | Description | Logic | Query Wording | Severity | Method |
|----------|----------|-------------|-------|---------------|----------|--------|
| LB-001 | Reconciliation | Lab data mismatch with external | If internal lab record does not match external lab transfer on [test, date, value] | Laboratory data discrepancy identified between CRF and central lab data. Please verify. | Major | Reconciliation |
| LB-002 | Consistency | Lab unit inconsistent | If lab unit for same test changes between visits without documented reason | Unit for [lab test] changed from [Unit A] to [Unit B] between visits. Please verify. | Minor | SAS |

### Inclusion/Exclusion Module

| Check ID | Category | Description | Logic | Query Wording | Severity | Method |
|----------|----------|-------------|-------|---------------|----------|--------|
| IE-001 | Consistency | Subject not meeting age criterion | If subject age at screening < 18 or > 75 | Subject age at screening does not meet the protocol-defined age criterion (18-75). Please verify date of birth and informed consent date. | Critical | SAS |
| IE-002 | Completeness | I/E criteria not fully assessed | If any I/E criterion has missing response (Yes/No) | Not all inclusion/exclusion criteria have been assessed. Please complete the assessment for all criteria. | Major | System |

### Exposure/IP Module

| Check ID | Category | Description | Logic | Query Wording | Severity | Method |
|----------|----------|-------------|-------|---------------|----------|--------|
| EX-001 | Consistency | Dose exceeds protocol-defined maximum | If administered dose > protocol-specified max dose | Administered dose exceeds the protocol-defined maximum dose. Please verify the dose and provide reason. | Critical | System |
| EX-002 | Timeline | Treatment start date after AE onset | If first dose date > first AE start date for treatment-emergent AE check | Treatment start date is after the first adverse event onset date. Please verify treatment and AE dates. | Major | SAS |

## Example External Data Reconciliation

| Recon ID | Data Source | Key Fields | Method | Frequency |
|----------|------------|------------|--------|-----------|
| RECON-001 | Central Lab | Sample ID, Test Name, Collection Date, Result | Automated | Per transfer |
| RECON-002 | SAE Reporting | Subject ID, AE Term, SAE Date | Semi-automated | Per event |
| RECON-003 | Randomization | Subject ID, Randomization Date, Treatment Arm | Automated | Per randomization |
