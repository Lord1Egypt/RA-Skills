# Security & Privacy

## Data Transmission

**What is sent to Ekybot:**
- Agent status (running/stopped/health)
- Performance metrics (response time, model usage)
- Cost tracking data (API usage, spending)
- Conversation metadata (timestamp, model, token count)

**What is never sent:**
- Actual conversation content or prompts
- Local files or documents
- User credentials or API keys
- Personal or sensitive information

## Authentication

**Token-based security:**
- Unique secure token generated per workspace
- Tokens can be revoked instantly via Ekybot dashboard
- All API calls require valid token authentication
- No password storage on local machine

## Local vs Remote

**Local processing:**
- Your AI agents run entirely on your machine
- OpenClaw workspace data stays local
- No remote code execution

**Remote features:**
- Dashboard interface for monitoring
- Mobile app connectivity
- Team collaboration features
- Cost analytics and reporting

## Background Service

**Monitoring daemon:**
- Lightweight Node.js process (< 10MB RAM)
- Streams telemetry every 60 seconds
- Can be paused or disabled anytime
- Automatically restarts if OpenClaw restarts

**Service control:**
```bash
# Stop telemetry
npm run stop

# Check health  
npm run health

# Restart service
npm run start
```

## Configuration Changes

**During installation, the connector modifies:**
- `~/.openclaw/config.json` → Adds Ekybot endpoint
- Creates `~/.ekybot/connector-config.json` → Stores token
- Adds startup script to OpenClaw plugins

**Uninstallation:**
- Removes all configuration entries
- Deletes authentication token
- Stops background service
- Restores original OpenClaw config

## Encryption

**All communications use:**
- HTTPS/TLS 1.3 for API calls
- WebSocket Secure (WSS) for real-time updates
- AES-256 encryption for stored tokens
- Certificate pinning for Ekybot endpoints

## Open Architecture

**Core components:**
- Connection logic: Open source
- Authentication layer: Auditable
- Telemetry format: Documented JSON
- API specifications: Public documentation

**Proprietary components:**
- Ekybot platform backend
- Mobile applications
- Advanced analytics

## Privacy Compliance

**Data handling:**
- No personal data collection
- Agent metadata only
- User controls data retention
- Can delete all data via dashboard

**Geographical:**
- Data processed in EU/US regions
- Compliant with GDPR
- No data sharing with third parties
- User owns all agent activity data

## Trust & Verification

**Verify the connector:**
```bash
# Check what's actually running
ps aux | grep ekybot

# Inspect network connections
netstat -an | grep ekybot

# Review configuration
cat ~/.ekybot/connector-config.json
```

**Source code:** Core connector components are open source and available for security review.

**Community:** Join the OpenClaw Discord for security discussions and updates.