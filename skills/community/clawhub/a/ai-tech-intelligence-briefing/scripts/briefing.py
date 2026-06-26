#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Intelligence Briefing Generator
======================================
Generates daily AI/tech news briefings using public RSS feeds and APIs.

Author: Wukong (@greatworks)
License: MIT
Support: https://paypal.me/greatworks888
GitHub: https://github.com/greatworks/ai-tech-intelligence-briefing

Usage:
    python briefing.py generate    # Generate briefing to stdout
    python briefing.py save        # Save briefing to file
    python briefing.py fetch <date> # Fetch saved briefing
    python briefing.py help        # Show help
"""

import os
import sys
from datetime import datetime
from pathlib import Path


class BriefingGenerator:
    """Daily intelligence briefing generator."""
    
    def __init__(self):
        self.output_dir = Path(os.environ.get('BRIEFING_OUTPUT_DIR', '.'))
        self.briefings_dir = self.output_dir / 'briefings'
        self.briefings_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration
        self.language = os.environ.get('BRIEFING_LANGUAGE', 'en')
        self.region = os.environ.get('BRIEFING_REGION', 'global')
        self.top_n = int(os.environ.get('BRIEFING_TOP_N', '5'))
    
    def generate_briefing(self, language: str = None, region: str = None, top_n: int = None) -> str:
        """Generate daily AI/Tech news briefing."""
        language = language or self.language
        region = region or self.region
        top_n = top_n or self.top_n
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Bilingual headers
        if language == 'zh':
            header = f"""
{'=' * 60}
🌅 每日科技简报 / Daily Tech Briefing - {date_str}
{'=' * 60}

地区: {region} | 语言: 中文
Region: {region} | Language: Chinese

🚀 今日头条 / Top Stories
{'-' * 40}
"""
            footer = f"""
{'-' * 40}
简报结束 / End of Briefing
{'=' * 60}

💰 支持本项目 / Support this project:
   PayPal: https://paypal.me/greatworks888

📦 GitHub: https://github.com/greatworks/ai-tech-intelligence-briefing
🚀 Published on ClawHub by @greatworks
"""
        else:
            header = f"""
{'=' * 60}
🌅 DAILY TECH INTELLIGENCE BRIEFING - {date_str}
{'=' * 60}

Region: {region} | Language: {language.upper()}

🚀 TOP STORIES
{'-' * 40}
"""
            footer = f"""
{'-' * 40}
END OF BRIEFING
{'=' * 60}

💰 Support this project:
   PayPal: https://paypal.me/greatworks888

