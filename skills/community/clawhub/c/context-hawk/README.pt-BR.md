# 🦅 Context-Hawk

> **Guardião de Memória Contextual de IA** — Pare de perder o fio, comece a lembrar o que importa.

*Dê a qualquer agente de IA uma memória que realmente funciona — através de sessões, tópicos e tempo.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## O que ele faz

A maioria dos agentes de IA sofrem de **amnésia** — cada nova sessão começa do zero. O Context-Hawk resolve isso com um sistema de gerenciamento de memória de nível de produção que captura automaticamente o que importa, deixa o ruído sumir e lembra o que é certo na hora certa.

**Sem Context-Hawk:**
> "Eu já te disse — prefiro respostas concisas!"
> (próxima sessão, o agente esquece de novo)

**Com Context-Hawk:**
> (aplica silenciosamente suas preferências de comunicação desde a sessão 1)
> ✅ Entrega resposta concisa e direta toda vez

---

## ❌ Without vs ✅ With Context-Hawk (TODO: translate)

| Scenario | ❌ Without Context-Hawk | ✅ With Context-Hawk |
|----------|------------------------|---------------------|
| **New session starts** | Blank — knows nothing about you | ✅ Injects relevant memories automatically |
| **User repeats a preference** | "I told you before..." | Remembers from day 1 |
| **Long task runs for days** | Restart = start over | Task state persists via `hawk resume` |
| **Context gets large** | Token bill skyrockets | 5 compression strategies keep it lean |
| **Duplicate info** | Same fact stored 10 times | SimHash dedup — stored once |
| **Memory recall** | All similar, redundant injection | MMR diverse recall — no repetition |
| **Memory management** | Everything piles up forever | 4-tier decay — noise fades, signal stays |
| **Self-improvement** | Repeats the same mistakes | importance + access_count tracking → smart promotion |
| **Multi-agent team** | Each agent starts fresh | Shared memory via LanceDB |

---

## ✨ 12 Funcionalidades Principais

---

## ✨ 12 Funcionalidades Principais

| # | Funcionalidade | Descrição |
|---|---------|-------|
| 1 | **Persistência de Estado de Tarefa** | `hawk resume` — persiste o estado, retoma após reinício |
| 2 | **Memória de 4 Camadas** | Working → Short → Long → Archive com decaimento Weibull |
| 3 | **JSON Estruturado** | Pontuação de importância (0-10), categoria, camada, camadas L0/L1/L2 |
| 4 | **Pontuação de Importância IA** | Pontua automaticamente as memórias, descarta conteúdo de baixo valor |
| 5 | **5 Estratégias de Injeção** | A(alta-imp) / B(relacionada à tarefa) / C(recente) / D(top5) / E(completa) |
| 6 | **5 Estratégias de Compressão** | summarize / extract / delete / promote / archive |
| 7 | **Auto-Introspecção** | Verifica clareza da tarefa, informações faltantes, detecção de loop |
| 8 | **Busca Vetorial LanceDB** | Opcional — busca híbrida vetorial + BM25 |
| 9 | **Fallback Memória Pura** | Funciona sem LanceDB, persistência JSONL |
| 10 | **Autodeduplicação** | Mescla automaticamente memórias duplicadas |
| 11 | **MMR Recall** | Maximal Marginal Relevance — diverse recall, no repetition |
| 12 | **6-Category Extraction** | LLM-powered: fact / preference / decision / entity / task / other |

---

## 🚀 Instalação Rápida

```bash
# Instalação em uma linha (recomendado)
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# Ou diretamente via pip
pip install context-hawk

# Com todas as funcionalidades (incluindo sentence-transformers)
pip install "context-hawk[all]"
```

---

## 📦 Memória de Estado de Tarefa (Funcionalidade Mais Valiosa)

