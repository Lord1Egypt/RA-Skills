# n8n MCP Server

> **Complete Model Context Protocol Server for n8n Workflow Creation & Management**

A comprehensive MCP server that creates, validates, and manages n8n workflows with **100% compliance** to official n8n guidelines.

## 🚀 Quick Start

### 1. Automated Setup
```bash
# Run the setup script (recommended)
./setup.sh
```

### 2. Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python3 test_n8n_mcp_server.py

# Start server
python3 n8n_mcp_server_complete.py
```

## ✨ Features

- 🔧 **Complete Workflow Creation** - Generate full n8n workflows from natural language
- ⚡ **Individual Node Creation** - Create custom nodes with full guideline compliance
- ✅ **Comprehensive Validation** - Validate against all n8n standards
- 🚀 **Performance Optimization** - Built-in performance and security analysis
- 📚 **Guidelines Integration** - Complete n8n development guidelines embedded
- 🎨 **Multi-Style Support** - Both declarative and programmatic building styles
- 🔐 **Security Analysis** - Built-in security best practices
- 📤 **Export Functionality** - JSON and YAML export formats

## 🔧 MCP Tools

| Tool | Description |
|------|-------------|
| `create_workflow` | Create complete n8n workflows from descriptions |
| `create_node` | Generate individual n8n nodes |
| `validate_workflow` | Comprehensive workflow validation |
| `validate_node` | Node compliance checking |
| `get_guidelines` | Access n8n development guidelines |
| `optimize_workflow` | Performance and security optimization |
| `suggest_improvements` | AI-powered improvement suggestions |
| `export_workflow` | Export in multiple formats |
| `generate_credentials` | Create credential configurations |

## 📚 Resources

| Resource | Description |
|----------|-------------|
| `n8n://guidelines/complete` | Complete n8n development guidelines |
| `n8n://templates/nodes` | Comprehensive node templates |
| `n8n://patterns/workflows` | Common workflow patterns |
| `n8n://credentials/templates` | Credential configurations |

## 🎯 Usage Examples

### Create a Workflow
```json
{
  "tool": "create_workflow",
  "arguments": {
    "name": "Daily Sales Report",
    "description": "Fetch sales data, process it, and email the team",
    "pattern": "scheduled_report"
  }
}
```

### Create a Custom Node
```json
{
  "tool": "create_node",
  "arguments": {
    "name": "WeatherAPI",
    "service": "weather",
    "operations": ["getCurrentWeather", "getForecast"],
    "building_style": "declarative"
  }
}
```

### Validate a Workflow
```json
{
  "tool": "validate_workflow",
  "arguments": {
    "workflow": { /* your workflow JSON */ },
    "strict_mode": true
  }
}
```

## 📋 Requirements

- **Python**: 3.11+ 
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space

## 📖 Documentation

- **Complete Guide**: `n8n_mcp_server_documentation.md`
- **n8n Guidelines**: `n8n_node_development_guide.pdf`
- **Test Suite**: `test_n8n_mcp_server.py`

## 🧪 Testing

```bash
# Run comprehensive test suite
python3 test_n8n_mcp_server.py

# Expected: 100% test success rate
```

## 🔗 MCP Client Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "n8n-mcp-server": {
      "command": "python3",
      "args": ["/path/to/n8n_mcp_server_complete.py"],
      "env": {}
    }
  }
}
```

## 📊 Validation & Compliance

### Compliance Levels
- **90-100**: ✅ Excellent - Full n8n compliance
- **80-89**: 🟡 Good - Minor improvements needed  
- **70-79**: 🟠 Fair - Several issues to address
- **Below 70**: 🔴 Poor - Major compliance issues

### Built-in Guidelines
- ✅ Official n8n naming conventions
- ✅ Node type recommendations (Trigger vs Action)
- ✅ Building style selection (Declarative vs Programmatic)
- ✅ Security best practices
- ✅ Performance optimization
- ✅ Community standards compliance

## 🎨 Workflow Patterns

| Pattern | Use Case |
|---------|----------|
| `api_to_database` | Data synchronization, imports |
| `scheduled_report` | Daily/weekly reports, monitoring |
| `webhook_processor` | Real-time integrations, events |
| `data_pipeline` | ETL processes, data warehousing |
| `notification_system` | Alert systems, status updates |
| `file_processing` | Document processing, conversion |

## 🔐 Security Features

- 🛡️ **Credential Validation** - Ensures proper credential usage
- 🔒 **HTTPS Enforcement** - Warns about insecure connections
- 🔍 **Secret Detection** - Identifies hardcoded passwords
- ✅ **Input Sanitization** - Validates all parameters
- 🔐 **Access Control** - Proper permission handling

## 🛠️ Files Included

| File | Description |
|------|-------------|
| `n8n_mcp_server_complete.py` | Main MCP server implementation |
| `test_n8n_mcp_server.py` | Comprehensive test suite |
| `n8n_mcp_server_documentation.md` | Complete documentation |
| `n8n_node_development_guide.pdf` | Official n8n guidelines |
| `setup.sh` | Automated setup script |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

## 🎉 Benefits

- 🔒 **100% n8n Compliance** - Guaranteed adherence to official standards
- 🚀 **Rapid Development** - Create workflows in minutes, not hours
- 🛡️ **Built-in Security** - Security best practices automatically applied
- 📖 **Comprehensive Documentation** - Complete guides and examples
- 🔄 **Future-Proof** - Based on latest n8n guidelines
- 🧪 **Thoroughly Tested** - Extensive test suite included

## 🚀 Get Started

1. **Run Setup**: `./setup.sh`
2. **Start Server**: `python3 n8n_mcp_server_complete.py`
3. **Connect Client**: Configure your MCP client
4. **Create Workflows**: Start building n8n workflows with confidence!

---

**Ready to create professional n8n workflows with guaranteed compliance?** 🎯

The n8n MCP Server makes it easy to build high-quality n8n integrations that meet all official standards and best practices.

