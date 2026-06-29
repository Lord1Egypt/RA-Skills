"""Transaction categorizer backed by SQLite match rules and manual overrides.

Supports regex, exact, and contains matching with priority ordering.
Categories form a tree — matching a leaf automatically includes all ancestors.
"""

import re


class Categorizer:
    """Categorizes transactions using rules and manual overrides from a DatabaseHandler."""

    def __init__(self, db_handler):
        """
        Args:
            db_handler: A connected DatabaseHandler instance.
        """
        self.db = db_handler

    # ------------------------------------------------------------------ #
    #  Core matching
    # ------------------------------------------------------------------ #

    def _match_description(self, pattern: str, match_type: str, description: str) -> bool:
        """Try to match *pattern* against *description* using the given *match_type*."""
        if match_type == "regex":
            return re.search(pattern, description, re.IGNORECASE) is not None
        elif match_type == "exact":
            return pattern.lower() == description.lower()
        elif match_type == "contains":
            return pattern.lower() in description.lower()
        return False

    def categorize(self, transaction_id: int, recalculate: bool = True, rules: list | None = None, commit: bool = True) -> int | None:
        """Categorize a single transaction.

        Checks id_matches (manual override) first, then match_rules by priority.
        Updates the transaction's category_id and matched_rule_id.

        Returns the matched category_id, or None if no match.
        """
        cur = self.db.get_cursor()

        # 1. Check manual override — always wins, clears rule tracking
        cur.execute(
            "SELECT category_id FROM id_matches WHERE transaction_id = ?",
            (transaction_id,),
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE transactions SET category_id = ?, matched_rule_id = NULL WHERE id = ?",
                (row[0], transaction_id),
            )
            if commit:
                self.db.commit()
            # Auto-create external_transfer link for transfer-type categories
            self._link_external_transfer(transaction_id, row[0], recalculate=recalculate, commit=commit)
            return row[0]

        # 2. Get the transaction description and amount
        cur.execute(
            "SELECT description, amount FROM transactions WHERE id = ?",
            (transaction_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        description, amount = row[0], row[1]

        # 3. Apply match rules in priority order (highest priority first)
        rules_list = rules
        if rules_list is None:
            cur.execute(
                "SELECT id, category_id, pattern, match_type, amount_min, amount_max FROM match_rules "
                "WHERE enabled = 1 ORDER BY priority DESC, id ASC"
            )
            rules_list = cur.fetchall()

        for rule_id, category_id, pattern, match_type, amount_min, amount_max in rules_list:
            if not self._match_description(pattern, match_type, description):
                continue
            # Check amount constraints
            if amount_min is not None and amount < amount_min:
                continue
            if amount_max is not None and amount > amount_max:
                continue
            # Match found
            cur.execute(
                "UPDATE transactions SET category_id = ?, matched_rule_id = ? WHERE id = ?",
                (category_id, rule_id, transaction_id),
            )
            if commit:
                self.db.commit()

            # Auto-create external_transfer link for transfer-type categories
            self._link_external_transfer(transaction_id, category_id, recalculate=recalculate, commit=commit)

            return category_id

        # No match — clear any previous rule-based assignment
        cur.execute(
            "UPDATE transactions SET category_id = NULL, matched_rule_id = NULL WHERE id = ?",
            (transaction_id,),
        )
        if commit:
            self.db.commit()
        return None

    def _link_external_transfer(self, transaction_id: int, category_id: int, recalculate: bool = True, commit: bool = True) -> None:
        """Create an external_transfer link if the category is a transfer type.

        Only creates if not already linked.
        """
        cur = self.db.get_cursor()
        # Check category type
        cur.execute("SELECT category_type, associated_account_id FROM categories WHERE id = ?", (category_id,))
        row = cur.fetchone()
        if not row or row[0] != "transfer":
            return
        associated_account_id = row[1]
        # Check if already linked
        cur.execute(
            "SELECT id FROM transaction_links WHERE from_transaction_id = ? AND link_type = 'external_transfer'",
            (transaction_id,),
        )
        if cur.fetchone():
            return
        cur.execute(
            "INSERT INTO transaction_links (from_transaction_id, to_transaction_id, link_type, ratio, comment, to_account_id) "
            "VALUES (?, NULL, 'external_transfer', 1.0, 'auto-linked via categorize', ?)",
            (transaction_id, associated_account_id),
        )
        if commit:
            self.db.commit()
        if recalculate:
            self.db.recalculate_adjusted_amounts()

    def categorize_new(self) -> dict:
        """Categorize only uncategorized transactions (category_id IS NULL).

        Skips transactions that already have a category (rule or manual).

        Returns a dict with counts and detail lists: {'matched': int, 'unmatched': int, 'categorized_details': list}
        """
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT id FROM transactions WHERE category_id IS NULL"
        )
        uncategorized = [row[0] for row in cur.fetchall()]

        # Query rules once to avoid N+1 query problem
        cur.execute(
            "SELECT id, category_id, pattern, match_type, amount_min, amount_max FROM match_rules "
            "WHERE enabled = 1 ORDER BY priority DESC, id ASC"
        )
        rules = cur.fetchall()

        matched = 0
        for txn_id in uncategorized:
            result = self.categorize(txn_id, recalculate=False, rules=rules, commit=False)
            if result is not None:
                matched += 1

        if matched > 0:
            self.db.commit()
            self.db.recalculate_adjusted_amounts()

        categorized_details = []
        if uncategorized:
            placeholders = ",".join("?" for _ in uncategorized)
            cur.execute(
                f"SELECT t.id, t.date, t.description, t.amount, c.name, r.pattern, r.match_type, r.priority "
                f"FROM transactions t "
                f"LEFT JOIN categories c ON t.category_id = c.id "
                f"LEFT JOIN match_rules r ON t.matched_rule_id = r.id "
                f"WHERE t.id IN ({placeholders})",
                uncategorized
            )
            for row in cur.fetchall():
                t_id, t_date, t_desc, t_amount, cat_name, r_pat, r_type, r_prio = row
                is_manual = (cat_name is not None) and (r_pat is None)
                categorized_details.append({
                    "id": t_id,
                    "date": t_date,
                    "description": t_desc,
                    "amount": t_amount,
                    "category_name": cat_name,
                    "rule_pattern": r_pat,
                    "rule_type": r_type,
                    "rule_priority": r_prio,
                    "is_manual": is_manual,
                })

        return {
            "matched": matched,
            "unmatched": len(uncategorized) - matched,
            "categorized_details": categorized_details
        }

    def categorize_all(self) -> dict:
        """Re-categorize ALL transactions using current rules.

        Resets rule-based matches (matched_rule_id IS NOT NULL) first,
        then re-runs rules on every transaction. Manual overrides
        (id_matches) are preserved and always win.

        Returns a dict with counts: {'matched': int, 'unmatched': int}
        """
        cur = self.db.get_cursor()

        # Clear all rule-based category assignments
        cur.execute(
            "UPDATE transactions SET category_id = NULL, matched_rule_id = NULL "
            "WHERE id NOT IN (SELECT transaction_id FROM id_matches)"
        )

        # Now categorize everything
        cur.execute("SELECT id FROM transactions")
        all_ids = [row[0] for row in cur.fetchall()]

        # Query rules once to avoid N+1 query problem
        cur.execute(
            "SELECT id, category_id, pattern, match_type, amount_min, amount_max FROM match_rules "
            "WHERE enabled = 1 ORDER BY priority DESC, id ASC"
        )
        rules = cur.fetchall()

        matched = 0
        for txn_id in all_ids:
            result = self.categorize(txn_id, recalculate=False, rules=rules, commit=False)
            if result is not None:
                matched += 1

        self.db.commit()
        self.db.recalculate_adjusted_amounts()

        return {"matched": matched, "unmatched": len(all_ids) - matched}

    # ------------------------------------------------------------------ #
    #  Category hierarchy
    # ------------------------------------------------------------------ #

    def get_category_path(self, category_id: int) -> list[dict]:
        """Return the path from leaf to root for a category.

        Returns a list of dicts: [{'id': ..., 'name': ...}, ...]
        starting with the leaf category and ending with the root.
        """
        cur = self.db.get_cursor()
        path = []
        current_id = category_id
        visited = set()

        while current_id is not None and current_id not in visited:
            visited.add(current_id)
            cur.execute(
                "SELECT id, name, parent_id FROM categories WHERE id = ?",
                (current_id,),
            )
            row = cur.fetchone()
            if not row:
                break
            path.append({"id": row[0], "name": row[1]})
            current_id = row[2]

        return path

    def get_all_tags(self, transaction_id: int) -> list[str]:
        """Get all category names for a transaction, including ancestors.

        This replicates the old parent-propagation behavior: matching a
        child tag also includes all parent tags.
        """
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT category_id FROM transactions WHERE id = ?",
            (transaction_id,),
        )
        row = cur.fetchone()
        if not row or row[0] is None:
            return []

        path = self.get_category_path(row[0])
        return [cat["name"] for cat in path]

    # ------------------------------------------------------------------ #
    #  Rule management
    # ------------------------------------------------------------------ #

    def add_rule(
        self,
        category_id: int,
        pattern: str,
        match_type: str = "regex",
        priority: int = 0,
        amount_min: float | None = None,
        amount_max: float | None = None,
    ) -> int:
        """Add a new match rule and re-categorize all transactions.

        Returns the rule id.
        """
        cur = self.db.get_cursor()
        cur.execute(
            "INSERT INTO match_rules (category_id, pattern, match_type, priority, amount_min, amount_max) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (category_id, pattern, match_type, priority, amount_min, amount_max),
        )
        self.db.commit()
        self.categorize_all()
        return cur.lastrowid

    def remove_rule(self, rule_id: int) -> bool:
        """Remove a match rule and re-categorize all transactions.

        Returns True if a rule was deleted.
        """
        cur = self.db.get_cursor()
        cur.execute("DELETE FROM match_rules WHERE id = ?", (rule_id,))
        deleted = cur.rowcount > 0
        self.db.commit()
        if deleted:
            self.categorize_all()
        return deleted

    def list_rules(self) -> list[dict]:
        """Return all match rules ordered by priority."""
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT r.id, r.category_id, c.name, r.pattern, r.match_type, "
            "r.priority, r.enabled, r.amount_min, r.amount_max "
            "FROM match_rules r JOIN categories c ON r.category_id = c.id "
            "ORDER BY r.priority DESC, r.id ASC"
        )
        return [
            {
                "id": row[0],
                "category_id": row[1],
                "category_name": row[2],
                "pattern": row[3],
                "match_type": row[4],
                "priority": row[5],
                "enabled": bool(row[6]),
                "amount_min": row[7],
                "amount_max": row[8],
            }
            for row in cur.fetchall()
        ]

    def add_manual_match(self, transaction_id: int, category_id: int) -> int:
        """Add a one-off manual match (id_match). Returns the id_match id."""
        cur = self.db.get_cursor()
        cur.execute(
            "INSERT OR REPLACE INTO id_matches (transaction_id, category_id) VALUES (?, ?)",
            (transaction_id, category_id),
        )
        # Also update the transaction's category_id and clear rule tracking
        cur.execute(
            "UPDATE transactions SET category_id = ?, matched_rule_id = NULL WHERE id = ?",
            (category_id, transaction_id),
        )
        self.db.commit()
        # Auto-create external_transfer link for transfer-type categories
        self._link_external_transfer(transaction_id, category_id, recalculate=True)
        return cur.lastrowid

    def remove_manual_match(self, transaction_id: int) -> bool:
        """Remove a manual match (id_match). Returns True if it existed and was removed."""
        cur = self.db.get_cursor()
        # Check if manual match exists
        cur.execute(
            "SELECT category_id FROM id_matches WHERE transaction_id = ?",
            (transaction_id,),
        )
        row = cur.fetchone()
        if not row:
            return False

        # Delete from id_matches
        cur.execute(
            "DELETE FROM id_matches WHERE transaction_id = ?",
            (transaction_id,),
        )
        # Reset transaction's category_id and matched_rule_id
        cur.execute(
            "UPDATE transactions SET category_id = NULL, matched_rule_id = NULL WHERE id = ?",
            (transaction_id,),
        )
        # Delete auto-created external transfer links
        cur.execute(
            "DELETE FROM transaction_links WHERE from_transaction_id = ? AND link_type = 'external_transfer'",
            (transaction_id,),
        )
        self.db.commit()
        self.db.recalculate_adjusted_amounts()
        return True

    # ------------------------------------------------------------------ #
    #  Queries
    # ------------------------------------------------------------------ #

    def get_uncategorized(self) -> list[dict]:
        """Return all transactions without a category."""
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT t.id, t.date, t.description, t.amount, a.name "
            "FROM transactions t JOIN accounts a ON t.account_id = a.id "
            "WHERE t.category_id IS NULL "
            "ORDER BY t.date DESC"
        )
        return [
            {
                "id": row[0],
                "date": row[1],
                "description": row[2],
                "amount": row[3],
                "account": row[4],
            }
            for row in cur.fetchall()
        ]

    def get_uncategorized_grouped(self, non_zero: bool = False) -> list[dict]:
        """Group uncategorized transactions by description.

        Returns list of dicts with description, count, total, avg_amount,
        account_names, sorted by count descending.
        """
        sql = """
            SELECT t.description, COUNT(*) as cnt, ROUND(SUM(t.amount), 2) as total, 
                   ROUND(AVG(t.amount), 2) as avg_amount, GROUP_CONCAT(DISTINCT a.name) as accounts 
            FROM transactions t JOIN accounts a ON t.account_id = a.id 
            WHERE t.category_id IS NULL
        """
        if non_zero:
            sql += " AND (t.adjusted_amount IS NULL OR t.adjusted_amount != 0)"
        sql += " GROUP BY t.description ORDER BY cnt DESC"

        cur = self.db.get_cursor()
        cur.execute(sql)
        return [
            {
                "description": row[0],
                "count": row[1],
                "total": row[2],
                "avg_amount": row[3],
                "accounts": row[4],
            }
            for row in cur.fetchall()
        ]

    def preview_rule(
        self, pattern: str, match_type: str = "regex", limit: int = 20
    ) -> list[dict]:
        """Show transactions that would match a rule (dry run).

        Returns a list of matching transaction dicts.
        """
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT t.id, t.date, t.description, t.amount, a.name "
            "FROM transactions t JOIN accounts a ON t.account_id = a.id"
        )
        matches = []
        for row in cur.fetchall():
            txn = {
                "id": row[0],
                "date": row[1],
                "description": row[2],
                "amount": row[3],
                "account": row[4],
            }
            if self._match_description(pattern, match_type, txn["description"]):
                matches.append(txn)
                if len(matches) >= limit:
                    break
        return matches

    # ------------------------------------------------------------------ #
    #  Category management
    # ------------------------------------------------------------------ #

    def add_category(
        self, name: str, parent_id: int | None = None,
        category_type: str = "expense", description: str = None,
        associated_account_id: int | None = None
    ) -> int:
        """Add a new category. Returns the category id."""
        cur = self.db.get_cursor()
        cur.execute(
            "INSERT INTO categories (name, parent_id, category_type, description, associated_account_id) VALUES (?, ?, ?, ?, ?)",
            (name, parent_id, category_type, description, associated_account_id),
        )
        self.db.commit()
        return cur.lastrowid

    def get_category_by_name(self, name: str) -> dict | None:
        """Look up a category by name."""
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT id, name, parent_id, category_type, description, associated_account_id FROM categories WHERE name = ?",
            (name,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {"id": row[0], "name": row[1], "parent_id": row[2], "category_type": row[3], "description": row[4], "associated_account_id": row[5]}

    def list_categories(self) -> list[dict]:
        """Return all categories."""
        cur = self.db.get_cursor()
        cur.execute("SELECT id, name, parent_id, category_type, description, associated_account_id FROM categories ORDER BY name")
        return [
            {"id": row[0], "name": row[1], "parent_id": row[2], "category_type": row[3], "description": row[4], "associated_account_id": row[5]}
            for row in cur.fetchall()
        ]

    def get_category(self, category_id: int) -> dict | None:
        """Look up a single category by ID."""
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT id, name, parent_id, category_type, description, associated_account_id FROM categories WHERE id = ?",
            (category_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {"id": row[0], "name": row[1], "parent_id": row[2], "category_type": row[3], "description": row[4], "associated_account_id": row[5]}

    def get_parent(self, category_id: int) -> dict | None:
        """Return the parent category, or None if root."""
        cat = self.get_category(category_id)
        if not cat or cat["parent_id"] is None:
            return None
        return self.get_category(cat["parent_id"])

    def get_subtree(self, category_id: int) -> list[dict]:
        """Return all descendants of a category (flat list with depth).

        Returns list of dicts with 'id', 'name', 'parent_id', 'description', 'depth'.
        Depth 0 = direct children, 1 = grandchildren, etc.
        Does NOT include the category itself.
        """
        result = []
        cur = self.db.get_cursor()

        def _recurse(pid, depth):
            cur.execute(
                "SELECT id, name, parent_id, category_type, description, associated_account_id FROM categories WHERE parent_id = ?",
                (pid,),
            )
            for row in cur.fetchall():
                result.append({
                    "id": row[0], "name": row[1],
                    "parent_id": row[2], "category_type": row[3],
                    "description": row[4], "depth": depth,
                    "associated_account_id": row[5],
                })
                _recurse(row[0], depth + 1)

        _recurse(category_id, 0)
        return result

    def get_children(self, category_id: int) -> list[dict]:
        """Return direct children of a category."""
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT id, name, parent_id, description, associated_account_id FROM categories WHERE parent_id = ?",
            (category_id,),
        )
        return [
            {"id": row[0], "name": row[1], "parent_id": row[2], "description": row[3], "associated_account_id": row[4]}
            for row in cur.fetchall()
        ]

    def update_category(
        self,
        category_id: int,
        name: str | None = None,
        parent_id: int | None = ...,  # sentinel to distinguish None from unset
        category_type: str | None = None,
        description: str | None = ...,  # sentinel
        associated_account_id: int | None = ...,  # sentinel
    ) -> bool:
        """Update a category's name, parent, type, description, or associated account.

        Only updates fields that are explicitly passed. Use None to clear
        parent_id, description, or associated_account_id. Returns True if any change was made.
        """
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if parent_id is not ...:
            updates.append("parent_id = ?")
            params.append(parent_id)
        if category_type is not None:
            updates.append("category_type = ?")
            params.append(category_type)
        if description is not ...:
            updates.append("description = ?")
            params.append(description)
        if associated_account_id is not ...:
            updates.append("associated_account_id = ?")
            params.append(associated_account_id)

        if not updates:
            return False

        params.append(category_id)
        cur = self.db.get_cursor()
        cur.execute(
            f"UPDATE categories SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        self.db.commit()
        return cur.rowcount > 0

    def delete_category(
        self,
        category_id: int,
        reassign: int | None = None,
        force: bool = False,
    ) -> bool:
        """Delete a category.

        Args:
            category_id: The category to delete.
            reassign: Category ID to move children, rules, and manual matches to.
                Required if the category has children. When provided, rules and
                manual matches are also reassigned. If None, rules and manual
                matches are deleted.
            force: If True, allow deleting rules/matches without reassignment.
                Children are NEVER deleted — reassign is always required if
                children exist.

        Returns True if the category was deleted.

        Raises:
            ValueError: If children exist without reassign, or if there are
                rules/matches without reassign and force is False.
        """
        cur = self.db.get_cursor()

        # Check category exists
        cur.execute("SELECT id, parent_id FROM categories WHERE id = ?", (category_id,))
        cat_row = cur.fetchone()
        if not cat_row:
            return False

        # Check for children — always require reassign
        cur.execute("SELECT COUNT(*) FROM categories WHERE parent_id = ?", (category_id,))
        child_count = cur.fetchone()[0]
        if child_count > 0 and reassign is None:
            raise ValueError(
                f"Category {category_id} has {child_count} child(ren). "
                "reassign is required — children cannot be deleted or orphaned."
            )

        # Check for rules and manual matches
        cur.execute(
            "SELECT COUNT(*) FROM match_rules WHERE category_id = ?", (category_id,)
        )
        rule_count = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM id_matches WHERE category_id = ?", (category_id,)
        )
        match_count = cur.fetchone()[0]

        if (rule_count > 0 or match_count > 0) and reassign is None and not force:
            raise ValueError(
                f"Category {category_id} has {rule_count} rule(s) and "
                f"{match_count} manual match(es). Provide reassign or use force=True."
            )

        if reassign is not None:
            # Reassign children
            cur.execute(
                "UPDATE categories SET parent_id = ? WHERE parent_id = ?",
                (reassign, category_id),
            )
            # Reassign rules
            cur.execute(
                "UPDATE match_rules SET category_id = ? WHERE category_id = ?",
                (reassign, category_id),
            )
            # Reassign manual matches
            cur.execute(
                "UPDATE id_matches SET category_id = ? WHERE category_id = ?",
                (reassign, category_id),
            )
        else:
            # Delete rules (cascade handles match_rules via FK)
            cur.execute("DELETE FROM match_rules WHERE category_id = ?", (category_id,))
            # Delete manual matches
            cur.execute("DELETE FROM id_matches WHERE category_id = ?", (category_id,))

        # Delete the category itself (ON DELETE SET NULL handles transactions)
        cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.db.commit()

        # Re-categorize to reflect changes
        self.categorize_all()

        return True
