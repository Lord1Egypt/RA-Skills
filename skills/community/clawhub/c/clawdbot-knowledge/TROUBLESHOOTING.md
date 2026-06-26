# Enhanced N8N MCP Server - Troubleshooting Guide

## 🔧 **Common Issues & Solutions**

### **1. Server Startup Issues**

#### **Problem: Server won't start**
```bash
Error: ModuleNotFoundError: No module named 'credential_manager'
```

**Solution:**
```bash
# Install missing dependencies
pip install -r backend/requirements.txt
pip install cryptography flask-cors

# Ensure you're in the correct directory
cd backend
python web_server.py
```

#### **Problem: Port already in use**
```bash
Error: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find process using port 8080
lsof -i :8080
# Or on Windows
netstat -ano | findstr :8080

# Kill the process or change port
export SERVER_PORT=8081
python web_server.py
```

### **2. Credential Management Issues**

#### **Problem: Credential encryption fails**
```bash
Error: Invalid encryption key length
```

**Solution:**
```bash
# Generate proper 32-character key
python -c "import secrets; print(secrets.token_urlsafe(32)[:32])"

# Set in .env file
ENCRYPTION_KEY=your-32-character-key-here-exactly
```

#### **Problem: Service validation fails**
```bash
Error: Service validation failed: Connection timeout
```

**Solutions:**
1. **Check service availability:**
   ```bash
   # Test OpenAI
   curl -H "Authorization: Bearer sk-your-key" https://api.openai.com/v1/models
   
   # Test local services
   curl http://localhost:3001/health  # AnythingLLM
   curl http://localhost:5678/healthz # N8N
   ```

2. **Verify credentials:**
   - API keys are correct and active
   - URLs are accessible
   - No typos in configuration

3. **Network connectivity:**
   - Check firewall settings
   - Verify proxy configuration
   - Test DNS resolution

### **3. Database Connection Issues**

#### **Problem: Supabase connection fails**
```bash
Error: Invalid API key or insufficient permissions
```

**Solution:**
```bash
# Verify Supabase configuration
curl -H "apikey: your-anon-key" \
     -H "Authorization: Bearer your-anon-key" \
     https://your-project.supabase.co/rest/v1/

# Check project URL format
# Correct: https://abcdefgh.supabase.co
# Incorrect: https://supabase.co/dashboard/project/abcdefgh
```

#### **Problem: PostgreSQL connection timeout**
```bash
Error: could not connect to server: Connection timed out
```

**Solution:**
```bash
# Test connection manually
psql -h localhost -p 5432 -U postgres -d your_database

# Check PostgreSQL is running
sudo systemctl status postgresql
# Or on Windows
sc query postgresql

# Verify connection parameters
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_DATABASE=n8n_mcp_server
```

### **4. API Integration Issues**

#### **Problem: OpenAI API rate limits**
```bash
Error: Rate limit exceeded
```

**Solution:**
```bash
# Configure rate limiting in .env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# Use different model or tier
NL_MODEL_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo  # Instead of gpt-4
```

#### **Problem: N8N API authentication fails**
```bash
Error: Unauthorized - Invalid API key
```

**Solution:**
1. **Generate N8N API key:**
   - Open N8N interface
   - Go to Settings → API Keys
   - Create new API key
   - Copy the key exactly

2. **Verify N8N configuration:**
   ```bash
   # Test N8N API
   curl -H "X-N8N-API-KEY: your-api-key" \
        http://localhost:5678/api/v1/workflows
   ```

### **5. Frontend/UI Issues**

#### **Problem: Credential page not loading**
```bash
Error: 404 Not Found - /credentials
```

**Solution:**
```bash
# Check if credential management is available
grep -r "CREDENTIAL_MANAGEMENT_AVAILABLE" backend/

# Ensure credential_routes.py exists
ls backend/credential_routes.py

# Restart server
python backend/web_server.py
```

#### **Problem: JavaScript errors in browser**
```bash
Error: credentialManager is not defined
```

**Solution:**
1. **Check file paths:**
   ```bash
   # Verify static files exist
   ls static/js/credentials.js
   ls templates/credentials.html
   ```

2. **Clear browser cache:**
   - Hard refresh (Ctrl+F5)
   - Clear browser cache
   - Check browser console for errors

### **6. Environment Configuration Issues**

#### **Problem: Environment variables not loading**
```bash
Error: KeyError: 'OPENAI_API_KEY'
```

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify .env format (no spaces around =)
# Correct: API_KEY=value
# Incorrect: API_KEY = value

