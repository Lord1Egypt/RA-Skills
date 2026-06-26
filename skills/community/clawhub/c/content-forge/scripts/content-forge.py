#!/usr/bin/env python3
"""
content-forge CLI
Generate content ideas, outlines, and drafts using AI/LLM patterns
"""

import argparse
import sys
import json
import random
from datetime import datetime

# Content templates and patterns
TEMPLATES = {
    "blog": {
        "how_to": {
            "title": "How to {action} in {timeframe}",
            "outline": [
                "Introduction: The problem with {topic}",
                "Step 1: {step1}",
                "Step 2: {step2}",
                "Step 3: {step3}",
                "Common mistakes to avoid",
                "Conclusion and next steps"
            ]
        },
        "listicle": {
            "title": "{number} {adjective} Ways to {action}",
            "outline": [
                "Introduction: Why {topic} matters",
                "Method 1: {method1}",
                "Method 2: {method2}",
                "Method 3: {method3}",
                "Bonus tip: {bonus}",
                "Conclusion"
            ]
        },
        "case_study": {
            "title": "How {company} {achievement} in {timeframe}",
            "outline": [
                "Introduction: The challenge",
                "Background: About {company}",
                "The problem they faced",
                "The solution they implemented",
                "Results and metrics",
                "Key takeaways"
            ]
        }
    },
    "social": {
        "twitter_thread": {
            "structure": [
                "Hook: {hook}",
                "Context: {context}",
                "Point 1: {point1}",
                "Point 2: {point2}",
                "Point 3: {point3}",
                "CTA: {cta}"
            ]
        },
        "linkedin_post": {
            "structure": [
                "Hook (1-2 sentences)",
                "Story/Insight (3-5 sentences)",
                "Key lesson/takeaway",
                "Engagement question"
            ]
        }
    }
}

CONTENT_PATTERNS = {
    "hooks": [
        "I spent {time} learning {topic}. Here's what I discovered:",
        "Stop doing {old_way}. Do this instead:",
        "The biggest myth about {topic}:",
        "In {year}, I {achievement}. Here's the exact process:",
        "Nobody talks about {topic}, but they should:"
    ],
    "adjectives": ["Proven", "Simple", "Effective", "Powerful", "Essential", "Game-Changing"],
    "timeframes": ["30 days", "1 week", "24 hours", "2025", "3 months", "6 months"],
    "actions": ["Grow Your Business", "Learn Faster", "Save Money", "Build an Audience", "Improve Productivity"]
}


def generate_blog_idea(topic, style="how_to"):
    """Generate a blog post idea"""
    if style not in TEMPLATES["blog"]:
        style = "how_to"
    
    template = TEMPLATES["blog"][style]
    
    # Fill in template variables
    variables = {
        "action": random.choice(CONTENT_PATTERNS["actions"]),
        "timeframe": random.choice(CONTENT_PATTERNS["timeframes"]),
        "topic": topic,
        "number": random.choice([3, 5, 7, 10]),
        "adjective": random.choice(CONTENT_PATTERNS["adjectives"]),
        "step1": f"Understand {topic} fundamentals",
        "step2": f"Apply {topic} techniques",
        "step3": f"Optimize your {topic} workflow",
        "method1": f"Start with small {topic} wins",
        "method2": f"Build consistent {topic} habits",
        "method3": f"Scale your {topic} efforts",
        "bonus": f"Advanced {topic} strategies",
        "company": "Company X",
        "achievement": "10x'd their results"
    }
    
    title = template["title"].format(**variables)
    outline = [item.format(**variables) for item in template["outline"]]
    
    return {
        "title": title,
        "outline": outline,
        "style": style,
        "topic": topic
    }


def generate_social_post(platform, topic, tone="professional"):
    """Generate social media content"""
    hook_template = random.choice(CONTENT_PATTERNS["hooks"])
    hook = hook_template.format(
        time=random.choice(["1 year", "6 months", "1000 hours"]),
        topic=topic,
        old_way=f"traditional {topic}",
        year="2024",
        achievement=f"mastered {topic}"
    )
    
    if platform == "twitter":
        posts = []
        posts.append(f"🧵 {hook}\n\n1/ 🧵")
        posts.append(f"2/ Most people get {topic} wrong because they focus on tactics, not strategy.")
        posts.append(f"3/ The real secret? Consistency beats intensity every time.")
        posts.append(f"4/ Start small. Master the basics. Then scale.\n\nThat's the formula.")
        posts.append(f"5/ What's your biggest challenge with {topic}?\n\nDrop a comment below 👇")
        return {"platform": "twitter", "thread": posts, "topic": topic}
    
    elif platform == "linkedin":
        content = f"""{hook}

I've been working with {topic} for {random.choice(['3 years', '5 years', 'over a decade'])}.

The one thing that separates those who succeed from those who don't?

They don't wait for perfect conditions. They start with what they have.

What's one thing you're going to start this week?

#{topic.replace(' ', '')} #ProfessionalGrowth #CareerAdvice"""
        return {"platform": "linkedin", "content": content, "topic": topic}
    
    return {"platform": platform, "content": "Platform not supported", "topic": topic}


