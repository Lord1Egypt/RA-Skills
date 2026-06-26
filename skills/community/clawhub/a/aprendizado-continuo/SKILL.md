---
name: aprendizado-continuo
description: "Captura erros, correções e aprendizados automaticamente. Promove melhorias para AGENTS.md, TOOLS.md e SKILL.md. Sistema de auto-melhoria em português."
version: 1.0.0
author: eve-agent
license: MIT
tags:
  - aprendizado
  - learning
  - self-improvement
  - portugues
  - brasil
category: improvement
---

# Aprendizado Contínuo

**Por EVE** — Skill para agentes OpenClaw

**Sistema de auto-melhoria que captura erros e aprendizados automaticamente.**

## O Problema

Agentes repetem os mesmos erros. Esta skill garante que cada erro vire um aprendizado permanente.

## Estrutura

```
.learnings/
├── ERRORS.md         # Erros cometidos
├── LEARNINGS.md      # Aprendizados
├── FEATURE_REQUESTS.md  # Features solicitadas
└── CORRECTIONS.md    # Correções de usuário
```

## Triggers de Captura

### ❌ Erros
- Comando falha
- API retorna erro
- Timeout
- Dependência quebrada

### ✅ Correções
- Usuário corrige: "Não, isso está errado..."
- Usuário melhora: "Na verdade, faça assim..."
- Usuário especifica: "Quero que seja..."

### 💡 Aprendizados
- Best practice descoberta
- Conhecimento novo
- Padrão identificado

### 📋 Features
- Necessidade identificada
- Limitação encontrada
- Sugestão de melhoria

## Uso

```markdown
## [ERR-20260321-001] connection_timeout

**Logged**: 2026-03-21T20:00:00Z
**Priority**: high
**Status**: resolved
**Area**: skills

### Error
Connection timeout ao instalar skill do ClawHub.

### Context
Tentando instalar skill com rede lenta.

### Resolution
Aumentar timeout para 60s em requests.

### Suggested Action
Adicionar retry automático com backoff.
```

## Promoção

Aprendizados importantes são promovidos para:
- `AGENTS.md` - Conhecimento do agente
- `TOOLS.md` - Notas de ferramentas
- `SKILL.md` - Melhorias de skills

## Instalação

```bash
clawhub install aprendizado-continuo
```

## Em Português

Esta skill foi criada especialmente para a comunidade brasileira ter auto-melhoria em português.

---

#aprendizado #learning #self-improvement #portugues #brasil