Mesmo após reinício, queda de energia ou troca de sessão, Context-Hawk continua exatamente de onde parou.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "Completar a documentação da API",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Revisar template de arquitetura", "Relatar ao usuário"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["Cobertura deve alcançar 98%", "APIs devem ser versionadas"],
  "resumed_count": 3
}
```

```bash
hawk task "Completar a documentação"  # Criar tarefa
hawk task --step 1 done             # Marcar passo concluído
hawk resume                           # Retomar após reinício ← ESSENCIAL!
```

---

## 🧠 Memória Estruturada

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Conteúdo original completo",
  "summary": "Resumo em uma linha",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Pontuação de Importância

| Pontuação | Tipo | Ação |
|-------|------|--------|
| 0.9-1.0 | Decisões/regras/erros | Permanente, decaimento mais lento |
| 0.7-0.9 | Tarefas/preferências/conhecimento | Memória de longo prazo |
| 0.4-0.7 | Diálogo/discussão | Curto prazo, decaimento para arquivo |
| 0.0-0.4 | Chat/mensagens de saudação | **Descartar, nunca armazenar** |

---

## 🎯 5 Estratégias de Injeção de Contexto

| Estratégia | Gatilho | Economia |
|----------|---------|---------|
| **A: Alta Importância** | `importância ≥ 0.7` | 60-70% |
| **B: Relacionada à Tarefa** | scope coincide | 30-40% ← padrão |
| **C: Recente** | últimos 10 turnos | 50% |
| **D: Top5 Recall** | top 5 `access_count` | 70% |
| **E: Completa** | sem filtro | 100% |

---

## 🗜️ 5 Estratégias de Compressão

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 Sistema de Alerta de 4 Níveis

| Nível | Limiar | Ação |
|-------|--------|--------|
| ✅ Normal | < 60% | Silencioso |
| 🟡 Observação | 60-79% | Sugerir compressão |
| 🔴 Crítico | 80-94% | Pausar escrita automática, forçar sugestão |
| 🚨 Perigo | ≥ 95% | Bloquear escritas, compressão obrigatória |

---

## 🚀 Início Rápido

```bash
# Instalar plugin LanceDB (recomendado)
openclaw plugins install memory-lancedb-pro@beta

# Ativar skill
openclaw skills install ./context-hawk.skill

# Inicializar
hawk init

# Comandos essenciais
hawk task "Minha tarefa"    # Criar tarefa
hawk resume             # Retomar última tarefa ← MUITO IMPORTANTE
hawk status            # Ver uso de contexto
hawk compress          # Comprimir memória
hawk strategy B        # Mudar para modo relacionado à tarefa
hawk introspect         # Relatório de auto-introspecção
```

---

## Auto-Trigger: A Cada N Turnos

A cada **10 turnos** (padrão, configurável), Context-Hawk automaticamente:

1. Verifica nível de contexto
2. Avalia importância das memórias
3. Relata status ao usuário
4. Sugere compressão se necessário

```bash
# Configuração (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # verificar a cada N turnos
  "keep_recent": 5,                 # preservar últimos N turnos
  "auto_compress_threshold": 70      # comprimir quando > 70%
}
```

---

## Estrutura de Arquivos

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Ferramenta CLI Python
└── references/
    ├── memory-system.md           # Arquitetura de 4 camadas
    ├── structured-memory.md      # Formato de memória e importância
    ├── task-state.md           # Persistência de estado de tarefa
    ├── injection-strategies.md  # 5 estratégias de injeção
    ├── compression-strategies.md # 5 estratégias de compressão
    ├── alerting.md             # Sistema de alerta
    ├── self-introspection.md   # Auto-introspecção
    ├── lancedb-integration.md  # Integração LanceDB
    └── cli.md                  # Referência CLI
```

---

## Especificações Técnicas

| | |
|---|---|
| **Persistência** | Arquivos JSONL locais, sem banco de dados |
| **Busca vetorial** | LanceDB (opcional) + sentence-transformers embedding local, fallback automático para arquivos |
| **Busca** | BM25 + busca vetorial ANN + fusão RRF |
| **Provedores de Embedding** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **Cross-Agent** | Universal, sem lógica de negócio, funciona com qualquer agente de IA |
| **Zero-Config** | Funciona pronto para uso (modo BM25-only) |
| **Python** | 3.12+ |

---

## Licença

MIT — livre para usar, modificar e distribuir.
