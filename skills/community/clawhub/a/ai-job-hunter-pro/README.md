# 🎯 AI Job Hunter Pro

> An intelligent job search assistant powered by OpenClaw + Claude, featuring RAG-based resume-JD semantic matching, automated application pipeline, and data-driven tracking.

## Why This Exists

Job searching is broken. You spend 2-3 hours daily on repetitive tasks: browsing listings, tailoring resumes, writing cover letters, tracking applications. **AI Job Hunter Pro reduces this to <10 minutes of human review per day.**

Unlike simple keyword matchers, this skill uses **RAG (Retrieval-Augmented Generation)** to deeply understand your resume and semantically match it against job descriptions — catching opportunities that keyword filters miss.

## Features

| Feature | Description |
|---------|-------------|
| 🧠 **RAG Matching** | ChromaDB-powered semantic matching between your resume and JDs |
| 📝 **Smart Cover Letters** | AI-generated, tailored to each specific position |
| 🔑 **ATS Optimization** | Keyword analysis to beat Applicant Tracking Systems |
| 📊 **Funnel Analytics** | Track: Discovered → Applied → Interview → Offer |
| 🔄 **Feedback Loop** | Like/dislike jobs to continuously improve recommendations |
| 🌐 **Multi-Platform** | LinkedIn, Boss直聘, Indeed, Glassdoor |
| 🔒 **Privacy-First** | All data stored locally, your resume never leaves your machine |

## Quick Start

### 1. Install

```bash
# Add to your OpenClaw skills
npx playbooks add skill ai-job-hunter-pro

# Or manually
cd ~/.openclaw/workspace/skills
git clone https://github.com/YourUsername/ai-job-hunter-pro.git
```

### 2. Setup

```bash
cd ai-job-hunter-pro
pip install -r scripts/requirements.txt
python3 scripts/setup_rag.py --init
```

### 3. Import Your Resume

```bash
python3 scripts/rag_engine.py --import-resume ~/path/to/resume.pdf
```

### 4. Edit Your Profile

```bash
cp assets/profile_template.json ~/job_profile.json
# Edit with your preferences: target roles, locations, salary, platforms
```

### 5. Start Hunting

Talk to your OpenClaw agent:

```
"Find AI product manager jobs matching my resume"
"Auto-apply to the top 5 matches in dry-run mode"
"Show me my application funnel report"
"I liked the ByteDance role, disliked the banking one"
```

## Architecture

```
┌─────────────┐  ┌──────────────┐  ┌──────────────────┐
│Resume Parser │  │  RAG Engine   │  │ User Preferences │
│ PDF/DOCX     │  │ChromaDB+Embed │  │ Location/Salary  │
└──────┬───────┘  └──────┬────────┘  └────────┬─────────┘
       │                 │                     │
       └─────────────────┼─────────────────────┘
                         ▼
        ┌─────────────────────────────────┐
        │    OpenClaw AI Agent Core       │
        │  ┌──────────┐ ┌─────────────┐  │
        │  │Job Match  │ │Cover Letter │  │
        │  │  Engine   │ │  Generator  │  │
        │  └──────────┘ └─────────────┘  │
        │  ┌──────────────────────────┐  │
        │  │    ATS Optimizer         │  │
        │  └──────────────────────────┘  │
        └─────────────┬───────────────────┘
                      ▼
  ┌──────┐  ┌──────┐  ┌──────────┐  ┌──────────┐
  │Linked│  │Indeed│  │Glassdoor │  │Boss直聘  │
  │  In  │  │      │  │          │  │          │
  └──────┘  └──────┘  └──────────┘  └──────────┘
                      ▼
  ┌─────────────────────────────────────────────┐
  │  SQLite Tracker + Funnel Analytics          │
  │  Discovered → Applied → Interview → Offer   │
  └─────────────────────────────────────────────┘
```

## File Structure

```
ai-job-hunter-pro/
├── SKILL.md                    # OpenClaw skill definition
├── README.md                   # This file
├── scripts/
│   ├── requirements.txt        # Python dependencies
│   ├── setup_rag.py           # One-time setup script
│   ├── rag_engine.py          # Core RAG matching engine
│   ├── apply_pipeline.py      # Cover letter + ATS + submission
│   └── tracker.py             # Application status tracking
├── assets/
│   └── profile_template.json  # User profile template
└── references/
    └── platform_notes.md      # Platform-specific integration notes
```

## Configuration

Edit `~/job_profile.json` to customize:

- **target_roles**: Job titles to search for
- **target_locations**: Preferred cities
- **salary_range**: Min/max salary expectations
- **platforms**: Which job sites to search (enable/disable each)
- **preferences**: Daily limits, confirmation mode, match threshold

## How RAG Matching Works

1. **Resume Vectorization**: Your resume is parsed into semantic chunks (work experience, skills, education) and embedded into vectors using `all-MiniLM-L6-v2`
2. **JD Embedding**: Each job description is similarly embedded
3. **Cosine Similarity**: We calculate multi-dimensional similarity between your resume chunks and each JD
4. **Weighted Scoring**: 60% top chunk match + 40% average match = final score
5. **Feedback Adjustment**: Your like/dislike signals adjust future query vectors by ±5-15%

## Contributing

PRs welcome! Areas where help is needed:

- [ ] Additional platform integrations (拉勾, 猎聘, etc.)
- [ ] Improved Chinese resume parsing
- [ ] Interview scheduling integration
- [ ] Browser automation for form filling
- [ ] Multi-language cover letter support

## License

MIT

## Author

Built by [Your Name] — transitioning from Disney Product Manager to AI PM, one automated application at a time. 🎯