# Load environment manually
export $(cat .env | xargs)
python backend/web_server.py
```

#### **Problem: Feature flags not working**
```bash
Error: Natural language processing not available
```

**Solution:**
```bash
# Enable features in .env
FEATURE_NATURAL_LANGUAGE_WORKFLOWS=true
NL_PROCESSING_ENABLED=true
NL_MODEL_PROVIDER=openai

# Restart server after changes
```

### **7. Docker/Container Issues**

#### **Problem: Docker services not accessible**
```bash
Error: Connection refused to localhost:5678
```

**Solution:**
```bash
# Check Docker containers
docker ps

# Verify port mapping
docker run -p 5678:5678 n8nio/n8n

# Use container IP instead of localhost
docker inspect container_name | grep IPAddress
```

### **8. Performance Issues**

#### **Problem: Slow response times**
```bash
Warning: Request timeout after 30 seconds
```

**Solution:**
```bash
# Optimize configuration
WORKFLOW_PROCESSING_INTERVAL=1000  # Reduce interval
WORKFLOW_BATCH_SIZE=5              # Smaller batches
CACHE_ENABLED=true                 # Enable caching

# Monitor resource usage
top -p $(pgrep -f web_server.py)
```

## 🔍 **Diagnostic Tools**

### **1. Health Check Endpoint**
```bash
curl http://localhost:8080/api/health
```

### **2. Credential Status**
```bash
curl http://localhost:8080/api/credentials/services
```

### **3. Configuration Validation**
```bash
curl http://localhost:8080/api/credentials/configuration/validate
```

### **4. Service Testing**
```bash
# Test specific service
curl -X POST http://localhost:8080/api/credentials/service/openai/validate

# Test all services
curl -X POST http://localhost:8080/api/credentials/validate-all
```

## 📊 **Logging & Monitoring**

### **Enable Debug Logging**
```bash
# In .env file
DEBUG_MODE=true
LOG_LEVEL=DEBUG
DEV_VERBOSE_LOGGING=true

# Check logs
tail -f logs/n8n_mcp_server.log
```

### **Monitor System Resources**
```bash
# CPU and Memory usage
htop

# Disk usage
df -h

# Network connections
netstat -tulpn | grep :8080
```

## 🛠️ **Recovery Procedures**

### **1. Reset Configuration**
```bash
# Backup current config
cp .env .env.backup
cp config/credentials.json config/credentials.json.backup

# Reset to defaults
cp .env.template .env
rm config/credentials.json

# Restart server
python backend/web_server.py
```

### **2. Regenerate Encryption Keys**
```bash
# Generate new keys
curl -X POST http://localhost:8080/api/credentials/setup/generate-key

# Update .env file with new keys
# Note: This will invalidate existing encrypted credentials
```

### **3. Export/Import Configuration**
```bash
# Export current configuration
curl http://localhost:8080/api/credentials/export > config_backup.json

# Import configuration (manual process)
# Edit config_backup.json and update credentials manually
```

## 📞 **Getting Help**

### **1. Check Documentation**
- Setup Guide: `docs/SETUP_GUIDE.md`
- API Documentation: Available at `/api/credentials/services`
- Feature Documentation: `ENHANCED_N8N_MCP_SERVER_DOCUMENTATION.md`

### **2. Enable Verbose Logging**
```bash
# Maximum verbosity
DEBUG_MODE=true
LOG_LEVEL=DEBUG
DEV_VERBOSE_LOGGING=true
DEV_AUTO_RELOAD=true
```

### **3. Test Individual Components**
```bash
# Test credential manager
python -c "from backend.credential_manager import credential_manager; print(credential_manager.get_enabled_services())"

# Test validation
python backend/n8n_compliance_validator.py
```

### **4. Common Error Patterns**

| Error Pattern | Likely Cause | Solution |
|---------------|--------------|----------|
| `ModuleNotFoundError` | Missing dependencies | `pip install -r requirements.txt` |
| `Connection refused` | Service not running | Start the service |
| `Invalid API key` | Wrong credentials | Verify API key |
| `Permission denied` | File permissions | `chmod 644 .env` |
| `Port in use` | Another process | Change port or kill process |
| `Timeout` | Network/firewall | Check connectivity |

## ✅ **Verification Checklist**

After troubleshooting, verify everything works:

- [ ] Server starts without errors
- [ ] Health check returns 200 OK
- [ ] Credential page loads
- [ ] At least one service validates successfully
- [ ] Configuration can be exported
- [ ] No JavaScript errors in browser console
- [ ] All required environment variables are set
- [ ] Encryption/decryption works correctly

If all items are checked, your Enhanced N8N MCP Server should be working correctly! 🎉
