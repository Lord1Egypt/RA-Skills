# 🔴 EVE — Research Supervisor Pro

> Persistent AI Research Supervisor Agent — from your first idea to a publication-ready LaTeX paper.

---

## 🎛️ Three Modes

| Mode | Description | Best For |
|---|---|---|
| 🤖 **Auto** | Topic in → full paper out, ~15 min, no interruptions | Quick exploration, first pass |
| 🎯 **Semi-Auto** | Auto pipeline with 3 smart pauses for your decisions | Thesis work, serious research |
| 🔧 **Manual** | One command at a time, full control | Advanced users, specific tasks |

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Semantic Search | Find papers by meaning via Semantic Scholar |
| 📥 PDF Download | Download real PDFs from arXiv with metadata |
| 🕸️ Citation Graph | Build who-cites-whom network, find foundational papers |
| 📊 Citation Ranking | Rank papers by citation count |
| 🔬 Gap Detection | LLM-powered research gap analysis (★★★ ranked) |
| 💡 Idea Generation | Generate specific, publishable research ideas |
| 📝 Paper Writing | Full LaTeX papers — survey + research |
| 📈 Real Data → Figures | Feed your results → auto-generate matplotlib graphs |
| 📋 Real Data → Tables | Comparison + ablation tables in LaTeX |
| 📚 Auto Bibliography | Every paper → instant BibTeX entry, zero manual work |
| 🎓 Thesis Context | Your specific research context for targeted suggestions |
| 📋 Venue Checklists | Requirements for IEEE TIFS, NeurIPS, CVPR, thesis, and more |
| 🖥️ Server Monitor | SSH into GPU server, check jobs, GPU usage, pull results |
| 🔔 Experiment Alerts | Watch training, alert on completion/crash/milestone |
| 🗺️ Research Roadmap | Full step-by-step plan when you have no data yet |
| 🧠 Session Memory | Remembers your research across sessions and weeks |

---

## 🚀 Install from GitHub

### One-line install (copy + paste)
```bash
git clone https://github.com/amzayn/eve-research-supervisor-pro && cd eve-research-supervisor-pro && bash install.sh && mkdir -p ~/.openclaw/workspace/skills/eve-research-supervisor-pro && cp SKILL.md ~/.openclaw/workspace/skills/eve-research-supervisor-pro/SKILL.md && echo "✅ EVE installed!"
```

### Step by step
```bash
# 1. Download
git clone https://github.com/amzayn/eve-research-supervisor-pro
cd eve-research-supervisor-pro

# 2. Install scripts + dependencies
bash install.sh

# 3. Register skill with OpenClaw
mkdir -p ~/.openclaw/workspace/skills/eve-research-supervisor-pro
cp SKILL.md ~/.openclaw/workspace/skills/eve-research-supervisor-pro/SKILL.md

# 4. Talk to your AI
# "EVE, start research mode"
```

### Verify installation
```bash
ls ~/.openclaw/workspace/research-supervisor-pro/scripts/
# Should show 18 scripts
```

### First time setup (optional but recommended)
```bash
# Set your thesis context for targeted suggestions
python3 ~/.openclaw/workspace/research-supervisor-pro/scripts/thesis_context.py init

# Configure your GPU server for monitoring
python3 ~/.openclaw/workspace/research-supervisor-pro/scripts/server_monitor.py setup
```

## 🚀 Quick Start

### First time — set your thesis context
```bash
python3 scripts/thesis_context.py init
```

### Run full auto pipeline
```bash
python3 scripts/arxiv_downloader.py "watermark diffusion models" 30
python3 scripts/bib_generator.py
python3 scripts/citation_graph.py
python3 scripts/semantic_ranker.py
python3 scripts/pdf_parser.py
python3 scripts/gap_detector.py
python3 scripts/idea_generator.py
python3 scripts/paper_writer.py survey notes.md "Your Topic" paper.tex "Your Name"
```

