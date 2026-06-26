---
name: gb-citation
description: 
  可根据截图生成国标GB/T 7714-2015的引用标注，触发词："/国标引用" 或 "/gb-cite"
  
  author: Michelle-Lao
  license: MIT
---

# GB/T 7714-2015 Citation Generator

## Trigger Conditions

Activate this skill when ANY of the following is true:
- User message contains an image (journal/book cover)
- User message contains a URL/web link AND asks for citation
- Message text contains "/国标引用" or "/gb-cite"

## Workflow

### Step 1: Detect Input Type

| Input Type | Detection |
|---|---|
| Image (cover) | Message contains image attachment |
| Web link | Message contains URL AND user asks for citation |
| Citation conversion | Message contains an existing citation in APA/Chicago/MLA/Vancouver/Harvard/etc. with or without "/国标引用" or "/gb-cite" |

### Step 2: Extract Information

#### For Images (Screenshots of Journal Articles or Book Covers)

Use vision to read the screenshot/image. First determine if this is a **journal article** or a **monograph/book**:

**Journal indicators (most common):**
- Journal name at top (e.g., "IEEE Transactions on...", "ScienceDirect", "Web of Science")
- Volume, Issue numbers (Vol. 26, Issue 1)
- Page numbers (pp. 59-81)
- DOI visible
- Multiple authors with "Received", "Accepted", "Published online" dates
- Article title format (typically longer, descriptive)

**Book/Monograph indicators:**
- Copyright page with publisher, place of publication, year
- Edition statement (2nd edition, etc.)
- ISBN visible
- Typically fewer authors (1-3)
- "Press", "Publishing" in publisher name

**Extract these fields:**

1. **Document type** — Journal [J] or Book [M] (determine first!)
2. **Authors** — All authors. Chinese: 姓前名后. English: surname ALL CAPS, e.g. SMITH J, WANG Xiaoming
3. **Title** — Full title including subtitle if present
4. **Source** — Journal name / Conference name / Publisher
5. **Year** — Publication year (4 digits)
6. **Volume** — Volume number (if journal)
7. **Issue** — Issue number (if journal)
8. **Pages** — Page range OR article number (e.g. 45-52 or e123456)
9. **DOI** — If visible
10. **Edition** — For books only (e.g. 第2版)
11. **Place** — Publication place (city), for books only

#### For Citation Conversion (APA/Chicago/MLA → GB/T 7714-2015)

Parse the provided citation. Extract:
1. **Authors** — Parse author names (reformat to GB/T 7714 rules)
2. **Title** — Extract title/publication name
3. **Source** — Journal/Book/Publisher/Conference name
4. **Year** — Publication year
5. **Volume/Issue/Pages** — If journal article
6. **Edition/Place/Publisher** — If book
7. **URL/DOI** — If online resource
8. **Document type** — Infer from citation structure

Reformat all extracted fields into GB/T 7714-2015 sequence format.

#### For Web Links

Fetch the webpage content. Extract:
1. **Authors** — From byline, meta tags, or page content
2. **Title** — From `<title>` tag or page heading
3. **Website name** — Domain or site name
4. **Date** — Publication date (YYYY-MM-DD or YYYY-MM or YYYY)
5. **URL** — Full URL
6. **Access date** — Today's date in YYYY-MM-DD

If author/year missing, use GB/T 7714 allowed placeholders:
- No author → [佚名]
- No date → [无日期]

### Step 3: Validate Completeness

Before generating citation, check required fields by document type:

| Type | Required Fields |
|---|---|
| Journal article | Authors, Title, Journal, Year, Volume(Issue), Pages/Article No. |
| Book | Authors, Title, Place, Publisher, Year. Edition if not 1st. |
| Conference paper | Authors, Title, Conference name, Place, Year, Pages |
| Thesis (Master/Doctor) | Author, Title, [D/OL], Place, University, Year |
| Newspaper article | Author, Title, Newspaper name, Date, Edition |
| Report | Author, Title, [R/OL], Place, Publisher, Year |
| Standard | Standard number, Standard name, Place, Publisher, Year (or responsible org) |
| Patent | Applicant/Owner, Title, Patent number, Date |
| Database | Database name, URL, Access date |
| Archives | Responsible party, Title, Place, Publisher, Year |
| Map | Cartographer/Responsible party, Title, Place, Publisher, Year |
| Dataset | Creator, Title, Place, Publisher, Year |
| Web document | Authors (or [佚名]), Title, Website, Date (or [无日期]), URL, Access date |

