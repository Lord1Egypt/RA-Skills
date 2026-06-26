"""
scripts/batch_classify.py

Batch-classify the last N unclassified transactions using classify_with_llm
(Tier 2), which sends the full ledger tree to the LLM and picks the right
line item. Processes transactions in groups of BATCH_SIZE per LLM call to
keep things fast.
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

# Load .env before imports
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

import server.paths as paths
from server.db import get_db
from server.llm import chat

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 100
BATCH_SIZE = 10  # transactions per LLM call


def batch_classify(limit: int = 100):
    conn = get_db(paths.DB_PATH)

    # Fetch unclassified non-pending transactions (most recent first)
    rows = conn.execute(
        """
        SELECT t.id, t.merchant, t.amount, t.date, t.plaid_category,
               ba.name as account_name, ba.id as bank_account_id,
               ba.default_ledger_id
        FROM transactions t
        JOIN bank_accounts ba ON ba.id = t.bank_account_id
        JOIN bank_connections bc ON bc.id = ba.connection_id
        LEFT JOIN transaction_entries te ON te.transaction_id = t.id
        WHERE t.pending = 0 AND te.id IS NULL
        ORDER BY t.date DESC, t.rowid DESC
        LIMIT ?
    """,
        (limit,),
    ).fetchall()

    print(f"Found {len(rows)} transactions to classify")

    # Build ledger tree once
    ledgers = conn.execute("SELECT id, name FROM ledgers ORDER BY name").fetchall()
    line_items = conn.execute("""
        SELECT li.id, li.name, li.item_type, li.ledger_id, l.name AS ledger_name
        FROM line_items li JOIN ledgers l ON l.id = li.ledger_id
        ORDER BY l.name, li.name
    """).fetchall()

    ledger_tree_lines = []
    for ledger in ledgers:
        ledger_tree_lines.append(f"Ledger: {ledger['name']} (id={ledger['id']})")
        for li in line_items:
            if li["ledger_id"] == ledger["id"]:
                ledger_tree_lines.append(f"  - [{li['item_type']}] {li['name']} (id={li['id']})")
    ledger_tree = "\n".join(ledger_tree_lines)

    # Map line_item_id -> ledger_id for fast lookup
    li_to_ledger = {li["id"]: li["ledger_id"] for li in line_items}
    li_ids = set(li_to_ledger.keys())

    classified = 0
    failed = 0

    # Process in batches
    for batch_start in range(0, len(rows), BATCH_SIZE):
        batch = rows[batch_start : batch_start + BATCH_SIZE]

        # Build batch prompt
        txn_lines = []
        for i, t in enumerate(batch):
            txn_lines.append(
                f"{i + 1}. merchant={t['merchant']!r} amount={t['amount']:.2f} "
                f"date={t['date']} account={t['account_name']!r} "
                f"plaid_category={t['plaid_category']!r}"
            )

        system_msg = (
            "You are a personal finance classifier. Classify each transaction "
            "into exactly ONE line item from the ledger tree below.\n\n"
            f"## Ledger Tree\n{ledger_tree}\n\n"
            "Reply with ONLY a JSON array — no markdown — one object per transaction:\n"
            '[{"index":1,"line_item_id":"<exact id>","confidence":0.9,"reasoning":"<short>"},...]'
        )
        user_msg = (
            "## Transactions to classify\n"
            + "\n".join(txn_lines)
            + "\n\nReply with the JSON array only."
        )

        try:
            raw = chat(
                [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.0,
            )

            # Strip markdown fences if present
            raw = raw.strip()
            if raw.startswith("```"):
                raw = "\n".join(raw.split("\n")[1:])
                if raw.endswith("```"):
                    raw = raw[:-3].strip()

            results = json.loads(raw)
            if not isinstance(results, list):
                results = [results]

        except Exception as e:
            print(f"  Batch {batch_start // BATCH_SIZE + 1} LLM error: {e}")
            failed += len(batch)
            continue

        for item in results:
            idx = item.get("index", 1) - 1
            if idx < 0 or idx >= len(batch):
                continue
            t = batch[idx]
            line_item_id = item.get("line_item_id")
            confidence = float(item.get("confidence", 0.8))

            if line_item_id not in li_ids:
                print(f"  Unknown line_item_id {line_item_id!r} for {t['merchant']}")
                failed += 1
                continue

            ledger_id = li_to_ledger[line_item_id]
            entry_id = str(uuid.uuid4())
            uncertain = 1 if confidence < 0.7 else 0

            conn.execute(
                """
                INSERT OR IGNORE INTO transaction_entries
                (id, transaction_id, ledger_id, line_item_id, amount,
                 entry_type, source, confidence, uncertain, reasoning, reviewed)
                VALUES (?, ?, ?, ?, ?, 'spending', 'llm', ?, ?, ?, 0)
            """,
                (
                    entry_id,
                    t["id"],
                    ledger_id,
                    line_item_id,
                    t["amount"],
                    confidence,
                    uncertain,
                    item.get("reasoning", ""),
                ),
            )
            classified += 1

        conn.commit()
        done = min(batch_start + BATCH_SIZE, len(rows))
        print(f"  Progress: {done}/{len(rows)} — classified {classified} so far")

    conn.close()
    print(f"\nDone: {classified} classified, {failed} failed")
    return classified, failed


if __name__ == "__main__":
    batch_classify(LIMIT)
