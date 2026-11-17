---
name: camara-deputados
description: "Research Brazil's Chamber of Deputies using its official open-data API. Use for federal deputies, Chamber bills, votes, events, committees, parliamentary fronts, and CEAP expenses; use senado-federal for Senate-only records."
license: MIT
metadata:
  author: Daniel Marques
  version: "1.1.1"
---

# Câmara dos Deputados

Use official Chamber data to answer factual legislative questions and build reproducible queries.

- API: `https://dadosabertos.camara.leg.br/api/v2`
- Swagger: `https://dadosabertos.camara.leg.br/swagger/api.html`
- Authentication: none
- Response envelope: normally `{ "dados": ..., "links": [...] }`

## Route the task

- Read [references/api-endpoints.md](references/api-endpoints.md) to select endpoints and parameters.
- Read [references/response-shapes.md](references/response-shapes.md) when implementing pagination, dates, status filters, or error handling.
- Read [references/cross-house.md](references/cross-house.md) when a proposition moved between the Chamber and Senate.
- For a quick inspection, run `python3 scripts/camara.py <command>`.
- For reusable Python code, import `CamaraClient` from `camara_client.py`.

## Core workflow

1. Identify the entity before making detail requests. Search deputies by name and propositions by type, number, and year; retain the official numeric ID returned by the API.
2. Query reference endpoints for codes instead of guessing or relying on remembered dictionaries.
3. Follow the response link whose `rel` is `next`. Stop when it is absent or the requested page limit is reached.
4. Preserve official field names and distinguish an empty successful response from an upstream error.
5. For current-day queries, interpret “today” in `America/Sao_Paulo` and state the retrieval date when freshness matters.
6. Cite or return the exact API URL used when the answer needs to be auditable.

## Important contracts

- Proposition topic filters use `codTema`, not `tema`.
- Proposition status filters use `codSituacao`. There is no single stable code meaning every possible “in progress” state; resolve the intended status from `/referencias/proposicoes/codSituacao`.
- Working groups use `/grupos`, `/grupos/{id}`, `/grupos/{id}/historico`, and `/grupos/{id}/membros`.
- Proposition references use `/referencias/proposicoes/codSituacao` and `/referencias/proposicoes/codTema`.
- Deputy speeches use `dataInicio` and `dataFim` in `YYYY-MM-DD`.
- The API has no direct `/deputados/{id}/presenca` resource. Do not infer formal attendance solely from event participant lists.
- Plenary is currently organization ID `180`, but verify it through `/orgaos/180` before embedding it in long-lived code.

## Python client

```python
from datetime import date

from camara_client import CamaraClient

client = CamaraClient()
try:
    deputados = await client.buscar_deputado_por_nome("nome")
    proposicoes = await client.pesquisar_proposicoes(
        sigla_tipo="PL",
        ano=2026,
        cod_tema=40,
    )
    discursos = await client.get_discursos_deputado(
        deputados[0]["id"],
        date(2026, 1, 1),
        date(2026, 12, 31),
    )
finally:
    await client.close()
```

Use an explicit `cod_situacao` when filtering status. The legacy `tramitando=True` option raises a validation error because its former mapping was incomplete.

## Output discipline

- Separate data reported by the Chamber from interpretation.
- Include proposition type, number, year, ID, current status, and last relevant movement when available.
- Do not describe a proposition as approved, enacted, archived, or pending from a numeric code that was not resolved against the reference endpoint.
- For CEAP totals, state the period, currency treatment, and whether cancelled or refunded documents were included.
