import sqlite3
import calendar
import logging
import csv
import operator
import json

from datetime import date, datetime
from functools import reduce
from database_handler import DatabaseHandler

logging.basicConfig(level=logging.INFO)

class AssetDeficit(Exception):
    """
    Exception that is raised when there is a mismatch between the amount of assets in the database and the amount of assets in the transactions
    """
    def __init__(self, message, data_parser: 'DataParser') -> None:
        """
        Parameters:
        message (str): The error message to be displayed.
        data_parser (DataParser): The DataParser instance where the error occurred.
        """
        super().__init__(message)
        self.data_parser = data_parser
        logging.error(message)
        data_parser.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")
        logging.error("Unprocessed transactions:")
        for row in data_parser.transaction_cur.fetchall():
            logging.error(row)
        data_parser.db.conn.rollback()

class SpecialCases:
    """
    SpecialCases class handles special cases when adding data to the database. 
    The special cases are defined in a json file as a list of cases with the following structure:
    [{
        "condition": [
            { 
                "index": int, // Integer value of the column
                "value": str // String that the value of the column should be compared to
                ("operator": str) // If index represents a date, then operator needs to be provided
            },
            // ... more conditions ... ]
        },
        "replacement": [
            {
                "index": int, // Integer value of the column
                "value": str // String that the value of the column should be replaced with
            },
            // ... more replacements ... ] 
    } ... more cases ... ]
    """
    def __init__(self, file_path: str):
        """
        Parameters:
        file_path (str): Path to json file containing special cases.
        """
        # Read special cases from json file
        try:
            with open(file_path, "r", encoding="utf-8") as special_cases_file:
                special_cases = json.load(special_cases_file)
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="cp1252") as special_cases_file:
                special_cases = json.load(special_cases_file)

        # Define a mapping from operator strings to functions
        ops = {
            "==": operator.eq,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "!=": operator.ne
        }
        # Create a list of functions that check if a row matches a special case
        # and a list of functions that replace a row with a new row
        special_conditions = []
        special_replacements = []
        for case in special_cases:
            conditions = []
            for condition in case["condition"]:
                index = condition["index"]
                value = condition["value"]
                # If index is 0, then the value is a date encoded as YYYY-MM-DD and needs to be converted to a date object
                if index == 0:
                    value = datetime.strptime(value, "%Y-%m-%d").date()
                op_func = ops.get(condition.get("operator", "=="))  # default to "=="
                # Create a function that checks if a row matches a condition
                # Default values are used to avoid late binding
                conditions.append(lambda x, index=index, op_func=op_func, value=value: op_func(x[index], value))
            special_conditions.append(lambda x, conditions=conditions: all(condition(x) for condition in conditions))
            replacements = []
            for replacement in case["replacement"]:
                index = replacement["index"]
                value = replacement["value"]
                # Create a function that replaces a row with a new row
                # Default values are used to avoid late binding
                replacements.append(lambda x, index=index, value=value: x[:index] + (value,) + x[index + 1:])
            special_replacements.append(reduce(lambda f, g: lambda x: g(f(x)), replacements))

        # Check that special_conditions and special_replacements have the same length
        # If not, raise an error saying there was an error parsing the special cases file
        if len(special_conditions) != len(special_replacements):
            raise ValueError("Error parsing special cases file. Number of conditions and replacements do not match.")

        # Combine special_conditions and special_replacements into a single list
        self.special_cases = list(zip(special_conditions, special_replacements))

    #Check if a row matches a special case
    def handle_special_cases(self, row: list):
        """
        Takes a row from the csv file as a list and does replacements if the row matches a special case.

        Parameters:
        row (list): A row from the csv file.

        Returns:
        list: The same row after replacements have been made.
        """
        for i in range(len(self.special_cases)):
            #Special conditions are functions that check if a row matches a special case
            #They are stored in the first element of the special_cases list
            if self.special_cases[i][0](row):
                #Special replacements are functions that replace a row with a new row
                #They are stored in the second element of the special_cases list
                row = self.special_cases[i][1](row)
        return row

