# Matching Strategy

Use this strategy to select the most suitable CCDB factor, not merely the first returned factor.

## Mandatory search policy

For non-trivial requests, do all of the following unless the user explicitly narrows scope:
1. search with the strongest Chinese term
2. search with at least one Chinese synonym or broader/narrower Chinese variant
3. search with the strongest English equivalent
4. search with at least one English synonym or alternative wording
5. compare all high-scoring candidates across all runs before selecting a winner

## Constraints to extract and preserve

Always try to preserve these constraints from the user request:
- target object or activity
- process / stage / scenario
- geography / grid / country / region
- unit
- year / applicability period
- source preference if the user implies it

## Candidate selection hierarchy

Prefer candidates in this order:
1. direct semantic match + matching region + matching unit
2. direct semantic match + matching region + compatible unit
3. direct semantic match + weaker region match + compatible unit
4. broader parent-category fallback with explicit warning

## Red flags

Downgrade or reject candidates when:
- country/region conflicts with the user requirement
- unit is clearly incompatible with the intended use
- the result refers to a different lifecycle stage or category
- the result is too generic while a more specific candidate exists
- the result is economically-based or scope-3-spend-based when the user wanted physical activity-based factors

## Output classification

Classify the chosen result as one of:
- direct_match
- close_match
- fallback_generic
- not_suitable

## Multi-round refinement guidance

If the first search set does not yield a reliable result, refine in this order:
1. remove modifiers and test the core noun
2. add process keyword
3. add or remove geography keyword
4. switch Chinese ↔ English
5. broaden to parent category
6. try common domain synonyms

## Required explanation in final answer

The final answer should explain:
- why the chosen factor is the best available match
- what other candidates were considered
- what mismatch risks remain
- what further clarification would improve confidence if needed
