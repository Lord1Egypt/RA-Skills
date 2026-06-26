# CAX plugin example: recrystallization grain growth

Use this as an example of how to apply the `create-plugin` workflow to a real request.

## Request shape

Target repository: `https://github.com/maxencefaldor/cax`

Goal:
- add a simple plugin for grain growth during recrystallization in metal
- keep it minimal, readable, and convention-friendly
- documentation required
- runtime testing may be skipped if dependency handling is difficult

## How to approach it

1. Read the repository first.
	- Inspect `README.md`, `pyproject.toml`, docs, and contribution/style clues.
	- Use DeepWiki MCP source-code queries if available:
		- ask for the main extension points for adding a new complex system
		- ask which built-in systems are the smallest and best examples to study first
		- read structure/contents for the repo documentation when helpful
	- Find existing systems under `src/cax/cs/`.
	- Inspect a few compact implementations such as `life` and `elementary` to learn the library shape.

2. Learn the modular structure.
	- CAX organizes systems around `ComplexSystem` with separate perception/update pieces in many built-ins.
	- Formatting/style clues include tab indentation, short focused modules, modern typing, and straightforward docstrings.

3. Make a minimal plan.
	- Build a standalone package instead of patching upstream unless the user explicitly wants an upstream PR.
	- Expose one small public class plus one or two initialization helpers.
	- Keep the physical model pedagogical rather than exhaustive.

4. Implement a simple plugin.
	- Example package layout:
		- `pyproject.toml`
		- `README.md`
		- `src/cax_recrystallization/__init__.py`
		- `src/cax_recrystallization/cs.py`
		- `src/cax_recrystallization/init.py`
	- Example model choice:
		- grain orientation stored as one-hot channels
		- one extra stored-energy channel
		- dominant-neighbor switching rule
		- explicit high-energy nucleation rule
		- simple render method for visually distinct grains

5. Check convention fit without overpromising.
	- If full runtime execution is hard, still do feasible checks such as syntax compilation and code-structure review.
	- State clearly that runtime validation was not completed.

6. Document the result.
	- include installation
	- include one short usage example
	- list simplifying assumptions
	- explain state layout if the plugin is stateful

## Lessons from this example

- A good plugin task starts with repo learning, not coding.
- Mirroring small upstream modules is usually better than inventing a brand-new structure.
- Minimal, honest documentation is part of the deliverable, not an optional extra.
- When verification is limited, say so plainly and avoid inflated claims.
