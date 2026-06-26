---
name: clawwork
description: Execute tarefas profissionais via ClawWork - transforme Zero em um coworker de IA economicamente viável. Use quando precisar executar trabalhos complexos, gerar documentos, realizar análises ou automatizar tarefas profissionais com medição de custo/benefício.
metadata:
  openclaw:
    emoji: 💰
    requires:
      bins: ["python3"]
---

# ClawWork Skill

Integração com ClawWork para execução de tarefas profissionais com tracking econômico.

## O que é

ClawWork transforma o assistente em um "coworker de IA" que:
- Executa tarefas profissionais reais (220 tarefas em 44 setores)
- Paga por tokens utilizados
- Ganha "dinheiro" ao completar tarefas com qualidade
- Mantém balance econômico (sobrevivência)

## Comandos

### CLI

```bash
# Status dos agentes
skill clawwork status

# Comparar modelos
skill clawwork compare

# Executar tarefa (requer E2B_API_KEY)
skill clawwork run -t "Criar análise de mercado"
skill clawwork run -t "Gerar plano de marketing" -m kimi-coding/k2p5
```

### Uso Direto

```bash
# Via script
/home/freedom/.openclaw/workspace/skills/clawwork/clawwork.sh status

# Via Python
python /home/freedom/.openclaw/workspace/skills/clawwork/cli.py status
```

## Setup

### 1. Configurar API Keys

Edite `~/.openclaw/workspace/ClawWork/.env`:

```bash
# OpenRouter (já configurado ✅)
OPENAI_API_KEY=sk-or-v1-xxx
OPENAI_API_BASE=https://openrouter.ai/api/v1

# E2B - necessário para execução de código
# Obtenha gratuitamente em: https://e2b.dev/
E2B_API_KEY=e2b_xxx
```

### 2. Iniciar Dashboard (opcional)

```bash
cd ~/.openclaw/workspace/ClawWork
./start_dashboard.sh
```

Acesse: http://localhost:3000

### 3. Testar

```bash
skill clawwork status
```

## Funcionamento

```
Usuário: /clawwork "Criar análise de mercado para SaaS B2B"

Zero → Classifica tarefa → [Technology / Software Engineer]
     → Define valor → [$50 baseado em salário BLS]
     → Executa via GLM-4.7 + ferramentas
     → Avalia qualidade → [GPT-4o scoring]
     → Calcula economics:
       💸 Custo tokens: $2.50
       💵 Pagamento: $45.00 (qualidade 90%)
       📊 Lucro: $42.50
     → Retorna resultado + métricas
```

## Dados Existentes

Já temos testes anteriores:
- **GLM-4.7**: 157 dias de logs
- **Kimi K2.5**: 220 dias de logs
- **Qwen3 Max**: 220 dias de logs

## Localização

| Componente | Path |
|------------|------|
| ClawWork | `~/.openclaw/workspace/ClawWork/` |
| Skill | `~/.openclaw/workspace/skills/clawwork/` |
| Config | `~/.openclaw/workspace/ClawWork/.env` |
| Dados | `~/.openclaw/workspace/ClawWork/livebench/data/` |

## Mais Informações

- Repositório: https://github.com/HKUDS/ClawWork
- Dataset: [GDPVal](https://openai.com/index/gdpval/)
- Leaderboard: https://hkuds.github.io/ClawWork/
