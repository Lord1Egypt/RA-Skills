---
name: ghl-lead-qualifier
description: Skill de qualificação conversacional automática para leads do GoHighLevel (GHL). Conduz a triagem inteligente via WhatsApp (usando o gateway STEVO / SMS), extrai informações de orçamento/nicho e atualiza as etapas no Kanban.
triggers:
  - qualificar lead
  - triagem ghl
  - lead qualifier
  - qualificador whatsapp
  - stevo whatsapp
---

# GHL Lead Qualifier Skill (STEVO / WhatsApp Engine)
**Desenvolvido por / Créditos:** Rafa Martins (rafacpti@gmail.com)

---

## 🚀 Onboarding & Setup Rápido (Primeiro Uso)

Ao executar a skill pela primeira vez:
1. Exibir checklist visual de status `[OK]` / `[PENDENTE]`.
2. Obtenha seu token de acesso MCP Habilis no portal de desenvolvedores: [https://ia.sthub.com.br](https://ia.sthub.com.br).
3. Obtenha seu GHL Private Integration Token e Location ID nas configurações do GoHighLevel.
4. Assegure que as variáveis de ambiente locais estejam definidas:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export GHL_API_KEY="pit-..."
   export GHL_LOCATION_ID="your_location_id"
   ```

---

Esta skill dita a lógica de inteligência conversacional para o Hermes interagir com novos leads que chegam pelo Webhook ou pelo GHL.

---

## 📱 CANAL DE COMUNICAÇÃO: STEVO INTEGRATION
No GoHighLevel desta conta, o WhatsApp está conectado através do app **STEVO (Marketplace AppId: 682cd9287059b4173d8b17bd)**, que utiliza a rota do tipo **SMS (`TYPE_CUSTOM_SMS`)**.

### ⚠️ Regra de Ouro no Disparo de Mensagens:
Ao enviar mensagens via API v2 do GHL ou via `ghl_client.py`, passe o parâmetro de canal como `SMS` (ou `WhatsApp`). O STEVO intercepta a chamada de SMS e entrega como **mensagem de WhatsApp nativa** no celular do lead!

---

## 🧠 FLUXO DE TRIAGEM AUTOMÁTICA EM 3 PASSOS

1. **Mensagem de Abertura Imparável & Tratamento de Inbound:**
   - Envia um texto direto, sem cara de robô:
   *"Olá {nome}! Vi que você solicitou informações. Qual é a sua prioridade no momento?"*
   - **Reações a mensagens enviadas:** Se a mensagem inbound for uma reação emoji (`Reaction: 💯`, `Reaction: ❤️`, etc.) a um comunicado ou oferta, classifique imediatamente como **Engajamento Ativo / Lead Quente** e responda com o próximo passo da oferta.
   - **Mensagens de abertura / cortesia:** Para mensagens curtas receptivas ("Tudo na paz", "Olá"), envie texto de triagem para identificar a necessidade do cliente (ex: Segurança Eletrônica, TI, PAPI Cloud).
   - **Interesse Direto em Produtos/Cursos/IA (ex: "quero MBA AI"):** Classifique imediatamente como **Lead Quente / Produto AI** e dispare apresentação e link de matrícula ou proposta.
   - **Negociação Comercial Ativa (ex: "conseguiu formular a proposta"):** Classifique como **Negociação Ativa / Proposta Comercial** e priorize o envio da proposta pendente.
   - **Dúvidas Técnicas & Instâncias PAPI (ex: "license blocked", "erro ao criar instância"):** Classifique como **Suporte Crítico / PAPI Instâncias** e priorize no topo da auditoria para liberação de licença/instância no painel.
   - **Áudios Transcritos (`Audio Message. Transcription: ...`):** O gateway STEVO transcreve notas de voz recebidas; extraia o texto transcrito para qualificar a intenção normalmente.
   - **Códigos 2FA / Relay SMS de Plataformas (ex: códigos do Facebook/Meta):** Descarte do funil comercial e classifique como **Notificação de Sistema / 2FA**.
   - **Mensagens de erro de template:** Se o corpo da mensagem contiver tags não interpretadas (`%referencia%`, `%http_retorno%`), marque como **Erro de Integração** para auditoria técnica.

2. **Extração de Qualificadores:**
   - O Hermes lê a resposta do lead e classifica em:
     - **Lead Quente:** Orçamento disponível / Urgência imediata $\to$ Aplica tag `lead-quente` e move para a etapa `Interesse identificado` no Kanban.
     - **Lead Frio:** Sem orçamento / Apenas curioso $\to$ Aplica tag `lead-frio` e move para nutrir no GHL.

3. **Atualização do CRM (GHL API v2):**
   ```bash
   python3 /root/.hermes/metaads/ghl_client.py --action update_opp_stage --opp-id <OPP_ID> --stage-id <STAGE_ID>
   ```

   ---

   ## 📚 REFERÊNCIAS & GUIAS SUPORTE
   - Para detalhes e arquétipos de classificação de conversas da fila de espera, consulte `references/unanswered_leads_triaging_patterns.md`.
