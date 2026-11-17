# SDD — Editorial Refinement Engine (ERE)

Módulo: Editorial Refinement Engine 
Versão: 1.1 
Status: Draft revisado

## 1. Objetivo

Desenvolver um mecanismo de refinamento editorial responsável por transformar textos produzidos por modelos generativos em conteúdo mais natural, consistente e adequado ao perfil editorial do usuário, sem alterar fatos nem simular engano sobre a origem do texto. A proposta continua sendo produzir qualidade próxima à de um editor humano, agora com maior governança, auditabilidade, avaliação e adaptabilidade multicanal.

## 2. Motivação

Modelos generativos frequentemente produzem texto com estrutura repetitiva, conectores previsíveis, baixo ritmo de leitura, pouca personalidade editorial e contextualização limitada. Ferramentas e práticas de avaliação de conteúdo gerado por LLM indicam que qualidade não deve ser tratada como uma métrica única, mas como combinação de fidelidade, legibilidade, aderência de estilo e utilidade para o caso de uso.

## 3. Arquitetura

```text
Crawler
 │
 ▼
Parser
 │
 ▼
Resumo IA
 │
 ▼
════════════════════════════════════════════════════
Editorial Refinement Engine
════════════════════════════════════════════════════
 │
 ├── Style Selector
 ├── Structure Engine
 ├── Intro Generator
 ├── Rhythm Engine
 ├── Lexical Engine
 ├── Connector Engine
 ├── Context Engine
 ├── Editorial Persona
 ├── Fact Preservation Layer
 │ ├── Entity Lock Tool
 │ ├── Quote Protector Tool
 │ └── Claim Extractor Tool
 ├── Governance Layer
 │ ├── Editorial Rules Engine
 │ ├── Versioning & Audit Log Tool
 │ └── Human Review Copilot
 ├── Optimization Layer
 │ ├── SEO Intent Skill
 │ ├── Multichannel Adaptation Skill
 │ └── Localization Skill
 ├── Evaluation Layer
 │ ├── AI Auditor
 │ ├── Readability Analyzer
 │ ├── Style Diff Tool
 │ └── Quality Score
 └── Prompt Chain Orchestrator
 │
 ▼
Preview
 │
 ▼
WordPress / RSS / Social / Newsletter / CMS
```

## 4. Skills adicionais

### 4.1 Fact Preservation Skill

Responsável por garantir preservação factual entre texto de entrada, resumo IA e texto refinado. Deve identificar e travar entidades nomeadas, números, datas, valores monetários, cargos, relações e citações literais antes da reescrita.

### 4.2 Brand Voice Skill

Responsável por aprender padrões editoriais a partir de artigos aprovados, rejeitados e editados manualmente. O objetivo é modelar preferências por domínio, publicação, editoria ou organização, sem depender apenas de parâmetros fixos de estilo.

### 4.3 SEO Intent Skill

Responsável por alinhar o texto ao objetivo editorial e de busca: intenção, cobertura de entidades, organização de headings, meta description, slug e elementos úteis para publicação. Há amplo ecossistema de ferramentas gratuitas de análise SEO e textual que mostram viabilidade operacional para esse tipo de componente.

### 4.4 Compliance & Risk Skill

Responsável por identificar linguagem de risco, afirmações absolutas, promessas sensíveis e ausência de ressalvas em domínios regulados, como saúde, finanças e jurídico. Deve operar como camada de alerta e não como mecanismo de censura automática.

### 4.5 Multichannel Adaptation Skill

Responsável por adaptar o mesmo conteúdo-base para WordPress, RSS, newsletter, LinkedIn, redes sociais e snippets de distribuição editorial. Assistentes editoriais voltados a publishers já enfatizam otimização e transferência de conteúdo para canais distintos.

### 4.6 Human Review Copilot Skill

Responsável por apresentar sugestões aprováveis, diffs explicáveis e justificativas das transformações realizadas. Esse skill reduz atrito com revisão humana e melhora a auditoria do pipeline.

### 4.7 Summarization Quality Skill

Responsável por avaliar a qualidade do resumo IA anterior ao refinamento, medindo cobertura, omissões, compressão e risco de distorção. O refinamento editorial não deve mascarar falhas de origem do resumo.

