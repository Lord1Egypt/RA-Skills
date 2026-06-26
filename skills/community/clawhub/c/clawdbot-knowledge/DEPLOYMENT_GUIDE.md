# CLAWD Deployment Guide

**Version:** 1.0  
**Last Updated:** 2026-02-05  
**Status:** Production Ready  

---

## 📋 TABLE OF CONTENTS

1. [System Requirements](#system-requirements)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Installation Steps](#installation-steps)
4. [Configuration Setup](#configuration-setup)
5. [Security Hardening](#security-hardening)
6. [Database & Storage Setup](#database--storage-setup)
7. [Service Configuration](#service-configuration)
8. [Monitoring & Logging](#monitoring--logging)
9. [Backup & Disaster Recovery](#backup--disaster-recovery)
10. [Troubleshooting](#troubleshooting)
11. [Deployment Checklist](#deployment-checklist)

---

## 🖥️ SYSTEM REQUIREMENTS

### Minimum Requirements
- **OS:** Linux (Ubuntu 20.04 LTS or newer recommended)
- **CPU:** 4 cores (8+ cores recommended for production)
- **RAM:** 8GB minimum (16GB+ recommended)
- **Storage:** 50GB SSD (100GB+ recommended)
- **Python:** 3.9+ (3.11+ recommended)
- **Node.js:** 18+ (for web components)

### Recommended Production Setup
```
┌─────────────────────────────────────┐
│ Load Balancer (Nginx/HAProxy)       │
├─────────────────────────────────────┤
│ CLAWD Instance 1                    │
│ CLAWD Instance 2                    │
│ CLAWD Instance 3                    │
├─────────────────────────────────────┤
│ PostgreSQL (Cluster)                │
│ Redis (Cache & Queue)               │
├─────────────────────────────────────┤
│ Monitoring (Prometheus + Grafana)   │
│ Logging (ELK Stack)                 │
└─────────────────────────────────────┘
```

### Network Requirements
- Port 80 (HTTP) - Redirect to HTTPS
- Port 443 (HTTPS) - Main application
- Port 5432 (PostgreSQL) - Internal only
- Port 6379 (Redis) - Internal only
- Port 9090 (Prometheus) - Internal only

---

## ✅ PRE-DEPLOYMENT CHECKLIST

Before starting deployment, ensure:

- [ ] Server provisioned and accessible
- [ ] SSH keys configured for secure access
- [ ] Firewall rules configured
- [ ] DNS records pointing to your server
- [ ] SSL/TLS certificate obtained (Let's Encrypt recommended)
- [ ] Backup storage configured
- [ ] Monitoring tools set up
- [ ] Team access and permissions configured

---

## 🚀 INSTALLATION STEPS

### Step 1: System Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required dependencies
sudo apt install -y \
  python3.11 \
  python3.11-venv \
  python3.11-dev \
  nodejs \
  npm \
  git \
  curl \
  wget \
  build-essential \
  libssl-dev \
  libffi-dev \
  postgresql-14 \
  redis-server \
  nginx \
  supervisor

# Create CLAWD system user
sudo useradd -m -s /bin/bash -d /home/clawd clawd
```

### Step 2: Clone Repository

```bash
cd /home/clawd
git clone https://github.com/deepall/clawd.git
cd clawd
git checkout main

# Set permissions
sudo chown -R clawd:clawd /home/clawd/clawd
```

### Step 3: Create Virtual Environment

```bash
cd /home/clawd/clawd
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Python Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Verify installation
python3 -c "import clawd; print('✅ CLAWD installed successfully')"
```

### Step 5: Install Node.js Dependencies (if applicable)

```bash
cd /home/clawd/clawd/web
npm install

# Build frontend (if needed)
npm run build
```

---

## ⚙️ CONFIGURATION SETUP

### Step 1: Environment Variables

Create `/home/clawd/clawd/.env` with the following variables:

```bash
# Application Settings
CLAWD_ENV=production
CLAWD_HOST=0.0.0.0
CLAWD_PORT=8000
CLAWD_DEBUG=false
CLAWD_LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://clawd:password@localhost:5432/clawd_db
DATABASE_POOL_SIZE=20
DATABASE_POOL_TIMEOUT=30

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_secure_password

# API Configuration
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
API_RATE_LIMIT=1000

# Email Configuration (if needed)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_email_password

# GLM Configuration (if using GLM instead of Claude)
GLM_API_KEY=your_glm_api_key
GLM_API_BASE=https://open.bigmodel.cn/api/paas/v4
ANTHROPIC_DEFAULT_OPUS_MODEL=glm-4.7
ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.7
ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-4.5-air

# Security Settings
SECRET_KEY=generate_a_long_random_string_here
SESSION_TIMEOUT=3600
JWT_ALGORITHM=HS256
JWT_EXPIRY=86400

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=daily
BACKUP_RETENTION_DAYS=30
BACKUP_PATH=/home/clawd/backups
```

### Step 2: Secure Environment File

```bash
# Set proper permissions
chmod 600 /home/clawd/clawd/.env
chown clawd:clawd /home/clawd/clawd/.env

# Verify sensitive data is not in version control
echo ".env" >> /home/clawd/clawd/.gitignore
```

### Step 3: Database Configuration

```bash
# Create PostgreSQL user
sudo -u postgres psql << SQL
CREATE ROLE clawd WITH LOGIN PASSWORD 'secure_password_here';
ALTER ROLE clawd CREATEDB;
SQL

# Create database
sudo -u postgres createdb -O clawd clawd_db

# Run migrations
cd /home/clawd/clawd
source venv/bin/activate
python3 manage.py migrate
```

### Step 4: Redis Configuration

```bash
# Edit Redis config
sudo nano /etc/redis/redis.conf

# Required settings:
# requirepass your_secure_password
# maxmemory 4gb
# maxmemory-policy allkeys-lru
# appendonly yes

# Restart Redis
sudo systemctl restart redis-server
```

---

## 🔒 SECURITY HARDENING

### 1. SSL/TLS Certificate

```bash
# Using Let's Encrypt (recommended)
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com

# Certificate renewal (automatic with systemd timer)
sudo certbot renew --dry-run
```

### 2. Firewall Configuration

```bash
sudo ufw enable
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS
sudo ufw deny 5432/tcp    # PostgreSQL (block external)
sudo ufw deny 6379/tcp    # Redis (block external)
```

### 3. Secret Management

```bash
# Use environment variables instead of hardcoding
# Use cloud secret managers (AWS Secrets Manager, HashiCorp Vault, etc.)
# Rotate API keys regularly

# Generate secure secrets
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Application Security Headers

Configure in Nginx:
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

### 5. Input Validation & Sanitization

All user inputs must be validated:
```python
from bleach import clean

def sanitize_input(user_input):
    """Sanitize user input to prevent XSS"""
    allowed_tags = []  # No HTML tags allowed
    return clean(user_input, tags=allowed_tags, strip=True)
```

---

## 💾 DATABASE & STORAGE SETUP

### PostgreSQL Backup Strategy

```bash
# Daily backup script
cat > /usr/local/bin/backup-clawd-db.sh << 'SCRIPT'
#!/bin/bash
BACKUP_DIR="/home/clawd/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U clawd -h localhost clawd_db | \
  gzip > $BACKUP_DIR/clawd_db_${TIMESTAMP}.sql.gz

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "clawd_db_*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional)
# aws s3 cp $BACKUP_DIR/clawd_db_${TIMESTAMP}.sql.gz \
#   s3://your-bucket/backups/

echo "✅ Backup completed: $BACKUP_DIR/clawd_db_${TIMESTAMP}.sql.gz"
SCRIPT

chmod +x /usr/local/bin/backup-clawd-db.sh

# Schedule with cron
echo "0 2 * * * /usr/local/bin/backup-clawd-db.sh" | sudo crontab -
```

### Redis Persistence

```bash
# Ensure RDB snapshots are enabled
sudo nano /etc/redis/redis.conf

# Set:
# save 900 1         # Save after 900 sec if 1 key changed
# save 300 10        # Save after 300 sec if 10 keys changed
# save 60 10000      # Save after 60 sec if 10000 keys changed
# appendonly yes     # Enable AOF

sudo systemctl restart redis-server
```

---

## ⚙️ SERVICE CONFIGURATION

### Supervisor Configuration for CLAWD

Create `/etc/supervisor/conf.d/clawd.conf`:

```ini
[program:clawd]
directory=/home/clawd/clawd
command=/home/clawd/clawd/venv/bin/python3 -m clawd.main
user=clawd
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/clawd/clawd.log
environment=PATH="/home/clawd/clawd/venv/bin",HOME="/home/clawd"
stopsignal=TERM
stopwaitsecs=10
```

Enable and start:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start clawd
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/clawd`:

```nginx
upstream clawd_backend {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    client_max_body_size 20M;
    proxy_read_timeout 60s;

    location / {
        proxy_pass http://clawd_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        access_log off;
        proxy_pass http://clawd_backend/health;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/clawd /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📊 MONITORING & LOGGING

### Prometheus Configuration

Create `/etc/prometheus/clawd.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'clawd'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### ELK Stack Setup (Optional)

```bash
# Install Elasticsearch, Logstash, Kibana
sudo apt install -y elasticsearch logstash kibana

# Configure Logstash to parse CLAWD logs
# Configure Kibana dashboards for monitoring
```

### Application Logging

Configure structured logging in `/home/clawd/clawd/logging_config.json`:

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "standard": {
      "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    },
    "json": {
      "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "standard",
      "level": "INFO"
    },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "filename": "/var/log/clawd/clawd.log",
      "formatter": "json",
      "maxBytes": 10485760,
      "backupCount": 10
    }
  },
  "root": {
    "handlers": ["console", "file"],
    "level": "INFO"
  }
}
```

---

## 🔄 BACKUP & DISASTER RECOVERY

### Backup Strategy

**Daily Backups:**
- Database dumps (PostgreSQL)
- Configuration files
- Uploaded files

**Weekly Backups:**
- Full system snapshots
- Source code repository

**Monthly Backups:**
- Archived to cold storage

### Recovery Procedures

**Database Recovery:**
```bash
# List available backups
ls -lah /home/clawd/backups/

# Restore from backup
gunzip -c /home/clawd/backups/clawd_db_20260205_020000.sql.gz | \
  psql -U clawd -d clawd_db
```

**Full System Recovery:**
```bash
# 1. Restore filesystem from backup
# 2. Reinstall CLAWD from scratch
# 3. Restore database
# 4. Verify all services
# 5. Run health checks
```

---

## 🔧 TROUBLESHOOTING

### Common Issues & Solutions

#### Issue 1: Service Won't Start
```bash
# Check logs
sudo systemctl status clawd
sudo journalctl -u clawd -n 100

# Verify environment variables
source /home/clawd/clawd/.env
env | grep CLAWD

# Check permissions
ls -la /home/clawd/clawd/
sudo chown -R clawd:clawd /home/clawd/clawd
```

#### Issue 2: Database Connection Failed
```bash
# Test PostgreSQL connection
psql -U clawd -d clawd_db -h localhost

# Check if PostgreSQL is running
sudo systemctl status postgresql

# Verify connection string
echo $DATABASE_URL
```

#### Issue 3: High Memory Usage
```bash
# Check memory consumption
top -p $(pgrep -f "python3 -m clawd")

# Adjust Redis maxmemory
redis-cli CONFIG GET maxmemory
redis-cli CONFIG SET maxmemory 4gb

# Check for memory leaks
python3 -m memory_profiler
```

#### Issue 4: SSL Certificate Issues
```bash
# Check certificate expiry
openssl x509 -enddate -noout -in /etc/letsencrypt/live/yourdomain.com/cert.pem

# Renew certificate
sudo certbot renew

# Test renewal process
sudo certbot renew --dry-run
```

---

## ✅ DEPLOYMENT CHECKLIST

Before going live, verify:

### Pre-Deployment
- [ ] All dependencies installed and tested
- [ ] Environment variables configured
- [ ] Database initialized and migrations run
- [ ] SSL/TLS certificates installed
- [ ] Firewall rules configured
- [ ] Backup system operational
- [ ] Monitoring system configured
- [ ] Team training completed

### Deployment
- [ ] Run health checks: `python3 manage.py check`
- [ ] Run tests: `pytest tests/`
- [ ] Load test with production load
- [ ] Verify all API endpoints
- [ ] Test authentication & authorization
- [ ] Verify SSL/TLS configuration
- [ ] Test database backups
- [ ] Test failover & recovery

### Post-Deployment
- [ ] Monitor system metrics for 24 hours
- [ ] Review logs for errors
- [ ] Verify backup integrity
- [ ] Confirm monitoring alerts working
- [ ] Document any issues encountered
- [ ] Brief team on system status
- [ ] Plan post-launch improvements

### Performance Targets
- API Response Time: < 200ms (p95)
- Availability: 99.9%
- Error Rate: < 0.1%
- CPU Usage: < 70%
- Memory Usage: < 80%
- Disk Usage: < 80%

---

## 📞 SUPPORT & CONTACTS

- **Technical Issues:** support@clawd.io
- **Security Issues:** security@clawd.io
- **Documentation:** docs.clawd.io
- **Status Page:** status.clawd.io

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-05  
**Next Review:** 2026-03-05  

