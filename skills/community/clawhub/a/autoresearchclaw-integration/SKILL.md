---
name: researchclaw
description: OpenClaw integration for AutoResearchClaw - fully autonomous research from idea to paper. Use when user requests academic research, literature review, or paper writing such as: (1) "Research [topic]", (2) "Write a paper about [topic]", (3) "Find literature on [topic]", (4) "Analyze [research question]", (5) "Generate academic paper from [idea]". Auto-installs AutoResearchClaw, configures LLM backend, runs 23-stage pipeline, returns LaTeX paper + experimental code + real citations.
---

# ResearchClaw

AutoResearchClaw is a fully autonomous 23-stage research pipeline that transforms a single research idea into a conference-ready academic paper with real literature from OpenAlex, Semantic Scholar, and arXiv.

## Quick Start

### Basic Usage

User says: "Research [topic]"

Agent workflow:
1. Check if AutoResearchClaw is installed (`which researchclaw`)
2. If not installed: clone, setup venv, install with `pip install -e .`
3. Copy `config.researchclaw.example.yaml` → `config.arc.yaml`
4. Ask user for LLM provider choice (OpenAI-compatible or ACP agent)
5. Configure with API keys or ACP agent selection
6. Run: `researchclaw run --topic "[topic]" --auto-approve`
7. Monitor progress, return results from `artifacts/rc-*/deliverables/`

### Configuration

Ask user for LLM backend preference:

**Option 1: OpenAI-compatible API**
```yaml
llm:
  provider: "openai-compatible"
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"  # or ask for key
  primary_model: "gpt-4o"
  fallback_models: ["gpt-4o-mini"]
```

**Option 2: ACP Agent (Claude Code, Codex, Gemini)**
```yaml
llm:
  provider: "acp"
  acp:
    agent: "claude"  # or "codex", "gemini", etc.
    cwd: "."
```

## Installation

### Check Installation
```bash
which researchclaw || echo "Not installed"
```

### Install AutoResearchClaw
```bash
cd ~
git clone https://github.com/aiming-lab/AutoResearchClaw.git
cd AutoResearchClaw
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Verify Installation
```bash
researchclaw --version
```

## Running Research

### Basic Command
```bash
researchclaw run --topic "Your research idea" --auto-approve
```

### With Specific Config
```bash
researchclaw run --config config.arc.yaml --topic "Your research idea" --auto-approve
```

### Output Location
Results in: `~/AutoResearchClaw/artifacts/rc-YYYYMMDD-HHMMSS-<hash>/deliverables/`

## Deliverables

After completion, the agent should:
1. Check `deliverables/` directory contents
2. Present key outputs:
   - `paper.tex` - Conference-ready LaTeX
   - `paper_draft.md` - Markdown paper
   - `references.bib` - Real citations
   - `verification_report.json` - Citation integrity check
   - `runs/` - Experimental code and results
   - `charts/` - Generated figures
   - `reviews.md` - Multi-agent peer review
3. Copy/present relevant sections to user

## Pipeline Stages (23 Total)

### Phase A: Research Scoping
- Stage 1: TOPIC_INIT
- Stage 2: PROBLEM_DECOMPOSE

### Phase B: Literature Discovery
- Stage 3: SEARCH_STRATEGY
- Stage 4: LITERATURE_COLLECT
- Stage 5: LITERATURE_SCREEN [gate]
- Stage 6: KNOWLEDGE_EXTRACT

### Phase C: Knowledge Synthesis
- Stage 7: SYNTHESIS
- Stage 8: HYPOTHESIS_GEN

### Phase D: Experiment Design
- Stage 9: EXPERIMENT_DESIGN [gate]
- Stage 10: CODE_GENERATION
- Stage 11: RESOURCE_PLANNING

### Phase E: Experiment Execution
- Stage 12: EXPERIMENT_RUN
- Stage 13: ITERATIVE_REFINE
- Stage 14: RESULT_ANALYSIS
- Stage 15: RESEARCH_DECISION

### Phase F: Analysis & Decision
- Stage 16: PAPER_OUTLINE
- Stage 17: PAPER_DRAFT
- Stage 18: PEER_REVIEW
- Stage 19: PAPER_REVISION

### Phase G: Paper Writing
- Stage 20: QUALITY_GATE [gate]
- Stage 21: KNOWLEDGE_ARCHIVE
- Stage 22: EXPORT_PUBLISH
- Stage 23: CITATION_VERIFY

## Hardware Awareness

AutoResearchClaw auto-detects:
- NVIDIA CUDA (GPU)
- Apple MPS (M1/M2/M3)
- CPU-only fallback

Adapts code generation, imports, and experiment scale accordingly.

## Quality Features

- **Real Citations**: OpenAlex, Semantic Scholar, arXiv - no hallucinated references
- **4-Layer Verification**: arXiv ID → CrossRef DOI → Semantic Scholar → LLM relevance
- **Multi-Agent Debate**: Hypothesis generation, result analysis, peer review
- **Self-Healing**: NaN/Inf detection, automatic code repair
- **Conference Templates**: NeurIPS, ICLR, ICML support

## OpenClaw Bridge Integration (Optional)

Enable in `config.arc.yaml`:
```yaml
openclaw_bridge:
  use_cron: true          # Scheduled research runs
  use_message: true       # Progress notifications (Discord/Slack/Telegram)
  use_memory: true        # Cross-session knowledge persistence
  use_sessions_spawn: true # Parallel sub-sessions
  use_web_fetch: true     # Live web search during literature review
  use_browser: false      # Browser-based paper collection
```

## MetaClaw Integration (Optional)

For cross-run learning:
```yaml
metaclaw_bridge:
  enabled: true
  skills_dir: "~/.metaclaw/skills"
  lesson_to_skill:
    enabled: true
    min_severity: "warning"
    max_skills_per_run: 5
```

## Troubleshooting

### Installation Issues
```bash
# Check Python version
python3 --version  # Requires 3.8+

# Install dependencies
pip install -r requirements.txt
```

### LLM API Errors
- Verify `OPENAI_API_KEY` is set
- Check API endpoint is accessible
- Fallback models configured correctly

### Sandbox Issues
- Ensure Python path is correct: `.venv/bin/python`
- Check allowed imports in config
- Adjust memory limits if needed

### Literature Collection Failures
- Check internet connectivity
- Semantic Scholar API key optional (higher rate limits)
- OpenAlex should work without API key

## Advanced Usage

### Specify Research Domains
```bash
researchclaw run --topic "Your topic" --domains ml,nlp --auto-approve
```

### Target Specific Conference
```yaml
export:
  target_conference: "neurips_2025"  # neurips_2025 | iclr_2026 | icml_2026
```

### Custom Prompts
```yaml
prompts:
  custom_file: "custom_prompts.yaml"
```

## Resources

- **GitHub**: https://github.com/aiming-lab/AutoResearchClaw
- **Integration Guide**: See AutoResearchClaw docs/integration-guide.md
- **Testing Guide**: See AutoResearchClaw docs/TESTER_GUIDE.md
- **Discord**: https://discord.gg/u4ksqW5P

## Comparison with Superpowers

- **ResearchClaw**: Academic research, literature review, paper writing, experimental validation
- **Superpowers**: Software development, TDD, code review, production code

Use ResearchClaw for research/paper generation. Use Superpowers for production software implementation. They complement each other when researching then implementing findings.