---
name: CRM Entity Extraction
description: Standard Operating Procedure (SOP) that bridges extraction logic to CRM append operations via atomic nodes.
os: all
requires:
  bins: [gog]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This workflow relies entirely on discrete, single-responsibility atomic nodes rather than a monolithic loop.
- **Standardized Work (Hyojun Sagyo):** This node represents a strict, step-by-step Standard Operating Procedure (SOP) for data extraction and persistence.
- **Jidoka (自働化):** Includes autonomous self-healing loops with hard verification stops between every step.

# CRM Entity Extraction SOP

This procedure guides the agent to extract structured data and append it to a CRM spreadsheet using explicitly defined atomic nodes.

## Cognitive Directives
WHEN [A business-related email or note containing CRM data is received]
THEN [
  Follow this strict Standard Operating Procedure:

  **Step 1: Entity Extraction**
  - Execute the `LLM-Extract-JSON` atomic skill to extract structured entities (name, org, date).
  - **Jidoka Stop:** Check if the sub-agent returns a valid JSON object matching the requested schema. IF it returns unstructured text, instruct the skill to format correctly and retry. Do NOT proceed until valid JSON is acquired.

  **Step 2: Append to CRM**
  - Execute the `Google Sheets Append Row` (or equivalent) atomic node, passing the extracted JSON row.
  - **Jidoka Stop:** Verify the atomic node returns a successful JSON confirmation. IF the API request fails, retry up to 3 times with the exact error output. IF it still fails, report the error and STOP.
]

## Expected Output
A JSON summary of the extracted data and the successful append confirmation.
