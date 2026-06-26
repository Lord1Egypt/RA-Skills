# Examples

## Example 1: Email triage
Command:
python3 scripts/create_filter.py --type email --criteria "include: client,contract,invoice" --priority high

Result:
Creates a reusable high-priority email rule.

## Example 2: News cleanup
Command:
python3 scripts/create_filter.py --type news --criteria "include: AI,agents,funding" --priority medium

Result:
Creates a reusable news filtering rule.

## Example 3: Search result cleanup
Command:
python3 scripts/create_filter.py --type search --criteria "exclude: spam,duplicate,low-quality" --priority medium

Result:
Creates a reusable search filtering rule.
