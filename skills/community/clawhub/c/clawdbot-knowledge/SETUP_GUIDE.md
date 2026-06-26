# Enhanced N8N MCP Server - Complete Setup Guide

## 🚀 **Quick Start**

### **1. Environment Setup**

1. **Copy the environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Configure basic settings:**
   ```bash
   # Edit .env file
   ENVIRONMENT=development
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ENCRYPTION_KEY=your-32-character-encryption-key-here
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   pip install cryptography  # For credential encryption
   ```

### **2. Start the Server**

```bash
python backend/web_server.py
```

The server will be available at: http://localhost:8080

### **3. Access Credential Management**

Navigate to: http://localhost:8080/credentials

## 📋 **Service Configuration Guide**

### **AI/LLM Services**

#### **OpenAI API**
1. **Get API Key:**
   - Visit: https://platform.openai.com/api-keys
   - Create new API key
   - Copy the key (starts with `sk-`)

2. **Configure in UI:**
   - Service: OpenAI API
   - API Key: `sk-your-key-here`
   - Model: `gpt-4` (optional)
   - Base URL: `https://api.openai.com/v1` (default)

#### **AnythingLLM**
1. **Setup AnythingLLM:**
   ```bash
   docker run -d -p 3001:3001 --name anythingllm mintplexlabs/anythingllm
   ```

2. **Configure:**
   - Base URL: `http://localhost:3001`
   - API Key: Get from AnythingLLM settings
   - Workspace: `default`

#### **Flowise**
1. **Setup Flowise:**
   ```bash
   npx flowise start
   ```

2. **Configure:**
   - Base URL: `http://localhost:3000`
   - API Key: Get from Flowise settings
   - Chatflow ID: Your specific chatflow

### **Database Services**

#### **Supabase**
1. **Create Project:**
   - Visit: https://supabase.com
   - Create new project
   - Get URL and keys from settings

2. **Configure:**
   - URL: `https://your-project.supabase.co`
   - Anon Key: Public anon key
   - Service Role Key: Service role key (optional)

#### **NocoDB**
1. **Setup NocoDB:**
   ```bash
   docker run -d --name nocodb -p 8080:8080 nocodb/nocodb:latest
   ```

2. **Configure:**
   - Base URL: `http://localhost:8080`
   - API Token: Get from NocoDB account settings

#### **Qdrant Vector Database**
1. **Setup Qdrant:**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. **Configure:**
   - Host: `localhost`
   - Port: `6333`
   - API Key: (optional for local setup)
   - Collection Name: `n8n_workflows`

### **Workflow Automation**

#### **N8N Instance**
1. **Setup N8N:**
   ```bash
   docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
   ```

2. **Configure:**
   - Base URL: `http://localhost:5678`
   - API Key: Get from N8N settings
   - Username/Password: Your N8N credentials

#### **ActivePieces**
1. **Setup ActivePieces:**
   ```bash
   docker run -d --name activepieces -p 8080:80 activepieces/activepieces
   ```

2. **Configure:**
   - Base URL: `http://localhost:8080`
   - API Key: Get from ActivePieces settings

### **Authentication Services**

#### **Google OAuth**
1. **Create OAuth App:**
   - Visit: https://console.developers.google.com
   - Create new project or select existing
   - Enable Google+ API
   - Create OAuth 2.0 credentials

2. **Configure:**
   - Client ID: Your Google client ID
   - Client Secret: Your Google client secret
   - Redirect URI: `http://localhost:8080/auth/google/callback`
   - Scopes: `openid,email,profile`

#### **GitHub OAuth**
1. **Create OAuth App:**
   - Visit: https://github.com/settings/applications/new
   - Application name: Enhanced N8N MCP Server
   - Homepage URL: `http://localhost:8080`
   - Authorization callback URL: `http://localhost:8080/auth/github/callback`

2. **Configure:**
   - Client ID: Your GitHub client ID
   - Client Secret: Your GitHub client secret

## 🎯 **Credential Packages**

### **AI Package**
Includes: OpenAI, AnythingLLM, Flowise, LiteLLM
```bash
# Enable in .env
PACKAGE_AI_ENABLED=true
```

