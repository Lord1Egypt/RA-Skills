# Originality and license restrictions

## Target

This process is used for legal, compliant, ethical, and maintainable adaptation. It should help users refine their ideas and recreate designs that fit the style of the target project, rather than pretending to be a copy.

## Content that is generally safe to absorb

- High-level thinking and product concepts.
- Common architectural patterns.
- Publicly documented workflow.
- Behavioral needs expressed in own words.
- Algorithms and technologies that are standard, unprotectable or properly licensed.
- Configuration concepts recreated for the target environment.

## Content that needs to be handled with caution

- Large chunks of code from other projects.
- Unique text, prompts, examples, documents, graphics, names or brand expressions.
- Highly tied and non-obvious implementation structure to the reference project.
- Makefile containing license header or attribution requirements.
- Dependencies with restrictive license.
- Private or proprietary repositories.

## Security adaptation process

1. Summarize reference capabilities in neutral language.
2. Identify the problem it solves.
3. Independently design the original solution for the target project.
4. Implement new code using target project conventions.
5. Adjust concept naming to target project semantics.
6. Add tests based on desired behavior rather than on the internal implementation of the reference project.
7. When a license requires a signature, retain the necessary signature.
8. Document license uncertainty as a risk rather than ignoring it.

## Risk Signal

- The output retains the same file structure and naming of the reference project without target project specific justification.
- The output contains a lot of identical or nearly identical code/text.
- The Agent cannot explain why the target design differs from the reference design.
- The new module has a high degree of overlap with the existing modules of the target project.
- The only reason is just "that's what the reference project does".

## Recommended statements in reports

Recommended to use:

- "Inspired by the way reference projects are treated in..."
- "Reimplemented as a module that matches the style of the target project, for..."
- "The reference project solved this problem with X; this project chose Y because..."

Avoid using:

- "Copied from..."
- "Exactly the same as..."
- "Hidden imitation..."
- "Make it seem irrelevant..."
