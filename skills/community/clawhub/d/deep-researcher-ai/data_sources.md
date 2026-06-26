# Deep Researcher — Data Sources Registry
## Academic, Economic, Industry, and Technology Sources

---

## PRIORITY: HIGH (Free, Open Access)

### arXiv
- **URL**: `https://export.arxiv.org/api/query`
- **Best for**: Cutting-edge AI/ML/theory papers, preprints
- **No API key required**
- **Rate limit**: ~1000 requests/hour
- **Coverage**: Physics, math, CS, quantitative biology, finance, statistics

### PubMed / PubMed Central
- **URL**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- **Best for**: Biomedical, life sciences, clinical research
- **No API key required**
- **Query format**: `?db=pubmed&term=search&rettype=abstract&retmax=50`

### World Bank Open Data
- **URL**: `https://api.worldbank.org/v2/`
- **Best for**: GDP, demographics, development indicators by country
- **No API key required**
- **Format**: JSON, `?format=json`

### IMF Data API
- **URL**: `https://api.imf.org/v1/`
- **Best for**: Macroeconomic indicators, financial data
- **Free registration available**
- **Coverage**: World Economic Outlook, financial soundness indicators

### OECD Statistics
- **URL**: `https://stats.oecd.org/`
- **Best for**: Comparative country data, policy trends, education, health
- **Mostly open access**

### Semantic Scholar
- **URL**: `https://api.semanticscholar.org/`
- **Best for**: CS academic papers with citation graphs
- **Free tier available**

### Hugging Face Hub API
- **URL**: `https://api.huggingface.co/`
- **Best for**: AI/ML model trends, dataset discovery, recent papers
- **Free tier**: 60 requests/hour

### GitHub API
- **URL**: `https://api.github.com/`
- **Best for**: Code trends, repository statistics, developer activity
- **Free tier**: 60 requests/hour (unauthenticated)

---

## PRIORITY: MEDIUM (Free + Institutional/Subscription)

### Google Scholar
- **Tool**: `batch_web_search` — search by topic and keywords
- **Best for**: Broad academic coverage across all disciplines
- **Tip**: Use specific query operators like `"exact phrase"` and `site:scholar.google.com`

### IEEE Xplore
- **Tool**: `batch_web_search` + institutional access
- **Best for**: Electrical engineering, CS, networking, communications
- **Tip**: Many papers available via open access

### McKinsey & Company Insights
- **URL**: `https://www.mckinsey.com/featured-insights`
- **Best for**: Business strategy, technology, policy insights
- **Access**: Many articles publicly available

### Google Patents
- **URL**: `https://patents.google.com/`
- **Best for**: Innovation trends, R&D tracking, technology history
- **Access**: Free and open

---

## PRIORITY: LOW (Supplemental / Current Events)

### Reuters / BBC News
- **Use for**: Current events context, recent developments
- **Tool**: `batch_web_search`
- **Note**: Use as supporting context, not primary sources

### Statista
- **URL**: `https://www.statista.com/`
- **Best for**: Market statistics, consumer data, industry reports
- **Note**: Premium subscription required for full access; use available public data

---

## SEARCH STRATEGY

### Keyword Expansion Template
For any topic, generate keyword variants:
1. Core term + synonyms
2. Core term + subfield (e.g., "AI" + "healthcare" = "AI healthcare")
3. Acronyms and full forms (e.g., "NLP" AND "Natural Language Processing")
4. Related field terms (e.g., "machine learning" → "deep learning", "neural networks")
5. Application domains (e.g., "computer vision" → "autonomous vehicles", "medical imaging")

### Boolean Search Template
```
(core_term AND related_term) NOT excluded_term
"exact phrase" AND (author OR institution)
(topic A OR topic B) AND (year >= 2020)
```

### Source Diversity Checklist
At least one source from each tier:
- [ ] Academic: arXiv / PubMed / Google Scholar
- [ ] Economic: World Bank / IMF / OECD
- [ ] Industry: McKinsey / Gartner / company reports
- [ ] Technology: GitHub / Hugging Face / Google Patents

---

## API ACCESS NOTES

- **Rate limit respect**: Always add delays between bulk API calls
- **No API key needed** for: arXiv, World Bank, PubMed, Google Patents, Semantic Scholar (free tier)
- **Cache results**: Store source metadata locally to avoid repeat API calls
- **Verify access**: Check HTTP 200 status on all URLs before citing