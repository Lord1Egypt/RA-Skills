#!/usr/bin/env python3
"""
AI Ops Outreach Generator
Generates personalized cold outreach messages for AI Operations services.
"""
import argparse
import sys

CLIENT_TEMPLATES = {
    'solo_founder': {
        'pain_points': [
            'content creation',
            'social media management',
            'lead research',
            'admin tasks',
            'email management'
        ],
        'framing': 'cofounder',
        'price': '$200-500/month',
        'outcome': 'your project moving forward every day',
        'time_saved': '10-15 hours per week'
    },
    'agency_owner': {
        'pain_points': [
            'client reporting',
            'lead follow-up',
            'data aggregation',
            'competitive research'
        ],
        'framing': 'automation partner',
        'price': '$500-1,500/month',
        'outcome': 'automated workflows that scale',
        'time_saved': '20+ hours per week'
    },
    'consultant': {
        'pain_points': [
            'market research',
            'due diligence',
            'competitive analysis',
            'report generation'
        ],
        'framing': 'research analyst',
        'price': '$500-2,000/month',
        'outcome': 'deliver more client work without hiring',
        'time_saved': '15-20 hours per week'
    },
    'ecommerce': {
        'pain_points': [
            'competitor price monitoring',
            'inventory management',
            'customer review analysis',
            'product research'
        ],
        'framing': 'operations manager',
        'price': '$300-800/month',
        'outcome': 'know everything about your market instantly',
        'time_saved': '8-12 hours per week'
    }
}

SUBJECTS = [
    "Your AI operations, handled",
    "Stop doing {pain} manually",
    "The AI cofounder setup for {industry}",
    "{pain.title()} on autopilot — interested?",
]

def generate_outreach(client_type, industry=None, specific_pain=None):
    t = CLIENT_TEMPLATES.get(client_type, CLIENT_TEMPLATES['solo_founder'])
    pain = specific_pain or t['pain_points'][0]
    industry = industry or 'your business'
    
    subject_templates = [
        f"Your AI operations, handled",
        f"Stop doing {pain} manually — I run it for you",
        f"The AI ops setup that handles {pain} 24/7",
    ]
    
    bodies = [
        f"""Hi,

You're probably spending too much time on {pain}.

I manage AI operations for {industry} — which means I handle the {pain} work so you can focus on growth.

Most clients save {t['time_saved']} in the first month. They don't manage AI. I do.

Setup fee: waived this month. {t['price']} after. Cancel anytime.

Interested?""",

        f"""Hi,

{industry.capitalize()} owners tell me the same thing: they have the strategy, but execution suffers because of {pain}.

I run AI operations — the {pain} gets handled every day without you thinking about it.

Not a tool you learn. Not a dashboard you check. Just {t['outcome']}.

{', '.join(t['pain_points'][:3]).title()} — all handled.

{'$300/month' if client_type == 'solo_founder' else t['price']}, no contract. Worth a 15-min call?""",

        f"""Hi,

I manage AI agents for {industry} owners who are buried in {pain}.

The setup: I connect to your tools, learn your workflows, and run them 24/7.

The result: {t['outcome']}.

One client used to spend every Sunday on content. Now AI handles it while she sleeps. Her job: review what AI produced.

Looking for 2 more clients to onboard this month.

Is that interesting?""",
    ]
    
    return {
        'subjects': subject_templates,
        'bodies': bodies,
        'client_type': client_type,
        'pain': pain,
        'price': t['price'],
        'time_saved': t['time_saved'],
        'outro': f"\n---\nGenerated for: {client_type}\nPrice: {t['price']}\nTime saved: {t['time_saved']}"
    }

def main():
    parser = argparse.ArgumentParser(description='Generate AI Ops outreach messages')
    parser.add_argument('--client', default='solo_founder',
                        choices=list(CLIENT_TEMPLATES.keys()),
                        help='Client type')
    parser.add_argument('--industry', default=None, help='Specific industry')
    parser.add_argument('--pain', default=None, help='Specific pain point')
    parser.add_argument('--format', default='markdown',
                        choices=['markdown', 'plain', 'email'])
    args = parser.parse_args()

    result = generate_outreach(args.client, args.industry, args.pain)
    
    print(f"=== AI Ops Outreach Generator ===")
    print(f"Client: {args.client} | Pain: {result['pain']} | Price: {result['price']}")
    print()
    
    for i, (subj, body) in enumerate(zip(result['subjects'], result['bodies']), 1):
        print(f"--- Variant {i} ---")
        print(f"Subject: {subj}")
        print()
        print(body)
        print(result['outro'])
        print()
    
    print(f"\nUsage examples:")
    print(f"  python3 generate_outreach.py --client agency_owner")
    print(f"  python3 generate_outreach.py --client ecommerce --pain 'competitor monitoring'")

if __name__ == '__main__':
    main()