### **Database Package**
Includes: Supabase, NocoDB, Qdrant, PostgreSQL
```bash
# Enable in .env
PACKAGE_DATABASE_ENABLED=true
```

### **Automation Package**
Includes: N8N, ActivePieces
```bash
# Enable in .env
PACKAGE_AUTOMATION_ENABLED=true
```

### **Full Stack Package**
Includes: All available services
```bash
# Enable in .env
PACKAGE_FULL_STACK_ENABLED=true
```

## 🔧 **Advanced Configuration**

### **Environment Variables**

#### **Core Settings**
```bash
# Environment
ENVIRONMENT=development|staging|production
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
DEBUG_MODE=true

# Security
SECRET_KEY=your-secret-key-32-chars-minimum
ENCRYPTION_KEY=your-encryption-key-32-chars-exactly
SESSION_TIMEOUT=3600
```

#### **Feature Flags**
```bash
# Core Features
FEATURE_NATURAL_LANGUAGE_WORKFLOWS=true
FEATURE_AUTO_NODE_GENERATION=true
FEATURE_WORKFLOW_OPTIMIZATION=true
FEATURE_REAL_TIME_VALIDATION=true

# Experimental Features
FEATURE_AI_WORKFLOW_SUGGESTIONS=false
FEATURE_COLLABORATIVE_EDITING=false
```

#### **Workflow Engine**
```bash
# Processing
WORKFLOW_PROCESSING_INTERVAL=5000
WORKFLOW_BATCH_SIZE=10
WORKFLOW_RETRY_ATTEMPTS=3
WORKFLOW_TIMEOUT=300

# Natural Language
NL_PROCESSING_ENABLED=true
NL_MODEL_PROVIDER=openai
NL_CONTEXT_WINDOW=4096
NL_TEMPERATURE=0.7
```

### **Security Best Practices**

1. **Generate Secure Keys:**
   ```bash
   # Use the built-in key generator
   curl -X POST http://localhost:8080/api/credentials/setup/generate-key \
        -H "Content-Type: application/json" \
        -d '{"length": 32}'
   ```

2. **Environment-Specific Configuration:**
   ```bash
   # Development
   DEBUG_MODE=true
   LOG_LEVEL=DEBUG
   
   # Production
   DEBUG_MODE=false
   LOG_LEVEL=INFO
   ENVIRONMENT=production
   ```

3. **Credential Encryption:**
   - All sensitive credentials are automatically encrypted
   - Encryption key should be 32 characters exactly
   - Never commit .env files to version control

## 🧪 **Testing Your Setup**

### **1. Health Check**
```bash
curl http://localhost:8080/api/health
```

### **2. Credential Validation**
```bash
curl -X POST http://localhost:8080/api/credentials/validate-all
```

### **3. Service Testing**
```bash
curl -X POST http://localhost:8080/api/credentials/service/openai/validate
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Install missing dependencies
pip install cryptography flask-cors pydantic
```

#### **Credential Validation Fails**
1. Check API keys are correct
2. Verify service URLs are accessible
3. Check firewall/network settings
4. Review service-specific documentation

#### **Database Connection Issues**
1. Verify database is running
2. Check connection strings
3. Ensure proper permissions
4. Test connectivity manually

### **Debug Mode**
```bash
# Enable verbose logging
DEBUG_MODE=true
LOG_LEVEL=DEBUG
DEV_VERBOSE_LOGGING=true
```

### **Service Status**
Check the credential management dashboard at:
http://localhost:8080/credentials

## 📚 **Additional Resources**

- **API Documentation:** `/api/credentials/services`
- **Health Monitoring:** `/api/health`
- **Configuration Export:** `/api/credentials/export`
- **Setup Wizard:** Available in the web interface

## 🎉 **Next Steps**

1. **Complete the Setup Wizard** in the web interface
2. **Configure your preferred services** using the credential manager
3. **Test all connections** using the validation tools
4. **Create your first workflow** using natural language
5. **Explore advanced features** like auto-optimization

Your Enhanced N8N MCP Server is now ready for production use! 🚀
