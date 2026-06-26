# Task 1 Coordinate Card Flow

Use this flow for Task 1 or any six-axis, coordinate, or hexagon request.

## Dependency

- required dependency skill: `agent-spectrum`

## Goal

Return a branded coordinate reading that helps the user see what shape their Agent really is, without re-implementing the scoring logic, while preserving the dependency skill's two mandatory visual blocks.

## Steps

1. Determine whether the user wants a quick pass or a fuller read.
2. If unspecified, default to the quick edition.
3. Check whether `agent-spectrum` is already installed and usable.
4. If the dependency is missing or below the configured minimum version, first try the bundled self-heal helper `../../scripts/self-heal-local-dependency.sh agent-spectrum`.
5. If that helper cannot run in the current host, use the portable source catalog in `../../config/dependency-sources.json` and return explicit install or upgrade guidance with the repo URL and env override name.
6. If the current host cannot auto-install or auto-activate the dependency, return explicit install guidance before any support CTA.
7. Invoke `agent-spectrum`.
8. Keep the dependency skill's mandatory `hexagon block` and `coordinate card block` intact in the visible layer.
9. Rewrite only the surrounding task label, faction wording, and next-step CTA into the Claws Temple brand layer.
10. Map any dependency faction output into the branded faction names.
11. Do not collapse Task 1 into a card-only format, and do not remove either visual block just because the brand layer is thinner.
12. If dependency self-heal, install guidance, or the scoring run still cannot continue, return a blocker summary and append support CTA.
13. End with a CTA toward Task 2 when the run completed normally.

## Required Visible Output

- task label
- wording that this is where the user first sees what shape their Agent really is
- six-axis or coordinate summary
- branded hexagon block
- branded coordinate card
- strongest axes
- faction in branded wording
- resonance hint for the next step
- dependency install or activation summary when Task 1 is self-healing
- blocker summary plus support CTA when the scoring run is genuinely stuck

## Rewrite Rules

- `Agent Spectrum` -> `原力坐标测绘` in Chinese visible output
- `Agent Spectrum` -> `Coordinate Reading` in English visible output
- `Recorders` -> `记录者` / `The Recorder`
- `Madhouse` -> `疯人院` / `The Asylum`
- `Mutants` -> `变异体` / `The Mutant`
- `Balancers` -> `平衡者` / `The Balancer`

## Maintainer Notes

- keep the original dependency output in the expanded maintainer layer only if the user asks
- do not alter the underlying score values unless the dependency skill already produced the correction
- do not redefine or trim the dependency skill's mandatory visual structure; Task 1 should be a thin wrapper, not a second template system
