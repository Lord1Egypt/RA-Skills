"""Stats module: SQL views and query functions for financial-categorizer.

Creates views for dashboard and CLI consumption.
All views use adjusted_amount directly — ownership_ratio, transfers,
and reimbursements are already baked in.
"""

from datetime import date


class Stats:
    """Query financial stats from pre-computed views."""

    def __init__(self, db_handler):
        self.db = db_handler
        self._ensure_views()

    def _ensure_views(self):
        """Create or replace SQL views."""
        cur = self.db.get_cursor()

        cur.execute("DROP VIEW IF EXISTS v_effective_transactions")
        cur.execute("DROP VIEW IF EXISTS v_monthly_summary")
        cur.execute("DROP VIEW IF EXISTS v_category_monthly")
        cur.execute("DROP VIEW IF EXISTS v_daily_spending")
        cur.execute("DROP VIEW IF EXISTS v_cumulative_spending_monthly")
        cur.execute("DROP VIEW IF EXISTS v_daily_spending_moving_average")
        cur.execute("DROP VIEW IF EXISTS v_category_monthly_averages")
        cur.execute("DROP VIEW IF EXISTS v_salary_periods")
        cur.execute("DROP VIEW IF EXISTS v_salary_period_summary")
        cur.execute("DROP VIEW IF EXISTS v_category_salary_period")
        cur.execute("DROP VIEW IF EXISTS v_breakout_categories")
        cur.execute("DROP VIEW IF EXISTS v_uncategorized_groups")

        cur.execute("""
            CREATE VIEW v_effective_transactions AS
            SELECT t.id, t.date, t.description, t.amount, t.adjusted_amount,
                   t.account_id, t.category_id, t.status, t.comment,
                   a.name AS account_name, a.type AS account_type,
                   c.name AS category_name,
                   COALESCE(c.category_type, 'expense') AS category_type,
                   a.ownership_ratio,
                   (t.adjusted_amount / a.ownership_ratio) AS unsplit_amount,
                   t.amount AS raw_amount,
                   (t.amount * a.ownership_ratio) AS raw_split_amount
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.adjusted_amount IS NOT NULL AND a.type = 'tracked'
        """)

        cur.execute("""
            CREATE VIEW v_monthly_summary AS
            SELECT strftime('%Y-%m', date) AS month,
                   ROUND(SUM(CASE WHEN adjusted_amount > 0 AND category_type != 'transfer' THEN adjusted_amount ELSE 0 END), 2) AS total_income,
                   ROUND(SUM(CASE WHEN adjusted_amount < 0 AND category_type != 'transfer' THEN adjusted_amount ELSE 0 END), 2) AS total_expenses,
                   ROUND(SUM(CASE WHEN category_type != 'transfer' THEN adjusted_amount ELSE 0 END), 2) AS net,
                   ROUND(SUM(CASE WHEN unsplit_amount > 0 AND category_type != 'transfer' THEN unsplit_amount ELSE 0 END), 2) AS total_income_unsplit,
                   ROUND(SUM(CASE WHEN unsplit_amount < 0 AND category_type != 'transfer' THEN unsplit_amount ELSE 0 END), 2) AS total_expenses_unsplit,
                   ROUND(SUM(CASE WHEN category_type != 'transfer' THEN unsplit_amount ELSE 0 END), 2) AS net_unsplit,
                   ROUND(SUM(CASE WHEN raw_amount > 0 AND category_type != 'transfer' THEN raw_amount ELSE 0 END), 2) AS total_income_gross,
                   ROUND(SUM(CASE WHEN raw_amount < 0 AND category_type != 'transfer' THEN raw_amount ELSE 0 END), 2) AS total_expenses_gross,
                   ROUND(SUM(CASE WHEN category_type != 'transfer' THEN raw_amount ELSE 0 END), 2) AS net_gross,
                   ROUND(SUM(CASE WHEN raw_split_amount > 0 AND category_type != 'transfer' THEN raw_split_amount ELSE 0 END), 2) AS total_income_raw_split,
                   ROUND(SUM(CASE WHEN raw_split_amount < 0 AND category_type != 'transfer' THEN raw_split_amount ELSE 0 END), 2) AS total_expenses_raw_split,
                   ROUND(SUM(CASE WHEN category_type != 'transfer' THEN raw_split_amount ELSE 0 END), 2) AS net_raw_split
            FROM v_effective_transactions
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month
        """)

        cur.execute("""
            CREATE VIEW v_category_monthly AS
            SELECT COALESCE(c.name, 'Uncategorized') AS category_name,
                   t.category_id,
                   COALESCE(c.category_type, 'expense') AS category_type,
                   strftime('%Y-%m', t.date) AS month,
                   ROUND(SUM(t.adjusted_amount), 2) AS total,
                   ROUND(SUM(t.adjusted_amount / a.ownership_ratio), 2) AS total_unsplit,
                   ROUND(SUM(t.amount), 2) AS total_gross,
                   ROUND(SUM(t.amount * a.ownership_ratio), 2) AS total_raw_split,
                   COUNT(*) AS count
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.adjusted_amount IS NOT NULL AND a.type = 'tracked'
            GROUP BY strftime('%Y-%m', t.date), t.category_id
            ORDER BY month, category_name
        """)

        cur.execute("""
            CREATE VIEW v_daily_spending AS
            SELECT date, adjusted_amount, COALESCE(c.name, 'Uncategorized') AS category_name,
                   COALESCE(c.category_type, 'expense') AS category_type
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE adjusted_amount IS NOT NULL AND adjusted_amount < 0
              AND a.type = 'tracked'
            ORDER BY date
        """)

        cur.execute("""
            CREATE VIEW v_cumulative_spending_monthly AS
            WITH daily_spending AS (
                SELECT
                    date,
                    strftime('%Y-%m', date) AS month,
                    ROUND(SUM(adjusted_amount), 2) AS daily_amount
                FROM transactions t
                JOIN accounts a ON a.id = t.account_id
                LEFT JOIN categories c ON c.id = t.category_id
                WHERE adjusted_amount IS NOT NULL AND adjusted_amount < 0
                  AND (category_id IS NULL OR COALESCE(c.category_type, 'expense') != 'transfer')
                  AND a.type = 'tracked'
                GROUP BY date
            )
            SELECT
                date,
                month,
                daily_amount,
                ROUND(SUM(daily_amount) OVER (
                    PARTITION BY month
                    ORDER BY date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ), 2) AS cumulative_amount
            FROM daily_spending
        """)

        cur.execute("""
            CREATE VIEW v_daily_spending_moving_average AS
            WITH RECURSIVE date_range(date) AS (
                SELECT MIN(date) FROM transactions WHERE date IS NOT NULL
                UNION ALL
                SELECT date(date, '+1 day') FROM date_range WHERE date < (SELECT MAX(date) FROM transactions)
            ),
            daily_spending AS (
                SELECT
                    date,
                    SUM(adjusted_amount) AS daily_amount
                FROM transactions t
                JOIN accounts a ON a.id = t.account_id
                LEFT JOIN categories c ON c.id = t.category_id
                WHERE adjusted_amount IS NOT NULL AND adjusted_amount < 0
                  AND (category_id IS NULL OR COALESCE(c.category_type, 'expense') != 'transfer')
                  AND a.type = 'tracked'
                GROUP BY date
            )
            SELECT
                dr.date,
                COALESCE(ds.daily_amount, 0.0) AS daily_amount,
                ROUND(AVG(COALESCE(ds.daily_amount, 0.0)) OVER (
                    ORDER BY dr.date
                    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
                ), 2) AS moving_average
            FROM date_range dr
            LEFT JOIN daily_spending ds ON dr.date = ds.date
        """)

        cur.execute("""
            CREATE VIEW v_category_monthly_averages AS
            SELECT
                category_name,
                category_id,
                category_type,
                ROUND(AVG(total), 2) AS average_monthly_spending,
                ROUND(AVG(count), 1) AS average_monthly_count
            FROM v_category_monthly
            GROUP BY category_id
        """)

        cur.execute("""
            CREATE VIEW v_salary_periods AS
            WITH settings AS (
                SELECT 
                    COALESCE((SELECT value FROM metadata WHERE key = 'salary_period_mode'), 'fixed') AS mode,
                    COALESCE((SELECT CAST(value AS INTEGER) FROM metadata WHERE key = 'salary_period_fixed_day'), 25) AS fixed_day,
                    COALESCE((SELECT value FROM metadata WHERE key = 'salary_period_category_name'), 'Salary') AS salary_cat_name
            ),
            primary_salary_dates AS (
                SELECT date FROM transactions WHERE recurring_id IN (
                    SELECT id FROM recurring_payments WHERE name = 'Salary' OR category_id = (
                        SELECT id FROM categories WHERE name = (SELECT salary_cat_name FROM settings)
                    )
                )
                UNION
                SELECT date
                FROM (
                    SELECT 
                        t.date,
                        ROW_NUMBER() OVER (
                            PARTITION BY strftime('%Y-%m', t.date) 
                            ORDER BY t.amount DESC, t.date ASC
                        ) AS rank
                    FROM transactions t
                    JOIN categories c ON t.category_id = c.id
                    JOIN accounts a ON t.account_id = a.id
                    WHERE c.name = (SELECT salary_cat_name FROM settings)
                      AND t.amount > 0
                      AND a.type = 'tracked'
                )
                WHERE rank = 1 AND NOT EXISTS (
                    SELECT 1 FROM transactions WHERE recurring_id IN (
                        SELECT id FROM recurring_payments WHERE name = 'Salary' OR category_id = (
                            SELECT id FROM categories WHERE name = (SELECT salary_cat_name FROM settings)
                        )
                    )
                )
            )
            SELECT 
                t.id AS transaction_id,
                t.date,
                CASE 
                    WHEN (SELECT mode FROM settings) = 'salary' THEN
                        strftime('%Y-%m', COALESCE(
                            (SELECT MAX(s.date) FROM primary_salary_dates s WHERE s.date <= t.date),
                            t.date
                        ))
                    ELSE
                        CASE 
                            WHEN CAST(strftime('%d', t.date) AS INTEGER) >= (SELECT fixed_day FROM settings)
                                THEN strftime('%Y-%m', date(t.date, 'start of month', '+1 month'))
                            ELSE strftime('%Y-%m', t.date)
                        END
                END AS period
            FROM transactions t
        """)


        cur.execute("""
            CREATE VIEW v_salary_period_summary AS
            WITH txn_with_period AS (
                SELECT
                    t.adjusted_amount,
                    (t.adjusted_amount / a.ownership_ratio) AS unsplit_amount,
                    t.amount AS raw_amount,
                    (t.amount * a.ownership_ratio) AS raw_split_amount,
                    COALESCE(c.category_type, 'expense') AS category_type,
                    p.period
                FROM transactions t
                JOIN v_salary_periods p ON t.id = p.transaction_id
                JOIN accounts a ON a.id = t.account_id
                LEFT JOIN categories c ON c.id = t.category_id
                WHERE t.adjusted_amount IS NOT NULL 
                  AND COALESCE(c.category_type, 'expense') != 'transfer'
                  AND a.type = 'tracked'
            )
            SELECT
                period,
                ROUND(SUM(CASE WHEN adjusted_amount > 0 THEN adjusted_amount ELSE 0 END), 2) AS total_income,
                ROUND(SUM(CASE WHEN adjusted_amount < 0 THEN adjusted_amount ELSE 0 END), 2) AS total_expenses,
                ROUND(SUM(adjusted_amount), 2) AS net,
                ROUND(SUM(CASE WHEN unsplit_amount > 0 THEN unsplit_amount ELSE 0 END), 2) AS total_income_unsplit,
                ROUND(SUM(CASE WHEN unsplit_amount < 0 THEN unsplit_amount ELSE 0 END), 2) AS total_expenses_unsplit,
                ROUND(SUM(unsplit_amount), 2) AS net_unsplit,
                ROUND(SUM(CASE WHEN raw_amount > 0 THEN raw_amount ELSE 0 END), 2) AS total_income_gross,
                ROUND(SUM(CASE WHEN raw_amount < 0 THEN raw_amount ELSE 0 END), 2) AS total_expenses_gross,
                ROUND(SUM(raw_amount), 2) AS net_gross,
                ROUND(SUM(CASE WHEN raw_split_amount > 0 THEN raw_split_amount ELSE 0 END), 2) AS total_income_raw_split,
                ROUND(SUM(CASE WHEN raw_split_amount < 0 THEN raw_split_amount ELSE 0 END), 2) AS total_expenses_raw_split,
                ROUND(SUM(raw_split_amount), 2) AS net_raw_split
            FROM txn_with_period
            GROUP BY period
            ORDER BY period
        """)

        cur.execute("""
            CREATE VIEW v_category_salary_period AS
            SELECT COALESCE(c.name, 'Uncategorized') AS category_name,
                   t.category_id,
                   COALESCE(c.category_type, 'expense') AS category_type,
                   p.period AS month,
                   ROUND(SUM(t.adjusted_amount), 2) AS total,
                   ROUND(SUM(t.adjusted_amount / a.ownership_ratio), 2) AS total_unsplit,
                   ROUND(SUM(t.amount), 2) AS total_gross,
                   ROUND(SUM(t.amount * a.ownership_ratio), 2) AS total_raw_split,
                   COUNT(*) AS count
            FROM transactions t
            JOIN v_salary_periods p ON t.id = p.transaction_id
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.adjusted_amount IS NOT NULL AND a.type = 'tracked'
            GROUP BY p.period, t.category_id
            ORDER BY month, category_name
        """)

        cur.execute("""
            CREATE VIEW v_breakout_categories AS
            WITH breakout_mapping AS (
                SELECT id,
                       CASE
                           WHEN id IN (4, 50) THEN 'Groceries'
                           WHEN id = 6 THEN 'Loans'
                           WHEN id IN (7, 8, 48) THEN 'Restaurants'
                           WHEN id IN (14, 31) THEN 'Housing'
                           WHEN id IN (26, 27, 28, 29, 52) THEN 'Car'
                           WHEN id IN (12, 15, 35, 41) THEN 'Shopping'
                           WHEN id IN (17, 19, 23, 24, 25, 42, 43, 44, 49) THEN 'Leisure'
                           WHEN id IN (5, 11, 13, 22, 40, 45, 46, 47) THEN 'Household Other'
                           WHEN id IN (10, 16, 30, 36, 37, 38, 39, 51) THEN 'Other'
                           ELSE NULL
                       END AS display_name
                FROM categories
            )
            SELECT
                COALESCE(bm.display_name, 'Uncategorized') AS display_name,
                CASE
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Groceries' THEN '4,50'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Loans' THEN '6'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Restaurants' THEN '7,8,48'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Housing' THEN '14,31'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Car' THEN '26,27,28,29,52'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Shopping' THEN '12,15,35,41'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Leisure' THEN '17,19,23,24,25,42,43,44,49'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Household Other' THEN '5,11,13,22,40,45,46,47'
                    WHEN COALESCE(bm.display_name, 'Uncategorized') = 'Other' THEN '10,16,30,36,37,38,39,51'
                    ELSE ''
                END AS category_ids,
                strftime('%Y-%m', t.date) AS month,
                ROUND(SUM(t.adjusted_amount), 2) AS total
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN breakout_mapping bm ON t.category_id = bm.id
            WHERE t.adjusted_amount IS NOT NULL 
              AND t.adjusted_amount < 0
              AND a.type = 'tracked'
              AND (t.category_id IS NULL OR t.category_id NOT IN (SELECT id FROM categories WHERE category_type = 'transfer'))
            GROUP BY COALESCE(bm.display_name, 'Uncategorized'), month
        """)

        cur.execute("""
            CREATE VIEW v_uncategorized_groups AS
            WITH cleaned_txns AS (
                SELECT
                    t.id,
                    t.date,
                    t.amount,
                    t.description AS latest_full_text,
                    a.name AS account_name,
                    CASE
                        WHEN t.description LIKE 'Swish betalning %' THEN TRIM(SUBSTR(t.description, 16))
                        WHEN t.description LIKE 'Swish inbetalning %' THEN TRIM(SUBSTR(t.description, 18))
                        WHEN (t.description LIKE 'Kortk_p %' OR t.description LIKE 'Kortköp %') 
                             THEN TRIM(SUBSTR(t.description, 16))
                        ELSE t.description
                    END AS group_key
                FROM transactions t
                JOIN accounts a ON a.id = t.account_id
                WHERE t.category_id IS NULL AND a.type = 'tracked'
                  AND (t.adjusted_amount IS NULL OR t.adjusted_amount != 0)
            ),
            grouped_txns AS (
                SELECT
                    group_key,
                    COUNT(*) AS match_count,
                    ROUND(SUM(amount), 2) AS total_amount,
                    MAX(date) AS latest_date
                FROM cleaned_txns
                GROUP BY group_key
            )
            SELECT
                g.group_key,
                g.match_count,
                g.total_amount,
                g.latest_date,
                (
                    SELECT c.amount
                    FROM cleaned_txns c
                    WHERE c.group_key = g.group_key AND c.date = g.latest_date
                    LIMIT 1
                ) AS latest_amount,
                (
                    SELECT c.latest_full_text
                    FROM cleaned_txns c
                    WHERE c.group_key = g.group_key AND c.date = g.latest_date
                    LIMIT 1
                ) AS latest_full_text,
                (
                    SELECT group_concat(DISTINCT c.account_name)
                    FROM cleaned_txns c
                    WHERE c.group_key = g.group_key
                ) AS account_names
            FROM grouped_txns g
        """)

        self.db.commit()

    def monthly_summary(self, month: str = None, period_type: str = "calendar",
                        unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> list[dict]:
        """Get monthly income/expenses/net.

        Args:
            month: Optional filter 'YYYY-MM'. If None, returns all months.
            period_type: 'calendar' or 'salary'.
            unsplit: If True, returns unsplit (household net) values.
            gross: If True, returns gross (household raw) values.
            raw_split: If True, returns raw-split (ownership split, no reimbursement adjustments) values.

        Returns list of dicts with month, total_income, total_expenses, net.
        """
        cur = self.db.get_cursor()
        view = "v_salary_period_summary" if period_type == "salary" else "v_monthly_summary"
        col = "period" if period_type == "salary" else "month"
        suffix = ""
        if gross:
            suffix = "_gross"
        elif unsplit:
            suffix = "_unsplit"
        elif raw_split:
            suffix = "_raw_split"

        if month:
            cur.execute(
                f"SELECT {col}, total_income{suffix}, total_expenses{suffix}, net{suffix} "
                f"FROM {view} WHERE {col} = ?",
                (month,),
            )
        else:
            cur.execute(
                f"SELECT {col}, total_income{suffix}, total_expenses{suffix}, net{suffix} "
                f"FROM {view}"
            )
        return [
            {"month": r[0], "total_income": r[1], "total_expenses": r[2], "net": r[3]}
            for r in cur.fetchall()
        ]

    def cash_flow_summary(self, month: str = None, period_type: str = "default",
                          unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> list[dict]:
        """Get monthly cash flow summary (Operating, Transfers, Net).

        Args:
            month: Optional filter 'YYYY-MM'. If None, returns all months.
            period_type: 'default', 'calendar', or 'salary'.
            unsplit: If True, returns unsplit (household net) values.
            gross: If True, returns gross (household raw) values.
            raw_split: If True, returns raw-split (ownership split, no reimbursement adjustments) values.

        Returns:
            list of dicts with:
                - period: "YYYY-MM"
                - operating: Operating cash flow
                - transfers: Transfers cash flow
                - net: operating + transfers
        """
        if period_type == "default":
            mode = self.db.get_metadata("salary_period_mode", "fixed")
            period_type = "salary" if mode in ("fixed", "salary") else "calendar"

        cur = self.db.get_cursor()

        # Determine how period is calculated
        if period_type == "salary":
            period_expr = "p.period"
            join_periods = "JOIN v_salary_periods p ON t.id = p.transaction_id"
        else:
            period_expr = "strftime('%Y-%m', t.date)"
            join_periods = ""

        if gross:
            operating_col = "t.amount"
            transfer_col = "t.amount * COALESCE(tl.ratio, 1.0)"
        elif unsplit:
            operating_col = "(t.adjusted_amount / t.ownership_ratio)"
            transfer_col = "t.amount * COALESCE(tl.ratio, 1.0)"
        elif raw_split:
            operating_col = "(t.amount * t.ownership_ratio)"
            transfer_col = "t.amount * t.ownership_ratio * COALESCE(tl.ratio, 1.0)"
        else:
            operating_col = "t.adjusted_amount"
            transfer_col = "t.amount * t.ownership_ratio * COALESCE(tl.ratio, 1.0)"

        query = f"""
            WITH txn_with_period AS (
                SELECT
                    t.id,
                    t.amount,
                    t.adjusted_amount,
                    a.ownership_ratio,
                    COALESCE(c.category_type, 'expense') AS category_type,
                    c.associated_account_id,
                    {period_expr} AS period
                FROM transactions t
                JOIN accounts a ON t.account_id = a.id
                LEFT JOIN categories c ON c.id = t.category_id
                {join_periods}
                WHERE a.type = 'tracked'
            ),
            resolved_transfers AS (
                SELECT
                    t.id,
                    t.period,
                    t.category_type,
                    {operating_col} AS op_amount,
                    {transfer_col} AS tr_amount,
                    COALESCE(tl.to_account_id, t.associated_account_id) AS target_account_id
                FROM txn_with_period t
                LEFT JOIN transaction_links tl ON tl.from_transaction_id = t.id 
                    AND tl.link_type IN ('internal_transfer', 'external_transfer')
            ),
            transfers_with_neutrality AS (
                SELECT
                    t.period,
                    t.category_type,
                    t.op_amount,
                    t.tr_amount,
                    CASE
                        WHEN t.id IN (SELECT from_transaction_id FROM transaction_links WHERE link_type = 'internal_transfer') THEN 1
                        WHEN t.id IN (SELECT to_transaction_id FROM transaction_links WHERE link_type = 'internal_transfer') THEN 1
                        WHEN t.target_account_id IS NOT NULL AND a_target.type = 'tracked' THEN 1
                        WHEN t.target_account_id IS NOT NULL AND a_target.type = 'external' AND a_target.cash_neutral = 1 THEN 1
                        ELSE 0
                    END AS is_neutral
                FROM resolved_transfers t
                LEFT JOIN accounts a_target ON t.target_account_id = a_target.id
            )
            SELECT
                period,
                ROUND(SUM(CASE WHEN category_type != 'transfer' THEN op_amount ELSE 0.0 END), 2) AS operating,
                ROUND(SUM(CASE WHEN category_type = 'transfer' AND is_neutral = 0 THEN tr_amount ELSE 0.0 END), 2) AS transfers,
                ROUND(SUM(CASE WHEN category_type != 'transfer' THEN op_amount ELSE 0.0 END) + 
                      SUM(CASE WHEN category_type = 'transfer' AND is_neutral = 0 THEN tr_amount ELSE 0.0 END), 2) AS net
            FROM transfers_with_neutrality
            {"WHERE period = ?" if month else ""}
            GROUP BY period
            ORDER BY period DESC
        """

        if month:
            cur.execute(query, (month,))
        else:
            cur.execute(query)

        return [
            {
                "period": r[0],
                "operating": r[1] or 0.0,
                "transfers": r[2] or 0.0,
                "net": r[3] or 0.0,
            }
            for r in cur.fetchall()
        ]

    def category_total(self, category_id: int, month: str = None,
                       date_from: date = None, date_to: date = None,
                       period_type: str = "calendar",
                       unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> dict:
        """Get total for a category including all children.

        Args:
            category_id: The category to sum (includes subcategories).
            month: Optional 'YYYY-MM' filter.
            date_from/date_to: Optional date range.
            period_type: 'calendar' or 'salary'.
            unsplit: If True, returns unsplit total.
            gross: If True, returns gross total.

        Returns dict with category_id, total, count.
        """
        # Gather all category IDs (self + subtree)
        from financial_categorizer.categorizer import Categorizer
        cat = Categorizer.__new__(Categorizer)
        cat.db = self.db

        ids = [category_id]
        subtree = cat.get_subtree(category_id)
        ids.extend(c["id"] for c in subtree)

        placeholders = ",".join("?" * len(ids))
        conditions = [f"t.category_id IN ({placeholders})"]
        params = list(ids)

        from_clause = "v_effective_transactions t"
        if period_type == "salary" and month:
            from_clause += " JOIN v_salary_periods p ON t.id = p.transaction_id"
            conditions.append("p.period = ?")
            params.append(month)
        elif month:
            conditions.append("strftime('%Y-%m', t.date) = ?")
            params.append(month)

        if date_from:
            conditions.append("t.date >= ?")
            params.append(date_from)
        if date_to:
            conditions.append("t.date <= ?")
            params.append(date_to)

        where = " AND ".join(conditions)

        amount_col = "t.adjusted_amount"
        if gross:
            amount_col = "t.raw_amount"
        elif unsplit:
            amount_col = "t.unsplit_amount"
        elif raw_split:
            amount_col = "t.raw_split_amount"

        cur = self.db.get_cursor()
        cur.execute(
            f"SELECT ROUND(SUM({amount_col}), 2), COUNT(*) "
            f"FROM {from_clause} WHERE {where}",
            params,
        )
        row = cur.fetchone()
        return {
            "category_id": category_id,
            "total": row[0] if row[0] else 0.0,
            "count": row[1],
        }

    def top_spending(self, month: str = None, limit: int = 10,
                     period_type: str = "calendar",
                     unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> list[dict]:
        """Top spending categories.

        Args:
            month: Optional 'YYYY-MM' filter.
            limit: Max categories to return.
            period_type: 'calendar' or 'salary'.
            unsplit: If True, returns unsplit totals.
            gross: If True, returns gross totals.

        Returns list of dicts sorted by total spending (most negative first).
        """
        cur = self.db.get_cursor()
        params = []
        view = "v_category_salary_period" if period_type == "salary" else "v_category_monthly"
        col = "month"
        total_col = "total"
        if gross:
            total_col = "total_gross"
        elif unsplit:
            total_col = "total_unsplit"
        elif raw_split:
            total_col = "total_raw_split"

        conditions = [f"{total_col} < 0"]
        if month:
            conditions.append(f"{col} = ?")
            params.append(month)

        where = " AND ".join(conditions)
        cur.execute(
            f"SELECT category_name, category_id, {col}, {total_col}, count "
            f"FROM {view} WHERE {where} "
            f"ORDER BY {total_col} ASC LIMIT ?",
            params + [limit],
        )
        return [
            {"category_name": r[0], "category_id": r[1], "month": r[2],
             "total": r[3], "count": r[4]}
            for r in cur.fetchall()
        ]

    def trend(self, category_id: int, date_from: date = None,
              date_to: date = None, period_type: str = "calendar",
              unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> list[dict]:
        """Monthly breakdown for a category (including children).

        Returns list of dicts with month, total, count.
        """
        from financial_categorizer.categorizer import Categorizer
        cat = Categorizer.__new__(Categorizer)
        cat.db = self.db

        ids = [category_id]
        subtree = cat.get_subtree(category_id)
        ids.extend(c["id"] for c in subtree)

        placeholders = ",".join("?" * len(ids))
        conditions = [f"category_id IN ({placeholders})"]
        params = list(ids)

        view = "v_category_salary_period" if period_type == "salary" else "v_category_monthly"
        col = "month"

        if date_from:
            conditions.append(f"{col} >= strftime('%Y-%m', ?)")
            params.append(date_from)
        if date_to:
            conditions.append(f"{col} <= strftime('%Y-%m', ?)")
            params.append(date_to)

        where = " AND ".join(conditions)
        total_col = "total"
        if gross:
            total_col = "total_gross"
        elif unsplit:
            total_col = "total_unsplit"
        elif raw_split:
            total_col = "total_raw_split"

        cur = self.db.get_cursor()
        cur.execute(
            f"SELECT {col}, ROUND(SUM({total_col}), 2), SUM(count) "
            f"FROM {view} WHERE {where} "
            f"GROUP BY {col} ORDER BY {col}",
            params,
        )
        return [
            {"month": r[0], "total": r[1] if r[1] else 0.0, "count": r[2]}
            for r in cur.fetchall()
        ]

    def compare(self, period: str = None, period_type: str = "calendar",
                unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> list[dict]:
        """Month-over-month comparison.

        Args:
            period: 'YYYY-MM' for calendar or 'YYYY-MM' for salary period starting that month.
                    If None, compares last two periods.
            period_type: 'calendar' (1st-last) or 'salary' (25th-24th).
            unsplit: If True, returns unsplit comparison.
            gross: If True, returns gross comparison.
            raw_split: If True, returns raw-split (ownership split, no reimbursement adjustments) comparison.

        Returns list of dicts with period, total_income, total_expenses, net,
                prev_ prefixed fields, and delta fields.
        """
        cur = self.db.get_cursor()

        if period_type == "salary":
            # Salary period: 25th of previous month to 24th of current month
            # Period '2026-03' means Feb 25 - Mar 24
            rows = self._salary_period_summary(cur, unsplit=unsplit, gross=gross, raw_split=raw_split)
        else:
            rows = self._calendar_month_summary(cur, unsplit=unsplit, gross=gross, raw_split=raw_split)

        if len(rows) < 2 and period is None:
            # Not enough data for comparison, just return what we have
            return rows

        # Find the target and previous periods
        if period:
            target = None
            for i, r in enumerate(rows):
                if r["period"] == period:
                    target = r
                    prev = rows[i - 1] if i > 0 else None
                    break
            if not target:
                return []
        else:
            target = rows[-1]
            prev = rows[-2]

        result = {
            "period": target["period"],
            "total_income": target["total_income"],
            "total_expenses": target["total_expenses"],
            "net": target["net"],
        }

        if prev:
            result["prev_period"] = prev["period"]
            result["prev_total_income"] = prev["total_income"]
            result["prev_total_expenses"] = prev["total_expenses"]
            result["prev_net"] = prev["net"]
            result["income_delta"] = round(target["total_income"] - prev["total_income"], 2)
            result["expense_delta"] = round(target["total_expenses"] - prev["total_expenses"], 2)
            result["net_delta"] = round(target["net"] - prev["net"], 2)
            # Percentage changes (handle zero prev)
            result["income_pct"] = round((result["income_delta"] / abs(prev["total_income"])) * 100, 1) if prev["total_income"] else None
            result["expense_pct"] = round((result["expense_delta"] / abs(prev["total_expenses"])) * 100, 1) if prev["total_expenses"] else None
            result["net_pct"] = round((result["net_delta"] / abs(prev["net"])) * 100, 1) if prev["net"] else None

        return result

    def _calendar_month_summary(self, cur, unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> list[dict]:
        suffix = ""
        if gross:
            suffix = "_gross"
        elif unsplit:
            suffix = "_unsplit"
        elif raw_split:
            suffix = "_raw_split"
        cur.execute(
            f"SELECT month, total_income{suffix}, total_expenses{suffix}, net{suffix} "
            f"FROM v_monthly_summary ORDER BY month"
        )
        return [
            {"period": r[0], "total_income": r[1] or 0.0,
             "total_expenses": r[2] or 0.0, "net": r[3] or 0.0}
            for r in cur.fetchall()
        ]

    def _salary_period_summary(self, cur, unsplit: bool = False, gross: bool = False, raw_split: bool = False) -> list[dict]:
        """Aggregate by salary period (25th to 24th of next month).
        Period label is the month of the 24th, e.g. '2026-03' = Feb 25 - Mar 24.
        """
        suffix = ""
        if gross:
            suffix = "_gross"
        elif unsplit:
            suffix = "_unsplit"
        elif raw_split:
            suffix = "_raw_split"
        cur.execute(
            f"SELECT period, total_income{suffix}, total_expenses{suffix}, net{suffix} "
            f"FROM v_salary_period_summary ORDER BY period"
        )
        return [
            {"period": r[0], "total_income": r[1] or 0.0,
             "total_expenses": r[2] or 0.0, "net": r[3] or 0.0}
            for r in cur.fetchall()
        ]

    def external_transfers_summary(
        self, month: str = None, period_type: str = "calendar",
        unsplit: bool = False, gross: bool = False, raw_split: bool = False
    ) -> list[dict]:
        """Calculate net capital transfers to external accounts.

        Returns a list of dicts:
        [
            {
                "period": "YYYY-MM",
                "account_id": int,
                "account_name": str,
                "net_transferred": float
            },
            ...
        ]
        """
        cur = self.db.get_cursor()

        # Determine how period is calculated
        if period_type == "salary":
            period_expr = "p.period"
            join_periods = "JOIN v_salary_periods p ON t.id = p.transaction_id"
        else:
            period_expr = "strftime('%Y-%m', t.date)"
            join_periods = ""

        # Determine target net amount expression based on flags
        if gross or unsplit or raw_split:
            amount_expr = "-1.0 * t.amount * COALESCE(tl.ratio, 1.0)"
        else:
            amount_expr = "-1.0 * t.amount * a_orig.ownership_ratio * COALESCE(tl.ratio, 1.0)"

        if month:
            query = f"""
                WITH resolved_transfers AS (
                    SELECT
                        {period_expr} AS period,
                        COALESCE(tl.to_account_id, c.associated_account_id) AS target_account_id,
                        {amount_expr} AS net_amount
                    FROM transactions t
                    JOIN accounts a_orig ON t.account_id = a_orig.id
                    {join_periods}
                    LEFT JOIN transaction_links tl ON tl.from_transaction_id = t.id AND tl.link_type = 'external_transfer'
                    LEFT JOIN categories c ON t.category_id = c.id
                    WHERE (tl.id IS NOT NULL OR c.associated_account_id IS NOT NULL)
                )
                SELECT
                    r.period,
                    r.target_account_id,
                    COALESCE(a_target.name, 'Unspecified External Account') AS target_account_name,
                    ROUND(SUM(r.net_amount), 2) AS net_transferred
                FROM resolved_transfers r
                LEFT JOIN accounts a_target ON r.target_account_id = a_target.id
                WHERE r.period = ?
                GROUP BY r.period, r.target_account_id
                ORDER BY r.period DESC, target_account_name ASC
            """
            cur.execute(query, (month,))
        else:
            query = f"""
                WITH resolved_transfers AS (
                    SELECT
                        {period_expr} AS period,
                        COALESCE(tl.to_account_id, c.associated_account_id) AS target_account_id,
                        {amount_expr} AS net_amount
                    FROM transactions t
                    JOIN accounts a_orig ON t.account_id = a_orig.id
                    {join_periods}
                    LEFT JOIN transaction_links tl ON tl.from_transaction_id = t.id AND tl.link_type = 'external_transfer'
                    LEFT JOIN categories c ON t.category_id = c.id
                    WHERE (tl.id IS NOT NULL OR c.associated_account_id IS NOT NULL)
                )
                SELECT
                    r.period,
                    r.target_account_id,
                    COALESCE(a_target.name, 'Unspecified External Account') AS target_account_name,
                    ROUND(SUM(r.net_amount), 2) AS net_transferred
                FROM resolved_transfers r
                LEFT JOIN accounts a_target ON r.target_account_id = a_target.id
                GROUP BY r.period, r.target_account_id
                ORDER BY r.period DESC, target_account_name ASC
            """
            cur.execute(query)

        return [
            {
                "period": row[0],
                "account_id": row[1],
                "account_name": row[2],
                "net_transferred": row[3] or 0.0,
            }
            for row in cur.fetchall()
        ]

    def get_period_boundaries(self, as_of_date):
        """Retrieve start date, end date, and period name for the period containing as_of_date.

        Returns (start_date, next_payday_date, period_name)
        """
        from datetime import datetime, timedelta, date
        from financial_categorizer.recurring import RecurringManager, _to_date
        
        cur = self.db.get_cursor()
        cur.execute("SELECT key, value FROM metadata WHERE key LIKE 'salary_period_%'")
        meta = dict(cur.fetchall())
        mode = meta.get("salary_period_mode", "fixed")
        fixed_day = int(meta.get("salary_period_fixed_day", "25"))
        salary_cat_name = meta.get("salary_period_category_name", "Salary")

        as_of_date = _to_date(as_of_date)

        if mode == "salary":
            cur.execute("""
                WITH settings AS (
                    SELECT 
                        COALESCE((SELECT value FROM metadata WHERE key = 'salary_period_mode'), 'fixed') AS mode,
                        COALESCE((SELECT CAST(value AS INTEGER) FROM metadata WHERE key = 'salary_period_fixed_day'), 25) AS fixed_day,
                        COALESCE((SELECT value FROM metadata WHERE key = 'salary_period_category_name'), 'Salary') AS salary_cat_name
                ),
                primary_salary_dates AS (
                    SELECT date FROM transactions WHERE recurring_id IN (
                        SELECT id FROM recurring_payments WHERE name = 'Salary' OR category_id = (
                            SELECT id FROM categories WHERE name = (SELECT salary_cat_name FROM settings)
                        )
                    )
                    UNION
                    SELECT date
                    FROM (
                        SELECT 
                            t.date,
                            ROW_NUMBER() OVER (
                                PARTITION BY strftime('%Y-%m', t.date) 
                                ORDER BY t.amount DESC, t.date ASC
                            ) AS rank
                        FROM transactions t
                        JOIN categories c ON t.category_id = c.id
                        JOIN accounts a ON t.account_id = a.id
                        WHERE c.name = (SELECT salary_cat_name FROM settings)
                          AND t.amount > 0
                          AND a.type = 'tracked'
                    )
                    WHERE rank = 1 AND NOT EXISTS (
                        SELECT 1 FROM transactions WHERE recurring_id IN (
                            SELECT id FROM recurring_payments WHERE name = 'Salary' OR category_id = (
                                SELECT id FROM categories WHERE name = (SELECT salary_cat_name FROM settings)
                            )
                        )
                    )
                )
                SELECT date FROM primary_salary_dates ORDER BY date ASC
            """)
            paydays = [_to_date(row[0]) for row in cur.fetchall()]
            
            past_paydays = [d for d in paydays if d <= as_of_date]
            if past_paydays:
                period_start = max(past_paydays)
            else:
                # Default to 1st of month
                period_start = date(as_of_date.year, as_of_date.month, 1)

            future_paydays = [d for d in paydays if d > period_start]
            if future_paydays:
                next_payday = min(future_paydays)
            else:
                # Project exactly 1 month
                try:
                    delta_y = (period_start.month + 1 - 1) // 12
                    next_m = (period_start.month + 1 - 1) % 12 + 1
                    next_y = period_start.year + delta_y
                    last_day = RecurringManager.get_last_day_of_month(next_y, next_m)
                    next_payday = date(next_y, next_m, min(period_start.day, last_day.day))
                except Exception:
                    next_payday = period_start + timedelta(days=30)
            
            period_name = period_start.strftime("%Y-%m")
            return period_start, next_payday, period_name
        else:
            # Fixed day mode
            from financial_categorizer.recurring import RecurringManager
            if as_of_date.day >= fixed_day:
                period_start = date(as_of_date.year, as_of_date.month, fixed_day)
                delta_y = (as_of_date.month + 1 - 1) // 12
                next_m = (as_of_date.month + 1 - 1) % 12 + 1
                next_y = as_of_date.year + delta_y
                last_day = RecurringManager.get_last_day_of_month(next_y, next_m)
                next_payday = date(next_y, next_m, min(fixed_day, last_day.day))
                period_name = next_payday.strftime("%Y-%m")
            else:
                prev_y = as_of_date.year if as_of_date.month > 1 else as_of_date.year - 1
                prev_m = as_of_date.month - 1 if as_of_date.month > 1 else 12
                last_day_prev = RecurringManager.get_last_day_of_month(prev_y, prev_m)
                period_start = date(prev_y, prev_m, min(fixed_day, last_day_prev.day))
                
                last_day_curr = RecurringManager.get_last_day_of_month(as_of_date.year, as_of_date.month)
                next_payday = date(as_of_date.year, as_of_date.month, min(fixed_day, last_day_curr.day))
                period_name = next_payday.strftime("%Y-%m")
                
            return period_start, next_payday, period_name

    def get_historical_daily_spend(self, as_of_date, window_days=30, level=1):
        """Calculate average daily spending over window_days, grouped by category rollup level."""
        from datetime import timedelta
        from financial_categorizer.recurring import _to_date
        
        cur = self.db.get_cursor()
        as_of_date = _to_date(as_of_date)
        start_window = as_of_date - timedelta(days=window_days - 1)
        
        # Load categories to map hierarchy
        cur.execute("SELECT id, name, parent_id FROM categories")
        cat_map = {row[0]: {"name": row[1], "parent_id": row[2]} for row in cur.fetchall()}
        
        def get_category_rollup_name(cat_id):
            if level == 0:
                return "Total Spend"
            if cat_id is None:
                return "Other"
            node = cat_map.get(cat_id)

            if not node:
                return "Other"
            if level == 1:
                # Follow parent pointers to the top-level parent
                visited = set()
                while node["parent_id"] is not None and node["parent_id"] not in visited:
                    visited.add(node["parent_id"])
                    parent = cat_map.get(node["parent_id"])
                    if not parent:
                        break
                    node = parent
                return node["name"]
            # Default level 2 or others: use direct leaf category name
            return node["name"]

        cur.execute("""
            SELECT t.category_id, COALESCE(c.category_type, 'expense') AS cat_type, t.adjusted_amount
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.date BETWEEN ? AND ?
              AND t.adjusted_amount IS NOT NULL
              AND a.type = 'tracked'
              AND t.recurring_id IS NULL
        """, (str(start_window), str(as_of_date)))
        
        rows = cur.fetchall()
        
        category_totals = {}
        total_sum = 0.0
        for cat_id, cat_type, adj_amount in rows:
            if cat_type != 'expense':
                continue
            name = get_category_rollup_name(cat_id)
            category_totals[name] = category_totals.get(name, 0.0) + adj_amount
            total_sum += adj_amount
            
        category_averages = {}
        for name, total in category_totals.items():
            avg_rate = total / window_days
            # Filter out average daily spend less than 1 SEK in magnitude
            if abs(avg_rate) < 1.0:
                continue
            category_averages[name] = avg_rate
            
        return {
            "window_start": start_window,
            "window_end": as_of_date,
            "days": window_days,
            "categories": category_averages,
            "total_daily_average": total_sum / window_days
        }


    def get_projected_spend(self, as_of_date, window_days=30, level=1):
        """Aggregate projected spending from as_of_date to the end of the period."""
        from datetime import timedelta
        from financial_categorizer.recurring import RecurringManager, _to_date
        
        cur = self.db.get_cursor()
        as_of_date = _to_date(as_of_date)
        
        # Period boundaries
        start_date, next_payday, period_name = self.get_period_boundaries(as_of_date)
        
        # Days remaining (projection starts the day after as_of_date)
        remaining_days = max(0, (next_payday - as_of_date).days - 1)
        projection_start = as_of_date + timedelta(days=1)
        projection_end = next_payday - timedelta(days=1)
        
        # Period to date actual recurring (separated by type)
        # NOTE: alias must not collide with accounts.type — "GROUP BY type"
        # resolves to the accounts column (constant 'tracked') and collapses
        # all rows into one group, mixing income and expenses.
        cur.execute("""
            SELECT COALESCE(c.category_type, 'expense') AS cat_type, SUM(t.adjusted_amount)
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.date BETWEEN ? AND ?
              AND t.adjusted_amount IS NOT NULL
              AND a.type = 'tracked'
              AND t.recurring_id IS NOT NULL
            GROUP BY cat_type
        """, (str(start_date), str(as_of_date)))
        rec_rows = {row[0]: row[1] for row in cur.fetchall()}
        actual_rec_expense = rec_rows.get("expense", 0.0)
        actual_rec_income = rec_rows.get("income", 0.0)

        # Period to date actual non-recurring (separated by type)
        cur.execute("""
            SELECT COALESCE(c.category_type, 'expense') AS cat_type, SUM(t.adjusted_amount)
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.date BETWEEN ? AND ?
              AND t.adjusted_amount IS NOT NULL
              AND a.type = 'tracked'
              AND t.recurring_id IS NULL
            GROUP BY cat_type
        """, (str(start_date), str(as_of_date)))
        non_rec_rows = {row[0]: row[1] for row in cur.fetchall()}
        actual_non_rec_expense = non_rec_rows.get("expense", 0.0)
        actual_non_rec_income = non_rec_rows.get("income", 0.0)
        
        actual_total_expense = actual_rec_expense + actual_non_rec_expense
        actual_total_income = actual_rec_income + actual_non_rec_income
        actual_net_flow = actual_total_expense + actual_total_income
        
        # Historical daily variable rates
        hist = self.get_historical_daily_spend(as_of_date, window_days=window_days, level=level)
        
        # Project variable spend
        projected_variable_categories = {}
        projected_variable_total = 0.0
        for name, rate in hist["categories"].items():
            proj = rate * remaining_days
            projected_variable_categories[name] = proj
            projected_variable_total += proj
            
        # Upcoming expected recurring payments
        upcoming_recurring = []
        upcoming_recurring_total = 0.0
        if remaining_days > 0:
            rm = RecurringManager(self.db)
            expected_all = rm.get_expected_in_range(
                projection_start, projection_end,
                period_start=start_date, as_of_date=as_of_date,
            )
            # Only future-dated occurrences count as upcoming: period-anchored
            # expectations already drifted past as_of are either paid (actuals
            # include them) or stale anchors -- counting them double-counts.
            upcoming_recurring = [item for item in expected_all if item["upcoming"]]

            upcoming_recurring_total = sum(item["amount"] for item in upcoming_recurring)
            
        total_estimated = (actual_net_flow + projected_variable_total + upcoming_recurring_total)
                           
        return {
            "period_name": period_name,
            "period_start": start_date,
            "period_end": next_payday,
            "as_of_date": as_of_date,
            "remaining_days": remaining_days,
            "projection_start": projection_start if remaining_days > 0 else None,
            "projection_end": projection_end if remaining_days > 0 else None,
            "actual_recurring": actual_rec_expense + actual_rec_income,
            "actual_non_recurring": actual_non_rec_expense + actual_non_rec_income,
            "actual_total": actual_net_flow,
            "actual_rec_expense": actual_rec_expense,
            "actual_rec_income": actual_rec_income,
            "actual_non_rec_expense": actual_non_rec_expense,
            "actual_non_rec_income": actual_non_rec_income,
            "actual_total_expense": actual_total_expense,
            "actual_total_income": actual_total_income,
            "actual_net_flow": actual_net_flow,
            "historical_daily_averages": hist["categories"],
            "historical_daily_total": hist["total_daily_average"],
            "projected_variable_categories": projected_variable_categories,
            "projected_variable_total": projected_variable_total,
            "upcoming_recurring": upcoming_recurring,
            "upcoming_recurring_total": upcoming_recurring_total,
            "total_estimated": total_estimated
        }






    def refresh_period_projection(self, as_of_date=None):
        """Recompute the period projection table and v_burn_down view.

        Called after data mutations (import, categorize, manual-match,
        link/unlink) so dashboards consume a projection identical to the
        estimate-period CLI logic. Replaces the table wholesale: the latest
        refresh wins.
        """
        if as_of_date is None:
            as_of_date = date.today()

        proj = self.get_projected_spend(as_of_date, window_days=30, level=0)
        upcoming_expense = sum(
            -item["amount"] for item in proj["upcoming_recurring"] if item["amount"] < 0
        )
        upcoming_income = sum(
            item["amount"] for item in proj["upcoming_recurring"] if item["amount"] > 0
        )

        cur = self.db.get_cursor()
        cur.execute("DROP TABLE IF EXISTS period_projection")
        cur.execute("""
            CREATE TABLE period_projection (
                as_of_date TEXT,
                period_name TEXT,
                period_start TEXT,
                period_end TEXT,
                total_estimated REAL,
                projected_variable_total REAL,
                upcoming_recurring_total REAL,
                upcoming_recurring_expense REAL,
                actual_total_expense REAL,
                actual_total_income REAL,
                upcoming_recurring_income REAL,
                remaining_days INTEGER
            )
        """)
        cur.execute(
            "INSERT INTO period_projection VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                str(proj["as_of_date"]),
                proj["period_name"],
                str(proj["period_start"]),
                str(proj["period_end"]),
                round(proj["total_estimated"], 2),
                round(proj["projected_variable_total"], 2),
                round(proj["upcoming_recurring_total"], 2),
                round(upcoming_expense, 2),
                round(proj["actual_total_expense"], 2),
                round(proj["actual_total_income"], 2),
                round(upcoming_income, 2),
                proj["remaining_days"],
            ),
        )

        cur.execute("DROP TABLE IF EXISTS period_projection_items")
        cur.execute("""
            CREATE TABLE period_projection_items (
                config_id INTEGER,
                payment_date TEXT,
                name TEXT,
                amount REAL,
                upcoming INTEGER,
                source TEXT
            )
        """)
        # Full-period expected occurrences: upcoming ones feed the projection,
        # the full set (incl. already-passed) feeds dashboards' "typical" burn path.
        from financial_categorizer.recurring import RecurringManager

        expected = RecurringManager(self.db).get_expected_in_range(
            proj["period_start"], proj["period_end"], as_of_date=as_of_date
        )
        today = as_of_date
        cur.executemany(
            "INSERT INTO period_projection_items VALUES (?,?,?,?,?,?)",
            [
                (
                    item["config_id"],
                    str(item["date"]),
                    item["name"],
                    round(item["amount"], 2),
                    1 if item["date"] > today else 0,
                    "expected",
                )
                for item in expected
            ],
        )
        # Second pass: recurring payments already made this period whose NEXT
        # scheduled occurrence falls after the period end (e.g. loans on the
        # 27th) are missed by forward projection. Add the actual in-period
        # payment so dashboards can show the typical full-period pattern.
        cur.execute("""
            INSERT INTO period_projection_items
            SELECT t.recurring_id, t.date, r.name, ROUND(t.adjusted_amount, 2), 0, 'actual'
            FROM transactions t
            JOIN recurring_payments r ON r.id = t.recurring_id
            WHERE t.date >= ? AND t.date <= ?
              AND r.end_date IS NULL
              AND t.adjusted_amount != 0
              AND t.recurring_id NOT IN (
                  SELECT config_id FROM period_projection_items
                  WHERE upcoming = 1 AND source = 'expected'
              )
            ORDER BY t.date
        """, (str(proj["period_start"]), str(proj["period_end"])))
        # Stale dedupe: an expected occurrence dated before as_of for a
        # template that WAS paid in-period duplicates the actual row above
        # (drift makes the projected date lag the real payment). Drop the
        # stale expected row, keep the actual one.
        cur.execute("""
            DELETE FROM period_projection_items
            WHERE source = 'expected' AND upcoming = 0
              AND config_id IN (
                  SELECT DISTINCT t.recurring_id FROM transactions t
                  WHERE t.recurring_id IS NOT NULL
                    AND t.date >= ? AND t.date <= ?
                    AND t.adjusted_amount != 0
              )
        """, (str(proj["period_start"]), str(proj["period_end"])))

        cur.execute("DROP VIEW IF EXISTS v_burn_down")
        cur.execute("""
            CREATE VIEW v_burn_down AS
            -- Income-anchored, mirrors get_projected_spend(): day 0 starts at
            -- actual income + upcoming income items; remaining_net tracks the
            -- net position (anchor minus cumulative expenses). All scalar
            -- inputs come from period_projection (written by the Python
            -- projection logic) so no projection math is duplicated here.
            WITH p AS (SELECT * FROM period_projection LIMIT 1),
            anchor AS (
                SELECT actual_total_income + upcoming_recurring_income AS income_anchor
                FROM p
            ),
            days(d) AS (
                WITH RECURSIVE seq(i) AS (
                    SELECT 0 UNION ALL SELECT i + 1 FROM seq
                    WHERE i < (SELECT CAST(julianday('now') - julianday((SELECT period_start FROM p)) AS INT))
                )
                SELECT date((SELECT period_start FROM p), printf('+%d days', i)) FROM seq
            )
            SELECT
                d,
                ROUND((SELECT income_anchor FROM anchor), 2) AS income_anchor,
                ROUND(
                    (SELECT income_anchor FROM anchor)
                    - COALESCE((
                        SELECT SUM(-t.adjusted_amount)
                        FROM transactions t
                        JOIN accounts a ON a.id = t.account_id
                        LEFT JOIN categories c ON c.id = t.category_id
                        WHERE t.date >= (SELECT period_start FROM p)
                          AND t.date <= d
                          AND t.adjusted_amount < 0
                          AND a.type = 'tracked'
                          AND COALESCE(c.category_type, 'expense') != 'transfer'
                    ), 0), 2) AS remaining_net
            FROM days
        """)
        self.db.commit()
