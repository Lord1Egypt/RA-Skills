# Cloudflare Developer Platform Skill for OpenClaw

> **English** | [Tiếng Việt](#tiếng-việt)

## Overview

A comprehensive OpenClaw skill for Cloudflare Developer Platform, covering Workers, Pages, D1, R2, KV, AI services, security best practices, and deployment patterns. Built from the complete [Cloudflare Starter Hub](https://onboarding.orangecloud.vn/) learning path.

## What's Included

- ✅ **Quick Actions** - Deploy Workers, setup D1/R2, common workflows
- ✅ **Decision Trees** - Storage choice (KV/D1/R2), SSL/TLS modes, cache strategies
- ✅ **Best Practices** - Workers, D1, Security, Performance optimization
- ✅ **Common Mistakes & Fixes** - Troubleshooting table with solutions
- ✅ **Architecture Patterns** - Fullstack apps, APIs, RAG with Workers AI
- ✅ **Troubleshooting Guides** - Step-by-step debugging workflows

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install cloudflare-developer
```

### Manual Installation

```bash
cd ~/.openclaw/skills
git clone https://github.com/infamoustho/cloudflare-developer-skill cloudflare-developer
```

## Usage

Once installed, the skill provides comprehensive guidance for:

1. **Deploying serverless applications** - Workers, Pages, full-stack apps
2. **Setting up storage** - D1 databases, KV namespaces, R2 buckets
3. **Configuring security** - WAF, SSL/TLS, bot protection, rate limiting
4. **Optimizing performance** - CDN cache, Tiered Cache, image optimization
5. **Troubleshooting issues** - Common errors with specific fixes
6. **Applying architecture patterns** - Production-ready templates

## Key Decision Trees

### Storage Choice
```
Config/flags → KV
Structured data (SQL) → D1
Files/uploads → R2
```

### SSL/TLS Mode
```
Valid cert → Full (strict) ✅
Self-signed → Full
HTTP only → Flexible (avoid if possible)
```

### Cache Strategy
```
Static assets → Cache (long TTL)
Dynamic HTML → Bypass
API with auth → Bypass
```

## Example Workflows

### Deploy a Worker
```bash
wrangler init my-worker
wrangler dev
wrangler deploy
```

### Setup D1 Database
```bash
wrangler d1 create my-db
# Add binding to wrangler.toml
wrangler d1 migrations apply my-db
```

### Setup R2 Bucket
```bash
wrangler r2 bucket create my-bucket
# Add binding to wrangler.toml
```

## Resources

- [Cloudflare Developer Docs](https://developers.cloudflare.com/)
- [Cloudflare Starter Hub](https://onboarding.orangecloud.vn/)
- [Developer Changelog](https://developers.cloudflare.com/changelog/)
- [Community Forums](https://community.cloudflare.com/)

## Contributing

Contributions welcome! Please open an issue or PR on GitHub.

## License

MIT

---

## Tiếng Việt

# Skill Cloudflare Developer Platform cho OpenClaw

## Tổng quan

Skill toàn diện cho OpenClaw về Cloudflare Developer Platform, bao gồm Workers, Pages, D1, R2, KV, AI services, best practices bảo mật, và deployment patterns. Được xây dựng từ lộ trình học đầy đủ của [Cloudflare Starter Hub](https://onboarding.orangecloud.vn/).

## Nội dung

- ✅ **Quick Actions** - Deploy Workers, setup D1/R2, workflows thường dùng
- ✅ **Decision Trees** - Chọn storage (KV/D1/R2), SSL/TLS modes, cache strategies
- ✅ **Best Practices** - Workers, D1, Security, Performance optimization
- ✅ **Common Mistakes & Fixes** - Bảng troubleshooting với giải pháp
- ✅ **Architecture Patterns** - Fullstack apps, APIs, RAG với Workers AI
- ✅ **Troubleshooting Guides** - Workflows debug từng bước

## Cài đặt

### Qua ClawHub (Khuyên dùng)

```bash
clawhub install cloudflare-developer
```

### Cài đặt thủ công

```bash
cd ~/.openclaw/skills
git clone https://github.com/infamoustho/cloudflare-developer-skill cloudflare-developer
```

## Sử dụng

Sau khi cài đặt, skill cung cấp hướng dẫn đầy đủ cho:

1. **Deploy serverless applications** - Workers, Pages, full-stack apps
2. **Setup storage** - D1 databases, KV namespaces, R2 buckets
3. **Configure security** - WAF, SSL/TLS, bot protection, rate limiting
4. **Optimize performance** - CDN cache, Tiered Cache, image optimization
5. **Troubleshoot issues** - Lỗi thường gặp với fixes cụ thể
6. **Apply architecture patterns** - Templates production-ready

## Decision Trees Chính

### Chọn Storage
```
Config/flags → KV
Structured data (SQL) → D1
Files/uploads → R2
```

### SSL/TLS Mode
```
Có valid cert → Full (strict) ✅
Self-signed → Full
Chỉ HTTP → Flexible (tránh nếu có thể)
```

### Cache Strategy
```
Static assets → Cache (long TTL)
Dynamic HTML → Bypass
API có auth → Bypass
```

## Workflows Ví dụ

### Deploy Worker
```bash
wrangler init my-worker
wrangler dev
wrangler deploy
```

### Setup D1 Database
```bash
wrangler d1 create my-db
# Thêm binding vào wrangler.toml
wrangler d1 migrations apply my-db
```

### Setup R2 Bucket
```bash
wrangler r2 bucket create my-bucket
# Thêm binding vào wrangler.toml
```

## Tài nguyên

- [Cloudflare Developer Docs](https://developers.cloudflare.com/)
- [Cloudflare Starter Hub](https://onboarding.orangecloud.vn/)
- [Developer Changelog](https://developers.cloudflare.com/changelog/)
- [Community Forums](https://community.cloudflare.com/)

## Đóng góp

Rất hoan nghênh đóng góp! Vui lòng mở issue hoặc PR trên GitHub.

## License

MIT
