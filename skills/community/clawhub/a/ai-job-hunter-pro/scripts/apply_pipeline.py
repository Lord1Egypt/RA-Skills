#!/usr/bin/env python3
"""
AI Job Hunter Pro — Application Pipeline
Handles cover letter generation, ATS optimization, and application submission tracking.

Flow:
  Job selected → Generate cover letter → Optimize resume for ATS → Dry run preview → Submit
"""

import argparse
import json
import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DB_PATH = os.path.expanduser("~/.ai-job-hunter-pro/applications.db")
PROFILE_PATH = os.path.expanduser("~/job_profile.json")

# ---------------------------------------------------------------------------
# Database Setup
# ---------------------------------------------------------------------------
def init_db(db_path=DB_PATH):
    """Initialize the SQLite tracking database."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            job_title TEXT,
            company TEXT,
            platform TEXT,
            url TEXT,
            match_score REAL,
            status TEXT DEFAULT 'discovered',
            cover_letter TEXT,
            ats_keywords TEXT,
            applied_at TEXT,
            updated_at TEXT,
            notes TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id TEXT NOT NULL,
            old_status TEXT,
            new_status TEXT,
            changed_at TEXT,
            FOREIGN KEY (application_id) REFERENCES applications(id)
        )
    """)
    conn.commit()
    return conn

