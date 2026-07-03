"""CSV export framework for bulk data extraction (Wave 1B F6b).

Mirror of csv_import: a SCHEMAS dict (the column ORDER each entity writes),
a request validator, and a writer. Export is the inverse of import — the
columns written line up with what `csv_import.SCHEMAS` accepts, so an
export → re-import round-trip is a no-op under `--on-duplicate skip`.

Functions:
- validate_export_request: check entity_type + output path safety
- write_csv_rows: write rows to a CSV file (overwrite, never append)
- udf_column_name: stable `cf_<name>` naming for exported UDF columns

The caller (an export-* action) owns the DB read; this lib only validates
the request and serialises the already-fetched rows. No DB access here
beyond the optional UDF-name passthrough the caller hands in.
"""
import csv
import os


# ---------------------------------------------------------------------------
# Export column order per entity. Deliberately curated business columns (not
# every DB column): excludes surrogate scope columns the importer regenerates
# (company_id, naming_series) and immutable audit columns (created_at /
# updated_at are kept — useful context, ignored on re-import). The order is the
# header order in the output file. Each set is a SUBSET-compatible superset of
# the matching csv_import schema's required+optional columns so a round-trip
# imports cleanly.
# ---------------------------------------------------------------------------

SCHEMAS = {
    "lead": [
        "id", "lead_name", "company_name", "email", "phone", "source",
        "territory", "industry", "status", "assigned_to", "notes",
        "created_at", "updated_at",
    ],
    "opportunity": [
        "id", "opportunity_name", "opportunity_type", "expected_revenue",
        "probability", "weighted_revenue", "source", "expected_closing_date",
        "stage", "assigned_to", "notes", "created_at", "updated_at",
    ],
    "crm_contact": [
        "id", "name", "email", "phone", "mobile", "job_title", "linkedin_url",
        "lifecycle", "crm_company_id", "assigned_to_user_id", "notes",
        "created_at", "updated_at",
    ],
    "crm_company": [
        "id", "name", "domain", "industry", "employee_count", "annual_revenue",
        "linkedin_url", "lifecycle", "linked_customer_id",
        "assigned_to_user_id", "notes", "created_at", "updated_at",
    ],
}


def udf_column_name(field_name):
    """Exported column name for a UDF field: `cf_<field_name>`."""
    return f"cf_{field_name}"


def validate_export_request(entity_type, output_path):
    """Validate an export request.

    Args:
        entity_type: one of SCHEMAS keys
        output_path: destination .csv path (caller's --output)

    Returns:
        (real_path, errors). `errors` is a list; empty means valid and
        `real_path` is the realpath-resolved destination. The output path is
        NOT required to exist (it's a write target), but its parent directory
        must, and it must carry a .csv extension (symmetry with the import
        path-safety check + guards against writing to an arbitrary location).
    """
    errors = []
    if entity_type not in SCHEMAS:
        return None, [f"Unknown entity type: {entity_type}"]

    if not output_path:
        return None, ["Output path is required"]

    real = os.path.realpath(output_path)
    if not real.lower().endswith(".csv"):
        errors.append("--output must point to a .csv file")
    parent = os.path.dirname(real)
    if parent and not os.path.isdir(parent):
        errors.append(f"Output directory does not exist: {parent}")

    return (real if not errors else None), errors


def write_csv_rows(file_path, base_columns, rows, udf_columns=None):
    """Write rows to a CSV file (overwrite, never append).

    Args:
        file_path: destination path (already validated/realpath'd)
        base_columns: the ordered native columns (SCHEMAS[entity_type])
        rows: list of dicts. Native column values keyed by column name; UDF
            values keyed by the `cf_<name>` exported column name.
        udf_columns: optional ordered list of `cf_<name>` columns to append
            after the native columns (only when UDFs were requested AND data
            exists). Absent / empty => native columns only.

    Returns:
        Number of data rows written.

    Mode is 'w' (truncate — an existing file is OVERWRITTEN, not appended).
    Encoding is utf-8-sig (BOM) so Excel opens it cleanly, matching the
    import reader's utf-8-sig.
    """
    columns = list(base_columns)
    if udf_columns:
        columns = columns + list(udf_columns)

    written = 0
    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: ("" if row.get(c) is None else row.get(c))
                             for c in columns})
            written += 1

    return written
