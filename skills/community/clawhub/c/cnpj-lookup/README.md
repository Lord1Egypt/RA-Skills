# CNPJ Lookup - Brazilian Company Search

🔍 **CNPJ Lookup** is a skill for querying Brazilian company data using public APIs.

## Features

- **Brazilian CNPJ Search** - Query company data by CNPJ (Cadastro Nacional da Pessoa Jurídica)
- **Multiple Providers** - Automatic fallback: BrasilAPI → CNPJ.ws → OpenCNPJ
- **Caching** - 24-hour cache to avoid redundant API calls
- **Detailed Data** - Returns company name, status, address, CNAE, QSA (socios), and more

## What is CNPJ?

CNPJ (Cadastro Nacional da Pessoa Jurídica) is the Brazilian equivalent of an EIN (Employer Identification Number). Every company in Brazil must register and obtain a unique CNPJ number.

## Installation

```bash
clawhub install cnpj-lookup
```

## Usage

```bash
# Basic lookup (Markdown output)
python3 scripts/cnpj_lookup.py "12.345.678/0001-95"

# JSON output
python3 scripts/cnpj_lookup.py "12.345.678/0001-95" --json

# Force specific provider
python3 scripts/cnpj_lookup.py "12.345.678/0001-95" --provider brasilapi

# Ignore cache
python3 scripts/cnpj_lookup.py "12.345.678/0001-95" --no-cache

# Detailed (includes QSA - company partners)
python3 scripts/cnpj_lookup.py "12.345.678/0001-95" --detailed
```

## Example Output

```markdown
## Company Data
- **CNPJ:** 12.345.678/0001-95
- **Name:** EMPRESA EXEMPLO LTDA
- **Status:** ACTIVE
- **Type:** MATRIZ
- **Address:** AV. PAULISTA, 1000 - SÃO PAULO/SP
- **Phone:** (11) 99999-9999
- **Email:** contato@empresa.com.br
```

## Requirements

- Python 3.7+
- Internet connection
- Public Brazilian CNPJ APIs (automatically used)

## License

MIT