# ---------------------------------------------------------------------------
# Cover Letter Generator
# ---------------------------------------------------------------------------
class CoverLetterGenerator:
    """Generate tailored cover letters based on resume + JD matching."""

    # Bilingual keyword bank for matching JD requirements to profile highlights
    HIGHLIGHT_MAP = {
        "ai": "Built AI-native applications from scratch, including an AI Job Hunter with RAG-based semantic matching and an AI travel planner using Gemini Pro.",
        "llm": "Hands-on experience with LLM integration (Claude, Gemini), prompt engineering, and building RAG pipelines with ChromaDB for production use.",
        "rag": "Designed and implemented a RAG system using ChromaDB vector database for semantic resume-JD matching, achieving accurate cross-lingual retrieval.",
        "agent": "Built an autonomous AI Agent on the OpenClaw framework capable of multi-platform job search, automated application, and feedback-driven optimization.",
        "product": "Served as Product Owner at Shanghai Disney Resort, leading 8 app releases with 27 features shipped, impacting 400M+ users through digital campaigns.",
        "agile": "Established agile sprint processes at Disney, increasing release frequency from bi-monthly to monthly and cutting delivery cycles by 50%.",
        "sql": "Built 6 operational dashboards using SQL at Disney and 4 business dashboards at Amazon, driving data-informed testing and operations.",
        "python": "Developed 3 Python automation tools at Amazon processing 800M+ data records, improving single-project configuration efficiency by 90%.",
        "data": "MSc in Data Science from UCL (QS #9, GPA 3.9/4.0), with coursework in statistics, machine learning, and data visualization.",
        "mobile": "Led mobile app product development at Disney, managing the official app across 8 release cycles with high-concurrency stability.",
        "supply": "Managed supply chain logistics network buildout at Amazon across 6 countries, handling 400+ requirements and enabling millions of additional orders annually.",
        "scrum": "Led a 9-person cross-functional team (5 dev + 4 QA) using Scrum methodology, delivering 127 product requirements in 5 months.",
        "数据分析": "使用SQL搭建6个APP运营数据看板（迪士尼）和4个业务数据看板（亚马逊），用数据驱动测试计划和业务决策。",
        "产品经理": "担任上海迪士尼乐园产品Owner，主导8次APP发版、上线27个核心需求，带领9人团队实施敏捷开发。",
        "敏捷": "建立APP敏捷迭代发版流程，将发版频率从每2个月提升至每月，产品交付周期缩短50%。",
        "大模型": "独立开发AI Native应用，集成Claude/Gemini等大模型API，具备Prompt Engineering和RAG系统设计经验。",
        "小程序": "负责迪士尼微信小程序8次MKT Campaign的产品研发与上线，累计触达400万+用户。",
        "供应链": "在亚马逊管理6个国家的供应链物流网络配置，累计处理400+业务需求，中东配送效率提高15%。",
        "自动化": "基于Python研发3个自动化工具，批量处理8亿条数据，单一配置项目效率提升90%。",
        "项目管理": "管理亚马逊新国家、新库房、新配送中心的供应链网络搭建，以及2个供应商从0到1的系统接入。",
    }

    def __init__(self, profile: dict):
        self.profile = profile
        self.name = profile.get("full_name", "Candidate")
        self.notes = profile.get("cover_letter_notes", "")

    def generate(self, job: dict, match_reasons: list = None) -> str:
        """Generate a tailored cover letter based on JD keyword matching."""
        title = job.get("title", "the position")
        company = job.get("company", "your company")
        description = job.get("description", "")
        is_chinese = self._is_chinese(description)

        # Find which highlights match this JD
        matched_highlights = self._match_highlights(description)

        if is_chinese:
            return self._generate_chinese(title, company, matched_highlights)
        else:
            return self._generate_english(title, company, matched_highlights)

    def _is_chinese(self, text: str) -> bool:
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        return chinese_chars > len(text) * 0.1

    def _match_highlights(self, description: str) -> list:
        """Match JD keywords against highlight bank, return top relevant highlights."""
        desc_lower = description.lower()
        scored = []
        for keyword, highlight in self.HIGHLIGHT_MAP.items():
            if keyword.lower() in desc_lower:
                scored.append((keyword, highlight))
        # Deduplicate: prefer longer keyword matches, limit to 3
        seen_highlights = set()
        unique = []
        for kw, hl in scored:
            if hl not in seen_highlights:
                seen_highlights.add(hl)
                unique.append((kw, hl))
        return unique[:3]

    def _generate_chinese(self, title, company, highlights) -> str:
        name = self.name
        years = self.profile.get("years_experience", 3)

        hl_text = ""
        if highlights:
            points = "\n".join(f"  - {hl}" for _, hl in highlights)
            hl_text = f"\n我的经历与贵司需求高度契合：\n{points}\n"
        else:
            hl_text = "\n我具备扎实的产品管理经验和技术理解力，能够快速上手并推动产品落地。\n"

        return f"""尊敬的招聘负责人：

您好！我对贵司{company}的{title}岗位非常感兴趣。我拥有{years}年产品经理经验，先后在上海迪士尼乐园（软件产品经理）和亚马逊（项目经理）负责数字化产品与供应链系统，同时持有伦敦大学学院（UCL）数据科学硕士学位。
{hl_text}
目前，我正在从传统产品管理转向AI产品方向，已独立开发了基于RAG技术的AI求职助手和AI游园规划应用，具备从0到1的AI产品设计与落地能力。

期待有机会进一步交流，谢谢！

{name}"""

    def _generate_english(self, title, company, highlights) -> str:
        name = self.name
        years = self.profile.get("years_experience", 3)

        hl_text = ""
        if highlights:
            points = "\n".join(f"  - {hl}" for _, hl in highlights)
            hl_text = f"\nMy experience directly aligns with your requirements:\n{points}\n"
        else:
            hl_text = "\nI bring a strong combination of product execution and technical depth that positions me well for this role.\n"

        return f"""Dear Hiring Manager,

I am writing to express my interest in the {title} position at {company}. With {years} years of product management experience at Shanghai Disney Resort and Amazon, combined with an MSc in Data Science from UCL (QS #9), I bring a unique blend of product rigor and technical depth.
{hl_text}
I am currently transitioning into AI product management, having independently built an AI-powered job search assistant featuring RAG-based semantic matching (ChromaDB) and an AI travel planner using Gemini Pro — demonstrating my ability to ship AI-native products from concept to launch.

I would welcome the opportunity to discuss how my experience can contribute to {company}'s goals.

Best regards,
{name}"""