class DataParser:
    """
    DataParser class handles the processing of transactions in the database.
    """
    def __init__(self, db: DatabaseHandler, special_cases: SpecialCases = None):
        """
        Parameters:
        database (DatabaseHandler): The database to add data to.
        special_cases (SpecialCases): SpecialCases object that handles special rules when adding data to the database.
        """
        self.listing_change = {"to_asset":None,"to_asset_amount":None,"to_rowid":None}
        self.pending_transfer = {"rowid": None, "account": None, "amount": None, "date": None}
        self.db = db
        self.special_cases = special_cases
        # Two cursors are used, one for handling writing processed lines and one responsible for keeping track of unprocessed lines
        self._data_cur = None
        self._transaction_cur = None

    # Getter function for self.data_cur
    @property
    def data_cur(self) -> sqlite3.Cursor:
        """
        Returns:
        sqlite3.Cursor: Cursor for creating new transactions in the database.
        """
        # If self._data_cursor is None, ask the database for a cursor
        if self._data_cur is None:
            self._data_cur = self.db.get_cursor()
        return self._data_cur
    
    # Getter function for self.transaction_cur
    @property
    def transaction_cur(self) -> sqlite3.Cursor:
        """
        Returns:
        sqlite3.Cursor: Cursor for iterating over transactions in the database.
        """
        # If self._transaction_cur is None, ask the database for a cursor
        if self._transaction_cur is None:
            self._transaction_cur = self.db.get_cursor()
        return self._transaction_cur


    @staticmethod
    def _to_sek_price(row: tuple) -> float:
        """Compute the SEK per-share price from a transaction row.

        The Avanza CSV stores `total` and `courtage` in SEK (already
        FX-converted), while `price` is in the instrument's native currency.
        For buy/sell (total != 0) we derive the SEK market price from the
        total, correcting for courtage:
            sell (total > 0): sek_price = (total + courtage) / abs(amount)
            buy  (total < 0): sek_price = (abs(total) - courtage) / abs(amount)
        For total == 0 (Tillgångsinsättning) the SEK price cannot be derived
        from the row alone — the native price is returned and will be
        corrected by the next update_prices run for non-SEK instruments.
        """
        amount = row[4]
        price = row[5]
        total = row[6]
        courtage = row[7] if row[7] is not None else 0.0
        if abs(amount) < 0.0001 or abs(total) < 0.0001:
            return price
        sek_market_value = abs(total) + (courtage if total > 0 else -courtage)
        return sek_market_value / abs(amount)

    def convert_number(self,number_string : str) -> float:
        """
        Takes a number as a string and converts it to a float, also converts comma to dot as decimal separator and '-' to 0.
        
        Parameters:
        number_string (str): A number as a string.

        Returns:
        float: The number as a float.
        """
        return 0.0 if number_string in ("-", "") else float(number_string.replace(",","."))
    
    def _is_unsettled_trade(self, transaction) -> bool:
        """Heuristic for an unsettled trade (pending nota) in new-format CSV.

        Avanza includes preliminary same-day buys/sells whose brokerage and FX
        conversion are not yet finalized; they appear with empty Courtage and
        empty Valutakurs for non-SEK instruments. Restricted to non-SEK so that
        legitimate SEK zero-courtage trades are never flagged (issue #78).
        """
        if len(transaction) < 10:
            return False
        if transaction[2] not in ('Köp', 'Sälj'):
            return False
        if transaction[7] == 'SEK':
            return False
        courtage_unset = self.convert_number(transaction[8]) == 0.0
        valutakurs_unset = str(transaction[9]).strip() in ('', '-')
        return courtage_unset and valutakurs_unset

    def add_data(self, file_path: str, allow_unsettled: bool = False) -> int:
        """
        Takes a path to a csv file downloaded from Avanza and adds the data to the database.
        Uses group-level deduplication to match split/combined transactions.

        Parameters:
        file_path (str): Path to csv file downloaded from Avanza.

        Returns:
        int: Number of rows added to the database.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as avanza_data_file:
                avanza_data = csv.reader(avanza_data_file, delimiter=';')
                avanza_header_row = next(avanza_data)
                new_format = "Transaktionsvaluta" in avanza_header_row
                avanza_data = list(avanza_data)
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="cp1252") as avanza_data_file:
                avanza_data = csv.reader(avanza_data_file, delimiter=';')
                avanza_header_row = next(avanza_data)
                new_format = "Transaktionsvaluta" in avanza_header_row
                avanza_data = list(avanza_data)

        max_date = max([datetime.strptime(row[0],"%Y-%m-%d") for row in avanza_data]).date()
        min_date = min([datetime.strptime(row[0],"%Y-%m-%d") for row in avanza_data]).date()
        logging.debug("Date range of transactions to be added: {} - {}".format(min_date,max_date))

        rows_added = 0
        self.db.connect()
        cur = self.db.conn.cursor()

        # Virtual accounts map onto their parent for dedup matching, so that a
        # transaction allocated to a virtual portfolio is still recognised as
        # "already imported" when the source CSV is re-imported on the parent
        # account. (See issue #74 prestudy #2 — parent-remap, not account-agnostic.)
        virtual_map = self.db.get_virtual_map()

        # 1. Fetch existing REAL transactions in the date range. Synthetic rows
        #    (origin = 'virtual') are excluded: they are never re-imported from
        #    CSV and must not shadow or be shadowed by real re-imports.
        existing_transactions = cur.execute(
            "SELECT date, account, transaction_type, asset_name, amount, price, isin "
            "FROM transactions "
            "WHERE date >= ? AND date <= ? AND (origin = 'avanza' OR origin IS NULL)",
            (min_date, max_date)
        ).fetchall()

        # 2. Group existing transactions in DB, remapping each virtual account
        #    back to its parent so allocated rows collapse onto the parent key
        #    that the proposed CSV groups use.
        existing_groups = {}
        for tx in existing_transactions:
            # tx: (date, account, transaction_type, asset_name, amount, price, isin)
            # key: (date, account_for_key, transaction_type, isin_or_asset_name)
            isin_val = tx[6]
            asset_name = tx[3]
            account_for_key = virtual_map.get(tx[1], tx[1])
            key = (tx[0], account_for_key, tx[2], isin_val if (isin_val and isin_val.strip()) else asset_name)
            if key not in existing_groups:
                existing_groups[key] = []
            existing_groups[key].append(tx)

        # 3. Parse and group proposed CSV transactions
        proposed_groups = {}
        unsettled_skipped = []
        for transaction in avanza_data:
            # Defer unsettled trades (pending nota): same-day exports of non-SEK
            # buys/sells can have empty Courtage and Valutakurs because brokerage
            # and FX conversion are not yet finalized. Ingesting them would store
            # rows with zero courtage and incomplete totals. Skip and warn so the
            # user re-exports after settlement and re-imports (issue #78).
            if new_format and not allow_unsettled and self._is_unsettled_trade(transaction):
                unsettled_skipped.append(transaction)
                continue
            if new_format:
                row = (
                    datetime.strptime(transaction[0], "%Y-%m-%d").date(),
                    transaction[1], transaction[2], transaction[3].strip(),
                    self.convert_number(transaction[4]), self.convert_number(transaction[5]),
                    self.convert_number(transaction[6]), self.convert_number(transaction[8]),
                    transaction[7], transaction[11]
                )
            else:
                row = (
                    datetime.strptime(transaction[0], "%Y-%m-%d").date(),
                    transaction[1], transaction[2], transaction[3].strip(),
                    self.convert_number(transaction[4]), self.convert_number(transaction[5]),
                    self.convert_number(transaction[6]), self.convert_number(transaction[7]),
                    transaction[8], transaction[9]
                )

            if self.special_cases is not None:
                row = self.special_cases.handle_special_cases(row)

            isin_val = row[9]
            asset_name = row[3]
            key = (row[0], row[1], row[2], isin_val if (isin_val and isin_val.strip()) else asset_name)

            if key not in proposed_groups:
                proposed_groups[key] = []
            proposed_groups[key].append(row)

        if unsettled_skipped:
            logging.warning(
                f"Skipping {len(unsettled_skipped)} unsettled trade(s) with pending nota "
                f"(empty Courtage/Valutakurs on non-SEK buy/sell). "
                f"Re-export after settlement and re-import:"
            )
            for tx in unsettled_skipped:
                logging.warning(f"  skipped: {tx[0]} {tx[1]} {tx[2]} '{tx[3]}'")

        # 4. Perform group-level matching and insertion
        for key, proposed_rows in proposed_groups.items():
            existing_rows = existing_groups.get(key, [])

            if not existing_rows:
                # No existing transactions in this group, insert all
                for row in proposed_rows:
                    logging.debug("Adding row to database: {}".format(row))
                    cur.execute('INSERT INTO transactions(date, account, transaction_type,asset_name,amount,price,total,courtage,currency,isin) VALUES(?,?,?,?,?,?,?,?,?,?);', row)
                    rows_added += 1
            else:
                # Compare sum of amount
                sum_proposed = sum(row[4] for row in proposed_rows)
                sum_existing = sum(tx[4] for tx in existing_rows)

                if abs(sum_proposed - sum_existing) < 1e-4:
                    # Group matches, skip duplicate
                    logging.debug(f"Skipping duplicate transaction group for key {key} (proposed sum: {sum_proposed}, existing sum: {sum_existing})")
                    continue
                else:
                    # Sums do not match, fall back to exact row-by-row matching
                    for row in proposed_rows:
                        matched = False
                        for tx in existing_rows:
                            # Match amount and price
                            if abs(row[4] - tx[4]) < 1e-4 and abs(row[5] - tx[5]) < 1e-4:
                                matched = True
                                break
                        if not matched:
                            logging.debug("Adding row to database: {}".format(row))
                            cur.execute('INSERT INTO transactions(date, account, transaction_type,asset_name,amount,price,total,courtage,currency,isin) VALUES(?,?,?,?,?,?,?,?,?,?);', row)
                            rows_added += 1

        self.db.conn.commit()
        self.db.disconnect()
        logging.info("Added {} rows to the database".format(rows_added))
        return rows_added
    
    def reset_processed_transactions(self) -> None:
        """
        Resets the processed flag for all transactions in the database. Also resets cohort_data, cohort_assets, assets, cohort_cash_flows and asset_prices tables.
        """
        self.data_cur.execute("UPDATE transactions SET processed = 0")
        self.db.reset_table("cohort_data")
        self.db.reset_table("cohort_assets")
        self.db.reset_table("assets")
        self.db.reset_table("cohort_cash_flows")
        self.db.reset_table("asset_prices")
        self.db.commit()

    def reset_for_reprocessing(self) -> None:
        """
        Reset cohort tables and the processed flag so the next
        ``process_transactions`` call performs a full clean rebuild.

        Unlike ``reset_processed_transactions`` this preserves the
        ``asset_prices`` table so that externally-fetched historical prices
        are not wiped out on every import.
        """
        self.data_cur.execute("UPDATE transactions SET processed = 0")
        self.db.reset_table("cohort_data")
        self.db.reset_table("cohort_assets")
        self.db.reset_table("assets")
        self.db.reset_table("cohort_cash_flows")
        self.db.commit()

    @staticmethod
    def allocate_to_month(transaction_date: date) -> date:
        """
        Takes a date and returns which month the transaction should be allocated to.
        If the transaction is made within the first cutoff_days of the month, allocate it to the previous month.

        Parameters:
        transaction_date (date): The date of the transaction.

        Returns:
        date: The date of the month the transaction should be allocated to.
        """
        cutoff_days = 10
        day = transaction_date.day
        month = transaction_date.month
        year = transaction_date.year

        if day <= cutoff_days:
            if month > 1:
                month = month - 1
            else:
                month = 12
                year = year - 1
        
        day = calendar.monthrange(year,month)[1]
        return date(year,month,day)

    def cohort_value(self, cohort_month, account: str, as_of_date = None) -> float:
        """
        Calculate the estimated value of a cohort (month + account).
        Value = cash (capital) + sum(asset_amount * price).
        Uses asset_prices history if as_of_date is provided, otherwise latest_price.

        Parameters:
        cohort_month: The cohort month date.
        account (str): The account name.
        as_of_date: Resolve prices as of this date.

        Returns:
        float: Estimated cohort value.
        """
        # Get cash for this cohort
        row = self.data_cur.execute(
            "SELECT capital FROM cohort_data WHERE month = ? AND account = ?",
            (cohort_month, account)
        ).fetchone()
        cash = row[0] if row else 0.0

        # Get asset holdings for this cohort
        cursor = self.data_cur.execute("""
            SELECT ma.asset_id, ma.amount, ma.average_price, a.latest_price
            FROM cohort_assets ma
            JOIN assets a ON ma.asset_id = a.asset_id
            WHERE ma.month = ? AND ma.account = ? AND ma.amount > 0
        """, (cohort_month, account))
        holdings = cursor.fetchall()

        asset_value = 0.0
        for asset_id, amount, avg_price, latest_price in holdings:
            if as_of_date is not None:
                price, _, _, _ = self.db.get_price(asset_id, as_of_date)
            else:
                price, _, _, _ = self.db.get_price(asset_id, None)

            if price <= 0.0001:
                price = avg_price if avg_price is not None else 0.0

            asset_value += amount * price

        return cash + asset_value

    def available_capital(self, account: str) -> list:
        """
        Get available capital for a specific account.
        Returns list of (month, capital) tuples ordered oldest first.

        Parameters:
        account (str): Account name to get capital for.

        Returns:
        list: List of (month, capital) tuples with capital > 0 for that account.
        """
        res = self.data_cur.execute(
            "SELECT month, capital FROM cohort_data WHERE account = ? AND capital > 0 ORDER BY month ASC",
            (account,)
        ).fetchall()
        return res if res else [(None, 0)]

    def available_asset(self, asset_id: int, account: str = None) -> list:
        """
        Get available assets for each recorded month. If there is no recorded month, return (None,0).
        
        Parameters:
        asset_id (int): The id of the asset to get available assets for.
        account (str, optional): The account to filter by. If None, returns assets for all accounts.

        Returns:
        list: List of tuples with the first element being the month and the second element being the amount of available assets for that month.
        """
        if account:
            res = self.data_cur.execute("SELECT month, amount FROM cohort_assets WHERE amount > 0 AND asset_id = ? AND account = ? ORDER BY month ASC",(asset_id, account)).fetchall()
        else:
            res = self.data_cur.execute("SELECT month, amount FROM cohort_assets WHERE amount > 0 AND asset_id = ? ORDER BY month ASC",(asset_id,)).fetchall()
        
        if len(res) > 0:
            return res
        else:
            return [(None,0)]

    def handle_deposit(self, row: tuple) -> None:
        """
        Takes a transaction row and adds the amount to the capital of the month the transaction is allocated to.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        month = self.allocate_to_month(row[0])
        amount = row[6]
        account = row[1]
        self.data_cur.execute("INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)", (month, account))
        self.data_cur.execute("UPDATE cohort_data SET capital = capital + ?, deposit = deposit + ?, active_base = active_base + ? WHERE month = ? AND account = ?", (amount, amount, amount, month, account))
        # Reset transaction_cur since new funds are available
        self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
        self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_withdrawal(self, row: tuple) -> None:
        """
        Takes a transaction row and subtracts the amount from the capital of the oldest month(s) with available capital.
        Logs each partial allocation to cohort_cash_flows, aggregated by the transaction's month.
        If there is not enough total capital available, the transaction is not processed.
        In per-account mode, only uses capital from the same account.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        total_amount = -row[6]
        remaining_amount = total_amount
        account = row[1]
        transaction_date = row[0]
        transaction_month = self.allocate_to_month(transaction_date)
        
        month_capital = self.available_capital(account)
        total_capital = sum(e[1] for e in month_capital)
        if total_capital + 1e-4 >= total_amount:
            i = 0
            while remaining_amount > 1e-4:
                (oldest_available,capital) = month_capital[i]
                month_amount = min(remaining_amount,capital)

                # Calculate withdrawal fraction R and reduce active_base proportionally
                cv = self.cohort_value(oldest_available, account, as_of_date=transaction_date)
                if cv > 1e-4:
                    r = month_amount / cv
                    r = min(r, 1.0)  # Cap at 100%
                    # Snapshot TWRR before zeroing active_base on full withdrawal
                    if r >= 1.0 - 1e-6:
                        ab_row = self.data_cur.execute(
                            "SELECT active_base FROM cohort_data WHERE month = ? AND account = ?",
                            (oldest_available, account)).fetchone()
                        ab = ab_row[0] if ab_row and ab_row[0] else 0.0
                        if ab > 1e-4:
                            self.data_cur.execute(
                                "UPDATE cohort_data SET closed_return = ? WHERE month = ? AND account = ?",
                                (cv / ab, oldest_available, account))
                    self.data_cur.execute(
                        "UPDATE cohort_data SET active_base = active_base * (1 - ?) WHERE month = ? AND account = ?",
                        (r, oldest_available, account))

                self.data_cur.execute("UPDATE cohort_data SET capital = capital - ?, withdrawal = withdrawal + ? WHERE month = ? AND account = ?", (month_amount, month_amount, oldest_available, account))
                
                # Aggregate cash flow for the cohort in the transaction month
                self.data_cur.execute("""
                    INSERT INTO cohort_cash_flows (cohort_month, account, transaction_month, amount)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(cohort_month, account, transaction_month)
                    DO UPDATE SET amount = amount + excluded.amount
                """, (oldest_available, account, transaction_month, -month_amount))
                
                remaining_amount -= month_amount
                i += 1
            self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
            self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_purchase(self, row: tuple) -> None: 
        """
        Takes a transaction row and subtracts the purchase amount from the capital of the oldest month(s) with available capital.
        Then allocates a proportional amount of the asset to those months.
        If there is not enough total capital available, the transaction is not processed.
        In per-account mode, only uses capital from the same account.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        asset = row[3]
        account = row[1]
        self.data_cur.execute("INSERT OR IGNORE INTO assets (asset) VALUES (?) ",(asset,))
        asset_id = self.data_cur.execute("SELECT asset_id FROM assets WHERE asset = ?",(asset,)).fetchone()[0]
        asset_amount = row[4]
        price = self._to_sek_price(row)
        total_amount = -row[6]
        date = row[0]
        if price > 0:
            self.data_cur.execute("UPDATE assets SET latest_price = ?, latest_price_date = ? WHERE asset_id = ?", (price, date, asset_id))
            self.data_cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (?, ?, ?, 'transaction')", (asset_id, date, price))
        remaining_amount = total_amount
        month_capital = self.available_capital(account)
        total_capital = sum(e[1] for e in month_capital)
        if total_capital + 1e-3 >= total_amount:
            i = 0
            while remaining_amount > 1e-3:
                (oldest_available,capital) = month_capital[i]
                month_amount = min(remaining_amount,capital)
                month_asset_amount = month_amount / total_amount * asset_amount
                self.data_cur.execute("UPDATE cohort_data SET capital = capital - ? WHERE month = ? AND account = ?", (month_amount, oldest_available, account))
                self.data_cur.execute("INSERT OR IGNORE INTO cohort_assets(month,asset_id,account) VALUES (?,?,?)",(oldest_available,asset_id,account))
                self.data_cur.execute("UPDATE cohort_assets SET average_price = ?/(amount+?)*?+amount/(amount+?)*average_price WHERE month = ? AND asset_id = ? AND account = ?",(month_amount,month_amount,price,month_amount,oldest_available,asset_id,account))
                self.data_cur.execute("UPDATE cohort_assets SET average_purchase_price = ?/(purchased_amount+?)*?+purchased_amount/(purchased_amount+?)*average_purchase_price WHERE month = ? AND asset_id = ? AND account = ?",(month_amount,month_amount,price,month_amount,oldest_available,asset_id,account))
                self.data_cur.execute("UPDATE cohort_assets SET amount = amount + ?, purchased_amount = purchased_amount + ? WHERE month = ? AND asset_id = ? AND account = ?",(month_asset_amount, month_asset_amount, oldest_available,asset_id,account))
                remaining_amount -= month_amount
                i += 1
            # Reset transaction_cur since new assets are available
            self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
            self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")
 
    def handle_sale(self, row: tuple) -> None:
        """
        Takes a transaction row and subtracts the sale asset amount from the oldest month(s) with that available asset.
        Then adds the sale amount to the capital of those months.
        If there is not enough total assets available, the transaction is not processed.
        In per-account mode, sale proceeds are returned to the selling account's capital for those months.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        asset = row[3]
        account = row[1]
        self.data_cur.execute("INSERT OR IGNORE INTO assets (asset) VALUES (?) ",(asset,))
        asset_id = self.data_cur.execute("SELECT asset_id FROM assets WHERE asset = ?",(asset,)).fetchone()[0]
        asset_amount = -row[4]
        price = self._to_sek_price(row)
        total_amount = row[6]
        date = row[0]
        if price > 0:
            self.data_cur.execute("UPDATE assets SET latest_price = ?, latest_price_date = ? WHERE asset_id = ?", (price, date, asset_id))
            self.data_cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (?, ?, ?, 'transaction')", (asset_id, date, price))
        remaining_amount = asset_amount
        month_asset_amounts = self.available_asset(asset_id, account)

        total_asset_amount = sum(e[1] for e in month_asset_amounts)
        
        # FIX: Check if we are selling an asset with 0 average purchase price (cost_basis=0)
        # If so, retroactively inject the sale total_amount as a deposit in the month the shares were acquired
        for (oldest_available, amount) in month_asset_amounts:
            # Check if this cohort has 0 active base (deposit) for these shares
            res = self.data_cur.execute(
                "SELECT average_purchase_price FROM cohort_assets WHERE month = ? AND asset_id = ? AND account = ?",
                (oldest_available, asset_id, account)
            ).fetchone()
            if res and res[0] == 0.0:
                # Calculate the proportionate sale amount for these specific shares
                proportionate_sale_amount = (amount / asset_amount) * total_amount if asset_amount > 0 else 0
                if proportionate_sale_amount > 0:
                    # Retroactively create a deposit in that month
                    self.data_cur.execute(
                        "UPDATE cohort_data SET deposit = deposit + ?, active_base = active_base + ? WHERE month = ? AND account = ?",
                        (proportionate_sale_amount, proportionate_sale_amount, oldest_available, account)
                    )
                    # Update average purchase price so we don't trigger this again for a partial sale
                    proportionate_price = proportionate_sale_amount / amount
                    self.data_cur.execute(
                        "UPDATE cohort_assets SET average_purchase_price = ? WHERE month = ? AND asset_id = ? AND account = ?",
                        (proportionate_price, oldest_available, asset_id, account)
                    )

        if total_asset_amount + 1e-3 >= asset_amount:

            i = 0
            while remaining_amount > 1e-3:
                (oldest_available,amount) = month_asset_amounts[i]
                month_amount = min(remaining_amount,amount)
                month_capital_amount = month_amount / asset_amount * total_amount
                self.data_cur.execute("UPDATE cohort_assets SET average_sale_price = ?/(sold_amount+?)*?+sold_amount/(sold_amount+?)*average_sale_price WHERE month = ? AND asset_id = ? AND account = ?",(month_amount,month_amount,price,month_amount,oldest_available,asset_id,account))
                self.data_cur.execute("UPDATE cohort_assets SET amount = amount - ?, sold_amount = sold_amount + ? WHERE month = ? AND asset_id = ? AND account = ?",(month_amount, month_amount, oldest_available,asset_id,account))
                self.data_cur.execute("INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)", (oldest_available, account))
                self.data_cur.execute("UPDATE cohort_data SET capital = capital + ? WHERE month = ? AND account = ?", (month_capital_amount, oldest_available, account))
                remaining_amount -= month_amount
                i += 1
            # Reset transaction_cur since new funds are available
            self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
            self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_dividend(self, row: tuple) -> None:
        """
        Takes a transaction row and adds the dividend amount proporionally to the capital of all the month(s) with that available asset.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        dividend_month = self.allocate_to_month(row[0])
        account = row[1]
        asset = row[3]
        result = self.data_cur.execute("SELECT asset_id FROM assets WHERE asset = ?",(asset,)).fetchone()
        if result is None:
            self.data_cur.execute("INSERT OR IGNORE INTO assets (asset) VALUES (?) ",(asset,))
            result = self.data_cur.execute("SELECT asset_id FROM assets WHERE asset = ?",(asset,)).fetchone()
        asset_id = result[0]
        remaining_amount = row[4]
        # Per-share rate used to credit capital. The price column (row[5]) is
        # in the instrument's native currency while `total` (row[6]) is in
        # SEK, so crediting shares * price silently mixes currencies for
        # foreign-currency dividends (issue #85). Derive the SEK per-share
        # rate from the SEK total instead; fall back to the price column only
        # when the amount is zero or missing.
        if abs(row[4]) > 1e-6 and abs(row[6]) > 1e-6:
            dividend_per_asset = abs(row[6]) / abs(row[4])
        else:
            dividend_per_asset = row[5]
        month_asset_amounts = self.available_asset(asset_id, account)
        for (month,asset_amount) in month_asset_amounts:
                self.data_cur.execute("INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)", (month, account))
                self.data_cur.execute("UPDATE cohort_data SET capital = capital + ? WHERE month = ? AND account = ?", (asset_amount*dividend_per_asset, month, account))
                remaining_amount -= asset_amount
        if remaining_amount > 0:
            self.data_cur.execute("INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)", (dividend_month, account))
            self.data_cur.execute("UPDATE cohort_data SET capital = capital + ? WHERE month = ? AND account = ?", (remaining_amount*dividend_per_asset, dividend_month, account))
        # Reset transaction_cur since new funds are available
        self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
        self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_interest(self, row: tuple) -> None:
        """
        Takes a transaction row and adds the interest amount proportionally to the capital of all month(s) with available capital.
        In per-account mode, distributes only within the account's own capital, so savings account
        interest stays attributed to savings account months (not leaked to investment account months).

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        dividend_month = self.allocate_to_month(row[0])
        account = row[1]
        remaining_amount = row[6]
        month_capital = self.available_capital(account)
        total_capital = sum([month[1] for month in month_capital])
        dividend_per_capital = remaining_amount / total_capital
        for (month, capital) in month_capital:
            amount_added = capital * dividend_per_capital
            self.data_cur.execute("INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)", (month, account))
            self.data_cur.execute("UPDATE cohort_data SET capital = capital + ? WHERE month = ? AND account = ?", (amount_added, month, account))
            remaining_amount -= amount_added
        if remaining_amount > 0:
            self.data_cur.execute("INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)", (dividend_month, account))
            self.data_cur.execute("UPDATE cohort_data SET capital = capital + ? WHERE month = ? AND account = ?", (remaining_amount, dividend_month, account))
        # Reset transaction_cur since new funds are available
        self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
        self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_fees(self, row: tuple) -> None:
        """
        Takes a transaction row and subtracts the fee amount from the capital of the oldest month(s) with available capital.
        Logs each partial allocation to cohort_cash_flows, aggregated by the transaction's month.
        If there is not enough total capital available, the transaction is not processed.
        In per-account mode, only uses capital from the same account.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        total_amount = -row[6]
        remaining_amount = total_amount
        account = row[1]
        transaction_date = row[0]
        transaction_month = self.allocate_to_month(transaction_date)
        
        month_capital = self.available_capital(account)
        total_capital = sum(e[1] for e in month_capital)
        if total_capital + 1e-4 >= total_amount:
            i = 0
            while remaining_amount > 1e-4:
                (oldest_available,capital) = month_capital[i]
                month_amount = min(remaining_amount,capital)
                self.data_cur.execute("UPDATE cohort_data SET capital = capital - ? WHERE month = ? AND account = ?", (month_amount, oldest_available, account))
                
                # Aggregate fee cash flow for the cohort in the transaction month
                self.data_cur.execute("""
                    INSERT INTO cohort_cash_flows (cohort_month, account, transaction_month, amount)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(cohort_month, account, transaction_month)
                    DO UPDATE SET amount = amount + excluded.amount
                """, (oldest_available, account, transaction_month, -month_amount))
                
                remaining_amount -= month_amount
                i += 1
            self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
            self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_listing_change(self, row: tuple) -> None:
        """
        Takes a transaction row and changes the asset name and amount.
        The first time the function is called, the old asset name and amount is saved and the transaction is not processed.
        The second time the function is called, the old asset name and amount is changed to the new asset name and amount and both transactions are marked as processed.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """  
        if self.listing_change["to_asset"] is None:
            self.listing_change["to_asset"] = row[3]
            self.listing_change["to_asset_amount"] = row[4]
            self.listing_change["to_rowid"] = row[-1]
        else:
            asset = row[3]
            amount = -row[4]
            (asset_id,) = self.data_cur.execute("SELECT asset_id FROM assets WHERE asset = ?",(asset,)).fetchone()
            self.data_cur.execute("UPDATE assets SET asset = ?, amount = ? WHERE asset_id = ?",(self.listing_change["to_asset"],self.listing_change["to_asset_amount"],asset_id))
            change_factor = self.listing_change["to_asset_amount"]/amount
            self.data_cur.execute("UPDATE cohort_assets SET amount = amount * ? WHERE asset_id = ?",(change_factor,asset_id))
            self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ? OR rowid = ?",(row[-1],self.listing_change["to_rowid"],))
            self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")
            self.listing_change = {"to_asset":None,"to_asset_amount":None,"to_rowid":None}
    
    def handle_asset_deposit(self, row: tuple) -> None:
        """
        Takes a transaction row and adds the amount to the assets of the month the transaction is allocated to.
        Counts as a deposit for the month the transaction is allocated to so the price is also added to the deposit of that month.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        month = self.allocate_to_month(row[0])
        account = row[1]
        asset = row[3]
        amount = row[4]
        price = self._to_sek_price(row)
        self.data_cur.execute("INSERT OR IGNORE INTO assets (asset) VALUES (?) ",(asset,))
        asset_id = self.data_cur.execute("SELECT asset_id FROM assets WHERE asset = ?",(asset,)).fetchone()[0]
        date = row[0]
        
        # Historical price lookup for transactions lacking price
        if price <= 0.0001:
            res_price, is_interp, gap, res_date = self.db.get_price(asset_id, date)
            if res_price > 0.0001:
                price = res_price
                desc = "interpolated" if is_interp else f"as of {res_date}"
                logging.info(f"Resolved missing price for {asset} on {date} using get_price ({price} {desc})")
                self.data_cur.execute("UPDATE transactions SET price = ? WHERE rowid = ?", (price, row[-1]))

        # Only record a price point if we have a usable (> 0) price, so that
        # an unresolved deposit does not poison asset_prices / latest_price
        # with a literal 0.0 that would cause the asset to be silently valued
        # at zero until a real price appears.
        if price > 0:
            self.data_cur.execute("UPDATE assets SET latest_price = ?, latest_price_date = ? WHERE asset_id = ?", (price, date, asset_id))
            self.data_cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (?, ?, ?, 'transaction')", (asset_id, date, price))
        self.data_cur.execute("INSERT OR IGNORE INTO cohort_assets(month,asset_id,account) VALUES (?,?,?)",(month,asset_id,account))
        # Update average price and average purchase price
        self.data_cur.execute("UPDATE cohort_assets SET average_price = (? * ? + amount * average_price) / (amount + ?) WHERE month = ? AND asset_id = ? AND account = ?", (amount, price, amount, month, asset_id, account))
        self.data_cur.execute("UPDATE cohort_assets SET average_purchase_price = (? * ? + purchased_amount * average_purchase_price) / (purchased_amount + ?) WHERE month = ? AND asset_id = ? AND account = ?", (amount, price, amount, month, asset_id, account))
        # Update amount and purchased amount
        self.data_cur.execute("UPDATE cohort_assets SET amount = amount + ? WHERE month = ? AND asset_id = ? AND account = ?",(amount,month,asset_id,account))
        self.data_cur.execute("INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)", (month, account))
        self.data_cur.execute("UPDATE cohort_data SET deposit = deposit + ?, active_base = active_base + ? WHERE month = ? AND account = ?", (amount*price, amount*price, month, account))
        # Reset transaction_cur since new assets are available
        self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?",(row[-1],))
        self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_ignore(self, row: tuple) -> None:
        """
        Marks a transaction as processed without any further action.
        Used for negligible transactions like tiny fraction write-offs.
        
        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        logging.debug(f"Ignoring transaction {row[0]} {row[2]} {row[3]} with amount {row[6]}")
        self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?", (row[-1],))
        self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")

    def handle_internal_transfer(self, row: tuple) -> None:
        """
        Handles 'Intern överföring' (internal transfer between accounts).
        Processes transfers in pairs (OUT and IN) to preserve FIFO month attribution.
        Logs resulting cash flow events to cohort_cash_flows, aggregated by the transaction's month.

        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        # Handle standalone incoming transfers from external accounts not tracked in DB
        if row[6] > 0 and "Insättning från" in str(row[3]):
            # Incoming transfer from external account not tracked in DB
            # Treat as deposit to provide capital for subsequent purchases
            self.handle_deposit(row)
            return
        
        if self.pending_transfer["rowid"] is None:
            # First of pair
            self.pending_transfer["rowid"] = row[-1]
            self.pending_transfer["account"] = row[1]
            self.pending_transfer["amount"] = row[6]
            self.pending_transfer["date"] = row[0]
            # Don't mark processed yet
            return
        
        # Second of pair
        first_rowid = self.pending_transfer["rowid"]
        second_rowid = row[-1]
        
        # Determine OUT (-) and IN (+)
        if self.pending_transfer["amount"] < 0:
            out_account = self.pending_transfer["account"]
            out_amount = -self.pending_transfer["amount"]
            out_date = self.pending_transfer["date"]
            out_rowid = self.pending_transfer["rowid"]
            
            in_account = row[1]
            in_amount = row[6]
            in_date = row[0]
            in_rowid = row[-1]
        else:
            out_account = row[1]
            out_amount = -row[6]
            out_date = row[0]
            out_rowid = row[-1]
            
            in_account = self.pending_transfer["account"]
            in_amount = self.pending_transfer["amount"]
            in_date = self.pending_transfer["date"]
            in_rowid = self.pending_transfer["rowid"]

        # Issue #82: parent->virtual transfers shift the deposit column (so the
        # virtual inherits real deposit attribution for APY/display) instead of
        # transfer_net. Physical-to-physical transfers keep transfer_net.
        vr = self.data_cur.execute(
            "SELECT is_virtual, parent_account FROM accounts WHERE account_id = ?",
            (in_account,),
        ).fetchone()
        parent_to_virtual = bool(vr and vr[0] and vr[1] == out_account)
        shift_col = "deposit" if parent_to_virtual else "transfer_net"

        # Get FIFO allocations from OUT account (following withdrawal pattern)
        month_capital = self.available_capital(out_account)
        total_capital = sum(e[1] for e in month_capital)
        
        if total_capital + 1e-4 >= out_amount:
            allocations = []
            remaining = out_amount
            i = 0
            
            out_transaction_month = self.allocate_to_month(out_date)
            
            while remaining > 1e-4:
                (oldest_available, capital) = month_capital[i]
                month_amount = min(remaining, capital)
                allocations.append((oldest_available, month_amount))
                
                # Calculate withdrawal fraction R and reduce active_base for OUT account
                cv = self.cohort_value(oldest_available, out_account, as_of_date=out_date)
                if cv > 1e-4:
                    r = month_amount / cv
                    r = min(r, 1.0)
                    self.data_cur.execute(
                        "UPDATE cohort_data SET active_base = active_base * (1 - ?) WHERE month = ? AND account = ?",
                        (r, oldest_available, out_account))

                # Remove from OUT account. shift_col is 'deposit' for
                # parent->virtual (issue #82) and 'transfer_net' otherwise.
                self.data_cur.execute(
                    f"UPDATE cohort_data SET capital = capital - ?, {shift_col} = {shift_col} - ? WHERE month = ? AND account = ?",
                    (month_amount, month_amount, oldest_available, out_account)
                )

                # Deposits do not produce cohort_cash_flows (only withdrawals do),
                # so skip the cash-flow row on the deposit-shift path; otherwise
                # the Modified Dietz denominator (deposit + sum_w_cf) double-counts.
                if not parent_to_virtual:
                    self.data_cur.execute("""
                        INSERT INTO cohort_cash_flows (cohort_month, account, transaction_month, amount)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(cohort_month, account, transaction_month)
                        DO UPDATE SET amount = amount + excluded.amount
                    """, (oldest_available, out_account, out_transaction_month, -month_amount))
                
                remaining -= month_amount
                i += 1
            
            # Add to IN account in same months
            in_transaction_month = self.allocate_to_month(in_date)
            for oldest_available, amount in allocations:
                self.data_cur.execute(
                    "INSERT OR IGNORE INTO cohort_data(month, account) VALUES(?,?)",
                    (oldest_available, in_account)
                )
                # Add to IN account. shift_col is 'deposit' for parent->virtual
                # (issue #82) and 'transfer_net' otherwise.
                self.data_cur.execute(
                    f"UPDATE cohort_data SET capital = capital + ?, active_base = active_base + ?, {shift_col} = {shift_col} + ? WHERE month = ? AND account = ?",
                    (amount, amount, amount, oldest_available, in_account)
                )

                if not parent_to_virtual:
                    self.data_cur.execute("""
                        INSERT INTO cohort_cash_flows (cohort_month, account, transaction_month, amount)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(cohort_month, account, transaction_month)
                        DO UPDATE SET amount = amount + excluded.amount
                    """, (oldest_available, in_account, in_transaction_month, amount))
            
            # Mark BOTH processed
            self.transaction_cur.execute(
                "UPDATE transactions SET processed = 1 WHERE rowid = ? OR rowid = ?",
                (first_rowid, second_rowid)
            )
            logging.debug(f"Internal transfer pair processed: {out_amount} from {out_account} to {in_account}")
        
        else:
            # Insufficient capital - defer the entire pair
            logging.debug(
                f"Internal transfer pair deferred: account {out_account} needs {out_amount}, has {total_capital}"
            )
            # Reset pending transfer so both transactions stay unprocessed
            # They'll be retried later when capital becomes available
            self.pending_transfer = {"rowid": None, "account": None, "amount": None, "date": None}
            return
        
        # Reset pending transfer
        self.pending_transfer = {"rowid": None, "account": None, "amount": None, "date": None}
        
        # Reset cursor since we marked transactions processed
        self.transaction_cur.execute(
            "SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC"
        )

    def handle_remove_shares(self, row: tuple) -> None:
        """
        Removes shares from portfolio without affecting capital (for Byte transactions).
        Used for Värdepappersuttag with negative amount.
        
        Parameters:
        row (tuple): A row from the transactions table in the database.
        """
        asset = row[3]
        account = row[1]
        self.data_cur.execute("INSERT OR IGNORE INTO assets (asset) VALUES (?) ",(asset,))
        asset_id = self.data_cur.execute("SELECT asset_id FROM assets WHERE asset = ?",(asset,)).fetchone()[0]
        asset_amount = -row[4]  # Convert negative to positive
        remaining_amount = asset_amount
        month_asset_amounts = self.available_asset(asset_id, account)
        total_asset_amount = sum(e[1] for e in month_asset_amounts)
        
        if total_asset_amount + 1e-3 >= asset_amount:
            i = 0
            while remaining_amount > 1e-3:
                (oldest_available, amount) = month_asset_amounts[i]
                month_amount = min(remaining_amount, amount)
                # Just remove shares, no capital change
                self.data_cur.execute("UPDATE cohort_assets SET amount = amount - ? WHERE month = ? AND asset_id = ? AND account = ?",
                                     (month_amount, oldest_available, asset_id, account))
                remaining_amount -= month_amount
                i += 1
            # Reset transaction_cur
            self.transaction_cur.execute("UPDATE transactions SET processed = 1 WHERE rowid = ?", (row[-1],))
            self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")
        else:
            # Not enough shares - this shouldn't happen for valid Byte transactions
            logging.warning(f"Not enough shares to remove for {asset}: have {total_asset_amount}, need {asset_amount}")
            raise AssetDeficit(f"Not enough shares to remove for {asset}", self)

    def _on_transaction_processed(self, row: tuple) -> None:
        """
        Hook invoked after each transaction is processed (after dispatch,
        before the next unprocessed row is fetched). Override to track
        per-transaction state. The default implementation is a no-op.
        """
        pass

    def process_transactions(self, raise_on_unprocessed: bool = True) -> None:
        """
        Process transactions all transactions in the database that have not been processed yet.
        After attempting to processing all transactions, the function checks if there are any unprocessed transactions left.
        If there are, an AssetDeficit exception is raised and the database is rolled back. Otherwise, the changes are committed.
        """
        unprocessed_lines = self.transaction_cur.execute("SELECT *,rowid FROM transactions WHERE processed == 0 ORDER BY date ASC, rowid ASC")
        row = unprocessed_lines.fetchone()
        #Consider upgrading to python3.8 to make this more elegant with := statment
        while row is not None:
            # Re-apply special cases if defined
            if self.special_cases is not None:
                row_data = row[:10]
                updated_row_data = self.special_cases.handle_special_cases(row_data)
                
                # Convert string representation of numbers (from special cases json) back to float
                final_row_data = list(updated_row_data)
                for idx in (4, 5, 6, 7):
                    if isinstance(final_row_data[idx], str) and final_row_data[idx] not in ('-', ''):
                        try:
                            final_row_data[idx] = float(final_row_data[idx].replace(',', '.'))
                        except ValueError:
                            pass
                updated_row_data = tuple(final_row_data)
                
                if updated_row_data != row_data:
                    # row layout: (date..isin[0-9], processed[10], origin[11], rowid[12]).
                    # Use row[-1] for rowid and preserve origin so the in-memory row
                    # stays aligned with the actual column order after the origin
                    # column was added (issue #74).
                    rowid = row[-1]
                    origin_val = row[-2]
                    logging.info(f"Re-applying special case change for transaction on {row[0]}: {row_data} -> {updated_row_data}")
                    self.data_cur.execute("""
                        UPDATE transactions
                        SET date = ?, account = ?, transaction_type = ?, asset_name = ?,
                            amount = ?, price = ?, total = ?, courtage = ?, currency = ?, isin = ?
                        WHERE rowid = ?
                    """, updated_row_data + (rowid,))
                    row = updated_row_data + (0, origin_val, rowid)

            month = self.allocate_to_month(row[0])
            if row[2] == "Insättning" or row[2] == "Autogiroinsättning":
                self.handle_deposit(row)
            elif row[2] == "Uttag":
                self.handle_withdrawal(row)
            elif row[2] == "Köp":
                self.handle_purchase(row)
            elif row[2] == "Sälj":
                self.handle_sale(row)
            elif row[2] == "Utdelning":
                self.handle_dividend(row)
            elif row[2] == "Räntor" or row[2] == "Ränta" or row[2] == "Inlåningsränta" or row[2] == "Utlåningsränta" or row[2] == "Uttag av riskkostnad":
                # Interest can either be negative and handled as a fee, or positive and handled like a dividend on capital
                # Uttag av riskkostnad is a risk premium fee (always negative)
                if row[6] > 0:
                    self.handle_interest(row)
                else:
                    self.handle_fees(row)
            elif row[2] == "Utbokning fraktioner":
                # Tiny fraction write-off, ignore (negligible amount)
                self.handle_ignore(row)
            elif "Utländsk källskatt" in row[2] or "Prelskatt" in row[2] or "Preliminärskatt" in row[2] or "Avkastningsskatt" in row[2]:
                self.handle_fees(row)
            elif "Byte" in row[2] or row[2] == "Övrigt":
                self.handle_listing_change(row)
            elif row[2] == "Tillgångsinsättning":
                self.handle_asset_deposit(row)
            elif row[2] == "Intern överföring":
                self.handle_internal_transfer(row)
            elif row[2] == "Värdepappersinsättning":
                # Check if this is part of a "Byte" (change) transaction
                # If amount is positive, it's adding shares (already handled by special cases converting to Tillgångsinsättning)
                # If it wasn't converted, ignore it
                self.handle_ignore(row)
            elif row[2] == "Värdepappersuttag":
                # Removing shares (usually part of "Byte" transaction)
                if row[4] < 0:  # Negative amount means removing shares
                    self.handle_remove_shares(row)
                else:
                    self.handle_ignore(row)
            else:
                raise(ValueError)
            self._on_transaction_processed(row)
            row = unprocessed_lines.fetchone()

        unprocessed_count = self.transaction_cur.execute("SELECT COUNT(*) FROM transactions WHERE processed == 0").fetchone()[0]
        if unprocessed_count > 0:
            if raise_on_unprocessed:
                raise AssetDeficit("There are {} transaction(s) that could not be processed due to a missmatch of assets in the database".format(unprocessed_count),self)
            else:
                logging.warning("There are {} transaction(s) left unprocessed (normal for temporary historical snapshots)".format(unprocessed_count))
        else:
            #Calculate summary data and put it in asset table
            asset_ids = self.data_cur.execute("SELECT asset_id FROM assets").fetchall()
            for (id,) in asset_ids:
                month_asset_data = self.data_cur.execute("SELECT amount, average_price, average_purchase_price, average_sale_price, purchased_amount, sold_amount FROM cohort_assets WHERE asset_id = ?",(id,)).fetchall()
                amount = 0
                average_price = 0
                average_purchase_price = 0
                average_sale_price = 0
                purchased_amount = 0
                sold_amount = 0
                for month_asset in month_asset_data:
                    month_amount, month_average_price, month_average_purchase_price, month_average_sale_price, month_purchased_amount, month_sold_amount = month_asset
                    if month_amount > 1e-3:
                        average_price = month_amount/(month_amount+amount)*month_average_price+amount/(month_amount+amount)*average_price
                        amount += month_amount
                    if month_purchased_amount > 1e-3:
                        average_purchase_price = month_purchased_amount/(month_purchased_amount+purchased_amount)*month_average_purchase_price+purchased_amount/(month_purchased_amount+purchased_amount)*average_purchase_price
                        purchased_amount += month_purchased_amount
                    if month_sold_amount > 1e-3:
                        average_sale_price = month_sold_amount/(month_sold_amount+sold_amount)*month_average_sale_price+sold_amount/(month_sold_amount+sold_amount)*average_sale_price
                        sold_amount += month_sold_amount
                self.data_cur.execute("UPDATE assets SET amount = ?, average_price = ?, average_purchase_price = ?, average_sale_price = ?, purchased_amount = ?, sold_amount = ? WHERE asset_id = ?",(amount,average_price,average_purchase_price,average_sale_price,purchased_amount,sold_amount,id,))
            #Commit changes
            self.db.commit()

if __name__ == "__main__":
    # Create DatabaseHandler object
    db = DatabaseHandler("data/asset_data.db")
    # Create SpecialCases object
    special_cases = SpecialCases("data/special_cases.json")
    # Create DataAdder object
    data_adder = DataParser(db,special_cases)
    # Add data from newdata.csv to the database
    rows_added = data_adder.add_data("data/newdata.csv")

    # Print number of rows added to the database
    print("Added {} rows to the database".format(rows_added))
    
    # Process transactions
    data_adder.process_transactions()