# Human-Perceived Semantic Complexity and Budget

## Contents

- Core principle
- Qualitative scoring
- Target selection
- Identity anchors
- Factor definitions
- Score bands and semantic budgets
- Compression priority
- Budget enforcement
- Anti-generic identity test
- Compression stopping rule

Use this reference to score a source image, set an output budget, and decide what must be removed.

## Core principle

Human observers compress repeated texture and repeated objects into perceptual groups. Count independently meaningful systems, not literal pixels or object instances.

When repeated elements form one semantic system through perceptual grouping, preserve the group's overall contour, arrangement order, proportional relationships, dominant rhythm, and identity-bearing asymmetries rather than reconstructing every visible instance.

Examples:

- many meat slices can become one food mass;
- many leaves can become one canopy;
- many windows can become one facade rhythm;
- several distant people can become one crowd silhouette;
- many buildings can become one skyline system.

## Qualitative scoring

Estimate complexity from entity diversity, relationship density, depth complexity, focal competition, and surface detail. Use the score bands below as qualitative budgets, not as a precise numeric measurement.

## Target selection

Use the user's requested target when supplied. Otherwise:

- default to a maximum of 6 out of 10;
- aim for 3 to 5 for a simple object or single figure;
- aim for 5 to 6 for a multi-subject or environmental scene;
- use a target above 6 only when the user explicitly requests a denser reconstruction.

Choose the lowest score within the applicable range that preserves recognizability and the required spatial identity.

Apply the selected score band below as the authoritative semantic-system and focal budget.

## Identity anchors

Choose three to six facts that make the reference specifically recognizable rather than merely recognizable as a category. Favor distinctive silhouette or asymmetry; subject relationships, relative scale, overlap, direction, pose, orientation, openings, negative space, identity-bearing attributes, value hierarchy, and one recognizable environmental shape. HSB palette roles are assigned by rule, not extracted from the source; they do not count as reference-specific identity anchors. Preserve relationships before surface detail.

## Factor definitions

### Semantic entity diversity

Judge how many different independently meaningful groups a human must recognize.

Low examples:

- one object;
- one person;
- one grouped food mass;
- one skyline mass;
- one crowd silhouette.

High examples:

- several distinct people with separate roles;
- furniture, vehicles, signs, tools, architecture, and animals that all matter independently;
- many unique objects with narrative importance.

### Relationship density

Judge how many relationships must be understood:

- holding, facing, sitting beside, leaning on, crossing, stacking, nesting, or connecting;
- foreground subject framing background action;
- one object blocking another;
- a row arranged along a wall;
- strong scale contrast between near and far subjects.

A scene with few objects may still be complex when relationships are important.

### Depth complexity

Low:

- isolated object;
- single flat plane;
- simple side view.

Medium:

- subject plus background;
- one foreground overlap;
- person, counter, and wall.

High:

- foreground, midground, background, and distant layers;
- strong perspective and scale change;
- many overlapping layers.

### Focal competition

Low:

- one unmistakable focal system.

Medium:

- one dominant system and one subordinate secondary system.

High:

- several equally strong faces, signs, lights, or isolated objects;
- no clear visual hierarchy.

Evaluate focal competition against the selected score band's semantic-system and focal limits.

### Surface detail

Include texture, folds, reflections, hair detail, food detail, tiny windows, decorative marks, and local contour noise.

Keep this factor deliberately weak. A highly textured object can remain semantically simple if humans perceive it as one group.

### Internal detail density

Judge how many separately readable subdivisions survive inside each semantic system. Repetition may still belong to one system, but dense per-instance structure can overload an icon even when the object count is perceptually grouped.

For targets of 6 or lower:

- preserve two or three identity-bearing internal cues in the primary system;
- preserve at most one useful internal pattern in each supporting system unless additional structure is itself identity-bearing;
- collapse remaining internal structure into solid planes, grouped marks, shared rhythm, or negative space.

Do not use the number of visible instances as the detail limit. Numerous instances may remain when they read as one subordinate group and do not receive independent internal description.

### Fidelity allocation

For the primary system, preserve silhouette, orientation, relational scale, and identity-bearing attributes. For subordinate systems, preserve group-level structure and remove fine internal anatomy or construction details.

### Visual shape budget

- Use 3 to 8 major mass shapes as a baseline.
- Keep independently meaningful secondary shapes below 15 where practical.

These are advisory visual thresholds, not hard targets or rejection criteria. A mass shape is a geometric form, not a semantic-system counting unit. A focal center describes attention hierarchy, not a semantic-system counting unit. Semantic-system count, internal detail density, and recognizability take priority over raw polygon or object count.

## Score bands and semantic budgets

### 1 to 2

Allow:

- one dominant system;
- almost no environmental context;
- one silhouette or symbol;
- only an essential internal mark.

The result should behave like a pictogram.

### 3 to 4

Allow:

- one dominant system;
- up to one supporting system;
- minimal internal subdivision;
- no more than two independently readable focal groups.

Typical structures:

- food mass plus plate;
- object plus base;
- person plus one identity accessory;
- animal plus ground cue.

### 5

Allow:

- one dominant system;
- up to two weak supporting systems;
- one simple spatial relationship or repetition rhythm;
- limited foreground-background separation.

Supporting systems must remain subordinate.

### 6

Allow:

- one dominant system;
- up to two fully meaningful supporting systems;
- a small grouped secondary rhythm;
- controlled foreground, midground, and background separation.

Never allow four or more equally important focal centers.

### 7 to 8

Allow multiple independent subjects and stronger scene structure, but continue grouping and deleting. The result may retain:

- multiple subject relationships;
- clearer depth hierarchy;
- secondary focal areas;
- more environmental information.

This range is usually too dense for strict icon-level output.

### 9 to 10

Reserve for an explicitly requested dense reconstruction. Many independent semantic groups, relationships, and depth layers may survive. This range is normally incompatible with the purpose of this skill.

## Compression priority

The source-analysis stage may group repeated elements first so they are counted correctly. During active compression, use this priority:

1. Delete.
2. Group.
3. Demote.
4. Simplify.

Do not reduce overload by drawing the same number of objects with thinner lines or fewer details. Reduce the number of meanings that survive.

Do not reject a result merely because it contains many physical instances. Reject it when those instances become independently meaningful through excessive internal structure, local variation, or competing emphasis.

## Budget enforcement

If the proposed result exceeds the target:

1. remove low-value semantic groups;
2. merge repeated subjects into one mass or rhythm;
3. turn environmental objects into flat planes or marks;
4. reduce depth layers;
5. remove competing focal areas;
6. collapse internal subdivisions within retained systems, preserving only identity-bearing structure;
7. reduce palette accent roles and repeated micro-marks.

## Anti-generic identity test

Ask internally:

"Would this compressed description fit many unrelated images of the same category?"

If yes, restore the minimum identity anchors needed to make it specific to the reference.

## Compression stopping rule

Continue simplifying until removing one more meaningful element would cause one of these failures:

- primary subject becomes ambiguous;
- action or pose becomes unclear;
- distinctive spatial identity disappears;
- scale relationship collapses;
- composition becomes generic;
- a critical identity anchor is lost.

Stop at the minimum sufficient representation.
