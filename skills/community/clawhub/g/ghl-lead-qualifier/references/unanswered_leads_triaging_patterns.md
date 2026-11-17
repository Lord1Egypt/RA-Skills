# Padrões de Triagem e Classificação de Leads no GHL (Conversas Não Respondidas)

Ao analisar a fila de conversas pendentes de resposta extraídas via `ghl_client.py --action unanswered`, classifique as mensagens segundo os arquétipos abaixo para definir a ação adequada:

---

## 1. 💼 Comercial & Fechamento Imediato (🔥 Lead Quente)
- **Padrão:** Confirmação de escopo, solicitação/cobrança de formalização de proposta (*"ok formaliza a proposta pra podermos avaliar"*, *"quando consegue finalizar?"*, *"essa obra seria em Vitória ES"*, *"Temos essas localidades... Consegue atender alguma? Teria interesse?"*).
- **Ação:** Prioridade máxima. Enviar proposta comercial formalizada (com condições de pagamento/entrada alinhadas), cronograma e confirmação de prazo / raio de atendimento.
- **Tag GHL:** `lead-quente`, `interesse-confirmado`, `aguardando-proposta`.

---

## 2. 🚚 Cotações Operacionais, Fornecedores & Logística (🟡 Operacional / Suprimentos)
- **Padrão:** Cotação de listas de materiais, alinhamento de quem compra/instala (*"Muito material pra cotar"*, *"nós que instalamos e compramos tudo?"*), pedidos de frete ou envio de equipamentos.
- **Ação:** Alinhar escopo de fornecimento vs serviço, enviar relação de itens para cotação com fornecedores parceiros e responder com prazos de entrega.
- **Tag GHL:** `operacional-logistica`, `cotacao-pendente`, `parceiro-fornecedor`.

---

## 3. 🛠️ Chamados Técnicos & Faturamento (🟢 Suporte / Financeiro / Terceirização)
- **Padrão:** Notificações de chamados concluídos, números de chamado técnico e valores (*"Chamado: 1000008604 valor 120 obrigada"*), alinhamento de chamado em campo (*"Quem te acionou referente a este chamado?"*, *"amanha quem vai te acompanhar é a analista X"* com vCard).
- **Ação:** Validar no ERP/sistema financeiro ou com o analista designado, gerar 

---

## 4. 🚨 Suporte Técnico Crítico & Instâncias PAPI (🔴 Suporte Técnico / Licença)
- **Padrão:** Mensagens relatando erros de ativação, licença bloqueada ou falha ao criar instâncias (*"Ok . Eu tento criar insrancia e informa license bloqued"*, *"license blocked"*, *"erro ao criar instância"*).
- **Ação:** Prioridade Alta. Verificar status da licença/conta no painel PAPI (papi.api.br), realizar o desbloqueio ou liberação de créditos e orientar o cliente no WhatsApp.
- **Tag GHL:** `suporte-tecnico`, `licenca-bloqueada`, `papi-instancia`.

---

## 5. 🎓 Interesse Direto em Educação & MBA AI (🔥 Lead Quente - Produto)
- **Padrão:** Mensagens diretas buscando informações sobre cursos, capacitações ou MBA (*"quero MBA AI"*, *"como funciona o MBA"*).
- **Ação:** Lead Quente. Enviar apresentação do programa, grade curricular e link de inscrição/atendimento comercial.
- **Tag GHL:** `lead-quente`, `mba-ai`, `interesse-educacao`. fatura/faturamento correspondente e confirmar acompanhamento técnico.
- **Tag GHL:** `chamado-finalizado`, `suporte-eunerd`, `financeiro-pendente`.

---

## 4. 📅 Agendamentos & Visitas (🟢 Agendamento)
- **Padrão:** Confirmação de horários ou datas de reunião (*"Coloquei às 09h, tudo bem?"*).
- **Ação:** Validar disponibilidade na agenda, confirmar presença e enviar convite de calendário.
- **Tag GHL:** `agendamento-confirmado`.

---

## 5. 🚨 Alertas Operacionais de Clientes Ativos (🚨 Alerta)
- **Padrão:** Reporte de sistemas parados, falhas em condomínio parceiro (*"Tudo parado aqui"*).
- **Ação:** Prioridade técnica. Acionar suporte de campo imediatamente e responder ao cliente informando que a equipe técnica foi destacada.
- **Tag GHL:** `alerta-operacional`, `suporte-urgente`.

---

## 6. 🤖 Broadcasts e Mensagens Institucionais (⚪ Sem Ação)
- **Padrão:** Comunicados de grupos externos, webinários, eventos de comunidades terceiras (*"Falta pouco, galera! No dia 31..."*).
- **Ação:** Não responder de forma automatizada (evita ruído em grupos/comunidades).
