# Answer Template Format

The fine-tuned model generates structured answer templates with these sections:

## Question type
One of: `calculation`, `definition`, `explain`, `describe`, `derive`, `analyse`, `practical`

## Given
Bullet list of quantities, conditions, or data stated in the question.

## Required
What the student must find, state, explain, derive, or conclude.

## Formulae / principles
Relevant equations (with symbol definitions) or physics principles (laws, conservation rules).

## Answer frame
Numbered steps outlining the solution approach:
1. Setup / identify quantities
2. Select and apply the governing principle
3. Work through intermediate steps
4. State the final answer clearly

## Check
Verification items:
- Units and dimensions
- Sign / direction conventions
- Significant figures
- Reasonableness of magnitude

## Example

**Question**: A ball of mass 0.15 kg is thrown vertically upwards with a speed of 20 m/s. Calculate the maximum height.

**Template**:
```
## Question type
calculation

## Given
- m = 0.15 kg, u = 20 m/s, v = 0 at max height, g = 9.81 m/s²

## Required
- Calculate maximum height h

## Formulae / principles
- v² = u² + 2as (kinematics under constant acceleration)

## Answer frame
1. At max height v = 0, acceleration a = -g (upward positive)
2. Rearrange: 0 = u² - 2gh → h = u²/(2g)
3. Substitute: h = 400/19.62 ≈ 20.4 m

## Check
- Units: m²s⁻²  / ms⁻² = m ✓
- Magnitude reasonable for a thrown ball ✓
```
