# Integrity Audit

Run integrity checks before cosmetic redesign. The most dangerous charts often look polished.

## Core questions

1. What is the claim or comparison?
2. What is the numerical effect in the data?
3. What visual effect does the graphic show?
4. Are the visual and numerical effects proportional?
5. What context would change the interpretation: denominator, sample size, time window, baseline, uncertainty, source, transformation, inflation, population, exposure, or filter?

## Baselines and scales

Bars and columns encode magnitude by length, so a visible zero baseline is usually required. If the meaningful story is deviation from a reference, use a dot plot, interval plot, slope chart, or difference chart instead of a truncated bar.

Line charts and scatterplots do not always require zero baselines, but the chosen range must not exaggerate trivial variation or hide important variation. Label transformations, log scales, index bases, breaks, and independent panel scales.

## Lie factor

When a visual effect can be measured, compute:

`lie factor = visual percent change / data percent change`

Values near 1 are visually proportional. Large departures suggest exaggeration or understatement. Opposite signs indicate a severe reversal of meaning. Use `scripts/lie_factor.py` or the lie-factor fields in `assets/chart-spec-template.json`.

## Area, volume, and pictorial scaling

If a one-dimensional quantity is encoded with area or volume, check whether the displayed area or volume is actually proportional to the number. Scaling both height and width by the data value squares the apparent effect; scaling height, width, and depth cubes it.

Prefer position or length for precise quantitative comparison unless the area is the actual measured phenomenon.

## Denominators and exposure

Counts often need denominators. Crime, defects, cases, emissions, failures, claims, clicks, and incidents may require rates per population, units, time, exposure, tests, or opportunities. Maps are especially prone to confusing raw counts with population density.

## Context and omitted comparisons

A graphic may distort by omission. Check whether the time window, comparison group, benchmark, seasonal cycle, historical range, or uncertainty range is too narrow for the claim. Add context where it changes interpretation.

## Uncertainty and sample size

Show uncertainty when data are estimates, samples, forecasts, simulations, measurements, model outputs, or small-n comparisons. Use intervals, bands, raw points, sample sizes, sensitivity panels, or notes. Label what the interval means.

## Checklist for existing charts

- Axis labels and units are visible.
- Baseline and scale choices match the encoding.
- Same scales are used across comparable panels, unless clearly labeled otherwise.
- Source, sample, filters, denominator, and time window are available.
- Visual dimensions are proportional to numerical quantities.
- Aggregation does not hide distribution or outliers central to the claim.
- Color is not the only way to identify important groups.
- Decorative marks do not overpower evidence.
