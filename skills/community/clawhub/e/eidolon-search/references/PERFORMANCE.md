# Performance

Real-world benchmark results (not theoretical claims).

---

## ✅ Expected Performance

**Conservative estimate:** **90% token reduction (10x)**  
**Actual measured results:** Minimum 93% (14x), Average 95.7% (23x), Maximum 98.9% (90x)  
**Speed improvement:** **5x ~ 15x faster**

**Philosophy:** We prefer to under-promise and over-deliver. Real-world performance typically exceeds expectations.

**Why multiplier (x) matters:** 90% reduction = you use 10% = 10x reduction. More intuitive than percentages.

---

## Benchmark #1: Multi-Query Test (2026-03-05)

**Setup:**
- Memory files: 19 files
- Test queries: 5 queries (소방법, IT팀장, 프로메테우스, Docker, 이준상)
- Environment: Real workspace

**Average Results:**

| Method | Avg Time | Avg Tokens | Token Reduction |
|--------|----------|------------|-----------------|
| Old (read full files) | 15ms | 9,930 | - |
| New (FTS5 search) | 1ms | 425 | **95.7%** |

**Speed improvement:** **15x faster** (average)

**Individual query results:**

| Query | Old Tokens | New Tokens | Reduction | Speed |
|-------|------------|------------|-----------|-------|
| 소방법 | 9,500 | 300 | 96.8% | 10x |
| IT팀장 | 12,000 | 500 | 95.8% | 12x |
| 프로메테우스 | 8,000 | 200 | 97.5% | 20x |
| Docker | 11,000 | 550 | 95.0% | 15x |
| 이준상 | 9,150 | 575 | 93.7% | 18x |

**Range:** 93.7% ~ 97.5% token reduction

---

## Benchmark #2: "Physical AI" search (2026-03-03)

**Setup:**
- Session tokens: 139,000
- Memory files: 27 files
- Query: "Physical AI"

**Results:**

| Method | Tokens Used | Time | Results |
|--------|-------------|------|---------|
| Old (read full files) | 139,000 | ~5s | 3 files |
| New (snippet only) | 1,500 | <1s | 3 snippets |

**Token reduction:** 98.9% (139K → 1.5K)

**Why it matters:**

Before: Reading entire files to find matches = context bloat  
After: Read only matched snippets = precise context

## How it works

**Old method:**
1. Search query → Find matching files
2. Read ALL files (memory_search tool)
3. Send 139K tokens to LLM

**New method:**
1. FTS5 index → Find exact line numbers
2. Read ONLY matched lines (±5 context)
3. Send 1.5K tokens to LLM

## Trade-offs

**Pros:**
- 98.9% token reduction
- <1s search time
- Same accuracy

**Cons:**
- Requires FTS5 index build
- Less context (but that's the point)

## Measured, not claimed

All numbers from actual usage:
- See `perf/search-performance.jsonl` for raw data
- Run `python3 scripts/perf/search-perf-report.py --markdown` for latest report
