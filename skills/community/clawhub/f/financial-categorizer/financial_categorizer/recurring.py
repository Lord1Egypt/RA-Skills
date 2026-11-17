import logging
import re
from datetime import date, datetime, timedelta

logger = logging.getLogger("financial-categorizer")

def _to_date(val):
    """Helper to convert date representation into a datetime.date object.

    Handles None, strings, datetime.date, and datetime.datetime.
    """
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        if isinstance(val, datetime):
            return val.date()
        return val
    if isinstance(val, str):
        if " " in val:
            val = val.split(" ")[0]
        if "T" in val:
            val = val.split("T")[0]
        return date.fromisoformat(val)
    return val

class RecurringManager:
    """Manages recurring payments (subscriptions, utilities, salary, etc.).

    Handles schema updates, rule management (add, update, remove), automatic matching,
    resumption of cancelled subscriptions, and stats queries.
    """

    def __init__(self, db_handler):
        """
        Args:
            db_handler: A connected DatabaseHandler instance.
        """
        self.db = db_handler

    # ------------------------------------------------------------------ #
    #  Date Matching Logic
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_last_day_of_month(year: int, month: int) -> date:
        """Helper to get the last day of a given month/year."""
        if month == 12:
            return date(year, 12, 31)
        return date(year, month + 1, 1) - timedelta(days=1)

    @staticmethod
    def get_nth_weekday_of_month(year: int, month: int, day_of_week: int, nth: int) -> date | None:
        """Find the nth occurrence of day_of_week in the month.

        nth = 1 to 5, or -1 for the last occurrence.
        day_of_week = 0 (Monday) to 6 (Sunday).
        """
        first_day = date(year, month, 1)
        last_day = RecurringManager.get_last_day_of_month(year, month)
        
        matching_dates = []
        curr = first_day
        while curr <= last_day:
            if curr.weekday() == day_of_week:
                matching_dates.append(curr)
            curr += timedelta(days=1)

        if nth == -1:
            return matching_dates[-1] if matching_dates else None
        elif 1 <= nth <= len(matching_dates):
            return matching_dates[nth - 1]
        return None

    @staticmethod
    def matches_schedule(
        tx_dt: date,
        start_dt: date,
        end_dt: date | None,
        interval_type: str,
        interval_value: int,
        day_of_month: int | None,
        day_of_week: int | None,
        week_of_month: int | None,
        tolerance_days: int
    ) -> bool:
        """Check if tx_dt falls within the expected schedule of a recurring series (with tolerance)."""
        tx_dt = _to_date(tx_dt)
        start_dt = _to_date(start_dt)
        end_dt = _to_date(end_dt)

        # Outer date bounds check
        if tx_dt < start_dt:
            return False
        # Allow small tolerance past end_date for late postings
        if end_dt is not None and tx_dt > end_dt + timedelta(days=tolerance_days):
            return False

        # 1. Monthly Interval
        if interval_type == "monthly":
            # Check candidate months: current, previous, next to handle tolerance overlap
            candidate_months = []
            for delta_m in (-1, 0, 1):
                m_c = tx_dt.month + delta_m
                y_c = tx_dt.year
                if m_c < 1:
                    m_c += 12
                    y_c -= 1
                elif m_c > 12:
                    m_c -= 12
                    y_c += 1
                candidate_months.append((y_c, m_c))

            for y_c, m_c in candidate_months:
                months_diff = (y_c - start_dt.year) * 12 + (m_c - start_dt.month)
                if months_diff < 0 or months_diff % interval_value != 0:
                    continue

                # Find expected date in candidate month
                exp_dt = None
                last_day = RecurringManager.get_last_day_of_month(y_c, m_c)
                
                if day_of_month is not None:
                    if day_of_month == -1:
                        exp_dt = last_day
                    else:
                        d_c = min(day_of_month, last_day.day)
                        exp_dt = date(y_c, m_c, d_c)
                elif day_of_week is not None and week_of_month is not None:
                    exp_dt = RecurringManager.get_nth_weekday_of_month(y_c, m_c, day_of_week, week_of_month)
                else:
                    # Default: use day of start_dt
                    exp_dt = date(y_c, m_c, min(start_dt.day, last_day.day))

                if exp_dt:
                    # Validate against absolute limits
                    if exp_dt < start_dt or (end_dt is not None and exp_dt > end_dt):
                        continue
                    if abs((tx_dt - exp_dt).days) <= tolerance_days:
                        return True

        # 2. Weekly Interval
        elif interval_type == "weekly":
            weeks_diff_approx = (tx_dt - start_dt).days // 7
            for delta_w in (-1, 0, 1):
                w_c = weeks_diff_approx + delta_w
                if w_c < 0 or w_c % interval_value != 0:
                    continue

                anchor_dt = start_dt + timedelta(weeks=w_c)
                if day_of_week is not None:
                    days_shift = day_of_week - anchor_dt.weekday()
                    exp_dt = anchor_dt + timedelta(days=days_shift)
                else:
                    exp_dt = anchor_dt

                if exp_dt < start_dt or (end_dt is not None and exp_dt > end_dt):
                    continue
                if abs((tx_dt - exp_dt).days) <= tolerance_days:
                    return True

        # 3. Yearly Interval
        elif interval_type == "yearly":
            candidate_years = (tx_dt.year - 1, tx_dt.year, tx_dt.year + 1)
            for y_c in candidate_years:
                years_diff = y_c - start_dt.year
                if years_diff < 0 or years_diff % interval_value != 0:
                    continue

                last_day = RecurringManager.get_last_day_of_month(y_c, start_dt.month)
                exp_dt = date(y_c, start_dt.month, min(start_dt.day, last_day.day))

                if exp_dt < start_dt or (end_dt is not None and exp_dt > end_dt):
                    continue
                if abs((tx_dt - exp_dt).days) <= tolerance_days:
                    return True

        # 4. Days Interval
        elif interval_type == "days":
            days_diff = (tx_dt - start_dt).days
            if days_diff < -tolerance_days:
                return False
            k = round(days_diff / interval_value)
            for delta_k in (-1, 0, 1):
                k_c = k + delta_k
                if k_c < 0:
                    continue
                exp_dt = start_dt + timedelta(days=k_c * interval_value)
                if exp_dt < start_dt or (end_dt is not None and exp_dt > end_dt):
                    continue
                if abs((tx_dt - exp_dt).days) <= tolerance_days:
                    return True

        return False

    # ------------------------------------------------------------------ #
    #  Rule Operations
    # ------------------------------------------------------------------ #

    def add_recurring(
        self,
        name: str,
        pattern: str,
        match_type: str = "contains",
        amount_min: float | None = None,
        amount_max: float | None = None,
        interval_type: str = "monthly",
        interval_value: int = 1,
        day_of_month: int | None = None,
        day_of_week: int | None = None,
        week_of_month: int | None = None,
        start_date: date | str | None = None,
        end_date: date | str | None = None,
        category_id: int | None = None,
        account_id: int | None = None,
        tolerance_days: int = 4
    ) -> int:
        """Create a new recurring payment configuration in the database."""
        start_date = _to_date(start_date)
        if start_date is None:
            start_date = date.today()
        end_date = _to_date(end_date)

        cur = self.db.get_cursor()
        cur.execute("""
            INSERT INTO recurring_payments (
                name, pattern, match_type, amount_min, amount_max,
                interval_type, interval_value, day_of_month, day_of_week, week_of_month,
                tolerance_days, start_date, end_date, category_id, account_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, pattern, match_type, amount_min, amount_max,
            interval_type, interval_value, day_of_month, day_of_week, week_of_month,
            tolerance_days, start_date.isoformat(),
            end_date.isoformat() if end_date else None,
            category_id, account_id
        ))
        self.db.commit()
        return cur.lastrowid

    def update_recurring(self, recurring_id: int, **kwargs) -> bool:
        """Update fields of an existing recurring payment configuration."""
        cur = self.db.get_cursor()
        cur.execute("SELECT id FROM recurring_payments WHERE id = ?", (recurring_id,))
        if not cur.fetchone():
            return False

        if not kwargs:
            return True

        set_clauses = []
        params = []
        for k, v in kwargs.items():
            if k in (
                "name", "pattern", "match_type", "amount_min", "amount_max",
                "interval_type", "interval_value", "day_of_month", "day_of_week",
                "week_of_month", "tolerance_days", "start_date", "end_date",
                "category_id", "account_id"
            ):
                set_clauses.append(f"{k} = ?")
                v_res = _to_date(v) if k in ("start_date", "end_date") else v
                if isinstance(v_res, date):
                    params.append(v_res.isoformat())
                else:
                    params.append(v_res)

        if not set_clauses:
            return True

        params.append(recurring_id)
        sql = f"UPDATE recurring_payments SET {', '.join(set_clauses)} WHERE id = ?"
        cur.execute(sql, tuple(params))
        self.db.commit()
        return True

    def remove_recurring(self, recurring_id: int, hard: bool = False, cancel_date: date | str | None = None) -> bool:
        """Remove a recurring payment configuration.

        If hard is True, deletes the row completely.
        If hard is False, soft-deletes/cancels by setting end_date.
        """
        cur = self.db.get_cursor()
        cur.execute("SELECT id, start_date FROM recurring_payments WHERE id = ?", (recurring_id,))
        row = cur.fetchone()
        if not row:
            return False

        if hard:
            cur.execute("DELETE FROM recurring_payments WHERE id = ?", (recurring_id,))
            self.db.commit()
            return True

        # Soft-close/cancel
        cancel_date = _to_date(cancel_date)
        if cancel_date is None:
            cur.execute("SELECT MAX(date) FROM transactions WHERE recurring_id = ?", (recurring_id,))
            last_txn_row = cur.fetchone()
            if last_txn_row and last_txn_row[0]:
                cancel_date = _to_date(last_txn_row[0])
            else:
                cancel_date = date.today()

        cur.execute("UPDATE recurring_payments SET end_date = ? WHERE id = ?", (cancel_date.isoformat(), recurring_id))
        self.db.commit()
        return True

    # ------------------------------------------------------------------ #
    #  Transaction Matching & Linking
    # ------------------------------------------------------------------ #

    def link_transactions(self, dry_run: bool = False, auto_close: bool = False) -> dict:
        """Match existing transactions to active and cancelled recurring payment configs.

        Performs:
        1. Auto-resumption if transaction matches a cancelled configuration and is post-end-date.
        2. Assigning recurring_id to matching transactions.
        3. Auto-closing active configs that are missing expected payments.

        Returns a dictionary of actions taken: {'linked': list, 'resumed': list, 'closed': list, 'warnings': list}
        """
        cur = self.db.get_cursor()
        
        cur.execute("""
            SELECT id, name, pattern, match_type, amount_min, amount_max,
                   interval_type, interval_value, day_of_month, day_of_week, week_of_month,
                   tolerance_days, start_date, end_date, category_id, account_id
            FROM recurring_payments
            ORDER BY id ASC
        """)
        configs = []
        for row in cur.fetchall():
            configs.append({
                "id": row[0], "name": row[1], "pattern": row[2], "match_type": row[3],
                "amount_min": row[4], "amount_max": row[5], "interval_type": row[6],
                "interval_value": row[7], "day_of_month": row[8], "day_of_week": row[9],
                "week_of_month": row[10], "tolerance_days": row[11],
                "start_date": _to_date(row[12]),
                "end_date": _to_date(row[13]),
                "category_id": row[14], "account_id": row[15]
            })

        cur.execute("""
            SELECT id, date, description, amount, account_id, category_id
            FROM transactions
            WHERE recurring_id IS NULL
            ORDER BY date ASC
        """)
        unlinked_txs = []
        for row in cur.fetchall():
            unlinked_txs.append({
                "id": row[0], "date": _to_date(row[1]), "description": row[2],
                "amount": row[3], "account_id": row[4], "category_id": row[5]
            })

        results = {"linked": [], "resumed": [], "closed": [], "warnings": []}

        def _match_desc(pattern: str, m_type: str, desc: str) -> bool:
            if m_type == "regex":
                return re.search(pattern, desc, re.IGNORECASE) is not None
            elif m_type == "exact":
                return pattern.lower() == desc.lower()
            elif m_type == "contains":
                return pattern.lower() in desc.lower()
            return False

        for tx in unlinked_txs:
            matched_config = None
            amount_bounds_warnings = []
            for conf in configs:
                if not _match_desc(conf["pattern"], conf["match_type"], tx["description"]):
                    continue
                if conf["account_id"] is not None and conf["account_id"] != tx["account_id"]:
                    continue

                # Check schedule matches
                schedule_matches = self.matches_schedule(
                    tx["date"], conf["start_date"], conf["end_date"],
                    conf["interval_type"], conf["interval_value"],
                    conf["day_of_month"], conf["day_of_week"], conf["week_of_month"],
                    conf["tolerance_days"]
                )

                # Check amount min and max
                amount_ok = True
                if conf["amount_min"] is not None and tx["amount"] < conf["amount_min"]:
                    amount_ok = False
                if conf["amount_max"] is not None and tx["amount"] > conf["amount_max"]:
                    amount_ok = False

                if schedule_matches:
                    if amount_ok:
                        matched_config = conf
                        break
                    else:
                        amount_bounds_warnings.append({
                            "type": "amount_bounds",
                            "id": conf["id"],
                            "name": conf["name"],
                            "tx_id": tx["id"],
                            "tx_date": tx["date"].isoformat() if hasattr(tx["date"], "isoformat") else str(tx["date"]),
                            "tx_desc": tx["description"],
                            "tx_amount": tx["amount"],
                            "amount_min": conf["amount_min"],
                            "amount_max": conf["amount_max"]
                        })
                
                elif conf["end_date"] is not None and tx["date"] > conf["end_date"]:
                    if not amount_ok:
                        continue
                    is_superseded = False
                    for other in configs:
                        if other["id"] != conf["id"] and other["name"].lower() == conf["name"].lower():
                            if other["end_date"] is None or other["end_date"] > conf["end_date"]:
                                is_superseded = True
                                break
                    if not is_superseded:
                        new_id = None
                        if not dry_run:
                            new_id = self.add_recurring(
                                name=conf["name"], pattern=conf["pattern"], match_type=conf["match_type"],
                                amount_min=conf["amount_min"], amount_max=conf["amount_max"],
                                interval_type=conf["interval_type"], interval_value=conf["interval_value"],
                                day_of_month=conf["day_of_month"], day_of_week=conf["day_of_week"],
                                week_of_month=conf["week_of_month"], start_date=tx["date"],
                                category_id=conf["category_id"], account_id=conf["account_id"],
                                tolerance_days=conf["tolerance_days"]
                            )
                            new_conf = {
                                "id": new_id, "name": conf["name"], "pattern": conf["pattern"], "match_type": conf["match_type"],
                                "amount_min": conf["amount_min"], "amount_max": conf["amount_max"], "interval_type": conf["interval_type"],
                                "interval_value": conf["interval_value"], "day_of_month": conf["day_of_month"], "day_of_week": conf["day_of_week"],
                                "week_of_month": conf["week_of_month"], "tolerance_days": conf["tolerance_days"],
                                "start_date": tx["date"], "end_date": None, "category_id": conf["category_id"], "account_id": conf["account_id"]
                            }
                            configs.append(new_conf)
                            matched_config = new_conf
                        else:
                            matched_config = {"id": -1, "name": conf["name"], "is_dry_run_resumption": True}
                        
                        results["resumed"].append({
                            "tx_id": tx["id"], "tx_date": tx["date"], "tx_desc": tx["description"],
                            "parent_id": conf["id"], "new_id": new_id, "name": conf["name"]
                        })
                        break
            
            if matched_config:
                if not dry_run:
                    cur.execute("UPDATE transactions SET recurring_id = ? WHERE id = ?", (matched_config["id"], tx["id"]))
                    if matched_config.get("category_id") is not None and tx["category_id"] is None:
                        cur.execute("UPDATE transactions SET category_id = ? WHERE id = ?", (matched_config["category_id"], tx["id"]))
                
                results["linked"].append({
                    "tx_id": tx["id"], "tx_date": tx["date"], "tx_desc": tx["description"],
                    "tx_amount": tx["amount"], "recurring_id": matched_config["id"],
                    "recurring_name": matched_config["name"]
                })
            else:
                results["warnings"].extend(amount_bounds_warnings)

        if not dry_run and results["linked"]:
            self.db.commit()

        cur.execute("SELECT account_id, MAX(date) FROM transactions GROUP BY account_id")
        acct_boundaries = {row[0]: _to_date(row[1]) for row in cur.fetchall() if row[1]}
        
        cur.execute("SELECT MAX(date) FROM transactions")
        global_max_row = cur.fetchone()
        global_max_dt = _to_date(global_max_row[0]) if (global_max_row and global_max_row[0]) else date.today()

        for conf in configs:
            if conf["end_date"] is not None:
                continue

            bound_dt = acct_boundaries.get(conf["account_id"]) if conf["account_id"] is not None else global_max_dt
            if not bound_dt:
                continue

            cur.execute("SELECT MAX(date) FROM transactions WHERE recurring_id = ?", (conf["id"],))
            last_matched_row = cur.fetchone()
            last_pmt = _to_date(last_matched_row[0]) if (last_matched_row and last_matched_row[0]) else conf["start_date"]

            next_exp = None
            if conf["interval_type"] == "monthly":
                delta_y = (last_pmt.month + conf["interval_value"] - 1) // 12
                next_m = (last_pmt.month + conf["interval_value"] - 1) % 12 + 1
                next_y = last_pmt.year + delta_y
                last_day_of_next = RecurringManager.get_last_day_of_month(next_y, next_m)
                
                if conf["day_of_month"] is not None:
                    if conf["day_of_month"] == -1:
                        next_exp = last_day_of_next
                    else:
                        next_exp = date(next_y, next_m, min(conf["day_of_month"], last_day_of_next.day))
                elif conf["day_of_week"] is not None and conf["week_of_month"] is not None:
                    next_exp = RecurringManager.get_nth_weekday_of_month(next_y, next_m, conf["day_of_week"], conf["week_of_month"])
                else:
                    next_exp = date(next_y, next_m, min(conf["start_date"].day, last_day_of_next.day))
            elif conf["interval_type"] == "weekly":
                next_exp = last_pmt + timedelta(weeks=conf["interval_value"])
            elif conf["interval_type"] == "yearly":
                next_y = last_pmt.year + conf["interval_value"]
                start_d = _to_date(conf["start_date"])
                last_day_of_next = RecurringManager.get_last_day_of_month(next_y, start_d.month)
                next_exp = date(next_y, start_d.month, min(start_d.day, last_day_of_next.day))
            elif conf["interval_type"] == "days":
                next_exp = last_pmt + timedelta(days=conf["interval_value"])

            if next_exp and (next_exp + timedelta(days=conf["tolerance_days"])) < bound_dt:
                results["warnings"].append({
                    "id": conf["id"], "name": conf["name"], "expected": next_exp, "boundary": bound_dt
                })
                if auto_close:
                    if not dry_run:
                        self.remove_recurring(conf["id"], hard=False, cancel_date=last_pmt)
                    results["closed"].append({
                        "id": conf["id"], "name": conf["name"], "end_date": last_pmt
                    })

        return results

    # ------------------------------------------------------------------ #
    #  Auto-Discovery Logic
    # ------------------------------------------------------------------ #

    def discover_recurring_candidates(self, dry_run: bool = False) -> list[dict]:
        """Auto-discover regular recurring patterns in the transaction log.

        Cleans descriptions, groups transactions, finds regular intervals,
        and saves them (or previews if dry_run is True). Also checks for
        and closes active subscriptions that are dead.
        """
        cur = self.db.get_cursor()
        
        cur.execute("SELECT id, date, description, amount, account_id, category_id FROM transactions ORDER BY date ASC")
        txs = cur.fetchall()

        def _clean_desc(d: str) -> str:
            if re.search(r'(?i)Netflix', d):
                return 'Netflix'
            if re.search(r'(?i)Spotify', d):
                return 'Spotify'
            if re.search(r'(?i)Disney', d):
                return 'Disney Plus'
            if re.search(r'(?i)CSN Centrala', d):
                return 'CSN'
                
            d_c = re.sub(r'(?i)^Kortk.p\s+\d{6}\s+', '', d)
            d_c = re.sub(r'(?i)^Kortk.p\s+', '', d_c)
            d_c = re.sub(r'(?i)^Reservation Kortk.p\s+\d{6}\s+', '', d_c)
            d_c = re.sub(r'(?i)^Reserverat\s+', '', d_c)
            d_c = re.sub(r'\s+P\w{8,10}$', '', d_c)
            return d_c.strip()

        groups = {}
        group_names = {}
        for row in txs:
            t_id, t_dt_str, t_desc, t_amt, t_acc, t_cat = row
            t_dt = _to_date(t_dt_str)
            cleaned = _clean_desc(t_desc)
            if not cleaned or len(cleaned) < 3:
                continue
            sign = 1 if t_amt >= 0 else -1
            key = (cleaned.lower(), sign, t_acc)
            if key not in groups:
                groups[key] = []
                group_names[key] = {}
            groups[key].append({
                "id": t_id, "date": t_dt, "amount": t_amt, "category_id": t_cat
            })
            group_names[key][cleaned] = group_names[key].get(cleaned, 0) + 1

        discovered = []

        for key, items in groups.items():
            cleaned_lower, sign, acc_id = key
            cleaned_repr = max(group_names[key], key=group_names[key].get)
            
            if len(items) < 3:
                continue

            items.sort(key=lambda x: x["date"])
            dates = [it["date"] for it in items]
            
            # Filter out short-span ad-hoc clusters (e.g. vacation spending)
            total_span = (dates[-1] - dates[0]).days
            if total_span < 30:
                continue

            amounts = [it["amount"] for it in items]
            categories = [it["category_id"] for it in items if it["category_id"] is not None]



            gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
            
            n_gaps = len(gaps)
            avg_gap = sum(gaps) / n_gaps
            variance = sum((g - avg_gap) ** 2 for g in gaps) / n_gaps
            std_dev = variance ** 0.5

            interval_type = None
            interval_value = 1
            day_of_month = None
            day_of_week = None

            if 25 <= avg_gap <= 35 and std_dev < 7:
                days_of_month = [d.day for d in dates]
                dom_mean = sum(days_of_month) / len(days_of_month)
                dom_var = sum((d - dom_mean) ** 2 for d in days_of_month) / len(days_of_month)
                dom_std = dom_var ** 0.5
                if dom_std > 5:
                    interval_type = "days"
                    interval_value = int(round(avg_gap))
                    day_of_month = None
                else:
                    interval_type = "monthly"
                    interval_value = 1
                    day_of_month = max(set(days_of_month), key=days_of_month.count)
            elif 50 <= avg_gap <= 70 and std_dev < 10:
                interval_type = "monthly"
                interval_value = 2
                days = [d.day for d in dates]
                day_of_month = max(set(days), key=days.count)
            elif 80 <= avg_gap <= 100 and std_dev < 12:
                interval_type = "monthly"
                interval_value = 3
                days = [d.day for d in dates]
                day_of_month = max(set(days), key=days.count)
            elif 6 <= avg_gap <= 8 and std_dev < 2:
                interval_type = "weekly"
                interval_value = 1
                weekdays = [d.weekday() for d in dates]
                day_of_week = max(set(weekdays), key=weekdays.count)
            elif 13 <= avg_gap <= 15 and std_dev < 3:
                interval_type = "weekly"
                interval_value = 2
                weekdays = [d.weekday() for d in dates]
                day_of_week = max(set(weekdays), key=weekdays.count)
            elif 350 <= avg_gap <= 380 and std_dev < 15:
                interval_type = "yearly"
                interval_value = 1
            elif 1 <= avg_gap <= 10 and std_dev < 1.5:
                interval_type = "days"
                interval_value = int(round(avg_gap))

            if interval_type:
                min_amt = min(amounts)
                max_amt = max(amounts)
                suggested_cat = max(set(categories), key=categories.count) if categories else None

                discovered.append({
                    "name": cleaned_repr,
                    "pattern": cleaned_repr,

                    "match_type": "contains",
                    "amount_min": min_amt,
                    "amount_max": max_amt,
                    "interval_type": interval_type,
                    "interval_value": interval_value,
                    "day_of_month": day_of_month,
                    "day_of_week": day_of_week,
                    "start_date": dates[0],
                    "category_id": suggested_cat,
                    "account_id": acc_id,
                    "tx_count": len(items),
                    "tx_ids": [it["id"] for it in items]
                })

        saved_configs = []
        if not dry_run:
            cur.execute("SELECT pattern FROM recurring_payments")
            existing_patterns = set(row[0].lower() for row in cur.fetchall())

            for cand in discovered:
                if cand["pattern"].lower() in existing_patterns:
                    continue

                new_id = self.add_recurring(
                    name=cand["name"], pattern=cand["pattern"], match_type=cand["match_type"],
                    amount_min=cand["amount_min"], amount_max=cand["amount_max"],
                    interval_type=cand["interval_type"], interval_value=cand["interval_value"],
                    day_of_month=cand["day_of_month"], day_of_week=cand["day_of_week"],
                    start_date=cand["start_date"], category_id=cand["category_id"],
                    account_id=cand["account_id"]
                )
                cand["id"] = new_id
                saved_configs.append(cand)

            # Automatically run matching and auto-closing of dead existing active configurations
            self.link_transactions(dry_run=False, auto_close=True)
        else:
            saved_configs = discovered

        return saved_configs

    # ------------------------------------------------------------------ #
    #  Stats Calculations
    # ------------------------------------------------------------------ #

    def get_recurring_stats(self, query: str | None = None, period_type: str = "default", period: str | None = None) -> dict:
        """Query statistics for active subscriptions and utility configurations.

        Returns stats filtered by name/ID, or a general active outflow dashboard.
        """
        cur = self.db.get_cursor()

        if period_type == "default":
            mode = self.db.get_metadata("salary_period_mode", "fixed")
            resolved_pt = "salary" if mode in ("fixed", "salary") else "calendar"
        else:
            resolved_pt = period_type

        sql = """
            SELECT r.id, r.name, r.pattern, r.match_type, r.interval_type, r.interval_value,
                   r.day_of_month, r.day_of_week, r.week_of_month, r.start_date, r.end_date,
                   c.name, a.name, r.amount_min, r.amount_max, r.tolerance_days
            FROM recurring_payments r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN accounts a ON r.account_id = a.id
        """
        params = []
        if query is not None:
            if str(query).isdigit():
                sql += " WHERE r.id = ?"
                params.append(int(query))
            else:
                sql += " WHERE r.name LIKE ?"
                params.append(f"%{query}%")
        
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()

        configs = []
        for row in rows:
            configs.append({
                "id": row[0], "name": row[1], "pattern": row[2], "match_type": row[3],
                "interval_type": row[4], "interval_value": row[5], "day_of_month": row[6],
                "day_of_week": row[7], "week_of_month": row[8], "start_date": row[9],
                "end_date": row[10], "category_name": row[11], "account_name": row[12],
                "amount_min": row[13], "amount_max": row[14], "tolerance_days": row[15]
            })


        details = []
        total_monthly_outflow = 0.0
        active_count = 0

        for conf in configs:
            cur.execute("""
                SELECT t.id, t.date, t.description, t.amount, t.adjusted_amount, sp.period
                FROM transactions t
                JOIN v_salary_periods sp ON t.id = sp.transaction_id
                WHERE t.recurring_id = ?
                ORDER BY t.date DESC
            """, (conf["id"],))
            matched_txs = []
            for tx_row in cur.fetchall():
                matched_txs.append({
                    "id": tx_row[0], "date": tx_row[1], "description": tx_row[2],
                    "amount": tx_row[3], "adjusted_amount": tx_row[4],
                    "salary_period": tx_row[5]
                })

            lifetime_total = sum(tx["adjusted_amount"] for tx in matched_txs)
            
            curr_year = datetime.today().year
            ytd_total = sum(tx["adjusted_amount"] for tx in matched_txs if _to_date(tx["date"]).year == curr_year)


            last_pmt = matched_txs[0] if matched_txs else None

            next_exp = None
            if conf["end_date"] is None:
                active_count += 1
                last_pmt_dt = _to_date(last_pmt["date"]) if last_pmt else _to_date(conf["start_date"])
                
                if conf["interval_type"] == "monthly":
                    delta_y = (last_pmt_dt.month + conf["interval_value"] - 1) // 12
                    next_m = (last_pmt_dt.month + conf["interval_value"] - 1) % 12 + 1
                    next_y = last_pmt_dt.year + delta_y
                    last_day_of_next = RecurringManager.get_last_day_of_month(next_y, next_m)
                    
                    if conf["day_of_month"] is not None:
                        if conf["day_of_month"] == -1:
                            next_exp = last_day_of_next
                        else:
                            next_exp = date(next_y, next_m, min(conf["day_of_month"], last_day_of_next.day))
                    elif conf["day_of_week"] is not None and conf["week_of_month"] is not None:
                        next_exp = RecurringManager.get_nth_weekday_of_month(next_y, next_m, conf["day_of_week"], conf["week_of_month"])
                    else:
                        next_exp = date(next_y, next_m, min(_to_date(conf["start_date"]).day, last_day_of_next.day))
                elif conf["interval_type"] == "weekly":
                    next_exp = last_pmt_dt + timedelta(weeks=conf["interval_value"])
                elif conf["interval_type"] == "yearly":
                    next_y = last_pmt_dt.year + conf["interval_value"]
                    start_d = _to_date(conf["start_date"])
                    last_day_of_next = RecurringManager.get_last_day_of_month(next_y, start_d.month)
                    next_exp = date(next_y, start_d.month, min(start_d.day, last_day_of_next.day))
                elif conf["interval_type"] == "days":
                    next_exp = last_pmt_dt + timedelta(days=conf["interval_value"])

                outflow_amt = 0.0
                if last_pmt:
                    outflow_amt = last_pmt["amount"]
                elif conf["amount_min"] is not None and conf["amount_max"] is not None:
                    outflow_amt = (conf["amount_min"] + conf["amount_max"]) / 2
                elif conf["amount_min"] is not None:
                    outflow_amt = conf["amount_min"]

                if outflow_amt < 0:
                    if conf["interval_type"] == "monthly":
                        total_monthly_outflow += (outflow_amt / conf["interval_value"])
                    elif conf["interval_type"] == "weekly":
                        total_monthly_outflow += (outflow_amt * 4.33 / conf["interval_value"])
                    elif conf["interval_type"] == "yearly":
                        total_monthly_outflow += (outflow_amt / 12.0 / conf["interval_value"])
                    elif conf["interval_type"] == "days":
                        total_monthly_outflow += (outflow_amt * 30.4 / conf["interval_value"])

            details.append({
                "config": conf,
                "transactions": matched_txs,
                "last_payment": last_pmt,
                "next_expected": next_exp,
                "lifetime_total": lifetime_total,
                "ytd_total": ytd_total,
                "active": conf["end_date"] is None
            })

        return {
            "details": details,
            "active_count": active_count,
            "total_monthly_outflow": total_monthly_outflow
        }

    def get_expected_in_range(self, start_date: date, end_date: date, period_start: date = None, as_of_date: date = None) -> list[dict]:
        """Generate expected payment occurrences and estimated adjusted amounts for active templates
        within the date range [start_date, end_date] (inclusive).

        Each occurrence carries an ``upcoming`` flag (date > as_of_date,
        default today). Callers wanting "still owed" must filter on it:
        real-world interval drift pushes projected dates into the past, where
        they are either already paid (actuals cover them) or stale anchors.
        """
        cur = self.db.get_cursor()
        if as_of_date is None:
            as_of_date = date.today()

        
        # Select active recurring templates
        cur.execute("""
            SELECT r.id, r.name, r.pattern, r.match_type, r.interval_type, r.interval_value,
                   r.day_of_month, r.day_of_week, r.week_of_month, r.start_date, r.end_date,
                   r.amount_min, r.amount_max, r.account_id, r.category_id, c.name
            FROM recurring_payments r
            LEFT JOIN categories c ON r.category_id = c.id
            WHERE r.end_date IS NULL
        """)
        rows = cur.fetchall()
        
        expected_occurrences = []
        
        for row in rows:
            conf = {
                "id": row[0], "name": row[1], "pattern": row[2], "match_type": row[3],
                "interval_type": row[4], "interval_value": row[5], "day_of_month": row[6],
                "day_of_week": row[7], "week_of_month": row[8], "start_date": row[9],
                "end_date": row[10], "amount_min": row[11], "amount_max": row[12],
                "account_id": row[13], "category_id": row[14], "category_name": row[15]
            }
            
            # Find last payment to anchor the projection
            cur.execute("""
                SELECT date, adjusted_amount, amount FROM transactions
                WHERE recurring_id = ?
                ORDER BY date DESC LIMIT 1
            """, (conf["id"],))
            last_pmt = cur.fetchone()
            
            if last_pmt:
                anchor_dt = _to_date(last_pmt[0])
                est_adjusted_amount = last_pmt[1]
            else:
                anchor_dt = _to_date(conf["start_date"])
                # Resolve account ownership ratio to calculate estimated adjusted amount
                ratio = 1.0
                if conf["account_id"]:
                    cur.execute("SELECT ownership_ratio FROM accounts WHERE id = ?", (conf["account_id"],))
                    a_row = cur.fetchone()
                    if a_row:
                        ratio = a_row[0]
                
                val = 0.0
                if conf["amount_min"] is not None and conf["amount_max"] is not None:
                    val = (conf["amount_min"] + conf["amount_max"]) / 2
                elif conf["amount_min"] is not None:
                    val = conf["amount_min"]
                est_adjusted_amount = val * ratio
            
            # Project dates starting from anchor_dt
            def _next_expected_date(last_date: date) -> date:
                if conf["interval_type"] == "monthly":
                    delta_y = (last_date.month + conf["interval_value"] - 1) // 12
                    next_m = (last_date.month + conf["interval_value"] - 1) % 12 + 1
                    next_y = last_date.year + delta_y
                    last_day_of_next = RecurringManager.get_last_day_of_month(next_y, next_m)
                    if conf["day_of_month"] is not None:
                        if conf["day_of_month"] == -1:
                            return last_day_of_next
                        else:
                            return date(next_y, next_m, min(conf["day_of_month"], last_day_of_next.day))
                    elif conf["day_of_week"] is not None and conf["week_of_month"] is not None:
                        return RecurringManager.get_nth_weekday_of_month(next_y, next_m, conf["day_of_week"], conf["week_of_month"])
                    else:
                        start_d = _to_date(conf["start_date"])
                        return date(next_y, next_m, min(start_d.day, last_day_of_next.day))
                elif conf["interval_type"] == "weekly":
                    return last_date + timedelta(weeks=conf["interval_value"])
                elif conf["interval_type"] == "yearly":
                    next_y = last_date.year + conf["interval_value"]
                    start_d = _to_date(conf["start_date"])
                    last_day_of_next = RecurringManager.get_last_day_of_month(next_y, start_d.month)
                    return date(next_y, start_d.month, min(start_d.day, last_day_of_next.day))
                elif conf["interval_type"] == "days":
                    return last_date + timedelta(days=conf["interval_value"])
                raise ValueError(f"Unknown interval type: {conf['interval_type']}")
            
            curr_dt = anchor_dt
            # Iterate and find all expected dates inside range
            if conf["interval_value"] <= 0:
                continue
                
            iterations = 0
            while iterations < 100:  # Safe guard boundary
                iterations += 1
                try:
                    curr_dt = _next_expected_date(curr_dt)
                except Exception:
                    break
                if curr_dt > end_date:
                    break
                lower_bound = period_start if period_start is not None else start_date
                if curr_dt >= lower_bound:
                    expected_occurrences.append({
                        "config_id": conf["id"],
                        "name": conf["name"],
                        "date": curr_dt,
                        "amount": est_adjusted_amount,
                        "category_name": conf["category_name"] or "None",
                        "upcoming": curr_dt > as_of_date
                    })

                    
        expected_occurrences.sort(key=lambda x: x["date"])
        return expected_occurrences

