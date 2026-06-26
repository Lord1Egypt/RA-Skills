"""Domain detection — maps research topic to academic domain & venue context."""

from __future__ import annotations

_DOMAIN_KEYWORDS: dict[str, tuple[list[str], str, str]] = {
    # domain_id: (keywords, display_name, top_venues)
    "ml": (
        ["machine learning", "deep learning", "neural network", "transformer",
         "reinforcement learning", "GAN", "diffusion model", "LLM", "language model",
         "computer vision", "NLP", "representation learning", "self-supervised",
         "federated learning", "meta-learning", "continual learning", "few-shot",
         "knowledge distillation", "attention mechanism", "fine-tuning", "RLHF",
         "vision transformer", "ViT", "BERT", "GPT", "autoencoder"],
        "machine learning",
        "NeurIPS, ICML, ICLR",
    ),
    "physics": (
        ["quantum", "thermodynamic", "electrodynamic", "particle physics",
         "condensed matter", "statistical mechanics", "cosmology", "astrophysics",
         "plasma", "optics", "photonics", "relativity", "gravitational",
         "PDE", "PINN", "physics-informed", "Burgers", "Navier-Stokes",
         "Darcy flow", "Schrödinger", "scientific computing", "operator learning",
         "neural operator", "Fourier neural", "DeepONet"],
        "physics",
        "Physical Review Letters, Nature Physics, JHEP",
    ),
    "chemistry": (
        ["molecular", "catalysis", "polymer", "organic chemistry", "inorganic",
         "electrochemistry", "spectroscopy", "crystallography", "drug discovery",
         "protein folding", "computational chemistry", "DFT", "force field"],
        "chemistry",
        "JACS, Nature Chemistry, Angewandte Chemie",
    ),
    "economics": (
        ["econometric", "macroeconomic", "microeconomic", "game theory",
         "market", "fiscal policy", "monetary", "behavioral economics",
         "causal inference", "panel data", "regression discontinuity",
         "instrumental variable", "supply chain", "auction"],
        "economics",
        "AER, Econometrica, QJE, Review of Economic Studies",
    ),
    "mathematics": (
        ["theorem", "proof", "prove", "conjecture", "topology", "algebra",
         "number theory", "combinatorics", "differential equation",
         "stochastic process", "functional analysis", "manifold",
         "Riemannian", "category theory", "graph theory",
         "neural ODE", "dynamical system", "Lorenz", "chaotic",
         "Lyapunov", "attractor", "ODE solver", "trajectory prediction",
         "mathematical formulation", "mathematical proof", "derivation",
         "Brownian motion", "branching process", "Galton-Watson",
         "Markov chain", "martingale", "ergodic", "convergence theorem",
         "marginal distribution", "extinction probability", "Feynman-Kac",
         "measure theory", "Hilbert space", "Banach space", "operator theory",
         "variational", "Euler-Lagrange", "calculus of variations"],
        "mathematics",
        "Annals of Mathematics, Inventiones Mathematicae, JAMS",
    ),
    "engineering": (
        ["robotics", "control system", "signal processing", "FPGA",
         "embedded system", "VLSI", "antenna", "fluid dynamics", "CFD",
         "finite element", "structural", "mechatronics", "autonomous"],
        "engineering",
        "IEEE Transactions, ASME journals, AIAA",
    ),
    "biology": (
        ["genomics", "proteomics", "transcriptomics", "CRISPR",
         "single-cell", "phylogenetic", "ecology", "neuroscience",
         "bioinformatics", "sequencing", "gene expression", "epigenetic"],
        "biology",
        "Nature, Science, Cell, PNAS",
    ),
}


def _detect_domain(topic: str, domains: tuple[str, ...] = ()) -> tuple[str, str, str]:
    """Detect research domain from topic string and config domains.

    Returns ``(domain_id, display_name, top_venues)``.
    Falls back to ``("ml", "machine learning", "NeurIPS, ICML, ICLR")``.
    """
    # If user explicitly specified domains, check them first
    for d in domains:
        d_lower = d.lower().strip()
        for did, (kws, dname, venues) in _DOMAIN_KEYWORDS.items():
            if d_lower in (did, dname) or any(k in d_lower for k in kws[:3]):
                return did, dname, venues

    # Auto-detect from topic text
    topic_lower = topic.lower()
    best_did, best_score = "ml", 0
    # BUG-101: Explicit theoretical intent words boost non-empirical domain scores.
    # Topics like "derive the mathematical formulation of X diffusion model"
    # should classify as math, not ML, even if "diffusion model" is an ML keyword.
    _theoretical_intent = any(
        w in topic_lower
        for w in ("derive", "prove", "mathematical formulation",
                  "mathematical proof", "formal proof", "formalism")
    )
    for did, (kws, dname, venues) in _DOMAIN_KEYWORDS.items():
        score = sum(1 for k in kws if k.lower() in topic_lower)
        # Boost non-empirical domains when theoretical intent is detected
        if _theoretical_intent and did in ("mathematics", "physics", "economics"):
            score += 1
        if score > best_score:
            best_score = score
            best_did = did

    did = best_did
    _, dname, venues = _DOMAIN_KEYWORDS[did]
    return did, dname, venues


def _is_ml_domain(domain_id: str) -> bool:
    """Check if the detected domain is ML/AI."""
    return domain_id == "ml"
