# Workflows

## First-Time Setup

```bash
pip install -r requirements.txt
mkdir -p data
cp assets/special_cases_template.json data/special_cases.json
# Edit data/special_cases.json if you have corporate actions
python scripts/cli.py import data/transactions.csv
python scripts/cli.py stats --update-prices auto
```

## Adding More Data

```bash
python scripts/cli.py import data/new_transactions.csv
python scripts/cli.py stats
```

## Reset Everything

```bash
python cli.py reset --confirm
```
