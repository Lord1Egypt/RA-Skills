---
name: camara-deputados
description: Monitor and research the Brazilian Chamber of Deputies (Câmara dos Deputados) legislative activity. Use when: (1) searching for bills/proposições by author, keyword, type or year, (2) checking today's or upcoming agenda/events, (3) looking up deputies (deputados) by name, party or state, (4) tracking voting results (votações) in plenary or committees, (5) checking committee (comissão) schedules and membership, (6) monitoring specific bills' tramitação/status, (7) retrieving deputy expenses (CEAP/cota parlamentar), (8) searching for frentes parlamentares, grupos de trabalho, (9) any question about the Câmara dos Deputados, deputies, or federal bills. Base URL: https://dadosabertos.camara.leg.br/api/v2 — no auth required, returns JSON.
version: "1.0.1"
author: "Daniel Marques"
license: "MIT"
---

# Câmara dos Deputados — API de Dados Abertos

Base URL: `https://dadosabertos.camara.leg.br/api/v2`
Docs/Swagger: `https://dadosabertos.camara.leg.br/swagger/api.html`
No authentication required. All endpoints return JSON.

## Common query params
- `itens` — page size (default 15, max 100)
- `pagina` — page number
- `ordem` — `ASC` or `DESC`
- `ordenarPor` — field name for sorting

---

## Key Endpoints

### Deputies (Deputados)
```
GET /deputados
  ?nome=         # name search
  ?siglaPartido= # party (e.g. PT, PL, MDB)
  ?siglaUf=      # state (e.g. SP, RJ, AM)
  ?idLegislatura=57  # current legislature
  ?ordem=ASC&ordenarPor=nome

GET /deputados/{id}           # full profile
GET /deputados/{id}/discursos # speeches
  ?dataInicio=YYYY-MM-DD&dataFim=YYYY-MM-DD
GET /deputados/{id}/despesas  # CEAP expenses
  ?ano=YYYY&mes=MM
GET /deputados/{id}/frentes   # parliamentary fronts
GET /deputados/{id}/ocupacoes # professional history
GET /deputados/{id}/orgaos    # committee memberships
```

### Bills / Proposições
```
GET /proposicoes
  ?siglaTipo=PL      # type: PL, PEC, MPV, PDC, PLP, etc.
  ?numero=123
  ?ano=2026
  ?autor=Nome        # author name (partial match)
  ?tema=             # topic id (see /referencias/temas)
  ?keywords=         # keywords
  ?dataApresentacaoInicio=YYYY-MM-DD
  ?dataApresentacaoFim=YYYY-MM-DD
  ?codSituacao=      # status code
  ?tramitacaoSenado=true  # bills currently in Senate
  ?ordem=DESC&ordenarPor=id

GET /proposicoes/{id}             # full detail
GET /proposicoes/{id}/autores     # authorship
GET /proposicoes/{id}/relacionadas# related bills
GET /proposicoes/{id}/temas       # topics
GET /proposicoes/{id}/tramitacoes # full history/status
GET /proposicoes/{id}/votacoes    # votes on this bill
```

### Votações (Voting)
```
GET /votacoes
  ?dataInicio=YYYY-MM-DD&dataFim=YYYY-MM-DD
  ?idOrgao=180       # 180 = Plenário
  ?siglaPartido=
  ?ordem=DESC&ordenarPor=dataHoraRegistro

GET /votacoes/{id}             # vote detail
GET /votacoes/{id}/votos       # individual votes per deputy
GET /votacoes/{id}/orientacoes # party orientations
```

### Events / Agenda (Eventos)
```
GET /eventos
  ?dataInicio=YYYY-MM-DD
  ?dataFim=YYYY-MM-DD
  ?siglaOrgao=       # committee sigla or PLEN for plenary
  ?codTipoEvento=    # see /referencias/tiposEvento
  ?codSituacao=      # see /referencias/situacoesEvento
  ?ordem=ASC&ordenarPor=dataHoraInicio

GET /eventos/{id}          # event detail
GET /eventos/{id}/deputados # attending deputies
GET /eventos/{id}/orgaos    # organizing bodies
GET /eventos/{id}/pauta     # agenda items
GET /eventos/{id}/votacoes  # votes in this session
```

