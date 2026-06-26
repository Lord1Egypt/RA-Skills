---
name: academic-talon
description: 🎓 Full-stack academic research assistant - Search papers → Extract publication-ready BibTeX (header) → Full TEI XML document structure parsing (via GROBID) → Archive to Zotero → Serve local PDFs. Fixed arXiv AND search semantics, generates conference/journal-standard BibTeX, auto-creates Zotero collections, enables deep document understanding via GROBID structured parsing.
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["python"],
      "env": [
        "ZOTERO_API_KEY",
        "ZOTERO_LIBRARY_ID",
        "GROBID_API_URL"
      ],
      "config": [],
      "secrets": [
        "ZOTERO_API_KEY"
      ]
    },
    "install": [
      {
        "id": "pip-install-deps",
        "kind": "pip",
        "package": "-r requirements.txt",
        "label": "Install Python dependencies (requests python-dotenv pyzotero)"
      }
    ],
    "emoji": "🎓",
    "notes": "⚠️ **SECURITY WARNING**: This skill downloads PDFs from arbitrary URLs and runs an HTTP server to serve local files. Intended FOR PRIVATE INTRANET USE ONLY. Do NOT expose this skill's PDF server to the public internet. All-in-one academic paper management: Search → Extract BibTeX → Archive to Zotero → Serve local PDFs. Fixes arXiv AND search, generates publication-ready BibTeX, auto-creates Zotero collections. Requires GROBID for PDF parsing and Zotero API key for archiving."
  }
}
---

# 🎓 Academic Talon Skill

**Your AI-powered academic research assistant** for paper search → BibTeX extraction → Zotero archiving → local PDF serving.

> Save hours of manual work searching papers, copying citations, and organizing your library.

---

## 🎯 What it does (when to use this skill)

Trigger this skill when the user wants to:

| Task | Description |
|------|-------------|
| 🔍 **Search papers** | Find papers across multiple academic search engines (arXiv, Google Scholar, Semantic Scholar, Tavily) |
| 📝 **Extract BibTeX (header analysis)** | Parse PDF header and output **publication-ready BibTeX** matching AI conference/journal standards |
| 📄 **Full text analysis** | Extract full document structure in TEI XML format for further processing |
| 🗄️ **Archive to Zotero** | Automatically save papers to your Zotero library, default to `openclaw` collection, auto-create collections |
| 📂 **Local PDF library** | Maintain a local PDF collection and serve it via HTTP for direct access from Zotero |

---

## 🔧 Architecture & Dependencies

This is a **toolbox skill** that provides multiple independent academic research tools. You can use just the features you need. A common complete workflow looks like this:

```
User Query
    ↓
[academic-talon] ← this skill
    ↓
1. Search → Multiple search APIs (arXiv, Google Scholar via SerpAPI, etc.)
    ↓
2. PDF Download → saved to local `pdfs/` directory
    ↓
3. PDF Parsing → **GROBID service** processes PDF
    ↓
   - Header analysis → extracts metadata → skill generates clean BibTeX
   - Full text analysis → returns complete TEI XML with full document structure
    ↓
4. If header analysis: BibTeX Generation → skill formats clean publication-ready output
    ↓
5. Zotero Archiving → via **pyzotero** → your Zotero library → auto-add to collection
    ↓
6. PDF Serving → built-in HTTP server serves PDFs from your intranet
    ↓
Result: Paper in Zotero with working PDF link, clean BibTeX ready for citation
```

*You don't have to use this full workflow - use individual tools as needed.*

### Required External Services

| Service | Purpose | Why do you need it? | Required? |
|---------|---------|-------------------|----------|
| **GROBID** | PDF metadata extraction | Parses PDF headers to extract title, authors, publication info for BibTeX | ✅ **Required** |
| **Zotero API** | Paper archiving | Stores papers in your Zotero library with correct metadata | ✅ **Required for archiving** |
| **SerpAPI Key** | Google Scholar search | enables searching Google Scholar | ⚙️ Optional (enables more results) |
| **Semantic Scholar API Key** | Semantic Scholar search | enables Semantic Scholar results | ⚙️ Optional |
| **Tavily API Key** | Tavily search | enables Tavily results | ⚙️ Optional |

