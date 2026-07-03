# EVEZ OSINT Suspect Inference Matrix

## Description
Isolate and identify suspect inference networking matrices. Compute statistical probabilities of likely crimes using eigenforensic spectral analysis (AEMDAS pipeline).

## When to Use
- Building suspect networks from OSINT evidence
- Computing crime probabilities for multiple suspects
- Generating intervention priority reports
- Analyzing police misconduct patterns
- Civil rights disclosure cases

## How to Use

### Run the engine
```bash
cd /home/openclaw/.openclaw/workspace/evez-osint-engine
python3 core/suspect_matrix.py
```

### CLI
```bash
python3 core/osint_cli.py run -i input.json -o report.md -f markdown
python3 core/osint_cli.py analyze --suspect-id <id> --name <name> --role officer --org "Evanston PD"
```

### Python API
```python
from core.suspect_matrix import SuspectInferenceEngine, SuspectNode, NetworkEdge
engine = SuspectInferenceEngine()
# ... add suspects, edges, run pipeline
```

## Output
- JSON report: `reports/suspect-matrix-report.json`
- Markdown report: `reports/suspect-matrix-report.md`

## Eigenvalue Constants
- Phi = 0.973 (coherence ceiling)
- eta* = 0.03 (irreducible uncertainty floor)
- r = 0.45 (criticality ratio)
- lambda_dom = -0.333 (dominant negative eigenvalue)

All probabilities bounded: eta* <= P <= 0.95.
