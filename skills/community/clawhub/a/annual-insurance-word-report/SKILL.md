---
name: annual-insurance-word-report-openclaw
description: Generate annual insurance welfare Word reports from `gh_hg_bscyearall_dues` in OpenClaw format. The packaged Python entry extracts the target year, inspects MySQL column comments, maps business fields into the bundled Word template, and writes the final `.docx` report.
---

# Annual Insurance Word Report

## What this package does

- Resolves the target year from `year` or from `request_text`
- Queries `gh_hg_bscyearall_dues`
- Reads `INFORMATION_SCHEMA.COLUMNS` comments before rendering
- Fills the bundled yearly Word template without depending on Word COM
- Writes the finished `.docx` file to `outputs/` by default

## Inputs

- `request_text`: optional natural-language request, for example `帮我生成2023年业务报告`
- `year`: optional explicit year, for example `2023`
- `template_path`: optional custom `.docx` template path
- `output_path`: optional custom output `.docx` path
- `db_host`: optional, default `127.0.0.1`
- `db_port`: optional, default `3306`
- `db_user`: optional, default `root`
- `db_password`: optional, default `root`
- `database`: optional, default `test_db`
- `table_name`: optional, default `gh_hg_bscyearall_dues`
- `charset`: optional, default `utf8mb4`
- `mysql_cli`: optional fallback path to `mysql` CLI if `PyMySQL` is unavailable

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run with an explicit year:

```bash
python src/main.py --year 2023
```

Run with request text extraction:

```bash
python src/main.py --request-text "帮我生成2023年业务报告"
```

Custom database example:

```bash
python src/main.py --year 2023 --database test_db --db-user root --db-password root
```

## Notes

- The default output path is `outputs/annual-insurance-report-<year>.docx`.
- The default template is stored as text in `assets/beijing_office_annual_template.docx.base64.txt` and is restored to a temporary `.docx` at runtime.
- The package keeps the original business mapping: `团意、子女、女工、重疾、轻症、住院、津贴、补充、两癌、综合A、综合B、合计`.
- If `PyMySQL` is not installed, the entry falls back to the `mysql` CLI when `mysql_cli` is provided or `mysql` is on `PATH`.
