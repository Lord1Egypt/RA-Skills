"""CSV import framework for bulk data loading.

Provides validation, parsing, and bulk insert utilities for importing
items, customers, suppliers, accounts, and opening balances from CSV files.

Functions:
- validate_csv: Check CSV structure against a schema
- parse_csv_rows: Parse and clean CSV rows
- bulk_insert: Insert rows into a table in batches
"""
import csv
import os
import re
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation

_SAFE_NAME = re.compile(r'^[a-z][a-z0-9_]*$')


# ---------------------------------------------------------------------------
# Schema definitions for importable entities
# ---------------------------------------------------------------------------

SCHEMAS = {
    "item": {
        "required": ["item_code", "name", "uom"],
        "optional": ["group", "valuation_method", "description",
                      "default_warehouse", "opening_stock", "opening_rate"],
        "defaults": {"valuation_method": "fifo", "uom": "Nos"},
    },
    "customer": {
        "required": ["name"],
        "optional": ["customer_type", "territory", "default_currency",
                      "email", "phone", "tax_id"],
        "defaults": {"customer_type": "Company", "default_currency": "USD"},
    },
    "supplier": {
        "required": ["name"],
        "optional": ["supplier_type", "country", "default_currency",
                      "email", "phone", "tax_id"],
        "defaults": {"supplier_type": "Company", "default_currency": "USD"},
    },
    "account": {
        "required": ["name", "root_type"],
        "optional": ["account_number", "account_type", "parent_name",
                      "currency", "is_group"],
        "defaults": {"currency": "USD", "is_group": "0"},
    },
    "opening_balance": {
        "required": ["account_number", "debit", "credit"],
        "optional": ["party_type", "party_name"],
        "defaults": {},
    },
    # -------------------------------------------------------------------
    # Wave 1B F6 — CRM entities. `decimal_fields` lists columns that must
    # parse as Decimal (rejected at validate time if non-numeric). These
    # mirror the foundation `lead` / `opportunity` tables and the growth
    # `crm_contact` / `crm_company` tables. Required columns match each
    # table's NOT NULL business key; everything else is optional.
    # -------------------------------------------------------------------
    "lead": {
        "required": ["lead_name"],
        "optional": ["company_name", "email", "phone", "source", "territory",
                      "industry", "status", "assigned_to", "notes"],
        "defaults": {"status": "new"},
    },
    "opportunity": {
        "required": ["opportunity_name"],
        "optional": ["opportunity_type", "expected_revenue", "probability",
                      "source", "expected_closing_date", "assigned_to",
                      "stage", "notes"],
        "defaults": {"opportunity_type": "sales", "stage": "new",
                      "expected_revenue": "0", "probability": "0"},
        "decimal_fields": ["expected_revenue"],
    },
    "crm_contact": {
        "required": ["name"],
        "optional": ["email", "phone", "mobile", "job_title", "linkedin_url",
                      "lifecycle", "assigned_to_user_id", "notes"],
        "defaults": {"lifecycle": "lead"},
    },
    "crm_company": {
        "required": ["name"],
        "optional": ["domain", "industry", "employee_count", "annual_revenue",
                      "linkedin_url", "lifecycle", "linked_customer_id",
                      "assigned_to_user_id", "notes"],
        "defaults": {"lifecycle": "prospect"},
        "decimal_fields": ["annual_revenue"],
    },
}


