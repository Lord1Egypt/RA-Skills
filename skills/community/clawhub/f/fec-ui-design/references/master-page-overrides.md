# Global/page level difference coverage

When the project needs to maintain UI consistency for a long time, use `design-system/MASTER.md` to store the global design system, and use `design-system/pages/<page>.md` to store page-level differences.

## Reading order

1. First check whether the current page has `design-system/<project>/pages/<page>.md`.
2. If it exists, the rules in the page file cover the same dimensions in the Master.
3. If it does not exist, follow `design-system/<project>/MASTER.md` exactly.
4. The page file only records differences and does not copy the full text of the Master.

## Generate command

```bash
node skills/fec-ui-design/scripts/design-system.mjs "saas analytics dashboard" --project "Acme Console" --persist --output-dir .
```

Generate page overrides:

```bash
node skills/fec-ui-design/scripts/design-system.mjs "saas analytics dashboard" --project "Acme Console" --page dashboard --persist --output-dir .
```

## Page override should contain

- Differences in page tasks and information density
- Layout differences: workspace, table, chart, form, detail page or marketing first screen
- token difference: only write the semantic color, spacing, status or chart color that needs to be covered
- Component differences: only write new or changed component behaviors on the current page
- QA Focus: The current page’s most error-prone responsiveness, accessibility, performance, or interaction risks
