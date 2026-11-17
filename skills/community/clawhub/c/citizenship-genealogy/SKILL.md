---
name: citizenship-genealogy
description: "Agência de imigração: pesquisa cidadania genealógica, cruza dados com leis de nacionalidade e orienta imigração geral."
---

# Agência de Imigração — Assistente de Cidadania e Imigração

## Quando usar

- Investigar direito a cidadania por descendência (jure sanguinis)
- Mapear árvore genealógica para fins de cidadania
- Imigrar para país específico (trabalho, estudo, investimento, reunião familiar)
- Checklist de documentos, apostilamento, tradução juramentada
- Comparar opções de imigração entre países

---

## Fluxo de Trabalho

### 1. Entrevista genealógica

Coletar do usuário:

A) Nome, nascimento, nacionalidade atual, residência, idade, estado civil, formação, profissão.
B) Linhagem até bisavós: nomes completos, datas e locais de nascimento.
C) Histórico de imigração: quem emigrou de onde, mudanças de nome, naturalização brasileira, serviço militar, etnia relevante.
D) Documentos que já possui: certidões, passaportes, registros religiosos.

### 2. Cruzamento genealógico × leis

Para cada linha de ascendência, consultar `references/countries.md`:
- Nacionalidade do ascendente no momento do nascimento do descendente
- Perda por naturalização, casamento ou serviço militar
- Quebra de linha (ex: mulher antes de 1948 na Itália)
- Legitimação, adoção

### 3. Classificação

- **ALTA** — documentação provavelmente disponível, linha contínua
- **MÉDIA** — possível com pesquisa adicional
- **BAIXA** — improvável por quebra legal
- **INVIÁVEL** — impossível com dados atuais

### 4. Relatório

Gerar tabela: país, geração, probabilidade, prazo, custo, documentos, próximos passos.

---

## Parte 2 — Imigração Geral

### Perfil do imigrante

Nacionalidade, idade, formação, experiência, idiomas, finanças, objetivo.

### Vias por modalidade

Consultar `references/immigration-pathways.md`.

**Trabalho:** Canadá (Express Entry), Alemanha (Blue Card, 5 anos para cidadania), Austrália (SkillSelect), Portugal (D2), EUA (H-1B), UK (Skilled Worker), Irlanda (Critical Skills).

**Estudo:** Canadá (PGWP→Express Entry), Alemanha (Job Seeker Visa), Irlanda (Stamp 1G).

**Investimento:** Portugal (€500k fundos), Grécia (€250k-800k imóvel), Malta (€150k).

**Reunião familial:** cônjuge, filhos, pais.

**Aposentadoria:** Portugal D7 (€760/mês), Grécia (€2k/mês).

### Planejamento financeiro

Taxas, exames, traduções, apostilamentos, idioma, passagens, custo de vida inicial.

### Cronograma

Mês 1-2: documentos e exames. Mês 3-4: submissão. Mês 4-8: processamento. Mês 8-10: aprovação. Mês 10-12: mudança.

---

## Parte 3 — Documentos e Legalização

Cadeia documental contínua: Usuário → Pais → Avós → Bisavós.

Apostilamento (Convenção de Haia): obrigatório para documentos brasileiros no exterior.

Tradução juramentada: por tradutor público concursado.

---

## Parte 4 — Fontes Genealógicas e Pesquisa Documental

### Plataformas de árvore genealógica

Consultar `references/genealogy-sources.md` para detalhes completos, APIs e contatos.

**Ordem recomendada de pesquisa:**
1. **FamilySearch** (gratuito, API gratuita, 1,8 bilhão de pessoas)
2. **Antenati** (Itália, registros civis 1809–1900+, gratuito)
3. **Tombo.pt** (Portugal, registros paroquiais, gratuito)
4. **AdatbázisokOnline** (Hungria, registros civis de Budapeste, gratuito)
5. **Archiwa Państwowe + Genealogia w Archiwach** (Polônia, gratuito)
6. **Geneanet** (Europa, especialmente França, freemium)
7. **Findmypast** (Reino Unido e Irlanda, pago)
8. **Ancestry** (30 bilhões de registros, pago)
9. **MyHeritage** (61M árvores, freemium)

### API FamilySearch (gratuita)
- **URL:** https://api.familysearch.org/platform/
- **Como obter chave:** https://www.familysearch.org/innovate/apply
- **Endpoints:** Person, Ancestry, Descendancy, Search, Match, Places, Memories
- **Docs:** https://www.familysearch.org/en/developers/docs/api/resources
- **Parceiros oficiais:** Ancestry, MyHeritage, Findmypast

### Fluxo de pesquisa em fontes oficiais

**Etapa 1 — Coleta familiar:** Nomes, datas aproximadas, cidades, religião, mudanças de nome.

**Etapa 2 — Plataformas gratuitas:**
- FamilySearch → buscar ancestral e cadeia completa
- Antenati → certidão civil italiana
- Civil Online (PT) → certidão portuguesa
- GRO online (UK) → certidão britânica
- IrishGenealogy.ie → certidão irlandesa