---

## ⚙️ Setup Instructions

### 1. Install Python dependencies

```bash
pip install -r skills/academic-talon/requirements.txt
```

### 2. Configure environment variables (`skills/academic-talon/.env`)

```env
# ========== Zotero Configuration (Required for archiving) ==========
ZOTERO_API_KEY=your_zotero_api_key_here
ZOTERO_LIBRARY_ID=your_library_id_here
ZOTERO_LIBRARY_TYPE=user  # or "group" for group libraries

# ========== GROBID Configuration (Required for PDF parsing) ==========
GROBID_API_URL=http://localhost:8070/api
# Or if you use Docker Compose behind nginx:
# GROBID_API_URL=http://localhost:8080/api

# ========== Optional Search API Keys ==========
# Get these from their respective websites
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key
SERPAPI_KEY=your_serpapi_key_for_google_scholar
TAVILY_API_KEY=your_tavily_api_key

# ========== Local PDF Serving (Optional) ==========
# After starting the PDF server, set this to your intranet URL:
# Example: PDF_BASE_URL=http://192.168.1.100:8000/
PDF_BASE_URL=http://your-server-ip:port/
```

| Environment Variable | What it does |
|----------------------|--------------|
| `ZOTERO_API_KEY` | Your Zotero API key from [Zotero settings](https://www.zotero.org/settings/keys) |
| `ZOTERO_LIBRARY_ID` | Your Zotero library ID (found in Zotero API URL) |
| `ZOTERO_LIBRARY_TYPE` | `"user"` for your personal library, `"group"` for group libraries |
| `GROBID_API_URL` | URL of your GROBID service endpoint |
| `PDF_BASE_URL` | Base URL for your locally running PDF server (e.g. `http://10.26.20.168:18001/`) |

### 3. Start GROBID (for PDF parsing)

**Option A: Docker Compose (Recommended)**

Create `compose.yml` in your GROBID directory:

```yaml
version: "3.9"
services:
  grobid:
    # Choose the right image for your hardware:
    # - For non-GPU environments: grobid/grobid:0.8.2-crf (CRF-only model, smaller)
    # - For GPU environments: grobid/grobid:0.8.2-full (includes CRF + deep learning models)
    image: grobid/grobid:0.8.2-crf
    container_name: grobid
    restart: unless-stopped
    expose:
      - "8070"
    environment:
      JAVA_OPTS: "-Xms512m -Xmx4g"
    volumes:
      - ./grobid/tmp:/opt/grobid/tmp
      - ./grobid/logs:/opt/grobid/logs
```

> 💡 **Image selection**: Use `grobid/grobid:0.8.2-crf` for CPU-only / non-GPU environments (smaller image, faster startup). Use `grobid/grobid:0.8.2-full` if you have GPU and want maximum accuracy with deep learning models.

Start:
```bash
docker-compose up -d
```

**Option B: Direct run**

Follow [GROBID documentation](https://grobid.readthedocs.io/) to run directly.

### 4. (Optional) Start the Local PDF Server

If you want to serve downloaded PDFs locally:

```bash
# Start on port 8000, allow all intranet access
python skills/academic-talon/scripts/start_pdf_server.py start 8000 内网

# Check status
python skills/academic-talon/scripts/start_pdf_server.py status

# Stop
python skills/academic-talon/scripts/start_pdf_server.py stop
```

The server:
- Serves only from the `pdfs/` directory (sandboxed, no access outside)
- Default binds to all interfaces → accessible from your entire intranet
- Filenames are citation keys (e.g. `zhang2025hallucinationdetection.pdf`)
- When `PDF_BASE_URL` is configured, archived papers automatically get the correct local URL

---

## 📖 Usage (for LLM)

### Input Schema

| Parameter | Type | Description | Required | Default |
|-----------|------|-------------|----------|---------|
| `action` | string | Action to perform: `search`, `download`, `analyze`, `archive` | Yes | `search` |
| `query` | string | Search keywords | Yes (search) | - |
| `limit` | integer | Max results to return | No | `10` |
| `source` | string | Search source: `all`, `arxiv`, `google_scholar`, `semantic_scholar`, `tavily` | No | `all` |
| `engine_weights` | object | How many results from each engine | No | `{"arxiv": 5, "google_scholar": 3, "semantic_scholar": 1, "tavily": 1}` |
| `url` | string | PDF URL to download | Yes (download) | - |
| `filename` | string | Custom filename for downloaded PDF | No | auto from citation key |
| `paper_info` | object | Paper metadata (title, authors, year) for citation key generation | No | - |
| `pdf_input` | string | Path to local PDF or URL to remote PDF | Yes (analyze) | - |
| `analysis_type` | string | `header` → outputs publication-ready BibTeX; `fulltext` → outputs TEI XML of full document | No | `header` |
| `collection` | string | Zotero collection name to add paper to | No | `openclaw` |

### Output Format

All actions return JSON in this format:

```json
{
  "success": true,
  "action": "search",
  "query": "your search query",
  "results": [
    {
      "title": "Paper Title",
      "authors": ["Author One", "Author Two"],
      "year": "2025",
      "abstract": "Paper abstract...",
      "url": "https://...",
      "pdf_url": "https://...",
      "source": "arxiv"
    }
  ]
}
```

---

## ✨ Features (and how they help your research)

### 1. **Fixed arXiv Search**
- ❌ **Before**: arXiv API defaults to OR semantics → searching "LLM judge knowledge possession" returns papers with just one keyword → many irrelevant results
- ✅ **Now**: **Proper AND semantics** matches what you get in browser search. Every result contains **all** query terms in title or abstract.
- 🎯 **Benefit**: Get relevant results first try, no scrolling through irrelevant papers

### 2. **Publication-Ready BibTeX Generation**
- Follows exactly the format used by top AI conferences (NeurIPS, ICML, ICLR, CVPR, etc.)
- **Correct entry types**:
  - Journal article → `@article`
  - Conference paper → `@inproceedings` with conference name in `booktitle`
  - arXiv preprint → `@article` with `journal = {arXiv preprint xxxx.xxxxx}` **exactly matching your example**
- **Cleans up junk**: removes unnecessary fields like `date`, `month`, `publisher`, `day` that shouldn't be in final submissions
- **Correct citation keys**: `lastnameYearTitle` → `zhang2025hallucinationdetection` matches standard academic practice

**Example output (ready to paste into your manuscript):**

```bib
@article{zhang2025hallucinationdetection,
  author = {Zhang, Chenggong and Wang, Haopeng},
  title = {Hallucination Detection and Evaluation of Large Language Model},
  year = {2025},
  journal = {arXiv preprint 2512.22416},
  abstract = {Hallucinations in Large Language Models...},
}
```

```bib
@inproceedings{gal2016dropout,
  author = {Gal, Yarin and Ghahramani, Zoubin},
  title = {Dropout as a bayesian approximation: Representing model uncertainty in deep learning},
  booktitle = {ICML},
  year = {2016},
}
```

### 3. **Smart Zotero Archiving**
- 🎯 **Default collection**: all papers go to `openclaw` unless you specify otherwise
- 🪄 **Auto-creation**: if the collection doesn't exist, skill automatically creates it
- 🔄 **Smart duplicate handling**: if paper already exists in your library, skill **adds it to the target collection** instead of failing
- 🏷️ **Correct Zotero types**: preprint → `preprint`, conference → `conferencePaper`, journal → `journalArticle`
- 📍 **Local PDF links**: when you run the local PDF server, links point directly to your local copy

**Benefit**: Build your research library without repetitive manual clicking.

### 4. **Local PDF Library Serving**
- Maintain all your PDFs locally
- Built-in HTTP server with start/stop/status management
- Designed for intranet access → you can access your PDFs from any device on your network
- Zotero links point directly to local files → no downloading the same PDF multiple times

---

## 🔒 Security Considerations

### ⚠️ Important Security Notes

1. **PDF Processing goes to GROBID**:
   - This skill sends PDF content to the configured `GROBID_API_URL` for metadata extraction
   - **Recommendation**: Run GROBID locally on your own machine/infrastructure for privacy
   - If you use a third-party GROBID service, be aware that they will see your PDFs

2. **Local PDF Server**:
   - This skill runs an HTTP server that serves PDF files from the `pdfs/` directory
   - It is **designed for intranet/private network use only**
   - The server **does NOT include authentication**
   - ❌ **Do NOT expose this server directly to the public internet**
   - ✅ Only run on trusted private networks, or put it behind a reverse proxy with authentication

3. **File Access Restrictions**:
   - All file operations (download, analysis) are **sandboxed to the `pdfs/` directory within this skill's installation**
   - Directory traversal attacks are prevented by path checking
   - The skill cannot access or modify files outside its own directory

4. **API Key Storage**:
   - All API keys are stored locally in the `.env` file
   - Never commit `.env` to version control
   - Keys are only used for API requests directly from your machine to the service providers

### Best Security Practices

- ✅ Run GROBID locally (don't send sensitive PDFs to third parties)
- ✅ Keep PDF server on private/intranet network only
- ✅ Use reverse proxy with authentication if you need public access
- ✅ Use a dedicated Zotero API key with limited permissions
- ✅ Don't expose GROBID directly to the internet (use the recommended nginx proxy with IP whitelist)

---

## 📋 Complete Workflow Example

```python
# 1. Search for papers
result = skill.run({
  "action": "search",
  "query": "LLM judge knowledge possession",
  "limit": 5
})

# 2. Download PDF for first result
paper = result["results"][0]
download_result = skill.run({
  "action": "download",
  "url": paper["pdf_url"],
  "paper_info": paper
})

# 3. Extract BibTeX from downloaded PDF
analyze_result = skill.run({
  "action": "analyze",
  "pdf_input": download_result["pdf_path"],
  "analysis_type": "header"
})

# 4. Archive to Zotero (goes to openclaw collection by default)
paper["bibtex"] = analyze_result["result"]
archive_result = skill.run({
  "action": "archive",
  "paper_info": paper
})

if archive_result["success"]:
  print(f"✅ Paper archived to Zotero: {archive_result['result']['item_id']}")
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|---------|
| `GROBID server not accessible` | Check GROBID is running, verify `GROBID_API_URL` in `.env` |
| `Zotero API error` | Check `ZOTERO_API_KEY` and `ZOTERO_LIBRARY_ID` are correct |
| `arXiv search returns nothing` | Check network connectivity, arXiv API sometimes blocks unusual IPs |
| `PDF analysis returns empty` | Check PDF isn't corrupted, verify GROBID is working |
| `Local PDF link doesn't work` | Check PDF server is running, verify `PDF_BASE_URL` matches server address |
| `Duplicate papers in Zotero` | Skill detects duplicates by title/DOI and adds to collection, safe to ignore |

---

## 📊 Benefits for Academic Research

- **Saves time**: Go from keywords → archived paper in minutes instead of manually copying everything
- **Consistent citations**: Always get clean BibTeX ready for journal/conference submission
- **Organized library**: Automatic collection management keeps your papers organized
- **Local access**: Keep all PDFs locally and access them from anywhere on your network
- **Correct search**: Get relevant results from arXiv with proper AND semantics

---

## 📦 Dependencies Summary

- **Python**: 3.6+
- **Python packages**: `requests`, `python-dotenv`, `pyzotero`
- **External services**: GROBID (PDF parsing), Zotero API (archiving)
- **Optional APIs**: SerpAPI (Google Scholar), Semantic Scholar API, Tavily API

---

## 📄 License

MIT License - free for academic and commercial use.
