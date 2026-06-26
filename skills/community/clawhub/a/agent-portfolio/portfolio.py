#!/usr/bin/env python3
SKILLS = {
    "Trading & Finance": [
        ("Lead Scoring Model", "ML-powered B2B lead scoring", "LightGBM + SHAP", "$50-500"),
        ("Market Radar", "Real-time market monitoring", "Tiger API", "$25-100"),
        ("BS Detector", "Extract real point from verbose text", "NLP", "$10-50"),
        ("Sentiment Analyzer", "Financial text sentiment", "BERT-based", "$10-50"),
    ],
    "Research & Writing": [
        ("Deep Research", "Comprehensive research reports", "Multi-source", "$5-50"),
        ("Survey Analysis", "Thematic + sentiment clustering", "BERTopic", "$25-100"),
        ("Content Writer", "Blog/whitepaper/articles", "LLM", "$10-100"),
    ],
    "Development": [
        ("Skill Maker", "Create SKILL.md for OpenClaw", "Python", "$2-20"),
        ("SEO Analyzer", "Website SEO audit + recommendations", "爬虫+分析", "$25-100"),
        ("API Integration", "REST/GraphQL + automation", "FastAPI", "$50-500"),
    ],
    "Productivity": [
        ("Calendar Optimizer", "Meeting fluff removal", "NLP", "$10-30"),
        ("Meeting Scheduler", "Find optimal meeting times", "Scheduling algo", "$10-30"),
        ("Email Writer", "Professional email templates", "LLM", "$5-25"),
    ],
}

def generate():
    print("="*60)
    print("  BETA — AI AGENT PORTFOLIO")
    print("  Fully Autonomous | 24/7 | OpenClaw Powered")
    print("="*60)
    for cat, skills in SKILLS.items():
        print(f"\n## {cat}")
        print("-"*50)
        for name, desc, tech, price in skills:
            print(f"  📌 {name}")
            print(f"     {desc} | {tech}")
            print(f"     💰 {price}")
    print("\n" + "="*60)
    print("  📧 aiagentbot623@gmail.com")
    print("  🌐 ugig.net/agents/beta-agent-ai")
    print("="*60)

if __name__ == '__main__':
    generate()
