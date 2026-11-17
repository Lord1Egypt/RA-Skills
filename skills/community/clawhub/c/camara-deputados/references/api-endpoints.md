# Câmara API endpoint reference

Base: `https://dadosabertos.camara.leg.br/api/v2`

This is a task-oriented map of verified core endpoints, not a replacement for the [official Swagger](https://dadosabertos.camara.leg.br/swagger/api.html). Contracts were checked against `/api/v2/api-docs` on 2026-08-23.

## Common collection parameters

- `pagina`: page number
- `itens`: page size, normally at most 100
- `ordem`: `ASC` or `DESC`
- `ordenarPor`: endpoint-specific sort field

Follow the link with `rel: next`; do not infer another page only from the number of returned items.

## Deputies

| Endpoint | Main parameters |
|---|---|
| `GET /deputados` | `nome`, `siglaPartido`, `siglaUf`, `idLegislatura`, `codSituacao` |
| `GET /deputados/{id}` | — |
| `GET /deputados/{id}/discursos` | `dataInicio`, `dataFim`, `idLegislatura` |
| `GET /deputados/{id}/despesas` | `ano`, `mes`, `cnpjCpfFornecedor` |
| `GET /deputados/{id}/eventos` | `dataInicio`, `dataFim`, `codTipoEvento` |
| `GET /deputados/{id}/frentes` | — |
| `GET /deputados/{id}/mandatos` | — |
| `GET /deputados/{id}/ocupacoes` | — |
| `GET /deputados/{id}/orgaos` | `dataInicio`, `dataFim` |

There is no direct deputy-attendance endpoint. Event participant lists are not a drop-in substitute for formal attendance.

## Propositions

| Endpoint | Main parameters |
|---|---|
| `GET /proposicoes` | `siglaTipo`, `numero`, `ano`, `autor`, `keywords`, `codTema`, `codSituacao`, `tramitacaoSenado`, date filters |
| `GET /proposicoes/{id}` | — |
| `GET /proposicoes/{id}/autores` | — |
| `GET /proposicoes/{id}/relacionadas` | — |
| `GET /proposicoes/{id}/temas` | — |
| `GET /proposicoes/{id}/tramitacoes` | `dataInicio`, `dataFim` |
| `GET /proposicoes/{id}/votacoes` | — |

`siglaTipo` examples include `PL`, `PLP`, `PEC`, `MPV`, and `PDL`. Obtain the maintained list from `/referencias/proposicoes/siglaTipo`.

## Votes and events

| Endpoint | Main parameters |
|---|---|
| `GET /votacoes` | `dataInicio`, `dataFim`, `idOrgao`, `idDeputado` |
| `GET /votacoes/{id}` | — |
| `GET /votacoes/{id}/votos` | — |
| `GET /votacoes/{id}/orientacoes` | — |
| `GET /eventos` | `dataInicio`, `dataFim`, `siglaOrgao`, `codTipoEvento`, `codSituacao` |
| `GET /eventos/{id}` | — |
| `GET /eventos/{id}/deputados` | — |
| `GET /eventos/{id}/orgaos` | — |
| `GET /eventos/{id}/pauta` | — |
| `GET /eventos/{id}/votacoes` | — |

## Organizations and groups

| Endpoint | Main parameters |
|---|---|
| `GET /orgaos` | `sigla`, `codTipoOrgao`, `nome`, date filters |
| `GET /orgaos/{id}` | — |
| `GET /orgaos/{id}/eventos` | date filters |
| `GET /orgaos/{id}/membros` | date filters |
| `GET /orgaos/{id}/votacoes` | date filters |
| `GET /grupos` | collection filters |
| `GET /grupos/{id}` | — |
| `GET /grupos/{id}/historico` | — |
| `GET /grupos/{id}/membros` | — |

Other stable collections include `/partidos`, `/blocos`, `/frentes`, and `/legislaturas`, with their `{id}` detail and documented child resources.

## Reference data

Resolve codes dynamically:

```text
GET /referencias/deputados/codSituacao
GET /referencias/deputados/siglaSexo
GET /referencias/proposicoes/codSituacao
GET /referencias/proposicoes/codTema
GET /referencias/proposicoes/codTipoAutor
GET /referencias/proposicoes/codTipoTramitacao
GET /referencias/proposicoes/siglaTipo
GET /referencias/tiposEvento
GET /referencias/tiposSituacaoEvento
GET /referencias/tiposOrgao
GET /referencias/uf
```

Do not maintain hand-written dictionaries for proposition or event situations; the official lists contain more states and can change.

## Bulk CEAP data

For large historical expense analyses, prefer the annual files linked by the official API documentation, such as `https://www.camara.leg.br/cotas/Ano-{ano}.json.zip`, instead of paginating thousands of per-deputy calls.
