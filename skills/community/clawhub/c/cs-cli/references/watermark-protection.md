# Document Watermark Protection Workflow

> **Preread**: `references/image-processing.md` for `image watermark` parameters, and `references/pdf-processing.md` for `pdf watermark`/`remove-watermark` parameters.

## Scenario

The user needs to add a watermark before sharing a document, or remove an existing watermark.

## Decision Tree

| User Need | Input Type | Route To |
|-----------|------------|----------|
| Add watermark | Image | `image watermark` |
| Add watermark | PDF | `pdf watermark` |
| Remove watermark | PDF | `pdf remove-watermark` |
| Remove watermark | Image | `image enhance --mode 10` |

## Recommended Parameters

| Scenario | Recommended Parameters |
|----------|------------------------|
| Internal document | `--text "INTERNAL USE ONLY" --opacity 0.3` |
| Draft marker | `--text "DRAFT" --opacity 0.2 --color "#999999"` |
| Copyright protection | `--text "COPYRIGHT Company Name" --opacity 0.15 --size 36` |
| Confidential document | `--text "CONFIDENTIAL" --opacity 0.4 --color "#FF0000"` |

## Notes

- PDF watermarking supports at most 100 pages.
- Watermark removal quality depends on the complexity of the original watermark.
- Image watermarking is irreversible for the output file. The original image is not modified; a new file is produced.
