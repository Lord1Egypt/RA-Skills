# GHL Unanswered Leads Triaging & Pattern Recognition

When querying unanswered conversations using `ghl_client.py --action unanswered`, incoming messages fall into these primary categories requiring specific actions:

## 1. Billing / Financial Inquiries (Dúvidas de Faturamento)
- **Patterns:** Mentions of "fatura", "vencimento", "boleto", "segunda via", "pix", "comprovante", "pagamento".
- **Example:** "aqui a fatura vence hoje. Queria ver se tem como você me dar o valor" (Amanda Patricia)
- **Classification:** 🟡 **Dúvida Financeira / Faturamento**
- **Action:** Route to billing support or generate/send the invoice payment link/barcode.

## 2. Automated System / Balance Alerts (Notificações de Sistema)
- **Patterns:** System balance templates, e.g. "Seu saldo atual é de *R$ X*", "Créditos insuficientes", "Mensagem do sistema".
- **Classification:** 🤖 **Notificação de Sistema STEVO/Papi**
- **Action:** Ignore / No response needed (automated outbound check).

## 3. Integration / Unparsed Template Errors (Erros de Integração)
- **Patterns:** Raw template variable place-holders like `%referencia%`, `%http_retorno%`, `{referencia}`, `%status%`.
- **Classification:** ⚠️ **Erro de Integração**
- **Action:** Flag for technical audit; fix the automated workflow/template rendering in GHL or n8n.

## 4. Active Engagement & Reaction Emojis
- **Patterns:** Emojis like `Reaction: 💯`, `Reaction: ❤️`, `Reaction: 👍` in response to broadcast announcements.
- **Classification:** 🔥 **Lead Quente (Engajamento Ativo)**
- **Action:** Send next offer step or schedule automated follow-up.

## 5. Short Inbound / Greeting Messages (Abertura / Cortesia)
- **Patterns:** "oi", "olá", "tudo bem?", "boa noite", "bom dia". Single-word or short receptive messages.
- **Classification:** 💬 **Abertura / Cortesia**
- **Action:** Respond with standard welcoming qualification prompt.

## 6. Technical Support & Activation Blocked (Erro de Licença / Instância Bloqueada)
- **Patterns:** "license blocked", "licença bloqueada", "erro ao criar instância", "instancia bloqueada", "não consigo conectar qr code", "falha na ativação".
- **Example:** "Ok . Eu tento criar insrancia e informa license bloqued" (Seguro Veicular)
- **Classification:** 🚨 **Suporte Crítico / Desbloqueio de Ativação**
- **Action:** Prioridade máxima. Verificar status da licença/assinatura no painel administrativo PAPI / PostgreSQL e liberar a criação da instância antes do churn do lead.

## 7. Checkout Abandonment & High Intent (Checkout Iniciado / Pacote)
- **Patterns:** Tags `customer_event`, `event_checkout_started`, `plano_pacote_X` sem pagamento imediato.
- **Classification:** 🔥 **Lead Quente / Recuperação de Checkout**
- **Action:** Enviar mensagem personalizada de apoio técnico e incentivo de fechamento.

## 8. Third-Party Broadcast / Newsletter Filtering (Transmissões Externas)
- **Patterns:** Mensagens longas com links externos de lançamento de outros produtos (ex.: `evolutionfoundation.com.br/lancamento`), DDI internacional corporativo (`+1203...`), grupos/comunidades salvas no CRM.
- **Classification:** 🚫 **Broadcast de Terceiros / Descartar**
- **Action:** Filtrar da fila de triagem ativa, ignorar ou marcar como lido sem gerar alerta falso positivo.