### 4.8 Localization Skill

Responsável por adaptar o conteúdo a idioma, convenções culturais, variantes regionais e expectativa de leitura do público-alvo, indo além de tradução literal.

## 5. Tools adicionais

### 5.1 Entity Lock Tool

Congela nomes, números, datas, percentuais, cargos, URLs e outros elementos críticos antes do refinamento. Qualquer alteração posterior exige justificativa e rastreio.

### 5.2 Claim Extractor Tool

Extrai afirmações verificáveis do texto original, do resumo IA e do texto refinado, permitindo comparar se surgiram claims não autorizados.

### 5.3 Quote Protector Tool

Preserva citações literais, trechos regulatórios e blocos marcados como intocáveis, impedindo paráfrases indevidas.

### 5.4 Prompt Chain Orchestrator

Executa etapas curtas e especializadas de transformação textual com possibilidade de rollback, versionamento e isolamento de responsabilidade por etapa. Esse modelo torna o pipeline mais previsível do que um único prompt monolítico.

### 5.5 Style Diff Tool

Compara original e refinado, classificando mudanças em estrutura, ritmo, léxico, tom, contexto, SEO e legibilidade.

### 5.6 Editorial Rules Engine

Aplica guias editoriais programáveis por projeto, incluindo voz ativa, limite de tamanho de título, política de siglas, estilo de intertítulos, uso de links e padrões de capitalização.

### 5.7 Readability Analyzer

Calcula legibilidade, densidade sintática, tamanho médio de frase, dispersão de parágrafos, uso de voz passiva e escaneabilidade. Há ferramentas gratuitas e open source para esse tipo de análise, incluindo Hemingway, Datayze, Textorum e Eclipse Readability Studio.

### 5.8 SEO Annotation Tool

Gera title, excerpt, slug, headings sugeridos, FAQ editorial e outras anotações úteis para publicação e distribuição. Ferramentas gratuitas de SEO já cobrem parte desse tipo de análise, o que favorece uma implementação inicial híbrida.

### 5.9 Source Context Retriever

Recupera contexto apenas das fontes já coletadas pelo pipeline de coleta do usuário, respeitando a regra de não inventar fatos.

### 5.10 Versioning & Audit Log Tool

Armazena entrada, saída, prompts, scores, alertas, diffs e decisões humanas de aprovação. Essa camada é essencial para debugging, compliance e melhoria contínua.

## 6. Classificação de custo das skills e tools

### 6.1 Matriz de licenciamento e custo

| Item | Categoria | Classificação | Observação |
|---|---|---|---|
| Fact Preservation Skill | Skill interna | Open source / desenvolvimento próprio | Pode ser implementada com NLP open source e regras próprias; não costuma existir pronta e gratuita como solução completa. |
| Brand Voice Skill | Skill interna | Desenvolvimento próprio / possivelmente paga | Normalmente exige embeddings, histórico editorial e ajuste fino sobre dados internos. |
| SEO Intent Skill | Skill híbrida | Freemium / gratuita parcial | Pode começar com ferramentas SEO gratuitas e evoluir para motor próprio. |
| Compliance & Risk Skill | Skill interna | Desenvolvimento próprio / possivelmente paga | Em domínios regulados, tende a exigir regras e taxonomias próprias. |
| Multichannel Adaptation Skill | Skill interna | Desenvolvimento próprio | Pode ser construída internamente a partir de templates e prompts por canal. |
| Human Review Copilot Skill | Skill interna | Desenvolvimento próprio | Valor está na UX de revisão, no diff e no workflow editorial. |
| Summarization Quality Skill | Skill interna | Open source / desenvolvimento próprio | Pode usar métricas e checagens automatizadas com LLM evals e regras. |
| Localization Skill | Skill híbrida | Desenvolvimento próprio / freemium | Pode usar modelos e glossários próprios; parte de tradução pode vir de serviços externos. |
| Entity Lock Tool | Tool interna | Open source / desenvolvimento próprio | Implementável com NER, regex, validação semântica e regras locais. |
| Claim Extractor Tool | Tool interna | Open source / desenvolvimento próprio | Pode usar pipelines NLP/LLM para extração estruturada de claims. |
| Quote Protector Tool | Tool interna | Open source / desenvolvimento próprio | Simples de construir com marcação e preservação de spans. |
| Prompt Chain Orchestrator | Tool de orquestração | Open source / freemium / paga | Pode ser implementado com frameworks próprios ou de workflow; categoria costuma ter opções abertas e comerciais. |
| Style Diff Tool | Tool interna | Open source / desenvolvimento próprio | Pode ser implementado com diff semântico e regras de classificação de mudanças. |
| Editorial Rules Engine | Tool interna | Open source / desenvolvimento próprio | Regras editoriais são naturalmente codificáveis e customizadas. |
| Readability Analyzer | Tool analítica | Gratuita / open source / freemium | Há opções grátis e open source já disponíveis para análise de legibilidade. |
| SEO Annotation Tool | Tool analítica | Gratuita parcial / freemium | Muitos componentes de análise SEO têm versão gratuita ou uso limitado sem custo. |
| Source Context Retriever | Tool interna | Desenvolvimento próprio | Depende do pipeline de coleta e da base do próprio produto. |
| Versioning & Audit Log Tool | Tool interna | Open source / desenvolvimento próprio | Pode usar banco, eventos e logging internos sem licença adicional. |

