# Web Performance Optimization

## Overview

Website performance optimization is a scalar eval domain — you have a concrete number (load time, Lighthouse score, Core Web Vitals) and you want to minimize/maximize it. The optimization loop runs Lighthouse or custom perf scripts as the metric command.

## Setup

```bash
# Minimize load time
./auto-optimizer.sh \
  --eval-mode scalar \
  --metric "lighthouse https://yoursite.com --output json 2>/dev/null | jq '.audits[\"interactive\"].numericValue'" \
  --file ./src/pages/index.js \
  --goal minimize \
  --budget 20 \
  --session "web-perf"

# Maximize Lighthouse score
./auto-optimizer.sh \
  --eval-mode scalar \
  --metric "lighthouse https://yoursite.com --output json 2>/dev/null | jq '.categories.performance.score * 100'" \
  --file ./next.config.js \
  --goal maximize \
  --budget 15 \
  --session "lighthouse-score"
```

## Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|-----------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4s | > 4s |
| FID (First Input Delay) | < 100ms | 100–300ms | > 300ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |
| TTFB (Time to First Byte) | < 200ms | 200–500ms | > 500ms |

## High-Leverage Optimization Targets

The loop should focus on these files (each has large impact per change):

1. **`next.config.js` / `vite.config.js`** — bundle splitting, image optimization, caching headers
2. **Main page component** — code splitting, lazy loading, above-the-fold prioritization
3. **CSS/styling** — critical CSS inlining, font loading strategy
4. **Image handling** — next/image configuration, WebP conversion, lazy loading
5. **API routes** — caching strategy, response compression

## Metric Commands

```bash
# Lighthouse performance score (0-100)
lighthouse $URL --output json --quiet | jq '.categories.performance.score * 100'

# Time to Interactive (ms)
lighthouse $URL --output json --quiet | jq '.audits.interactive.numericValue'

# Custom: measure API response time
curl -w "%{time_total}" -o /dev/null -s https://api.yoursite.com/endpoint

# Custom: measure bundle size
du -k dist/assets/*.js | awk '{sum += $1} END {print sum}'
```

## Binary Evals for Pre-Deploy Checks

Before deploying, use binary evals to catch obvious quality regressions:

```markdown
# Web Quality Evals

1. Does the page load without JavaScript errors in the browser console? → yes/no
2. Is the Lighthouse performance score above 80? → yes/no
3. Do all images have alt text? → yes/no
4. Is the page mobile-responsive (no horizontal scroll on 375px)? → yes/no
5. Does the page load in under 3 seconds on a simulated 4G connection? → yes/no
```

## Historical Benchmark

Example of what the loop achieves:
- Starting Lighthouse score: 42
- After 67 iterations: score 89 (load time: 1100ms → 67ms)
- Key improvements: image optimization, code splitting, cache headers, font loading

The hypothesis log was critical here — early iterations tried CSS minification repeatedly. After logging that it had minimal impact (score +1 per attempt), the loop shifted to higher-impact changes (code splitting: +8, image optimization: +15).
