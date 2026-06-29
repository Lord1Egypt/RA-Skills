"""CSV importer for financial-categorizer.

Auto-detects bank CSV format (Nordea, ICA) and imports transactions
into the SQLite database with deduplication. Handles pending transactions
("Reserverat" in Nordea) by updating them when the settled version appears.
"""

import csv
import datetime
import os
import logging
import re

logger = logging.getLogger(__name__)


def clean_description(desc: str) -> str:
    """Normalize descriptions by removing bank transaction prefixes."""
    d = desc.lower()
    # Matches 'reservation kortköp', 'reservation kortkp', 'reservation kortk\xf6p', etc.
    d = re.sub(r'^reservation\s+kortk[\xf6\ufffd\w]+p\s+', '', d)
    # Matches 'kortköp YYMMDD', 'kortkp YYMMDD', etc.
    d = re.sub(r'^kortk[\xf6\ufffd\w]+p\s+\d{6}\s+', '', d)
    # Fallback to remove standalone reservation prefix
    d = re.sub(r'^reservation\s+', '', d)
    return d.strip()


# Known CSV formats. Detection uses a unique header combo per format.
CSV_FORMATS = {
    "nordea": {
        "detect_headers": ["Bokföringsdag", "Rubrik"],
        "date_col": "Bokföringsdag",
        "amount_col": "Belopp",
        "desc_col": "Rubrik",
    },
    "ica": {
        "detect_headers": ["Datum", "Text", "Typ"],
        "date_col": "Datum",
        "amount_col": "Belopp",
        "desc_col": "Text",
    },
}