### 6.2 Itens explicitamente gratuitos ou com opção gratuita conhecida

Com base nas referências coletadas, os componentes abaixo têm suporte claro em ferramentas gratuitas ou open source, ao menos para MVP parcial:

- Readability Analyzer, com alternativas como Hemingway, Datayze, Textorum e Eclipse Readability Studio.
- SEO Intent Skill e SEO Annotation Tool em modo inicial, com apoio de Ahrefs Free Tools, Semrush Free Tools, SmallSEOTools e analisadores gratuitos de texto SEO.
- Parte da instrumentação de avaliação textual, com ferramentas gratuitas de legibilidade e análise estrutural.

### 6.3 Itens que tendem a exigir desenvolvimento próprio

Os itens abaixo não aparecem como soluções amplamente gratuitas e prontas para uso completo no contexto editorial descrito, sendo mais adequados para implementação interna:

- Brand Voice Skill.
- Compliance & Risk Skill.
- Human Review Copilot Skill.
- Editorial Rules Engine.
- Source Context Retriever.
- Versioning & Audit Log Tool.

## 7. Componentes originais revisados

### 7.1 Style Selector

Responsável por selecionar o estilo editorial com base em categoria, idioma, domínio e perfil do projeto.

Entrada:
- categoria
- idioma
- configuração do site
- perfil editorial

Saída:

```json
{
 "style": "journalistic"
}
```

Estilos suportados:
- Jornalístico
- Revista
- Tecnologia
- Corporativo
- Financeiro
- Acadêmico
- Institucional
- Minimalista

### 7.2 Structure Engine

Responsável por variar a estrutura do artigo por tipo de conteúdo, objetivo editorial e canal de publicação.

### 7.3 Rhythm Engine

Responsável por alternar frases curtas e longas, reduzir períodos excessivos, evitar monotonia sintática e reorganizar parágrafos para melhorar fluxo de leitura.

### 7.4 Lexical Engine

Responsável por enriquecer o vocabulário e controlar repetição por pesos, prioridade contextual e blacklist de clichês.

### 7.5 Intro Generator

Responsável por variar introduções com seleção pseudoaleatória parametrizada por estilo, canal, tema e nível de refinamento.

### 7.6 Connector Engine

Responsável por diversificar conectores e reduzir previsibilidade estrutural em transições discursivas.

### 7.7 Context Engine

Responsável por enriquecer contexto sem inventar fatos, utilizando apenas material já coletado no pipeline do produto.

### 7.8 Editorial Persona

Permite que cada site tenha um perfil como:

```yaml
style: technology
tone: neutral
verbosity: medium
humor: false
opinion_level: low
paragraph_size: medium
sentence_length: mixed
seo: true
```

### 7.9 AI Auditor

