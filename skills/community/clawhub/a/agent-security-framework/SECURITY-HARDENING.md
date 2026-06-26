# ASF-26 Website Security Hardening

## Threat Model

**Who might attack the website:**
- External attackers seeking API access
- Malicious agents trying to inject content
- DDoS attempts
- Spam bots

## Security Controls

### 1. HTTPS & TLS
```yaml
# nginx.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;
```

### 2. Web Application Firewall
- Rate limiting: 100 req/min per IP
- Bot detection
- SQL injection protection
- XSS prevention

### 3. Authentication
- API key authentication for agent access
- OIDC for admin panel
- mTLS for agent ↔ website communication

### 4. Monitoring
- Log all requests to secure logging system
- Alert on anomalous patterns
- Integrate with ASF security tools

## Docker Compose Hardened Stack

```yaml
services:
  website:
    image: wordpress
    ports:
      - "443:443"
    environment:
      - HTTPS=on
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - asf_internal
  
  waf:
    image: modsecurity/nginx-modsecurity
    volumes:
      - ./owasp-modsecurity-crs:/etc/modsecurity.d:ro
```

## Integration with ASF Tools

- Port scan detection: security-tools/port-scan-detector.sh
- Fake agent detection: security-tools/fake-agent-detector.sh
- Spam monitoring: security-tools/moltbook-spam-monitor.sh

See also: security-v3-comprehensive.md, moltbook-security-proposal-v2.md