### Committees (Órgãos / Comissões)
```
GET /orgaos
  ?sigla=CCJC        # committee abbreviation
  ?codTipoOrgao=     # type (see /referencias/tiposOrgao)
  ?nome=

GET /orgaos/{id}            # detail
GET /orgaos/{id}/eventos    # committee agenda
GET /orgaos/{id}/membros    # current membership
GET /orgaos/{id}/votacoes   # votes by committee
```

### Parties & Blocs (Partidos / Blocos)
```
GET /partidos?ordem=ASC&ordenarPor=sigla
GET /partidos/{id}
GET /partidos/{id}/membros

GET /blocos
GET /blocos/{id}
```

### Parliamentary Fronts (Frentes)
```
GET /frentes
GET /frentes/{id}
GET /frentes/{id}/membros
```

### Working Groups (Grupos de Trabalho)
```
GET /gruposTrabalho
GET /gruposTrabalho/{id}
GET /gruposTrabalho/{id}/membros
```

### Legislative Sessions (Legislaturas)
```
GET /legislaturas
GET /legislaturas/{id}
GET /legislaturas/{id}/mesa  # presiding board
```

### Reference Data
```
GET /referencias/deputados/codSituacao
GET /referencias/proposicoes/codSituacaoProposicao
GET /referencias/proposicoes/siglaTipo
GET /referencias/proposicoes/tema
GET /referencias/tiposEvento
GET /referencias/tiposOrgao
GET /referencias/uf
```

---

## Common Tasks

### Today's agenda
```bash
DATE=$(date +%Y-%m-%d)
curl "https://dadosabertos.camara.leg.br/api/v2/eventos?dataInicio=$DATE&dataFim=$DATE&ordem=ASC&ordenarPor=dataHoraInicio"
```

### Search bills by keyword
```bash
curl "https://dadosabertos.camara.leg.br/api/v2/proposicoes?keywords=transporte+público&ano=2026&ordem=DESC&ordenarPor=id&itens=20"
```

### Find a deputy
```bash
curl "https://dadosabertos.camara.leg.br/api/v2/deputados?nome=Marcos+Pontes&idLegislatura=57"
```

### Recent plenary votes
```bash
curl "https://dadosabertos.camara.leg.br/api/v2/votacoes?idOrgao=180&dataInicio=2026-03-01&ordem=DESC&ordenarPor=dataHoraRegistro&itens=10"
```

### Bill status / tramitação
```bash
curl "https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id}/tramitacoes"
```

---

## Notes
- Legislature 57 = current (started Feb 2023)
- Plenário orgão id = 180
- CEAP data also available as bulk download: `https://www.camara.leg.br/cotas/Ano-{ano}.json.zip`
- Full API reference: see `references/api-endpoints.md` for parameter details
- Swagger UI: `https://dadosabertos.camara.leg.br/swagger/api.html`

---

## API Quirks & Tips

- **Standard response wrapper**: All endpoints return `{dados: [...], links: [...]}`. The Python client's `_get()` automatically extracts `dados`.
- **Pagination**: Use `itens` (page size, max 100) and `pagina` (page number). The Python client's `_get_list()` auto-paginates — if `dados` has fewer items than `itens`, it's the last page.
- **Date format**: Always ISO format `YYYY-MM-DD` (unlike Senado which uses `YYYYMMDD`).
- **Legislature 57**: Current legislature (2023-2027). Most endpoints default to current if not specified.
- **Plenário ID**: orgão id = 180 for plenary hall.
- **tramitacaoSenado**: Use `?tramitacaoSenado=true` on proposições endpoint to find bills currently being reviewed by the Senate.
- **CEAP bulk data**: Deputy expenses also available as bulk download at `https://www.camara.leg.br/cotas/Ano-{ano}.json.zip`.

---

## Python Client (async)

You can use the async Python client for programmatic access:

