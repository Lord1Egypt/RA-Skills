#!/usr/bin/env python3
"""
Persona Validation Script
Cross-references persona assumptions against real customer data.
"""

import argparse
import json
import sys
from datetime import datetime
from collections import defaultdict

def load_persona(persona_path):
    """Load persona JSON file."""
    with open(persona_path, "r") as f:
        return json.load(f)

def load_insights(insights_path):
    """Load Reddit insights JSON file."""
    with open(insights_path, "r") as f:
        return json.load(f)

def validate_pain_points(persona, insights):
    """Validate persona pain points against Reddit data."""
    persona_pains = persona.get("pain_points", [])
    reddit_pains = insights.get("pain_points", [])
    
    validation = {
        "validated": [],
        "unvalidated": [],
        "additional_signals": []
    }
    
    # Check each persona pain point
    for pain in persona_pains:
        pain_lower = pain.lower()
        matches = []
        
        for reddit_pain in reddit_pains:
            # Check if pain point appears in Reddit data
            text = reddit_pain.get("text", "").lower()
            keywords = [kw.lower() for kw in reddit_pain.get("keywords", [])]
            
            # Simple keyword matching
            if any(kw in pain_lower for kw in keywords) or any(word in text for word in pain_lower.split()):
                matches.append({
                    "source": reddit_pain.get("url"),
                    "text": reddit_pain.get("text"),
                    "score": reddit_pain.get("score"),
                    "sentiment": reddit_pain.get("sentiment")
                })
        
        if matches:
            validation["validated"].append({
                "pain_point": pain,
                "evidence_count": len(matches),
                "top_evidence": sorted(matches, key=lambda x: x["score"], reverse=True)[:3]
            })
        else:
            validation["unvalidated"].append({
                "pain_point": pain,
                "note": "No direct evidence found in Reddit data"
            })
    
    # Find additional pain points from Reddit not in persona
    reddit_themes = set()
    for reddit_pain in reddit_pains[:20]:  # Top 20
        for keyword in reddit_pain.get("keywords", []):
            reddit_themes.add(keyword.lower())
    
    persona_themes = set()
    for pain in persona_pains:
        persona_themes.update(pain.lower().split())
    
    additional = reddit_themes - persona_themes
    if additional:
        validation["additional_signals"] = [
            {
                "theme": theme,
                "note": "Found in Reddit data but not in persona"
            }
            for theme in list(additional)[:10]
        ]
    
    return validation

def validate_demographics(persona, insights):
    """Validate demographic assumptions."""
    demographics = persona.get("demographics", {})
    
    validation = {
        "validated": [],
        "assumptions": [],
        "notes": []
    }
    
    # Note: Reddit data doesn't typically include detailed demographics
    # This section flags demographic claims as assumptions requiring survey validation
    for key, value in demographics.items():
        validation["assumptions"].append({
            "field": key,
            "claimed_value": value,
            "note": "Demographic data not available in Reddit insights. Validate via survey or interviews."
        })
    
    return validation

def validate_goals(persona, insights):
    """Validate persona goals against feature requests."""
    persona_goals = persona.get("goals", [])
    feature_requests = insights.get("feature_requests", [])
    
    validation = {
        "validated": [],
        "unvalidated": [],
        "additional_goals": []
    }
    
    for goal in persona_goals:
        goal_lower = goal.lower()
        matches = []
        
        for req in feature_requests:
            text = req.get("text", "").lower()
            patterns = [p.lower() for p in req.get("patterns", [])]
            
            if any(word in text for word in goal_lower.split()) or any(p in goal_lower for p in patterns):
                matches.append({
                    "source": req.get("url"),
                    "text": req.get("text"),
                    "score": req.get("score")
                })
        
        if matches:
            validation["validated"].append({
                "goal": goal,
                "evidence_count": len(matches),
                "top_evidence": sorted(matches, key=lambda x: x["score"], reverse=True)[:3]
            })
        else:
            validation["unvalidated"].append({
                "goal": goal,
                "note": "No direct evidence in feature requests"
            })
    
    return validation

def calculate_confidence_score(validation_results):
    """Calculate overall confidence score (0-100)."""
    pain_points = validation_results.get("pain_points", {})
    goals = validation_results.get("goals", {})
    
    total_claims = 0
    validated_claims = 0
    
    # Pain points
    total_claims += len(pain_points.get("validated", [])) + len(pain_points.get("unvalidated", []))
    validated_claims += len(pain_points.get("validated", []))
    
    # Goals
    total_claims += len(goals.get("validated", [])) + len(goals.get("unvalidated", []))
    validated_claims += len(goals.get("validated", []))
    
    if total_claims == 0:
        return 0
    
    confidence = int((validated_claims / total_claims) * 100)
    return confidence

