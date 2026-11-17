# Instagram Follow-Gate & GoHighLevel (GHL) Sync Pattern

## 🎯 Conceito e Arquitetura do Follow-Gate
A Meta proíbe disparos ativos de DM para usuários que apenas clicaram em "Seguir" (política anti-spam da Instagram Graph API). Para abrir a janela de mensageria de 24 horas, o lead precisa iniciar uma interação ativa:
1. Comentário em publicação / Reels ("QUERO", "PAPI", etc.)
2. Envio de Mensagem Direta (DM)
3. Resposta a Story / Menção

### Fluxograma de Execução:
```
[ Comentário no Post/Reels / DM Inbound ]
                   │
                   ▼
       [ Webhook Meta Graph API ]
                   │
                   ▼
     [ Checagem: Segue a Conta Business? ]
          /                       \
        NÃO                       SIM
        /                           \
[ Portão Fechado (GATE_LOCKED) ]   [ Portão Aberto (GATE_UNLOCKED) ]
[ Envia DM: Peça para seguir ]     [ Entrega Link/Recompensa ]
[ Quick Reply: "Já Segui" ]        [ Cria Contato GHL com Tags ]
                                   [ Move Card no Kanban GHL ]
```

---

## 🛠 Modelos de Implementação (3 Vias)

### Via 1: GoHighLevel Nativo (Sem Servidor Intermediário)
1. Conectar perfil em: **GHL ➔ Settings ➔ Integrations ➔ Facebook & Instagram**.
2. Criar Workflow em **Automation ➔ Workflows**:
   - **Gatilho:** `Customer Replied` (Filtro: `Reply Channel = Instagram Direct`).
   - **Ação 1:** Verificar tag / condição ou enviar resposta com botão de confirmação.
   - **Ação 2:** Adicionar Tag `Instagram-Follower-Convertido`.
   - **Ação 3:** Criar/Atualizar Oportunidade no pipeline do Kanban.

### Via 2: ManyChat como Gateway
1. Conectar Instagram no ManyChat.
2. Criar regra de automação: Disparo em comentários de Reels ou palavras-chave de DM ("QUERO").
3. ManyChat executa checagem de seguidor (`user.follows_business_account`).
4. Ao desbloquear, ManyChat faz requisição HTTP `POST` para o Webhook do GoHighLevel.

### Via 3: Servidor Próprio / Meta Graph API (`/root/instagram_crm_automation`)
1. Servidor Python FastAPI/HTTPS rodando em porta local (ex: `8095`).
2. Webhook Meta registrado no portal *developers.facebook.com* com assinatura em `messages` e `messaging_postbacks`.
3. Script `instagram_follow_gate.py` faz o dispatch direto na API v2 do GHL via `ghl_kommo_client.py`.

---

## 🔌 Endpoints GoHighLevel API v2 Utilizados

### 1. Upsert de Contato
- **Endpoint:** `POST Habilis MCP Gateway (https://xvix.com.br/api/mcp)
- **Headers:**
  - `Authorization: Bearer <GHL_ACCESS_TOKEN>`
  - `Version: 2021-07-28`
  - `Content-Type: application/json`
- **Tags padrão:** `["Instagram-Follower-Convertido", "PAPI-Lead-Quente"]`
- **Custom Field:** `instagram_username`

### 2. Criação / Movimentação de Oportunidade no Kanban
- **Endpoint:** `POST Habilis MCP Gateway (https://xvix.com.br/api/mcp)
- **Campos essenciais:**
  - `locationId`: ID da subconta GHL
  - `contactId`: ID retornado no upsert
  - `pipelineId`: ID do pipeline (ex: `eVCpOc3uOHjw9SaraCgL`)
  - `pipelineStageId`: ID da etapa (ex: `e3e6f7fd-bc5e-4103-903f-de1ecf4b4e49`)
  - `monetaryValue`: Valor da oportunidade (ex: `49.90`)
  - `status`: `open`

---

## ⚠️ Checklist de Troubleshooting & Armadilhas Críticas

1. **Permissão de Mensagens no App Instagram (Causa #1 de DMs não recebidas):**
   * No app do Instagram no celular da conta:
     👉 **Configurações e privacidade ➔ Mensagens e respostas a stories ➔ Ferramentas de mensagens ➔ Ativar 'Permitir acesso às mensagens'**.
   * Se essa chave estiver desligada, a Meta silencia e bloqueia 100% dos webhooks e respostas de bots/APIs para DMs.

2. **Tipo de Conta Instagram:**
   * A conta deve ser **Profissional (Empresarial ou Criador de Conteúdo)** e vinculada à Página do Facebook. Contas pessoais não têm acesso à Graph API de mensageria.

3. **Escopos de Token no GHL (Erro 403 Forbidden):**
   * Se chamadas para `/conversations/search` ou `/contacts/` retornarem `403 Forbidden`, verificar os escopos concedidos ao Token na Private Integration (`conversations.readonly`, `contacts.write`, `opportunities.write`).

4. **Janela de 24 Horas da Meta:**
   * Respostas automáticas só são permitidas dentro da janela de 24h após o último envio de mensagem pelo usuário. Fora dessa janela, apenas templates de mensagens aprovados ou notificações pontuais são autorizados.