**If required fields are missing:**
- If only optional fields missing (e.g., DOI, page numbers for online-first articles): Generate citation without them
- If critical fields missing (authors, title, year, journal name for articles; authors, title, place, publisher, year for books): Report ONLY the missing fields concisely, then ask user to provide them
- Example: "Missing: publication year. Please provide."
- DO NOT output lengthy analysis of what you saw in the image

### Step 4: Generate Citation

Read `references/gb7714-2015.md` for complete format rules and examples.

**Output format (CRITICAL):**
- **DO NOT output thinking process, analysis, or explanations**
- **DO NOT use phrases like "Based on the image...", "I can see...", "Here is the citation..."**
- Output ONLY the formatted citation itself
- Single citation per request (unless user asks for multiple)
- No markdown formatting around the citation (plain text)
- If English authors present, use space between initials, e.g. `SMITH J D` not `SMITH J.D.`

### Step 5: Handle Multiple Citations

If user sends multiple images or asks for multiple citations:
- Process each independently
- Output as numbered list: `[1]`, `[2]`, etc.
- Validate each before generating

## Document Type Determination

| Clues | Type |
|---|---|
| "Vol.", "Volume", "卷", 期号, DOI visible | Journal article [J] |
| "Press", "出版社", "Publishing", ISBN, edition | Book [M] |
| "Proceedings", "会议", "Conference", "Symposium" | Conference paper [C] |
| "硕士", "博士", "Master", "Doctoral", "Dissertation" | Thesis [D] or [D/OL] |
| "报", "Times", "Post", "日报", "晚报" | Newspaper article [N] or [N/OL] |
| "Report", "报告", "Technical Report", "White Paper" | Report [R] or [R/OL] |
| "GB/T", "ISO", "Standard", "标准" | Standard [S] or [S/OL] |
| "Patent", "专利", "CN", "US" + number | Patent [P] or [P/OL] |
| "Database", "数据库" | Database [DB/OL] |
| "Archive", "档案" | Archives [A] or [A/OL] |
| "Map", "Atlas", "舆图", "地图" | Map [CM] |
| "Dataset", "数据集" | Dataset [DS] |
| URL, no print identifiers, webpage content | Web document [EB/OL] |

## Academic Database Screenshots

When processing screenshots from academic databases (ScienceDirect, Web of Science, IEEE Xplore, PubMed, etc.):

### Common Journal Patterns

**IEEE Xplore / IEEE Transactions:**
- Header shows: "IEEE TRANSACTIONS ON XXX, VOL. X, NO. X, MONTH YEAR"
- Authors with IEEE membership badges (ignore these)
- Page number in top right corner

**ScienceDirect:**
- Blue header with journal name
- "Volume X, Issue Y, Pages Z"
- "Received", "Revised", "Accepted" dates
- DOI at bottom

**Web of Science / Journal page:**
- Journal name at top
- Article title prominent
- Author list with affiliations
- "Published online" date

**PubMed:**
- Journal name, year, volume(issue): pages
- PMID and DOI
- Author list with superscript affiliations

### Key Rule: Journal vs Book

**MOST screenshots from academic databases are JOURNAL ARTICLES [J]**

Only classify as Book [M] if you see:
- ISBN
- "Copyright page" with publisher city/year
- Edition statement
- Chapter/page structure typical of books
- "Monograph", "Edited volume" labels

## Citation Conversion Rules

When converting from APA/Chicago/MLA to GB/T 7714-2015:

