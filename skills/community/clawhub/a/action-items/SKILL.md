---
name: "action-items"
description: "Extrai tarefas, prazos e responsáveis de atas, transcrições ou notas de reunião. Gera lista organizada de action items com prioridade e dono."
metadata:
  - productivity
  - meeting
  - task
  - management
  - organization
  - workflow
allowed-tools:
  - read
  - write
  - memory_search
  - memory_get
user-invocable: true
---

# Action Items Tracker 📋🎯

Transforma atas de reunião, transcrições e notas soltas em uma lista organizada de action items — com dono, prazo, prioridade e status. Acaba com aquele clássico "quem faz o quê até quando?"

## Público-Alvo

Profissionais que participam de reuniões (todo mundo). Especialmente útil para: gerentes de projeto, coordenadores, equipes ágeis, freelancers com clientes, estagiários.

## Trigger

Invocar quando o usuário:
- Compartilhar notas de reunião / ata
- Pedir "extrair action items"
- Falar "organizar tarefas dessa reunião"
- Dizer "oque ficou pendente da reunião?"
- Enviar transcrição de reunião
- Pedir "follow-up" de uma reunião

## Diferenciais

1. **Extração inteligente** — Lê notas soltas e identifica o que é ação (verbos no futuro, "precisamos", "vou", "fica pra", "até dia") vs. o que é apenas informação.
2. **Prioridade automática** — Detecta urgência pelo contexto: "urgente", "ASAP", "prazo curto", "bloqueio" → prioridade alta. "Alinhar", "avaliar", "verificar" → prioridade normal.
3. **Detecção de dono** — Identifica quem é o responsável pela ação ("João vai fazer", "Eu cuido", "Maria fica com").
4. **Pré-formatado para ferramentas** — Gera saída pronta pra copiar pro Trello, Notion, Asana, ou lista de tarefas.
5. **Follow-up automático** — Se usado mais de uma vez, pergunta se ações passadas foram concluídas e gera status.
6. **Resumo da reunião + ações** — Junto com os action items, gera um mini-resumo do que foi decidido.
7. **Inferência de prazo** — Se a reunião for hoje e não tiver prazo explícito, pergunta ou assume um prazo padrão (próxima reunião / 7 dias).

## Workflow

### Passo 1: Receber as notas

O usuário pode enviar:

**Notas de reunião estruturadas:**
```
Reunião projeto X - 15/06
- João vai finalizar o layout até sexta
- Maria precisa aprovar o orçamento
- Eu fico com a integração do gateway
- urgente: resolver bug do login
- Próxima reunião: 22/06
```

**Notas soltas (o que realmente acontece):**
```
reuniao projeto
layout - joao finalizar
orcamento maria aprovar
gateway - eu
bug login urgente
prox reuniao 22/06
```

**Transcrição de reunião (texto corrido):**
```
"Então pessoal, o João vai finalizar o layout até sexta-feira. Maria, você pode aprovar o orçamento? E eu fico com a integração do gateway. Ah, e tem um bug no login que é urgente, alguém pega?"
```

### Passo 2: Processar e extrair

1. Analisar o texto e identificar:
   - **Ações:** frases com verbo no futuro, "vou", "precisamos", "fica pra", "até [data]"
   - **Donos:** nomes mencionados, "eu" → perguntar quem é, "você" → detectar pelo contexto
   - **Prazos:** datas, "sexta", "semana que vem", "até dia X", "ASAP", "urgente"
   - **Prioridades:** palavras-chave (urgente, crítico, bloqueio → alta; normal → média; sem pressa → baixa)
2. Agrupar em uma tabela/lista limpa.
3. Gerar resumo da reunião.
4. Perguntar se o usuário quer salvar para follow-up futuro.

### Passo 3: Gerar saída

#### Modo Padrão (WhatsApp)

```
📋 *ACTION ITEMS — Reunião Projeto X*
📅 Data: 15/06/2026

*🔴 Alta Prioridade*
• Resolver bug do login — *dono: ?* — prazo: URGENTE
  → Ninguém foi designado. Quem pega?

*🟡 Média Prioridade*
• Finalizar layout — dono: *João* — prazo: 19/06 (sexta)
• Aprovar orçamento — dono: *Maria* — prazo: ? ⁉️
  → Qual o prazo, Maria?

*🟢 Baixa Prioridade*
• Integrar gateway de pagamento — dono: *eu (André)* — prazo: 22/06

*📌 Resumo da Reunião*
Definidas as tarefas da sprint do Projeto X. Layout em andamento, orçamento pendente de aprovação, gateway integrado na sequência. Bug do login precisa de atenção imediata.

*📅 Próxima Reunião:* 22/06/2026
```

#### Modo Export (para copiar pro Trello/Notion)

```
# Action Items - Projeto X (15/06)

## 🔴 Alta
- [ ] Resolver bug do login | Dono: ? | Prazo: URGENTE

## 🟡 Média
- [ ] Finalizar layout | Dono: João | Prazo: 19/06
- [ ] Aprovar orçamento | Dono: Maria | Prazo: ?

## 🟢 Baixa
- [ ] Integrar gateway | Dono: André | Prazo: 22/06
```

#### Modo Follow-up (segunda reunião)

Quando o usuário chamar a skill de novo para uma reunião do mesmo projeto:

```
📋 *FOLLOW-UP — Reunião Projeto X (22/06)*

📊 *Status das ações passadas:*
✅ Finalizar layout — *Concluído* 🎉
❌ Aprovar orçamento — *Pendente* ⚠️
🔄 Integrar gateway — *Em andamento (70%)*
❌ Resolver bug login — *Não iniciado* 🚨

🎯 *Novos Action Items desta reunião:*
...
```

## Regras de Extração

- **Verbo + nome = ação:** "João vai finalizar" → ação + dono
- **"Eu"** → perguntar "Quem é você?" na primeira execução, salvar em memória
- **Datas relativas:** "sexta" → próxima sexta, "semana que vem" → data correta baseada no timestamp
- **"Urgente", "crítico", "ASAP", "bloqueio"** → prioridade ALTA
- **"Importante", "prioridade"** → prioridade MÉDIA
- **"Verificar", "avaliar", "depois", "se der tempo"** → prioridade BAIXA
- Manter o que foi **decidido** separado do que é **ação** — nem tudo que é dito é ação.
- Se não houver dono explícito pra uma ação: marcar como "?" e perguntar pra quem.

## Notes

- Se as notas forem muito longas (>2000 chars), resumir primeiro o essencial da reunião e depois extrair ações.
- Se o usuário disser "eu" sem contexto, perguntar: "Quem é você na reunião? (pra eu saber quais ações são suas)"
- Para follow-up, manter histórico em memória (usar memory_search/memory_get).
- Idealmente, perguntar no final: "Quer que eu salve pra acompanhar na próxima reunião?"
- WhatsApp-friendly: bullet lists, sem tabelas markdown, uso de emojis pra categorizar.

---
⭐ *Gostou desta skill?* Deixe uma estrela no [ClawHub](https://clawhub.ai) para ajudar outros a encontrá-la!
