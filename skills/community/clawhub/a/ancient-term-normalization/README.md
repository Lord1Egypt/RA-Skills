# Ancient Term Normalisation Skill

This repository contains the code and resources for the **ancient-term-normalization** skill.  
It provides scripts and data to convert character recognition outputs into normalised terms suitable for further search and retrieval in humanities research.

## Usage

1. Install dependencies from `scripts/requirements.txt` in a virtual environment.
2. Run the normalisation script:

   ```bash
   python scripts/normalize_terms.py --input path/to/recognized_chars.json --workspace path/to/workspace
   ```

3. A `term_normalisation` folder will be created in the workspace containing `normalized_terms.json`.

## Project structure

- `SKILL.md` – Defines the skill’s metadata and user instructions.
- `scripts/` – Python scripts implementing the term normalisation logic.
- `references/` – Detailed documentation and domain rules.
- `assets/` – Schemas, templates and lookup data.
- `examples/` – Sample input and output files.
- `tests/` – Basic tests verifying the script’s behaviour.
- `agents/` – Platform specific integration config.

## License

Released under the MIT license. See `LICENSE.txt` for details.