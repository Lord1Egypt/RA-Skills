# Zero-Touch Orchestration & Dynamic Webhook Architecture
**Créditos:** Rafa Martins (rafacpti@gmail.com)

## 1. Zero-Touch Headless Setup (Orquestrador)
Para implantar o agente de forma 100% automatizada sem perguntas interativas no terminal:
- Exporte as variáveis de ambiente antes de executar `./install.sh`:
  - `META_ACCESS_TOKEN`: Token de acesso de longa duração.
  - `META_AD_ACCOUNT_ID`: Conta principal de anúncios (ex: `act_327126129438619`).
  - `MONITORED_AD_ACCOUNTS`: `all` ou lista de contas separadas por vírgula.
  - `GHL_LOCATION_ID`: ID da subconta no GoHighLevel.
  - `GHL_API_KEY`: API Key / PIT v2 Token do GHL.
  - `CRON_FREQ`: Frequência do agendador (ex: `every 6h`).
  - `ALERT_DELIVER`: Destino dos alertas (`origin`, `whatsapp`, `telegram`, `discord`, `local`).

O script detecta a presença de `META_ACCESS_TOKEN` e `META_AD_ACCOUNT_ID` e desativa todas as perguntas `read -p`.

---

## 2. Roteamento Dinâmico de Webhook (`ghl_webhook_server.py`)
O servidor de webhook suporta dois modos de recebimento:

1. **Rota Genérica de Tenant Único:**
   - URL: `http://<IP>:<PORT>/webhook`
   - O servidor lê a variável de ambiente `GHL_LOCATION_ID` injetada na inicialização do serviço.

2. **Rota Multi-Tenant:**
   - URL: `http://<IP>:<PORT>/webhook/<LOCATION_ID>`
   - O servidor sobrescreve dinamicamente a `GHL_LOCATION_ID` para a requisição em questão, permitindo que a mesma instância atenda múltiplos clientes ou subcontas sem conflito de rotas.
