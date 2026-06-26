#!/usr/bin/env python3
"""Test script for Family Finance Manager"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import handle

def test_health_report():
    """Test health report generation"""
    request = {
        "action": "health-report",
        "family": {
            "members": [{"name": "爸爸", "age": 40, "role": "self", "income": 30000}],
            "monthlyIncome": 50000,
            "annualIncome": 600000,
            "incomeStability": "high"
        },
        "assets": {"liquid": 100000, "investments": 200000, "property": 3000000, "other": 100000},
        "liabilities": {"mortgage": 1500000, "loans": 100000, "creditCards": 20000},
        "monthlyExpenses": {"housing": 8000, "transportation": 3000, "food": 6000, "healthcare": 2000, "education": 3000, "entertainment": 2000, "other": 3000},
        "insurance": {"life": 500000, "health": 300000, "property": 1000000},
        "riskProfile": "moderate",
        "goals": [{"name": "子女教育金", "amount": 1000000, "years": 15, "priority": "high"}]
    }
    result = handle(request)
    assert result["success"] == True
    data = result["data"]
    assert "overallScore" in data
    assert "dimensions" in data
    print(f"✓ health-report: score={data['overallScore']}, grade={data['scoreGrade']}")
    return data

def test_analyze():
    """Test financial analysis"""
    request = {
        "action": "analyze",
        "family": {"monthlyIncome": 50000, "annualIncome": 600000, "incomeStability": "high", "members": []},
        "assets": {"liquid": 100000, "investments": 200000, "property": 3000000, "other": 100000},
        "liabilities": {"mortgage": 1500000, "loans": 100000, "creditCards": 20000},
        "monthlyExpenses": {"housing": 8000, "transportation": 3000, "food": 6000, "healthcare": 2000, "education": 3000, "entertainment": 2000, "other": 3000}
    }
    result = handle(request)
    assert result["success"] == True
    data = result["data"]
    assert "incomeExpense" in data
    assert "netWorth" in data
    print(f"✓ analyze: savingsRate={data['incomeExpense']['savingsRate']}%, netWorth={data['netWorth']['netWorth']}")
    return data

def test_goal_plan():
    """Test savings goal planning"""
    request = {
        "action": "goal-plan",
        "family": {"monthlyIncome": 50000, "annualIncome": 600000, "members": []},
        "assets": {"liquid": 100000, "investments": 200000, "property": 0, "other": 0},
        "monthlyExpenses": {"housing": 8000, "transportation": 3000, "food": 6000, "healthcare": 2000, "education": 3000, "entertainment": 2000, "other": 3000},
        "riskProfile": "moderate",
        "goals": [{"name": "购房首付款", "amount": 1000000, "years": 5, "priority": "high"}]
    }
    result = handle(request)
    assert result["success"] == True
    data = result["data"]
    assert "monthlyRequired" in data
    assert "milestones" in data
    print(f"✓ goal-plan: monthlyRequired={data['monthlyRequired']}, milestones={len(data['milestones'])}")
    return data

def test_insurance():
    """Test insurance recommendations"""
    request = {
        "action": "insurance",
        "family": {"monthlyIncome": 50000, "annualIncome": 600000, "members": [{"name": "爸爸", "age": 40, "role": "self"}, {"name": "妈妈", "age": 38, "role": "spouse"}]},
        "insurance": {"life": 0, "health": 0, "property": 0}
    }
    result = handle(request)
    assert result["success"] == True
    data = result["data"]
    assert "coverageGaps" in data
    assert "recommendations" in data
    print(f"✓ insurance: totalGap={data['totalRecommendedCoverage']}, recs={len(data['recommendations'])}")
    return data

def test_risk_warning():
    """Test risk warning"""
    request = {
        "action": "risk-warning",
        "family": {"monthlyIncome": 20000, "incomeStability": "low", "members": []},
        "assets": {"liquid": 10000, "investments": 0, "property": 0, "other": 0},
        "liabilities": {"mortgage": 0, "loans": 50000, "creditCards": 10000},
        "monthlyExpenses": {"housing": 5000, "transportation": 2000, "food": 3000, "healthcare": 1000, "education": 0, "entertainment": 2000, "other": 2000}
    }
    result = handle(request)
    assert result["success"] == True
    data = result["data"]
    assert "overallRiskLevel" in data
    assert "riskFactors" in data
    print(f"✓ risk-warning: level={data['overallRiskLevel']}, factors={len(data['riskFactors'])}")
    return data

if __name__ == "__main__":
    print("Testing Family Finance Manager...\n")
    test_health_report()
    test_analyze()
    test_goal_plan()
    test_insurance()
    test_risk_warning()
    print("\n✅ All tests passed!")
