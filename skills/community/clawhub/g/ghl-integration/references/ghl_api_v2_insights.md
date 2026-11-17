# GoHighLevel API v2 Integration Insights

## ⚠️ Pitfall Crítico: Cloudflare Error 1010 (Access Denied)
- **Causa:** Os endpoints `Habilis MCP Gateway (https://xvix.com.br/api/mcp) e `Habilis MCP Gateway (https://xvix.com.br/api/mcp) utilizam proteção Cloudflare WAF rigorosa que bloqueia silenciosamente User-Agents padrão de bibliotecas Python (`Python-urllib/3.x`, `requests/x.y`) com `HTTP 403 Forbidden` / `Error 1010: Access denied`.
- **Solução Obrigatória:** Toda requisição HTTP para a API v2/v1 do LeadConnector/GHL DEVE enviar um header `User-Agent` personalizado de navegador ou cliente válido (ex: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`).

```python
headers = {
    "Authorization": f"Bearer {ghl_token}",
    "Version": "2021-07-28",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
```

## ⚠️ Limitações Importantes de Webhook na API v2
- **Criação Programática de Webhook:** A API v2 do GoHighLevel não permite criar ou assinar Webhooks via endpoint `/webhooks/` com chaves de Location (Private Integration Tokens / PIT).
- **Solução de Automação:** 
  1. **Configuração Visual:** O usuário adiciona a ação HTTP POST de Webhook dentro do Workflow visual do GHL.
  2. **Path Multi-Tenant:** A URL do Webhook deve incluir o Location ID do cliente (`/webhook/<GHL_LOCATION_ID>`) para permitir o roteamento isolado de contatos no servidor `ghl_webhook_server.py`.
  3. **Fallback Polling:** Caso o cliente prefira não criar o Webhook visual, o Cron Job com a ação `--action unanswered` realiza a varredura autônoma via API REST a cada ciclo.
