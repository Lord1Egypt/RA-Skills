"""
Test suite for Anti-Rug Token Security Checker.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCENARIO_A_SYMBOLS, PROTOCOL_TAGS, FATAL_RULES, RISK_WEIGHTS
from exceptions import AntiRugError, NetworkError, ContractNotFoundError


class TestConfig(unittest.TestCase):
    """Test configuration values."""
    
    def test_scenario_a_symbols(self):
        """Test that scenario A symbols are lowercase."""
        for symbol in SCENARIO_A_SYMBOLS:
            self.assertEqual(symbol, symbol.lower())
    
    def test_protocol_tags(self):
        """Test that protocol tags are lowercase."""
        for tag in PROTOCOL_TAGS:
            self.assertEqual(tag, tag.lower())
    
    def test_fatal_rules_structure(self):
        """Test fatal rules have required keys."""
        required_keys = {"check", "code", "description", "implication"}
        for rule in FATAL_RULES:
            self.assertTrue(required_keys.issubset(rule.keys()))
    
    def test_risk_weights_sum(self):
        """Test risk weights sum to 1.0."""
        total = sum(RISK_WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0, places=2)


class TestValidators(unittest.TestCase):
    """Test cross-validation validators."""
    
    def setUp(self):
        """Set up test fixtures."""
        from validators import get_all_validators
        self.validators = get_all_validators()
    
    def test_validators_registered(self):
        """Test that validators are properly registered."""
        self.assertGreater(len(self.validators), 0)
    
    def test_mint_ownership_neutralized(self):
        """Test CV-01: Mintable with dead owner is neutralized."""
        from validators.cv_mint_ownership import validate
        
        ind = {"is_mintable": True, "owner_is_dead": True, "holder_count": 1000}
        scenario = {"scenario": "C"}
        
        result = validate(ind, scenario)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "neutralized")
        self.assertLess(result["score_delta"], 0)
    
    def test_mint_ownership_amplified(self):
        """Test CV-01: Mintable with active owner in scenario C is amplified."""
        from validators.cv_mint_ownership import validate
        
        ind = {"is_mintable": True, "owner_is_dead": False, "holder_count": 100}
        scenario = {"scenario": "C"}
        
        result = validate(ind, scenario)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "amplified")
        self.assertGreater(result["score_delta"], 0)
    
    def test_concentration_contextual(self):
        """Test CV-02: High concentration with protocol addresses is contextual."""
        from validators.cv_concentration import validate
        
        ind = {"top10_pct": 60, "protocol_held_pct": 30}
        scenario = {"scenario": "B"}
        
        result = validate(ind, scenario)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "contextual")
    
    def test_concentration_amplified(self):
        """Test CV-02: High concentration without protocol addresses is amplified."""
        from validators.cv_concentration import validate
        
        ind = {"top10_pct": 60, "protocol_held_pct": 5}
        scenario = {"scenario": "C"}
        
        result = validate(ind, scenario)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "amplified")


class TestExceptions(unittest.TestCase):
    """Test custom exceptions."""
    
    def test_network_error(self):
        """Test NetworkError can be raised and caught."""
        with self.assertRaises(NetworkError):
            raise NetworkError("Connection failed")
    
    def test_contract_not_found_error(self):
        """Test ContractNotFoundError."""
        with self.assertRaises(ContractNotFoundError):
            raise ContractNotFoundError("Contract not found")


class TestFatalRules(unittest.TestCase):
    """Test fatal rules engine."""
    
    def test_honeypot_rule(self):
        """Test honeypot detection rule."""
        rule = next(r for r in FATAL_RULES if r["code"] == "HONEYPOT")
        
        # Should trigger
        ind_trigger = {"is_honeypot": True}
        self.assertTrue(rule["check"](ind_trigger))
        
        # Should not trigger
        ind_safe = {"is_honeypot": False}
        self.assertFalse(rule["check"](ind_safe))
    
    def test_extreme_tax_rule(self):
        """Test extreme tax detection rule."""
        rule = next(r for r in FATAL_RULES if r["code"] == "EXTREME_TAX")
        
        # Should trigger
        ind_trigger = {"sell_tax": 60}
        self.assertTrue(rule["check"](ind_trigger))
        
        # Should not trigger
        ind_safe = {"sell_tax": 10}
        self.assertFalse(rule["check"](ind_safe))


if __name__ == "__main__":
    unittest.main()
