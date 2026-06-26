"""
server/classifier.py — Classifier for Friday Budgeting Pro.

Classification pipeline (post issue #205):
  Primary (classify_transaction): SINGLE unified LLM call that evaluates
      priority-ordered classification_rules with full ledger tree, hints,
      account context, recent reviewed entries, and a transfer hint — all
      in one prompt.  Replaces the legacy two-stage (Tier 1 + Tier 2) flow.
  Auto-promotion (flag_for_review + maybe_promote_to_rule): after enough
      consistent reviewed entries for a merchant, auto-create a routing_rule.

Legacy compat:
  classify_with_rules / classify_with_llm — kept as thin wrappers around
      classify_transaction() so older callers / tests keep working.  New
      code should call classify_transaction() directly.
  apply_rules — deterministic substring match against routing_rules.  Kept
      for the legacy auto-promoted-rule fast path.
"""

from __future__ import annotations

import json
import sqlite3


def _strip_markdown_json(raw: str) -> str:
    """Strip markdown code fences from an LLM response before JSON parsing.

    The LLM sometimes wraps JSON in ```json ... ``` or ``` ... ``` fences
    even when told not to.  Strip them so json.loads always gets clean input.
    """
    s = raw.strip()
    if s.startswith("```"):
        # Drop the opening fence line
        lines = s.splitlines()
        lines = lines[1:]  # remove ```json or ```
        # Drop the closing fence if present
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    return s


# ---------------------------------------------------------------------------
# Batch LLM classification (issue #207)
# ---------------------------------------------------------------------------

# Maximum prompt character count before splitting into sub-batches.
# Approximates ~20 000 tokens (chars / 4 ≈ tokens).
MAX_BATCH_CHARS = 80_000


def _build_batch_user_msg(
    conn: sqlite3.Connection,
    transactions: list[dict],
    rules: list[dict],
    ledger_tree: str,
    hints: list[str],
) -> str:
    """Build the user-side content for a batch classification prompt."""
    enabled_rules = [r for r in rules if r.get("enabled", True)]
    if enabled_rules:
        rules_lines: list[str] = []
        for r in enabled_rules:
            li_note = f" -> line_item_id={r['line_item_id']}" if r.get("line_item_id") else ""
            rules_lines.append(
                f"  [{r['priority']:>3}] id={r['id']}  type={r['rule_type']}"
                f"  name=\"{r['name']}\""
                f"  desc=\"{r['description']}\"{li_note}"
            )
        rules_text = "\n".join(rules_lines)
    else:
        rules_text = "  (no enabled rules)"

    hints_text = "\n".join(f"  - {h}" for h in hints) if hints else "  (none)"

    txn_sections: list[str] = []
    for idx, txn in enumerate(transactions):
        merchant = txn.get("merchant") or "(unknown)"
        amount = txn.get("amount", 0.0)
        date = txn.get("date", "unknown")
        account_name = txn.get("account_name", "")
        account_description = txn.get("account_description", "")
        plaid_category = txn.get("plaid_category", "")

        lines = [
            f"### Transaction {idx}",
            f"  Merchant            : {merchant}",
            f"  Amount              : ${amount:.2f}",
            f"  Date                : {date}",
        ]
        if account_name:
            lines.append(f"  Account             : {account_name}")
        if account_description:
            lines.append(f"  Account description : {account_description}")
        if plaid_category:
            lines.append(f"  Plaid category      : {plaid_category}")

        recent = _fetch_recent_same_merchant(conn, merchant) if merchant else []
        if recent:
            rec_lines = [
                f"  - {r['date']} | {r['merchant']} | ${r['amount']:.2f}"
                f" -> {r['ledger_name']} / {r['line_item_name']} (id={r['line_item_id']})"
                for r in recent
            ]
            lines.append("  Recent reviewed entries for this merchant:")
            lines.extend(rec_lines)
        else:
            lines.append("  Recent reviewed entries: (none)")

        if txn.get("possible_transfer"):
            lines.append(
                "  WARNING: Transfer detector flagged this as a possible internal transfer."
            )

        txn_sections.append("\n".join(lines))

    txns_text = "\n\n".join(txn_sections)

    return (
        f"## Classification Rules (priority ASC - first match wins)\n{rules_text}\n\n"
        f"## Ledger Tree\n{ledger_tree}\n\n"
        f"## Classification Hints\n{hints_text}\n\n"
        f"## Transactions To Classify\n{txns_text}\n\n"
        "Reply with the JSON array only."
    )


