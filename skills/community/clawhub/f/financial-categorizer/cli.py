#!/usr/bin/env python3
"""
CLI interface for financial-categorizer.

Provides command-line access to import, categorization, and category management.
"""

import argparse
import logging
import sys
from pathlib import Path

from financial_categorizer.db_handler import DatabaseHandler, TransferManager
from financial_categorizer.categorizer import Categorizer
from financial_categorizer.importer import CSVImporter
from financial_categorizer.stats import Stats


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_db(db_path: str) -> DatabaseHandler:
    handler = DatabaseHandler(db_path)
    handler.connect()
    return handler


def confirm_action(prompt_message: str, yes_flag: bool = False) -> bool:
    """Prompt the user for confirmation on destructive actions.

    If yes_flag is True, bypasses confirmation and returns True.
    If stdin is not a TTY and yes_flag is False, exits with error.
    Otherwise, prompts interactively.
    """
    if yes_flag:
        return True
    if not sys.stdin.isatty():
        print("Error: Interactive confirmation is not available. Use --yes or -y to bypass confirmation.", file=sys.stderr)
        sys.exit(1)
    try:
        response = input(f"{prompt_message} [y/N]: ").strip().lower()
        if response in ('y', 'yes'):
            return True
        print("Aborted.")
        sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(1)


def _refresh_projection(db):
    """Refresh period_projection + v_burn_down after data mutations.

    Best-effort: projection staleness must never fail the mutation command.
    """
    try:
        Stats(db).refresh_period_projection()
    except Exception as exc:
        logging.getLogger(__name__).warning("period projection refresh failed: %s", exc)


def cmd_import(args):
    old_level = logging.getLogger().getEffectiveLevel()
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)

    db = get_db(args.db)
    try:
        importer = CSVImporter(db)
        cat = Categorizer(db)

        total = {"imported": 0, "skipped": 0, "errors": 0, "settled_pending": 0}
        all_file_results = []

        for path in args.files:
            result = importer.import_file(
                path, account_name=args.account,
                auto_create_account=not args.no_auto_account,
            )
            all_file_results.append((Path(path).name, result))
            for k in total:
                total[k] += result.get(k, 0)
            logger.info(
                f"{Path(path).name}: {result['imported']} imported, "
                f"{result['skipped']} skipped, {result['errors']} errors"
            )

        cat_result = None
        if total["imported"] > 0:
            cat_result = cat.categorize_new(auto_close=getattr(args, "close", False))
            logger.info(f"Categorized {cat_result['matched']} new transactions "
                        f"({cat_result['unmatched']} uncategorized)")
            
            # Print recurring payment matching results
            rr = cat_result.get("recurring_results", {})
            for l in rr.get("linked", []):
                logger.info(f"Linked transaction '{l['tx_desc']}' on {l['tx_date']} to recurring '{l['recurring_name']}'")
            for r in rr.get("resumed", []):
                print(f"[INFO] Transaction matching cancelled subscription '{r['name']}' detected. Automatically resumed subscription (new series ID: {r['new_id']}).")
            for w in rr.get("warnings", []):
                if w.get("type") == "amount_bounds":
                    print(f"[WARNING] Transaction '{w['tx_desc']}' on {w['tx_date']} ({w['tx_amount']:.2f} SEK) "
                          f"matched recurring '{w['name']}' (ID: {w['id']}) but was skipped because it fell outside "
                          f"configured amount bounds [{w['amount_min']}, {w['amount_max']}].")
                else:
                    print(f"[WARNING] Active recurring payment '{w['name']}' (expected around {w['expected']}) was not found in transaction history.")
            for c in rr.get("closed", []):
                print(f"[INFO] Automatically closed missing/dead recurring payment '{c['name']}' (end date set to {c['end_date']}).")

        if total["settled_pending"] > 0:

            logger.info(f"Settled {total['settled_pending']} pending transactions")

        # Print parsing failures to stderr (always, regardless of quiet/compact/verbose)
        for name, result in all_file_results:
            for f in result["details"]["failures"]:
                print(f"[ERROR] Row in {name}: {f['row']} (Reason: {f['reason']})", file=sys.stderr)

        # Print pending lifecycle warnings (reservations that disappeared
        # from the export without a settled counterpart)
        for name, result in all_file_results:
            for w in result.get("warnings", []):
                print(
                    f"[WARNING] {name}: pending [{w['id']}] {w['date']} "
                    f"{w['amount']:.2f} {w['description']}: {w['reason']}"
                )

        if not args.quiet:
            if not args.compact:
                # 1. Print skips (only in verbose mode)
                if args.verbose:
                    for name, result in all_file_results:
                        for s in result["details"]["skipped"]:
                            print(f"[SKIP] {s['date']} | {s['description']} | {s['amount']:.2f} SEK ({s['reason']})")

                # 2. Print settled pending transactions (for default and verbose modes)
                for name, result in all_file_results:
                    for s in result["details"]["settled"]:
                        print(f"[SETTLED] {s['date']} | {s['description']} | {s['amount']:.2f} SEK (Matched pending transaction)")

                # 3. Print newly imported transactions (for default and verbose modes)
                new_txn_ids = {n["id"] for name, result in all_file_results for n in result["details"]["new"]}
                if cat_result and "categorized_details" in cat_result:
                    for c in cat_result["categorized_details"]:
                        if c["id"] not in new_txn_ids:
                            continue
                        date_str = c["date"]
                        desc = c["description"]
                        amt = c["amount"]
                        cat_name = c["category_name"]
                        if cat_name:
                            if args.verbose:
                                if c["is_manual"]:
                                    print(f"[NEW] {date_str} | {desc} | {amt:.2f} SEK -> {cat_name} (Manual Override)")
                                else:
                                    rule_info = f"Rule: {c['rule_type']} '{c['rule_pattern']}', priority {c['rule_priority']}"
                                    print(f"[NEW] {date_str} | {desc} | {amt:.2f} SEK -> {cat_name} ({rule_info})")
                            else:
                                print(f"[NEW] {date_str} | {desc} | {amt:.2f} SEK -> {cat_name}")
                        else:
                            if args.verbose:
                                print(f"[NEW] {date_str} | {desc} | {amt:.2f} SEK -> [Uncategorized] (No matching rule)")
                            else:
                                print(f"[NEW] {date_str} | {desc} | {amt:.2f} SEK -> [Uncategorized]")

            # 4. Print total summary counts (compact, default, and verbose modes)
            print(f"Total: {total['imported']} imported, {total['skipped']} skipped, "
                  f"{total['errors']} errors")
        _refresh_projection(db)
    finally:
        db.disconnect()
        logging.getLogger().setLevel(old_level)