# ---------------------------------------------------------------------------
# ATS Optimizer
# ---------------------------------------------------------------------------
class ATSOptimizer:
    """Optimize resume highlights and keywords for ATS systems."""

    # Comprehensive bilingual keyword dictionary for PM/tech roles
    ATS_KEYWORDS = {
        # Technical skills
        "python", "sql", "javascript", "js", "react", "node", "java", "go",
        "html", "css", "api", "rest", "graphql", "docker", "kubernetes", "k8s",
        "aws", "gcp", "azure", "git", "ci/cd", "linux",
        # AI/ML specific
        "ai", "ml", "llm", "rag", "nlp", "gpt", "bert", "transformer",
        "prompt engineering", "fine-tuning", "embedding", "vector",
        "machine learning", "deep learning", "neural network",
        "chromadb", "langchain", "openai", "claude", "gemini",
        # Product/Business
        "agile", "scrum", "kanban", "jira", "confluence",
        "product management", "product strategy", "roadmap", "prd",
        "a/b testing", "okr", "kpi", "roi", "mvp",
        "user research", "ux", "figma", "prototype",
        # Data
        "data analysis", "data visualization", "tableau", "quicksight",
        "excel", "pandas", "numpy", "statistics",
        # Chinese equivalents
        "产品经理", "产品管理", "产品规划", "产品设计", "产品迭代",
        "敏捷开发", "敏捷", "项目管理", "需求分析", "需求管理",
        "数据分析", "数据驱动", "数据看板", "数据可视化",
        "用户研究", "用户体验", "用户增长", "用户画像",
        "人工智能", "机器学习", "深度学习", "大模型", "自然语言处理",
        "供应链", "物流", "仓储", "配送",
        "小程序", "微信", "app", "移动端",
        "跨团队", "跨部门", "团队管理", "技术栈",
        "自动化", "系统设计", "架构", "接口",
        "运营", "营销", "转化率", "留存",
    }

    def optimize(self, profile_text: str, jd_text: str) -> dict:
        """
        Analyze JD keywords and suggest resume optimizations.
        Supports both Chinese and English JDs.
        """
        jd_lower = jd_text.lower()
        profile_lower = profile_text.lower()

        # Find which ATS keywords appear in the JD
        jd_keywords = set()
        for kw in self.ATS_KEYWORDS:
            if kw.lower() in jd_lower:
                jd_keywords.add(kw)

        # Find which of those are also in the profile
        matched = set()
        missing = set()
        for kw in jd_keywords:
            if kw.lower() in profile_lower:
                matched.add(kw)
            else:
                missing.add(kw)

        ats_score = len(matched) / max(len(jd_keywords), 1) * 100

        # Generate actionable suggestions
        suggestions = []
        for kw in sorted(missing):
            suggestions.append(f"Add '{kw}' — mentioned in JD but not in your profile")

        return {
            "ats_score": round(ats_score, 1),
            "matched_keywords": sorted(matched),
            "missing_keywords": sorted(missing),
            "suggestions": suggestions[:8],
            "total_jd_keywords": len(jd_keywords),
            "total_matched": len(matched)
        }


