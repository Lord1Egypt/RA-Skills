# AHC-Automator: Documentação Completa

**Custom automation skill for Alan Harper Composites manufacturing workflows**

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação e Setup](#instalação-e-setup)
3. [Workflows Disponíveis](#workflows-disponíveis)
4. [Uso dos Scripts](#uso-dos-scripts)
5. [Configuração](#configuração)
6. [Troubleshooting](#troubleshooting)
7. [Manutenção](#manutenção)

---

## 🎯 Visão Geral

O AHC-Automator é um skill customizado para automatizar workflows específicos da Alan Harper Composites, integrando:

- **ClickUp**: Gerenciamento de projetos e tasks
- **Pipedrive**: CRM e gestão de deals
- **Email**: Monitoramento e processamento automatizado
- **WhatsApp**: Notificações em tempo real

### Workflows Implementados

1. **Email → ClickUp → Pipedrive Chain**: Automação completa de emails para tasks e deals
2. **Client Onboarding**: Onboarding estruturado de novos clientes
3. **Project Completion**: Sequência automatizada de conclusão de projetos

---

## 🛠️ Instalação e Setup

### Pré-requisitos

- Python 3.8+
- OpenClaw instalado e configurado
- Acesso às APIs do ClickUp e Pipedrive
- macOS com Apple Mail (para monitoramento de email)

### Setup Automático

```bash
cd /Users/andreantunes/.openclaw/workspace/skills/ahc-automator
python scripts/setup.py
```

O script de setup irá:
- Criar diretórios necessários
- Verificar dependências
- Configurar variáveis de ambiente
- Testar conectividade das APIs
- Validar configurações existentes

### Setup Manual

1. **Configurar variáveis de ambiente:**
   ```bash
   export CLICKUP_API_TOKEN="seu_token_clickup"
   export PIPEDRIVE_API_TOKEN="seu_token_pipedrive"
   ```

2. **Adicionar ao shell profile:**
   ```bash
   echo 'export CLICKUP_API_TOKEN="seu_token_clickup"' >> ~/.zshrc
   echo 'export PIPEDRIVE_API_TOKEN="seu_token_pipedrive"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verificar configuração:**
   ```bash
   python scripts/health_check.py --verbose
   ```

---

## 🔄 Workflows Disponíveis

### 1. Email → ClickUp → Pipedrive Chain

**Propósito**: Automatizar processamento de emails específicos de Ian e Ronaldo

**Como funciona**:
```
📧 Email recebido → 🔍 Parse keywords → ✅ Criar task ClickUp → 💼 Criar deal Pipedrive → 📱 Notificar WhatsApp
```

**Uso**:
```bash
# Processamento automático via cron
python scripts/email_to_clickup_pipedrive.py

# Teste com debug
python scripts/email_to_clickup_pipedrive.py --debug

# Filtrar por conta específica
python scripts/email_to_clickup_pipedrive.py --account ian@alanharpercomposites.com.br
```

**Keywords monitoradas**:
- **ClickUp**: "adicionar tarefa", "nova tarefa", "clickup", "lista de convidados"
- **Pipedrive**: "criar deal", "nova oportunidade", "adicionar contato", "pipedrive"

### 2. Client Onboarding Workflow

**Propósito**: Automatizar onboarding de novos clientes com estrutura completa

**Templates disponíveis**:
- `standard`: Projeto de composite manufacturing básico
- `aerospace`: Projeto aerospace com requisitos especiais
- `custom`: Projeto de engenharia customizada

**Uso**:
```bash
# Onboarding completo
python scripts/client_onboarding.py \
  --client "Empresa Cliente" \
  --email "contato@cliente.com" \
  --template aerospace \
  --value 50000 \
  --currency EUR

# Onboarding rápido (apenas ClickUp)
python scripts/client_onboarding.py --quick --client "Cliente Rápido"
```

**Estrutura de projeto criada**:
```
📁 [CLIENTE] - Composite Manufacturing Project
├── 📂 01 - Design & Engineering
├── 📂 02 - Material Planning
├── 📂 03 - Manufacturing
├── 📂 04 - Quality & Testing
└── 📂 05 - Delivery & Closure
```

### 3. Project Completion Sequence

**Propósito**: Automatizar conclusão de projetos com relatórios e follow-up

**Funcionalidades**:
- Geração automática de relatórios
- Trigger de faturação (opcional)
- Pesquisa de satisfação
- Notificações de stakeholders

**Uso**:
```bash
# Conclusão completa
python scripts/project_completion.py --task-id 86ad7y8rh --trigger-invoice

# Apenas relatórios
python scripts/project_completion.py --task-id 86ad7y8rh --no-survey

# Sem relatórios
python scripts/project_completion.py --task-id 86ad7y8rh --no-reports
```

---

## 📜 Uso dos Scripts

### Scripts Principais

#### email_to_clickup_pipedrive.py
```bash
python scripts/email_to_clickup_pipedrive.py [OPTIONS]

Options:
  --account TEXT    Filtrar por conta de email específica
  --debug          Ativar modo debug com logs detalhados
  --config PATH    Caminho para configuração personalizada
```

#### client_onboarding.py
```bash
python scripts/client_onboarding.py [OPTIONS]

Required:
  --client TEXT    Nome do cliente (obrigatório)

Options:
  --email TEXT     Email do cliente
  --template TEXT  Template: standard|aerospace|custom (default: standard)
  --value FLOAT    Valor do projeto em euros
  --currency TEXT  Moeda do projeto (default: EUR)
  --notes TEXT     Notas adicionais para o projeto
  --quick          Onboarding rápido (apenas ClickUp)
  --debug          Ativar modo debug
```

#### project_completion.py
```bash
python scripts/project_completion.py [OPTIONS]

Required:
  --task-id TEXT OR --project-id TEXT    ID da task/projeto (obrigatório)

Options:
  --client-name TEXT     Nome do cliente
  --no-reports          Não gerar relatórios
  --trigger-invoice     Trigger geração de fatura
  --no-survey           Não enviar pesquisa de satisfação
  --debug               Ativar modo debug
```

### Scripts de Suporte

#### health_check.py
```bash
# Check completo
python scripts/health_check.py

# Saída em JSON
python scripts/health_check.py --json

# Saída detalhada
python scripts/health_check.py --verbose
```

#### whatsapp_notifier.py
```bash
# Notificação de task criada
python scripts/whatsapp_notifier.py --type task_created --task-title "Nova Task"

# Notificação customizada
python scripts/whatsapp_notifier.py --type custom --message "Mensagem personalizada"

# Notificação de erro urgente
python scripts/whatsapp_notifier.py --type error --message "Erro crítico detectado"
```

#### setup.py
```bash
# Setup interativo
python scripts/setup.py

# Setup não-interativo
python scripts/setup.py --non-interactive

# Apenas verificar status
python scripts/setup.py --check-only
```

---

## ⚙️ Configuração

### Arquivo Principal: `configs/ahc_config.json`

```json
{
  "clickup": {
    "team_id": "90132745943",
    "default_space": "AHC Projects",
    "templates": {
      "standard": "901322408351",
      "aerospace": "901322408352",
      "custom": "901322408353"
    }
  },
  "pipedrive": {
    "api_token": "env:PIPEDRIVE_API_TOKEN",
    "default_pipeline": "AHC Manufacturing",
    "default_stage": "New Opportunity"
  },
  "email": {
    "monitor_accounts": [
      "ian@alanharpercomposites.com.br",
      "ronaldoaibot@gmail.com"
    ],
    "keywords": {
      "clickup": ["adicionar tarefa", "nova tarefa", "clickup"],
      "pipedrive": ["criar deal", "nova oportunidade", "pipedrive"]
    }
  },
  "whatsapp": {
    "notification_groups": ["AHC Team"],
    "message_templates": {
      "task_created": "✅ Nova tarefa: {task_title}",
      "deal_created": "💼 Novo deal: {deal_title}",
      "project_completed": "🎉 Projeto concluído: {project_name}",
      "client_onboarded": "👤 Novo cliente: {client_name}"
    }
  },
  "logging": {
    "level": "INFO",
    "directory": "/Users/andreantunes/.openclaw/workspace/logs/ahc-automator"
  }
}
```

### Variáveis de Ambiente

**Obrigatórias:**
- `CLICKUP_API_TOKEN`: Token da API ClickUp
- `PIPEDRIVE_API_TOKEN`: Token da API Pipedrive

**Opcionais:**
- `AHC_DEBUG`: Ativar modo debug (`true`/`false`)

### Customização

#### Adicionar Keywords
Edite `configs/ahc_config.json`:
```json
{
  "email": {
    "keywords": {
      "clickup": ["sua_palavra_chave", "outra_keyword"],
      "pipedrive": ["keyword_pipedrive"]
    }
  }
}
```

#### Modificar Templates de Mensagem
```json
{
  "whatsapp": {
    "message_templates": {
      "custom_template": "🔥 Sua mensagem customizada: {parametro}"
    }
  }
}
```

---

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. "API token não encontrado"
**Causa**: Variáveis de ambiente não configuradas
**Solução**:
```bash
export CLICKUP_API_TOKEN="seu_token"
export PIPEDRIVE_API_TOKEN="seu_token"
# Ou execute: python scripts/setup.py
```

#### 2. "Email não está sendo processado"
**Causa**: Cron jobs não configurados ou Apple Mail sem acesso
**Solução**:
```bash
# Verificar cron jobs
crontab -l

# Verificar se IDs estão presentes:
# 7c4c353d-55dd-4de9-b315-344f68e147e1 (Ian ClickUp)
# 26e299db-5273-482e-81a6-278667329669 (Ronaldo ClickUp)
# 878b8aa3-4dbc-41d1-8497-0c623e8764c3 (Ian Pipedrive)
```

#### 3. "ClickUp task creation fails"
**Causa**: Permissions ou Team ID incorreto
**Solução**:
```bash
# Verificar conectividade
python scripts/health_check.py

# Verificar Team ID na configuração
# Deve ser: "90132745943"
```

#### 4. "WhatsApp notifications not sent"
**Causa**: Integração WhatsApp não implementada
**Status**: Atualmente apenas logs - integração real pendente

### Logs e Debug

#### Localização dos Logs
```
/Users/andreantunes/.openclaw/workspace/logs/ahc-automator/
├── email_processing.log      # Processamento de emails
├── client_onboarding.log     # Onboarding de clientes
├── project_completion.log    # Conclusão de projetos
├── notifications.log         # Notificações WhatsApp
└── health_check.log         # Health checks
```

#### Ativar Debug Mode
```bash
export AHC_DEBUG=true
python scripts/email_to_clickup_pipedrive.py --debug
```

#### Analisar Logs
```bash
# Ver logs recentes
tail -f /Users/andreantunes/.openclaw/workspace/logs/ahc-automator/email_processing.log

# Buscar erros
grep "ERROR" /Users/andreantunes/.openclaw/workspace/logs/ahc-automator/*.log

# Logs das últimas 24 horas
find /Users/andreantunes/.openclaw/workspace/logs/ahc-automator -name "*.log" -newermt "1 day ago"
```

### Health Check Detalhado

```bash
# Check completo com detalhes
python scripts/health_check.py --verbose

# Saída:
# ✅ configuration: ok
# ✅ api_connectivity: ok  
# ⚠️  cron_jobs: warning
# ✅ logs: ok
# ✅ disk_space: ok
# ✅ workflows: ok
```

---

## 🔧 Manutenção

### Rotina Semanal

1. **Health Check**:
   ```bash
   python scripts/health_check.py --verbose
   ```

2. **Verificar Logs**:
   ```bash
   # Contar erros na semana
   grep "ERROR" /Users/andreantunes/.openclaw/workspace/logs/ahc-automator/*.log | wc -l
   ```

3. **Limpeza de Logs** (se necessário):
   ```bash
   # Arquivar logs antigos (>30 dias)
   find /Users/andreantunes/.openclaw/workspace/logs/ahc-automator -name "*.log" -mtime +30 -exec gzip {} \;
   ```

### Rotina Mensal

1. **Auditoria de Workflows**:
   ```bash
   # Verificar workflows ativos
   python scripts/health_check.py --json | jq '.checks.workflows'
   ```

2. **Verificar Automações**:
   ```bash
   # Confirmar cron jobs ativos
   crontab -l | grep -E "(7c4c353d|26e299db|878b8aa3)"
   ```

3. **Atualizar Configurações** (se necessário):
   - Revisar keywords em `configs/ahc_config.json`
   - Verificar templates de mensagens
   - Validar IDs de listas/projetos ClickUp

### Backup e Recuperação

#### Backup da Configuração
```bash
# Criar backup
cp -r /Users/andreantunes/.openclaw/workspace/skills/ahc-automator ~/backups/ahc-automator-$(date +%Y%m%d)

# Backup apenas configurações
tar -czf ~/backups/ahc-config-$(date +%Y%m%d).tar.gz \
  /Users/andreantunes/.openclaw/workspace/skills/ahc-automator/configs/
```

#### Recuperação
```bash
# Restaurar configuração
tar -xzf ~/backups/ahc-config-20260208.tar.gz -C /

# Re-executar setup se necessário
python scripts/setup.py --non-interactive
```

### Atualizações

#### Atualizar Keywords
```bash
# Editar configuração
nano configs/ahc_config.json

# Verificar mudanças
python scripts/health_check.py
```

#### Adicionar Novos Templates
1. Editar `scripts/client_onboarding.py`
2. Adicionar template em `load_project_templates()`
3. Atualizar configuração JSON
4. Testar: `python scripts/client_onboarding.py --template novo_template --client "Teste"`

---

## 📊 Métricas e ROI

### Time Savings Estimados

| Workflow | Manual | Automatizado | Frequência | Economia/Mês |
|----------|--------|--------------|------------|--------------|
| Email → ClickUp → Pipedrive | 15 min | 30 seg | 80/mês | 19+ horas |
| Client Onboarding | 2 horas | 10 min | 8/mês | 15+ horas |
| Project Completion | 1.5 horas | 15 min | 16/mês | 20+ horas |
| **TOTAL** | - | - | - | **54+ horas/mês** |

### Valor Monetário
- **Economia mensal**: 54+ horas
- **Valor (€50/hora)**: €2,700+/mês
- **ROI anual**: €32,400+

---

## 🆘 Suporte

### Contatos
- **Desenvolvedor**: Andre Antunes
- **Sistema**: OpenClaw AHC-Automator
- **Versão**: 1.0

### Reporting de Bugs
1. Execute health check: `python scripts/health_check.py --json > health_report.json`
2. Colete logs relevantes dos últimos 7 dias
3. Descreva o problema e passos para reproduzir
4. Inclua configuração (sem tokens) e logs

### Feature Requests
Funcionalidades planejadas:
- [ ] Integração real WhatsApp via API
- [ ] AI-powered email classification
- [ ] Dashboard de métricas
- [ ] Mobile notifications
- [ ] Accounting software integration

---

## 📚 Recursos Adicionais

### Documentação APIs
- [ClickUp API Docs](https://clickup.com/api)
- [Pipedrive API Docs](https://developers.pipedrive.com)
- [OpenClaw Documentation](https://docs.openclaw.com)

### Scripts de Exemplo
Veja pasta `workflows/` para exemplos de automações customizadas.

---

**© 2026 Alan Harper Composites - AHC-Automator v1.0**