# AI PM Playbook: Self-Improving Feedback Loop

This script analyzes telemetry from recent PM activities (prototyping, evals, launches) and suggests improvements to the PM's workflows and templates.

## Usage

```bash
python3 pm_feedback_loop.py <path_to_telemetry.json>
```

## Telemetry Input Format

Provide a JSON file with the following structure:

```json
{
    "activity_type": "Prototype Sprint",
    "friction_points": [
        "Engineering rejected prototype due to incompatible tech stack",
        "Stakeholders confused by lack of specific delivery dates"
    ],
    "outcomes": {
        "time_to_prototype_days": 3,
        "user_validation_score": 4.5,
        "eval_pass_rate": 0.62
    }
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `activity_type` | string | The type of PM activity that was completed (e.g., "Prototype Sprint", "Eval Run", "Launch Review"). |
| `friction_points` | array of strings | A list of problems or blockers encountered during the activity. |
| `outcomes` | object | Key-value pairs of measurable results from the activity. |

## Keyword Detection Logic

The script scans each friction point for keywords and maps them to specific improvement suggestions. The table below documents the full keyword-to-suggestion mapping.

| Keywords Detected | Suggestion Generated | Target File |
| :--- | :--- | :--- |
| `eval`, `hallucination` | Update eval rubric to include stricter criteria for hallucination detection. | `templates/ai_eval_rubric.md` |
| `alignment`, `stakeholder` | Review the Now/Next/Later framework to ensure it is being communicated effectively. | `references/roadmap_uncertainty.md` |
| `prototype`, `rebuild` | Revisit Step 4 of the prototyping workflow to ensure prototypes use production-ready tools. | `references/prototyping_workflow.md` |
| `safety`, `guardrail`, `red team` | Review responsible AI practices and update the red teaming plan to cover identified safety gaps. | `references/responsible_ai.md`, `templates/red_teaming_plan.md` |
| `bias`, `fairness` | Update eval rubric to include specific test cases for bias and fairness. | `templates/ai_eval_rubric.md` |
| `latency`, `speed` | Ensure latency is being tracked as a core User Experience metric. | `references/evaluation_metrics.md` |
| `trust`, `privacy` | Strengthen the transparency and trust-building pillars of the GTM strategy. | `references/gtm_strategy.md` |

## Outcome Thresholds

| Outcome Key | Threshold | Suggestion |
| :--- | :--- | :--- |
| `eval_pass_rate` | Below 0.8 (80%) | Consider refining the model prompt or updating the evaluation criteria. |

## Source Code

```python
#!/usr/bin/env python3
"""
AI PM Playbook - Self-Improving Feedback Loop
This script analyzes telemetry from recent PM activities (prototyping, evals, launches)
and suggests improvements to the PM's workflows and templates.
"""

import json
import os
import sys
from datetime import datetime

def analyze_telemetry(telemetry_file):
    """Analyzes the provided telemetry data and generates improvement suggestions."""
    if not os.path.exists(telemetry_file):
        print(f"Error: Telemetry file '{telemetry_file}' not found.")
        print("Please provide a JSON file containing execution data.")
        sys.exit(1)

    try:
        with open(telemetry_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: '{telemetry_file}' is not a valid JSON file.")
        sys.exit(1)

    print(f"--- AI PM Playbook: Feedback Loop Analysis ---")
    print(f"Analyzing telemetry from: {data.get('activity_type', 'Unknown Activity')}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    suggestions = []

    # Analyze Friction Points
    friction_points = data.get('friction_points', [])
    if friction_points:
        print("Identified Friction Points:")
        for point in friction_points:
            print(f"  - {point}")
            
            # Generate suggestions based on common friction points
            if "eval" in point.lower() or "hallucination" in point.lower():
                suggestions.append("Update `templates/ai_eval_rubric.md` to include stricter criteria for hallucination detection.")
            if "alignment" in point.lower() or "stakeholder" in point.lower():
                suggestions.append("Review `references/roadmap_uncertainty.md` to ensure the Now/Next/Later framework is being communicated effectively.")
            if "prototype" in point.lower() or "rebuild" in point.lower():
                suggestions.append("Revisit `references/prototyping_workflow.md` Step 4 to ensure prototypes are being built with production-ready tools.")
            if "safety" in point.lower() or "guardrail" in point.lower() or "red team" in point.lower():
                suggestions.append("Review `references/responsible_ai.md` and update `templates/red_teaming_plan.md` to cover the identified safety gaps.")
            if "bias" in point.lower() or "fairness" in point.lower():
                suggestions.append("Update `templates/ai_eval_rubric.md` to include specific test cases for bias and fairness.")
            if "latency" in point.lower() or "speed" in point.lower():
                suggestions.append("Review `references/evaluation_metrics.md` to ensure latency is being tracked as a core User Experience metric.")
            if "trust" in point.lower() or "privacy" in point.lower():
                suggestions.append("Revisit `references/gtm_strategy.md` to strengthen the transparency and trust-building pillars of your GTM strategy.")
    else:
        print("No major friction points identified in this run.")

    # Analyze Outcomes
    outcomes = data.get('outcomes', {})
    if outcomes:
        print("\nExecution Outcomes:")
        for key, value in outcomes.items():
            print(f"  - {key}: {value}")
            if key == "eval_pass_rate" and isinstance(value, (int, float)) and value < 0.8:
                 suggestions.append(f"Eval pass rate is low ({value}). Consider refining the model prompt or updating the evaluation criteria.")

    # Output Suggestions
    print("\n--- Improvement Suggestions ---")
    if suggestions:
        for i, suggestion in enumerate(set(suggestions), 1):
            print(f"{i}. {suggestion}")
    else:
        print("No specific workflow improvements suggested at this time. Keep monitoring.")
        
    print("\nFeedback loop complete. Apply these suggestions to your templates and references.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pm_feedback_loop.py <path_to_telemetry.json>")
        print("\nExample telemetry.json format:")
        print("""
        {
            "activity_type": "Prototype Sprint",
            "friction_points": [
                "Engineering rejected prototype due to incompatible tech stack",
                "Stakeholders confused by lack of specific delivery dates"
            ],
            "outcomes": {
                "time_to_prototype_days": 3,
                "user_validation_score": 4.5
            }
        }
        """)
        sys.exit(1)
        
    analyze_telemetry(sys.argv[1])
```
