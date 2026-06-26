---
name: canslim-analysis
description: Executes a hybrid quantitative and qualitative CANSLIM analysis on US stocks using a fixed schema and a modular Python pipeline, returning a ranked shortlist.
user-invocable: true
requires:
  - python3
os:
  - macos
  - linux
  - windows
---

# CANSLIM Hybrid Analyzer

Analyze US stocks using a three-stage modular pipeline:

1. Run a quantitative screen to filter candidates by earnings, leadership, and price/volume behavior.
2. Use OpenClaw AI enrichment to evaluate qualitative catalysts, float tightness, and institutional quality.
3. Generate a final ranked CANSLIM report using a fixed scoring contract.

## When to use

Use this skill when the user asks to:

- Run a comprehensive CANSLIM analysis on US stocks.
- Screen for market leaders combining both quantitative strength and recent catalysts.
- Generate a ranked shortlist with clear met/missed CANSLIM criteria.
- Audit or reproduce the pipeline with deterministic JSON handoffs.

## Required files

Expected local files (located in `Scripts/` directory):

- `Scripts/quantitative_analyzer.py`
- `Scripts/final_process.py`
- `Scripts/pdf_report_generator.py`
- `Scripts/requirements.txt`

Expected generated files (in `Scripts/` directory):

- `Scripts/intermediate_canslim.json`
- `Scripts/enriched_canslim.json`
- `Scripts/final_canslim_report.json`
- `Scripts/canslim_analysis.log`
- `Scripts/out/canslim_report_{date}.pdf` (PDF report with formatted analysis)

## Canonical JSON contract

The quantitative phase owns `Quantitative_Metrics`.

The AI phase must **preserve every field** already present in `Quantitative_Metrics` and must **only** fill `AI_Qualitative_Checks`.

### Intermediate schema

```json
{
  "Metadata": {
    "Schema_Version": "2.1",
    "Date_Run": "2026-03-15",
    "Market_Direction_M": "Confirmed Uptrend",
    "Total_Universe_Scanned": 503,
    "Successfully_Evaluated": 487,
    "Failed_Fetches": 16,
    "Skipped_For_Missing_Fundamentals": 39,
    "Stocks_Passed_To_AI": 27
  },
  "Stocks": [
    {
      "Ticker": "XYZ",
      "Company_Name": "XYZ Corp",
      "Quantitative_Metrics": {
        "C_Met": true,
        "C_Details": "Q EPS Growth: 38.0%",
        "Quarterly_EPS_Growth": 0.38,
        "EPS_Accelerating": false,
        "A_Met": true,
        "A_Details": "Annual EPS CAGR: 31.0%",
        "Annual_EPS_Growth": 0.31,
        "L_Met": true,
        "RS_Rating": 92.4,
        "S_Quant_Met": true,
        "S_Quant_Details": "Today volume >= 1.5x 50-day average, Up-day volume skew positive",
        "S_Score": 2,
        "Today_Volume_Strong": true,
        "Volume_Skew_Positive": true,
        "I_Quant_Flag": true,
        "I_Quant_Details": "78.0% institutional ownership",
        "N_Technical_Met": true,
        "N_Technical_Details": "Within 4.0% of 52-week high",
        "Near_52_Week_High": true,
        "Recent_Breakout": false,
        "Pct_From_High": 0.04,
        "Current_Price": 145.2,
        "Float_Shares": 42000000,
        "Institutional_Ownership": 0.78
      },
      "AI_Qualitative_Checks_Pending": {
        "N_New_Catalyst": null,
        "N_Catalyst_Details": "",
        "S_Float_Tightness": null,
        "S_Float_Details": "",
        "I_Institutional_Quality": null,
        "I_Institutional_Details": ""
      }
    }
  ]
}
```

## Enriched schema
The enriched schema must be the same as the intermediate schema, plus AI_Qualitative_Checks.
```json

{
  "Stocks": [
    {
      "Ticker": "XYZ",
      "Company_Name": "XYZ Corp",
      "Quantitative_Metrics": { "...": "unchanged and preserved" },
      "AI_Qualitative_Checks_Pending": {
        "N_New_Catalyst": null,
        "N_Catalyst_Details": "",
        "S_Float_Tightness": null,
        "S_Float_Details": "",
        "I_Institutional_Quality": null,
        "I_Institutional_Details": ""
      },
      "AI_Qualitative_Checks": {
        "N_New_Catalyst": true,
        "N_Catalyst_Details": "New product launch and raised guidance",
        "S_Float_Tightness": true,
        "S_Float_Details": "Tight float supported by low float and buyback activity",
        "I_Institutional_Quality": true,
        "I_Institutional_Details": "High-quality institutional sponsorship improving"
      }
    }
  ]
}
```