# ---------------------------------------------------------------------------
# Application Pipeline
# ---------------------------------------------------------------------------
class ApplicationPipeline:
    """Main pipeline: match → generate → optimize → apply → track."""

    def __init__(self, profile_path=PROFILE_PATH):
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                self.profile = json.load(f)
        else:
            self.profile = {"full_name": "User", "skills": [], "years_experience": 3}
            print(f"[WARN] Profile not found at {profile_path}. Using defaults.")

        self.conn = init_db()
        self.cover_gen = CoverLetterGenerator(self.profile)
        self.ats_opt = ATSOptimizer()

    def process_job(self, job: dict, mode: str = "dry-run",
                    generate_cover_letter: bool = True,
                    optimize_ats: bool = True) -> dict:
        """
        Process a single job through the pipeline.

        Modes:
            dry-run: Generate materials, show preview, don't submit
            submit: Actually submit the application
        """
        job_id = job.get("id", "unknown")
        result = {
            "job_id": job_id,
            "job_title": job.get("title"),
            "company": job.get("company"),
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        }

        # Step 1: Generate cover letter
        if generate_cover_letter:
            cover_letter = self.cover_gen.generate(
                job,
                match_reasons=job.get("match_reasons", [])
            )
            result["cover_letter"] = cover_letter

        # Step 2: ATS optimization
        if optimize_ats:
            ats_result = self.ats_opt.optimize(
                json.dumps(self.profile),
                job.get("description", "")
            )
            result["ats_analysis"] = ats_result

        # Step 3: Record in database
        self._record_application(job, result, mode)

        if mode == "dry-run":
            result["action"] = "PREVIEW ONLY — not submitted. Run with --mode submit to apply."
        else:
            result["action"] = "Application submitted (simulated)."
            self._update_status(job_id, "discovered", "applied")

        return result

    def _record_application(self, job: dict, result: dict, mode: str):
        """Record application in SQLite."""
        job_id = job.get("id", "unknown")
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO applications
                (id, job_id, job_title, company, platform, url, match_score,
                 status, cover_letter, ats_keywords, applied_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"app_{job_id}",
                job_id,
                job.get("title"),
                job.get("company"),
                job.get("platform"),
                job.get("url"),
                job.get("match_score", 0),
                "applied" if mode == "submit" else "discovered",
                result.get("cover_letter", ""),
                json.dumps(result.get("ats_analysis", {}).get("matched_keywords", [])),
                datetime.now().isoformat() if mode == "submit" else None,
                datetime.now().isoformat()
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")

    def _update_status(self, job_id: str, old_status: str, new_status: str):
        """Update application status with history tracking."""
        self.conn.execute("""
            UPDATE applications SET status = ?, updated_at = ? WHERE job_id = ?
        """, (new_status, datetime.now().isoformat(), job_id))

        self.conn.execute("""
            INSERT INTO status_history (application_id, old_status, new_status, changed_at)
            VALUES (?, ?, ?, ?)
        """, (f"app_{job_id}", old_status, new_status, datetime.now().isoformat()))

        self.conn.commit()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter Pro — Application Pipeline")
    parser.add_argument("--job-id", type=str, help="Job ID to process")
    parser.add_argument("--job-data", type=str, help="JSON file with job data")
    parser.add_argument("--mode", choices=["dry-run", "submit"], default="dry-run")
    parser.add_argument("--generate-cover-letter", action="store_true", default=True)
    parser.add_argument("--optimize-ats", action="store_true", default=True)
    parser.add_argument("--profile", type=str, default=PROFILE_PATH)

    args = parser.parse_args()
    pipeline = ApplicationPipeline(profile_path=args.profile)

    if args.job_data and os.path.exists(args.job_data):
        with open(args.job_data, "r") as f:
            jobs = json.load(f)
        if isinstance(jobs, dict):
            jobs = [jobs]
    else:
        # Demo job for testing
        jobs = [{
            "id": "demo_1",
            "title": "AI Product Manager",
            "company": "TechCorp",
            "description": "We need a PM with AI/ML experience, agile methodology, product strategy, and data-driven approach.",
            "url": "https://example.com/job/1",
            "platform": "linkedin",
            "match_score": 0.85,
            "match_reasons": ["Matching skills: product, agile, data, ai"]
        }]
        print("[INFO] No --job-data provided. Using demo job for testing.")

    for job in jobs:
        if args.job_id and job.get("id") != args.job_id:
            continue
        result = pipeline.process_job(
            job,
            mode=args.mode,
            generate_cover_letter=args.generate_cover_letter,
            optimize_ats=args.optimize_ats
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("---")


if __name__ == "__main__":
    main()