Executado após o refinamento para verificar repetição lexical, repetição sintática, voz passiva, frases longas, excesso de listas, conectores repetidos e clichês.

### 7.10 Quality Score

Pontuação geral baseada em score composto, com maior transparência analítica.

Subscores sugeridos:
- Factual Fidelity
- Editorial Naturalness
- Readability
- Style Adherence
- SEO Utility
- Reviewability

Fórmula sugerida:

\[
Q = 0.30F + 0.20N + 0.15R + 0.20S + 0.10E + 0.05V
\]

A lógica segue a recomendação de usar métricas específicas ao problema, em vez de um único indicador genérico de qualidade.

## 8. Pipeline revisado

```text
Texto IA
 ▼
Summarization Quality Skill
 ▼
Fact Preservation Skill
 ▼
Style Selector
 ▼
Structure Engine
 ▼
Intro Generator
 ▼
Rhythm Engine
 ▼
Lexical Engine
 ▼
Connector Engine
 ▼
Context Engine
 ▼
Editorial Persona
 ▼
SEO Intent Skill
 ▼
Localization Skill
 ▼
AI Auditor
 ▼
Readability Analyzer
 ▼
Style Diff Tool
 ▼
Quality Score
 ▼
Human Review Copilot
 ▼
Texto Final
```

## 9. Configuração por projeto

```yaml
editorial:
 enabled: true
 style: journalistic
 refinement_level: 60
 ai_auditor: true
 seo: true
 context_enrichment: true
 lexical_variation: true
 rhythm_adjustment: true
 connector_variation: true
 intro_variation: true
 fact_preservation: true
 entity_lock: true
 quote_protection: true
 claim_extraction: true
 readability_analysis: true
 style_diff: true
 human_review_copilot: true
 multichannel_adaptation: true
 localization: true
 versioning: true
 audit_log: true
```

## 10. Refinement level

Escala de 0–100:
- 0: texto praticamente original.
- 25: correções leves.
- 50: reestruturação moderada.
- 75: estilo editorial completo.
- 100: reescrita profunda mantendo fidelidade aos fatos.

## 11. API

### 11.1 Refinamento editorial

`POST /api/editorial/refine`

```json
{
 "text": "...",
 "style": "journalistic",
 "level": 70,
 "language": "pt-BR"
}
```

Resposta:

```json
{
 "text": "...",
 "quality_score": 94,
 "changes": 18,
 "editorial_style": "journalistic",
 "subscores": {
 "factual_fidelity": 98,
 "editorial_naturalness": 91,
 "readability": 89,
 "style_adherence": 94,
 "seo_utility": 88,
 "reviewability": 92
 }
}
```

### 11.2 Estilos

`GET /api/editorial/styles`

Retorna estilos disponíveis.

### 11.3 Perfis editoriais

`GET /api/editorial/profiles`

Lista perfis cadastrados.

### 11.4 Diff editorial

`POST /api/editorial/diff`

Compara original e refinado, retornando mudanças classificadas por tipo.

### 11.5 Auditoria

`GET /api/editorial/audit/{id}`

Retorna histórico de execução, prompts, scores, alertas e aprovação humana.

## 12. Interface

Nova seção em `Configurações → Editorial`.

Itens:
- Perfil Editorial
- Estilo
- Tom
- Criatividade
- SEO
- Contextualização
- Refinamento
- Idioma
- Público-alvo
- Compliance
- Fidelidade factual
- Revisão humana
- Canal de publicação

Pré-visualização:
- Original
- Refinado
- Diff estruturado

Indicadores:
- Quality Score
- Subscores
- Legibilidade
- Tempo estimado de leitura
- Alterações realizadas
- Risco factual
- Alertas de compliance

## 13. Critérios de aceite

- O texto refinado preserva integralmente os fatos.
- O estilo corresponde ao perfil configurado.
- Não há repetições excessivas.
- O score mínimo de qualidade é 85.
- O subscore de fidelidade factual deve ser maior ou igual a 95 em ambientes de produção sensíveis.
- O tempo adicional de processamento não ultrapassa 10 segundos por artigo.
- Todas as transformações são registradas para auditoria.
- O diff entre original e refinado pode ser explicado ao usuário/editor.

