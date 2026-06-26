---
name: cep-lookup
description: Looks up address data for a Brazilian CEP using the ViaCEP API.
metadata:
  {
    "openclaw":
      {
        "emoji": "📮",
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "axios",
              "bins": ["axios"],
              "label": "Install axios for HTTP requests",
            }
          ],
      },
  }
---

# CEP Lookup

Looks up the full address for a Brazilian postal code (CEP) using the public [ViaCEP](https://viacep.com.br) API. No authentication required.

## Triggers

Use this skill when the user mentions a CEP in any of these formats:
- `cep 01001-000`
- `CEP 20040020`
- `details for CEP 30140-110`

## Output

The skill returns:
- Street (logradouro)
- Neighborhood (bairro)
- City (localidade)
- State (UF)
- Complement, if available (complemento)

## Error handling

- Invalid CEP format → usage instruction
- CEP not found in ViaCEP database → informative message
- Network failure → generic error message
