#!/usr/bin/env python3
"""
Enhanced Hallucination Detector – Fixed implementation
"""

import re
import json
import sys
from datetime import datetime

class HallucinationDetector:
    def __init__(self):
        # ---- Truth database -------------------------------------------------
        self.facts_db = {
            "2+2": {"type": "numeric", "value": "4", "tolerance": 0.0},
            "capital of france": {"type": "string", "value": "paris"},
            "speed of light": {"type": "numeric", "value": "299792458", "unit": "m/s"},
            "water freezes at": {"type": "numeric", "value": "0", "unit": "°c"},
            "pi": {"type": "numeric", "value": "3.1415926535"}
        }
        
        # Uncertainty patterns (case-insensitive)
        self.uncertainty_patterns = [
            r"\b(i'm not sure|i think|maybe|perhaps|could|possibly|likely)\b",
            r"\b(unsure|doubt|question)\b",
            r"\b(could be|might be|sometimes|often)\b",
            r"\b(perhaps|probably)\b",
            r"\b(not sure\s+maybe|not sure\s+or\s+maybe)\b"
        ]
        
        self.speculative_patterns = [
            r"\b(likely|probably|probably not)\b"
        ]

    def _extract_numeric_values(self, text: str) -> list:
        return re.findall(r"\b\d+(?:\.\d+)?\b", text.replace(',', ''))

    def _match_numeric_value(self, expected_val: str, extracted_vals: list) -> bool:
        if not extracted_vals:
            return False
        try:
            exp_val = float(expected_val.replace(',', ''))
            for num_str in extracted_vals:
                try:
                    resp_num = float(num_str)
                    denom = abs(exp_val) if exp_val != 0 else 1e-6
                    if abs(resp_num - exp_val) / denom < 0.01:
                        return True
                except (ValueError, ZeroDivisionError):
                    pass
            return False
        except:
            return False

    def is_factual_consistent(self, query: str, response: str) -> tuple:
        query_lower = query.lower().strip()
        response_lower = response.lower().strip()
        
        # Find matching fact key
        matched_key = None
        for key in self.facts_db.keys():
            if key.lower() in query_lower:
                matched_key = key
                break
        
        if not matched_key:
            return True, "No matching fact"
        
        fact = self.facts_db[matched_key]
        expected_val = fact["value"].lower().replace(',', '')
        fact_type = fact["type"]
        response_lower = response.lower()
        
        if fact_type == "numeric":
            numbers = self._extract_numeric_values(response_lower)
            if not numbers:
                return False, "No numeric value found in response"
            for num_str in numbers:
                try:
                    resp_num = float(num_str)
                    exp_num = float(expected_val)
                    if abs(resp_num - exp_num) / max(abs(exp_num), 1e-6) < 0.01:
                        return True, "Numeric match within tolerance"
                except ValueError:
                    continue
            return False, f"Numeric mismatch: expected ~{expected_val}"
            
            # For non-numeric facts, exact substring check
        elif fact_type == "string":
            if expected_val in response_lower:
                return True, "Exact substring match"
            else:
                return False, f"String mismatch: expected '{expected_val}' not found"
        
        return True, "No fact to evaluate"

    def contains_uncertainty_pattern(self, text: str) -> bool:
        return any(re.search(p, text.lower(), re.IGNORECASE) for p in self.uncertainty_patterns)

    def contains_speculative_language(self, text: str) -> list:
        matches = []
        for pattern in self.speculative_patterns:
            matches.extend(re.findall(pattern, text.lower(), re.IGNORECASE))
        return matches

    def is_uncertain(self, text: str) -> bool:
        """Check if text contains uncertainty or speculative language.
        Returns True if flagged (should not cache), False if clean."""
        return self.contains_uncertainty_pattern(text) or bool(self.contains_speculative_language(text))

    def validate(self, query: str, response: str) -> dict:
        results = {
            "query": query[:100],
            "response_length": len(response),
            "valid": True,
            "checks": {}
        }

        # 1) Factual consistency
        fact_ok, fact_msg = self.is_factual_consistent(query, response)
        results["checks"]["factual_consistency"] = {
            "passed": fact_ok,
            "message": fact_msg
        }
        if not fact_ok:
            results["valid"] = False

        # 2) Uncertainty detection
        uncertainty_found = self.contains_uncertainty_pattern(response.lower())
        results["checks"]["uncertainty"] = {
            "passed": not uncertainty_found,
            "issues": self.contains_speculative_language(response.lower())
        }
        if uncertainty_found:
            results["valid"] = False

        # 3) Speculative language
        speculation_issues = self.contains_speculative_language(response.lower())
        results["checks"]["speculation"] = {
            "issues": speculation_issues,
            "passed": len(speculation_issues) == 0
        }
        if speculation_issues:
            results["valid"] = False

        return results

if __name__ == "__main__":
    if len(sys.argv) == 3:
        query, response = sys.argv[1], sys.argv[2]
        result = HallucinationDetector().validate(query, response)
        out = {
            "query": query,
            "response": response,
            "is_valid": result["valid"],
            "checks": result["checks"]
        }
        print(json.dumps(out, indent=2))
        with open("hallucination_validation_detailed.json", "w") as f:
            json.dump({"run": result, "timestamp": datetime.now().isoformat()+"Z"}, f, indent=2)