# n8n Workflow Templates

Production-ready workflow templates for common automation scenarios.

## Quick Reference

| Template | Use Case | Triggers |
|----------|----------|----------|
| Email Digest | Daily summaries | Schedule |
| Database Sync | Data synchronization | Schedule |
| Webhook Alert | Real-time notifications | Webhook |
| GitHub → Notion | Issue tracking | Webhook |
| DeepALL Processing | Document intelligence | Webhook/Schedule |
| FATONI Analysis | AI agent automation | Schedule |

## Voice Commands for Templates

```
"Create an email automation workflow"
"Build a database to Slack sync"
"Make a webhook that sends alerts"
"Set up document processing with DeepALL"
"Create FATONI analysis automation"
```

## 1. Email Automation Template

### Daily Email Digest
```json
{
  "name": "Daily Email Digest",
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{
            "field": "hours",
            "hoursInterval": 24
          }]
        },
        "triggerAt": "09:00"
      },
      "name": "Every Day at 9 AM",
      "position": [250, 300]
    },
    {
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "fromEmail": "automation@company.com",
        "toEmail": "user@company.com",
        "subject": "Daily Digest - {{ $today.format('YYYY-MM-DD') }}",
        "text": "Your daily summary goes here"
      },
      "name": "Send Email",
      "position": [450, 300]
    }
  ],
  "connections": {
    "Every Day at 9 AM": {
      "main": [[{"node": "Send Email", "type": "main", "index": 0}]]
    }
  },
  "active": false
}
```

**Voice Command:**
```
"Create a workflow that sends me an email every morning at 9 AM"
```

## 2. Database Synchronization Template

### PostgreSQL to Slack
```json
{
  "name": "Database to Slack Sync",
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 1}]
        }
      },
      "name": "Every Hour",
      "position": [250, 300]
    },
    {
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM sales WHERE created_at > NOW() - INTERVAL '1 hour'"
      },
      "credentials": {
        "postgres": "postgres-production"
      },
      "name": "Get New Sales",
      "position": [450, 300]
    },
    {
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "// Transform data\nconst count = items.length;\nreturn [{json: {count, items}}];"
      },
      "name": "Transform Data",
      "position": [650, 300]
    },
    {
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "operation": "sendMessage",
        "channel": "#sales",
        "text": "📊 New sales in the last hour: {{ $json.count }}"
      },
      "credentials": {
        "slackApi": "slack-workspace"
      },
      "name": "Notify Slack",
      "position": [850, 300]
    }
  ],
  "connections": {
    "Every Hour": {"main": [[{"node": "Get New Sales"}]]},
    "Get New Sales": {"main": [[{"node": "Transform Data"}]]},
    "Transform Data": {"main": [[{"node": "Notify Slack"}]]}
  }
}
```

**Voice Command:**
```
"Create a workflow that syncs my database to Slack every hour"
```

## 3. Webhook Alert Template

### Real-time Alert System
```json
{
  "name": "Webhook to Email Alert",
  "nodes": [
    {
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "alert",
        "httpMethod": "POST",
        "responseMode": "onReceived"
      },
      "name": "Webhook Trigger",
      "position": [250, 300]
    },
    {
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "fromEmail": "alerts@company.com",
        "toEmail": "admin@company.com",
        "subject": "⚠️ Alert: {{ $json.body.message }}",
        "text": "{{ $json.body.details }}"
      },
      "name": "Send Alert Email",
      "position": [450, 300]
    }
  ],
  "connections": {
    "Webhook Trigger": {"main": [[{"node": "Send Alert Email"}]]}
  }
}
```

**Voice Command:**
```
"Create a webhook that sends me alerts via email"
```

## 4. GitHub to Notion Template

### Issue Tracking
```json
{
  "name": "GitHub Issues to Notion",
  "nodes": [
    {
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "github-webhook",
        "httpMethod": "POST"
      },
      "name": "GitHub Webhook",
      "position": [250, 300]
    },
    {
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "string": [{
            "value1": "={{ $json.action }}",
            "operation": "equals",
            "value2": "opened"
          }]
        }
      },
      "name": "Check if New Issue",
      "position": [450, 300]
    },
    {
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "operation": "create",
        "databaseId": "your-database-id",
        "title": "={{ $json.issue.title }}",
        "properties": {
          "Status": "To Do",
          "Priority": "Medium",
          "URL": "={{ $json.issue.html_url }}"
        }
      },
      "credentials": {
        "notionApi": "notion-workspace"
      },
      "name": "Create Notion Task",
      "position": [650, 250]
    }
  ],
  "connections": {
    "GitHub Webhook": {"main": [[{"node": "Check if New Issue"}]]},
    "Check if New Issue": {"main": [[{"node": "Create Notion Task"}]]}
  }
}
```

**Voice Command:**
```
"Create a workflow that creates Notion tasks from GitHub issues"
```

## 5. DeepALL Document Processing Template