def cmd_categories(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        categories = cat.list_categories()

        if not categories:
            print("No categories defined.")
            return

        # Build tree display
        children_map = {}
        roots = []
        for c in categories:
            pid = c["parent_id"]
            if pid is None:
                roots.append(c)
            else:
                children_map.setdefault(pid, []).append(c)

        def print_tree(node, indent=0):
            prefix = "  " * indent
            type_str = f" [{node.get('category_type', 'expense')}]" if indent == 0 else ""
            print(f"{prefix}- {node['name']} (id={node['id']}){type_str}")
            for child in sorted(children_map.get(node["id"], []), key=lambda x: x["name"]):
                print_tree(child, indent + 1)

        for root in sorted(roots, key=lambda x: x["name"]):
            print_tree(root)
    finally:
        db.disconnect()


def cmd_add_category(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        assoc_id = None
        if args.associated_account:
            if args.associated_account.lower() not in ("none", "null"):
                assoc_id = resolve_account_id(db, args.associated_account)
        cid = cat.add_category(
            args.name, parent_id=args.parent, category_type=args.category_type,
            description=args.description, associated_account_id=assoc_id
        )
        print(f"Created category '{args.name}' (id={cid})")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.disconnect()


def cmd_update_category(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        kwargs = {}
        if args.name is not None:
            kwargs["name"] = args.name
        if args.parent is not None:
            kwargs["parent_id"] = args.parent
        if args.category_type is not None:
            kwargs["category_type"] = args.category_type
        if args.description is not None:
            kwargs["description"] = args.description
        if args.associated_account is not None:
            if args.associated_account.lower() in ("", "none", "null"):
                kwargs["associated_account_id"] = None
            else:
                kwargs["associated_account_id"] = resolve_account_id(db, args.associated_account)

        if not kwargs:
            print("Nothing to update. Specify --name, --parent, --associated-account, or --description.")
            return

        updated = cat.update_category(args.id, **kwargs)
        if updated:
            print(f"Updated category {args.id}")
        else:
            print(f"No changes made (category {args.id} not found or values unchanged)")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.disconnect()


def cmd_delete_category(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        category = cat.get_category(args.id)
        if not category:
            print(f"Category {args.id} not found")
            return

        cur = db.get_cursor()
        cur.execute("SELECT COUNT(*) FROM categories WHERE parent_id = ?", (args.id,))
        child_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM match_rules WHERE category_id = ?", (args.id,))
        rule_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM id_matches WHERE category_id = ?", (args.id,))
        match_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM transactions WHERE category_id = ?", (args.id,))
        txn_count = cur.fetchone()[0]

        print("Category Details:")
        print(f"  ID: {category['id']}")
        print(f"  Name: {category['name']}")
        print(f"  Type: {category['category_type']}")
        if category['description']:
            print(f"  Description: {category['description']}")
        print("Downstream Effects:")
        print(f"  Child categories: {child_count}")
        print(f"  Associated match rules: {rule_count}")
        print(f"  Manual transaction overrides: {match_count}")
        print(f"  Transactions currently assigned to this category: {txn_count}")

        if child_count > 0 and args.reassign is None:
            print("  ERROR: Cannot delete category with children unless --reassign is specified.", file=sys.stderr)
            sys.exit(1)

        if (rule_count > 0 or match_count > 0) and args.reassign is None and not args.force:
            print("  ERROR: Category has rules/matches. Use --reassign or --force to delete.", file=sys.stderr)
            sys.exit(1)

        if args.reassign:
            reassign_cat = cat.get_category(args.reassign)
            if not reassign_cat:
                print(f"  ERROR: Reassignment target category {args.reassign} not found.", file=sys.stderr)
                sys.exit(1)
            print(f"  Children, rules, and manual matches will be reassigned to: '{reassign_cat['name']}' (ID: {args.reassign})")
        else:
            if rule_count > 0 or match_count > 0:
                print("  WARNING: All associated match rules and manual matches will be permanently deleted.")
            if txn_count > 0:
                print("  WARNING: Transactions assigned to this category will be reset to uncategorized (NULL).")

        confirm_action(f"Are you sure you want to delete category '{category['name']}'?", getattr(args, 'yes', False))

        deleted = cat.delete_category(args.id, reassign=args.reassign, force=args.force)
        if deleted:
            msg = f"Deleted category {args.id}"
            if args.reassign:
                msg += f" (reassigned to {args.reassign})"
            print(msg)
        else:
            print(f"Category {args.id} not found")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.disconnect()


def cmd_rules(args):
    db = get_db(args.db)
    try:
        if args.transaction_id is not None:
            match = db.get_transaction_rule_match(args.transaction_id)
            if not match:
                print(f"Error: Transaction {args.transaction_id} not found.", file=sys.stderr)
                sys.exit(1)

            print(f"Transaction [{match['id']}] {match['date']}  {match['amount']:.2f} SEK  {match['description']}")
            if match["source"] == "uncategorized":
                print("Status: Uncategorized")
            elif match["source"] == "manual":
                print(f"Status: Manually categorized (Override) -> Category: [{match['category_id']}] {match['category_name']}")
            elif match["source"] == "rule":
                print(f"Status: Categorized by Rule #{match['rule_id']} -> Category: [{match['category_id']}] {match['category_name']}")
                print("Rule Details:")
                print(f"  Pattern:    /{match['rule_pattern']}/")
                print(f"  Match Type: {match['rule_match_type']}")
            return

        cat = Categorizer(db)
        rules = cat.list_rules()

        if not rules:
            print("No rules defined.")
            return

        for r in rules:
            status = "enabled" if r["enabled"] else "disabled"
            amt = ""
            if r.get("amount_min") is not None or r.get("amount_max") is not None:
                lo = f">={r['amount_min']}" if r['amount_min'] is not None else ""
                hi = f"<={r['amount_max']}" if r['amount_max'] is not None else ""
                amt = f"  amount:{lo}{hi}"
            print(f"  [{r['id']}] {r['category_name']:<20} "
                  f"{r['match_type']:<8} /{r['pattern']}/  "
                  f"priority={r['priority']} ({status}){amt}")
    finally:
        db.disconnect()


def cmd_add_rule(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        rule_id = cat.add_rule(
            args.category, args.pattern,
            match_type=args.type, priority=args.priority,
            amount_min=args.amount_min, amount_max=args.amount_max
        )
        print(f"Added rule {rule_id} and re-categorized all transactions")
    finally:
        db.disconnect()


def cmd_remove_rule(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        cur = db.get_cursor()
        cur.execute(
            "SELECT r.id, r.category_id, c.name, r.pattern, r.match_type, r.priority, r.enabled, r.amount_min, r.amount_max "
            "FROM match_rules r JOIN categories c ON r.category_id = c.id "
            "WHERE r.id = ?",
            (args.id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"Rule {args.id} not found")
            return

        rule = {
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

        print("Rule Details:")
        print(f"  ID: {rule['id']}")
        print(f"  Category: {rule['category_name']} (ID: {rule['category_id']})")
        print(f"  Pattern: /{rule['pattern']}/ (Type: {rule['match_type']})")
        print(f"  Priority: {rule['priority']}")
        print(f"  Status: {'enabled' if rule['enabled'] else 'disabled'}")
        if rule['amount_min'] is not None or rule['amount_max'] is not None:
            lo = f">={rule['amount_min']}" if rule['amount_min'] is not None else ""
            hi = f"<={rule['amount_max']}" if rule['amount_max'] is not None else ""
            print(f"  Amount range: {lo} {hi}")

        print("Downstream Effects:")
        print("  Removing this rule will cause all transactions to be re-categorized.")
        print("  Transactions previously categorized by this rule may revert to other rules or uncategorized.")

        confirm_action(f"Are you sure you want to remove rule {rule['id']}?", getattr(args, 'yes', False))

        removed = cat.remove_rule(args.id)
        if removed:
            print(f"Removed rule {args.id} and re-categorized all transactions")
        else:
            print(f"Rule {args.id} not found")
    finally:
        db.disconnect()


def cmd_preview(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        matches = cat.preview_rule(args.pattern, match_type=args.type, limit=args.limit)

        if not matches:
            print("No matches found.")
            return

        print(f"Matches ({len(matches)}):")
        for m in matches:
            print(f"  [{m['id']}] {m['date']}  {m['amount']:>10.2f}  {m['description']}")
    finally:
        db.disconnect()


def cmd_categorize(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)
        if args.all:
            result = cat.categorize_all()
            print(f"Re-categorized all: {result['matched']} matched, "
                  f"{result['unmatched']} unmatched")
            
            # Also run recurring linking when re-categorizing all
            from financial_categorizer.recurring import RecurringManager
            rm = RecurringManager(db)
            rr = rm.link_transactions(dry_run=False, auto_close=getattr(args, "close", False))
            for l in rr.get("linked", []):
                logger.info(f"Linked transaction '{l['tx_desc']}' on {l['tx_date']} to recurring '{l['recurring_name']}'")
        else:
            result = cat.categorize_new(auto_close=getattr(args, "close", False))
            print(f"Categorized new: {result['matched']} matched, "
                  f"{result['unmatched']} unmatched")
            
            # Print recurring payment matching results
            rr = result.get("recurring_results", {})
            for l in rr.get("linked", []):
                logger.info(f"Linked transaction '{l['tx_desc']}' on {l['tx_date']} to recurring '{l['recurring_name']}'")
            for r in rr.get("resumed", []):
                print(f"[INFO] Transaction matching cancelled subscription '{r['name']}' detected. Automatically resumed subscription (new series ID: {r['new_id']}).")
            for w in rr.get("warnings", []):
                if w.get("type") == "amount_bounds":
                    print(f"[WARNING] Transaction '{w['tx_desc']}' on {w['tx_date']} ({w['tx_amount']:.2f} SEK) "
                          f"matched recurring '{w['name']}' (ID: {w['id']}) but was skipped because it fell outside "
                          f"configured amount bounds [{w['amount_min']}, {w['amount_max']}].")
                else:
                    print(f"[WARNING] Active recurring payment '{w['name']}' (expected around {w['expected']}) was not found in transaction history.")
            for c in rr.get("closed", []):
                print(f"[INFO] Automatically closed missing/dead recurring payment '{c['name']}' (end date set to {c['end_date']}).")
        _refresh_projection(db)
    finally:
        db.disconnect()



def cmd_transactions(args):
    db = get_db(args.db)
    try:
        category_id = None
        if args.category:
            cat = Categorizer(db)
            lookup = cat.get_category_by_name(args.category)
            if not lookup:
                print(f"Error: Category '{args.category}' not found.", file=sys.stderr)
                sys.exit(1)
            category_id = lookup["id"]

        account_id = None
        if args.account:
            lookup = db.get_account_by_name(args.account)
            if not lookup:
                print(f"Error: Account '{args.account}' not found.", file=sys.stderr)
                sys.exit(1)
            account_id = lookup["id"]

        txns = db.get_transactions(
            category_id=category_id,
            uncategorized_only=args.uncategorized,
            non_zero=not args.include_zero,
            account_id=account_id,
            limit=args.limit,
        )

        if not txns:
            print("No transactions found.")
            return

        print(f"Transactions ({len(txns)}):")
        for t in txns:
            cat_str = f" [{t['category_name']}]" if t['category_name'] else " [Uncategorized]"
            if args.unsplit:
                main_val = t['unsplit_amount']
                diff_val = t['amount']
                helper_label = "raw"
            elif args.net:
                main_val = t['adjusted_amount']
                diff_val = t['amount']
                helper_label = "raw"
            else:
                main_val = t['amount']
                diff_val = t['adjusted_amount']
                helper_label = "adj"

            helper_str = f" ({helper_label}: {diff_val:.2f})" if abs(main_val - diff_val) > 1e-4 else ""
            print(f"  [{t['id']}] {t['date']}  {main_val:>10.2f} SEK{helper_str:<17}  {t['account_name']:<15} {cat_str:<18}  {t['description']}")
    finally:
        db.disconnect()


def cmd_uncategorized(args):
    db = get_db(args.db)
    try:
        cat = Categorizer(db)

        if args.group:
            groups = cat.get_uncategorized_grouped(
                non_zero=not args.include_zero,
                net=args.net,
                unsplit=args.unsplit
            )
            if not groups:
                print("All transactions are categorized.")
                return
            
            mode_label = ""
            if args.unsplit:
                mode_label = " (unsplit)"
            elif args.net:
                mode_label = " (net)"

            print(f"Uncategorized by description ({len(groups)} groups){mode_label}:")
            for g in groups:
                print(f"  {g['count']:>3}x  {g['total']:>10.2f}  avg={g['avg_amount']:>8.2f}  {g['description']}")
        else:
            uncategorized = db.get_transactions(
                uncategorized_only=True,
                non_zero=not args.include_zero,
                limit=999999,
            )
            if not uncategorized:
                print("All transactions are categorized.")
                return
            print(f"Uncategorized transactions ({len(uncategorized)}):")
            for t in uncategorized:
                if args.unsplit:
                    main_val = t['unsplit_amount']
                    diff_val = t['amount']
                    helper_label = "raw"
                elif args.net:
                    main_val = t['adjusted_amount']
                    diff_val = t['amount']
                    helper_label = "raw"
                else:
                    main_val = t['amount']
                    diff_val = t['adjusted_amount']
                    helper_label = "adj"

                helper_str = f" ({helper_label}: {diff_val:.2f})" if abs(main_val - diff_val) > 1e-4 else ""
                print(f"  [{t['id']}] {t['date']}  {main_val:>10.2f} SEK{helper_str:<17}  {t['description']}")
    finally:
        db.disconnect()


def cmd_accounts(args):
    db = get_db(args.db)
    try:
        accounts = db.list_accounts()
        if not accounts:
            print("No accounts defined.")
            return
        for a in accounts:
            print(f"  [{a['id']}] {a['name']:<20} type={a['type']:<10} "
                  f"ownership={a['ownership_ratio']:.2f}  {a['currency']}  "
                  f"cash_neutral={a['cash_neutral']}"
                  f"{('  ' + a['description']) if a['description'] else ''}")
    finally:
        db.disconnect()


def cmd_add_account(args):
    db = get_db(args.db)
    try:
        aid = db.add_account(
            args.name, type=args.type,
            ownership_ratio=args.ownership,
            currency=args.currency,
            description=args.description,
            cash_neutral=args.cash_neutral,
        )
        print(f"Created account '{args.name}' (id={aid})")
    finally:
        db.disconnect()


def cmd_update_account(args):
    db = get_db(args.db)
    try:
        kwargs = {}
        if args.name is not None:
            kwargs["name"] = args.name
        if args.type is not None:
            kwargs["type"] = args.type
        if args.ownership is not None:
            kwargs["ownership_ratio"] = args.ownership
        if args.currency is not None:
            kwargs["currency"] = args.currency
        if args.description is not None:
            kwargs["description"] = args.description
        if args.cash_neutral is not None:
            kwargs["cash_neutral"] = args.cash_neutral
        if not kwargs:
            print("Nothing to update.")
            return
        updated = db.update_account(args.id, **kwargs)
        print(f"Updated account {args.id}" if updated else f"Account {args.id} not found")
    finally:
        db.disconnect()


def cmd_delete_account(args):
    db = get_db(args.db)
    try:
        acct = db.get_account(args.id)
        if not acct:
            print(f"Account {args.id} not found")
            return

        cur = db.get_cursor()
        cur.execute("SELECT COUNT(*) FROM transactions WHERE account_id = ?", (args.id,))
        txn_count = cur.fetchone()[0]

        print("Account Details:")
        print(f"  ID: {acct['id']}")
        print(f"  Name: {acct['name']}")
        print(f"  Type: {acct['type']}")
        print(f"  Ownership Ratio: {acct['ownership_ratio']}")
        print(f"  Currency: {acct['currency']}")
        print(f"  Cash Neutral: {acct['cash_neutral']}")
        if acct['description']:
            print(f"  Description: {acct['description']}")

        print("Downstream Effects:")
        if txn_count > 0:
            print(f"  WARNING: There are {txn_count} transactions associated with this account.")
            print("           Deleting this account will FAIL due to database integrity restrictions (ON DELETE RESTRICT).")
        else:
            print("  No transactions are associated with this account. It can be safely deleted.")

        confirm_action(f"Are you sure you want to delete account '{acct['name']}'?", getattr(args, 'yes', False))

        deleted = db.delete_account(args.id)
        if deleted:
            print(f"Deleted account {args.id}")
        else:
            print(f"Account {args.id} not found")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.disconnect()


def cmd_manual_match(args):
    db = get_db(args.db)
    try:
        try:
            txn_id = resolve_transaction_id(db, args.transaction)
            cat_id = resolve_category_id(db, args.category)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        cat = Categorizer(db)
        cat.add_manual_match(txn_id, cat_id)
        # Fetch details for a friendly/clear confirmation printout
        cur = db.get_cursor()
        cur.execute("SELECT description FROM transactions WHERE id = ?", (txn_id,))
        txn_desc = cur.fetchone()[0]
        cur.execute("SELECT name FROM categories WHERE id = ?", (cat_id,))
        cat_name = cur.fetchone()[0]
        print(f"Manually matched transaction [{txn_id}] '{txn_desc}' -> category [{cat_id}] '{cat_name}'")
        _refresh_projection(db)
    finally:
        db.disconnect()


def cmd_manual_unmatch(args):
    db = get_db(args.db)
    try:
        try:
            txn_id = resolve_transaction_id(db, args.transaction)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        cat = Categorizer(db)
        if cat.remove_manual_match(txn_id):
            print(f"Removed manual categorization override for transaction [{txn_id}].")
        else:
            print(f"Error: Transaction [{txn_id}] does not have a manual categorization override.", file=sys.stderr)
            sys.exit(1)
        _refresh_projection(db)
    finally:
        db.disconnect()


def resolve_account_id(db, name_or_id: str) -> int:
    """Resolve an account name or ID to an account ID."""
    if not name_or_id:
        return None
    try:
        acct_id = int(name_or_id)
        acct = db.get_account(acct_id)
        if acct:
            return acct["id"]
    except ValueError:
        pass

    acct = db.get_account_by_name(name_or_id)
    if acct:
        return acct["id"]

    raise ValueError(f"Account '{name_or_id}' not found.")


def resolve_transaction_id(db, search_term: str) -> int:
    """Resolve a transaction by ID or search term.

    If multiple matches are found, raises ValueError with match details.
    """
    if not search_term:
        raise ValueError("Transaction identifier must not be empty.")

    # 1. Try to parse as transaction ID
    try:
        txn_id = int(search_term)
        cur = db.get_cursor()
        cur.execute("SELECT id FROM transactions WHERE id = ?", (txn_id,))
        if cur.fetchone():
            return txn_id
    except ValueError:
        pass

    # 2. Try to search by description
    cur = db.get_cursor()
    cur.execute(
        "SELECT t.id, t.date, t.amount, t.description, c.name, a.name "
        "FROM transactions t "
        "JOIN accounts a ON a.id = t.account_id "
        "LEFT JOIN categories c ON c.id = t.category_id "
        "WHERE t.description LIKE ?",
        (f"%{search_term}%",)
    )
    rows = cur.fetchall()
    if not rows:
        raise ValueError(f"No transaction found matching '{search_term}'.")

    if len(rows) > 1:
        matches = []
        for r in rows:
            cat_str = f" [{r[4]}]" if r[4] else " [Uncategorized]"
            matches.append(f"  [{r[0]}] {r[1]} {r[2]:>10.2f} SEK  {r[5]:<15} {cat_str:<18} {r[3]}")
        match_list = "\n".join(matches)
        raise ValueError(
            f"Multiple transactions found matching '{search_term}':\n{match_list}\n"
            "Please specify the transaction using its ID."
        )

    return rows[0][0]


def resolve_category_id(db, name_or_id: str) -> int:
    """Resolve a category name or ID to a category ID."""
    if not name_or_id:
        raise ValueError("Category identifier must not be empty.")

    # 1. Try to parse as category ID
    try:
        cat_id = int(name_or_id)
        cur = db.get_cursor()
        cur.execute("SELECT id FROM categories WHERE id = ?", (cat_id,))
        if cur.fetchone():
            return cat_id
    except ValueError:
        pass

    # 2. Try exact name match (case-insensitive)
    cur = db.get_cursor()
    cur.execute("SELECT id FROM categories WHERE LOWER(name) = LOWER(?)", (name_or_id,))
    row = cur.fetchone()
    if row:
        return row[0]

    # 3. Try substring match
    cur.execute("SELECT id, name FROM categories WHERE name LIKE ?", (f"%{name_or_id}%",))
    rows = cur.fetchall()
    if not rows:
        raise ValueError(f"Category '{name_or_id}' not found.")
    if len(rows) > 1:
        match_names = ", ".join(f"'{r[1]}' (ID: {r[0]})" for r in rows)
        raise ValueError(f"Multiple categories match '{name_or_id}': {match_names}. Please be more specific.")
    return rows[0][0]


def resolve_period_type(db, arg_value):
    if arg_value == "default":
        mode = db.get_metadata("salary_period_mode", "fixed")
        return "salary" if mode in ("fixed", "salary") else "calendar"
    return arg_value


def cmd_stats_summary(args):
    db = get_db(args.db)
    try:
        pt = resolve_period_type(db, args.period_type)
        stats = Stats(db)
        rows = stats.monthly_summary(month=args.month, period_type=pt,
                                     unsplit=args.unsplit, gross=args.gross,
                                     raw_split=args.raw_split)
        if not rows:
            print("No data found.")
            return

        mode_label = ""
        if args.gross:
            mode_label = " (gross)"
        elif args.unsplit:
            mode_label = " (unsplit)"
        elif args.raw_split:
            mode_label = " (raw-split)"

        for r in rows:
            print(f"{r['month']}{mode_label}  income={r['total_income']:>10.2f}  "
                  f"expenses={r['total_expenses']:>10.2f}  net={r['net']:>10.2f}")
    finally:
        db.disconnect()


def cmd_stats_category(args):
    db = get_db(args.db)
    try:
        pt = resolve_period_type(db, args.period_type)
        cat = Categorizer(db)
        stats = Stats(db)

        lookup = cat.get_category_by_name(args.name)
        if not lookup:
            print(f"Category '{args.name}' not found.")
            sys.exit(1)

        result = stats.category_total(
            lookup["id"], month=args.month,
            date_from=args.from_date, date_to=args.to_date,
            period_type=pt,
            unsplit=args.unsplit, gross=args.gross, raw_split=args.raw_split,
        )
        mode_label = "total"
        if args.gross:
            mode_label = "gross_total"
        elif args.unsplit:
            mode_label = "unsplit_total"
        elif args.raw_split:
            mode_label = "raw_split_total"

        print(f"{args.name}: {mode_label}={result['total']:>10.2f}  count={result['count']}")
    finally:
        db.disconnect()


def cmd_stats_trend(args):
    db = get_db(args.db)
    try:
        pt = resolve_period_type(db, args.period_type)
        cat = Categorizer(db)
        stats = Stats(db)

        lookup = cat.get_category_by_name(args.name)
        if not lookup:
            print(f"Category '{args.name}' not found.")
            sys.exit(1)

        rows = stats.trend(
            lookup["id"],
            date_from=args.from_date, date_to=args.to_date,
            period_type=pt,
            unsplit=args.unsplit, gross=args.gross, raw_split=args.raw_split,
        )
        if not rows:
            print("No data found.")
            return

        mode_label = "total"
        if args.gross:
            mode_label = "gross_total"
        elif args.unsplit:
            mode_label = "unsplit_total"
        elif args.raw_split:
            mode_label = "raw_split_total"

        print(f"Trend for {args.name}:")
        for r in rows:
            print(f"  {r['month']}  {mode_label}={r['total']:>10.2f}  count={r['count']}")
    finally:
        db.disconnect()


def cmd_stats_top(args):
    db = get_db(args.db)
    try:
        pt = resolve_period_type(db, args.period_type)
        stats = Stats(db)
        rows = stats.top_spending(month=args.month, limit=args.limit, period_type=pt,
                                  unsplit=args.unsplit, gross=args.gross, raw_split=args.raw_split)
        if not rows:
            print("No spending data found.")
            return

        mode_label = ""
        if args.gross:
            mode_label = " (gross)"
        elif args.unsplit:
            mode_label = " (unsplit)"
        elif args.raw_split:
            mode_label = " (raw-split)"

        print(f"Top spending{mode_label}{(' for ' + args.month) if args.month else ''}:")
        for r in rows:
            month_str = r['month'] if not args.month else ''
            month_col = f"{month_str}  " if month_str else ""
            print(f"  {month_col}{r['category_name']:<25} {r['total']:>10.2f}  ({r['count']} txns)")
    finally:
        db.disconnect()


def cmd_stats_transfers(args):
    db = get_db(args.db)
    try:
        pt = resolve_period_type(db, args.period_type)
        stats = Stats(db)
        rows = stats.external_transfers_summary(month=args.month, period_type=pt,
                                                unsplit=args.unsplit, gross=args.gross, raw_split=args.raw_split)
        if not rows:
            print("No transfers found.")
            return

        mode_label = ""
        if args.gross:
            mode_label = " (gross)"
        elif args.unsplit:
            mode_label = " (unsplit)"
        elif args.raw_split:
            mode_label = " (raw-split)"

        current_period = None
        for r in rows:
            if r["period"] != current_period:
                current_period = r["period"]
                print(f"\nPeriod: {current_period}{mode_label}")
            sign = "+" if r["net_transferred"] >= 0 else ""
            print(f"  {r['account_name']}: {sign}{r['net_transferred']:.2f}")
    finally:
        db.disconnect()


def cmd_recalculate(args):
    db = get_db(args.db)
    try:
        count = db.recalculate_adjusted_amounts()
        print(f"Recalculated adjusted_amount for {count} transactions")
    finally:
        db.disconnect()


def cmd_cleanup(args):
    db = get_db(args.db)
    try:
        if not args.dry_run:
            # Run dry-run style query to show what is about to be deleted
            report = db.cleanup_orphaned_records(dry_run=True)
            total_orphaned = report['orphaned_id_matches'] + report['orphaned_links']
            if total_orphaned == 0:
                print("No orphaned records found. Database is clean.")
                return

            print("Database Cleanup Preview:")
            print(f"  Orphaned ID matches to be deleted: {report['orphaned_id_matches']}")
            print(f"  Orphaned transaction links to be deleted: {report['orphaned_links']}")
            print("Downstream Effects:")
            print("  This will permanently delete the orphaned records listed above.")
            if report['orphaned_links'] > 0:
                print("  Adjusted amounts for all transactions will be recalculated.")

            confirm_action("Are you sure you want to proceed with database cleanup?", getattr(args, 'yes', False))

        report = db.cleanup_orphaned_records(dry_run=args.dry_run)
        action = "Found" if args.dry_run else "Deleted"
        print(f"{action} {report['orphaned_id_matches']} orphaned id_matches record(s).")
        print(f"{action} {report['orphaned_links']} orphaned transaction_links record(s).")
        if not args.dry_run and report['orphaned_links'] > 0:
            print("Recalculated adjusted_amount for all transactions.")
    finally:
        db.disconnect()


def cmd_cleanup_pending(args):
    db = get_db(args.db)
    try:
        force_ids = getattr(args, "force_id", None)
        try:
            report = db.cleanup_pending(dry_run=True, force_ids=force_ids)
        except ValueError as e:
            print(f"Error: {e}")
            return
        ghosts = report["ghosts"]
        unresolved = report["unresolved"]

        if ghosts:
            label = (
                "Ghost pending transaction(s) that would be deleted"
                if args.dry_run
                else "Ghost pending transaction(s) to delete"
            )
            print(f"{label}: {len(ghosts)}")
            for g in ghosts:
                m = g.get("matched_settled")
                match_type = g.get("match_type", "exact")
                if match_type == "forced":
                    matched = "forced by --force-id (no confident counterpart)"
                elif m:
                    matched = f"settled [{m['id']}] {m['date']} {m['amount']:.2f}"
                    if match_type == "inexact":
                        matched += " (inexact amount match)"
                    elif match_type == "split":
                        matched += " (split-authorization group)"
                else:
                    matched = "split-authorization group"
                print(
                    f"  [{g['id']}] {g['date']}  {g['amount']:>10.2f}  "
                    f"{g['description']}  <- {matched}"
                )
        else:
            print("No ghost pending transactions found.")

        if unresolved:
            print(f"Unresolved pending transaction(s) kept for manual review: {len(unresolved)}")
            for u in unresolved:
                note = (
                    "  [probable cancellation: no counterpart found]"
                    if u.get("probable_cancelled") else ""
                )
                print(f"  [{u['id']}] {u['date']}  {u['amount']:>10.2f}  {u['description']}{note}")
                for c in (u.get("candidates") or [])[:3]:
                    print(f"      candidate: settled [{c['id']}] {c['date']} {c['amount']:.2f}")

        if args.dry_run or not ghosts:
            return

        confirm_action(
            f"Are you sure you want to delete {len(ghosts)} ghost pending transaction(s)?",
            getattr(args, "yes", False),
        )

        report = db.cleanup_pending(dry_run=False, force_ids=force_ids)
        print(f"Deleted {report['deleted']} ghost pending transaction(s).")
    finally:
        db.disconnect()


def cmd_link(args):
    db = get_db(args.db)
    try:
        to_account_id = None
        if args.to_account:
            to_account_id = resolve_account_id(db, args.to_account)

        cur = db.get_cursor()

        # Get from_txn details
        cur.execute(
            "SELECT t.amount, a.ownership_ratio, t.description, t.date, a.name "
            "FROM transactions t JOIN accounts a ON t.account_id = a.id WHERE t.id = ?",
            (args.from_id,)
        )
        from_row = cur.fetchone()
        if not from_row:
            print(f"Error: from_transaction_id {args.from_id} not found", file=sys.stderr)
            sys.exit(1)
        from_amount, from_ownership, from_desc, from_date, from_acct_name = from_row

        # Get to_txn details if to_id is present
        to_amount, to_ownership, to_desc, to_date, to_acct_name = 0.0, 1.0, "", "", ""
        if args.to_id is not None:
            cur.execute(
                "SELECT t.amount, a.ownership_ratio, t.description, t.date, a.name "
                "FROM transactions t JOIN accounts a ON t.account_id = a.id WHERE t.id = ?",
                (args.to_id,)
            )
            to_row = cur.fetchone()
            if not to_row:
                print(f"Error: to_transaction_id {args.to_id} not found", file=sys.stderr)
                sys.exit(1)
            to_amount, to_ownership, to_desc, to_date, to_acct_name = to_row

        # Enforce ratio_to validations
        if args.ratio_to is not None and args.to_id is None:
            print("Error: --ratio-to requires a destination transaction (to_id)", file=sys.stderr)
            sys.exit(1)

        # Resolve which mode was used and compute final ratio
        ratio = 1.0
        if args.ratio is not None:
            ratio = args.ratio
        elif args.ratio_to is not None:
            if from_amount == 0:
                print("Error: from_transaction amount is 0, cannot calculate ratio-to", file=sys.stderr)
                sys.exit(1)
            ratio = (abs(to_amount) * args.ratio_to) / from_amount
        elif args.amount is not None:
            if from_amount == 0:
                print("Error: from_transaction amount is 0, cannot calculate ratio from amount", file=sys.stderr)
                sys.exit(1)
            ratio = args.amount / from_amount

        # Determine labels for output
        dry_run_str = " (DRY RUN - NO CHANGES MADE)" if args.dry_run else ""
        print(f"Link Preview{dry_run_str}:")
        print(f"  Type: {args.type}")
        print(f"  From Transaction: [{args.from_id}] {from_date} | {from_desc} | {from_amount:.2f} SEK (ownership: {from_ownership * 100:.0f}%, account: {from_acct_name})")
        if args.to_id is not None:
            print(f"  To Transaction:   [{args.to_id}] {to_date} | {to_desc} | {to_amount:.2f} SEK (ownership: {to_ownership * 100:.0f}%, account: {to_acct_name})")
        print(f"  Calculated DB Ratio: {ratio:.6f}")

        # Downstream effects calculation
        from_base = from_amount * from_ownership
        to_base = to_amount * to_ownership
        
        if args.type == "reimbursement":
            from_change = -(from_amount * from_ownership * ratio)
            to_change = from_amount * to_ownership * ratio
            from_new = from_base + from_change
            to_new = to_base + to_change
        elif args.type == "internal_transfer":
            from_change = -(from_base * ratio)
            to_change = -(to_base * ratio)
            from_new = from_base + from_change
            to_new = to_base + to_change
        else: # external_transfer
            from_change = -from_base
            from_new = 0.0
            to_change = 0.0
            to_new = 0.0

        print("\nDownstream Effects (adjusted_amount):")
        print(f"  From [{args.from_id}]: {from_base:10.2f} SEK  ==> {from_new:10.2f} SEK  ({from_change:+.2f} SEK)")
        if args.to_id is not None:
            print(f"  To   [{args.to_id}]: {to_base:10.2f} SEK  ==> {to_new:10.2f} SEK  ({to_change:+.2f} SEK)")
        print()

        if not args.dry_run:
            tm = TransferManager(db)
            link_id = tm.link_transactions(
                args.from_id, args.to_id, args.type,
                ratio=ratio, comment=args.comment,
                to_account_id=to_account_id,
            )
            print(f"Created link {link_id} ({args.type})")
            _refresh_projection(db)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.disconnect()


def cmd_unlink(args):
    db = get_db(args.db)
    try:
        cur = db.get_cursor()
        cur.execute(
            "SELECT id, from_transaction_id, to_transaction_id, link_type, ratio, comment "
            "FROM transaction_links WHERE id = ?",
            (args.id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"Link {args.id} not found")
            return

        link_id, from_id, to_id, link_type, ratio, comment = row

        print("Link Details:")
        print(f"  ID: {link_id}")
        print(f"  Type: {link_type}")
        print(f"  Ratio: {ratio}")
        if comment:
            print(f"  Comment: {comment}")

        cur.execute("SELECT id, date, description, amount FROM transactions WHERE id = ?", (from_id,))
        from_txn = cur.fetchone()
        if from_txn:
            print(f"  From Transaction: [{from_txn[0]}] {from_txn[1]} | {from_txn[2]} | {from_txn[3]:.2f}")

        if to_id:
            cur.execute("SELECT id, date, description, amount FROM transactions WHERE id = ?", (to_id,))
            to_txn = cur.fetchone()
            if to_txn:
                print(f"  To Transaction:   [{to_txn[0]}] {to_txn[1]} | {to_txn[2]} | {to_txn[3]:.2f}")

        print("Downstream Effects:")
        print("  Removing this link will revert the adjusted_amount for these transactions to their base values.")

        confirm_action(f"Are you sure you want to remove link {link_id}?", getattr(args, 'yes', False))

        tm = TransferManager(db)
        removed = tm.unlink(args.id)
        if removed:
            print(f"Removed link {args.id}")
        else:
            print(f"Link {args.id} not found")
        _refresh_projection(db)
    finally:
        db.disconnect()


def cmd_links(args):
    db = get_db(args.db)
    try:
        tm = TransferManager(db)
        links = tm.list_links(link_type=args.type)
        if not links:
            print("No links found.")
            return
        for l in links:
            to_str = f" -> {l['to_transaction_id']}" if l['to_transaction_id'] else ""
            print(f"  [{l['id']}] {l['from_transaction_id']}{to_str}  "
                  f"{l['link_type']}  ratio={l['ratio']}  "
                  f"{(l['comment'] or '')}")
    finally:
        db.disconnect()


def cmd_suggest_links(args):
    db = get_db(args.db)
    try:
        tm = TransferManager(db)
        suggestions = tm.suggest_links(days_tolerance=args.days, min_amount=args.min_amount)
        if not suggestions:
            print("No transfer suggestions found.")
            return
        print(f"Found {len(suggestions)} potential transfer(s):\n")
        for i, s in enumerate(suggestions, 1):
            print(f"  {i}. {s['from_account']} -> {s['to_account']}")
            print(f"     From: #{s['from_transaction_id']}  {s['from_date']}  {s['from_amount']:.2f}  {s['from_description']}")
            print(f"     To:   #{s['to_transaction_id']}  {s['to_date']}  {s['to_amount']:.2f}  {s['to_description']}")
            print(f"     Days apart: {s['days_apart']}")
            print(f"     link {s['from_transaction_id']} {s['to_transaction_id']} --type internal_transfer")
            print()
    finally:
        db.disconnect()


def cmd_auto_link(args):
    db = get_db(args.db)
    try:
        tm = TransferManager(db)
        if not args.dry_run:
            result = tm.auto_link_transfers(days_tolerance=args.days, dry_run=True)
            internal = result.get("internal", [])
            if not internal:
                print("No internal transfers found.")
                return

            print("Auto-Link Preview:")
            print(f"  Would link {len(internal)} internal transfer(s):")
            for item in internal:
                print(f"    {item['from_account']} -> {item['to_account']}  {item['amount']:.2f}  "
                      f"({item['from_date']} - {item['to_date']})")
            print("Downstream Effects:")
            print("  This will create transfer links between these transactions and adjust their amounts.")
            print("  Make sure to backup your database before proceeding.")

            confirm_action("Are you sure you want to proceed with auto-linking?", getattr(args, 'yes', False))

        result = tm.auto_link_transfers(days_tolerance=args.days, dry_run=args.dry_run)
        internal = result.get("internal", [])
        if not internal:
            print("No internal transfers found.")
            return
        action = "Would link" if args.dry_run else "Linked"
        print(f"{action} {len(internal)} internal transfer(s):")
        for item in internal:
            print(f"  {item['from_account']} -> {item['to_account']}  {item['amount']:.2f}  "
                  f"({item['from_date']} - {item['to_date']})")
    finally:
        db.disconnect()


def cmd_transfer_rules(args):
    db = get_db(args.db)
    try:
        rules = db.get_transfer_rules()
        if not rules:
            print("No transfer rules defined.")
            return
        for r in rules:
            print(f"  [{r['id']}] {r['match_type']:<8} /{r['pattern']}/")
    finally:
        db.disconnect()


def cmd_add_transfer_rule(args):
    db = get_db(args.db)
    try:
        rule_id = db.add_transfer_rule(args.pattern, match_type=args.type)
        print(f"Added transfer rule {rule_id}")
    finally:
        db.disconnect()


def cmd_remove_transfer_rule(args):
    db = get_db(args.db)
    try:
        cur = db.get_cursor()
        cur.execute("SELECT id, pattern, match_type FROM transfer_rules WHERE id = ?", (args.id,))
        row = cur.fetchone()
        if not row:
            print(f"Transfer rule {args.id} not found")
            return

        rule_id, pattern, match_type = row
        print("Transfer Rule Details:")
        print(f"  ID: {rule_id}")
        print(f"  Pattern: /{pattern}/ (Type: {match_type})")
        print("Downstream Effects:")
        print("  Removing this rule will prevent auto-link from automatically linking new matching transactions.")

        confirm_action(f"Are you sure you want to remove transfer rule {rule_id}?", getattr(args, 'yes', False))

        removed = db.remove_transfer_rule(args.id)
        if removed:
            print(f"Removed transfer rule {args.id}")
        else:
            print(f"Transfer rule {args.id} not found")
    finally:
        db.disconnect()


def cmd_stats_compare(args):
    db = get_db(args.db)
    try:
        resolved_pt = resolve_period_type(db, args.period_type)
        stats = Stats(db)
        result = stats.compare(period=args.month, period_type=resolved_pt,
                               unsplit=args.unsplit, gross=args.gross, raw_split=args.raw_split)
        if not result:
            print("Not enough data for comparison.")
            return

        mode_label = ""
        if args.gross:
            mode_label = " (gross)"
        elif args.unsplit:
            mode_label = " (unsplit)"
        elif args.raw_split:
            mode_label = " (raw-split)"

        if isinstance(result, list):
            # Not enough periods for comparison
            for r in result:
                print(f"{r['period']}{mode_label}  income={r['total_income']:>10.2f}  "
                      f"expenses={r['total_expenses']:>10.2f}  net={r['net']:>10.2f}")
            return

        pt = "salary period" if resolved_pt == "salary" else "month"
        print(f"Period: {result['period']} ({pt}){mode_label}")
        print(f"  Income:   {result['total_income']:>10.2f}")
        print(f"  Expenses: {result['total_expenses']:>10.2f}")
        print(f"  Net:      {result['net']:>10.2f}")

        if "prev_period" in result:
            print(f"\nvs {result['prev_period']}{mode_label}:")
            for field, label in [("income", "Income"), ("expense", "Expenses"), ("net", "Net")]:
                delta = result[f"{field}_delta"]
                pct = result[f"{field}_pct"]
                pct_str = f" ({pct:+.1f}%)" if pct is not None else ""
                print(f"  {label}: {delta:+.2f}{pct_str}")
    finally:
        db.disconnect()


def cmd_salary_config(args):
    db = get_db(args.db)
    try:
        mode = db.get_metadata("salary_period_mode", "fixed")
        day = db.get_metadata("salary_period_fixed_day", "25")
        category = db.get_metadata("salary_period_category_name", "Salary")
        print("Salary Period Configuration:")
        print(f"  Mode:            {mode}")
        print(f"  Fixed Day:       {day}")
        print(f"  Salary Category: {category}")
    finally:
        db.disconnect()


def cmd_set_salary_mode(args):
    db = get_db(args.db)
    try:
        db.set_metadata("salary_period_mode", args.mode)
        from financial_categorizer.stats import Stats
        Stats(db)
        print(f"Salary period mode set to: {args.mode}")
    finally:
        db.disconnect()


def cmd_set_salary_day(args):
    db = get_db(args.db)
    try:
        if args.day < 1 or args.day > 28:
            print("Error: day must be between 1 and 28")
            sys.exit(1)
        db.set_metadata("salary_period_fixed_day", str(args.day))
        from financial_categorizer.stats import Stats
        Stats(db)
        print(f"Salary period fixed day set to: {args.day}")
    finally:
        db.disconnect()


def cmd_set_salary_category(args):
    db = get_db(args.db)
    try:
        db.set_metadata("salary_period_category_name", args.category)
        from financial_categorizer.stats import Stats
        Stats(db)
        print(f"Salary period category set to: {args.category}")
    finally:
        db.disconnect()


def parse_cash_neutral(value):
    if value.lower() in ("true", "1", "yes"):
        return 1
    if value.lower() in ("false", "0", "no"):
        return 0
    raise argparse.ArgumentTypeError("Boolean-like value expected (1/0, true/false, yes/no).")


def cmd_stats_cashflow(args):
    db = get_db(args.db)
    try:
        pt = resolve_period_type(db, args.period_type)
        stats = Stats(db)
        rows = stats.cash_flow_summary(month=args.month, period_type=pt,
                                       unsplit=args.unsplit, gross=args.gross, raw_split=args.raw_split)
        if not rows:
            print("No data found.")
            return
        
        mode_label = ""
        if args.gross:
            mode_label = " (Gross)"
        elif args.unsplit:
            mode_label = " (Unsplit)"
        elif args.raw_split:
            mode_label = " (Raw-Split)"

        header_period = "Period" if pt == "salary" else "Month"
        header_period_label = f"{header_period}{mode_label}"
        print(f"{header_period_label:<20}  {'Operating':>12}  {'Transfers':>12}  {'Net':>12}")
        print("-" * 64)
        for r in rows:
            print(f"{r['period']:<20}  {r['operating']:>12.2f}  {r['transfers']:>12.2f}  {r['net']:>12.2f}")
    finally:
        db.disconnect()


def format_interval(i_type, i_val):
    if i_type == "monthly":
        if i_val == 1: return "monthly"
        if i_val == 3: return "quarterly"
        return f"every {i_val}m"
    elif i_type == "weekly":
        if i_val == 1: return "weekly"
        return f"every {i_val}w"
    elif i_type == "yearly":
        if i_val == 1: return "yearly"
        return f"every {i_val}y"
    elif i_type == "days":
        if i_val == 1: return "daily"
        return f"every {i_val}d"
    return f"{i_type} ({i_val})"


def format_day(dom, dow, wom):
    if dom is not None:
        if dom == -1: return "last day"
        return f"day {dom}"
    if dow is not None:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_name = days[dow] if 0 <= dow < 7 else f"day {dow}"
        if wom is not None:
            if wom == -1: return f"last {day_name}"
            prefix = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}.get(wom, f"{wom}th")
            return f"{prefix} {day_name}"
        return day_name
    return "N/A"


def cmd_recurring(args):
    db = get_db(args.db)
    try:
        cur = db.get_cursor()
        sql = """
            SELECT r.id, r.name, r.pattern, r.interval_type, r.interval_value, r.start_date, r.end_date, c.name
            FROM recurring_payments r
            LEFT JOIN categories c ON r.category_id = c.id
        """
        clauses = []
        if args.status == "active":
            clauses.append("r.end_date IS NULL")
        elif args.status == "cancelled":
            clauses.append("r.end_date IS NOT NULL")
        
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
            
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("No recurring payments found.")
            return
            
        print("Recurring Payments:")
        for r in rows:
            status_str = "Active" if r[6] is None else f"Cancelled ({r[6]})"
            int_str = format_interval(r[3], r[4])
            print(f"  [{r[0]}] {r[1]}  pattern='{r[2]}'  interval={int_str}  "
                  f"start={r[5]}  category={r[7] or 'None'}  status={status_str}")
    finally:
        db.disconnect()


def cmd_add_recurring(args):
    db = get_db(args.db)
    try:
        # Resolve category if passed
        category_id = None
        if args.category:
            cur = db.get_cursor()
            cur.execute("SELECT id FROM categories WHERE name = ?", (args.category,))
            row = cur.fetchone()
            if not row:
                print(f"[ERROR] Category '{args.category}' not found.", file=sys.stderr)
                return
            category_id = row[0]

        # Resolve account if passed
        account_id = None
        if args.account:
            cur = db.get_cursor()
            cur.execute("SELECT id FROM accounts WHERE name = ?", (args.account,))
            row = cur.fetchone()
            if not row:
                print(f"[ERROR] Account '{args.account}' not found.", file=sys.stderr)
                return
            account_id = row[0]

        from financial_categorizer.recurring import RecurringManager
        rm = RecurringManager(db)

        if args.dry_run:
            db.connect()
            db.conn.execute("BEGIN TRANSACTION")
            try:
                new_id = rm.add_recurring(
                    name=args.name, pattern=args.pattern, match_type=args.match_type,
                    amount_min=args.amount_min, amount_max=args.amount_max,
                    interval_type=args.interval, interval_value=args.interval_val,
                    day_of_month=args.day_of_month, day_of_week=args.day_of_week,
                    week_of_month=args.week_of_month, start_date=args.start_date,
                    category_id=category_id, account_id=account_id,
                    tolerance_days=args.tolerance
                )
                result = rm.link_transactions(dry_run=True)
                print(f"[DRY-RUN] Would add recurring payment '{args.name}' (ID: {new_id})")
                print(f"[DRY-RUN] Would link {len(result['linked'])} transactions:")
                for l in result["linked"]:
                    print(f"  - {l['tx_date']}  {l['tx_desc']:<40}  amount={l['tx_amount']:>10.2f}")
            finally:
                db.conn.rollback()
        else:
            new_id = rm.add_recurring(
                name=args.name, pattern=args.pattern, match_type=args.match_type,
                amount_min=args.amount_min, amount_max=args.amount_max,
                interval_type=args.interval, interval_value=args.interval_val,
                day_of_month=args.day_of_month, day_of_week=args.day_of_week,
                week_of_month=args.week_of_month, start_date=args.start_date,
                category_id=category_id, account_id=account_id,
                tolerance_days=args.tolerance
            )
            print(f"Successfully added recurring payment '{args.name}' (ID: {new_id})")
            result = rm.link_transactions(dry_run=False)
            print(f"Linked {len(result['linked'])} transactions to this configuration.")
            for l in result["linked"]:
                logger.info(f"Linked transaction '{l['tx_desc']}' on {l['tx_date']} to recurring '{args.name}'")
    finally:
        db.disconnect()


def cmd_update_recurring(args):
    db = get_db(args.db)
    try:
        # Resolve category if passed
        category_id = None
        if args.category:
            cur = db.get_cursor()
            cur.execute("SELECT id FROM categories WHERE name = ?", (args.category,))
            row = cur.fetchone()
            if not row:
                print(f"[ERROR] Category '{args.category}' not found.", file=sys.stderr)
                return
            category_id = row[0]

        # Resolve account if passed
        account_id = None
        if args.account:
            cur = db.get_cursor()
            cur.execute("SELECT id FROM accounts WHERE name = ?", (args.account,))
            row = cur.fetchone()
            if not row:
                print(f"[ERROR] Account '{args.account}' not found.", file=sys.stderr)
                return
            account_id = row[0]

        from financial_categorizer.recurring import RecurringManager
        rm = RecurringManager(db)

        # Build update kwargs
        kwargs = {}
        if args.name is not None: kwargs["name"] = args.name
        if args.pattern is not None: kwargs["pattern"] = args.pattern
        if args.match_type is not None: kwargs["match_type"] = args.match_type
        if args.amount_min is not None: kwargs["amount_min"] = args.amount_min
        if args.amount_max is not None: kwargs["amount_max"] = args.amount_max
        if args.interval is not None: kwargs["interval_type"] = args.interval
        if args.interval_val is not None: kwargs["interval_value"] = args.interval_val
        if args.day_of_month is not None: kwargs["day_of_month"] = args.day_of_month
        if args.day_of_week is not None: kwargs["day_of_week"] = args.day_of_week
        if args.week_of_month is not None: kwargs["week_of_month"] = args.week_of_month
        if args.start_date is not None: kwargs["start_date"] = args.start_date
        if args.tolerance is not None: kwargs["tolerance_days"] = args.tolerance
        if args.category is not None: kwargs["category_id"] = category_id
        if args.account is not None: kwargs["account_id"] = account_id

        if args.dry_run:
            db.connect()
            db.conn.execute("BEGIN TRANSACTION")
            try:
                success = rm.update_recurring(args.id, **kwargs)
                if not success:
                    print(f"[ERROR] Recurring payment ID {args.id} not found.", file=sys.stderr)
                    return
                result = rm.link_transactions(dry_run=True)
                print(f"[DRY-RUN] Would update recurring payment ID {args.id}")
                print(f"[DRY-RUN] Would link {len(result['linked'])} transactions:")
                for l in result["linked"]:
                    print(f"  - {l['tx_date']}  {l['tx_desc']:<40}  amount={l['tx_amount']:>10.2f}")
            finally:
                db.conn.rollback()
        else:
            success = rm.update_recurring(args.id, **kwargs)
            if not success:
                print(f"[ERROR] Recurring payment ID {args.id} not found.", file=sys.stderr)
                return
            print(f"Successfully updated recurring payment ID {args.id}")
            result = rm.link_transactions(dry_run=False)
            print(f"Linked {len(result['linked'])} transactions to this configuration.")
    finally:
        db.disconnect()


def cmd_remove_recurring(args):
    db = get_db(args.db)
    try:
        from financial_categorizer.recurring import RecurringManager
        rm = RecurringManager(db)
        if args.hard:
            action = "PERMANENTLY DELETE"
        else:
            action = "cancel (soft-close)"
        if not confirm_action(f"This will {action} recurring payment ID {args.id}. Proceed?", yes_flag=args.yes):
            return
        success = rm.remove_recurring(args.id, hard=args.hard, cancel_date=args.date)
        if not success:
            print(f"[ERROR] Recurring payment ID {args.id} not found.", file=sys.stderr)
            return
        if args.hard:
            print(f"Successfully deleted recurring payment ID {args.id} completely.")
        else:
            print(f"Successfully cancelled recurring payment ID {args.id}.")
    finally:
        db.disconnect()


def cmd_discover_recurring(args):
    db = get_db(args.db)
    try:
        from financial_categorizer.recurring import RecurringManager
        rm = RecurringManager(db)
        if not args.dry_run and not confirm_action(
            "Auto-discovery will save the discovered configurations, re-run transaction "
            "linking, and auto-close dead recurring configurations. Proceed? (Use --dry-run to preview first)",
            yes_flag=args.yes,
        ):
            return
        candidates = rm.discover_recurring_candidates(dry_run=args.dry_run)
        if not candidates:
            print("No recurring payment candidates found.")
            return

        if args.dry_run:
            print("Discovered Recurring Candidates (Preview - not saved):")
            for c in candidates:
                int_str = format_interval(c['interval_type'], c['interval_value'])
                day_str = format_day(c['day_of_month'], c['day_of_week'], c.get('week_of_month'))
                print(f"  Name: {c['name']:<30} | Interval: {int_str:<12} | Day: {day_str:<15} | Count: {c['tx_count']:>2} | Range: {c['amount_min']:.2f} to {c['amount_max']:.2f}")
        else:
            print(f"Auto-discovery completed. Saved {len(candidates)} new recurring payment configurations to database:")
            for c in candidates:
                int_str = format_interval(c['interval_type'], c['interval_value'])
                day_str = format_day(c['day_of_month'], c['day_of_week'], c.get('week_of_month'))
                print(f"  [{c.get('id', 'NEW')}] {c['name']:<30} | {int_str:<12} | Day: {day_str:<15} | Count: {c['tx_count']}")
    finally:
        db.disconnect()



def cmd_stats_recurring(args):
    db = get_db(args.db)
    try:
        from financial_categorizer.recurring import RecurringManager
        rm = RecurringManager(db)
        pt = resolve_period_type(db, args.period_type) if hasattr(args, "period_type") else "salary"
        stats = rm.get_recurring_stats(query=args.query, period_type=pt, period=args.month)

        if args.query:
            if not stats["details"]:
                print(f"No subscription matching '{args.query}' found.")
                return

            print(f"Subscription Report: {args.query}")
            print("=" * 64)
            for item in stats["details"]:
                c = item["config"]
                status_str = "Active" if c["end_date"] is None else f"Cancelled/Completed ({c['end_date']})"
                int_str = format_interval(c['interval_type'], c['interval_value'])
                print(f"Series ID: {c['id']}")
                print(f"  Name:          {c['name']}")
                print(f"  Pattern:       '{c['pattern']}' ({c['match_type']})")
                print(f"  Account:       {c['account_name'] or 'All'}")
                print(f"  Category:      {c['category_name'] or 'None'}")
                print(f"  Interval:      {int_str}")
                print(f"  Start Date:    {c['start_date']}")
                print(f"  End Date:      {c['end_date'] or 'Ongoing'}")
                print(f"  Status:        {status_str}")
                print(f"  Lifetime Paid: {item['lifetime_total']:>10.2f} SEK")
                print(f"  YTD Paid:      {item['ytd_total']:>10.2f} SEK")
                if item["next_expected"]:
                    print(f"  Next Expected: {item['next_expected']} (±{c['tolerance_days']} days)")
                
                print("\n  Matched Transactions:")
                if not item["transactions"]:
                    print("    No transactions matched.")
                else:
                    for tx in item["transactions"]:
                        print(f"    - {tx['date']} | {tx['description']:<40} | amount={tx['amount']:>10.2f} | period={tx['salary_period']}")
                print("-" * 64)
        else:
            if not stats["details"]:
                print("No recurring payment templates defined. Run 'discover-recurring' to create one.")
                return
                
            active_list = [item for item in stats["details"] if item["active"]]
            cancelled_list = [item for item in stats["details"] if not item["active"]]

            print("=== Active Subscriptions & Bills ===")
            print(f"{'ID':<4} {'Name':<25} {'Interval':<15} {'Next Expected':<13} {'Monthly Cost':>13}")
            print("-" * 75)
            for item in active_list:
                c = item["config"]
                next_str = str(item["next_expected"]) if item["next_expected"] else "N/A"
                
                outflow_amt = 0.0
                if item["last_payment"]:
                    outflow_amt = item["last_payment"]["amount"]
                elif c["amount_min"] is not None and c["amount_max"] is not None:
                    outflow_amt = (c["amount_min"] + c["amount_max"]) / 2
                elif c["amount_min"] is not None:
                    outflow_amt = c["amount_min"]
                
                monthly_equiv = 0.0
                if outflow_amt < 0:
                    if c["interval_type"] == "monthly":
                        monthly_equiv = outflow_amt / c["interval_value"]
                    elif c["interval_type"] == "weekly":
                        monthly_equiv = outflow_amt * 4.33 / c["interval_value"]
                    elif c["interval_type"] == "yearly":
                        monthly_equiv = outflow_amt / 12.0 / c["interval_value"]
                    elif c["interval_type"] == "days":
                        monthly_equiv = outflow_amt * 30.4 / c["interval_value"]

                int_str = format_interval(c['interval_type'], c['interval_value'])
                print(f"[{c['id']:>2}] {c['name']:<25} {int_str:<15} {next_str:<13} {monthly_equiv:>10.2f} SEK")
            
            print("-" * 75)
            print(f"Active Subscriptions Outflow: {stats['total_monthly_outflow']:>10.2f} SEK / month")
            print(f"Total Active Series Count:     {stats['active_count']}")

            if cancelled_list:
                from datetime import date
                from financial_categorizer.recurring import _to_date
                recent_cancelled = []
                for item in cancelled_list:
                    c = item["config"]
                    end_dt = _to_date(c["end_date"])
                    if end_dt and (date.today() - end_dt).days <= 365:
                        recent_cancelled.append(item)

                if recent_cancelled:
                    print("\n=== Recently Cancelled / Inactive Series (Last 12 Months) ===")
                    for item in recent_cancelled:
                        c = item["config"]
                        print(f"  [{c['id']}] {c['name']} (Ended: {c['end_date']}) - Total historical spend: {item['lifetime_total']:.2f} SEK")
    finally:
        db.disconnect()


def cmd_estimate_period(args):
    db = get_db(args.db)
    try:
        from financial_categorizer.stats import Stats
        cur = db.get_cursor()
        cur.execute("SELECT MAX(date) FROM transactions")
        row = cur.fetchone()
        if not row or not row[0]:
            print("No transactions found in database to estimate projection.")
            return
        
        from datetime import date
        as_of_date = date.today()
        last_tx_date = row[0]
        
        # Load estimation level preference
        level = args.level
        if level is None:
            level = int(db.get_metadata("estimate_level", "0"))
            
        stats_mgr = Stats(db)
        proj = stats_mgr.get_projected_spend(as_of_date, window_days=args.days, level=level)
        
        # Split recurring expectations
        upcoming_rec_expenses = sum(item['amount'] for item in proj['upcoming_recurring'] if item['amount'] < 0)
        upcoming_rec_income = sum(item['amount'] for item in proj['upcoming_recurring'] if item['amount'] >= 0)
        
        var_expenses = sum(val for val in proj['projected_variable_categories'].values() if val < 0)
        var_incomes = sum(val for val in proj['projected_variable_categories'].values() if val >= 0)
        
        projected_expenses = var_expenses + upcoming_rec_expenses
        projected_income = var_incomes + upcoming_rec_income
        
        print(f"Period:                    {proj['period_name']} ({proj['period_start']} to {proj['period_end']})")
        print(f"Last Imported Transaction: {last_tx_date}")
        print(f"Days Remaining:            {proj['remaining_days']} days", end="")
        if proj['remaining_days'] > 0:
            print(f" ({proj['projection_start']} to {proj['projection_end']})")
        else:
            print()
            
        print("\n=== Current Period-to-Date Actuals ===")
        print(f"  Total Actual Expenses: {proj['actual_total_expense']:>14.2f} SEK")
        print(f"  Total Actual Income:   {proj['actual_total_income']:>14.2f} SEK")
        print(f"  Net Period Flow So Far:{proj['actual_net_flow']:>14.2f} SEK")
        
        print(f"\n=== Projected for Remaining {proj['remaining_days']} Days ===")
        print(f"  Average Expenses       {proj['projected_variable_total']:>14.2f} SEK ({proj['historical_daily_total']:>7.2f} SEK/day)")
        if level > 0:
            for name, val in sorted(proj['projected_variable_categories'].items()):
                print(f"    {name:<20} {val:>14.2f} SEK")
        print(f"  Recurring Expenses     {upcoming_rec_expenses:>14.2f} SEK")
        print(f"  Projected Expenses     {projected_expenses:>14.2f} SEK")
        print(f"  Projected Income       {projected_income:>14.2f} SEK")

        
        print("\n" + "=" * 50)
        print(f"ESTIMATED NET FULL PERIOD:{proj['total_estimated']:>14.2f} SEK")

        print("=" * 50)

        
    finally:
        db.disconnect()



def cmd_set_estimate_level(args):
    db = get_db(args.db)
    try:
        db.set_metadata("estimate_level", str(args.level))
        level_label = {0: "0 (No Categories)", 1: "1 (Top Categories)", 2: "2 (Subcategories)"}.get(args.level, str(args.level))
        print(f"Successfully set default estimation rollup level to: {level_label}")
    finally:
        db.disconnect()



def main():
    parser = argparse.ArgumentParser(
        prog="financial-categorizer",
        description="Transaction categorization tool backed by SQLite.",
    )
    parser.add_argument("--db", default="data/finance.db", help="Path to SQLite database (default: data/finance.db)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # import
    p_import = subparsers.add_parser("import", help="Import CSV transactions")
    p_import.add_argument("files", nargs="+", help="CSV files to import")
    p_import.add_argument("--account", help="Account name (default: derived from filename)")
    p_import.add_argument("--no-auto-account", action="store_true",
                          help="Don't auto-create account if missing (raises error)")
    p_import.add_argument("--close", action="store_true",
                          help="Auto-close active recurring transactions that are missing expected payments")
    g_verbosity = p_import.add_mutually_exclusive_group()
    g_verbosity.add_argument("--quiet", "-q", action="store_true", help="Quiet mode: suppress all output except warnings/errors")
    g_verbosity.add_argument("--compact", "-c", action="store_true", help="Compact mode: show only summary counts")
    g_verbosity.add_argument("--verbose", "-v", action="store_true", help="Verbose mode: show detailed transaction and rule information")
    p_import.set_defaults(func=cmd_import)


    # accounts
    p_accounts = subparsers.add_parser("accounts", help="List all accounts")
    p_accounts.set_defaults(func=cmd_accounts)

    # add-account
    p_add_acct = subparsers.add_parser("add-account", help="Add a new account")
    p_add_acct.add_argument("name", help="Account name")
    p_add_acct.add_argument("--type", default="tracked",
                            choices=["tracked", "external"],
                            help="Account type: tracked (active bank account), external (savings/investment) (default: tracked)")
    p_add_acct.add_argument("--ownership", type=float, default=1.0,
                            help="Ownership ratio 0.0-1.0 (default: 1.0)")
    p_add_acct.add_argument("--currency", default="SEK", help="Currency (default: SEK)")
    p_add_acct.add_argument("--description", help="Account description")
    p_add_acct.add_argument("--cash-neutral", type=parse_cash_neutral, default=0,
                            help="Set as cash neutral transfer destination (choices: 1/0 or true/false, default: false)")
    p_add_acct.set_defaults(func=cmd_add_account)

    # update-account
    p_upd_acct = subparsers.add_parser("update-account", help="Update an account")
    p_upd_acct.add_argument("id", type=int, help="Account ID")
    p_upd_acct.add_argument("--name", help="New name")
    p_upd_acct.add_argument("--type", choices=["tracked", "external"],
                            help="New type")
    p_upd_acct.add_argument("--ownership", type=float, help="New ownership ratio")
    p_upd_acct.add_argument("--currency", help="New currency")
    p_upd_acct.add_argument("--description", help="New description")
    p_upd_acct.add_argument("--cash-neutral", type=parse_cash_neutral,
                            help="Update cash neutral flag (choices: 1/0 or true/false)")
    p_upd_acct.set_defaults(func=cmd_update_account)

    # delete-account
    p_del_acct = subparsers.add_parser("delete-account", help="Delete an account")
    p_del_acct.add_argument("id", type=int, help="Account ID")
    p_del_acct.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_del_acct.set_defaults(func=cmd_delete_account)

    # categories
    p_cats = subparsers.add_parser("categories", help="List all categories")
    p_cats.set_defaults(func=cmd_categories)

    # add-category
    p_add_cat = subparsers.add_parser("add-category", help="Add a new category")
    p_add_cat.add_argument("name", help="Category name")
    p_add_cat.add_argument("--parent", type=int, help="Parent category ID")
    p_add_cat.add_argument("--type", dest="category_type", default="expense",
                           choices=["income", "expense", "transfer"],
                           help="Category type (default: expense)")
    p_add_cat.add_argument("--description", help="Category description")
    p_add_cat.add_argument("--associated-account", help="Associated account name or ID")
    p_add_cat.set_defaults(func=cmd_add_category)

    # update-category
    p_upd_cat = subparsers.add_parser("update-category", help="Update a category")
    p_upd_cat.add_argument("id", type=int, help="Category ID")
    p_upd_cat.add_argument("--name", help="New name")
    p_upd_cat.add_argument("--parent", type=int, help="New parent category ID")
    p_upd_cat.add_argument("--type", dest="category_type",
                           choices=["income", "expense", "transfer"],
                           help="New category type")
    p_upd_cat.add_argument("--description", help="New description")
    p_upd_cat.add_argument("--associated-account", help="Associated account name or ID (use 'none' to clear)")
    p_upd_cat.set_defaults(func=cmd_update_category)

    # delete-category
    p_del_cat = subparsers.add_parser("delete-category", help="Delete a category")
    p_del_cat.add_argument("id", type=int, help="Category ID")
    p_del_cat.add_argument("--reassign", type=int, help="Reassign children/rules/matches to this category")
    p_del_cat.add_argument("--force", action="store_true", help="Force deletion without reassign (children still require --reassign)")
    p_del_cat.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_del_cat.set_defaults(func=cmd_delete_category)

    # rules
    p_rules = subparsers.add_parser("rules", help="List all match rules")
    p_rules.add_argument("transaction_id", type=int, nargs="?",
                         help="Optional transaction ID to show the matching rule for")
    p_rules.set_defaults(func=cmd_rules)

    # add-rule
    p_add_rule = subparsers.add_parser("add-rule", help="Add a categorization rule")
    p_add_rule.add_argument("category", type=int, help="Category ID to match")
    p_add_rule.add_argument("pattern", help="Pattern to match")
    p_add_rule.add_argument("--type", default="regex", choices=["regex", "exact", "contains"],
                            help="Match type (default: regex)")
    p_add_rule.add_argument("--priority", type=int, default=0, help="Rule priority (default: 0)")
    p_add_rule.add_argument("--amount-min", type=float, help="Minimum amount to match (inclusive)")
    p_add_rule.add_argument("--amount-max", type=float, help="Maximum amount to match (inclusive)")
    p_add_rule.set_defaults(func=cmd_add_rule)

    # remove-rule
    p_rem_rule = subparsers.add_parser("remove-rule", help="Remove a match rule")
    p_rem_rule.add_argument("id", type=int, help="Rule ID")
    p_rem_rule.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_rem_rule.set_defaults(func=cmd_remove_rule)

    # preview
    p_preview = subparsers.add_parser("preview", help="Preview what a rule would match")
    p_preview.add_argument("pattern", help="Pattern to test")
    p_preview.add_argument("--type", default="regex", choices=["regex", "exact", "contains"],
                           help="Match type (default: regex)")
    p_preview.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    p_preview.set_defaults(func=cmd_preview)

    # categorize
    p_cat = subparsers.add_parser("categorize", help="Categorize transactions")
    p_cat.add_argument("--all", action="store_true", help="Re-categorize all transactions")
    p_cat.add_argument("--close", action="store_true",
                        help="Auto-close active recurring transactions that are missing expected payments")
    p_cat.set_defaults(func=cmd_categorize)


    # transactions
    p_txns = subparsers.add_parser("transactions", help="Search and list transactions")
    p_txns.add_argument("--category", help="Filter by category name")
    p_txns.add_argument("--uncategorized", action="store_true", help="Show only uncategorized transactions")
    p_txns.add_argument("--include-zero", action="store_true", help="Include transactions with adjusted_amount = 0 in the output")
    p_txns.add_argument("--account", help="Filter by account name")
    p_txns.add_argument("--limit", type=int, default=50, help="Maximum number of transactions to return (default: 50)")
    g_txns = p_txns.add_mutually_exclusive_group()
    g_txns.add_argument("--net", action="store_true", help="Display personal net (adjusted_amount) as primary value")
    g_txns.add_argument("--unsplit", action="store_true", help="Display household net (unsplit_amount) as primary value")
    p_txns.set_defaults(func=cmd_transactions)

    # uncategorized
    p_uncat = subparsers.add_parser("uncategorized", help="Show uncategorized transactions")
    p_uncat.add_argument("--group", action="store_true", help="Group by description with counts and totals")
    p_uncat.add_argument("--include-zero", action="store_true", help="Include transactions with adjusted_amount = 0")
    g_uncat = p_uncat.add_mutually_exclusive_group()
    g_uncat.add_argument("--net", action="store_true", help="Display personal net (adjusted_amount) as primary value")
    g_uncat.add_argument("--unsplit", action="store_true", help="Display household net (unsplit_amount) as primary value")
    p_uncat.set_defaults(func=cmd_uncategorized)

    # manual-match
    p_manual = subparsers.add_parser("manual-match", help="Manually match a transaction to a category")
    p_manual.add_argument("transaction", type=str, help="Transaction ID or description query")
    p_manual.add_argument("category", type=str, help="Category ID or name query")
    p_manual.set_defaults(func=cmd_manual_match)

    # manual-unmatch
    p_manual_unmatch = subparsers.add_parser("manual-unmatch", help="Remove a manual categorization override")
    p_manual_unmatch.add_argument("transaction", type=str, help="Transaction ID or description query")
    p_manual_unmatch.set_defaults(func=cmd_manual_unmatch)

    # stats summary
    p_stats_summary = subparsers.add_parser("stats-summary", help="Monthly income/expenses/net")
    p_stats_summary.add_argument("--month", help="Filter to YYYY-MM")
    p_stats_summary.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                                 help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    g_stats_summary = p_stats_summary.add_mutually_exclusive_group()
    g_stats_summary.add_argument("--unsplit", action="store_true", help="Undo joint account split (household net)")
    g_stats_summary.add_argument("--gross", action="store_true", help="Undo split and ignore reimbursements (household raw)")
    g_stats_summary.add_argument("--raw-split", action="store_true", help="Ownership split without reimbursement adjustments (bank-view)")
    p_stats_summary.set_defaults(func=cmd_stats_summary)

    # stats category
    p_stats_cat = subparsers.add_parser("stats-category", help="Total for a category (inc. children)")
    p_stats_cat.add_argument("name", help="Category name")
    p_stats_cat.add_argument("--month", help="Filter to YYYY-MM")
    p_stats_cat.add_argument("--from", dest="from_date", type=lambda s: __import__('datetime').date.fromisoformat(s), help="Start date (YYYY-MM-DD)")
    p_stats_cat.add_argument("--to", dest="to_date", type=lambda s: __import__('datetime').date.fromisoformat(s), help="End date (YYYY-MM-DD)")
    p_stats_cat.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                                 help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    g_stats_cat = p_stats_cat.add_mutually_exclusive_group()
    g_stats_cat.add_argument("--unsplit", action="store_true", help="Undo joint account split (household net)")
    g_stats_cat.add_argument("--gross", action="store_true", help="Undo split and ignore reimbursements (household raw)")
    g_stats_cat.add_argument("--raw-split", action="store_true", help="Ownership split without reimbursement adjustments (bank-view)")
    p_stats_cat.set_defaults(func=cmd_stats_category)

    # stats trend
    p_stats_trend = subparsers.add_parser("stats-trend", help="Monthly breakdown for a category")
    p_stats_trend.add_argument("name", help="Category name")
    p_stats_trend.add_argument("--from", dest="from_date", type=lambda s: __import__('datetime').date.fromisoformat(s), help="Start date (YYYY-MM-DD)")
    p_stats_trend.add_argument("--to", dest="to_date", type=lambda s: __import__('datetime').date.fromisoformat(s), help="End date (YYYY-MM-DD)")
    p_stats_trend.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                                 help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    g_stats_trend = p_stats_trend.add_mutually_exclusive_group()
    g_stats_trend.add_argument("--unsplit", action="store_true", help="Undo joint account split (household net)")
    g_stats_trend.add_argument("--gross", action="store_true", help="Undo split and ignore reimbursements (household raw)")
    g_stats_trend.add_argument("--raw-split", action="store_true", help="Ownership split without reimbursement adjustments (bank-view)")
    p_stats_trend.set_defaults(func=cmd_stats_trend)

    # stats top
    p_stats_top = subparsers.add_parser("stats-top", help="Top spending categories")
    p_stats_top.add_argument("--month", help="Filter to YYYY-MM")
    p_stats_top.add_argument("--limit", type=int, default=10, help="Max categories (default: 10)")
    p_stats_top.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                                 help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    g_stats_top = p_stats_top.add_mutually_exclusive_group()
    g_stats_top.add_argument("--unsplit", action="store_true", help="Undo joint account split (household net)")
    g_stats_top.add_argument("--gross", action="store_true", help="Undo split and ignore reimbursements (household raw)")
    g_stats_top.add_argument("--raw-split", action="store_true", help="Ownership split without reimbursement adjustments (bank-view)")
    p_stats_top.set_defaults(func=cmd_stats_top)

    # stats-transfers
    p_stats_transfers = subparsers.add_parser("stats-transfers", help="Net transfers to external/savings accounts")
    p_stats_transfers.add_argument("--month", help="Filter to YYYY-MM")
    p_stats_transfers.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                                   help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    g_stats_transfers = p_stats_transfers.add_mutually_exclusive_group()
    g_stats_transfers.add_argument("--unsplit", action="store_true", help="Undo joint account split (household net)")
    g_stats_transfers.add_argument("--gross", action="store_true", help="Undo split and ignore reimbursements (household raw)")
    g_stats_transfers.add_argument("--raw-split", action="store_true", help="Ownership split without reimbursement adjustments (bank-view)")
    p_stats_transfers.set_defaults(func=cmd_stats_transfers)

    # recalculate
    p_recalc = subparsers.add_parser("recalculate", help="Recalculate adjusted_amount for all transactions")
    p_recalc.set_defaults(func=cmd_recalculate)

    # db-cleanup
    p_cleanup = subparsers.add_parser("db-cleanup", help="Clean up orphaned database records")
    p_cleanup.add_argument("--dry-run", action="store_true", help="Show orphaned records without deleting them")
    p_cleanup.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_cleanup.set_defaults(func=cmd_cleanup)

    # cleanup-pending
    p_cleanup_pending = subparsers.add_parser(
        "cleanup-pending",
        help="Delete ghost pending reservations whose settled counterpart already exists",
    )
    p_cleanup_pending.add_argument("--dry-run", action="store_true", help="Show ghost pending transactions without deleting them")
    p_cleanup_pending.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_cleanup_pending.add_argument(
        "--force-id", action="append", type=int, default=None, metavar="ID",
        help="Delete a specific pending transaction by id (repeatable), overriding match confidence",
    )
    p_cleanup_pending.set_defaults(func=cmd_cleanup_pending)

    # link
    p_link = subparsers.add_parser("link", help="Link two transactions")
    p_link.add_argument("from_id", type=int, help="From transaction ID")
    p_link.add_argument("to_id", type=int, nargs="?", default=None, help="To transaction ID (not needed for external_transfer)")
    p_link.add_argument("--type", required=True, choices=["internal_transfer", "external_transfer", "reimbursement"], help="Link type")
    
    group = p_link.add_mutually_exclusive_group()
    group.add_argument("--ratio", type=float, help="Ratio relative to from_transaction (default: 1.0 if no other mode is specified)")
    group.add_argument("--ratio-to", type=float, help="Ratio relative to to_transaction")
    group.add_argument("--amount", type=float, help="Exact cash/SEK amount to link/reimburse")

    p_link.add_argument("--comment", help="Comment")
    p_link.add_argument("--to-account", help="Target external account name or ID (only for external_transfer)")
    p_link.add_argument("--dry-run", action="store_true", help="Preview downstream changes without modifying the database")
    p_link.set_defaults(func=cmd_link)

    # unlink
    p_unlink = subparsers.add_parser("unlink", help="Remove a transaction link")
    p_unlink.add_argument("id", type=int, help="Link ID")
    p_unlink.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_unlink.set_defaults(func=cmd_unlink)

    # links
    p_links = subparsers.add_parser("links", help="List transaction links")
    p_links.add_argument("--type", choices=["internal_transfer", "external_transfer", "reimbursement"], help="Filter by type")
    p_links.set_defaults(func=cmd_links)

    # suggest-links
    p_suggest = subparsers.add_parser("suggest-links", help="Suggest potential internal transfers")
    p_suggest.add_argument("--days", type=int, default=3, help="Max days apart (default: 3)")
    p_suggest.add_argument("--min-amount", type=float, default=10.0, help="Minimum absolute amount (default: 10)")
    p_suggest.set_defaults(func=cmd_suggest_links)

    # auto-link
    p_auto_link = subparsers.add_parser("auto-link", help="Auto-detect internal transfers using transfer rules")
    p_auto_link.add_argument("--days", type=int, default=3, help="Max days apart (default: 3)")
    p_auto_link.add_argument("--dry-run", action="store_true", help="Show what would be linked without making changes")
    p_auto_link.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_auto_link.set_defaults(func=cmd_auto_link)

    # transfer-rules
    p_tr = subparsers.add_parser("transfer-rules", help="List transfer detection rules")
    p_tr.set_defaults(func=cmd_transfer_rules)

    # add-transfer-rule
    p_atr = subparsers.add_parser("add-transfer-rule", help="Add a transfer detection rule")
    p_atr.add_argument("pattern", help="Pattern to match")
    p_atr.add_argument("--type", default="contains", choices=["regex", "exact", "contains"],
                        help="Match type (default: contains)")
    p_atr.set_defaults(func=cmd_add_transfer_rule)

    # remove-transfer-rule
    p_rtr = subparsers.add_parser("remove-transfer-rule", help="Remove a transfer detection rule")
    p_rtr.add_argument("id", type=int, help="Rule ID")
    p_rtr.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_rtr.set_defaults(func=cmd_remove_transfer_rule)

    # stats-compare
    p_compare = subparsers.add_parser("stats-compare", help="Month-over-month comparison")
    p_compare.add_argument("--month", help="Period to compare (YYYY-MM, default: latest)")
    p_compare.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                           help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    g_compare = p_compare.add_mutually_exclusive_group()
    g_compare.add_argument("--unsplit", action="store_true", help="Undo joint account split (household net)")
    g_compare.add_argument("--gross", action="store_true", help="Undo split and ignore reimbursements (household raw)")
    g_compare.add_argument("--raw-split", action="store_true", help="Ownership split without reimbursement adjustments (bank-view)")
    p_compare.set_defaults(func=cmd_stats_compare)

    # salary-config
    p_sal_cfg = subparsers.add_parser("salary-config", help="Show current salary period configuration")
    p_sal_cfg.set_defaults(func=cmd_salary_config)

    # set-salary-mode
    p_set_mode = subparsers.add_parser("set-salary-mode", help="Set the salary period mode")
    p_set_mode.add_argument("mode", choices=["calendar", "fixed", "salary"],
                            help="Mode: calendar (1st-last), fixed (fixed day boundary), salary (auto payday-based)")
    p_set_mode.set_defaults(func=cmd_set_salary_mode)

    # set-salary-day
    p_set_day = subparsers.add_parser("set-salary-day", help="Set the fixed boundary day of the month")
    p_set_day.add_argument("day", type=int, help="Fixed day of the month (1-28)")
    p_set_day.set_defaults(func=cmd_set_salary_day)

    # set-salary-category
    p_set_cat = subparsers.add_parser("set-salary-category", help="Set the category name used to scan for salary paydays")
    p_set_cat.add_argument("category", help="Salary category name (default: Salary)")
    p_set_cat.set_defaults(func=cmd_set_salary_category)

    # stats-cashflow
    p_cf = subparsers.add_parser("stats-cashflow", help="Show monthly cash flow (Operating, Transfers, Net)")
    p_cf.add_argument("--month", help="Specific month (YYYY-MM)")
    p_cf.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                      help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    g_cf = p_cf.add_mutually_exclusive_group()
    g_cf.add_argument("--unsplit", action="store_true", help="Undo joint account split (household net)")
    g_cf.add_argument("--gross", action="store_true", help="Undo split and ignore reimbursements (household raw)")
    g_cf.add_argument("--raw-split", action="store_true", help="Ownership split without reimbursement adjustments (bank-view)")
    p_cf.set_defaults(func=cmd_stats_cashflow)

    # recurring
    p_rec = subparsers.add_parser("recurring", help="List recurring payments configurations")
    p_rec.add_argument("--status", choices=["active", "cancelled", "all"], default="active",
                       help="Filter by status (default: active)")
    p_rec.set_defaults(func=cmd_recurring)

    # add-recurring
    p_add_rec = subparsers.add_parser("add-recurring", help="Manually create a new recurring config")
    p_add_rec.add_argument("name", help="Name of subscription / recurring payment")
    p_add_rec.add_argument("pattern", help="Description pattern to match")
    p_add_rec.add_argument("--match-type", choices=["regex", "exact", "contains"], default="contains",
                           help="Match type (default: contains)")
    p_add_rec.add_argument("--amount-min", type=float, help="Minimum transaction amount")
    p_add_rec.add_argument("--amount-max", type=float, help="Maximum transaction amount")
    p_add_rec.add_argument("--interval", choices=["monthly", "weekly", "yearly", "days"], default="monthly",
                           help="Interval type (default: monthly)")
    p_add_rec.add_argument("--interval-val", type=int, default=1, help="Interval multiplier value (default: 1)")
    p_add_rec.add_argument("--day-of-month", type=int, help="Expected day of month (1-31, -1 for last day)")
    p_add_rec.add_argument("--day-of-week", type=int, help="Expected day of week (0=Mon, 6=Sun)")
    p_add_rec.add_argument("--week-of-month", type=int, choices=[1, 2, 3, 4, 5, -1],
                           help="Expected week of month (1-5, -1 for last)")
    p_add_rec.add_argument("--start-date", help="Start date (YYYY-MM-DD, default: today)")
    p_add_rec.add_argument("--tolerance", type=int, default=4, help="Tolerance window in days (default: 4)")
    p_add_rec.add_argument("--category", help="Category name to auto-assign/track")
    p_add_rec.add_argument("--account", help="Limit to specific account name")
    p_add_rec.add_argument("--dry-run", action="store_true", help="Preview matches without writing to DB")
    p_add_rec.set_defaults(func=cmd_add_recurring)

    # update-recurring
    p_upd_rec = subparsers.add_parser("update-recurring", help="Update an existing recurring config")
    p_upd_rec.add_argument("id", type=int, help="Recurring Payment ID")
    p_upd_rec.add_argument("--name", help="Name of subscription / recurring payment")
    p_upd_rec.add_argument("--pattern", help="Description pattern to match")
    p_upd_rec.add_argument("--match-type", choices=["regex", "exact", "contains"], help="Match type")
    p_upd_rec.add_argument("--amount-min", type=float, help="Minimum transaction amount")
    p_upd_rec.add_argument("--amount-max", type=float, help="Maximum transaction amount")
    p_upd_rec.add_argument("--interval", choices=["monthly", "weekly", "yearly", "days"], help="Interval type")
    p_upd_rec.add_argument("--interval-val", type=int, help="Interval multiplier value")
    p_upd_rec.add_argument("--day-of-month", type=int, help="Expected day of month (1-31, -1 for last day)")
    p_upd_rec.add_argument("--day-of-week", type=int, help="Expected day of week (0=Mon, 6=Sun)")
    p_upd_rec.add_argument("--week-of-month", type=int, choices=[1, 2, 3, 4, 5, -1],
                           help="Expected week of month (1-5, -1 for last)")
    p_upd_rec.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    p_upd_rec.add_argument("--tolerance", type=int, help="Tolerance window in days")
    p_upd_rec.add_argument("--category", help="Category name to auto-assign/track")
    p_upd_rec.add_argument("--account", help="Limit to specific account name")
    p_upd_rec.add_argument("--dry-run", action="store_true", help="Preview matches without writing to DB")
    p_upd_rec.set_defaults(func=cmd_update_recurring)

    # remove-recurring
    p_rem_rec = subparsers.add_parser("remove-recurring", help="Cancel or delete a recurring payment")
    p_rem_rec.add_argument("id", type=int, help="Recurring Payment ID")
    p_rem_rec.add_argument("--hard", action="store_true",
                           help="Delete configuration completely from the DB (otherwise soft-closes/cancels)")
    p_rem_rec.add_argument("--date", help="Cancellation date (YYYY-MM-DD, defaults to date of last matched transaction)")
    p_rem_rec.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt")
    p_rem_rec.set_defaults(func=cmd_remove_recurring)

    # discover-recurring
    p_disc_rec = subparsers.add_parser("discover-recurring",
                                       help="Auto-discover candidates and auto-close dead configurations")
    p_disc_rec.add_argument("--dry-run", action="store_true", help="Preview candidates without writing them to DB")
    p_disc_rec.add_argument("--yes", "-y", action="store_true", help="Bypass confirmation prompt (required to save and auto-link in non-interactive mode)")
    p_disc_rec.set_defaults(func=cmd_discover_recurring)

    # stats-recurring
    p_stats_rec = subparsers.add_parser("stats-recurring", help="Display recurring outflow and subscriptions stats")
    p_stats_rec.add_argument("query", nargs="?", help="Optional subscription name or ID to filter details")
    p_stats_rec.add_argument("--period-type", choices=["calendar", "salary", "default"], default="default",
                            help="Period type: calendar, salary, or default (dynamically determined by active salary config)")
    p_stats_rec.add_argument("--month", help="Filter details by month/period (YYYY-MM)")
    p_stats_rec.set_defaults(func=cmd_stats_recurring)

    # estimate-period
    p_est = subparsers.add_parser("estimate-period", help="Estimate/project remaining spending for the current period")
    p_est.add_argument("--days", type=int, default=30, help="Historical window in days to compute daily variable spend average")
    p_est.add_argument("--level", type=int, choices=[0, 1, 2], help="Override default category rollup level (0: none, 1: top, 2: detailed)")
    p_est.set_defaults(func=cmd_estimate_period)

    # set-estimate-level
    p_set_est = subparsers.add_parser("set-estimate-level", help="Set default category rollup level for spending estimation")
    p_set_est.add_argument("level", type=int, choices=[0, 1, 2], help="Rollup level (0: no categories, 1: top categories, 2: detailed subcategories)")
    p_set_est.set_defaults(func=cmd_set_estimate_level)

    args = parser.parse_args()



    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
