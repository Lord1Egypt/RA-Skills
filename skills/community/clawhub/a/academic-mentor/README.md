# Academic Mentor - AI-Powered Research Advisor

> Your AI research advisor for graduate studies and academic research - from project assessment to publication

**Version:** 0.1.0 | **Status:** Production Ready | **License:** MIT

---

## What is Academic Mentor?

Academic Mentor is an AI-powered research advisory system designed to help **graduate students and researchers** navigate their academic journey. It provides comprehensive guidance, professional documentation, and intelligent resource recommendations powered by advanced analysis.

### Core Capabilities

- **Research Assessment** - Evaluate research ideas across 5 dimensions (innovation, feasibility, impact, methodology, background)
- **Proposal Generation** - Generate research proposals, thesis proposals, and grant applications
- **Literature Analysis** - Analyze papers, identify trends, generate literature reviews
- **Advisor Matching** - Intelligent matching with faculty advisors and research labs
- **Paper Writing** - Generate paper outlines with section-by-section guidance
- **Resource Recommendations** - Recommend conferences, journals, funding, datasets

---

## Quick Start

### Installation

```bash
# Install dependencies
pip install -e .

# Install system dependencies for PDF processing (optional)
# macOS
brew install tesseract ghostscript poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils ghostscript
```

### Basic Usage

```python
import asyncio
from academic_mentor import AcademicMentor
from academic_mentor.types import ResearchProject, StudentBackground

async def main():
    # Initialize mentor
    mentor = AcademicMentor()

    # Define your research project
    project = ResearchProject(
        title="Neural Network Interpretability",
        field="Computer Science",
        subfield="Machine Learning",
        research_question="How can we make deep learning more interpretable?",
        background="Deep learning lacks interpretability...",
        objectives=[
            "Develop new interpretability methods",
            "Evaluate on real tasks",
        ],
        methodology="Theoretical analysis + empirical experiments",
        expected_methods=["Attribution methods", "Visualization"],
        student=StudentBackground(
            education_level="phd",
            field="Computer Science",
            year=2,
            skills=["Python", "PyTorch"],
        )
    )

    # Assess research quality
    assessment = await mentor.assess_research(project)
    print(f"Overall Score: {assessment.overall_score}/100")
    print(f"Readiness: {assessment.readiness_level}")

    # Generate research proposal
    proposal = await mentor.generate_proposal(project)
    print(f"Generated {len(proposal.sections)} sections")

    # Match with advisors
    matches = await mentor.match_advisors(project, top_n=10)
    print(f"Found {len(matches)} matching advisors")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Features in Detail

### 1. Research Assessment

Evaluate research ideas across 5 dimensions:

- **Innovation** (25%): Novelty and originality
- **Feasibility** (20%): Realistic with available resources
- **Impact** (20%): Potential significance
- **Methodology** (20%): Soundness of approach
- **Background** (15%): Student preparation

**Output:**
- Overall score (0-100)
- Readiness level (not-ready/needs-development/ready/highly-ready)
- Detailed dimension breakdowns
- Strengths, weaknesses, and recommendations

```python
assessment = await mentor.assess_research(project)
```

### 2. Research Proposal Generation

Generate professional research proposals:

**Types:**
- `research-proposal` - General research proposal
- `thesis-proposal` - Thesis/dissertation proposal
- `grant-application` - Grant application document

**Sections include:**
- Abstract, Introduction, Background
- Research Questions & Objectives
- Methodology, Expected Outcomes
- Timeline, Resources, References

```python
proposal = await mentor.generate_proposal(project, "research-proposal")
print(proposal.markdown_content)
```

### 3. Literature Analysis

Analyze academic literature on your topic:

**Features:**
- Search and analyze papers (integrates with academic databases)
- Identify research trends and gaps
- Extract common methodologies
- Generate literature review text
- Citation network analysis

```python
literature = await mentor.analyze_literature(
    query="machine learning interpretability",
    max_papers=20
)
print(literature.literature_review)
```

### 4. Advisor/Lab Matching

Find suitable advisors and research groups:

**Matching considers:**
- Research area alignment
- Methodology fit
- Resource availability
- Student background fit
- Advisor availability and style

**Output:**
- Ranked list of matches with scores
- Match reasoning and strengths
- Application difficulty assessment
- Recommended contact approach

```python
matches = await mentor.match_advisors(project, top_n=10)
for match in matches[:5]:
    print(f"{match.advisor.name}: {match.match_score}/100")
