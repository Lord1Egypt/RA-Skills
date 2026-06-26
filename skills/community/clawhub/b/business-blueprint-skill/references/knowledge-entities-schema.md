# Knowledge Entities Schema (v2 Minimal)

This document defines the field specification for knowledge entities in
``library.knowledge``. The schema is intentionally minimal: core fields are
strictly validated, optional fields are documented but not enforced. See
``domain-knowledge-design-v2.md`` for the rationale.

## Entity Overview

| Plural | entityType value | Example |
|--------|------|---------|
| ``painPoints`` | ``painPoint`` | ROI 不稳、素材疲劳 |
| ``strategies`` | ``strategy`` | 测款节奏策略、动态出价 |
| ``rules`` | ``rule`` | Facebook 政策红线 |
| ``metrics`` | ``metric`` | ROAS 基准 |
| ``practices`` | ``practice`` | 素材迭代周期 |
| ``pitfalls`` | ``pitfall`` | 过度依赖单一平台 |

User-defined entity-type arrays are allowed (e.g. ``caseStudies``). The
validator does not check array names.

## Core Fields (Strictly Validated)

All knowledge entities must have:

| Field | Type | Rule |
|-------|------|------|
| ``id`` | string | Format ``{prefix}-{seq}`` (e.g. ``pain-001``); globally unique |
| ``name`` | string | Non-empty |
| ``entityType`` | string | Non-empty |

## Optional Fields (Documented, Not Validated)

Recommended fields per entity type. Validator does NOT enforce these — soft
schema is deferred to Phase 3.

### painPoint

- ``description``, ``severity`` (low/medium/high/critical), ``level`` (1/2/3)
- ``relatedCapabilityIds``, ``solutions``, ``impactArea``

### strategy

- ``description``, ``severity``, ``level``
- ``applicableCapabilityIds``, ``prerequisites``, ``successRate``

### rule

- ``description``, ``severity``, ``platform``, ``penalty``, ``policyUrl``

### metric

- ``value``, ``unit``, ``benchmarkContext``, ``calculationMethod``

### practice

- ``description``, ``frequency``, ``successMetric``, ``difficulty``

### pitfall

- ``description``, ``severity``, ``avoidanceStrategy``, ``realCase``

### All entity types

- ``_selfCheck``: ``{passed: [...], questions: [...]}`` — see
  ``knowledge-self-check.md``

User-defined fields are allowed. Validator passes them through unchanged.

## Relations

Each relation: ``{id, type, from, to, label?}``. Validator enforces:

- ``from`` and ``to`` IDs exist somewhere in ``library``
- ``type`` is in the recognised whitelist (warning only — unknown types are
  permitted)

### Knowledge internal relation types

| type | from → to | semantics |
|------|-----------|-----------|
| ``solves`` | strategy → painPoint | Strategy addresses pain point |
| ``prevents`` | practice → pitfall | Practice avoids pitfall |
| ``measures`` | metric → strategy | Metric tracks strategy effectiveness |
| ``enforces`` | rule → strategy | Rule constrains strategy |
| ``requires`` | strategy → practice | Strategy depends on practice |
| ``causes`` | pitfall → painPoint | Pitfall causes pain point |

### Cross-type relation types (knowledge → architecture)

| type | from → to | semantics |
|------|-----------|-----------|
| ``impacts`` | painPoint → capability | Pain affects capability |
| ``supports`` | strategy → capability | Strategy supports capability |
| ``enforcedBy`` | rule → system | Rule constrains system |
| ``measuredBy`` | metric → system | Metric monitors system |

Direction is single-arrow: knowledge entities may point to architecture
entities, but architecture entities should not point to knowledge entities.

Semantic validity (e.g. ``measures`` must be metric→strategy specifically) is
NOT validated in v2. Recommend it via documentation only.

## Naming Conventions (Soft Recommendations)

- ``painPoint``: focus on the problem — ``"ROI 不稳"`` not ``"缺乏 ROI 监控系统"``
- ``strategy``: focus on the method — ``"测款节奏策略"`` not ``"优化 ROI"``
- ``rule``: source + content — ``"Facebook 广告政策红线"``
- ``metric``: indicator + benchmark — ``"ROAS 基准"``
- ``practice``: practice content — ``"素材迭代周期"``
- ``pitfall``: pitfall behaviour — ``"过度依赖单一平台"``
