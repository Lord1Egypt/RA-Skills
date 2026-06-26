# Câmara dos Deputados — Referência Completa de Endpoints

Base: `https://dadosabertos.camara.leg.br/api/v2`
Swagger: `https://dadosabertos.camara.leg.br/swagger/api.html`

## Deputados

| Endpoint | Params principais |
|---|---|
| `GET /deputados` | nome, siglaPartido, siglaUf, idLegislatura, siglaSexo, codSituacao |
| `GET /deputados/{id}` | — |
| `GET /deputados/{id}/discursos` | dataInicio, dataFim, idTipoDiscurso, ordenarPor, ordem |
| `GET /deputados/{id}/despesas` | ano, mes, cnpjCpfFornecedor, pagina, itens |
| `GET /deputados/{id}/documentos` | dataInicio, dataFim, codTipoDocumento |
| `GET /deputados/{id}/eventos` | dataInicio, dataFim, codTipoEvento |
| `GET /deputados/{id}/frentes` | — |
| `GET /deputados/{id}/mandatos` | — |
| `GET /deputados/{id}/ocupacoes` | — |
| `GET /deputados/{id}/orgaos` | dataInicio, dataFim |
| `GET /deputados/{id}/profissoes` | — |

## Proposições

| Endpoint | Params principais |
|---|---|
| `GET /proposicoes` | siglaTipo, numero, ano, autor, tema, keywords, dataApresentacaoInicio, dataApresentacaoFim, codSituacao, tramitacaoSenado |
| `GET /proposicoes/{id}` | — |
| `GET /proposicoes/{id}/autores` | — |
| `GET /proposicoes/{id}/relacionadas` | — |
| `GET /proposicoes/{id}/temas` | — |
| `GET /proposicoes/{id}/tramitacoes` | dataInicio, dataFim |
| `GET /proposicoes/{id}/votacoes` | — |

### Tipos de proposição (siglaTipo)
PL, PEC, PLP, MPV, PDC, PRC, REC, REQ, REP, REO, MSC, PLN, PDS, PFC, PDN, EMC, EMP, EMS, SBT, SCR, SGM, SMP

### Situações de proposição (codSituacao)
- `1` = Tramitando
- `2` = Arquivada
- `3` = Transformada em norma jurídica
- Consultar `/referencias/proposicoes/codSituacaoProposicao`

## Votações

| Endpoint | Params principais |
|---|---|
| `GET /votacoes` | dataInicio, dataFim, idOrgao, siglaPartido, idDeputado, ordem, ordenarPor |
| `GET /votacoes/{id}` | — |
| `GET /votacoes/{id}/votos` | — |
| `GET /votacoes/{id}/orientacoes` | — |

### Órgãos principais
- `180` = Plenário

## Eventos / Agenda

| Endpoint | Params principais |
|---|---|
| `GET /eventos` | dataInicio, dataFim, siglaOrgao, codTipoEvento, codSituacao, ordem, ordenarPor, itens |
| `GET /eventos/{id}` | — |
| `GET /eventos/{id}/deputados` | — |
| `GET /eventos/{id}/orgaos` | — |
| `GET /eventos/{id}/pauta` | — |
| `GET /eventos/{id}/votacoes` | — |

### Situações de evento (codSituacao)
- `1` = Convocada / Prevista
- `2` = Realizada
- `3` = Em andamento
- `4` = Cancelada

## Órgãos / Comissões

| Endpoint | Params principais |
|---|---|
| `GET /orgaos` | sigla, codTipoOrgao, nome, dataInicio, dataFim |
| `GET /orgaos/{id}` | — |
| `GET /orgaos/{id}/eventos` | dataInicio, dataFim, codTipoEvento |
| `GET /orgaos/{id}/membros` | dataInicio, dataFim |
| `GET /orgaos/{id}/votacoes` | dataInicio, dataFim |

### Tipos de órgão (codTipoOrgao)
- `2` = Comissão Permanente
- `3` = Comissão Temporária
- `4` = Comissão Especial
- `5` = Comissão Externa
- `6` = CPI
- `26` = Plenário Virtual
- Consultar `/referencias/tiposOrgao`

## Comissões principais (sigla)
CCJC, CFT, CDE, CSAUDE, CTRAB, CAPADR, CDC, CDU, CMADS, CREDN, CME, CTUR, CCULT, CDH, CCOM, CESPO, CVT, CSPCCO

## Partidos e Blocos

| Endpoint | Params |
|---|---|
| `GET /partidos` | sigla, dataInicio, dataFim, ordem, ordenarPor |
| `GET /partidos/{id}` | — |
| `GET /partidos/{id}/membros` | dataInicio, dataFim |
| `GET /blocos` | idLegislatura |
| `GET /blocos/{id}` | — |

## Frentes Parlamentares

| Endpoint |
|---|
| `GET /frentes` |
| `GET /frentes/{id}` |
| `GET /frentes/{id}/membros` |

## Grupos de Trabalho

| Endpoint |
|---|
| `GET /gruposTrabalho` |
| `GET /gruposTrabalho/{id}` |
| `GET /gruposTrabalho/{id}/membros` |

## Legislaturas

| Endpoint |
|---|
| `GET /legislaturas` |
| `GET /legislaturas/{id}` |
| `GET /legislaturas/{id}/mesa` |

- Legislatura atual: **57** (iniciada em 01/02/2023)

## Referências (dados auxiliares)

```
GET /referencias/deputados/codSituacao
GET /referencias/deputados/siglaSexo
GET /referencias/proposicoes/codSituacaoProposicao
GET /referencias/proposicoes/siglaTipo
GET /referencias/proposicoes/tema
GET /referencias/proposicoes/codTema
GET /referencias/tiposEvento
GET /referencias/tiposSituacaoEvento
GET /referencias/tiposOrgao
GET /referencias/uf
GET /referencias/partidos
```

## Bulk Data (despesas CEAP)
- `https://www.camara.leg.br/cotas/Ano-{ano}.json.zip`
- Anos disponíveis: 2008–atual
- Atualização diária
