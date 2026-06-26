"""
Reconciliation Matcher
Implements exact, fuzzy, and semantic matching
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Set
from difflib import SequenceMatcher
import unicodedata


class ReconciliationMatcher:
    """Match bank transactions with orders/invoices."""
    
    def __init__(
        self,
        match_mode: str = "smart",
        amount_tolerance: float = 0.01,
        date_range_days: int = 3,
        tier=None,
    ):
        """
        Initialize matcher.
        
        Args:
            match_mode: "exact", "fuzzy", or "smart"
            amount_tolerance: Amount tolerance for fuzzy matching (CNY)
            date_range_days: Date range for fuzzy matching
            tier: TierConfig instance
        """
        self.match_mode = match_mode
        self.amount_tolerance = amount_tolerance
        self.date_range_days = date_range_days
        self.tier = tier
    
    def match(
        self,
        transactions: List[Dict],
        orders: List[Dict],
    ) -> Dict:
        """
        Match transactions with orders.
        
        Returns:
            dict with keys: matched, differences, unclaimed, unmatched_orders, summary
        """
        # Track matched items
        matched_trans = []
        matched_orders = []
        differences = []
        unclaimed = []  # Transactions without matching orders
        unmatched_orders = []  # Orders without matching transactions
        
        # Build lookup structures
        trans_by_amount = self._index_by_amount(transactions)
        order_by_amount = self._index_by_amount(orders)
        
        # Track which items have been matched
        trans_matched = [False] * len(transactions)
        order_matched = [False] * len(orders)
        
        # Phase 1: Exact matching (date + exact amount)
        exact_matches = self._find_exact_matches(transactions, orders)
        for trans_idx, order_idx, diff in exact_matches:
            trans_matched[trans_idx] = True
            order_matched[order_idx] = True
            
            if diff == 0:
                matched_trans.append({
                    **transactions[trans_idx],
                    "matched_order": orders[order_idx],
                    "match_type": "exact",
                    "difference": 0,
                })
                matched_orders.append(order_idx)
            else:
                differences.append({
                    **transactions[trans_idx],
                    "matched_order": orders[order_idx],
                    "match_type": "exact",
                    "difference": diff,
                    "trans_amount": transactions[trans_idx]["amount"],
                    "order_amount": orders[order_idx]["amount"],
                })
        
        # Phase 2: Fuzzy matching (date range + amount tolerance)
        if self.match_mode in ("fuzzy", "smart"):
            fuzzy_matches = self._find_fuzzy_matches(
                transactions, orders, trans_matched, order_matched
            )
            for trans_idx, order_idx, diff in fuzzy_matches:
                trans_matched[trans_idx] = True
                order_matched[order_idx] = True
                
                if abs(diff) <= self.amount_tolerance:
                    matched_trans.append({
                        **transactions[trans_idx],
                        "matched_order": orders[order_idx],
                        "match_type": "fuzzy",
                        "difference": diff,
                    })
                    matched_orders.append(order_idx)
                else:
                    differences.append({
                        **transactions[trans_idx],
                        "matched_order": orders[order_idx],
                        "match_type": "fuzzy",
                        "difference": diff,
                        "trans_amount": transactions[trans_idx]["amount"],
                        "order_amount": orders[order_idx]["amount"],
                    })
        
        # Phase 3: Semantic matching (counterparty name) - Professional tier
        if self.match_mode == "smart" and self.tier and self.tier.is_pro:
            semantic_matches = self._find_semantic_matches(
                transactions, orders, trans_matched, order_matched
            )
            for trans_idx, order_idx, diff in semantic_matches:
                trans_matched[trans_idx] = True
                order_matched[order_idx] = True
                
                if abs(diff) <= self.amount_tolerance:
                    matched_trans.append({
                        **transactions[trans_idx],
                        "matched_order": orders[order_idx],
                        "match_type": "semantic",
                        "difference": diff,
                    })
                    matched_orders.append(order_idx)
                else:
                    differences.append({
                        **transactions[trans_idx],
                        "matched_order": orders[order_idx],
                        "match_type": "semantic",
                        "difference": diff,
                        "trans_amount": transactions[trans_idx]["amount"],
                        "order_amount": orders[order_idx]["amount"],
                    })
        
        # Collect unmatched items
        for i, trans in enumerate(transactions):
            if not trans_matched[i]:
                unclaimed.append({
                    **trans,
                    "status": "待处理",
                })
        
        for j, order in enumerate(orders):
            if not order_matched[j]:
                unmatched_orders.append({
                    **order,
                    "status": "待处理",
                })
        
        # Build summary
        summary = self._build_summary(
            matched_trans, differences, unclaimed, unmatched_orders
        )
        
        return {
            "matched": matched_trans,
            "differences": differences,
            "unclaimed": unclaimed,
            "unmatched_orders": unmatched_orders,
            "summary": summary,
        }
    
    def _index_by_amount(self, items: List[Dict]) -> Dict[float, List[int]]:
        """Index items by rounded amount for quick lookup."""
        index = {}
        for i, item in enumerate(items):
            if item.get("amount") is not None:
                # Round to 2 decimal places
                key = round(item["amount"], 2)
                if key not in index:
                    index[key] = []
                index[key].append(i)
        return index
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None
        
        if isinstance(date_str, datetime):
            return date_str
        
        date_str = str(date_str).strip()
        
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y%m%d",
            "%Y年%m月%d日",
            "%m/%d/%Y",
            "%d/%m/%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _date_distance(self, date1: str, date2: str) -> int:
        """Calculate days between two dates."""
        d1 = self._parse_date(date1)
        d2 = self._parse_date(date2)
        
        if d1 is None or d2 is None:
            return 999  # Unknown distance
        
        delta = abs((d1 - d2).days)
        return delta
    
    def _find_exact_matches(
        self,
        transactions: List[Dict],
        orders: List[Dict],
    ) -> List[Tuple[int, int, float]]:
        """Find exact matches (same date, same amount)."""
        matches = []
        
        for i, trans in enumerate(transactions):
            if trans.get("amount") is None or trans.get("date") is None:
                continue
            
            trans_amount = round(trans["amount"], 2)
            trans_date = trans["date"]
            
            for j, order in enumerate(orders):
                if order.get("amount") is None or order.get("date") is None:
                    continue
                
                order_amount = round(order["amount"], 2)
                order_date = order["date"]
                
                # Exact amount match
                if trans_amount != order_amount:
                    continue
                
                # Date match (same day)
                if self._date_distance(trans_date, order_date) == 0:
                    diff = trans_amount - order_amount
                    matches.append((i, j, diff))
        
        return matches
    
    def _find_fuzzy_matches(
        self,
        transactions: List[Dict],
        orders: List[Dict],
        trans_matched: List[bool],
        order_matched: List[bool],
    ) -> List[Tuple[int, int, float]]:
        """Find fuzzy matches (date range + amount tolerance)."""
        matches = []
        
        for i, trans in enumerate(transactions):
            if trans_matched[i]:
                continue
            if trans.get("amount") is None or trans.get("date") is None:
                continue
            
            trans_amount = round(trans["amount"], 2)
            trans_date = trans["date"]
            
            # Search for orders with similar amount
            for tolerance in [0, 0.01, 0.1, 1, 10]:
                for j, order in enumerate(orders):
                    if order_matched[j]:
                        continue
                    if order.get("amount") is None or order.get("date") is None:
                        continue
                    
                    order_amount = round(order["amount"], 2)
                    order_date = order["date"]
                    
                    # Amount within tolerance
                    if abs(trans_amount - order_amount) > tolerance + self.amount_tolerance:
                        continue
                    
                    # Date within range
                    if self._date_distance(trans_date, order_date) > self.date_range_days:
                        continue
                    
                    diff = trans_amount - order_amount
                    if abs(diff) <= self.amount_tolerance + tolerance:
                        matches.append((i, j, diff))
                        break
                else:
                    continue
                break
        
        return matches
    
    def _find_semantic_matches(
        self,
        transactions: List[Dict],
        orders: List[Dict],
        trans_matched: List[bool],
        order_matched: List[bool],
    ) -> List[Tuple[int, int, float]]:
        """Find semantic matches (counterparty name similarity)."""
        matches = []
        
        for i, trans in enumerate(transactions):
            if trans_matched[i]:
                continue
            if trans.get("amount") is None or trans.get("counterparty") is None:
                continue
            
            trans_counterparty = self._normalize_text(trans.get("counterparty", ""))
            if not trans_counterparty:
                continue
            
            trans_amount = round(trans["amount"], 2)
            trans_date = trans["date"]
            
            best_match = None
            best_score = 0
            
            for j, order in enumerate(orders):
                if order_matched[j]:
                    continue
                if order.get("amount") is None:
                    continue
                
                order_counterparty = self._normalize_text(order.get("counterparty", ""))
                if not order_counterparty:
                    continue
                
                # Calculate similarity
                score = self._similarity(trans_counterparty, order_counterparty)
                
                if score > 0.7 and score > best_score:
                    # Check amount
                    order_amount = round(order["amount"], 2)
                    if abs(trans_amount - order_amount) <= self.amount_tolerance:
                        # Check date
                        if trans_date and order.get("date"):
                            if self._date_distance(trans_date, order["date"]) <= self.date_range_days:
                                best_score = score
                                best_match = (i, j, trans_amount - order_amount)
                        else:
                            # No date constraint for semantic
                            best_score = score
                            best_match = (i, j, trans_amount - order_amount)
            
            if best_match:
                matches.append(best_match)
        
        return matches
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove common business suffixes
        suffixes = [
            "有限公司", "co.,ltd", "co., ltd", "company", "ltd", "llc",
            "inc.", "inc", "corporation", "corp",
        ]
        for suffix in suffixes:
            text = text.replace(suffix, "")
        
        # Remove special characters
        text = re.sub(r"[^\w\s]", "", text)
        
        # Normalize unicode
        text = unicodedata.normalize("NFKC", text)
        
        return text.strip()
    
    def _similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        if not text1 or not text2:
            return 0.0
        
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _build_summary(
        self,
        matched: List[Dict],
        differences: List[Dict],
        unclaimed: List[Dict],
        unmatched_orders: List[Dict],
    ) -> Dict:
        """Build reconciliation summary."""
        matched_amount = sum(
            m.get("matched_order", {}).get("amount", 0) or 0
            for m in matched
        )
        
        diff_amount = sum(d.get("difference", 0) or 0 for d in differences)
        
        unclaimed_amount = sum(t.get("amount", 0) or 0 for t in unclaimed)
        unmatched_amount = sum(o.get("amount", 0) or 0 for o in unmatched_orders)
        
        total_transactions = len(matched) + len(differences) + len(unclaimed)
        total_orders = len(matched) + len(differences) + len(unmatched_orders)
        
        match_rate = 0.0
        if total_transactions > 0:
            match_rate = len(matched) / total_transactions * 100
        
        recognition_rate = 0.0
        if total_orders > 0:
            recognition_rate = (len(matched) + len(differences)) / total_orders * 100
        
        return {
            "total_transactions": total_transactions,
            "total_orders": total_orders,
            "matched_count": len(matched),
            "difference_count": len(differences),
            "unclaimed_count": len(unclaimed),
            "unmatched_count": len(unmatched_orders),
            "match_rate": round(match_rate, 2),
            "recognition_rate": round(recognition_rate, 2),
            "matched_amount": round(matched_amount, 2),
            "difference_amount": round(abs(diff_amount), 2),
            "unclaimed_amount": round(unclaimed_amount, 2),
            "unmatched_amount": round(unmatched_amount, 2),
        }
