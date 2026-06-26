#!/usr/bin/env python3
"""
Survey Generator
Creates contextually relevant customer survey questions.
"""

import argparse
import json
import sys
from datetime import datetime

SURVEY_TEMPLATES = {
    "product_validation": [
        {
            "type": "multiple_choice",
            "question": "How do you currently solve [PROBLEM]?",
            "options": [
                "Manual process",
                "Spreadsheets",
                "Paid software",
                "Free tools",
                "Don't solve it",
                "Other (please specify)"
            ]
        },
        {
            "type": "scale",
            "question": "How satisfied are you with your current solution?",
            "scale": "1-5 (Very Dissatisfied to Very Satisfied)"
        },
        {
            "type": "open_ended",
            "question": "What's the most frustrating part of your current workflow for [PROBLEM]?"
        },
        {
            "type": "multiple_choice",
            "question": "How much time do you spend on [PROBLEM] per [TIME_UNIT]?",
            "options": [
                "Less than 1 hour",
                "1-3 hours",
                "3-5 hours",
                "5-10 hours",
                "More than 10 hours"
            ]
        },
        {
            "type": "open_ended",
            "question": "What features would make [SOLUTION] a must-have for you?"
        },
        {
            "type": "multiple_choice",
            "question": "What would you be willing to pay monthly for a solution that [VALUE_PROP]?",
            "options": [
                "$0 (would only use free version)",
                "$5-10",
                "$10-25",
                "$25-50",
                "$50-100",
                "$100+"
            ]
        },
        {
            "type": "scale",
            "question": "How likely are you to recommend [SOLUTION] to a colleague?",
            "scale": "1-10 (Not at all likely to Extremely likely)"
        },
        {
            "type": "multiple_choice",
            "question": "Which of these features is most important to you?",
            "options": "[FEATURE_LIST]"
        },
        {
            "type": "open_ended",
            "question": "What would prevent you from switching to a new solution?"
        },
        {
            "type": "multiple_choice",
            "question": "How did you hear about this survey?",
            "options": [
                "Social media",
                "Email",
                "Word of mouth",
                "Search engine",
                "Online community",
                "Other (please specify)"
            ]
        }
    ],
    "pricing": [
        {
            "type": "multiple_choice",
            "question": "What's your annual income range?",
            "options": [
                "Under $50k",
                "$50k-$100k",
                "$100k-$150k",
                "$150k-$250k",
                "$250k+"
            ]
        },
        {
            "type": "open_ended",
            "question": "What's your budget for [CATEGORY] tools per month?"
        },
        {
            "type": "multiple_choice",
            "question": "Do you prefer one-time purchase or subscription?",
            "options": [
                "One-time purchase",
                "Monthly subscription",
                "Annual subscription",
                "Freemium (free + paid tiers)",
                "No preference"
            ]
        }
    ]
}

DISTRIBUTION_TEMPLATES = {
    "google_forms": """
# Google Forms Setup

1. Go to https://forms.google.com
2. Create new form
3. Add questions below (copy-paste ready)

{questions}

## Distribution Settings
- Response limit: [SET LIMIT]
- Collect email: Optional
- Allow multiple responses: No
- Shuffle questions: Yes (to reduce bias)
    """,
    "typeform": """
# Typeform Setup

1. Go to https://typeform.com
2. Create new typeform
3. Add questions in conversational flow

{questions}

## Recommended Settings
- Welcome screen: Yes (explain purpose)
- Thank you screen: Yes (include incentive if applicable)
- Logic jumps: Consider adding based on responses
- Notifications: Enable for new responses
    """,
    "surveymonkey": """
# SurveyMonkey Setup

1. Go to https://surveymonkey.com
2. Create new survey
3. Add questions below

{questions}

## Distribution Options
- Email collector
- Web link (shareable)
- Social media
- Embed on website
    """
}

