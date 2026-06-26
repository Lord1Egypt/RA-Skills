---
name: case-echo
description: extract simple structured json fields from a short chinese medical case description. use when the user provides a brief chinese case summary and wants standard fields like sex, age, diagnosis, stage, egfr, pd-l1, or brain metastasis status.
---

# Case Echo

Extract structured JSON fields from a short Chinese medical case description.

## Use this skill for

- short case summaries in Chinese
- quick field extraction from one paragraph of case text
- converting semi-structured case text into simple JSON
- standardizing obvious fields before downstream analysis

## Fields

Extract these fields when present:

- sex
- age
- diagnosis
- stage
- egfr
- pd_l1
- brain_metastasis
- raw_text

## Execution

Run the bundled shell script and pass the original case text as one quoted argument:

bash scripts/run_case_echo.sh "<USER_CASE_TEXT>"

Replace `<USER_CASE_TEXT>` with the user's original case text.

## Output rules

- Return valid JSON only.
- Do not add explanation before or after the JSON.
- Keep missing fields as null.
- Do not invent values not present in the input text.
- This skill only structures text. It does not provide diagnosis or treatment recommendations.
