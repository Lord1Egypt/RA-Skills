# Quick Start Guide

Get up and running with Enterprise Agent OS in 15 minutes.

## Prerequisites

- Node.js >= 18.0.0
- PostgreSQL >= 14
- Redis >= 6
- Docker (optional, for easy setup)

## Option 1: Docker Compose (Fastest)

```bash
# Clone repository
git clone https://github.com/YourOrg/openclaw-enterprise-hub.git
cd openclaw-enterprise-hub

# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps

# Check health
curl http://localhost:3000/health

# View logs
docker-compose logs -f
```

That's it! Services are now running at:
- API: http://localhost:3000
- Admin UI: http://localhost:3000/admin
- GraphQL Playground: http://localhost:3000/graphql

## Option 2: Manual Setup

### Step 1: Install Dependencies

```bash
# Clone repository
git clone https://github.com/YourOrg/openclaw-enterprise-hub.git
cd openclaw-enterprise-hub

# Install Node.js dependencies
npm install

# Or use pnpm (faster)
pnpm install
```

### Step 2: Setup Databases

**PostgreSQL:**
```bash
# Create database
createdb enterprise_agent_os

# Run migrations
npm run db:migrate

# Verify
psql enterprise_agent_os -c "\dt"
```

**Redis:**
```bash
# Start Redis (if not running)
redis-server

# Verify
redis-cli ping
# Expected: PONG
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

**Minimum required configuration:**
```bash
# Database
DATABASE_URL=postgresql://localhost:5432/enterprise_agent_os

# Redis
REDIS_URL=redis://localhost:6379

# API
PORT=3000
NODE_ENV=development

# At least one system (for demo)
SALESFORCE_CLIENT_ID=your_salesforce_client_id
SALESFORCE_CLIENT_SECRET=your_salesforce_client_secret
SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com
```

### Step 4: Start Services

```bash
# Development mode (with hot reload)
npm run dev

# Production mode
npm run build
npm run start
```

### Step 5: Verify Installation

```bash
# Health check
curl http://localhost:3000/health

# Expected response:
{
  "status": "healthy",
  "components": [
    {"name": "database", "status": "healthy"},
    {"name": "redis", "status": "healthy"}
  ]
}
```

## First Permission Check

Let's test the core functionality:

```bash
curl -X POST http://localhost:3000/api/v1/permissions/check \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "demo@company.com",
    "resource": {
      "type": "customer",
      "id": "DEMO-001"
    },
    "action": "read",
    "systems": ["salesforce"]
  }'
```

**Expected response:**
```json
{
  "allowed": true,
  "permissionTopology": [
    {
      "system": "salesforce",
      "allowed": true,
      "permissions": ["read"],
      "source": "live"
    }
  ],
  "effectivePermissions": ["read"],
  "auditId": "audit-xxx-yyy",
  "metadata": {
    "latencyMs": 45,
    "cacheHit": false
  }
}
```

## Connect Your First System

### Salesforce Setup

1. **Create Connected App in Salesforce:**
   - Setup > Apps > App Manager > New Connected App
   - Enable OAuth Settings
   - Callback URL: `http://localhost:3000/auth/salesforce/callback`
   - Scopes: `full`, `api`, `refresh_token`

2. **Get Credentials:**
   - Consumer Key → `SALESFORCE_CLIENT_ID`
   - Consumer Secret → `SALESFORCE_CLIENT_SECRET`
   - Instance URL → `SALESFORCE_INSTANCE_URL`

3. **Update `.env`:**
   ```bash
   SALESFORCE_CLIENT_ID=your_consumer_key
   SALESFORCE_CLIENT_SECRET=your_consumer_secret
   SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com
   ```

4. **Test Connection:**
   ```bash
   curl http://localhost:3000/api/v1/adapters/salesforce/test
   ```

### Google Workspace Setup (Optional)

1. **Create Service Account:**
   - Go to Google Cloud Console
   - APIs & Services > Credentials
   - Create Service Account
   - Download JSON key

2. **Enable APIs:**
   - Admin SDK API
   - Drive API
   - Directory API

3. **Update `.env`:**
   ```bash
   GOOGLE_SERVICE_ACCOUNT_EMAIL=your-sa@project.iam.gserviceaccount.com
   GOOGLE_SERVICE_ACCOUNT_KEY=/path/to/key.json
   GOOGLE_ADMIN_EMAIL=admin@your-domain.com
   ```

4. **Test Connection:**
   ```bash
   curl http://localhost:3000/api/v1/adapters/google_workspace/test
   ```

## Admin UI Tour

Open http://localhost:3000/admin in your browser.

### Dashboard
- System health status
- Permission check rate
- Cache hit rate
- Connected systems

### Permission Check Tool
1. Enter user email
2. Select resource type and ID
3. Choose action (read/write/delete)
4. Select systems to check
5. Click "Check Permission"

View results:
- Permission topology (tree view)
- Conflicts (if any)
- Effective permissions
- Audit ID

### Audit Log Viewer
- Filter by user, resource, date range
- Export to CSV
- View permission topology for each check
- Detect anomalies

## Common Commands

```bash
# Development
npm run dev                 # Start dev server with hot reload
npm run test                # Run tests
npm run lint                # Lint code

# Database
npm run db:migrate          # Run migrations
npm run db:seed             # Seed demo data
npm run db:reset            # Reset database (WARNING: deletes data)

# Production
npm run build               # Build for production
npm run start               # Start production server

# Docker
docker-compose up -d        # Start all services
docker-compose down         # Stop all services
docker-compose logs -f      # View logs
docker-compose restart      # Restart services
```

## Troubleshooting

### Issue: Database connection failed

```bash
# Check PostgreSQL is running
pg_isready

# Check connection string
psql $DATABASE_URL

# Verify database exists
psql -l | grep enterprise_agent_os
```

### Issue: Redis connection failed

```bash
# Check Redis is running
redis-cli ping

# Check Redis URL
redis-cli -u $REDIS_URL ping
```

### Issue: Permission check returns 401 Unauthorized

```bash
# Verify system credentials
curl http://localhost:3000/api/v1/adapters/status

# Test specific system
curl http://localhost:3000/api/v1/adapters/salesforce/test
```

### Issue: High latency (> 100ms)

```bash
# Check cache hit rate
curl http://localhost:3000/metrics | grep cache_hit_rate

# Expected: > 80%

# Warm cache
curl -X POST http://localhost:3000/api/admin/cache/warm
```

## Next Steps

1. **Connect More Systems**
   - See [EXAMPLES.md](EXAMPLES.md) for SAP, Jira, Workday setup

2. **Create Workflows**
   - See [EXAMPLES.md](EXAMPLES.md) for workflow examples

3. **Setup Monitoring**
   - Configure Prometheus metrics export
   - Setup Grafana dashboards
   - Configure alerts

4. **Production Deployment**
   - See deployment guide in main documentation
   - Setup Kubernetes cluster
   - Configure high availability

5. **Pilot Program**
   - Onboard 1-2 users
   - Measure permission ticket reduction
   - Collect feedback

## Getting Help

- **Documentation**: Full docs in repository
- **Issues**: GitHub Issues
- **Email**: support@your-company.com
- **Slack**: Join our community (link in main README)

## What's Next?

- Read [EXAMPLES.md](EXAMPLES.md) for detailed usage examples
- Explore the Admin UI at http://localhost:3000/admin
- Check out the GraphQL Playground at http://localhost:3000/graphql
- Review architecture docs in the main repository

---

**You're ready to go!** Start with simple permission checks and gradually add more systems and workflows.