def parse_date(date_string: str) -> datetime.date:
    """Parse a date string in common Swedish bank formats.

    Supports: YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
    """
    date_string = date_string.strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.datetime.strptime(date_string, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date: {date_string!r}")


def parse_amount(amount_string: str) -> float:
    """Parse a Swedish-format amount string to float.

    Handles comma decimals, strips 'kr' and spaces. Keeps sign as-is.
    """
    s = amount_string.strip()
    s = s.replace("kr", "")
    s = s.replace(" ", "")
    s = s.replace("\xa0", "")  # non-breaking space
    s = s.replace(",", ".")
    return float(s)


def detect_format(header_row: list[str]) -> str | None:
    """Detect the CSV format from the header row.

    Returns the format name ('nordea', 'ica') or None if unrecognized.
    """
    header_set = set(header_row)
    for fmt_name, fmt_def in CSV_FORMATS.items():
        if all(h in header_set for h in fmt_def["detect_headers"]):
            return fmt_name
    return None


def _has_matching_settled(cur, account_id: int, pending_date: datetime.date, pending_desc: str, pending_amount: float) -> bool:
    """Check if a matching settled transaction already exists in the database."""
    cur.execute(
        "SELECT date, description, amount FROM transactions "
        "WHERE account_id = ? AND status = 'settled'",
        (account_id,),
    )
    settled_candidates = cur.fetchall()
    
    pending_desc_clean = clean_description(pending_desc)
    
    for s_date, s_desc, s_amount in settled_candidates:
        # 1. Description substring match
        s_desc_clean = clean_description(s_desc)
        if not (pending_desc_clean in s_desc_clean or s_desc_clean in pending_desc_clean):
            continue
        
        # 2. Date window match (settled date within 10 days after pending date)
        s_dt = datetime.date.fromisoformat(s_date) if isinstance(s_date, str) else s_date
        p_dt = datetime.date.fromisoformat(pending_date) if isinstance(pending_date, str) else pending_date
        days_diff = (s_dt - p_dt).days
        if not (0 <= days_diff <= 10):
            continue
            
        # 3. Amount tolerance match (same sign, within 1.0 SEK difference)
        if (s_amount < 0) != (pending_amount < 0):
            continue
        if abs(s_amount - pending_amount) > 1.0:
            continue
            
        return True
        
    return False

def extract_account_identifier(file_path: str) -> str | None:
    """Extract bank account number/identifier from Nordea CSV columns or file path.

    Returns normalized digits (e.g. '34138' or '32660134138') or None if not found.
    """
    # 1. Try to extract from Nordea CSV Avsändare/Mottagare columns
    try:
        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            header_row = next(reader)
            fmt_name = detect_format(header_row)
            if fmt_name == "nordea":
                avsandare_idx = header_row.index("Avsändare") if "Avsändare" in header_row else -1
                mottagare_idx = header_row.index("Mottagare") if "Mottagare" in header_row else -1
                for row in reader:
                    if not row:
                        continue
                    # Check Avsändare
                    if avsandare_idx != -1 and avsandare_idx < len(row):
                        val = row[avsandare_idx].strip().replace(" ", "").replace("-", "")
                        if val.isdigit() and len(val) >= 5:
                            return val
                    # Check Mottagare
                    if mottagare_idx != -1 and mottagare_idx < len(row):
                        val = row[mottagare_idx].strip().replace(" ", "").replace("-", "")
                        if val.isdigit() and len(val) >= 5:
                            return val
    except Exception:
        pass

    # 2. Fallback: Parse from filename
    basename = os.path.basename(file_path)
    # Match standard clearing + account number pattern like '3266_01_34138' or '3266 01 34138'
    m = re.search(r'\d{4}[_\s-]\d{2}[_\s-]\d{5,}', basename)
    if m:
        return re.sub(r'[_\s-]', '', m.group(0))
        
    # Match any sequence of 5 or more digits that is not part of a date (YYYY-MM-DD or YYYYMMDD)
    # Strip dates out first
    clean_name = re.sub(r'\d{4}-\d{2}-\d{2}', '', basename)
    clean_name = re.sub(r'\d{4}\d{2}\d{2}', '', clean_name)
    m = re.search(r'\d{5,}', clean_name)
    if m:
        return m.group(0)

    return None


def is_identifier_match(id1: str, id2: str) -> bool:
    """Check if two normalized account identifiers match (one is substring or suffix of another)."""
    return id1 in id2 or id2 in id1


class CSVImporter:
    """Imports bank CSV files into the transactions table."""

    def __init__(self, db_handler):
        """
        Args:
            db_handler: A connected DatabaseHandler instance.
        """
        self.db = db_handler

    def import_file(self, file_path: str, account_name: str = None, auto_create_account: bool = True) -> dict:
        """Import a CSV file into the database.

        Args:
            file_path: Path to the CSV file.
            account_name: Override account name. If None, derived from filename or history.
            auto_create_account: If True, create the account if it doesn't exist.

        Returns:
            dict with 'imported', 'skipped' (duplicates), 'errors' counts, and details lists.
        """
        current_id = extract_account_identifier(file_path)

        # Get history of imported source files per account
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT DISTINCT t.account_id, a.name, t.source_file "
            "FROM transactions t "
            "JOIN accounts a ON t.account_id = a.id "
            "WHERE t.source_file IS NOT NULL"
        )
        history = cur.fetchall()

        history_mappings = []
        for hist_acct_id, hist_acct_name, hist_file in history:
            hist_id = extract_account_identifier(hist_file)
            if hist_id:
                history_mappings.append((hist_acct_id, hist_acct_name, hist_id))

        target_acct = None

        if account_name is None:
            # 1. Try auto-detecting from history if current_id matches a historical identifier
            if current_id:
                matching_hist = [
                    (acct_id, acct_name)
                    for acct_id, acct_name, hist_id in history_mappings
                    if is_identifier_match(current_id, hist_id)
                ]
                if matching_hist:
                    unique_matches = list(set(matching_hist))
                    if len(unique_matches) == 1:
                        target_acct = unique_matches[0]
                    else:
                        names = ", ".join([name for _, name in unique_matches])
                        raise ValueError(
                            f"Ambiguous account mapping for identifier '{current_id}'. "
                            f"Historically associated with multiple accounts: {names}. "
                            f"Please specify --account explicitly."
                        )

            # 2. Check metadata if still not resolved
            if target_acct is None and current_id:
                accounts = self.db.list_accounts()
                matches = []
                for acct in accounts:
                    meta_ids = re.findall(r'\d{5,}', acct["name"] + " " + (acct["description"] or ""))
                    if any(is_identifier_match(current_id, mid) for mid in meta_ids) or \
                       current_id in acct["name"].lower() or \
                       current_id in (acct["description"] or "").lower():
                        matches.append((acct["id"], acct["name"]))
                if len(matches) == 1:
                    target_acct = matches[0]

            # 3. Fallback to deriving from filename
            if target_acct is None:
                derived_name = os.path.basename(file_path).split(".")[0]
                target_acct = (None, derived_name)
        else:
            acct = self.db.get_account_by_name(account_name)
            if acct:
                target_acct = (acct["id"], acct["name"])
            else:
                target_acct = (None, account_name)

        target_id, target_name = target_acct

        # Validate against conflicts in history
        if current_id:
            for hist_acct_id, hist_acct_name, hist_id in history_mappings:
                if is_identifier_match(current_id, hist_id):
                    if target_id is not None and target_id != hist_acct_id:
                        raise ValueError(
                            f"Account mismatch: File '{file_path}' contains account identifier '{current_id}' "
                            f"which has historically been imported to account '{hist_acct_name}' (ID {hist_acct_id}), "
                            f"but you specified target account '{target_name}' (ID {target_id})."
                        )
                    elif target_id is None and target_name != hist_acct_name:
                        raise ValueError(
                            f"Account mismatch: File '{file_path}' contains account identifier '{current_id}' "
                            f"which has historically been imported to account '{hist_acct_name}' (ID {hist_acct_id}), "
                            f"but you specified target account name '{target_name}'."
                        )

        if auto_create_account:
            account_id = self.db.ensure_account(target_name)
        else:
            acct = self.db.get_account_by_name(target_name)
            if not acct:
                raise ValueError(
                    f"Account '{target_name}' not found. Create it first or use auto_create_account=True."
                )
            account_id = acct["id"]

        imported = 0
        skipped = 0
        errors = 0
        settled_pending = 0

        details_new = []
        details_skipped = []
        details_settled = []
        details_failures = []

        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            header_row = next(reader)

            fmt_name = detect_format(header_row)
            if fmt_name is None:
                raise ValueError(
                    f"Unrecognized CSV format. Header: {header_row}"
                )

            fmt = CSV_FORMATS[fmt_name]
            date_idx = header_row.index(fmt["date_col"])
            amount_idx = header_row.index(fmt["amount_col"])
            desc_idx = header_row.index(fmt["desc_col"])

            cur = self.db.get_cursor()

            for row in reader:
                if not row or all(cell.strip() == "" for cell in row):
                    continue

                try:
                    raw_date = row[date_idx].strip()
                    is_pending = raw_date.lower() == "reserverat"
                    if is_pending:
                        txn_date = datetime.date.today()
                    else:
                        txn_date = parse_date(raw_date)
                    amount = parse_amount(row[amount_idx])
                    description = row[desc_idx].strip()
                except (ValueError, IndexError) as e:
                    errors += 1
                    details_failures.append({
                        "row": row,
                        "reason": str(e)
                    })
                    continue

                status = "pending" if is_pending else "settled"

                # For settled transactions, check if a pending one exists
                # with a matching description, same account, close date, and close amount.
                if status == "settled":
                    cur.execute(
                        "SELECT id, description, date, amount FROM transactions "
                        "WHERE account_id = ? AND status = 'pending'",
                        (account_id,),
                    )
                    pending_candidates = cur.fetchall()
                    
                    matched_pending_id = None
                    settled_desc_clean = clean_description(description)
                    
                    for p_id, p_desc, p_date, p_amount in pending_candidates:
                        # 1. Description substring match
                        p_desc_clean = clean_description(p_desc)
                        if not (p_desc_clean in settled_desc_clean or settled_desc_clean in p_desc_clean):
                            continue
                        
                        # 2. Date window match (settled date within 10 days after pending date)
                        p_dt = datetime.date.fromisoformat(p_date) if isinstance(p_date, str) else p_date
                        s_dt = datetime.date.fromisoformat(txn_date) if isinstance(txn_date, str) else txn_date
                        days_diff = (s_dt - p_dt).days
                        if not (0 <= days_diff <= 10):
                            continue
                        
                        # 3. Amount tolerance match (same sign, within 1.0 SEK difference)
                        if (p_amount < 0) != (amount < 0):
                            continue
                        if abs(p_amount - amount) > 1.0:
                            continue
                        
                        matched_pending_id = p_id
                        break  # Pick the first matching candidate
                    
                    if matched_pending_id is not None:
                        # Pre-check: Check if the settled version already exists in the database.
                        cur.execute(
                            "SELECT id FROM transactions "
                            "WHERE date = ? AND description = ? AND amount = ? AND account_id = ? AND status = 'settled'",
                            (txn_date, description, amount, account_id),
                        )
                        if cur.fetchone() is not None:
                            # The settled version already exists. We can safely delete the ghost pending transaction.
                            cur.execute("DELETE FROM transactions WHERE id = ?", (matched_pending_id,))
                            skipped += 1
                            details_skipped.append({
                                "date": txn_date,
                                "description": description,
                                "amount": amount,
                                "reason": "Settled version already exists; ghost pending transaction deleted"
                            })
                        else:
                            cur.execute(
                                "UPDATE transactions SET date = ?, description = ?, amount = ?, "
                                "adjusted_amount = ? * "
                                "(SELECT ownership_ratio FROM accounts WHERE accounts.id = account_id), "
                                "status = 'settled', source_file = ? WHERE id = ?",
                                (txn_date, description, amount, amount, file_path, matched_pending_id),
                            )
                            settled_pending += 1
                            imported += 1
                            details_settled.append({
                                "date": txn_date,
                                "description": description,
                                "amount": amount,
                                "matched_pending_id": matched_pending_id
                            })
                        continue

                if status == "pending":
                    if _has_matching_settled(cur, account_id, txn_date, description, amount):
                        skipped += 1
                        details_skipped.append({
                            "date": txn_date,
                            "description": description,
                            "amount": amount,
                            "reason": "Pending transaction already has settled counterpart"
                        })
                        continue

                try:
                    cur.execute(
                        "INSERT INTO transactions (date, description, amount, account_id, source_file, status, adjusted_amount) "
                        "VALUES (?, ?, ?, ?, ?, ?, ? * "
                        "(SELECT ownership_ratio FROM accounts WHERE accounts.id = ?))",
                        (txn_date, description, amount, account_id, file_path, status, amount, account_id),
                    )
                    imported += 1
                    details_new.append({
                        "id": cur.lastrowid,
                        "date": txn_date,
                        "description": description,
                        "amount": amount,
                        "status": status
                    })
                except Exception as e:
                    skipped += 1
                    details_skipped.append({
                        "date": txn_date,
                        "description": description,
                        "amount": amount,
                        "reason": f"Database unique constraint or error: {str(e)}"
                    })

            self.db.commit()

        return {
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "settled_pending": settled_pending,
            "details": {
                "new": details_new,
                "skipped": details_skipped,
                "settled": details_settled,
                "failures": details_failures,
            }
        }
