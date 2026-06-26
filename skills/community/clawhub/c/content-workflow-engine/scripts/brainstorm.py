#!/usr/bin/env python3
"""
Generate content ideas using AI or templates.

This script helps with content ideation by generating ideas
based on topics, keywords, or trends.
"""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

# Idea templates for different content types
IDEA_TEMPLATES = {
    "blog": [
        "How {topic} is Changing in {year}",
        "The Ultimate Guide to {topic}",
        "{number} Tools for Better {topic}",
        "Common Mistakes in {topic} and How to Avoid Them",
        "The Future of {topic}: {number} Predictions",
        "{topic} Best Practices for {audience}",
        "Why {topic} Matters More Than Ever",
        "Getting Started with {topic}: A Beginner's Guide",
        "Advanced Techniques for {topic}",
        "{topic} vs. {alternative}: Which is Right for You?"
    ],
    "social": [
        "Quick tip: {tip}",
        "Did you know? {fact}",
        "Question: {question}",
        "Poll: {poll_question}",
        "Thread: {thread_topic}",
        "Behind the scenes: {behind_scenes}",
        "Case study: {case_study}",
        "Resource: {resource}",
        "Announcement: {announcement}",
        "Quote: {quote}"
    ],
    "video": [
        "How to {action} in {time} minutes",
        "{topic} Tutorial for Beginners",
        "{number} Things You Didn't Know About {topic}",
        "Reacting to {reaction_topic}",
        "Interview with {person} about {topic}",
        "{topic} Explained Simply",
        "My Experience with {topic}",
        "{topic} Tools and Resources",
        "Common {topic} Questions Answered",
        "{topic} Case Study Analysis"
    ],
    "newsletter": [
        "Weekly Roundup: {week_date}",
        "{topic} News and Updates",
        "Industry Insights: {insight_topic}",
        "Resource Roundup: {resource_type}",
        "Behind the Blog: {behind_topic}",
        "Community Spotlight: {community_topic}",
        "Tips and Tricks: {tip_topic}",
        "Upcoming Events: {event_topic}",
        "Reader Questions Answered",
        "Monthly Digest: {month}"
    ]
}

# Fillers for template variables
TEMPLATE_FILLERS = {
    "year": ["2025", "2026", "this year", "next year"],
    "number": ["5", "7", "10", "15", "21"],
    "audience": ["beginners", "experts", "business owners", "creators", "developers"],
    "tip": ["improve your workflow", "save time", "increase engagement", "boost productivity"],
    "fact": ["most people overlook this", "this statistic will surprise you", "research shows"],
    "question": ["what's your biggest challenge?", "how do you handle this?", "what would you add?"],
    "poll_question": ["which option do you prefer?", "vote for your favorite", "what's your opinion?"],
    "thread_topic": ["breaking down complex concepts", "step-by-step guide", "common misconceptions"],
    "behind_scenes": ["how we create content", "our production process", "tools we use"],
    "case_study": ["how we achieved results", "client success story", "project breakdown"],
    "resource": ["free template", "helpful tool", "useful guide"],
    "announcement": ["new feature", "upcoming event", "product launch"],
    "quote": ["inspiring words", "industry insight", "thought leadership"],
    "action": ["master", "learn", "implement", "optimize"],
    "time": ["5", "10", "15", "30"],
    "reaction_topic": ["industry news", "controversial topic", "new technology"],
    "person": ["industry expert", "successful creator", "thought leader"],
    "week_date": ["this week", "last week", "the past 7 days"],
    "insight_topic": ["market trends", "consumer behavior", "technology shifts"],
    "resource_type": ["free tools", "helpful articles", "useful templates"],
    "behind_topic": ["our content process", "team insights", "what we're working on"],
    "community_topic": ["member achievements", "community projects", "user stories"],
    "tip_topic": ["productivity", "creativity", "efficiency"],
    "event_topic": ["webinars", "conferences", "workshops"],
    "month": ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"],
    "alternative": ["traditional methods", "competing solutions", "other approaches"]
}

def generate_ideas(topic, content_type, count=10, use_ai=False):
    """Generate content ideas based on topic and type."""
    
    if content_type not in IDEA_TEMPLATES:
        raise ValueError(f"Unsupported content type: {content_type}. Choose from: {list(IDEA_TEMPLATES.keys())}")
    
    templates = IDEA_TEMPLATES[content_type]
    ideas = []
    
    for i in range(count):
        # Select random template
        template = random.choice(templates)
        
        # Fill template variables
        idea = template
        for var in ["{topic}", "{year}", "{number}", "{audience}", "{tip}", "{fact}", 
                   "{question}", "{poll_question}", "{thread_topic}", "{behind_scenes}",
                   "{case_study}", "{resource}", "{announcement}", "{quote}", "{action}",
                   "{time}", "{reaction_topic}", "{person}", "{week_date}", "{insight_topic}",
                   "{resource_type}", "{behind_topic}", "{community_topic}", "{tip_topic}",
                   "{event_topic}", "{month}", "{alternative}"]:
            if var in idea:
                var_name = var.strip("{}")
                if var_name in TEMPLATE_FILLERS:
                    filler = random.choice(TEMPLATE_FILLERS[var_name])
                    idea = idea.replace(var, filler)
                elif var_name == "topic":
                    idea = idea.replace(var, topic)
        
        ideas.append({
            "id": i + 1,
            "title": idea,
            "type": content_type,
            "topic": topic,
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "estimated_time": f"{random.randint(1, 8)} hours",
            "target_audience": random.choice(["beginners", "intermediate", "experts"]),
            "keywords": generate_keywords(topic, content_type)
        })
    
    return ideas

