# 🏢 GoHighLevel (GHL) CRM v2 & Lead Automation Engine
### *Automação Completa de CRM, Pipelines e Triagem de Leads no GoHighLevel*

<p align="center">
  <img src="assets/logo.png" alt="GoHighLevel Logo" width="120" height="120" />
</p>

<p align="center">
  <a href="https://clawhub.ai"><img src="https://img.shields.io/badge/ClawHub-Skill-blue.svg" alt="ClawHub Skill" /></a>
  <a href="https://xvix.com.br"><img src="https://img.shields.io/badge/Habilis-MCP%20Gateway-purple.svg" alt="Habilis MCP Gateway" /></a>
  <img src="https://img.shields.io/badge/Security-Zero_Storage_Stateless-blueviolet.svg" alt="Zero Storage" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT" />
</p>

---

## 🇺🇸 English

### Overview
**GoHighLevel (GHL) Integration** connects AI agents directly to the **GoHighLevel API v2**. It enables autonomous contact creation and deduplication, opportunity Kanban stage transitions, unanswered lead triage, workflow triggers, and direct multi-channel messaging.

### 🚀 Quick Onboarding & First-Time Setup
1. **Get your Habilis MCP Token & GHL Credentials**:
   - Access the developer portal at [https://xvix.com.br](https://xvix.com.br) to generate your access token.
   - Obtain your GHL Private Integration Token and Location ID in your GoHighLevel sub-account settings.
2. **Configure Environment Variables**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export GHL_API_KEY="pit-..."
   export GHL_LOCATION_ID="your_ghl_location_id"
   ```
3. **Configure Hermes / OpenClaw (`config.yaml`)**:
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```
4. **Run Doctor Diagnostic**:
   ```bash
   python3 scripts/ghl_client.py list-pipelines
   ```

### Key Capabilities
- 👥 **Contact Management**: Search, create, update, and enrich leads with tags and custom fields.
- 📋 **Opportunity Pipeline Automation**: Move deals across Kanban stages automatically based on conversation outcomes.
- ⏰ **Unanswered Lead Triage**: Detects and follows up on cold or unresponsive prospects automatically.
- 🔒 **Zero-Storage Security**: GHL Private Integration tokens stay exclusively on your local machine.

---

## 🇧🇷 Português

### Visão Geral
A skill **GoHighLevel (GHL) Integration** conecta agentes de IA diretamente à **API v2 do GoHighLevel**. Permite gerenciar contatos, mover oportunidades no funil de vendas (Kanban), identificar leads sem resposta, disparar fluxos e enviar mensagens multicanal.

### 🚀 Onboarding Rápido & Primeiro Uso
1. **Obtenha seu Token Habilis MCP & Credenciais GHL**:
   - Acesse o portal de desenvolvedores em [https://xvix.com.br](https://xvix.com.br) para gerar seu token de acesso.
   - Obtenha seu Token de Integração Privada e Location ID no painel do GoHighLevel (Configurações ➡️ Integrações Privadas).
2. **Configure as Variáveis de Ambiente**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export GHL_API_KEY="pit-..."
   export GHL_LOCATION_ID="seu_ghl_location_id"
   ```
3. **Conecte o MCP no Hermes / OpenClaw (`config.yaml`)**:
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```
4. **Execute o Teste de Conexão**:
   ```bash
   python3 scripts/ghl_client.py list-pipelines
   ```

### Principais Recursos
- 👥 **Gestão Completa de Leads**: Criação, busca e atualização com tags personalizadas.
- 📋 **Movimentação no Kanban**: Atualização automática de estágios de negócio no funil de vendas.
- ⏰ **Triagem de Leads Sem Resposta**: Identificação proativa e reengajamento automatizado.
- 🔒 **Privacidade Zero-Storage**: Tokens do GHL permanecem protegidos no seu ambiente local.

---

## 📦 Installation / Instalação

```bash
hermes skills install ghl-integration
# or via clawhub
clawhub install ghl-integration
```
