"""
Tests for Expense Approval Workflow Designer
"""

import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from handler import handle

def test_returns_json():
    result = handle("test")
    parsed = json.loads(result)
    assert isinstance(parsed, dict)
    assert parsed["skill"] == "expense-approval-workflow-designer"
    print("✓ JSON test passed for expense-approval-workflow-designer")

def test_has_disclaimer():
    result = handle("test")
    assert "disclaimer" in result.lower()
    print("✓ Disclaimer test passed for expense-approval-workflow-designer")

def test_input_differentiation():
    # Test different inputs produce different outputs
    input1 = "simple request"
    input2 = "urgent request with $50000 amount"
    
    result1 = handle(input1)
    result2 = handle(input2)
    
    parsed1 = json.loads(result1)
    parsed2 = json.loads(result2)
    
    # Check input analysis differs
    assert parsed1["input_analysis"] != parsed2["input_analysis"]
    
    # Check at least one difference
    diff_found = False
    if parsed1.get("recommendations") != parsed2.get("recommendations"):
        diff_found = True
    if parsed1.get("next_steps") != parsed2.get("next_steps"):
        diff_found = True
    
    assert diff_found, "Different inputs should produce different outputs"
    print("✓ Differentiation test passed for expense-approval-workflow-designer")

if __name__ == "__main__":
    test_returns_json()
    test_has_disclaimer()
    test_input_differentiation()
    print("All tests passed for expense-approval-workflow-designer")