def generate_content_calendar(topics, days=7):
    """Generate a content calendar"""
    content_types = ["blog", "twitter", "linkedin", "newsletter"]
    calendar = []
    
    for day in range(1, days + 1):
        topic = random.choice(topics)
        content_type = content_types[day % len(content_types)]
        
        if content_type == "blog":
            idea = generate_blog_idea(topic)
            title = idea["title"]
        elif content_type == "twitter":
            title = f"Twitter thread about {topic}"
        elif content_type == "linkedin":
            title = f"LinkedIn post: Lessons from {topic}"
        else:
            title = f"Newsletter: Deep dive into {topic}"
        
        calendar.append({
            "day": day,
            "type": content_type,
            "topic": topic,
            "title": title
        })
    
    return calendar


def generate_headlines(topic, count=10):
    """Generate click-worthy headlines"""
    templates = [
        "How to {action} Without {objection}",
        "The {adjective} Guide to {topic} in {year}",
        "{number} {topic} Mistakes That Cost You {cost}",
        "Why Most People Fail at {topic} (And How to Fix It)",
        "I Tried {topic} for {time}. Here's What Happened",
        "The Truth About {topic} Nobody Talks About",
        "{number} Ways to {action} Starting Today",
        "How {company} Used {topic} to {result}",
        "Stop {bad_action}. Start {good_action} Instead",
        "The Ultimate {topic} Checklist for {audience}"
    ]
    
    headlines = []
    for template in templates[:count]:
        headline = template.format(
            action=random.choice(["Get Started", "Scale Up", "Save Time"]),
            objection="Spending a Fortune",
            topic=topic,
            adjective=random.choice(CONTENT_PATTERNS["adjectives"]),
            year="2025",
            number=random.choice([3, 5, 7, 10]),
            cost="Thousands",
            time="30 Days",
            company="One Company",
            result="10x Their Revenue",
            bad_action="Wasting Time",
            good_action="Working Smarter",
            audience="Beginners"
        )
        headlines.append(headline)
    
    return headlines


def main():
    parser = argparse.ArgumentParser(description='Content Forge - AI Content Generator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Blog idea command
    blog_parser = subparsers.add_parser('blog', help='Generate blog post ideas')
    blog_parser.add_argument('topic', help='Topic to write about')
    blog_parser.add_argument('-s', '--style', choices=['how_to', 'listicle', 'case_study'],
                            default='how_to', help='Blog style')
    blog_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Social post command
    social_parser = subparsers.add_parser('social', help='Generate social media content')
    social_parser.add_argument('platform', choices=['twitter', 'linkedin'], help='Platform')
    social_parser.add_argument('topic', help='Topic to post about')
    social_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Calendar command
    calendar_parser = subparsers.add_parser('calendar', help='Generate content calendar')
    calendar_parser.add_argument('topics', nargs='+', help='List of topics')
    calendar_parser.add_argument('-d', '--days', type=int, default=7, help='Number of days')
    calendar_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Headlines command
    headlines_parser = subparsers.add_parser('headlines', help='Generate headlines')
    headlines_parser.add_argument('topic', help='Topic for headlines')
    headlines_parser.add_argument('-n', '--num', type=int, default=10, help='Number of headlines')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'blog':
        result = generate_blog_idea(args.topic, args.style)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n📝 Blog Idea: {result['title']}\n")
            print("Outline:")
            for i, item in enumerate(result['outline'], 1):
                print(f"  {i}. {item}")
            print()
    
    elif args.command == 'social':
        result = generate_social_post(args.platform, args.topic)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if args.platform == 'twitter':
                print(f"\n🐦 Twitter Thread about '{result['topic']}':\n")
                for post in result['thread']:
                    print(f"{post}\n")
            else:
                print(f"\n💼 LinkedIn Post:\n{result['content']}\n")
    
    elif args.command == 'calendar':
        result = generate_content_calendar(args.topics, args.days)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n📅 {args.days}-Day Content Calendar:\n")
            for item in result:
                print(f"Day {item['day']}: [{item['type'].upper()}] {item['title']}")
            print()
    
    elif args.command == 'headlines':
        headlines = generate_headlines(args.topic, args.num)
        print(f"\n📰 Headlines for '{args.topic}':\n")
        for i, headline in enumerate(headlines, 1):
            print(f"{i}. {headline}")
        print()


if __name__ == '__main__':
    main()
