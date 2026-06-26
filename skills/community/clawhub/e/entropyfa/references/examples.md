# Examples

## Discover Available Data

Prompt:

`What financial planning data do you have built in?`

Command:

```sh
entropyfa data coverage
```

## Source-Backed Tax Lookup

Prompt:

`What are the 2026 single federal income tax brackets, and where did they come from?`

Command:

```sh
entropyfa data lookup --category tax --key federal_income_tax_brackets --year 2026 --filing-status single
```

## Roth Conversion With Schema First

Prompt:

`Help me run a Roth conversion analysis, but first figure out what inputs you still need.`

Commands:

```sh
entropyfa compute roth-conversion --schema
```

Then, once the missing inputs are known:

```sh
entropyfa compute roth-conversion --json '<JSON>'
```

## RMD Schedule

Prompt:

`Show a multi-year RMD schedule for this IRA.`

Commands:

```sh
entropyfa compute rmd-schedule --schema
entropyfa compute rmd-schedule --json '<JSON>'
```

## IRMAA Lookup

Prompt:

`What IRMAA tier applies to married filing separately if the taxpayer lived with their spouse during the year?`

Command:

```sh
entropyfa data lookup --category insurance --key irmaa_brackets --year 2026 --filing-status married_filing_separately --lived-with-spouse-during-year true
```

## Projection Without Visual

Prompt:

`Run a retirement projection and keep the output machine-readable.`

Command:

```sh
entropyfa compute projection --json '<JSON>'
```

## Projection With Visual

Prompt:

`Run the projection and show me the terminal dashboard too.`

Command:

```sh
entropyfa compute projection --visual --json '<JSON>'
```
