# Firecrawl Self-Hosting Reference Guide

This reference guide covers the setup, environment variables, and Docker Compose configurations for self-hosting Firecrawl.

## 1. Minimal Docker Compose Setup

```yaml
version: '3.8'

services:
  api:
    image: firecrawl/api:latest
    container_name: firecrawl-api
    restart: always
    ports:
      - "3002:3002"
    environment:
      - PORT=3002
      - HOST=0.0.0.0
      - REDIS_URL=redis://redis:6379/0
      - REDIS_RATE_LIMIT_URL=redis://redis:6379/1
      - PLAYWRIGHT_MICROSERVICE_URL=http://playwright-service:3000/scrape
      - USE_DB_AUTHENTICATION=false
    depends_on:
      - redis
      - playwright-service

  playwright-service:
    image: firecrawl/playwright-service:latest
    container_name: firecrawl-playwright
    restart: always
    environment:
      - PORT=3000
    resources:
      limits:
        cpus: '2.0'
        memory: 4096M

  redis:
    image: redis:7-alpine
    container_name: firecrawl-redis
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

---

## 2. Environment Variables Reference

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `PORT` | `3002` | Port for the main API entry server. |
| `HOST` | `0.0.0.0` | Binding host for the API server. |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string for the BullMQ job queue. |
| `REDIS_RATE_LIMIT_URL` | `redis://localhost:6379/1` | Redis connection string for rate limit tracking. |
| `PLAYWRIGHT_MICROSERVICE_URL` | `http://localhost:3000/scrape` | URL of the Playwright headless browser service. |
| `USE_DB_AUTHENTICATION` | `false` | Set to `true` to enable Supabase-based API key authentication. |
| `BULL_AUTH_KEY` | `None` | Authorization key for accessing the BullMQ queues admin panel. |
| `MAX_CPU` | `0.8` | Worker safety threshold: stops accepting new jobs if CPU usage exceeds 80%. |
| `MAX_RAM` | `0.8` | Worker safety threshold: stops accepting new jobs if RAM usage exceeds 80%. |
| `PROXY_SERVER` | `None` | Optional proxy server URL for rotating scraping requests. |
