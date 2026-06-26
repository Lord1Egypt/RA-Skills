# Convex + Obsidian - Integração de Memória Persistente

## 🎯 Objetivo
Memória persistente **automática** para o OpenClaw:
- **Convex (Hot)**: Salva cada conversa automaticamente
- **Obsidian (Deep)**: Conhecimento histórico consolidado
- **Busca Híbrida**: Contexto de memória injetado quando relevante

## ✅ Status: OPERACIONAL

## Arquitetura

```
Usuário fala → OpenClaw processa
     ↓
[Auto-save] → Convex (memória recente)
     ↓
Se detectar referência ao passado:
     ↓
[Busca Híbrida] → Convex + Obsidian
     ↓
[Contexto injetado] → "Lembre-se que ontem..."
```

## Componentes

### 1. Backend Convex
- **URL**: `https://energized-goshawk-977.convex.cloud`
- Schema: `convex/schema.ts`
- Funções: `convex/memory.ts`

### 2. Scripts Python

| Script | Função |
|--------|--------|
| `memory.py` | CLI completo (save/search/stats) |
| `search.py` | Busca híbrida (Convex + local) |
| `hook.py` | Integração automática (chamado pelo OpenClaw) |

### 3. CLI Tools

```bash
# Busca híbrida
./search.sh "nvidia" -n 5

# Salvar manualmente
./memory.sh save "Conteúdo" --session main-2026-03-27

# Estatísticas
./memory.sh stats
```

## Integração Automática no OpenClaw

### Opção 1: Hook pós-mensagem (Recomendado)

Editar `~/.openclaw/openclaw.json` para adicionar um hook:

```json
{
  "skills": {
    "entries": {
      "convex-obsidian": {
        "autoSave": true,
        "autoContext": true,
        "deploymentUrl": "https://energized-goshawk-977.convex.cloud"
      }
    }
  }
}
```

**Comportamento:**
- Cada mensagem salva automaticamente no Convex
- Se usuário mencionar "ontem", "antes", "lembra" → busca contexto
- Contexto injetado no início da resposta

### Opção 2: Comandos manuais

```
/memory search <query>     # Busca híbrida
/memory save <texto>       # Salvar no Convex
/memory context            # Ver contexto atual
```

### Opção 3: Via ferramenta memory_search

O OpenClaw já usa `memory_search` para buscar em arquivos locais.
Para incluir Convex, usar:

```python
# skills/convex-obsidian/search.py
./search.sh "query" --json
```

## Uso Atual (Testado)

```bash
cd /home/andrey/.openclaw/workspace/skills/convex-obsidian

# Buscar em ambas as fontes
./search.sh "amw" -n 5
./search.sh "nvidia configuracao" --json

# Salvar memória
./memory.sh save "Cliente pediu orçamento" \
  --session main-2026-03-27 \
  --tags cliente orcamento \
  --importance 8

# Salvar no Obsidian
./memory.sh save-obsidian "Resumo reunião..." \
  --title "Reunião Cliente XYZ" \
  --folder "05-AMW/Reuniões"
```

## Configuração de Variáveis

```bash
# ~/.openclaw/.env ou exportar
export CONVEX_DEPLOYMENT_URL="https://energized-goshawk-977.convex.cloud"
export VAULT_PATH="/home/andrey/Vault"
```

## Deploy/Redeploy do Convex

Se precisar atualizar o backend:

```bash
cd /home/andrey/.openclaw/workspace/skills/convex-obsidian

# Usar a chave preview
export CONVEX_DEPLOY_KEY="109326a5533f411792dae76dc8ae3f6f"
npx convex@latest deploy --preview-create openclaw-memory

# Ou com a chave completa
export CONVEX_DEPLOY_KEY="preview:andrey-tsushima:openclaw|eyJ2MiI6IjEwOTMyNmE1NTMzZjQxMTc5MmRhZTc2ZGM4YWUzZjZmIn0="
npx convex@latest deploy --preview-create openclaw-memory
```

## Exemplo de Busca Híbrida

```
$ ./search.sh "amw" -n 5

🔍 Resultados para: 'amw'
   Fontes: 2 Convex + 3 local

1. 🔥 convex://... (score: 3.80)
   [CONVEX - conversation] Cliente AMW pediu orçamento...

2. 📄 memory/2026-03-19.md (score: 0.70)
   Análise Técnica Integral de Inexecução — AMW...
```

## Próximos Passos (Para Integração Total)

1. **Auto-save**: Hook no ciclo de vida do OpenClaw
2. **Auto-context**: Detectar quando buscar memórias
3. **Sincronização**: Mover Convex → Obsidian após 30 dias
4. **Embeddings**: Busca semântica além de keyword

## Notas

- Convex gratuito: 1M operações/mês (suficiente)
- Obsidian: Armazenamento local ilimitado
- Latência: Convex ~50-100ms, Obsidian ~10ms
