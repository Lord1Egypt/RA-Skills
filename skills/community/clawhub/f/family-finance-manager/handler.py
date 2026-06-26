"""Family Finance Manager - Main Handler"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from engine.router import run_family_finance_engine
from engine.types import FamilyFinanceRequest

def handle(request_data: dict) -> dict:
    """Main entry point for handling family finance requests"""
    try:
        request = FamilyFinanceRequest(request_data)
        result = run_family_finance_engine(request)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """CLI entry point for testing"""
    import json
    
    # Sample request
    sample_request = {
        "action": "health-report",
        "family": {
            "name": "示例家庭",
            "members": [
                {"name": "爸爸", "age": 40, "role": "self", "income": 30000},
                {"name": "妈妈", "age": 38, "role": "spouse", "income": 20000}
            ],
            "monthlyIncome": 50000,
            "annualIncome": 600000,
            "incomeStability": "high"
        },
        "assets": {
            "liquid": 100000,
            "investments": 200000,
            "property": 3000000,
            "other": 100000
        },
        "liabilities": {
            "mortgage": 1500000,
            "loans": 100000,
            "creditCards": 20000
        },
        "monthlyExpenses": {
            "housing": 8000,
            "transportation": 3000,
            "food": 6000,
            "healthcare": 2000,
            "education": 3000,
            "entertainment": 2000,
            "other": 3000
        },
        "insurance": {
            "life": 500000,
            "health": 300000,
            "property": 1000000
        },
        "riskProfile": "moderate",
        "goals": [
            {"name": "子女教育金", "amount": 1000000, "years": 15, "priority": "high"},
            {"name": "退休金", "amount": 5000000, "years": 20, "priority": "medium"}
        ]
    }
    
    result = handle(sample_request)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