def validate_csv(file_path, entity_type):
    """Validate a CSV file against a schema.

    Args:
        file_path: Path to the CSV file
        entity_type: One of the SCHEMAS keys

    Returns:
        List of error strings. Empty = valid.
    """
    errors = []

    if entity_type not in SCHEMAS:
        return [f"Unknown entity type: {entity_type}"]

    schema = SCHEMAS[entity_type]

    if not os.path.exists(file_path):
        return [f"File not found: {file_path}"]

    try:
        with open(file_path, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []

            # Check required columns
            for col in schema["required"]:
                if col not in headers:
                    errors.append(f"Missing required column: {col}")

            if errors:
                return errors

            # Validate rows
            for i, row in enumerate(reader, start=2):
                for col in schema["required"]:
                    val = (row.get(col) or "").strip()
                    if not val:
                        errors.append(f"Row {i}: missing required value for '{col}'")

                # Validate decimal fields
                if entity_type == "opening_balance":
                    for field in ("debit", "credit"):
                        val = (row.get(field) or "0").strip()
                        try:
                            Decimal(val)
                        except InvalidOperation:
                            errors.append(f"Row {i}: invalid number for '{field}': {val}")

                # Generic decimal-field validation (Wave 1B F6 CRM money cols).
                # A blank optional money field is fine (it falls back to its
                # default / NULL); a present-but-non-numeric value is rejected.
                for field in schema.get("decimal_fields", []):
                    raw = row.get(field)
                    if raw is None:
                        continue
                    val = raw.strip()
                    if not val:
                        continue
                    try:
                        Decimal(val)
                    except InvalidOperation:
                        errors.append(f"Row {i}: invalid number for '{field}': {val}")

    except Exception as e:
        errors.append(f"Failed to read CSV: {e}")

    return errors


def parse_csv_rows(file_path, entity_type):
    """Parse a CSV file and return cleaned rows with defaults applied.

    Args:
        file_path: Path to the CSV file
        entity_type: One of the SCHEMAS keys

    Returns:
        List of dicts, each representing a row with defaults applied.
    """
    schema = SCHEMAS[entity_type]
    all_cols = schema["required"] + schema["optional"]
    defaults = schema.get("defaults", {})
    rows = []

    with open(file_path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {}
            for col in all_cols:
                val = (row.get(col) or "").strip()
                if not val and col in defaults:
                    val = defaults[col]
                if val:
                    cleaned[col] = val
            rows.append(cleaned)

    return rows


def bulk_insert(conn, table, columns, rows, batch_size=100,
                id_column="id", generate_ids=True,
                *, on_duplicate_mode="skip",
                dup_check=None, update_columns=None):
    """Insert rows into a table in batches, with optional duplicate handling.

    Args:
        conn: SQLite/PG connection (caller owns transaction)
        table: Table name
        columns: List of column names
        rows: List of dicts with column values
        batch_size: Rows per batch
        id_column: Name of the ID column
        generate_ids: Whether to auto-generate UUIDs for id_column
        on_duplicate_mode (keyword-only): how to treat a row that `dup_check`
            reports as already present. One of:
              * "skip"   — leave the existing row, count it under `skipped`
                           (the default; non-breaking for all existing callers,
                           none of which pass `dup_check`).
              * "update" — UPDATE the existing row in place from this row's
                           values (no second row inserted).
              * "fail"   — raise ValueError on the first duplicate (caller's
                           transaction rolls back).
            Ignored entirely when `dup_check` is None (legacy behaviour).
        dup_check: optional callable(conn, row) -> existing_id|None. When it
            returns an id, the row is a duplicate and `on_duplicate_mode`
            applies. When None, every row is inserted (legacy behaviour — this
            is why every pre-F6 caller is unaffected).
        update_columns: optional list restricting which columns an "update"
            writes (defaults to `columns` minus the id column). Always a subset
            of `columns`; each is whitelist-validated below.

    Returns:
        dict {"inserted": N, "updated": N, "skipped": N} when `dup_check` is
        provided; otherwise an int (the inserted count) for backward compat
        with the 4 pre-F6 callers.
    """
    legacy = dup_check is None
    if not rows:
        return 0 if legacy else {"inserted": 0, "updated": 0, "skipped": 0}

    if on_duplicate_mode not in ("skip", "update", "fail"):
        raise ValueError(f"Invalid on_duplicate_mode: {on_duplicate_mode}")

    if generate_ids and id_column not in columns:
        columns = [id_column] + list(columns)

    if not _SAFE_NAME.match(table):
        raise ValueError(f"Invalid table name: {table}")
    for col in columns:
        if not _SAFE_NAME.match(col):
            raise ValueError(f"Invalid column name: {col}")

    placeholders = ", ".join(["?"] * len(columns))
    col_names = ", ".join(columns)
    sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"

    # Columns an "update" mode writes (never the id / pk).
    upd_cols = update_columns if update_columns is not None else [
        c for c in columns if c != id_column
    ]
    for col in upd_cols:
        if not _SAFE_NAME.match(col) or col not in columns:
            raise ValueError(f"Invalid update column: {col}")

    inserted = 0
    updated = 0
    skipped = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        for row in batch:
            existing_id = dup_check(conn, row) if dup_check is not None else None
            if existing_id is not None:
                if on_duplicate_mode == "skip":
                    skipped += 1
                    continue
                if on_duplicate_mode == "fail":
                    raise ValueError(
                        f"Duplicate row in {table} (existing id {existing_id})")
                # update: only write columns whose value is provided (non-None),
                # so a sparse CSV row never blanks out an existing column.
                set_cols = [c for c in upd_cols if row.get(c) is not None]
                if set_cols:
                    set_sql = ", ".join(f"{c} = ?" for c in set_cols)
                    vals = [row.get(c) for c in set_cols] + [existing_id]
                    conn.execute(
                        f"UPDATE {table} SET {set_sql} WHERE {id_column} = ?",
                        vals)
                updated += 1
                continue

            values = []
            for col in columns:
                if col == id_column and generate_ids:
                    values.append(str(uuid.uuid4()))
                else:
                    values.append(row.get(col))
            conn.execute(sql, values)
            inserted += 1

    if legacy:
        return inserted
    return {"inserted": inserted, "updated": updated, "skipped": skipped}