def generate_survey(hypothesis, template_type="product_validation"):
    """
    Generate survey questions based on product hypothesis.
    
    Args:
        hypothesis: Product hypothesis string
        template_type: Type of survey template
    
    Returns:
        dict: Survey structure
    """
    # Parse hypothesis for key elements
    # Example: "AI tax optimizer for W-2 employees"
    parts = hypothesis.lower().split()
    
    # Extract problem/solution context
    problem = "tax optimization" if "tax" in hypothesis.lower() else "this problem"
    solution = hypothesis
    value_prop = f"saves you time and money on {problem}"
    
    # Get base template
    questions = SURVEY_TEMPLATES.get(template_type, SURVEY_TEMPLATES["product_validation"])
    
    # Customize questions
    customized = []
    for q in questions:
        customized_q = q.copy()
        customized_q["question"] = customized_q["question"].replace("[PROBLEM]", problem)
        customized_q["question"] = customized_q["question"].replace("[SOLUTION]", solution)
        customized_q["question"] = customized_q["question"].replace("[VALUE_PROP]", value_prop)
        customized_q["question"] = customized_q["question"].replace("[TIME_UNIT]", "month")
        
        # Customize feature list if present
        if "[FEATURE_LIST]" in str(customized_q.get("options", "")):
            if "tax" in hypothesis.lower():
                features = [
                    "Automatic deduction tracking",
                    "Real-time tax savings estimate",
                    "Integration with payroll",
                    "Year-end tax report generation",
                    "Audit protection"
                ]
            else:
                features = [
                    "Feature A",
                    "Feature B",
                    "Feature C",
                    "Feature D"
                ]
            customized_q["options"] = features
        
        customized.append(customized_q)
    
    survey = {
        "hypothesis": hypothesis,
        "template_type": template_type,
        "created_at": datetime.now().isoformat(),
        "total_questions": len(customized),
        "questions": customized,
        "distribution_templates": {}
    }
    
    # Generate distribution templates
    questions_text = "\n\n".join([
        f"Q{i+1}. {q['question']}\n   Type: {q['type']}\n" + 
        (f"   Options: {', '.join(q['options'])}" if 'options' in q else "") +
        (f"   Scale: {q['scale']}" if 'scale' in q else "")
        for i, q in enumerate(customized)
    ])
    
    for platform, template in DISTRIBUTION_TEMPLATES.items():
        survey["distribution_templates"][platform] = template.format(questions=questions_text)
    
    return survey

def main():
    parser = argparse.ArgumentParser(
        description="Generate customer survey from product hypothesis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate survey for product validation
  python survey-gen.py --hypothesis "AI tax optimizer for W-2 employees" --output survey.json
  
  # Generate pricing-focused survey
  python survey-gen.py --hypothesis "Premium budgeting app" --template pricing --output pricing-survey.json
        """
    )
    
    parser.add_argument("--hypothesis", required=True, help="Product hypothesis")
    parser.add_argument("--template", default="product_validation", choices=["product_validation", "pricing"], help="Survey template type")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument("--markdown", help="Optional markdown output file")
    
    args = parser.parse_args()
    
    print(f"Generating survey for: {args.hypothesis}", file=sys.stderr)
    
    survey = generate_survey(args.hypothesis, args.template)
    
    # Save JSON
    with open(args.output, "w") as f:
        json.dump(survey, f, indent=2)
    
    print(f"Survey saved to {args.output}", file=sys.stderr)
    
    # Save markdown if requested
    if args.markdown:
        with open(args.markdown, "w") as f:
            f.write(f"# Survey: {args.hypothesis}\n\n")
            f.write(f"**Created:** {survey['created_at']}\n\n")
            f.write(f"**Total Questions:** {survey['total_questions']}\n\n")
            f.write("## Questions\n\n")
            
            for i, q in enumerate(survey["questions"], 1):
                f.write(f"### Q{i}. {q['question']}\n\n")
                f.write(f"**Type:** {q['type']}\n\n")
                
                if "options" in q:
                    f.write("**Options:**\n")
                    for opt in q["options"]:
                        f.write(f"- {opt}\n")
                    f.write("\n")
                
                if "scale" in q:
                    f.write(f"**Scale:** {q['scale']}\n\n")
            
            f.write("\n## Distribution Templates\n\n")
            for platform, template in survey["distribution_templates"].items():
                f.write(f"### {platform.replace('_', ' ').title()}\n\n")
                f.write(f"```\n{template}\n```\n\n")
        
        print(f"Markdown version saved to {args.markdown}", file=sys.stderr)

if __name__ == "__main__":
    main()
