# Resume / CV Parser — Reference Guide

## Purpose
Extract a complete structured professional profile from any resume or CV (PDF, image, plain text, Word/DOCX screenshot), perform a quality assessment, and optionally score it against a job description.

---

## Step 1 — Document Reading Strategy

| Format | Approach |
|---|---|
| PDF (text-based) | Read full text; structure by visual section headers |
| PDF (scanned/image) | Read visually; follow heading hierarchy |
| Image / screenshot | Read visually; detect columns (two-column layouts are common) |
| Plain text | Parse by blank lines and all-caps section headers |
| HTML/LinkedIn export | Parse `<h2>` section headers and structured lists |

**Two-column layout detection**: Many modern resumes use two columns. Read the left column fully, then the right column. Don't read left-to-right across columns.

---

## Step 2 — Extract Personal Information

| Field | Notes |
|---|---|
| Full Name | Usually largest text at top; ignore academic titles (Dr., Prof.) unless they appear consistently |
| Professional title / headline | Subtitle below name, if present |
| Email | Look for @ symbol |
| Phone | All formats: +1 (555) 000-1234, 555.000.1234, +44 7700 900123 |
| Location | City, State/Country — do NOT expect full address on a resume |
| LinkedIn URL | linkedin.com/in/... |
| GitHub URL | github.com/... |
| Portfolio / website | Personal domain, Behance, Dribbble, Kaggle |
| Twitter / X | If provided |

---

## Step 3 — Extract Professional Summary

If present, quote the summary verbatim (max 150 words). If not present: `[NOT PROVIDED]`.

Note whether it is:
- A generic objective statement ("seeking a challenging role...")
- A specific value proposition ("10 years in fintech, led teams of 30+...")
- A skills-focused summary (list of tools/keywords)

---

## Step 4 — Extract Work Experience

For each role, extract:

| Field | Notes |
|---|---|
| Company name | |
| Job title | Use the exact title on the CV |
| Employment type | Full-time / Part-time / Contract / Freelance / Internship |
| Start date | Month + Year preferred |
| End date | Month + Year, or "Present" |
| Duration | Calculate: "2 yrs 4 mos" |
| Location | City, Country / Remote |
| Team size managed | If mentioned ("managed team of 12") |
| Budget managed | If mentioned ("P&L responsibility of $4M") |
| Key responsibilities | Extract as bullet list — original phrasing |
| Achievements & metrics | Separate from responsibilities — look for numbers, %, $, growth |
| Technologies used | Languages, frameworks, tools mentioned in this role |
| Promotion indicator | If title changed at same company, note as promotion |

**Sort**: Most recent first.

**Achievement extraction rules:**
- Prioritize bullets with quantified outcomes: "Reduced latency by 40%", "Grew revenue from $2M to $8M"
- Flag bullets with weak verbs and no metrics: "Helped with...", "Assisted in..." — mark as `[vague]`
- Distinguish responsibilities from achievements: "Managed social media" (responsibility) vs. "Grew Instagram followers from 10K to 85K in 8 months" (achievement)

---

## Step 5 — Extract Education

| Field | Notes |
|---|---|
| Institution | University / college / school name |
| Degree type | B.Sc., M.Eng., MBA, Ph.D., Associate, Diploma, Certificate |
| Field of study / Major | |
| Minor | If stated |
| Thesis / Dissertation title | If relevant |
| Graduation year | Or expected year |
| GPA / Grade | Only if provided; note scale (e.g., 3.8/4.0 or First Class) |
| Honors / Distinction | Magna cum laude, Dean's List, First Class Honours |
| Relevant coursework | If listed |
| Study abroad | If mentioned |

**Sort**: Most recent first.

---

## Step 6 — Extract Skills

Group extracted skills into a structured taxonomy:

| Category | Detection Patterns |
|---|---|
| Programming Languages | Python, JavaScript, TypeScript, Java, C++, Go, Rust, Swift, Kotlin, Ruby, PHP, R, MATLAB |
| Web Frameworks | React, Angular, Vue, Next.js, Django, Flask, FastAPI, Rails, Laravel, Spring Boot |
| Mobile | iOS, Android, React Native, Flutter, SwiftUI, Jetpack Compose |
| Data & ML | TensorFlow, PyTorch, scikit-learn, Pandas, NumPy, Spark, Hadoop, Databricks |
| Databases | PostgreSQL, MySQL, MongoDB, Redis, Cassandra, DynamoDB, Elasticsearch, Snowflake |
| Cloud & DevOps | AWS, GCP, Azure, Kubernetes, Docker, Terraform, Ansible, CI/CD, Jenkins, GitHub Actions |
| Design | Figma, Sketch, Adobe XD, Photoshop, Illustrator, InDesign, Canva |
| Product & Management | Agile, Scrum, Jira, Confluence, Roadmap, OKRs, A/B Testing, Product Analytics |
| Finance | Financial Modeling, DCF, Excel, Bloomberg, Tableau, Power BI, QuickBooks |
| Marketing | SEO, SEM, Google Analytics, HubSpot, Salesforce, Mailchimp, Social Media |
| Languages (spoken) | English, Spanish, Mandarin, etc. — with proficiency level if stated |
| Soft Skills | Leadership, Communication, Problem-solving — list separately |

