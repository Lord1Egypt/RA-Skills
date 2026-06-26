#!/usr/bin/env python3
"""
Requirement clarification framework.
Provides structured questions to help clarify vague requirements.
"""

import sys
import argparse
import json

# Question templates organized by project type
QUESTION_TEMPLATES = {
    'webapp': [
        "Who is the target user? (individuals, teams, public users)",
        "What's the core problem this solves?",
        "Any similar products to reference? (e.g., Twitter, Slack, Notion)",
        "Platform preference? (web, mobile, desktop, all)",
        "Timeline and scope? (quick prototype, MVP, full product)"
    ],
    'api': [
        "What data/functionality will this API provide?",
        "Who will consume this API? (internal services, third-party, public)",
        "Expected request volume? (low, medium, high)",
        "Authentication requirements? (none, API key, OAuth)",
        "Response format preference? (JSON, XML, GraphQL)"
    ],
    'automation': [
        "What manual process are you automating?",
        "How often does this need to run? (once, daily, on-demand)",
        "What triggers the automation? (time, event, manual)",
        "Where does input data come from?",
        "What should happen with the output?"
    ],
    'tool': [
        "What task does this tool help with?",
        "Who will use it? (just you, team, public)",
        "How will it be used? (CLI, GUI, web interface)",
        "What input does it need?",
        "What output should it produce?"
    ],
    'generic': [
        "What problem are you trying to solve?",
        "Who will use this?",
        "What's the expected outcome?",
        "Any technical constraints or preferences?",
        "Timeline and priority?"
    ]
}

def detect_project_type(requirement):
    """Detect project type from requirement text"""
    req_lower = requirement.lower()
    
    if any(word in req_lower for word in ['website', 'web app', 'dashboard', 'portal']):
        return 'webapp'
    elif any(word in req_lower for word in ['api', 'endpoint', 'service', 'backend']):
        return 'api'
    elif any(word in req_lower for word in ['automate', 'automation', 'script', 'cron']):
        return 'automation'
    elif any(word in req_lower for word in ['tool', 'utility', 'cli', 'command']):
        return 'tool'
    else:
        return 'generic'

def generate_questions(requirement, project_type=None):
    """Generate clarification questions based on requirement"""
    if project_type is None:
        project_type = detect_project_type(requirement)
    
    questions = QUESTION_TEMPLATES.get(project_type, QUESTION_TEMPLATES['generic'])
    
    return {
        'requirement': requirement,
        'detected_type': project_type,
        'questions': questions
    }

def main():
    parser = argparse.ArgumentParser(
        description='Generate clarification questions for vague requirements'
    )
    parser.add_argument(
        'requirement',
        help='The requirement to clarify (e.g., "I need a chat app")'
    )
    parser.add_argument(
        '--type',
        choices=['webapp', 'api', 'automation', 'tool', 'generic'],
        help='Override project type detection'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    
    args = parser.parse_args()
    
    result = generate_questions(args.requirement, args.type)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n📋 Requirement: {result['requirement']}")
        print(f"🔍 Detected type: {result['detected_type']}")
        print(f"\n❓ Clarification questions:\n")
        for i, q in enumerate(result['questions'], 1):
            print(f"{i}. {q}")
        print()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
