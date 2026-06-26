# AISEACT Search Strategies and Techniques

This document provides specific search strategies and techniques to help AI Agents effectively avoid low-quality sources and quickly find authoritative primary information.

---

## I. Core Strategies to Avoid Low-Quality Sources

### 1.1 Identifying Low-Quality Sources

**Source Types to Exclude**:

| Platform | URL Pattern | Risk Level |
|----------|-------------|------------|
| 百家号 (Baijiahao) | `baijiahao.baidu.com` | Extremely High |
| 百度知道 (Baidu Zhidao) | `zhidao.baidu.com` | High |
| 百度经验 (Baidu Jingyan) | `jingyan.baidu.com` | High |
| 搜狐号 (Sohu) | `sohu.com/a/` | Extremely High |
| 网易号 (NetEase) | `163.com` dynamic pages | High |
| 新浪看点 (Sina) | `k.sina.com.cn` | High |
| Tencent News (unofficial) | `new.qq.com` partial reprints | Medium |
| CSDN (non-original) | `csdn.net` heavy crawler content | High |
| 简书 (Jianshu) | `jianshu.com` | High |
| 知乎专栏 Zhihu (unverified) | `zhuanlan.zhihu.com` | Medium |

### 1.2 Exclusion Syntax

Use `-` to exclude specific sites in searches:

```
company_name -baijiahao -sohu -csdn -jianshu
```

**Note**: This syntax may not be supported in some search engines. The more reliable method is **actively identifying and skipping** these results.

### 1.3 Limitation Syntax (Recommended)

Use `site:` syntax to directly limit to authoritative sources:

| Target | Syntax | Example |
|--------|--------|---------|
| Government websites | `site:gov.cn` | `policy_topic site:gov.cn` |
| China Government Network | `site:gov.cn` | `policy_topic site:gov.cn` |
| 巨潮资讯 (Juchao) | `site:cninfo.com.cn` | `company_name annual_report site:cninfo.com.cn` |
| GitHub | `site:github.com` | `kubernetes site:github.com` |
| University websites | `site:edu.cn` | `major_name site:edu.cn` |
| English government | `site:gov` | `topic site:agency.gov` |

---

## II. Scenario-Based Search Strategies

### 2.1 Company Research Scenario

**Objective**: Obtain company official information, financial data, business introduction

**Primary Source Priority**:
1. Company official website (products, technology, team)
2. Prospectus/Annual reports (巨潮资讯网)
3. Investor relations pages
4. Official technical documentation/GitHub

**Search Combinations**:

```
# Basic information
company_name official website
site:company_domain

# Listing information (A-shares)
company_name 招股说明书 site:cninfo.com.cn
company_name 年报 site:cninfo.com.cn filetype:pdf

# Hong Kong stocks
company_name 招股書 site:hkexnews.hk

# US stocks
company_name IPO prospectus SEC
company_name annual report 10-K

# Investor relations
company_name investor relations
site:company_domain investor_relations

# Technical documentation
site:company_domain whitepaper
site:company_domain technical_architecture
```

**English Search (for cleaner results)**:
```
"Company Name" prospectus
"Company Name" annual report
"Company Name" technology whitepaper
```

### 2.2 Technical Questions Scenario

**Objective**: Obtain accurate technical information, best practices

**Primary Source Priority**:
1. Official documentation (first choice!)
2. GitHub official repositories
3. RFC/Standard documents
4. Academic papers

**Search Combinations**:

```
# Official documentation
technology_name official documentation
technology_name docs
site:technology-docs-domain docs

# GitHub
technology_name site:github.com
technology_name github

# Academic papers
technology_name survey paper
technology_name review filetype:pdf

# Alternatives to avoid CSDN
technology_name "stackoverflow.com"
technology_name "medium.com" (official accounts)
technology_name "dev.to" (official accounts)
```

**PDF Document Search**:
```
technology_name specification filetype:pdf
technology_name whitepaper filetype:pdf
technology_name RFC filetype:pdf
```

### 2.3 Policies and Regulations Scenario

**Objective**: Obtain official policy documents, original regulations

**Primary Source Priority**:
1. Government official websites (State Council, ministries)
2. Official legal databases
3. Official interpretation documents

**Search Combinations**:

```
# Policies and regulations
policy_topic site:gov.cn
policy_topic site:gov.cn filetype:pdf

# Specific ministries
policy_topic site:miit.gov.cn
policy_topic site:moe.gov.cn
policy_topic site:nhc.gov.cn

# Laws and regulations
law_name site:npc.gov.cn
regulation_name site:gov.cn

# English policies
"policy_topic" site:gov
China policy_topic white paper
```

### 2.4 Industry Research Scenario

**Objective**: Obtain industry data, market analysis

**Primary Source Priority**:
1. Government statistics (Bureau of Statistics)
2. Industry association reports
3. Listed company financial reports (industry data)
4. Authoritative research institution reports

**Search Combinations**:

```
# Official statistics
industry_name statistical yearbook site:stats.gov.cn
industry_name data site:gov.cn

# Industry associations
industry_name association site:org.cn
China industry_name association

# Industry reports
industry_name whitepaper filetype:pdf
industry_name research report site:cninfo.com.cn

# International data
industry_name market size report
industry_name statistics World Bank
```

### 2.5 Person/Event Scenario

**Objective**: Obtain accurate person information, event progression

**Primary Source Priority**:
1. Official announcements/statements
2. Authoritative media reports (original reports)
3. Official social media

**Search Combinations**:

