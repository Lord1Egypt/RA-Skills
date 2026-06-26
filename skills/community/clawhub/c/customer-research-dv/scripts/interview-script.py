#!/usr/bin/env python3
"""
Interview Script Generator
Creates structured customer interview scripts tailored to persona.
"""

import argparse
import json
import sys
from datetime import datetime

INTERVIEW_FRAMEWORKS = {
    "jobs_to_be_done": {
        "intro": [
            "Thank you for taking the time to speak with me today.",
            "I'm researching how people currently handle [PROBLEM_AREA].",
            "This is not a sales call - I'm genuinely trying to understand your workflow and challenges.",
            "The interview will take about 30 minutes. Is now still a good time?"
        ],
        "sections": [
            {
                "title": "Background & Context",
                "questions": [
                    "Tell me about your role and what you do day-to-day.",
                    "How long have you been in this position?",
                    "What are your main responsibilities related to [PROBLEM_AREA]?"
                ],
                "follow_ups": [
                    "Can you walk me through a typical [workflow/process]?",
                    "Who else is involved in this process?"
                ]
            },
            {
                "title": "Current Solution",
                "questions": [
                    "How do you currently solve [PROBLEM]?",
                    "What tools or systems do you use?",
                    "When did you start using this approach?"
                ],
                "follow_ups": [
                    "What made you choose that solution?",
                    "What alternatives did you consider?",
                    "How much does your current solution cost (time and money)?"
                ]
            },
            {
                "title": "Pain Points",
                "questions": [
                    "What's the most frustrating part of your current approach?",
                    "What would you improve if you could wave a magic wand?",
                    "Tell me about a recent time when [PROBLEM] caused issues."
                ],
                "follow_ups": [
                    "How often does that happen?",
                    "What's the impact when it goes wrong?",
                    "Have you tried to solve this before? What happened?"
                ]
            },
            {
                "title": "Ideal Solution",
                "questions": [
                    "If you could design the perfect solution, what would it look like?",
                    "What features would be must-haves vs nice-to-haves?",
                    "How would you measure success for a new solution?"
                ],
                "follow_ups": [
                    "What would make you switch from your current solution?",
                    "What would prevent you from switching?"
                ]
            },
            {
                "title": "Willingness to Pay",
                "questions": [
                    "What do you currently spend on solving this problem (time + money)?",
                    "If a solution saved you [X hours/week] or [Y dollars/month], what would that be worth to you?",
                    "Would you pay for a solution monthly, annually, or prefer one-time purchase?"
                ],
                "follow_ups": [
                    "Who makes the purchasing decision?",
                    "What's your budget approval process like?",
                    "What price range would make you think 'that's too expensive'?"
                ]
            },
            {
                "title": "Decision Process",
                "questions": [
                    "How do you typically evaluate new tools or solutions?",
                    "Who else would need to approve a new solution?",
                    "What would be your biggest concern about adopting something new?"
                ],
                "follow_ups": [
                    "How long does your evaluation process typically take?",
                    "What would need to be true for you to try a beta version?"
                ]
            }
        ],
        "closing": [
            "Is there anything else about [PROBLEM_AREA] that we haven't covered?",
            "Do you know anyone else who might have insights on this topic?",
            "Would you be open to a follow-up conversation once we've built something?",
            "Thank you so much for your time. This has been incredibly helpful."
        ]
    },
    "problem_validation": {
        "intro": [
            "Thanks for joining me today.",
            "I'm researching [PROBLEM_AREA] and would love to hear about your experience.",
            "Everything you share will be confidential - we're just trying to understand the problem space.",
            "Sound good? Let's dive in."
        ],
        "sections": [
            {
                "title": "Problem Discovery",
                "questions": [
                    "Tell me about the last time you dealt with [PROBLEM].",
                    "How often does this come up for you?",
                    "On a scale of 1-10, how painful is this problem?"
                ],
                "follow_ups": [
                    "Why that number?",
                    "What makes it so painful?",
                    "Is this getting better or worse over time?"
                ]
            },
            {
                "title": "Current Workarounds",
                "questions": [
                    "How are you handling this now?",
                    "What have you tried that didn't work?",
                    "If you do nothing, what happens?"
                ],
                "follow_ups": [
                    "How much time does your current approach take?",
                    "What's the cost (money, time, stress)?",
                    "Who else is impacted by this problem?"
                ]
            },
            {
                "title": "Solution Validation",
                "questions": [
                    "If I could solve [SPECIFIC PAIN POINT], would that be valuable?",
                    "What would success look like?",
                    "What concerns would you have about a new solution?"
                ],
                "follow_ups": [
                    "What would make you trust a new solution?",
                    "How would you want to learn about it?",
                    "What would make you recommend it to others?"
                ]
            }
        ],
        "closing": [
            "What's the one thing I should know about [PROBLEM_AREA] that I haven't asked?",
            "Who else should I talk to about this?",
            "Can I reach out if we build something?",
            "Thank you - this has been really valuable."
        ]
    }
}

