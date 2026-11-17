# Title Block Template (DWT)

This directory should contain your organization's standard AutoCAD DWT template.

## Expected Contents

- `title_block_A1.dwt` — A1 sheet with title block, border, and standard layers
- `title_block_A2.dwt` — A2 sheet variant
- `title_block_A3.dwt` — A3 sheet variant

## Requirements

1. All layers must match `standard_layers.json` exactly.
2. Text styles must reference fonts available in the project font pool (SHX/TTF).
3. Plot settings should be preset to your organization's standard CTB/STB.
4. No proxy objects or external references in the template itself.

## How to Use

Replace the placeholder `.md` file with actual `.dwt` files exported from AutoCAD:

```bash
# Example: copy your company template
cp /path/to/your_company_A1.dwt templates/title_block_A1.dwt
```

Then update `scripts/02_standardize.sh` to reference the correct template path.
