# Scoring Rubric

## General Rules

- Score each category as percentage of its max points
- **Full credit**: All critical items pass, most major items pass
- **Partial credit**: Critical items pass, some major fail
- **Minimal credit**: Some critical items fail
- **Zero credit**: Most critical items fail or category absent

## Per-Category Scoring

### 1. Semantic HTML (15 pts)
| Score | Criteria |
|-------|----------|
| 13-15 | Proper hierarchy, all landmarks, semantic elements throughout |
| 9-12 | Hierarchy correct, most landmarks, some unnecessary divs |
| 5-8 | Some semantic elements, significant div soup, heading issues |
| 1-4 | Mostly divs, few semantic elements |
| 0 | No semantic HTML |

### 2. ARIA & Accessibility (15 pts)
| Score | Criteria |
|-------|----------|
| 13-15 | All accessible names present, proper roles/states, live regions correct |
| 9-12 | Most elements accessible, minor gaps |
| 5-8 | Many missing labels, inconsistent ARIA |
| 1-4 | Widespread issues |
| 0 | No ARIA, no alt text, no labels |

### 3. Structured Data (15 pts)
| Score | Criteria |
|-------|----------|
| 13-15 | Comprehensive JSON-LD, correct type, all key properties, breadcrumbs |
| 9-12 | JSON-LD with correct type, some properties missing |
| 5-8 | Basic JSON-LD, incomplete or wrong type |
| 1-4 | Malformed or minimal |
| 0 | None |

### 4. Form Readability (10 pts)
| Score | Criteria |
|-------|----------|
| 9-10 | All labeled, grouped, autocomplete, error handling |
| 6-8 | Most labeled, some grouping, basic errors |
| 3-5 | Labels missing, no grouping, placeholder-only |
| 1-2 | Most inputs lack labels |
| 0 | N/A (no forms) or completely inaccessible |

### 5. Navigation Clarity (10 pts)
| Score | Criteria |
|-------|----------|
| 9-10 | Semantic nav, aria-current, skip link, breadcrumbs + structured data |
| 6-8 | Nav present, most covered, minor gaps |
| 3-5 | Basic nav, missing semantic markup or aria |
| 1-2 | Nav exists but not machine-readable |
| 0 | No navigation structure |

### 6. Automation Attributes (10 pts)
| Score | Criteria |
|-------|----------|
| 9-10 | Comprehensive data-testid, consistent naming, entity tagging |
| 6-8 | data-testid on most interactive elements |
| 3-5 | Some data-testid, inconsistent |
| 1-2 | Very few |
| 0 | None |

### 7. CSS Selector Stability (5 pts)
| Score | Criteria |
|-------|----------|
| 5 | Meaningful stable classes throughout |
| 3-4 | Mostly meaningful, some generated |
| 1-2 | Mixed |
| 0 | All generated or absent |

### 8. API Discoverability (10 pts)
| Score | Criteria |
|-------|----------|
| 9-10 | Canonical, pagination links, API docs, alternates |
| 6-8 | Canonical, some link relations |
| 3-5 | Canonical only |
| 1-2 | No link relations, URLs somewhat predictable |
| 0 | No discoverability |

### 9. Meta & Machine Signals (10 pts)
| Score | Criteria |
|-------|----------|
| 9-10 | Full meta, OG complete, lang, proper robots |
| 6-8 | Basic meta, partial OG |
| 3-5 | Minimal meta (charset + viewport) |
| 1-2 | Missing critical meta |
| 0 | No meta |

## Grade Scale

| Grade | Range | Meaning |
|-------|-------|---------|
| A | 90-100 | Excellent — highly agent-friendly |
| B | 80-89 | Good — works well, some improvements possible |
| C | 70-79 | Acceptable — agents can use with effort |
| D | 60-69 | Below average — significant barriers |
| F | <60 | Poor — agents will struggle |