For each skill, note:
- **Explicitly stated**: listed in a skills section
- **Implied by experience**: used in a work role description but not in skills section

---

## Step 7 — Extract Certifications, Licenses & Awards

| Field | Notes |
|---|---|
| Certification name | |
| Issuing body | AWS, Google, PMI, CPA board, etc. |
| Issue date | |
| Expiry date | |
| Credential ID | If listed |

**Common high-value certifications to flag:**
AWS (SAA, SAP, CCP), GCP (ACE, Professional), Azure (AZ-900, AZ-104), CPA, CFA, CISSP, PMP, Six Sigma, Scrum Master, CCIE, TOGAF

---

## Step 8 — Extract Projects, Publications, Volunteering

### Projects
| Name | Description | Stack / Tools | URL | Date |
|---|---|---|---|---|

### Publications / Patents
| Title | Publication / Venue | Date | Role (lead/co-author) | DOI/Link |
|---|---|---|---|---|

### Volunteering
| Organization | Role | Duration | Skills Demonstrated |
|---|---|---|---|

### Awards & Recognition
List name, issuer, year, brief description.

---

## Step 9 — Profile Assessment

| Dimension | Value | Notes |
|---|---|---|
| Total years of experience | X years | Calculated from first job start to present |
| Seniority level | Junior / Mid / Senior / Lead / Principal / Director / VP / C-Level | Based on title, experience, and scope |
| Primary domain | e.g., Backend Engineering, Data Science, Product Management, UX Design, Finance |
| Primary industry | e.g., FinTech, HealthTech, E-commerce, Consulting |
| Secondary industries | From employer backgrounds |
| Management experience | Yes (N direct reports) / No / Individual contributor |
| Remote experience | Yes / No / Partial |
| Global experience | Countries/regions worked in |
| Career trajectory | Ascending (each role is a step up) / Lateral / Mixed / Descending |

### Strengths (3–5 bullets)
What stands out positively: quantified achievements, breadth of skills, rapid progression, leadership, domain depth.

### Gaps & Weaknesses (3–5 bullets)
What is missing or weak:
- No quantified achievements (responsibilities only)
- Short tenures (< 1 year at multiple roles — note the pattern)
- Gap in employment history (flag with date range)
- Missing education details
- No portfolio / GitHub / LinkedIn URL
- Summary section absent
- Generic / keyword-stuffed language

### ATS Keyword Density
Common ATS (Applicant Tracking System) optimization issues:
- Is the resume ATS-parseable? (No tables in headers, no text boxes, no images with text)
- Is the job title searchable? (Avoid abbreviations like "PM" — spell out "Product Manager")
- Are skills listed explicitly (not just implied from descriptions)?

---

## Step 10 — Job Description Matching (if provided)

If the user provides a job description alongside the resume:

### Match Analysis
| Requirement | In Resume? | Evidence |
|---|---|---|
| Python (required) | Yes | "5 years Python, used in all roles since 2018" |
| Kubernetes (preferred) | Partial | "Docker" listed but not Kubernetes |
| 5+ years experience | Yes | 7 years total |
| Management experience | No | All roles are individual contributor |

### Match Score
- Required skills coverage: X/N (X%)
- Preferred skills coverage: X/N (X%)
- Experience match: Met / Exceeds / Below
- Overall fit: Strong / Moderate / Weak

### Missing Keywords to Add
List skills and keywords from the JD that are absent from the resume (if the candidate actually has them).

---

## Output Template

Present all sections in order. Skip empty sections with a one-line note:
`Publications: [None found]`

---

## Action Prompt
End with: "Would you like me to:
- Rewrite the professional summary for this role?
- Tailor this resume to a specific job description?
- Export the structured data as JSON?
- Identify the 5 most impactful improvements to this resume?"
