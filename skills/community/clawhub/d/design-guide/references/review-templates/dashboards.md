# Dashboard Review Template

Use for monitoring, analytics, operational health, business intelligence, and decision dashboards.

## Scope Inputs

- Decisions the dashboard must support.
- Metric owners, calculation definitions, refresh cadence, and comparison periods.
- Alert thresholds, drill-down paths, and required roles.

## Evidence Checklist

- KPI hierarchy reflects decision importance rather than visual novelty.
- Every metric exposes unit, time range, freshness, source, and comparison basis.
- Charts use an appropriate encoding, legible axes, consistent color semantics, and accessible alternatives.
- Filters declare whether they apply globally or locally and preserve/share state when required.
- Anomalies connect to explanation and action, not only decorative color.
- Loading, partial, stale, delayed, missing, and conflicting data remain distinguishable.

## High-Risk Findings

- `P0`: a chart or KPI can cause a materially wrong decision because its denominator, time window, or freshness is hidden.
- `P1`: users must manually reconcile panels with incompatible filters or units.
- `P2`: visual rhythm, annotation, density, or chart ink can be simplified.

## Acceptance Examples

- A user can explain what changed, compared with when, and whether the data is current.
- Global filter changes are visibly reflected in every affected panel.
- Color is never the sole carrier of status or series identity.
- Empty data is not rendered as a valid zero.