PERSONA_TEMPLATES = {
    "tech_pm_high_earner": {
        "title": "Tech PM ($200K+)",
        "problem_area": "productivity and efficiency",
        "problem": "staying organized and productive",
        "specific_contexts": [
            "managing multiple projects",
            "stakeholder communication",
            "prioritization decisions"
        ]
    },
    "solopreneur": {
        "title": "Solopreneur / Indie Maker",
        "problem_area": "business operations",
        "problem": "running a business solo",
        "specific_contexts": [
            "customer acquisition",
            "product development",
            "financial management"
        ]
    },
    "corporate_exec": {
        "title": "Corporate Executive",
        "problem_area": "strategic decision-making",
        "problem": "making data-driven decisions",
        "specific_contexts": [
            "team performance",
            "budget allocation",
            "competitive positioning"
        ]
    },
    "small_business_owner": {
        "title": "Small Business Owner",
        "problem_area": "business growth",
        "problem": "scaling operations",
        "specific_contexts": [
            "hiring and training",
            "customer retention",
            "cash flow management"
        ]
    }
}

def generate_interview_script(persona_type, framework="jobs_to_be_done", custom_problem=None):
    """
    Generate interview script tailored to persona.
    
    Args:
        persona_type: Type of persona (or custom dict)
        framework: Interview framework to use
        custom_problem: Optional custom problem area
    
    Returns:
        dict: Interview script structure
    """
    # Get persona template
    if isinstance(persona_type, str):
        persona = PERSONA_TEMPLATES.get(persona_type, PERSONA_TEMPLATES["solopreneur"])
    else:
        persona = persona_type
    
    # Get framework
    framework_template = INTERVIEW_FRAMEWORKS.get(framework, INTERVIEW_FRAMEWORKS["jobs_to_be_done"])
    
    # Customize questions
    problem_area = custom_problem or persona["problem_area"]
    problem = persona["problem"]
    
    script = {
        "persona": persona["title"],
        "problem_area": problem_area,
        "framework": framework,
        "created_at": datetime.now().isoformat(),
        "estimated_duration": "30-45 minutes",
        "intro": [q.replace("[PROBLEM_AREA]", problem_area) for q in framework_template["intro"]],
        "sections": [],
        "closing": [q.replace("[PROBLEM_AREA]", problem_area) for q in framework_template["closing"]]
    }
    
    # Customize sections
    for section in framework_template["sections"]:
        customized_section = {
            "title": section["title"],
            "duration": "5-7 minutes",
            "questions": [
                q.replace("[PROBLEM_AREA]", problem_area).replace("[PROBLEM]", problem)
                for q in section["questions"]
            ],
            "follow_ups": [
                f.replace("[PROBLEM_AREA]", problem_area).replace("[PROBLEM]", problem)
                for f in section["follow_ups"]
            ],
            "notes": []
        }
        
        # Add persona-specific context
        if "specific_contexts" in persona:
            customized_section["notes"].append(
                f"Persona-specific contexts to probe: {', '.join(persona['specific_contexts'])}"
            )
        
        script["sections"].append(customized_section)
    
    return script

def main():
    parser = argparse.ArgumentParser(
        description="Generate customer interview script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate script for tech PM persona
  python interview-script.py --persona tech_pm_high_earner --output interview.json
  
  # Custom problem area
  python interview-script.py --persona solopreneur --problem "content marketing" --output marketing-interview.json
  
  # Problem validation framework
  python interview-script.py --persona small_business_owner --framework problem_validation --output validation.json
  
Available personas:
  - tech_pm_high_earner
  - solopreneur
  - corporate_exec
  - small_business_owner
        """
    )
    
    parser.add_argument("--persona", required=True, help="Persona type")
    parser.add_argument("--framework", default="jobs_to_be_done", choices=["jobs_to_be_done", "problem_validation"], help="Interview framework")
    parser.add_argument("--problem", help="Custom problem area")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument("--markdown", help="Optional markdown output")
    
    args = parser.parse_args()
    
    print(f"Generating interview script for: {args.persona}", file=sys.stderr)
    
    script = generate_interview_script(args.persona, args.framework, args.problem)
    
    # Save JSON
    with open(args.output, "w") as f:
        json.dump(script, f, indent=2)
    
    print(f"Interview script saved to {args.output}", file=sys.stderr)
    
    # Save markdown if requested
    if args.markdown:
        with open(args.markdown, "w") as f:
            f.write(f"# Customer Interview Script\n\n")
            f.write(f"**Persona:** {script['persona']}\n\n")
            f.write(f"**Problem Area:** {script['problem_area']}\n\n")
            f.write(f"**Framework:** {script['framework']}\n\n")
            f.write(f"**Duration:** {script['estimated_duration']}\n\n")
            f.write(f"**Created:** {script['created_at']}\n\n")
            
            f.write("## Introduction\n\n")
            for line in script["intro"]:
                f.write(f"- {line}\n")
            f.write("\n")
            
            for section in script["sections"]:
                f.write(f"## {section['title']}\n\n")
                f.write(f"**Duration:** {section['duration']}\n\n")
                
                f.write("### Core Questions\n\n")
                for q in section["questions"]:
                    f.write(f"1. {q}\n")
                f.write("\n")
                
                f.write("### Follow-up Prompts\n\n")
                for fu in section["follow_ups"]:
                    f.write(f"- {fu}\n")
                f.write("\n")
                
                if section["notes"]:
                    f.write("### Notes\n\n")
                    for note in section["notes"]:
                        f.write(f"- {note}\n")
                    f.write("\n")
            
            f.write("## Closing\n\n")
            for line in script["closing"]:
                f.write(f"- {line}\n")
        
        print(f"Markdown version saved to {args.markdown}", file=sys.stderr)

if __name__ == "__main__":
    main()
