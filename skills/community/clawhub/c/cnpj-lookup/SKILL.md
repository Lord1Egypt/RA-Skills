---
name: cnpj-lookup
version: "1.0.0"
description: Consulta CNPJ via APIs públicas brasileiras (BrasilAPI, CNPJ.ws, OpenCNPJ) com fallback automático, cache e rate limit. Ativar quando o usuário pedir consulta, pesquisa ou detalhes de CNPJ, razão social, situação cadastral, CNAE, QSA ou endereço de empresa.
author: Klaus (OpenClaw)
tags: [cnpj, consulta, brasil, empresa, cnae, qsa]
---

# CNPJ Lookup 🔍

Consulta empresas brasileiras via CNPJ usando APIs públicas com fallback automático.

## Início Rápido

```
"Consultar CNPJ 12.345.678/0001-95"
"Pesquisar empresa pelo CNPJ 19131243000197"
"Me diga razão social, situação cadastral, CNAE principal, endereço e QSA"
"Detalhe do CNPJ 19131243000197 em JSON"
```

## Workflows

### Workflow 1: Consulta Simples (Resumo)
O usuário pede apenas informações básicas:
- Razão social
- Nome fantasia
- Situação cadastral
- Endereço resumido

**Prompt típico:** "consultar cnpj 19131243000197"

### Workflow 2: Consulta Completa (Detalhes + QSA)
O usuário pede informações detalhadas incluindo:
- CNAE principal e secundários
- Quadro de Sócios e Administradores (QSA)
- Contato (email, telefone)
- Capital social

**Prompt típico:** "consulta completa do CNPJ 19131243000197" ou "detalhes QSA"

### Workflow 3: Exportar JSON
O usuário quer dados estruturados para integração:
- Retorna JSON com schema normalizado
- Inclui metadados (fonte, cache, timestamp)

**Prompt típico:** "cnpj 19131243000197 json" ou "exportar dados CNPJ"

## Como Funciona

1. **Validação**: CNPJ é sanitizado (só dígitos) e verifica dígitos verificadores
2. **Cache**: Consulta anterior retorna dados em cache (TTL: 24h)
3. **Fallback em cascata**:
   - BrasilAPI → CNPJ.ws → OpenCNPJ
4. **Rate Limit**: Respeita limites de cada provider (30/2/30 req/min)
5. **Normalização**: Output padronizado independente do provider

## Execução via Script

```bash
# Consulta completa (já vem com detalhes por padrão: QSA, CNAEs, etc)
python3 scripts/cnpj_lookup.py 19131243000197

# Consulta com JSON
python3 scripts/cnpj_lookup.py 19131243000197 --json

# Forçar provider específico
python3 scripts/cnpj_lookup.py 19131243000197 --provider brasilapi

# Ignorar cache
python3 scripts/cnpj_lookup.py 19131243000197 --no-cache

# TTL customizado (em segundos)
python3 scripts/cnpj_lookup.py 19131243000197 --ttl 3600

# Consulta simples (apenas基本信息)
python3 scripts/cnpj_lookup.py 19131243000197 --detailed False
```

## Referências

- [Provedores](./references/providers.md) - Endpoints, limites e comportamento de rate limit
- [Campos](./references/fields.md) - Schema normalizado e divergências entre provedores

## Aviso

> Dados para consulta/enriquecimento; não substitui documento oficial.
