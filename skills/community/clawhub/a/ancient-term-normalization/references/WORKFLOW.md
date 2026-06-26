# Workflow

The ancient term normalisation skill operates as follows:

1. **Preparation** – An agent passes the path of the recognised characters JSON file and the workspace path to the script.
2. **Input validation** – The script reads the input JSON and ensures it contains a `recognized_chars` key. If the key is missing, the script exits with an error.
3. **Load mapping** – The script locates the alias mapping file `assets/data/historical_aliases.yaml` relative to its own directory and loads it using PyYAML.
4. **Normalisation** – For each recognised item:
   - If the item’s `text` key matches a key in the alias mapping, use the provided list of aliases, type and note.
   - Otherwise, set the normalised list to `[text]`, type to `unknown` and note to an empty string.
   - Copy the `confidence` score if present.
5. **Output generation** – The script writes the list of normalised terms as a JSON file at `term_normalisation/normalized_terms.json` within the workspace.
6. **Completion** – A message is printed to stdout summarising how many terms were normalised and where the output file is located.

This modular design allows other skills to build on the normalised output for search or evidence chain construction.