### Intelligent Document Pipeline
```json
{
  "name": "DeepALL Document Processing",
  "nodes": [
    {
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "document-upload",
        "httpMethod": "POST"
      },
      "name": "Document Upload",
      "position": [250, 300]
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/documents/upload",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [{
            "name": "file",
            "value": "={{ $binary.data }}"
          }]
        }
      },
      "name": "Upload to DeepALL",
      "position": [450, 300]
    },
    {
      "type": "n8n-nodes-base.wait",
      "parameters": {
        "amount": 30,
        "unit": "seconds"
      },
      "name": "Wait for Processing",
      "position": [650, 300]
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8000/api/v1/intelligence/query",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [{
            "name": "query",
            "value": "Summarize this document"
          }, {
            "name": "document_ids",
            "value": "={{ [$json.document_id] }}"
          }]
        }
      },
      "name": "Query DeepALL",
      "position": [850, 300]
    },
    {
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "subject": "Document Analysis Complete",
        "text": "Summary: {{ $json.answer }}"
      },
      "name": "Send Results",
      "position": [1050, 300]
    }
  ],
  "connections": {
    "Document Upload": {"main": [[{"node": "Upload to DeepALL"}]]},
    "Upload to DeepALL": {"main": [[{"node": "Wait for Processing"}]]},
    "Wait for Processing": {"main": [[{"node": "Query DeepALL"}]]},
    "Query DeepALL": {"main": [[{"node": "Send Results"}]]}
  }
}
```

**Voice Command:**
```
"Create a workflow that processes documents with DeepALL and emails results"
```

## 6. FATONI AI Agent Template

### Multi-Agent Data Analysis
```json
{
  "name": "FATONI Data Analysis",
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 24}]
        },
        "triggerAt": "08:00"
      },
      "name": "Daily Trigger",
      "position": [250, 300]
    },
    {
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM analytics WHERE date = CURRENT_DATE"
      },
      "name": "Get Daily Data",
      "position": [450, 300]
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:7777/api/agents/analyze",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [{
            "name": "agent",
            "value": "DataAnalyst"
          }, {
            "name": "task",
            "value": "analyze_sales_data"
          }, {
            "name": "data",
            "value": "={{ $json }}"
          }]
        }
      },
      "name": "FATONI Analysis",
      "position": [650, 300]
    },
    {
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const insights = items[0].json.insights;\nreturn [{json: {summary: insights.summary, recommendations: insights.recommendations}}];"
      },
      "name": "Extract Insights",
      "position": [850, 300]
    },
    {
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#insights",
        "text": "📊 Daily Analysis Summary:\n{{ $json.summary }}\n\n💡 Recommendations:\n{{ $json.recommendations }}"
      },
      "name": "Post to Slack",
      "position": [1050, 300]
    }
  ],
  "connections": {
    "Daily Trigger": {"main": [[{"node": "Get Daily Data"}]]},
    "Get Daily Data": {"main": [[{"node": "FATONI Analysis"}]]},
    "FATONI Analysis": {"main": [[{"node": "Extract Insights"}]]},
    "Extract Insights": {"main": [[{"node": "Post to Slack"}]]}
  }
}
```

**Voice Command:**
```
"Create a workflow that uses FATONI to analyze daily data"
```

## 7. Error Handling Template

### Robust Workflow with Retry Logic
```json
{
  "name": "API Call with Error Handling",
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "name": "Trigger",
      "position": [250, 300]
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.example.com/data",
        "options": {
          "retry": {
            "maxRetries": 3,
            "retryDelay": 1000
          }
        }
      },
      "name": "API Call",
      "position": [450, 300]
    },
    {
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [{
            "value1": "={{ $json.status }}",
            "operation": "equals",
            "value2": 200
          }]
        }
      },
      "name": "Check Success",
      "position": [650, 300]
    },
    {
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "subject": "✅ API Call Successful"
      },
      "name": "Success Email",
      "position": [850, 250]
    },
    {
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "subject": "❌ API Call Failed",
        "text": "Error: {{ $json.error }}"
      },
      "name": "Error Email",
      "position": [850, 350]
    }
  ],
  "connections": {
    "Trigger": {"main": [[{"node": "API Call"}]]},
    "API Call": {"main": [[{"node": "Check Success"}]]},
    "Check Success": {
      "main": [
        [{"node": "Success Email"}],
        [{"node": "Error Email"}]
      ]
    }
  }
}
```

**Voice Command:**
```
"Create a workflow with error handling and retry logic"
```

## Template Usage

### How to Use Templates

1. **Voice Command:**
   ```
   "Create a [template name] workflow"
   ```

2. **Customize:**
   - Workflow names
   - Schedule times
   - Email addresses
   - API endpoints
   - Data sources

3. **Deploy:**
   ```
   "Activate the [workflow name]"
   ```

4. **Test:**
   ```
   "Execute the [workflow name]"
   ```

### Template Customization

**Example Voice Commands:**
```
"Create an email workflow that runs every 2 hours"
"Make a database sync that posts to channel #analytics"
"Set up DeepALL processing for PDF files only"
"Create FATONI analysis with SecurityAuditor agent"
```

## Best Practices

### Workflow Design
- Start with simple templates
- Add error handling nodes
- Include logging/notifications
- Test before activating

### Node Configuration
- Use descriptive node names
- Add comments for complex logic
- Validate input data
- Handle empty results

### Performance
- Avoid infinite loops
- Set reasonable timeouts
- Use batch operations
- Cache when possible

## Resources

- **More Templates**: See n8n community workflows
- **Node Documentation**: https://docs.n8n.io/integrations/
- **Workflow Examples**: https://n8n.io/workflows
- **Community Forum**: https://community.n8n.io

---

**Ready to create your workflow?**
Use voice commands with these templates to automate your tasks!
