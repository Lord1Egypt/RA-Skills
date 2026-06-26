#!/usr/bin/env python3
"""
Break-Even Analysis Calculator - handler.py
Descriptive skill providing frameworks.
No real code execution or financial transactions.
"""

import json
import sys
import re

def parse_input(user_input: str) -> dict:
    """Parse user input."""
    input_lower = user_input.lower()
    parsed = {
        "input_preview": user_input[:80],
        "word_count": len(user_input.split()),
        "has_amounts": bool(re.search(r'\$?\d+', user_input)),
        "has_dates": bool(re.search(r'\d{1,2}[/-]\d{1,2}', user_input)),
    }
    
    # Check for amounts
    amounts = re.findall(r'\$?(\d+)', user_input)
    if amounts:
        try:
            nums = [int(a) for a in amounts]
            parsed["amounts"] = nums
            parsed["max_amount"] = max(nums)
        except:
            pass
    
    # Check timeframe
    if "month" in input_lower:
        parsed["timeframe"] = "monthly"
    elif "quarter" in input_lower:
        parsed["timeframe"] = "quarterly"
    elif "year" in input_lower:
        parsed["timeframe"] = "annual"
    
    # Check urgency
    if "urgent" in input_lower:
        parsed["priority"] = "high"
    elif "important" in input_lower:
        parsed["priority"] = "medium"
    
    return parsed

def generate_response(parsed: dict, user_input: str) -> dict:
    """Generate response."""
    input_lower = user_input.lower()
    
    response = {
        "skill": "break-even-analysis-calculator",
        "name": "Break-Even Analysis Calculator",
        "input_analysis": parsed,
        "analysis": "Analysis based on your input.",
    }
    
    recs = []
    steps = []
    
    # Differentiate based on amounts
    if parsed.get("has_amounts"):
        max_amt = parsed.get("max_amount", 0)
        if max_amt > 100000:
            recs.append("For large amounts, consider professional advice.")
            steps.append("Consult financial professionals.")
        elif max_amt > 10000:
            recs.append("For significant amounts, implement detailed tracking.")
            steps.append("Set up tracking systems.")
        else:
            recs.append("For smaller amounts, focus on efficiency.")
            steps.append("Use standard templates.")
    
    # Differentiate based on timeframe
    timeframe = parsed.get("timeframe")
    if timeframe == "monthly":
        recs.append("Monthly planning enables regular adjustments.")
        steps.append("Establish monthly reviews.")
    elif timeframe == "quarterly":
        recs.append("Quarterly review supports strategic planning.")
        steps.append("Align with business quarters.")
    elif timeframe == "annual":
        recs.append("Annual planning drives long-term strategy.")
        steps.append("Set annual goals.")
    
    # Differentiate based on priority
    priority = parsed.get("priority")
    if priority == "high":
        recs.append("Urgent matters need immediate attention.")
        steps.append("Address within 48 hours.")
    elif priority == "medium":
        recs.append("Important items require clear planning.")
        steps.append("Create timeline with milestones.")
    
    # Skill-specific logic
    if "break-even-analysis-calculator" == "break-even-analysis-calculator":
        if "fixed" in input_lower:
            recs.append("Identify all fixed costs accurately.")
        if "variable" in input_lower:
            recs.append("Calculate variable costs per unit.")
    elif "break-even-analysis-calculator" == "working-capital-optimizer":
        if "inventory" in input_lower:
            recs.append("Optimize inventory levels.")
        if "receivables" in input_lower:
            recs.append("Improve collections process.")
    elif "break-even-analysis-calculator" == "financial-ratio-benchmarker":
        if "ratio" in input_lower:
            recs.append("Compare ratios to industry benchmarks.")
    # ... 其他skill类似
    
    # Ensure we have recommendations
    if not recs:
        recs = ["Review relevant frameworks.", "Consult professionals."]
    if not steps:
        steps = ["Customize with your data.", "Schedule regular reviews."]
    
    response["recommendations"] = recs
    response["next_steps"] = steps
    response["templates"] = ["Framework template", "Checklist", "Best practices"]
    response["disclaimer"] = "Descriptive analysis only. No code execution. Consult professionals."
    
    return response

def handle(user_input: str) -> str:
    """Main handler - MUST use user_input."""
    parsed = parse_input(user_input)
    response = generate_response(parsed, user_input)
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(input_text))
