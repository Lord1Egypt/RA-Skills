# Quick Start

## Project Goal

This project is built around a fairly ordinary spreadsheet workflow:

1. inspect the table structure
2. identify likely issues
3. choose the most reliable processing step
4. suggest formulas or spreadsheet-native workflows for Excel and WPS

Nothing magical here. That is part of the point.

## How To Use The Draft

Start with these files:

- `README.md` for the project overview
- `SKILL.md` for the skill entry point
- `WORKFLOW.md` for the working notes
- `examples/` for sample input and expected response shapes

If you only read two files, start with `README.md` and `WORKFLOW.md`.

## Using It As A Skill

If you want to use the repository as an actual skill package, keep these files at the root:

- `SKILL.md`
- `WORKFLOW.md`
- `agents/openai.yaml`

The important part is that `SKILL.md` stays at the root and contains the trigger description and working rules.

## Recommended First Scenarios

Try the project against one of these common spreadsheet tasks:

- inspect a messy table with blanks, duplicates, and mixed dates
- match two sheets by an ID column
- clean a text column with extra spaces and inconsistent capitalization

These are intentionally plain examples. Spreadsheet trouble is usually plain right up until it stops being plain.

## Current Scope

The current draft is focused on:

- diagnosis from headers and sample rows
- formula suggestions for Excel and WPS
- cleanup workflows
- matching and summarization guidance

It does not currently aim to cover:

- chart generation
- visual styling
- full office automation

In other words, this project is much better at dealing with awkward tables than making them look impressive.