def generate_keywords(topic, content_type):
    """Generate relevant keywords for an idea."""
    base_keywords = [topic.lower(), content_type]
    
    # Add type-specific keywords
    if content_type == "blog":
        base_keywords.extend(["guide", "tutorial", "how-to", "tips"])
    elif content_type == "social":
        base_keywords.extend(["social media", "engagement", "community"])
    elif content_type == "video":
        base_keywords.extend(["video", "tutorial", "visual", "explainer"])
    elif content_type == "newsletter":
        base_keywords.extend(["email", "subscribers", "updates", "digest"])
    
    # Add some random related terms
    related_terms = ["2025", "trends", "best practices", "tools", "resources", 
                    "strategies", "examples", "case studies"]
    
    keywords = base_keywords + random.sample(related_terms, 3)
    return list(set(keywords))  # Remove duplicates

def save_ideas(ideas, output_file=None):
    """Save generated ideas to a file."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"brainstorm_{timestamp}.json"
    
    output_path = Path("brainstorm_output")
    output_path.mkdir(exist_ok=True)
    
    full_path = output_path / output_file
    
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "total_ideas": len(ideas),
        "ideas": ideas
    }
    
    with open(full_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    return full_path

def print_ideas(ideas, format="table"):
    """Print ideas in specified format."""
    if format == "table":
        print(f"\n{'ID':<4} {'Title':<60} {'Difficulty':<10} {'Time':<10}")
        print("-" * 90)
        for idea in ideas:
            print(f"{idea['id']:<4} {idea['title'][:57]:<60} {idea['difficulty']:<10} {idea['estimated_time']:<10}")
    
    elif format == "detailed":
        for idea in ideas:
            print(f"\n{'='*80}")
            print(f"Idea #{idea['id']}: {idea['title']}")
            print(f"{'='*80}")
            print(f"Type: {idea['type']}")
            print(f"Topic: {idea['topic']}")
            print(f"Difficulty: {idea['difficulty']}")
            print(f"Estimated time: {idea['estimated_time']}")
            print(f"Target audience: {idea['target_audience']}")
            print(f"Keywords: {', '.join(idea['keywords'])}")
    
    elif format == "json":
        print(json.dumps(ideas, indent=2))
    
    elif format == "simple":
        for idea in ideas:
            print(f"{idea['id']}. {idea['title']}")

def main():
    parser = argparse.ArgumentParser(description="Generate content ideas")
    parser.add_argument("--topic", required=True, help="Main topic for content ideas")
    parser.add_argument("--type", choices=list(IDEA_TEMPLATES.keys()), 
                       default="blog", help="Type of content to generate ideas for")
    parser.add_argument("--count", type=int, default=10, help="Number of ideas to generate")
    parser.add_argument("--format", choices=["table", "detailed", "json", "simple"],
                       default="table", help="Output format")
    parser.add_argument("--save", action="store_true", help="Save ideas to file")
    parser.add_argument("--output", help="Output file name (default: auto-generated)")
    parser.add_argument("--use-ai", action="store_true", 
                       help="Use AI for idea generation (requires API key)")
    
    args = parser.parse_args()
    
    print(f"🧠 Brainstorming content ideas...")
    print(f"   Topic: {args.topic}")
    print(f"   Type: {args.type}")
    print(f"   Count: {args.count}")
    
    try:
        # Generate ideas
        ideas = generate_ideas(args.topic, args.type, args.count, args.use_ai)
        
        # Print ideas
        print_ideas(ideas, args.format)
        
        # Save if requested
        if args.save:
            output_file = save_ideas(ideas, args.output)
            print(f"\n💾 Ideas saved to: {output_file}")
        
        # Summary
        print(f"\n📊 Summary:")
        print(f"   Total ideas generated: {len(ideas)}")
        
        # Count by difficulty
        difficulties = {}
        for idea in ideas:
            difficulties[idea['difficulty']] = difficulties.get(idea['difficulty'], 0) + 1
        
        for diff, count in difficulties.items():
            print(f"   {diff.title()}: {count}")
        
        print(f"\n🎯 Next steps:")
        print(f"   1. Review and select top ideas")
        print(f"   2. Prioritize based on audience and goals")
        print(f"   3. Create content calendar entries")
        print(f"   4. Start with easiest ideas to build momentum")
        
    except Exception as e:
        print(f"❌ Error generating ideas: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()