```
# Person information
person_name official
person_name site:company_domain

# Events
event_name official announcement site:gov.cn
event_name press conference

# Avoid rumors
event_name rumors debunked site:gov.cn
event_name fact check
```

---

## III. Advanced Search Techniques

### 3.1 File Type Limitation

Use `filetype:` to search for specific format documents:

| Format | Use Case | Example |
|--------|----------|---------|
| `filetype:pdf` | Official documents, reports, papers | `company_name annual report filetype:pdf` |
| `filetype:ppt` | Presentation slides | `technology_name introduction filetype:ppt` |
| `filetype:doc` | Word documents | `form_name application filetype:doc` |

### 3.2 Time Limitation

Get latest information:

```
# Use search engine's time filter
# Or add year keywords
company_name 2024
technology_name latest
```

### 3.3 Exact Match

Use `""` for exact phrase matching:

```
"artificial intelligence development outline" site:gov.cn
"company_name" listing
```

### 3.4 Synonym Expansion

Use `OR` to expand search:

```
(AI OR artificial intelligence OR machine learning) policy site:gov.cn
```

### 3.5 Site-Specific Search

Combine `site:` with keywords:

```
site:company_domain (whitepaper OR white paper)
site:cninfo.com.cn (annual report OR 年报)
```

---

## IV. Quick Decision Workflow

### 4.1 Decision When Seeing Search Results

**Step 1: Look at URL, Exclude Immediately**
- Contains `baijiahao.baidu.com` → Exclude
- Contains `sohu.com/a/` → Exclude
- Contains `csdn.net` and not well-known blogger → Exclude
- Contains `jianshu.com` → Exclude

**Step 2: Look at URL, Priority Click**
- Contains `gov.cn` / `gov` → Priority
- Contains `cninfo.com.cn` → Priority
- Contains target company official website → Priority
- Contains `github.com` (technical) → Priority
- Contains `edu.cn` / `edu` → Priority

**Step 3: Look at Title, Auxiliary Judgment**
- Title contains "official", "announcement", "report" → Likely reliable
- Title sensational, all caps → Be alert
- Title contains "shocking", "explosive" → Exclude

### 4.2 Assessment After Entering Page

**30-Second Quick Assessment**:

1. **Look at page top**
   - Clear logo and navigation → Formal website
   - Full-screen ads, pop-ups → Content farm

2. **Look at article header**
   - Author attribution, publication time → Formal
   - No author, no time → Suspicious

3. **Look at content quality**
   - Neat layout, standardized citations → Reliable
   - Messy layout, many typos → Low quality

4. **Look at "About Us"**
   - Has organization introduction, contact info → Traceable
   - No relevant info → Suspicious

---

## V. Common Traps and Avoidance

### 5.1 Content Farm Traps

**Characteristics**:
- Domain contains random characters
- Article bottom has many related recommendations (clickbait)
- Content pieced together, logic jumps
- No author information

**Avoidance**:
- Use `site:` to limit to authoritative sources
- Actively identify garbage domain patterns
- Priority click familiar authoritative domains

### 5.2 Rewritten Content Traps

**Characteristics**:
- Content seems familiar
- Unsmooth sentences (machine rewriting traces)
- No original viewpoints, pure copying
- Published on self-media platforms

**Avoidance**:
- Trace to original sources
- Directly search for official sources
- Don't cite self-media articles

### 5.3 Outdated Information Traps

**Characteristics**:
- Publication date is old
- Involves rapidly changing fields (technology, policy)
- Data obviously outdated

**Avoidance**:
- Pay attention to publication time
- Prioritize latest official information
- For rapidly changing fields, label information timeliness

### 5.4 Biased Information Traps

**Characteristics**:
- Obviously extreme positions
- Emotional language
- Lack of balanced viewpoints

**Avoidance**:
- Find multiple perspectives
- Prioritize neutral authoritative sources
- Distinguish facts from opinions

---

## VI. Practical Quick Reference

### 6.1 Authoritative Source Quick Reference

| Type | Domain | Purpose |
|------|--------|---------|
| China Government | gov.cn | Policies and regulations |
| 巨潮资讯 (Juchao) | cninfo.com.cn | Listed company announcements |
| Hong Kong Exchange | hkexnews.hk | HK announcements |
| SEC | sec.gov | US announcements |
| GitHub | github.com | Technical projects |
| Universities | edu.cn / edu | Academic research |
| International Orgs | org | Standards, reports |

### 6.2 Garbage Source Quick Reference

| Type | Domain Pattern | Handling |
|------|----------------|----------|
| 百家号 (Baijiahao) | baijiahao.baidu.com | Completely exclude |
| 搜狐号 (Sohu) | sohu.com/a/ | Completely exclude |
| 网易号 (NetEase) | 163.com dynamic pages | Completely exclude |
| CSDN crawler | csdn.net non-original | Cautious/Exclude |
| 简书 (Jianshu) | jianshu.com | Exclude |
| Content farm | Random character domains | Exclude |

### 6.3 Search Syntax Quick Reference

| Syntax | Function | Example |
|--------|----------|---------|
| `site:` | Limit to site | `topic site:gov.cn` |
| `filetype:` | Limit format | `topic filetype:pdf` |
| `""` | Exact match | `"artificial intelligence"` |
| `-` | Exclude | `topic -baijiahao` |
| `OR` | Or | `topic_A OR topic_B` |
| `()` | Grouping | `(topic_A OR topic_B) site:gov.cn` |

---

*Master these search strategies to enable AI Agents to accurately locate authoritative sources in the ocean of information.*