```

### 5. Paper Writing Assistance

Generate structured paper outlines:

**Paper types:**
- `conference` - Conference paper (8-10 pages)
- `journal` - Journal article (20-30 pages)
- `thesis-chapter` - Thesis chapter (30-50 pages)

**Each section includes:**
- Key points to cover
- Suggested length
- Writing tips

```python
outline = await mentor.generate_paper_outline(project, "conference")
```

### 6. Resource Recommendations

Comprehensive academic resources:

- **Conferences** - Relevant conferences with deadlines
- **Journals** - Suitable journals by impact factor
- **Funding** - Fellowship and grant opportunities
- **Datasets** - Relevant open datasets
- **Courses** - Learning resources

```python
resources = await mentor.recommend_resources(project)
print(f"Conferences: {len(resources.recommended_conferences)}")
print(f"Journals: {len(resources.recommended_journals)}")
```

### 7. PDF Processing

Parse academic papers from PDF:

```python
# Parse paper from PDF
paper = await mentor.parse_paper_pdf("paper.pdf")

# Generate BibTeX citations
bibtex = await mentor.generate_bibtex(papers)
```

---

## Project Structure

```
academic_mentor/
├── mentor.py              # Main AcademicMentor class
├── types/                 # Data models
│   ├── research.py        # Research project models
│   ├── advisor.py         # Advisor models
│   └── models.py          # Result models
├── modules/               # Core modules
│   ├── assessment/        # Research assessor
│   ├── proposal/          # Proposal generator
│   ├── literature/        # Literature analyzer
│   ├── matching/          # Advisor matcher
│   ├── writing/           # Writing assistant
│   └── recommendation/    # Resource recommender
├── pdf/                   # PDF processing
└── data/                  # Databases
    ├── advisors/          # Advisor database
    ├── conferences/       # Conference data
    └── journals/          # Journal data
```

---

## Use Cases

### For Graduate Students

**Starting PhD research:**
```python
# Get complete research package
assessment = await mentor.assess_research(project)
proposal = await mentor.generate_proposal(project)
advisors = await mentor.match_advisors(project)
resources = await mentor.recommend_resources(project)
```

**Preparing paper submission:**
```python
outline = await mentor.generate_paper_outline(project, "conference")
literature = await mentor.analyze_literature(project.research_question)
```

### For Researchers

**Exploring new research direction:**
```python
# Quick assessment
assessment = await mentor.assess_research(new_idea)
print(f"Innovation: {assessment.innovation_score}/100")
print("Recommendations:", assessment.recommendations)
```

**Finding collaborators:**
```python
matches = await mentor.match_advisors(project, top_n=20)
# Filter by location, availability, etc.
```

---

## Configuration

### Custom Assessment Weights

```python
mentor = AcademicMentor(
    assessment_weights={
        "innovation": 0.30,
        "feasibility": 0.20,
        "impact": 0.25,
        "methodology": 0.15,
        "background": 0.10
    }
)
```

### Custom Data Directory

```python
mentor = AcademicMentor(data_dir="/path/to/custom/data")
```

### Adding Advisors/Resources

Edit JSON files in `academic_mentor/data/`:
- `advisors/advisors.json`
- `conferences/conferences.json`
- `journals/journals.json`

---

## Testing

```bash
# Run complete test suite
python3 test_complete.py

# Run example
python3 example.py
```

**Expected output:**
```
✅ Test 1/6: Research Assessment - PASSED
✅ Test 2/6: Proposal Generation - PASSED
✅ Test 3/6: Literature Analysis - PASSED
✅ Test 4/6: Advisor Matching - PASSED
✅ Test 5/6: Paper Outline - PASSED
✅ Test 6/6: Resource Recommendations - PASSED
🎊 All tests passed!
```

---

## Python Advantages

| Feature | Python | TypeScript |
|---------|--------|------------|
| PDF Parsing | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| OCR | ⭐⭐⭐⭐⭐ | ❌ |
| Data Analysis | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Academic APIs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ML Integration | ⭐⭐⭐⭐⭐ | ⭐ |

For academic research with heavy PDF and data processing, **Python is the optimal choice**.

---

## Limitations & Disclaimers

### What Academic Mentor Can Do
✅ Provide structured guidance and templates
✅ Analyze research ideas objectively
✅ Match with advisors based on criteria
✅ Generate professional documentation

### What It Cannot Do
❌ Replace human mentorship and judgment
❌ Guarantee research success or funding
❌ Access real-time paper databases (requires API setup)
❌ Make research decisions for you

**Important:** Use as a tool to augment, not replace, human advisory.

---

## Roadmap

### Version 0.2.0 (Q2 2026)
- Integration with Semantic Scholar API
- Enhanced literature analysis with citation graphs
- Multi-language support
- LaTeX template generation

### Version 0.3.0 (Q3 2026)
- Integration with arXiv, PubMed
- Automatic paper submission checklist
- Research group collaboration features
- Mobile app

---

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas where we need help:**
- Advisor database expansion
- Conference/journal data updates
- Integration with academic APIs
- Test coverage
- Documentation improvements

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Acknowledgments

- OpenClaw community for the skill framework
- Open source Python ecosystem (Pydantic, pdfplumber, etc.)
- Academic community for best practices

---

**Built for the research community** 

*Empowering the next generation of researchers*