## Execution rules
Follow this checklist exactly:

1. Verify files: Confirm Scripts/quantitative_analyzer.py, Scripts/final_process.py, Scripts/pdf_report_generator.py, and Scripts/requirements.txt exist.

2. Create environment:
```bash
python3 -m venv canslim_analysis
source canslim_analysis/bin/activate  # Linux/Mac
canslim_analysis\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install --no-cache-dir -r Scripts/requirements.txt
```
4. Run quantitative analysis:
```bash
python Scripts/quantitative_analyzer.py
```

5. Verify intermediate output: Confirm Scripts/intermediate_canslim.json exists and contains Metadata, Stocks, Quantitative_Metrics, and AI_Qualitative_Checks_Pending.

6. Run OpenClaw AI enrichment:
- Read Scripts/intermediate_canslim.json.

- For each stock, preserve Ticker, Company_Name, and the entire Quantitative_Metrics object unchanged.

- Add AI_Qualitative_Checks with values for:

   - N_New_Catalyst
   - N_Catalyst_Details
   - S_Float_Tightness
   - S_Float_Details
   - I_Institutional_Quality
   - I_Institutional_Details

7. Write enriched output: Scripts/enriched_canslim.json

8. Run final processing:
```bash
python Scripts/final_process.py
```
This will automatically generate both the JSON report and the PDF report.

9. Display results: Read Scripts/final_canslim_report.json and present the ranked list of stocks, CANSLIM scores, met criteria, missed criteria, price, RS rating, and catalyst note.

10. PDF Report: The PDF report is generated in `Scripts/out/canslim_report_{date}.pdf` with professional formatting including:
    - Report header with metadata and score distribution
    - Individual stock sections with grades and CANSLIM criteria status
    - Key metrics tables (RS Rating, EPS growth, institutional ownership)
    - Detailed analysis for each criterion (C, A, N, S, L, I, M)

11. Delivery: Always attach the CANSLIM report PDF to the user-facing response when the analysis completes successfully.

12. Cleanup:
```bash
deactivate
```

## Scoring contract
Use this exact final scoring model:

C: Quantitative_Metrics.C_Met

A: Quantitative_Metrics.A_Met

L: Quantitative_Metrics.L_Met

M: Metadata.Market_Direction_M == "Confirmed Uptrend"

N: AI_Qualitative_Checks.N_New_Catalyst == true

S: Quantitative_Metrics.S_Quant_Met == true and AI_Qualitative_Checks.S_Float_Tightness == true

I: AI_Qualitative_Checks.I_Institutional_Quality == true

## Interpretation guidance
N_Technical_Met is supporting technical context, not the scored N letter by itself.

I_Quant_Flag is reference context, not the scored I letter by itself.

A stock can have strong technical N support and still miss final N if OpenClaw cannot verify a fresh catalyst.

A stock can have strong volume accumulation and still miss final S if OpenClaw cannot verify tight float or buyback support.

## Output format

Return the final user-facing answer in this structure:

Market Environment:
<1-2 sentence assessment of the M criterion>

Top CANSLIM Candidates:

| Rank | Ticker | Company | CANSLIM Score | Met Criteria | Missed Criteria | Price | RS Rating | AI Catalyst Note |
|------|--------|---------|---------------|--------------|-----------------|-------|-----------|------------------|
| 1 | XYZ | XYZ Corp | 6/7 | C, A, N, S, L, I | M | $145.20 | 92.4 | New product launch and raised guidance |

AI Catalyst Insights:

XYZ: Fresh catalyst confirmed; float tightness and institutional sponsorship also verified.

Notes & Caveats:
Mention missing data, lack of catalyst confirmation, or market-trend caution when relevant.

## Constraints
Never install dependencies globally.

Always use the canslim_analysis virtual environment.

Use only files generated by the current skill run.

Do not fabricate catalysts, float conclusions, or institutional-quality claims.

If no catalyst is found, set N_New_Catalyst to false and explain briefly.

If the AI phase cannot verify S or I, set the corresponding value to false instead of leaving it ambiguous.

Do not claim results are guaranteed investment advice. Always include disclaimers about risks and the need for further research.

## Failure handling

If execution fails:

State exactly which phase failed: Quantitative, AI Enrichment, or Final Processing.

Include the error message when available.

Recommend the smallest next step.

If the failure is a schema mismatch, state which required field is missing or was overwritten.