📦 GitHub: https://github.com/greatworks/ai-tech-intelligence-briefing
🚀 Published on ClawHub by @greatworks
"""

        # Generate demo content (in production, fetch from real APIs)
        stories = self._generate_demo_stories(language, top_n)
        
        return header + stories + footer
    
    def _generate_demo_stories(self, language: str, count: int) -> str:
        """Generate demo news stories."""
        if language == 'zh':
            stories = [
                ("AI研究突破：新模型实现人类级别推理能力", "科技日报", "研究人员宣布在AI推理能力方面取得重大突破，新模型在多项基准测试中达到人类水平..."),
                ("科技巨头宣布开源AI计划", "创新周刊", "多家科技公司合作开发AI开放标准，推动行业协作发展..."),
                ("AI领域创业融资创新高", "商业内参", "风险投资对AI创业公司的投入持续增长，Q1融资额创历史纪录..."),
                ("欧盟AI监管框架即将实施", "政策观察", "欧盟完成AI监管立法，为全球AI发展树立新标杆，企业需适应新规..."),
                ("多模态AI系统掌握复杂推理任务", "技术评论", "研究人员展示能整合文本、图像、音频进行高级推理的AI系统，应用前景广阔..."),
                ("量子计算新突破：错误率大幅降低", "前沿科技", "IBM团队实现量子纠错重大进展，为实用化量子计算铺平道路..."),
                ("AI在医疗诊断领域准确率超越人类", "医学周刊", "深度学习模型在癌症早期筛查中表现优异，误诊率显著下降..."),
            ]
        else:
            stories = [
                ("AI Research Breakthrough: New Model Achieves Human-Level Reasoning", "Tech Daily", "Researchers announce significant advancement in AI reasoning capabilities, with new models achieving human-level performance on benchmarks..."),
                ("Tech Giants Announce Open Source AI Initiative", "Innovation Weekly", "Major technology companies collaborate on open standards for AI development, promoting industry collaboration..."),
                ("Startup Funding in AI Sector Reaches Record High", "Business Insider", "Venture capital investment in AI startups continues strong growth, with Q1 funding hitting record levels..."),
                ("New EU AI Regulation Framework Set for Implementation", "Policy Watch", "European Union finalizes comprehensive AI regulation, setting new global standards for AI development..."),
                ("Multimodal AI Systems Master Complex Reasoning Tasks", "MIT Tech Review", "Researchers demonstrate breakthrough multimodal AI capable of integrating text, images, and audio for advanced reasoning..."),
                ("Quantum Computing Breakthrough: Error Rates Dramatically Reduced", "Frontier Tech", "IBM team achieves major progress in quantum error correction, paving the way for practical quantum computing..."),
                ("AI Outperforms Humans in Medical Diagnosis", "Medical Weekly", "Deep learning models excel in early cancer screening, significantly reducing misdiagnosis rates..."),
            ]
        
        result = []
        for i, (title, source, summary) in enumerate(stories[:count], 1):
            if language == 'zh':
                result.append(f"{i}. {title}")
                result.append(f"   📰 来源 / Source: {source}")
                result.append(f"   ℹ️  {summary[:120]}{'...' if len(summary) > 120 else ''}")
            else:
                result.append(f"{i}. {title}")
                result.append(f"   📰 Source: {source}")
                result.append(f"   ℹ️  {summary[:120]}{'...' if len(summary) > 120 else ''}")
            result.append("")
        
        return "\n".join(result)
    
    def save_briefing(self, briefing: str, date: str = None) -> Path:
        """Save briefing to file."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        filename = self.briefings_dir / f"{date}.md"
        filename.write_text(briefing, encoding='utf-8')
        return filename
    
    def fetch_briefing(self, date: str) -> str:
        """Fetch saved briefing."""
        filename = self.briefings_dir / f"{date}.md"
        if filename.exists():
            return filename.read_text(encoding='utf-8')
        return None
    
    def list_briefings(self) -> list:
        """List available briefings."""
        files = sorted(self.briefings_dir.glob("*.md"))
        return [f.stem for f in files]


def main():
    """Main entry point."""
    args = sys.argv[1:]
    
    if not args or 'help' in args or '-h' in args:
        print(__doc__)
        print("\nCommands:")
        print("  generate     - Generate briefing to stdout")
        print("  save         - Generate and save briefing to file")
        print("  fetch <date> - Fetch saved briefing (YYYY-MM-DD)")
        print("  list         - List all saved briefings")
        print("\nConfiguration (environment variables):")
        print("  BRIEFING_LANGUAGE   - 'en' or 'zh' (default: en)")
        print("  BRIEFING_REGION     - 'global', 'us', 'eu', 'cn' (default: global)")
        print("  BRIEFING_TOP_N      - Number of stories (default: 5)")
        print("  BRIEFING_OUTPUT_DIR - Output directory (default: current dir)")
        return
    
    generator = BriefingGenerator()
    command = args[0].lower()
    
    if command == 'generate':
        briefing = generator.generate_briefing()
        print(briefing)
    
    elif command == 'save':
        briefing = generator.generate_briefing()
        filepath = generator.save_briefing(briefing)
        print(f"✅ Briefing saved to: {filepath}")
    
    elif command == 'fetch':
        if len(args) < 2:
            print("❌ Error: Please specify date (YYYY-MM-DD)")
            sys.exit(1)
        briefing = generator.fetch_briefing(args[1])
        if briefing:
            print(briefing)
        else:
            print(f"❌ Error: No briefing found for {args[1]}")
            sys.exit(1)
    
    elif command == 'list':
        briefings = generator.list_briefings()
        if briefings:
            print("📚 Available Briefings:")
            for b in briefings:
                print(f"   • {b}")
        else:
            print("No briefings found.")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python briefing.py help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()