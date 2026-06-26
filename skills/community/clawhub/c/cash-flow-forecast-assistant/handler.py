#!/usr/bin/env python3
"""
{skill_name} - handler.py
Descriptive skill providing templates and frameworks.
No real code execution, external APIs, or financial transactions.
"""

import json
import sys
import re

def parse_input(user_input: str) -> dict:
    """Parse user input to extract key information."""
    input_lower = user_input.lower()
    parsed = {
        "original_input_preview": user_input[:100] + ("..." if len(user_input) > 100 else ""),
        "word_count": len(user_input.split()),
        "contains_amounts": bool(re.search(r'\$?\d+[,\.]?\d*', user_input)),
        "contains_dates": bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', user_input)),
    }
    
    # Detect key terms
    key_terms = ["income", "expenses", "savings", "debt", "monthly", "tax", "business", 
                 "personal", "profit", "cash", "customer", "supplier", "growth", "risk"]
    for term in key_terms:
        if term in input_lower:
            parsed[f"contains_{term}"] = True
    
    # Detect amounts
    amounts = re.findall(r'\$?(\d+[,\.]?\d*)', user_input)
    if amounts:
        try:
            nums = [float(a.replace(',', '')) for a in amounts]
            parsed["amounts_found"] = nums
            parsed["max_amount"] = max(nums)
            parsed["min_amount"] = min(nums)
            parsed["amount_count"] = len(nums)
            parsed["total_amount"] = sum(nums)
        except:
            pass
    
    # Detect timeframe
    if "month" in input_lower or "monthly" in input_lower:
        parsed["timeframe"] = "monthly"
    elif "quarter" in input_lower or "quarterly" in input_lower:
        parsed["timeframe"] = "quarterly"
    elif "year" in input_lower or "annual" in input_lower or "yearly" in input_lower:
        parsed["timeframe"] = "annual"
    
    # Detect priority
    if "urgent" in input_lower or "immediate" in input_lower or "asap" in input_lower:
        parsed["priority"] = "high"
    elif "important" in input_lower or "critical" in input_lower:
        parsed["priority"] = "medium"
    else:
        parsed["priority"] = "normal"
    
    return parsed

def generate_response(parsed_input: dict, user_input: str) -> dict:
    """Generate response based on parsed input."""
    input_lower = user_input.lower()
    
    # Base response
    response = {
        "skill": "cash-flow-forecast-assistant",
        "name": "Cash Flow Forecast Assistant",
        "input_analysis": parsed_input,
        "analysis": "Analysis generated based on your specific input characteristics.",
    }
    
    # Generate differentiated recommendations
    recommendations = []
    next_steps = []
    
    # Amount-based differentiation
    if parsed_input.get("contains_amounts"):
        max_amount = parsed_input.get("max_amount", 0)
        if max_amount > 100000:
            recommendations.append("For large amounts (over $100,000), consider professional advice.")
            next_steps.append("Engage financial advisor for amounts of this scale.")
        elif max_amount > 10000:
            recommendations.append("For significant amounts ($10,000-$100,000), implement robust tracking.")
            next_steps.append("Set up dedicated tracking for these transactions.")
        else:
            recommendations.append("For smaller amounts, focus on aggregation and pattern analysis.")
            next_steps.append("Track consistently to identify spending patterns.")
    
    # Timeframe differentiation
    timeframe = parsed_input.get("timeframe")
    if timeframe == "monthly":
        recommendations.append("Monthly analysis enables regular adjustments.")
        next_steps.append("Establish monthly review cadence.")
    elif timeframe == "quarterly":
        recommendations.append("Quarterly review balances responsiveness with strategy.")
        next_steps.append("Align with business quarters.")
    elif timeframe == "annual":
        recommendations.append("Annual planning supports long-term strategy.")
        next_steps.append("Use for strategic planning.")
    
    # Priority differentiation
    priority = parsed_input.get("priority")
    if priority == "high":
        recommendations.append("Urgent matters require immediate attention.")
        next_steps.append("Address within 48 hours.")
    elif priority == "medium":
        recommendations.append("Important items need clear deadlines.")
        next_steps.append("Create timeline with weekly checks.")
    else:
        recommendations.append("Normal priority allows systematic approach.")
        next_steps.append("Develop plan with monthly reviews.")
    
    # Skill-specific logic will be inserted here
    # Cash Flow Forecast Assistant specific logic
    if "seasonal" in input_lower:
        recommendations.append("Account for seasonal variations.")
        next_steps.append("Create separate forecasts for different seasons.")
    
    if "growth" in input_lower:
        recommendations.append("Plan for working capital during growth.")
        next_steps.append("Model growth scenarios.")
    
    if "volatile" in input_lower:
        recommendations.append("Build larger cash reserves.")
        next_steps.append("Create multiple scenarios.")
    
    # Ensure basic recommendations
    if not recommendations:
        recommendations = [
            "Review relevant financial frameworks.",
            "Consult with professionals.",
            "Use insights as starting point."
        ]
    
    if not next_steps:
        next_steps = [
            "Customize with your data.",
            "Establish tracking system.",
            "Schedule regular reviews."
        ]
    
    response["recommendations"] = recommendations
    response["next_steps"] = next_steps
    response["templates_available"] = [
        "Framework template",
        "Implementation checklist",
        "Scenario guidance",
        "Best practices"
    ]
    response["disclaimer"] = "Descriptive analysis only. No code execution or financial transactions. Consult professionals."
    
    return response

def handle(user_input: str) -> str:
    """Main handler function."""
    # Actually parse user input
    parsed = parse_input(user_input)
    
    # Generate response based on parsed input
    response = generate_response(parsed, user_input)
    
    # Return JSON
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(input_text))
