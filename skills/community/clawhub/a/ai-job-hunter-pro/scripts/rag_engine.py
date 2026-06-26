#!/usr/bin/env python3
"""
AI Job Hunter Pro — RAG Engine
Handles resume vectorization, JD semantic matching, and feedback-based query optimization.

Architecture:
  Resume PDF/DOCX → parse → chunk → embed → ChromaDB
  Job Description  → parse → embed → cosine similarity against resume vectors
  User feedback    → adjust query vector weights → improve future matches
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES = ["chromadb", "sentence_transformers"]

def check_dependencies():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"[ERROR] Missing packages: {', '.join(missing)}")
        print(f"Run: pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DB_DIR = os.path.expanduser("~/.ai-job-hunter-pro/chroma_db")
PROFILE_PATH = os.path.expanduser("~/job_profile.json")
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # Multilingual, 384-dim, supports Chinese+English
COLLECTION_NAME = "resume_chunks"
JOBS_COLLECTION = "job_descriptions"
FEEDBACK_COLLECTION = "user_feedback"

# ---------------------------------------------------------------------------
# RAG Engine Class
# ---------------------------------------------------------------------------
class RAGEngine:
    """Core RAG engine for resume-JD semantic matching."""

    def __init__(self, db_dir=DB_DIR):
        self.db_dir = db_dir
        os.makedirs(db_dir, exist_ok=True)

        print("[RAG] Loading embedding model...")
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.client = chromadb.PersistentClient(path=db_dir)
        self.resume_collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        self.jobs_collection = self.client.get_or_create_collection(
            name=JOBS_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        self.feedback_collection = self.client.get_or_create_collection(
            name=FEEDBACK_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"[RAG] Engine initialized. Resume chunks: {self.resume_collection.count()}")

    # -----------------------------------------------------------------------
    # Resume Import
    # -----------------------------------------------------------------------
    def import_resume(self, file_path: str) -> dict:
        """Parse and vectorize a resume file (PDF or DOCX)."""
        file_path = os.path.expanduser(file_path)
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            text = self._parse_pdf(file_path)
        elif ext in (".docx", ".doc"):
            text = self._parse_docx(file_path)
        elif ext in (".txt", ".md"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            return {"error": f"Unsupported format: {ext}. Use PDF, DOCX, or TXT."}

        if not text.strip():
            return {"error": "Could not extract text from file."}

        # Chunk the resume into semantic sections
        chunks = self._chunk_resume(text)

        # Clear old resume data
        if self.resume_collection.count() > 0:
            self.resume_collection.delete(where={"type": "resume"})

        # Embed and store
        embeddings = self.model.encode(chunks).tolist()
        ids = [f"resume_{hashlib.md5(c.encode()).hexdigest()[:8]}" for c in chunks]
        metadatas = [{"type": "resume", "section": f"chunk_{i}", "imported_at": datetime.now().isoformat()} for i in range(len(chunks))]

        self.resume_collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        return {
            "status": "success",
            "chunks_imported": len(chunks),
            "file": file_path,
            "sections": [c[:80] + "..." for c in chunks]
        }

    def _parse_pdf(self, path: str) -> str:
        """Extract text from PDF using available tools."""
        try:
            import subprocess
            result = subprocess.run(
                ["pdftotext", "-layout", path, "-"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Fallback: try PyPDF2 or pdfplumber
        try:
            import pdfplumber
            with pdfplumber.open(path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        except ImportError:
            pass

        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            pass

        return ""

    def _parse_docx(self, path: str) -> str:
        """Extract text from DOCX."""
        try:
            import docx
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except ImportError:
            # Fallback: use pandoc if available
            try:
                import subprocess
                result = subprocess.run(
                    ["pandoc", path, "-t", "plain"],
                    capture_output=True, text=True, timeout=30
                )
                return result.stdout
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return ""

    def _chunk_resume(self, text: str) -> list:
        """Split resume into semantic chunks for better retrieval."""
        # Strategy: split by common resume sections, then by paragraph
        section_markers = [
            "教育经历", "education",
            "工作经历", "work experience", "experience",
            "项目经历", "project", "projects",
            "技能", "skills", "技术栈",
            "其他", "other", "awards", "certifications",
            "summary", "objective", "个人简介",
        ]

        lines = text.split("\n")
        chunks = []
        current_chunk = []

        for line in lines:
            line_lower = line.strip().lower()
            # Check if this line is a section header
            is_header = any(marker in line_lower for marker in section_markers)

            if is_header and current_chunk:
                chunk_text = "\n".join(current_chunk).strip()
                if len(chunk_text) > 50:
                    chunks.append(chunk_text)
                current_chunk = [line]
            else:
                current_chunk.append(line)

        # Don't forget last chunk
        if current_chunk:
            chunk_text = "\n".join(current_chunk).strip()
            if len(chunk_text) > 50:
                chunks.append(chunk_text)

        # If chunking produced too few results, fall back to paragraph-based
        if len(chunks) < 3:
            chunks = self._chunk_by_paragraphs(text, max_chunk_size=500)

        return chunks

    def _chunk_by_paragraphs(self, text: str, max_chunk_size: int = 500) -> list:
        """Fallback: chunk by paragraph groups."""
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) > max_chunk_size and current:
                chunks.append(current)
                current = para
            else:
                current = current + "\n\n" + para if current else para
        if current:
            chunks.append(current)
        return chunks

    # -----------------------------------------------------------------------
    # Job Matching
    # -----------------------------------------------------------------------
    def match_jobs(self, jobs: list, min_score: float = 0.75) -> list:
        """
        Score and rank jobs against the resume using RAG.
        Includes JD text cleaning, keyword boosting, and industry relevance.
        """
        if self.resume_collection.count() == 0:
            return {"error": "No resume imported. Run --import-resume first."}

        resume_data = self.resume_collection.get(include=["documents", "embeddings"])
        resume_texts = resume_data["documents"]

        results = []
        for job in jobs:
            # Step 1: Clean JD text (remove LinkedIn/Indeed boilerplate)
            clean_desc = self._clean_jd_text(job.get('description', ''))
            title = job.get('title', '')
            company = job.get('company', '')

            # Step 2: Build weighted query text (title counts more than description)
            # Title is repeated to give it higher weight in embedding
            jd_text = f"{title}. {title}. {company}.\n{clean_desc}"
            jd_embedding = self.model.encode([jd_text])[0]

            # Step 3: RAG similarity query
            query_result = self.resume_collection.query(
                query_embeddings=[jd_embedding.tolist()],
                n_results=min(5, len(resume_texts)),
                include=["documents", "distances"]
            )

            distances = query_result["distances"][0]
            similarities = [1 - d for d in distances]
            avg_score = sum(similarities) / len(similarities) if similarities else 0
            top_score = max(similarities) if similarities else 0

            # Base RAG score: 60% top match + 40% average
            rag_score = 0.6 * top_score + 0.4 * avg_score

            # Step 4: Keyword boost (adds up to +0.15 for relevant tech keywords)
            keyword_boost = self._calculate_keyword_boost(title, clean_desc)

            # Step 5: Industry penalty (reduces score for clearly irrelevant industries)
            industry_penalty = self._calculate_industry_penalty(title, clean_desc, company)

            # Step 6: Combine scores
            match_score = rag_score + keyword_boost - industry_penalty

            # Apply feedback adjustment
            feedback_adj = self._get_feedback_adjustment(jd_embedding)
            match_score = min(1.0, max(0.0, match_score + feedback_adj))
            match_score = round(match_score, 3)

            if match_score >= min_score:
                top_chunks = query_result["documents"][0][:3]
                match_reasons = self._extract_match_reasons(title, clean_desc, top_chunks)

                results.append({
                    **job,
                    "match_score": match_score,
                    "match_reasons": match_reasons,
                    "score_breakdown": {
                        "rag_similarity": round(rag_score, 3),
                        "keyword_boost": round(keyword_boost, 3),
                        "industry_penalty": round(industry_penalty, 3),
                        "feedback_adj": round(feedback_adj, 3),
                    },
                    "top_matching_sections": [c[:100] + "..." for c in top_chunks[:2]]
                })

        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results

    def _clean_jd_text(self, text: str) -> str:
        """Remove LinkedIn/Indeed boilerplate noise from JD text."""
        if not text:
            return ""

        import re

        # Lines to remove (LinkedIn boilerplate)
        noise_patterns = [
            r"Seniority level.*",
            r"Employment type.*",
            r"Job function.*",
            r"Industries.*",
            r"Referrals increase your chances.*",
            r"See who you know.*",
            r"Show more.*",
            r"Show less.*",
            r"provided pay range.*",
            r"Your actual pay will be based.*",
            r"Base pay range.*",
            r"talk with your recruiter.*",
            r"Set alert for similar jobs.*",
            r"Report this job.*",
            r"Apply now.*",
            r"Save this job.*",
            r"以担保或任何理由索要财物.*",
            r"该职位来源于.*",
            r"职位来源于.*",
            r"CN¥[\d,\.]+.*",
            r"Not Applicable",
        ]

        lines = text.split("\n")
        cleaned = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            skip = False
            for pattern in noise_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    skip = True
                    break
            if not skip and len(line) > 2:
                cleaned.append(line)

        return "\n".join(cleaned)

    def _calculate_keyword_boost(self, title: str, description: str) -> float:
        """Boost score for jobs containing high-value keywords matching your profile."""
        text = f"{title} {description}".lower()
        boost = 0.0

        # High-value keywords (directly relevant to AI PM transition)
        high_value = ["ai", "人工智能", "大模型", "llm", "rag", "agent",
                      "prompt", "机器学习", "machine learning", "nlp",
                      "深度学习", "deep learning", "gpt", "claude"]
        for kw in high_value:
            if kw in text:
                boost += 0.03

        # Medium-value keywords (PM + tech skills you have)
        medium_value = ["product manager", "产品经理", "agile", "敏捷",
                        "sql", "python", "数据分析", "data analysis",
                        "data driven", "数据驱动", "app", "移动端",
                        "prd", "用户研究", "a/b test"]
        for kw in medium_value:
            if kw in text:
                boost += 0.015

        return min(0.15, boost)  # Cap at 0.15

    def _calculate_industry_penalty(self, title: str, description: str, company: str) -> float:
        """Penalize clearly irrelevant industries/roles."""
        text = f"{title} {description} {company}".lower()
        penalty = 0.0

        # Irrelevant industries
        irrelevant_industries = [
            "furniture", "家具", "制药", "pharmaceutical", "化工", "chemical",
            "房地产", "real estate", "保险", "insurance", "会计", "accounting",
            "矿业", "mining", "农业", "agriculture", "养殖",
        ]
        for kw in irrelevant_industries:
            if kw in text:
                penalty += 0.08

        # Irrelevant role types
        irrelevant_roles = ["intern", "实习", "trainee", "校招",
                            "销售", "sales rep", "会计", "财务分析"]
        title_lower = title.lower()
        for kw in irrelevant_roles:
            if kw in title_lower:
                penalty += 0.1

        return min(0.2, penalty)  # Cap at 0.2

    def _extract_match_reasons(self, title: str, description: str, resume_chunks: list) -> list:
        """Extract detailed match reasons with bilingual keyword detection."""
        full_text = f"{title} {description}".lower()
        reasons = []

        # Categorized keyword matching
        categories = {
            "AI/ML skills": ["ai", "人工智能", "llm", "大模型", "rag", "agent", "prompt",
                            "machine learning", "机器学习", "nlp", "deep learning"],
            "Product skills": ["product manager", "产品经理", "prd", "agile", "敏捷",
                              "scrum", "roadmap", "用户研究", "user research"],
            "Technical skills": ["python", "sql", "javascript", "api", "data",
                                "数据分析", "数据驱动", "data driven"],
            "Domain match": ["app", "移动端", "小程序", "digital", "数字化",
                           "供应链", "supply chain", "乐园", "旅游", "entertainment"],
        }

        for category, keywords in categories.items():
            matched = [kw for kw in keywords if kw in full_text]
            if matched:
                reasons.append(f"{category}: {', '.join(matched[:4])}")

        return reasons if reasons else ["General alignment"]

    # -----------------------------------------------------------------------
    # Feedback Loop
    # -----------------------------------------------------------------------
    def record_feedback(self, job_id: str, job_description: str, signal: str) -> dict:
        """
        Record user feedback (like/dislike) to adjust future matching.

        This works by storing liked/disliked JD embeddings, then adjusting
        match scores for future queries based on similarity to feedback vectors.
        """
        if signal not in ("like", "dislike"):
            return {"error": "Signal must be 'like' or 'dislike'"}

        jd_embedding = self.model.encode([job_description])[0].tolist()
        self.feedback_collection.add(
            ids=[f"feedback_{job_id}_{signal}"],
            embeddings=[jd_embedding],
            documents=[job_description],
            metadatas=[{
                "job_id": job_id,
                "signal": signal,
                "timestamp": datetime.now().isoformat()
            }]
        )

        return {"status": "recorded", "job_id": job_id, "signal": signal}

    def _get_feedback_adjustment(self, jd_embedding) -> float:
        """Calculate score adjustment based on feedback history."""
        if self.feedback_collection.count() == 0:
            return 0.0

        results = self.feedback_collection.query(
            query_embeddings=[jd_embedding.tolist()],
            n_results=min(10, self.feedback_collection.count()),
            include=["metadatas", "distances"]
        )

        adjustment = 0.0
        for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
            similarity = 1 - dist
            if similarity > 0.7:  # Only strong matches affect adjustment
                if meta["signal"] == "like":
                    adjustment += 0.05 * similarity
                else:
                    adjustment -= 0.05 * similarity

        return round(max(-0.15, min(0.15, adjustment)), 3)

    # -----------------------------------------------------------------------
    # Stats
    # -----------------------------------------------------------------------
    def get_stats(self) -> dict:
        return {
            "resume_chunks": self.resume_collection.count(),
            "jobs_indexed": self.jobs_collection.count(),
            "feedback_entries": self.feedback_collection.count(),
            "db_path": self.db_dir
        }


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter Pro — RAG Engine")
    parser.add_argument("--init", action="store_true", help="Initialize the vector database")
    parser.add_argument("--import-resume", type=str, help="Import resume file (PDF/DOCX/TXT)")
    parser.add_argument("--mode", choices=["search", "feedback", "stats"], help="Operation mode")
    parser.add_argument("--job-data", type=str, help="JSON file with job listings to match")
    parser.add_argument("--job-id", type=str, help="Job ID for feedback")
    parser.add_argument("--signal", choices=["like", "dislike"], help="Feedback signal")
    parser.add_argument("--min-score", type=float, default=0.75, help="Minimum match score")
    parser.add_argument("--platforms", type=str, default="linkedin,boss", help="Platforms to search")

    args = parser.parse_args()

    if args.init:
        os.makedirs(DB_DIR, exist_ok=True)
        print(f"[INIT] Vector database initialized at {DB_DIR}")
        engine = RAGEngine()
        print(f"[INIT] Stats: {json.dumps(engine.get_stats(), indent=2)}")
        return

    engine = RAGEngine()

    if args.import_resume:
        result = engine.import_resume(args.import_resume)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.mode == "stats":
        print(json.dumps(engine.get_stats(), indent=2))
        return

    if args.mode == "feedback":
        if not args.job_id or not args.signal:
            print("[ERROR] --job-id and --signal required for feedback mode")
            sys.exit(1)
        # In practice, the JD text would be loaded from the jobs database
        result = engine.record_feedback(args.job_id, "placeholder JD", args.signal)
        print(json.dumps(result, indent=2))
        return

    if args.mode == "search":
        if args.job_data and os.path.exists(args.job_data):
            with open(args.job_data, "r") as f:
                jobs = json.load(f)
        else:
            # Demo mode: create sample jobs for testing
            jobs = [
                {
                    "id": "demo_1",
                    "title": "AI Product Manager",
                    "company": "TechCorp",
                    "description": "Looking for a PM with experience in AI/ML products, agile development, and data-driven decision making. Experience with LLMs and RAG systems is a plus.",
                    "url": "https://example.com/job/1",
                    "platform": "linkedin"
                },
                {
                    "id": "demo_2",
                    "title": "Senior Product Manager - Platform",
                    "company": "BigTech Inc",
                    "description": "Lead platform product strategy. Experience with mobile apps, API design, and cross-functional team management required. Theme park or entertainment industry experience preferred.",
                    "url": "https://example.com/job/2",
                    "platform": "linkedin"
                }
            ]
            print("[INFO] No --job-data provided. Using demo jobs for testing.")

        results = engine.match_jobs(jobs, min_score=args.min_score)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
