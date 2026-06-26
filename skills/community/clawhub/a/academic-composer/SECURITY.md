# Security & Intended Use

## Academic Integrity

This skill is designed for **research and learning purposes only**.

Permitted uses:
- Personal research drafts and exploration
- Studying how to construct evidence-based arguments
- Learning proper citation formatting (APA, MLA, Chicago)
- Generating reference-based outlines to guide your own writing

**NOT permitted:**
- Submitting AI-generated essays as your own original work for academic assessment
- Bypassing academic integrity policies
- Any form of academic dishonesty

Users are solely responsible for ensuring their use complies with their institution's academic honesty policies. The authors of this skill accept no liability for misuse.

## Permissions

| Permission | Purpose |
|------------|---------|
| `shell` | Runs `scholar.py` (source metadata search), `pipeline.py` (local style analysis), `measure.py` (local pattern scoring) |
| `network` | `scholar.py` queries `api.semanticscholar.org` — **read-only metadata only** (title, authors, DOI, abstract). No essay content is sent. |

## Data Flow

| Component | Network | Data Sent |
|-----------|---------|-----------|
| `scholar.py` | api.semanticscholar.org | Search keywords only (no essay content) |
| `pipeline.py` | **None** | Fully local analysis |
| `measure.py` | **None** | Fully local analysis |
| LLM (essay generation & rewriting) | **Depends on host** | See note below |

**Important — LLM data flow:**
Essay generation and rewriting are performed by the orchestrating LLM (the agent's language model). If the agent uses a **remote model provider** (e.g., cloud-hosted API), essay content will be transmitted to that provider as part of the LLM conversation. If the agent uses a **local model** (e.g., on-device inference), no essay content leaves the machine. Users should check their agent's model configuration to understand where essay content is processed.

**Local scripts (`pipeline.py`, `measure.py`, `scholar.py`) never transmit essay content to any external service.** These scripts only perform local regex matching, spaCy dependency parsing, and Semantic Scholar metadata queries.

**Process-level privacy:**
Essay text is passed between scripts via file path or stdin (never as a CLI argument) to avoid exposure in process listings, system logs, or shell history.

## Credentials

This skill requires **no credentials**. There are no API keys, passwords, or tokens of any kind.

## Dependencies

| Library | Purpose | Network at runtime |
|---------|---------|-------------------|
| `spaCy en_core_web_sm` | Dependency parsing for MDD/ADD | None (local model, pre-installed by user) |
| `urllib` (stdlib) | Semantic Scholar API calls | Read-only metadata |

spaCy model must be installed manually by the user:
```bash
python -m spacy download en_core_web_sm
```
The skill does **not** auto-download models at runtime.

## Reporting

Report security issues at https://github.com/kevin0818-lxd/academic-composer/issues.