```python
import asyncio
from camara_client import get_camara_client

async def main():
    client = get_camara_client()
    
    # Listar deputados
    deps = await client.lista_deputados()
    
    # Buscar por nome
    resultado = await client.buscar_deputado_por_nome("Lula")
    
    # Pesquisar proposições
    props = await client.pesquisar_proposicoes(keywords="transporte", ano=2026)
    
    # Eventos de hoje
    from datetime import date
    eventos = await client.get_eventos_dia(date.today())
    
    await client.close()

asyncio.run(main())
```

### Available Methods

**Deputados:**
- `lista_deputados(legislatura)` — List deputies
- `buscar_deputado_por_nome(nome, legislatura)` — Search by name
- `get_deputado_detalhe(id)` — Full profile
- `get_despesas_deputado(id, ano)` — CEAP expenses
- `get_frentes_deputado(id)` — Parliamentary fronts
- `get_discursos_deputado(id, data_inicio, data_fim)` — Speeches
- `get_presenca_deputado(id, data_inicio, data_fim)` — Attendance
- `get_deputado_orgaos(id)` — Committee memberships
- `get_deputado_ocupacoes(id)` — Professional history

**Proposições:**
- `pesquisar_proposicoes(keywords, sigla_tipo, numero, ano, autor, tramitando, tema, tramitacao_senado)` — Search bills
- `get_proposicao_detalhe(id)` — Full detail
- `get_proposicao_tramitacao(id)` — Status history
- `get_proposicao_votacoes(id)` — Votes on bill
- `get_proposicao_autores(id)` — Authors
- `get_proposicao_temas(id)` — Topics/tags
- `get_proposicao_relacionadas(id)` — Related bills

**Eventos:**
- `get_eventos_dia(data)` — Day agenda
- `get_eventos_periodo(data_inicio, data_fim)` — Events in period
- `get_evento_detalhe(id)` — Event detail
- `get_evento_deputados(id)` — Deputies in event
- `get_evento_orgaos(id)` — Organizing bodies
- `get_evento_votacoes(id)` — Votes in event

**Votações:**
- `get_votacoes_periodo(data_inicio, data_fim, id_orgao)` — Votes in period
- `get_votacao_detalhe(id)` — Vote detail
- `get_votos_votacao(id)` — Individual votes
- `get_orientacoes_votacao(id)` — Party orientations

**Órgãos/Comissões:**
- `lista_orgaos()` — List committees
- `get_orgao_detalhe(id)` — Committee detail
- `get_eventos_orgao_periodo(id, data_inicio, data_fim)` — Committee agenda
- `get_membros_orgao(id)` — Current members
- `get_orgao_membros_periodo(id, data_inicio, data_fim)` — Members in period
- `get_votacoes_orgao(id, data_inicio, data_fim)` — Committee votes

**Legislaturas:**
- `lista_legislaturas()` — List legislatures
- `get_legislatura_detalhe(id)` — Legislature detail
- `get_legislatura_mesa(id)` — Presiding board

**Partidos:**
- `lista_partidos()` — List parties
- `get_partido_detalhe(id)` — Party detail
- `get_partido_membros(id)` — Party members

**Blocos:**
- `lista_blocos()` — List parliamentary blocs
- `get_bloco_detalhe(id)` — Bloc detail

**Frentes:**
- `lista_frentes(id_legislatura)` — List parliamentary fronts
- `get_frente_detalhe(id)` — Front detail
- `get_frente_membros(id)` — Front members

**Referências:**
- `get_referencias_situacao_deputado()` — Deputy status codes
- `get_referencias_situacao_proposicao()` — Bill status codes
- `get_referencias_tipo_proposicao()` — Bill type codes (PL, PEC, etc)
- `get_referencias_temas()` — Topic/theme list
- `get_referencias_tipos_evento()` — Event types
- `get_referencias_tipos_orgao()` — Committee types
- `get_referencias_uf()` — Brazilian states

**Utilitários:**
- `get_proposicoes_recentes(dias)` — Recent bills
- `get_votacoes_semana()` — This week's votes
- `get_eventos_semana()` — This week's events
- `get_pauta_evento(id)` — Event agenda items

Requires: `pip install httpx`