def _classify_batch_chunk(
    conn: sqlite3.Connection,
    transactions: list[dict],
    rules: list[dict],
    ledger_tree: str,
    hints: list[str],
) -> list[dict]:
    """Classify one sub-batch with a single LLM call. Returns results in input order."""
    from server.llm import chat

    system_msg = (
        "You are a personal finance classifier. You will classify a BATCH of "
        "bank transactions in ONE shot using all available context.\n\n"
        "Decision policy for EACH transaction:\n"
        "1. Walk the priority-ordered classification rules from top to bottom. "
        "The FIRST rule that clearly applies wins - stop scanning after the "
        "first match. Return that rule's id (and its line_item_id when present).\n"
        "2. If no rule clearly applies, infer the best line_item_id from the "
        "ledger tree, hints, account context, and recent similar entries. "
        "Set rule_id to null in that case.\n"
        "3. classification_type must reflect the chosen line item / rule: "
        "transfer | savings | spending | income | skip.\n"
        "4. Set confidence < 0.7 when you are not confident.\n\n"
        "Reply with ONLY a JSON array - no markdown, no text outside the array - "
        "with one object per transaction, in the SAME order:\n"
        '[{"transaction_index": 0, "rule_id": "<id or null>", '
        '"line_item_id": "<exact id or null>", '
        '"classification_type": "<transfer|savings|spending|income|skip>", '
        '"confidence": <0.0-1.0>, "reasoning": "<one sentence>"}, ...]'
    )

    user_msg = _build_batch_user_msg(conn, transactions, rules, ledger_tree, hints)

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    raw = chat(messages, temperature=0.0)

    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            raise ValueError(f"expected JSON array, got {type(parsed).__name__}")
    except (json.JSONDecodeError, ValueError) as exc:
        import logging

        logging.getLogger(__name__).warning(
            "classify_batch: LLM returned unparseable response: %s", exc
        )
        return [
            {
                "rule_id": None,
                "line_item_id": None,
                "classification_type": "spending",
                "confidence": 0.0,
                "uncertain": True,
                "reasoning": f"batch LLM parse error: {exc}",
            }
            for _ in transactions
        ]

    valid_types = {"transfer", "savings", "spending", "income", "skip"}

    index_map: dict[int, dict] = {}
    for item in parsed:
        if not isinstance(item, dict):
            continue
        idx = item.get("transaction_index")
        if idx is None:
            continue
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            continue
        if 0 <= idx < len(transactions):
            index_map[idx] = item

    results: list[dict] = []
    for i in range(len(transactions)):
        item = index_map.get(i)
        if item is None:
            results.append(
                {
                    "rule_id": None,
                    "line_item_id": None,
                    "classification_type": "spending",
                    "confidence": 0.0,
                    "uncertain": True,
                    "reasoning": "batch LLM did not return result for this transaction",
                }
            )
            continue

        confidence = float(item.get("confidence", 0.0))
        classification_type = item.get("classification_type", "spending")
        if classification_type not in valid_types:
            classification_type = "spending"

        results.append(
            {
                "rule_id": item.get("rule_id"),
                "line_item_id": item.get("line_item_id"),
                "classification_type": classification_type,
                "confidence": confidence,
                "uncertain": confidence < UNCERTAIN_THRESHOLD,
                "reasoning": str(item.get("reasoning", "")),
            }
        )

    return results


