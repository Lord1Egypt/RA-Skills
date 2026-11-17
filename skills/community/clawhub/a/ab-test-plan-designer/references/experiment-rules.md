# Rules for a test that survives a finance review

Reference for the A/B Test Plan Designer skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## Sample size

- n per arm = 16 * p(1-p) / d^2, with p the baseline rate and d the absolute difference to detect.
- The multiplier is 16 for 95% confidence and 80% power; wider confidence or higher power needs a bigger multiplier.
- A bigger baseline rate needs fewer conversions for the same absolute difference; a smaller difference needs many more.

## One variable, one decision rule

- Change the headline, or the image, or the offer; not two at once.
- Write the decision rule before the test: what counts as a win, a loss and an inconclusive result.
- Set stop rules for spend, for a broken page and for a tracking failure.

## How the platforms run tests

- Meta splits the audience evenly and asks for at least two weeks of runtime.
- Google's ad variation feature caps the duration at 84 days and splits the budget by percentage, and a 50/50 split does not guarantee an even impression split.
- Both platforms report a confidence level, so agree on yours before the launch.
