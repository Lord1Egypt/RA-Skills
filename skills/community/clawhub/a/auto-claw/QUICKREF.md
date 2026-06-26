# Auto-Claw CLI — 快速参考卡

```bash
cd /root/.openclaw/workspace/auto-company/projects/auto-claw

# === 完整审计 (推荐第一次) ===
python3 cli.py full-audit

# === 单项命令 ===
python3 cli.py seo --url http://example.com --web-root /var/www/html
python3 cli.py performance --url http://example.com --web-root /var/www/html
python3 cli.py cache --url http://example.com --web-root /var/www/html
python3 cli.py content-audit --url http://example.com --web-root /var/www/html
python3 cli.py image --url http://example.com --web-root /var/www/html

# === 增长工具 ===
python3 cli.py ab-test --url http://example.com/landing --element headline
python3 cli.py exit-intent --headline "等等！别走"
python3 cli.py geo --city 北京 --base-price 99
python3 cli.py promo
python3 cli.py faq --category pricing

# === WordPress操作 ===
python3 cli.py wp status --web-root /var/www/html
python3 cli.py wp posts --web-root /var/www/html
python3 cli.py wp create --web-root /var/www/html --title "新文章" --status draft

# === 竞品监控 ===
python3 cli.py competitor --our-price 99 --name "竞品A" --competitor-url https://competitor.com

# === AI内容生成 ===
python3 cli.py ai-content --title "How AI Changes SEO" --keyword "AI SEO" --length long

# === 演示 ===
python3 demo_complete.py      # 全部19个能力
python3 demo_seo.py          # SEO专项
python3 demo_content_audit.py  # 内容审计
```

## 部署文档

| 文档 | 用途 |
|------|------|
| `docs/seo-deployment-20260324.md` | SEO修复40问题 |
| `docs/performance-deployment-20260324.md` | 性能优化 |
| `docs/quick-wins-20260324.md` | 无风险可执行项 |
| `README-exec.md` | 执行摘要 |

## Cron自动化

```bash
# 每日8点自动审计
0 8 * * * cd /root/.openclaw/workspace/auto-company/projects/auto-claw && ./logs/audit-daily.sh
```
