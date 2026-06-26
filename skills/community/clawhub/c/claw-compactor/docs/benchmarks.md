# Claw Compactor Benchmark Results
> Comprehensive evaluation of Claw Compactor's token compression performance against LLMLingua-2 and other baselines.

## Methodology
All benchmarks use the same evaluation pipeline:

1. **Input:** Real-world AI agent workspace content (DevOps, trading, ML, sysadmin, mixed)
2. **Compression:** Each tool compresses input at target rates (0.3 and 0.5)
3. **Evaluation:** ROUGE-L (longest common subsequence) and IR-F1 (information retrieval) metrics
4. **Baseline:** Original uncompressed text as reference

ROUGE-L measures how well the compressed output preserves the meaning and content of the original. Higher is better.

## Head-to-Head: Claw Compactor vs LLMLingua-2

### Compression Rate = 0.3 (aggressive)
**ROUGE-L**, Claw Compactor=**0.653**, LLMLingua-2=0.346, Delta=**+88.2%**
Token reduction, Claw Compactor=70%, LLMLingua-2=70%, Delta=-
LLM cost, Claw Compactor=$0, LLMLingua-2=~$0.02/call, Delta=-
Latency, Claw Compactor=<50ms, LLMLingua-2=~300ms, Delta=**6x faster**

### Compression Rate = 0.5 (moderate)
| **ROUGE-L** | **0.723** | 0.570 | **+26.8%** |
| Token reduction | 50% | 50% | - |
| Latency | <50ms | ~250ms | **5x faster** |

## Why Does Claw Compactor Score Higher?
**Claw Compactor preserves semantic structure.** Instead of randomly dropping tokens (like perplexity-based methods), it uses rule-based deduplication, dictionary encoding, and structured compression that keeps the logical flow intact.

**LLMLingua-2 uses perplexity scoring** to decide which tokens to drop. This can remove tokens that are syntactically unimportant but semantically critical - especially in technical content with code snippets, IP addresses, and configuration values.

## Full Benchmark Matrix

### Deterministic Layers (L1–L5) vs Engram (L6)
| **RuleCompressor (L1–L5)** | 9.0% | **0.923** | **0.958** | ~6ms | 0 |
| **Engram (L6)** | **87.5%** | 0.038 | 0.414 | ~35s | 2 |
| RandomDrop baseline | 21.5% | 0.852 | 0.911 | ~0ms | 0 |

**Interpretation:**
- **L1–L5** are best for lossless/near-lossless prompt compression with maximum fidelity
- **Engram (L6)** is best for long-term memory compression where 87.5% reduction is needed
- Engram's low ROUGE-L reflects semantic restructuring, not information loss - the information is preserved in a different format

## Real-World Scenarios
| DevOps session transcript | 127,000 | 3,810 | **97%** | 1.2s |
| Trading bot memory | 45,000 | 22,500 | 50% | 0.3s |
| ML experiment notes | 32,000 | 14,400 | 55% | 0.2s |
| Sysadmin runbook | 18,000 | 10,800 | 40% | 0.1s |
| Mixed workspace (first run) | 167,821 | 50,346 | **70%** | 0.8s |

## Test Data
Benchmarks use 5 representative samples from real AI agent workspaces:

1. `sample_01_devops.json` - CI/CD pipeline debugging session
2. `sample_02_trading.json` - Crypto trading bot configuration
3. `sample_03_ml_short.json` - Machine learning experiment notes
4. `sample_04_mixed_long.json` - Multi-topic long session
5. `sample_05_sysadmin.json` - System administration runbook

All samples are included in `benchmark/data/` for reproducibility.

## Reproducing Benchmarks
```bash
cd claw-compactor

# Run the full benchmark suite
python3 benchmark/run_benchmark.py

# View results
cat benchmark/results/benchmark_results.json

# Generate human-readable report
python3 benchmark/report.py
```

## Comparison with Other Approaches

### vs SelectiveContext
SelectiveContext uses self-information to select important sentences. Claw Compactor operates at a finer granularity (line-level, token-level) and includes lossless layers that SelectiveContext lacks.

### vs Manual Prompt Engineering
Manual prompt shortening is labor-intensive and doesn't scale. Claw Compactor automates the process with consistent, reproducible results across any workspace.

### vs Prompt Caching Alone
Prompt caching (e.g., Anthropic's cache) reduces cost-per-token but doesn't reduce token count. Claw Compactor + caching = compound savings (50% fewer tokens × 90% cache discount = 95% savings).

## Links
- [Full benchmark data](../benchmark/results/benchmark_results.json), [Benchmark runner source](../benchmark/run_benchmark.py), [Main README](../README.md)