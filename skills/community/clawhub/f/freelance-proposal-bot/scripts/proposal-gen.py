#!/usr/bin/env python3
import sys
import json
import re
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print('Usage: python proposal-gen.py \"your niche e.g. logo designer\"')
        sys.exit(1)
    niche = sys.argv[1]
    
    # Simulate web_search gigs (replace with exec tool call in real)
    gigs = [
        {'title': 'Modern logo for tech startup', 'desc': 'Need clean minimalist logo, budget $300, urgent.', 'client': 'TechCo', 'budget': '$300'},
        {'title': 'Brand logo redesign', 'desc': 'Refresh existing logo, vector, $250 max.', 'client': 'SmallBiz', 'budget': '$250'},
        {'title': 'Ecom logo', 'desc': 'Simple ecom brand logo, quick turnaround.', 'client': 'ShopOwner', 'budget': '$200'}
    ]
    
    proposals = []
    rate = 50  # $/hr demo
    for i, gig in enumerate(gigs, 1):
        proposal = f"""
Proposal {i} for '{gig['title']}' - Client: {gig['client']} (Budget: {gig['budget']})

Subject: Perfect Logo Designer for Your {gig['title']}

Hi {gig['client']},

Saw your gig for {gig['title']} – I specialize in {niche} with 50+ 5-star reviews. 

My approach:
- 3 concepts in 48 hours
- Unlimited revisions
- Vector files + source

Price: $250 fixed (fits your budget).

Portfolio: [your-portfolio-link]

Ready to start? Reply to kick off.

Best,
Your Name
Freelance Logo Designer
$50/hr | Upwork Top Rated

Follow-up (Day 3):
Hi {gig['client']}, checking in on logo gig – available Monday?
"""
        proposals.append(proposal)
    
    output = f'# Freelance Proposals for "{niche}" - {datetime.now().strftime("%Y-%m-%d")}\n\n' + ''.join(proposals)
    
    with open('proposals.md', 'w') as f:
        f.write(output)
    print('Proposals generated: proposals.md')

if __name__ == '__main__':
    main()