def classify_batch(
    conn: sqlite3.Connection,
    transactions: list[dict],
    rules: list[dict],
    ledger_tree: str | None = None,
    hints: list[str] | None = None,
) -> list[dict]:
    """Classify a batch of transactions using as few LLM calls as possible.

    Issue #207: replaces the old per-transaction loop with a single batched
    LLM call.  Shared context (rules, ledger tree, hints) is built once and
    embedded in every batch prompt.  Prompts exceeding ``MAX_BATCH_CHARS``
    are split into sub-batches (greedy bin-packing; at least 1 txn per batch).

    Args:
        conn:         sqlite3 connection for fetching per-transaction context.
        transactions: List of transaction dicts (merchant, amount, date, etc).
        rules:        List of classification_rule dicts (priority ASC).
        ledger_tree:  Pre-rendered ledger tree string.  If None, fetched.
        hints:        List of hint strings.  If None, fetched.

    Returns:
        List of result dicts in the same order as *transactions*:
        {rule_id, line_item_id, classification_type, confidence, uncertain, reasoning}
    """
    if not transactions:
        return []

    if ledger_tree is None:
        ledger_tree = _build_ledger_tree(conn)
    if hints is None:
        hints = _fetch_hints(conn)

    results: list[dict | None] = [None] * len(transactions)

    batch_start = 0
    while batch_start < len(transactions):
        sub_txns: list[dict] = []
        sub_indices: list[int] = []

        for global_idx in range(batch_start, len(transactions)):
            sub_txns.append(transactions[global_idx])
            sub_indices.append(global_idx)

            user_msg = _build_batch_user_msg(conn, sub_txns, rules, ledger_tree, hints)
            if len(user_msg) > MAX_BATCH_CHARS and len(sub_txns) > 1:
                sub_txns.pop()
                sub_indices.pop()
                break

        if not sub_txns:
            sub_txns = [transactions[batch_start]]
            sub_indices = [batch_start]

        chunk_results = _classify_batch_chunk(conn, sub_txns, rules, ledger_tree, hints)
        for local_idx, global_idx in enumerate(sub_indices):
            results[global_idx] = chunk_results[local_idx]

        batch_start += len(sub_txns)

    for i, r in enumerate(results):
        if r is None:
            results[i] = {
                "rule_id": None,
                "line_item_id": None,
                "classification_type": "spending",
                "confidence": 0.0,
                "uncertain": True,
                "reasoning": "batch classification failed for this transaction",
            }

    return results  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Unified single LLM classification call (issue #205)
# ---------------------------------------------------------------------------

UNCERTAIN_THRESHOLD = 0.7


def _build_ledger_tree(conn: sqlite3.Connection) -> str:
    """Render the user's ledger tree as a readable string for the LLM prompt."""
    ledgers_rows = conn.execute("SELECT id, name FROM ledgers ORDER BY name").fetchall()
    line_items_rows = conn.execute(
        "SELECT li.id, li.name, li.ledger_id, li.item_type"
        "  FROM line_items li"
        "  JOIN ledgers l ON l.id = li.ledger_id"
        " ORDER BY l.name, li.name"
    ).fetchall()

    lines: list[str] = []
    for ledger_row in ledgers_rows:
        lines.append(f"  Ledger: {ledger_row['name']} (id={ledger_row['id']})")
        for li in line_items_rows:
            if li["ledger_id"] == ledger_row["id"]:
                # item_type column was added in a later migration; treat missing as ''.
                try:
                    item_type = li["item_type"] or ""
                except (IndexError, KeyError):
                    item_type = ""
                suffix = f" [{item_type}]" if item_type else ""
                lines.append(f"    - {li['name']}{suffix} (id={li['id']})")
    return "\n".join(lines) if lines else "  (no ledgers)"


def _fetch_hints(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT text FROM classification_hints ORDER BY id").fetchall()
    return [r["text"] for r in rows]


def _fetch_recent_same_merchant(
    conn: sqlite3.Connection, merchant: str, limit: int = 5
) -> list[dict]:
    """Return up to *limit* recent reviewed entries for *merchant*."""
    if not merchant:
        return []
    rows = conn.execute(
        "SELECT t.merchant, t.amount, t.date, te.line_item_id, li.name AS li_name,"
        "       l.name AS ledger_name"
        "  FROM transaction_entries te"
        "  JOIN transactions t  ON t.id  = te.transaction_id"
        "  JOIN line_items   li ON li.id = te.line_item_id"
        "  JOIN ledgers      l  ON l.id  = te.ledger_id"
        " WHERE te.reviewed = 1"
        "   AND t.merchant = ?"
        " ORDER BY t.date DESC"
        " LIMIT ?",
        (merchant, limit),
    ).fetchall()
    return [
        {
            "date": r["date"],
            "merchant": r["merchant"],
            "amount": r["amount"],
            "ledger_name": r["ledger_name"],
            "line_item_name": r["li_name"],
            "line_item_id": r["line_item_id"],
        }
        for r in rows
    ]


def classify_transaction(
    conn: sqlite3.Connection,
    transaction: dict,
    rules: list[dict],
    ledger_tree: str | None = None,
    hints: list[str] | None = None,
    context: dict | None = None,
) -> dict:
    """Classify a single transaction with ONE unified LLM call (issue #205).

    Combines what used to be Tier 1 (classify_with_rules) and Tier 2
    (classify_with_llm) into a single prompt containing:

    - Priority-ordered classification rules (first match wins)
    - Full ledger tree with all ledgers + line items + ids
    - Classification hints (free-text user context)
    - Account name + description
    - Up to 5 recent reviewed entries for the same merchant
    - Optional transfer hint and recent corrections
    - The transaction itself (merchant, amount, date, plaid category)

    Args:
        conn:        sqlite3 connection (row_factory must yield Row-like).
                     Used to fetch ledger_tree / hints / recent entries when
                     not supplied by the caller.
        transaction: dict with merchant, amount, date, and optional
                     account_name, account_description, plaid_category.
        rules:       List of classification_rule dicts (priority ASC).
        ledger_tree: Pre-rendered ledger tree string.  If None, the function
                     fetches it from *conn* itself.  Pass-in form is used by
                     ``classify_pending_transactions`` so the tree is fetched
                     once and shared across many transactions.
        hints:       List of hint strings.  If None, fetched from *conn*.
        context:     Optional context dict with:
                     - ``possible_internal_transfer`` (bool)
                     - ``recent_corrections`` (list[dict])

    Returns:
        Result dict with keys:
            rule_id, line_item_id, classification_type,
            confidence, uncertain, reasoning

    Raises:
        ValueError: If the LLM returns invalid JSON or an unknown
            classification_type.
    """
    from server.llm import chat  # local import keeps chat patchable in tests

    # ------------------------------------------------------------------
    # 1. Rules section (enabled only, priority order)
    # ------------------------------------------------------------------
    enabled_rules = [r for r in rules if r.get("enabled", True)]
    if enabled_rules:
        rules_lines: list[str] = []
        for r in enabled_rules:
            li_note = f" → line_item_id={r['line_item_id']}" if r.get("line_item_id") else ""
            rules_lines.append(
                f"  [{r['priority']:>3}] id={r['id']}  type={r['rule_type']}"
                f'  name="{r["name"]}"'
                f'  desc="{r["description"]}"{li_note}'
            )
        rules_text = "\n".join(rules_lines)
    else:
        rules_text = "  (no enabled rules)"

    # ------------------------------------------------------------------
    # 2. Ledger tree
    # ------------------------------------------------------------------
    if ledger_tree is None:
        ledger_tree = _build_ledger_tree(conn)

    # ------------------------------------------------------------------
    # 3. Hints
    # ------------------------------------------------------------------
    if hints is None:
        hints = _fetch_hints(conn)
    hints_text = "\n".join(f"  - {h}" for h in hints) if hints else "  (none)"

    # ------------------------------------------------------------------
    # 4. Transaction details
    # ------------------------------------------------------------------
    merchant = transaction.get("merchant") or "(unknown)"
    amount = transaction.get("amount", 0.0)
    date = transaction.get("date", "unknown")
    account_name = transaction.get("account_name", "")
    account_description = transaction.get("account_description", "")
    plaid_category = transaction.get("plaid_category", "")

    txn_lines = [
        f"  Merchant            : {merchant}",
        f"  Amount              : ${amount:.2f}",
        f"  Date                : {date}",
    ]
    if account_name:
        txn_lines.append(f"  Account             : {account_name}")
    if account_description:
        txn_lines.append(f"  Account description : {account_description}")
    if plaid_category:
        txn_lines.append(f"  Plaid category      : {plaid_category}")
    txn_text = "\n".join(txn_lines)

    # ------------------------------------------------------------------
    # 5. Recent same-merchant reviewed entries
    # ------------------------------------------------------------------
    recent_entries = _fetch_recent_same_merchant(conn, merchant) if merchant else []
    if recent_entries:
        recent_lines = [
            f"  - {r['date']} | {r['merchant']} | ${r['amount']:.2f}"
            f" → {r['ledger_name']} / {r['line_item_name']} (id={r['line_item_id']})"
            for r in recent_entries
        ]
        recent_text = "\n".join(recent_lines)
    else:
        recent_text = "  (none)"

    # ------------------------------------------------------------------
    # 6. Optional context (transfer hint, recent corrections)
    # ------------------------------------------------------------------
    context_parts: list[str] = []
    if context:
        if context.get("possible_internal_transfer"):
            context_parts.append(
                "  ⚠️  Transfer detector flagged this transaction as a "
                "possible internal transfer (same amount moved between accounts)."
            )
        corrections = context.get("recent_corrections") or []
        if corrections:
            corr_lines = [
                f"  - {c.get('date', '?')}  "
                f"{c.get('from_line_item', '?')} → {c.get('to_line_item', '?')}"
                for c in corrections
            ]
            context_parts.append(
                "  Recent manual corrections for this merchant:\n" + "\n".join(corr_lines)
            )
    context_text = "\n".join(context_parts) if context_parts else "  (none)"

    # ------------------------------------------------------------------
    # 7. Compose the single unified prompt
    # ------------------------------------------------------------------
    system_msg = (
        "You are a personal finance classifier. You classify a single bank "
        "transaction in ONE shot using all available context.\n\n"
        "Decision policy:\n"
        "1. Walk the priority-ordered classification rules from top to bottom. "
        "The FIRST rule that clearly applies wins — stop scanning after the "
        "first match. Return that rule's id (and its line_item_id when it "
        "has one).\n"
        "2. If no rule clearly applies, infer the best line_item_id from the "
        "ledger tree, hints, account context, and recent similar entries. "
        "Set rule_id to null in that case.\n"
        "3. classification_type must reflect the chosen line item / rule: "
        "transfer | savings | spending | income | skip. For unmatched "
        "transactions infer the type from the Plaid category and amount sign "
        "(negative = outflow = spending or transfer).\n"
        "4. Set confidence < 0.7 when you are not confident — the caller "
        "will flag the transaction for review.\n\n"
        "Reply with ONLY a JSON object — no markdown, no text outside the "
        "JSON — with these keys:\n"
        '{"rule_id": "<id or null>", "line_item_id": "<exact id or null>", '
        '"classification_type": "<transfer|savings|spending|income|skip>", '
        '"confidence": <0.0-1.0>, "reasoning": "<one sentence>"}'
    )

    user_msg = (
        f"## Classification Rules (priority ASC — first match wins)\n{rules_text}\n\n"
        f"## Ledger Tree\n{ledger_tree}\n\n"
        f"## Classification Hints\n{hints_text}\n\n"
        f"## Recent Reviewed Entries For This Merchant\n{recent_text}\n\n"
        f"## Additional Context\n{context_text}\n\n"
        f"## Transaction To Classify\n{txn_text}\n\n"
        "Reply with the JSON object only."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    # ------------------------------------------------------------------
    # 8. Call the LLM and parse
    # ------------------------------------------------------------------
    raw = chat(messages, temperature=0.0)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned non-JSON response: {raw!r}") from exc

    required_keys = {"classification_type", "confidence", "reasoning"}
    missing = required_keys - parsed.keys()
    if missing:
        raise ValueError(f"LLM JSON missing required keys {sorted(missing)!r}: {parsed!r}")

    confidence = float(parsed.get("confidence", 0.0))

    valid_types = {"transfer", "savings", "spending", "income", "skip"}
    classification_type = parsed.get("classification_type", "")
    if classification_type not in valid_types:
        raise ValueError(
            f"LLM returned unknown classification_type={classification_type!r}. "
            f"Expected one of {sorted(valid_types)!r}."
        )

    return {
        "rule_id": parsed.get("rule_id"),
        "line_item_id": parsed.get("line_item_id"),
        "classification_type": classification_type,
        "confidence": confidence,
        "uncertain": confidence < UNCERTAIN_THRESHOLD,
        "reasoning": str(parsed.get("reasoning", "")),
    }


# ---------------------------------------------------------------------------
# Legacy Tier-1 wrapper — kept for backward-compat (issue #205).
# Now implemented in terms of classify_transaction().
# ---------------------------------------------------------------------------


def classify_with_rules(
    transaction: dict,
    rules: list[dict],
    context: dict | None = None,
) -> dict:
    """Classify a single transaction using priority-ordered rules via the LLM.

    This is the primary Tier-1 entry point.  It passes the full ordered
    ``classification_rules`` list to the LLM and asks it to find the first
    matching rule.  The LLM is also given optional context such as a
    transfer-detection hint from issue #171 and recent manual corrections.

    Args:
        transaction: dict with any of the following keys (all optional except
            those needed for meaningful classification):

            - merchant             (str)  display name from the bank
            - amount               (real) signed transaction amount
            - date                 (str)  ISO-format date
            - account_name         (str)  human name of the bank account
            - account_description  (str)  user-set context for the account
            - plaid_category       (str)  Plaid category string

        rules: list of rule dicts as returned by
            ``list_rules()["rules"]``.  Expected keys per rule:
            ``id``, ``name``, ``description``, ``rule_type``,
            ``line_item_id``, ``priority``, ``enabled``.
            Pre-sorted by priority ASC; disabled rules are skipped.

        context: optional dict with any of:
            - ``possible_internal_transfer`` (bool)  hint from transfer
              detection (#171) — included in the prompt when True.
            - ``recent_corrections`` (list[dict])  recent manual overrides
              for this merchant; each dict should have ``from_line_item``,
              ``to_line_item``, and ``date``.

    Returns:
        A classification result dict::

            {
                "rule_id":             str | None,
                "line_item_id":        str | None,
                "classification_type": "transfer" | "savings" | "spending"
                                        | "income" | "skip",
                "confidence":          float,
                "uncertain":           bool,
                "reasoning":           str,
            }

        ``rule_id`` is the ID of the first matching rule, or ``None`` when no
        rule clearly applies.  ``uncertain`` is ``True`` when confidence < 0.7.

    Raises:
        ValueError: If the LLM returns invalid JSON or a response that is
            missing required fields.
    """
    from server.llm import chat  # local import keeps chat patchable in tests

    UNCERTAIN_THRESHOLD = 0.7

    # ------------------------------------------------------------------
    # 1. Build the rules section (enabled rules only, priority order)
    # ------------------------------------------------------------------
    enabled_rules = [r for r in rules if r.get("enabled", True)]

    if enabled_rules:
        rules_lines: list[str] = []
        for r in enabled_rules:
            li_note = f" → line_item_id={r['line_item_id']}" if r.get("line_item_id") else ""
            rules_lines.append(
                f"  [{r['priority']:>3}] id={r['id']}  type={r['rule_type']}"
                f'  name="{r["name"]}"'
                f'  desc="{r["description"]}"{li_note}'
            )
        rules_text = "\n".join(rules_lines)
    else:
        rules_text = "  (no enabled rules)"

    # ------------------------------------------------------------------
    # 2. Build the transaction section
    # ------------------------------------------------------------------
    merchant = transaction.get("merchant") or "(unknown)"
    amount = transaction.get("amount", 0.0)
    date = transaction.get("date", "unknown")
    account_name = transaction.get("account_name", "")
    account_description = transaction.get("account_description", "")
    plaid_category = transaction.get("plaid_category", "")

    txn_lines = [
        f"  Merchant            : {merchant}",
        f"  Amount              : ${amount:.2f}",
        f"  Date                : {date}",
    ]
    if account_name:
        txn_lines.append(f"  Account             : {account_name}")
    if account_description:
        txn_lines.append(f"  Account description : {account_description}")
    if plaid_category:
        txn_lines.append(f"  Plaid category      : {plaid_category}")
    txn_text = "\n".join(txn_lines)

    # ------------------------------------------------------------------
    # 3. Build the optional context section
    # ------------------------------------------------------------------
    context_parts: list[str] = []
    if context:
        if context.get("possible_internal_transfer"):
            context_parts.append(
                "  ⚠️  Transfer detector flagged this transaction as a "
                "possible internal transfer (same amount moved between accounts)."
            )
        corrections = context.get("recent_corrections") or []
        if corrections:
            corr_lines = [
                f"  - {c.get('date', '?')}  "
                f"{c.get('from_line_item', '?')} → {c.get('to_line_item', '?')}"
                for c in corrections
            ]
            context_parts.append(
                "  Recent manual corrections for this merchant:\n" + "\n".join(corr_lines)
            )
    context_text = "\n".join(context_parts) if context_parts else "  (none)"

    # ------------------------------------------------------------------
    # 4. Compose the prompt
    # ------------------------------------------------------------------
    system_msg = (
        "You are a personal finance classifier.  Your job is to evaluate "
        "priority-ordered classification rules and find the FIRST rule that "
        "clearly applies to the given transaction.  The FIRST match wins — "
        "stop evaluating after the first match.\n\n"
        "Reply with ONLY a JSON object — no markdown, no text outside the JSON — "
        "with these keys:\n"
        '{"rule_id": "<id or null>", "line_item_id": "<id or null>", '
        '"classification_type": "<transfer|savings|spending|income|skip>", '
        '"confidence": <0.0-1.0>, "reasoning": "<one sentence>"}\n\n'
        "Rules for null fields:\n"
        "- Set rule_id=null when no rule clearly applies.\n"
        "- Set line_item_id=null when the matched rule has no line_item_id, "
        "or when no rule matched.\n"
        "- When no rule matches, infer classification_type from the Plaid "
        "category and amount sign (negative = outflow = spending/transfer).\n"
        "- Set confidence < 0.7 (and the caller will set uncertain=true) when "
        "you are not confident."
    )

    user_msg = (
        f"## Classification Rules (priority ASC — first match wins)\n{rules_text}\n\n"
        f"## Transaction\n{txn_text}\n\n"
        f"## Additional Context\n{context_text}\n\n"
        "Reply with the JSON object only."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    # ------------------------------------------------------------------
    # 5. Call the LLM and parse the response
    # ------------------------------------------------------------------
    raw = chat(messages, temperature=0.0)

    try:
        parsed = json.loads(_strip_markdown_json(raw))
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned non-JSON response: {raw!r}") from exc

    # Validate required keys
    required_keys = {"rule_id", "classification_type", "confidence", "reasoning"}
    missing = required_keys - parsed.keys()
    if missing:
        raise ValueError(f"LLM JSON missing required keys {sorted(missing)!r}: {parsed!r}")

    confidence = float(parsed.get("confidence", 0.0))

    # Validate classification_type
    valid_types = {"transfer", "savings", "spending", "income", "skip"}
    classification_type = parsed.get("classification_type", "")
    if classification_type not in valid_types:
        raise ValueError(
            f"LLM returned unknown classification_type={classification_type!r}. "
            f"Expected one of {sorted(valid_types)!r}."
        )

    return {
        "rule_id": parsed.get("rule_id"),
        "line_item_id": parsed.get("line_item_id"),
        "classification_type": classification_type,
        "confidence": confidence,
        "uncertain": confidence < UNCERTAIN_THRESHOLD,
        "reasoning": str(parsed.get("reasoning", "")),
    }


# ---------------------------------------------------------------------------
# Legacy Tier 1 — deterministic substring rules (routing_rules table)
# ---------------------------------------------------------------------------


def apply_rules(
    conn: sqlite3.Connection,
    transaction: dict | sqlite3.Row,
) -> dict | None:
    """Match *transaction* against routing_rules and return an entry dict.

    Args:
        conn: An open sqlite3 connection (row_factory need not be set).
        transaction: A dict or sqlite3.Row with keys:
            - id            (str)  transaction primary key
            - merchant      (str)  merchant name from the bank
            - amount        (real) transaction amount
            - bank_account_id (str)

    Returns:
        A transaction_entry dict ready for insertion if a rule matches::

            {
                "transaction_id": <str>,
                "ledger_id":      <str>,
                "line_item_id":   <str>,
                "amount":         <real>,
                "source":         "rule",
                "confidence":     1.0,
                "reviewed":       0,
            }

        None if no routing_rule matches.

    Matching semantics:
        merchant_pattern is compared case-insensitively as a substring of
        transaction.merchant.  The first rule (lowest id) that matches wins.
    """
    merchant: str = transaction["merchant"] or ""

    # Fetch all rules ordered by id so the "first" match is deterministic.
    cursor = conn.execute(
        "SELECT rr.id, rr.merchant_pattern, rr.line_item_id, li.ledger_id"
        "  FROM routing_rules rr"
        "  JOIN line_items li ON li.id = rr.line_item_id"
        " ORDER BY rr.id ASC",
    )

    for row in cursor:
        pattern: str = row[1] or ""
        if pattern.lower() in merchant.lower():
            return {
                "transaction_id": transaction["id"],
                "ledger_id": row[3],
                "line_item_id": row[2],
                "amount": transaction["amount"],
                "source": "rule",
                "confidence": 1.0,
                "reviewed": 0,
            }

    return None


# ---------------------------------------------------------------------------
# Tier 2 — LLM-based classifier
# ---------------------------------------------------------------------------


def classify_with_llm(
    conn: sqlite3.Connection,
    transaction: dict | sqlite3.Row,
) -> dict:
    """Classify *transaction* using the LLM and return an entry dict.

    Builds rich context from the DB (ledger tree, classification hints, recent
    similar transactions) and asks the LLM to pick the best line_item.

    Args:
        conn: An open sqlite3 connection with row_factory = sqlite3.Row.
        transaction: A dict or sqlite3.Row with at minimum:
            - id        (str)
            - merchant  (str)
            - amount    (real)
            - date      (str, ISO format)

    Returns:
        A transaction_entry dict::

            {
                "transaction_id": <str>,
                "ledger_id":      <str>,
                "line_item_id":   <str>,
                "amount":         <real>,
                "source":         "llm",
                "confidence":     <float>,
                "reviewed":       0,
            }

    Raises:
        ValueError: If the LLM response is not valid JSON, is missing required
            fields, references a line_item_id that does not exist in the DB, or
            returns a ledger_id that does not match the ledger_id looked up from
            the line_item in the DB (ledger_id mismatch).
    """
    from server.llm import chat  # local import keeps chat patchable in tests

    # ------------------------------------------------------------------
    # 1. Build context: full ledger tree
    # ------------------------------------------------------------------
    ledgers_rows = conn.execute("SELECT id, name FROM ledgers ORDER BY name").fetchall()

    line_items_rows = conn.execute(
        "SELECT li.id, li.name, li.ledger_id, l.name AS ledger_name"
        "  FROM line_items li"
        "  JOIN ledgers l ON l.id = li.ledger_id"
        " ORDER BY l.name, li.name"
    ).fetchall()

    # Group line_items by ledger for a readable tree
    ledger_tree_lines: list[str] = []
    for ledger_row in ledgers_rows:
        ledger_tree_lines.append(f"  Ledger: {ledger_row['name']} (id={ledger_row['id']})")
        for li in line_items_rows:
            if li["ledger_id"] == ledger_row["id"]:
                ledger_tree_lines.append(f"    - {li['name']} (id={li['id']})")

    ledger_tree_text = "\n".join(ledger_tree_lines)

    # ------------------------------------------------------------------
    # 2. Build context: classification hints
    # ------------------------------------------------------------------
    hints_rows = conn.execute("SELECT text FROM classification_hints ORDER BY id").fetchall()
    hints_text = "\n".join(f"  - {r['text']}" for r in hints_rows)
    if not hints_text:
        hints_text = "  (none)"

    # ------------------------------------------------------------------
    # 3. Build context: account description (if present)
    # ------------------------------------------------------------------
    account_description: str | None = None
    if isinstance(transaction, dict):
        bank_account_id = transaction.get("bank_account_id")
    else:
        cols = (
            [d[0] for d in transaction.description] if hasattr(transaction, "description") else []
        )
        bank_account_id = transaction["bank_account_id"] if "bank_account_id" in cols else None
    if bank_account_id:
        acct_row = conn.execute(
            "SELECT description FROM bank_accounts WHERE id = ?",
            (bank_account_id,),
        ).fetchone()
        if acct_row and acct_row["description"]:
            account_description = acct_row["description"]

    # ------------------------------------------------------------------
    # 4. Build context: 5 most recent reviewed entries with same merchant
    # ------------------------------------------------------------------
    merchant: str = transaction["merchant"] or ""
    recent_rows = conn.execute(
        "SELECT t.merchant, t.amount, t.date, te.line_item_id, li.name AS li_name,"
        "       l.name AS ledger_name"
        "  FROM transaction_entries te"
        "  JOIN transactions t  ON t.id  = te.transaction_id"
        "  JOIN line_items   li ON li.id = te.line_item_id"
        "  JOIN ledgers      l  ON l.id  = te.ledger_id"
        " WHERE te.reviewed = 1"
        "   AND t.merchant = ?"
        " ORDER BY t.date DESC"
        " LIMIT 5",
        (merchant,),
    ).fetchall()

    if recent_rows:
        recent_lines = [
            f"  - {r['date']} | {r['merchant']} | ${r['amount']:.2f}"
            f" → {r['ledger_name']} / {r['li_name']} (id={r['line_item_id']})"
            for r in recent_rows
        ]
        recent_text = "\n".join(recent_lines)
    else:
        recent_text = "  (none)"

    # ------------------------------------------------------------------
    # 5. Compose the prompt
    # ------------------------------------------------------------------
    system_msg = (
        "You are a personal finance classifier. Your job is to classify a bank "
        "transaction into exactly ONE line item from the user's ledger. "
        "Reply with ONLY a JSON object — no markdown, no explanation outside the JSON — "
        "with these keys:\n"
        '  {"line_item_id": "<exact id>", "confidence": <0.0-1.0>, "reasoning": "<short>"}\n'
        "Choose the line_item_id that best fits the transaction based on the ledger tree, "
        "the user's hints, and any recent similar transactions."
    )

    account_context_section = (
        f"## Account Context\n  {account_description}\n\n" if account_description else ""
    )

    user_msg = (
        f"## Ledger Tree\n{ledger_tree_text}\n\n"
        f"## Classification Hints\n{hints_text}\n\n"
        f"## Recent Similar Transactions (reviewed)\n{recent_text}\n\n"
        f"{account_context_section}"
        f"## Transaction to Classify\n"
        f"  Merchant : {merchant}\n"
        f"  Amount   : ${transaction['amount']:.2f}\n"
        f"  Date     : {transaction.get('date', 'unknown')}\n\n"
        "Reply with the JSON object only."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    # ------------------------------------------------------------------
    # 5. Call the LLM and parse the response
    # ------------------------------------------------------------------
    raw = chat(messages, temperature=0.0)

    try:
        parsed = json.loads(_strip_markdown_json(raw))
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned non-JSON response: {raw!r}") from exc

    if "line_item_id" not in parsed:
        raise ValueError(f"LLM JSON missing 'line_item_id' key: {parsed!r}")

    line_item_id: str = parsed["line_item_id"]
    confidence: float = float(parsed.get("confidence", 0.0))

    # ------------------------------------------------------------------
    # 6. Resolve ledger_id from the DB (validates line_item_id exists)
    # ------------------------------------------------------------------
    li_row = conn.execute(
        "SELECT ledger_id FROM line_items WHERE id = ?",
        (line_item_id,),
    ).fetchone()

    if li_row is None:
        raise ValueError(
            f"LLM returned unknown line_item_id={line_item_id!r} which does not exist in the DB."
        )

    ledger_id: str = li_row["ledger_id"]

    # ------------------------------------------------------------------
    # 7. Validate ledger_id consistency if the LLM also returned one
    # ------------------------------------------------------------------
    if "ledger_id" in parsed:
        llm_ledger_id = parsed["ledger_id"]
        if llm_ledger_id != ledger_id:
            raise ValueError(
                f"LLM returned ledger_id={llm_ledger_id!r} but line_item_id={line_item_id!r}"
                f" belongs to ledger_id={ledger_id!r} — ledger_id mismatch."
            )

    return {
        "transaction_id": transaction["id"],
        "ledger_id": ledger_id,
        "line_item_id": line_item_id,
        "amount": transaction["amount"],
        "source": "llm",
        "confidence": confidence,
        "reviewed": 0,
    }


# ---------------------------------------------------------------------------
# Tier 2b — safe wrapper with fallback-to-review
# ---------------------------------------------------------------------------


def safe_classify(
    conn: sqlite3.Connection,
    transaction: dict | sqlite3.Row,
    fallback_to_review: bool = True,
) -> dict:
    """Classify *transaction* with graceful degradation on LLM validation failures.

    Wraps :func:`classify_with_llm` and intercepts ``ValueError`` raised by
    any validation step (bad JSON, missing ``line_item_id`` key, unknown
    ``line_item_id``, or ``ledger_id`` mismatch).

    Args:
        conn: An open sqlite3 connection with ``row_factory = sqlite3.Row``.
        transaction: A dict or sqlite3.Row with at minimum:
            - id        (str)
            - merchant  (str)
            - amount    (real)
            - date      (str, ISO format)
        fallback_to_review: When ``True`` (default) a validation failure
            returns a stub entry flagged for human review instead of raising.
            When ``False`` the ``ValueError`` is re-raised.

    Returns:
        On success: the entry dict returned by :func:`classify_with_llm`
        (possibly with ``source`` updated by a downstream
        :func:`flag_for_review` call if you use that separately).

        On validation failure with *fallback_to_review=True*::

            {
                "transaction_id":  <str>,
                "ledger_id":       None,
                "line_item_id":    None,
                "amount":          <real>,
                "source":          "llm-rejected",
                "confidence":      0.0,
                "reviewed":        0,
                "rejection_reason": "<short description of what went wrong>",
            }

    Raises:
        ValueError: Only when *fallback_to_review=False* and the LLM output
            fails validation.
    """
    import logging

    logger = logging.getLogger(__name__)

    try:
        return classify_with_llm(conn, transaction)
    except ValueError as exc:
        reason = str(exc)
        logger.warning(
            "safe_classify: LLM output rejected for transaction_id=%r — %s",
            transaction["id"],
            reason,
        )
        if not fallback_to_review:
            raise
        return {
            "transaction_id": transaction["id"],
            "ledger_id": None,
            "line_item_id": None,
            "amount": transaction["amount"],
            "source": "llm-rejected",
            "confidence": 0.0,
            "reviewed": 0,
            "rejection_reason": reason,
        }


# ---------------------------------------------------------------------------
# Tier 3 — review-flag + auto-promotion
# ---------------------------------------------------------------------------


def flag_for_review(
    transaction: dict,
    llm_result: dict,
    threshold: float = 0.75,
) -> dict:
    """Tag low-confidence LLM results as needing human review.

    This is a **pure function** — it performs no database reads or writes.

    Args:
        transaction: The raw transaction dict (used for context, not mutated).
        llm_result:  The entry dict produced by :func:`classify_with_llm`.
            Expected keys: ``transaction_id``, ``ledger_id``,
            ``line_item_id``, ``amount``, ``source``, ``confidence``,
            ``reviewed``.
        threshold:   Minimum confidence (inclusive) required for the result to
            pass through unchanged.  Defaults to **0.75**.  Callers can
            override — e.g. ``flag_for_review(txn, res, threshold=0.9)``
            for a stricter policy.

    Returns:
        A copy of *llm_result* with ``source`` set to ``"llm-needs-review"``
        when ``confidence < threshold``, otherwise *llm_result* unchanged.
        ``reviewed`` is always ``0`` on the returned entry.
    """
    if llm_result["confidence"] < threshold:
        flagged = dict(llm_result)
        flagged["source"] = "llm-needs-review"
        return flagged
    return llm_result


def maybe_promote_to_rule(
    conn: sqlite3.Connection,
    transaction: dict | sqlite3.Row,
    llm_result: dict,
) -> dict | None:
    """Auto-create a Tier-1 routing rule after 3+ consistent reviewed entries.

    Looks at recent ``transaction_entries`` for the same merchant that have
    ``source IN ('llm', 'manual')`` and ``reviewed = 1``.  If at least **3**
    of them share the same ``line_item_id`` as *llm_result*, a new
    ``routing_rule`` is inserted.

    **Idempotent** — if a rule with the same
    ``(merchant_pattern, line_item_id)`` pair already exists, the existing
    rule is returned and no duplicate is created.

    Args:
        conn:        An open sqlite3 connection.
        transaction: A dict or sqlite3.Row with at least a ``merchant`` key.
        llm_result:  The entry dict produced by :func:`classify_with_llm`
            (or :func:`flag_for_review`).  Must contain ``line_item_id``.

    Returns:
        A dict ``{"id": …, "merchant_pattern": …, "line_item_id": …}``
        for the new (or pre-existing) rule, or ``None`` if the promotion
        threshold was not met.
    """
    import uuid

    merchant: str = transaction["merchant"] or ""
    target_line_item_id: str = llm_result["line_item_id"]

    # ------------------------------------------------------------------
    # 1. Count consistent reviewed entries for this merchant + line_item
    # ------------------------------------------------------------------
    row = conn.execute(
        """
        SELECT COUNT(*) AS cnt
          FROM transaction_entries te
          JOIN transactions t ON t.id = te.transaction_id
         WHERE t.merchant = ?
           AND te.source IN ('llm', 'manual')
           AND te.reviewed = 1
           AND te.line_item_id = ?
        """,
        (merchant, target_line_item_id),
    ).fetchone()

    consistent_count: int = row[0] if row else 0

    if consistent_count < 3:
        return None

    # ------------------------------------------------------------------
    # 2. Idempotency check — return existing rule if one already exists
    # ------------------------------------------------------------------
    existing = conn.execute(
        """
        SELECT id, merchant_pattern, line_item_id
          FROM routing_rules
         WHERE merchant_pattern = ?
           AND line_item_id = ?
        """,
        (merchant, target_line_item_id),
    ).fetchone()

    if existing is not None:
        # Do NOT insert another log row for an already-existing rule.
        return {
            "id": existing[0],
            "merchant_pattern": existing[1],
            "line_item_id": existing[2],
        }

    # ------------------------------------------------------------------
    # 3. Collect the transaction ids that contributed to the promotion
    #    (the 3+ consistent reviewed entries for this merchant + line_item)
    # ------------------------------------------------------------------
    import time

    source_rows = conn.execute(
        """
        SELECT t.id AS txn_id
          FROM transaction_entries te
          JOIN transactions t ON t.id = te.transaction_id
         WHERE t.merchant = ?
           AND te.source IN ('llm', 'manual')
           AND te.reviewed = 1
           AND te.line_item_id = ?
        ORDER BY t.date DESC
        """,
        (merchant, target_line_item_id),
    ).fetchall()
    source_transaction_ids: list[str] = [r[0] for r in source_rows]

    # ------------------------------------------------------------------
    # 4. Create the new routing rule and write the audit log row atomically
    # ------------------------------------------------------------------
    new_id = str(uuid.uuid4())
    log_id = str(uuid.uuid4())
    created_at = int(time.time())

    conn.execute(
        """
        INSERT INTO routing_rules (id, merchant_pattern, line_item_id)
        VALUES (?, ?, ?)
        """,
        (new_id, merchant, target_line_item_id),
    )
    conn.execute(
        """
        INSERT INTO auto_promoted_rules_log
               (id, rule_id, merchant, line_item_id, source_transaction_ids, created_at)
        VALUES (?,  ?,       ?,        ?,            ?,                      ?)
        """,
        (
            log_id,
            new_id,
            merchant,
            target_line_item_id,
            json.dumps(source_transaction_ids),
            created_at,
        ),
    )
    conn.commit()

    return {
        "id": new_id,
        "merchant_pattern": merchant,
        "line_item_id": target_line_item_id,
    }