def validate_persona(persona_path, insights_path):
    """
    Validate persona against Reddit insights.
    
    Args:
        persona_path: Path to persona JSON
        insights_path: Path to Reddit insights JSON
    
    Returns:
        dict: Validation results
    """
    persona = load_persona(persona_path)
    insights = load_insights(insights_path)
    
    validation_results = {
        "persona_name": persona.get("name", "Unknown"),
        "validated_at": datetime.now().isoformat(),
        "data_source": insights.get("category"),
        "subreddits_analyzed": insights.get("subreddits_searched"),
        "pain_points": validate_pain_points(persona, insights),
        "demographics": validate_demographics(persona, insights),
        "goals": validate_goals(persona, insights),
        "recommendations": []
    }
    
    # Calculate confidence score
    confidence = calculate_confidence_score(validation_results)
    validation_results["confidence_score"] = confidence
    
    # Generate recommendations
    if confidence < 50:
        validation_results["recommendations"].append(
            "LOW CONFIDENCE: Persona has weak evidence. Conduct customer interviews to validate assumptions."
        )
    elif confidence < 75:
        validation_results["recommendations"].append(
            "MODERATE CONFIDENCE: Some claims validated, but gaps remain. Run targeted surveys on unvalidated points."
        )
    else:
        validation_results["recommendations"].append(
            "HIGH CONFIDENCE: Persona is well-supported by data. Consider additional validation for demographic assumptions."
        )
    
    # Flag unvalidated pain points
    unvalidated_pains = validation_results["pain_points"].get("unvalidated", [])
    if unvalidated_pains:
        validation_results["recommendations"].append(
            f"UNVALIDATED PAIN POINTS: {len(unvalidated_pains)} pain point(s) lack evidence. Verify in customer interviews."
        )
    
    # Flag additional signals
    additional = validation_results["pain_points"].get("additional_signals", [])
    if additional:
        validation_results["recommendations"].append(
            f"MISSING THEMES: {len(additional)} theme(s) found in data but not in persona. Consider adding: {', '.join([s['theme'] for s in additional[:5]])}"
        )
    
    return validation_results

def main():
    parser = argparse.ArgumentParser(
        description="Validate persona against customer research data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate persona against Reddit insights
  python persona-validator.py --persona persona.json --insights reddit-insights.json --output validated.json
  
  # Generate markdown report
  python persona-validator.py --persona persona.json --insights reddit-insights.json --output validated.json --markdown report.md
        """
    )
    
    parser.add_argument("--persona", required=True, help="Persona JSON file")
    parser.add_argument("--insights", required=True, help="Reddit insights JSON file")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument("--markdown", help="Optional markdown report")
    
    args = parser.parse_args()
    
    print(f"Validating persona: {args.persona}", file=sys.stderr)
    print(f"Against insights: {args.insights}", file=sys.stderr)
    
    validation = validate_persona(args.persona, args.insights)
    
    # Save JSON
    with open(args.output, "w") as f:
        json.dump(validation, f, indent=2)
    
    print(f"\nValidation complete!", file=sys.stderr)
    print(f"Confidence score: {validation['confidence_score']}/100", file=sys.stderr)
    print(f"Results saved to {args.output}", file=sys.stderr)
    
    # Save markdown if requested
    if args.markdown:
        with open(args.markdown, "w") as f:
            f.write(f"# Persona Validation Report\n\n")
            f.write(f"**Persona:** {validation['persona_name']}\n\n")
            f.write(f"**Validated:** {validation['validated_at']}\n\n")
            f.write(f"**Data Source:** {validation['data_source']}\n\n")
            f.write(f"**Confidence Score:** {validation['confidence_score']}/100\n\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            for rec in validation["recommendations"]:
                f.write(f"- {rec}\n")
            f.write("\n")
            
            # Pain Points Validation
            f.write("## Pain Points Validation\n\n")
            
            validated = validation["pain_points"].get("validated", [])
            if validated:
                f.write("### ✅ Validated Pain Points\n\n")
                for item in validated:
                    f.write(f"**{item['pain_point']}**\n\n")
                    f.write(f"Evidence count: {item['evidence_count']}\n\n")
                    f.write("Top evidence:\n\n")
                    for ev in item["top_evidence"]:
                        f.write(f"- [{ev['text'][:100]}...]({ev['source']}) (Score: {ev['score']})\n")
                    f.write("\n")
            
            unvalidated = validation["pain_points"].get("unvalidated", [])
            if unvalidated:
                f.write("### ⚠️ Unvalidated Pain Points\n\n")
                for item in unvalidated:
                    f.write(f"- **{item['pain_point']}**: {item['note']}\n")
                f.write("\n")
            
            additional = validation["pain_points"].get("additional_signals", [])
            if additional:
                f.write("### 💡 Additional Signals (Not in Persona)\n\n")
                for item in additional[:10]:
                    f.write(f"- {item['theme']}\n")
                f.write("\n")
            
            # Demographics
            f.write("## Demographics Validation\n\n")
            assumptions = validation["demographics"].get("assumptions", [])
            if assumptions:
                f.write("**Note:** Demographics require survey/interview validation.\n\n")
                for item in assumptions:
                    f.write(f"- **{item['field']}**: {item['claimed_value']} ({item['note']})\n")
                f.write("\n")
            
            # Goals
            f.write("## Goals Validation\n\n")
            
            validated_goals = validation["goals"].get("validated", [])
            if validated_goals:
                f.write("### ✅ Validated Goals\n\n")
                for item in validated_goals:
                    f.write(f"**{item['goal']}**\n\n")
                    f.write(f"Evidence count: {item['evidence_count']}\n\n")
            
            unvalidated_goals = validation["goals"].get("unvalidated", [])
            if unvalidated_goals:
                f.write("### ⚠️ Unvalidated Goals\n\n")
                for item in unvalidated_goals:
                    f.write(f"- **{item['goal']}**: {item['note']}\n")
        
        print(f"Markdown report saved to {args.markdown}", file=sys.stderr)

if __name__ == "__main__":
    main()