### Or just tell your AI agent:
```
"EVE, research watermark diffusion models — semi-auto mode"
```

---

## 🗺️ Research Roadmap (No Data Yet?)

EVE asks about your machine, timeline, and coding level — then generates a full roadmap:

```
PHASE A — Environment Setup      (1-2 days)
PHASE B — Baseline Implementation (3-5 days)
PHASE C — Your Method             (5-7 days)
PHASE D — Analysis                (2-3 days)
PHASE E — Paper Writing           (EVE handles this)
```

Step-by-step execution, smart resume across sessions, blocker handling.

---

## 📊 Real Data → Paper

Fill the template with your results:
```json
{
  "experiments": [{"name": "BER vs Epochs", "x": [...], "y": [...]}],
  "comparisons": [{"title": "vs Baselines", "methods": [...], "values": [...]}],
  "tables": [{"caption": "Results", "headers": [...], "rows": [[...]]}]
}
```

Run and get auto-generated figures + LaTeX tables in your paper:
```bash
python3 scripts/paper_writer.py research "Topic" data.json paper.tex "Author" "IEEE TIFS"
```

---

## 🖥️ Server Monitoring

```bash
python3 scripts/server_monitor.py setup    # one-time config
python3 scripts/server_monitor.py status   # GPU + jobs + disk
python3 scripts/server_monitor.py watch 12345  # live job log
```

## 🔔 Experiment Alerts

```bash
# Alert when BER drops below 0.1
python3 scripts/experiment_alert.py watch 12345 --metric BER --threshold 0.1

# Auto-update data template from training log
python3 scripts/experiment_alert.py update my_project logs/train.out
```

---

## 📁 File Structure

```
eve-research-supervisor-pro/
├── SKILL.md                          ← AI agent instructions
├── README.md                         ← This file
├── package.json                      ← ClawHub manifest
├── config.yaml                       ← Configuration
├── install.sh                        ← Auto installer
├── scripts/
│   ├── arxiv_downloader.py           Search & download papers
│   ├── semantic_search.py            Semantic Scholar search
│   ├── semantic_ranker.py            Rank by citations
│   ├── citation_graph.py             Build citation network
│   ├── pdf_parser.py                 Extract PDF content
│   ├── gap_detector.py               LLM gap detection
│   ├── idea_generator.py             LLM idea generation
│   ├── paper_writer.py               Full LaTeX paper writer
│   ├── build_survey.py               Survey builder
│   ├── bib_generator.py              Auto BibTeX generation
│   ├── thesis_context.py             Thesis context manager
│   ├── venue_checklist.py            Venue requirements
│   ├── server_monitor.py             SSH/SLURM monitoring
│   ├── experiment_alert.py           Training job alerts
│   ├── roadmap_tracker.py            Research roadmap tracker
│   ├── project_init.py               Project folder setup
│   ├── session_memory.py             Persistent memory
│   └── logger.py                     Pipeline logger
└── templates/
    ├── experiment_data_template.json  Real data format
    └── survey.tex                     LaTeX template
```

---

## ⚙️ Requirements

```bash
pip install requests pypdf matplotlib numpy
```

**Zero API setup on PetClaw** — uses built-in key automatically.

For non-PetClaw:
```bash
export OPENAI_API_KEY=your_key
export OPENAI_BASE_URL=https://api.openai-hk.com/v1
```

Optional (citation graph visualization):
```bash
brew install graphviz   # macOS
apt install graphviz    # Linux
```

---

## 📋 Supported Venues

IEEE TIFS · NeurIPS · CVPR · ICCV · ACM MM · IEEE TSP · Master's/PhD Thesis

---

## 👤 Author

**Zain Ul Abdeen**  
Master's student, Harbin Institute of Technology (Shenzhen)  
Research: AI watermarking, diffusion models, adversarial ML

---

## 📄 License

MIT — Free to use, modify, and share.