### Author Conversion
- APA: `Smith, J. D.` → `SMITH J D`
- APA (Chinese): `张三, 李四` → `张三, 李四`
- Chicago: `Smith, John D.` → `SMITH J D`
- MLA: `Smith, John D.` → `SMITH J D`

### Title Conversion
- Keep title as-is (do not translate unless user requests)
- APA sentence case → keep original or title case as appropriate
- Chicago/MLA title case → keep as-is

### Journal Article Conversion
**APA input:**
```
Smith, J. D. (2023). Title of article. Journal Name, 45(3), 123-135. https://doi.org/10.xxxx
```
**GB/T 7714-2015 output:**
```
SMITH J D. Title of article[J]. Journal Name, 2023, 45(3): 123-135.
```

### Book Conversion
**APA input:**
```
Smith, J. D. (2023). Book title (2nd ed.). Publisher.
```
**GB/T 7714-2015 output:**
```
SMITH J D. Book title[M]. 2nd ed. Place: Publisher, 2023.
```

### Web Document Conversion
**APA input:**
```
Smith, J. D. (2023, March 15). Title of webpage. Site Name. URL
```
**GB/T 7714-2015 output:**
```
SMITH J D. Title of webpage[EB/OL]. (2023-03-15)[access-date]. URL.
```

### Standard Conversion
**APA input:**
```
National Information Standards Organization. (2010). Dublin Core metadata element set: ANSI/NISO Z39.85-2012. NISO Press.
```
**GB/T 7714-2015 output:**
```
National Information Standards Organization. Dublin Core metadata element set: ANSI/NISO Z39.85-2012[S]. Baltimore: NISO Press, 2010.
```

### Patent Conversion
**APA input:**
```
Smith, J. D. (2024). Method and apparatus for natural language processing (U.S. Patent No. 10,123,456). U.S. Patent and Trademark Office.
```
**GB/T 7714-2015 output:**
```
SMITH J D. Method and apparatus for natural language processing: US10123456[P]. 2024-01-20.
```

## Rules (NEVER violate)

1. **CRITICAL — Output Style**: Output ONLY the formatted citation. NO thinking process, NO analysis, NO "Based on the image...", NO "Here is the citation...". Just the plain citation text.
2. **CRITICAL — Journal vs Book**: MOST screenshots from academic databases (ScienceDirect, Web of Science, IEEE, etc.) are JOURNAL ARTICLES [J]. Do NOT mistake them for books. Only use [M] if you see ISBN, copyright page with publisher, or "edition" statement.
3. **NEVER infer or fabricate information.** If a field is not visible/readable, report it as missing.
4. **NEVER guess authors** from partial names or unclear text.
5. **NEVER assume edition=1** for books — only include edition if explicitly stated as 2nd or higher.
6. **Chinese authors**: 姓前名后, no space, e.g. `张三, 李四`
7. **English authors**: surname ALL CAPS, given name initials, e.g. `SMITH J D, WANG X M`
8. **Hyphenated English surnames**: keep hyphen, all caps, e.g. `WILLIAMS-ELLIS A`
9. **Multi-part English surnames (with prepositions)**: all caps, e.g. `DE MORGAN A`
10. **Chinese pinyin names**: surname ALL CAPS, given name can be full or abbreviated, e.g. `LI Jiangning` or `LI JN`
11. **Organization as author**: record organization name directly as author, e.g. `全国信息与文献标准化技术委员会`
12. **Multiple authors**: 3 or fewer — list all. More than 3 — first author + `, 等` (Chinese) or `, et al.` (English)
13. **Punctuation**: Use `.` after each element in sequence format. Use `//` before conference name.
14. **Web documents**: Always include `[EB/OL]` and access date `[YYYY-MM-DD]`.
15. **DOI format**: End with `DOI:10.xxxx/xxxxx` after URL if available.
16. **Electronic resource update date**: If modified, include `(YYYY-MM-DD)` before access date.
17. **Other title info (subtitle)**: Use `:` before subtitle.
18. **Combined titles (合订题名)**: Separate multiple titles with `;`.
19. **No author (顺序编码制)**: Omit author field and start with title directly.