**Etapa 3 — Validação oficial:**
- Certidão de Nascimento do ascendente (obrigatória)
- CNN (Certidão Negativa de Naturalização) — para Itália
- Certidões de Casamento — toda a cadeia

**Etapa 4 — Obtenção online (quando disponível):**
- **Portugal:** civilonline.mj.pt (€10)
- **Espanha:** sede.mjusticia.gob.es
- **Alemanha:** verwaltung.bund.de
- **Reino Unido:** gro.gov.uk (£7–11)
- **Irlanda:** irishgenealogy.ie (€6)

**Etapa 5 — Legalização:**
- Apostilamento em cartório (Convenção de Haia)
- Tradução juramentada por tradutor público
- Conferência tripla de nomes/datas/locais

### Estratégias por país de origem

| Origem | Fonte principal | Fonte secundária |
|---------|----------------|------------------|
| Itália | Antenati + Comune | FamilySearch + Museu da Imigração |
| Portugal | Tombo.pt + Civil Online | Torre do Tombo |
| Alemanha | Standesamt + Bundesarchiv | FamilySearch |
| Hungria | AdatbázisokOnline | FamilySearch |
| Polônia | Archiwa Państwowe | Geneanet |
| Irlanda | IrishGenealogy.ie + GRO | Findmypast |
| Espanha | Sede Mjusticia + R Civil | FamilySearch |

---

## Pesquisa em tempo real (Composio)

Quando o usuário precisar de dados atualizados, usar Firecrawl via Composio:
1. `composio search "cidadania italiana 2026"` para ferramentas relevantes
2. `composio execute FIRECRAWL_SEARCH -d '{"q":"query","limit":5}'` para buscar dados
3. `composio execute FIRECRAWL_SCRAPE -d '{"url":"...","formats":["markdown"]}'` para extrair conteúdo

Isso garante dados sempre atualizados sobre mudanças nas leis de cidadania e imigração.

---

## Perguntas diagnósticas

1. De quais países seus ascendentes vieram?
2. Tem certidões de avós/bisavós?
3. Algum ascendente se naturalizou brasileiro?
4. Já possui outra cidadania?
5. Objetivo: passaporte, morar fora, ou manter como opção?

---

## Avisos

- **NÃO é aconselhamento jurídico** — é orientação baseada em pesquisa de fontes oficiais
- **⚠️ Mudanças recentes (2024–2026):** Itália, Alemanha, Portugal e Canadá mudaram leis
- Leis de imigração mudam frequentemente — verificar com consulado ou advogado
- Quando não souber, dizer explicitamente e indicar fonte oficial
- Erro em documentos = atraso de meses ou indeferimento

---

## Fontes oficiais

- [IRCC Canadá](https://www.canada.ca/en/immigration-refugees-citizenship.html)
- [EU Immigration Portal](https://immigration-portal.ec.europa.eu/)
- [USCIS](https://www.uscis.gov/)
- [UK Visas](https://www.gov.uk/browse/visas-immigration)
- [BAMF Alemanha](https://www.bamf.de/)
- [INIS Irlanda](https://www.irishimmigration.ie/)
- [DFA Irlanda Cidadania](https://www.dfa.ie/citizenship/)
- [Hungarian Consulate LA](https://losangeles.mfa.gov.hu/eng/page/hungarian-citizenship)
- [Normattiva Itália](https://www.normattiva.it/)
- [HCCH Apostille](https://www.hcch.net/en/instruments/conventions/specialised-sections/apostille)
- [FamilySearch](https://www.familysearch.org/)
- [FamilySearch Developers API](https://developers.familysearch.org)
- [Antenati Itália](https://antenati.cultura.gov.it/)
- [MyHeritage](https://www.myheritage.com/)
- [Ancestry](https://www.ancestry.com/)
- [Geneanet](https://www.geneanet.org/)
- [Findmypast](https://www.findmypast.com/)
- [Tombo.pt](https://tombo.pt/)
- [Arquivo Torre do Tombo](https://antt.dglab.gov.pt/)
- [Civil Online Portugal](https://www.civilonline.mj.pt)
- [Sede Mjusticia Espanha](https://sede.mjusticia.gob.es)
- [Verwaltung.bund.de](https://verwaltung.bund.de)
- [GRO Reino Unido](https://www.gro.gov.uk/)
- [IrishGenealogy.ie](https://www.irishgenealogy.ie/)
- [AdatbázisokOnline Hungria](https://adatbazisokonline.mnl.gov.hu/)
- [Archiwa Państwowe Polônia](https://archiwa.gov.pl/)
- [National Archives UK](https://www.nationalarchives.gov.uk/)
- [Ellis Island](https://www.libertyellisfoundation.org/)
- [Bundesarchiv](https://www.bundesarchiv.de/)
- [NARA EUA](https://www.archives.gov/)
- [Library Archives Canada](https://www.bac-lac.gc.ca/)
- [Archives France](https://www.culture.gouv.fr/Thematiques/Archives)
- [Archivo Indias](https://www.culturaydeporte.gob.es/archivos-aga.html)
- [Arquivo Nacional Brasil](https://www.arquivonacional.gov.br/)
- [Museu da Imigração SP](https://museudaimigracao.org.br/)
