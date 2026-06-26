# Auto-Claw 性能优化部署方案

**生成时间**: 2026-03-24 09:00 UTC  
**目标站点**: http://linghangyuan1234.dpdns.org  
**当前性能评分**: 40/100  
**目标性能评分**: 70+/100

---

## 📊 诊断结果

### 缓存状态

| 缓存类型 | 状态 | TTL | 影响 |
|---------|------|-----|------|
| 页面缓存 | ❌ 未启用 | 0s | 🔴 高 |
| 浏览器缓存 | ✅ 已启用 | 86400s | 🟢 低 |
| Opcode缓存 | ✅ 已启用 | 3600s | 🟢 低 |
| 对象缓存 | ❌ 未启用 | 0s | 🔴 高 |

### 核心问题

1. **页面缓存未启用** — 最影响TTFB，拖慢整体加载50-80%
2. **对象缓存未启用** — 数据库查询未缓存，高并发时崩溃风险

### 当前TTFB问题

从性能诊断结果看，TTFB (Time To First Byte) 极高，可能原因：
- 无页面缓存，每次请求都执行PHP+数据库
- 无对象缓存，重复查询数据库
- PHP-FPM配置可能不足

---

## 🔧 修复步骤

### Step 1: 安装页面缓存插件

推荐使用 **WP Super Cache**（轻量级，适合1-5人小团队）：

```bash
cd /www/wwwroot/linghangyuan1234.dpdns.org

# 安装WP Super Cache
WP_CLI_PHP=/www/server/php/82/bin/php /usr/local/bin/wp plugin install wp-super-cache --activate

# 验证
WP_CLI_PHP=/www/server/php/82/bin/php /usr/local/bin/wp plugin list | grep wp-super-cache
```

**备选**: 如果需要更高级功能（CDN集成、懒加载），使用 **WP Rocket**：
```bash
# WP Rocket需要手动上传激活，此处略过
```

### Step 2: 安装Redis对象缓存

```bash
# 安装Redis服务端（如果尚未安装）
apt-get install redis-server

# 启动Redis
systemctl enable redis
systemctl start redis

# 验证Redis
redis-cli ping
# 应返回: PONG

# 安装Redis对象缓存插件
WP_CLI_PHP=/www/server/php/82/bin/php /usr/local/bin/wp plugin install redis-cache --activate

# 启用Redis对象缓存
WP_CLI_PHP=/www/server/php/82/bin/php /usr/local/bin/wp redis enable

# 验证
WP_CLI_PHP=/www/server/php/82/bin/php /usr/local/bin/wp redis status
```

### Step 3: 配置Nginx FastCGI缓存（可选，更高效）

在 `/etc/nginx/sites-available/linghangyuan1234` 添加：

```nginx
# FastCGI缓存配置
fastcgi_cache_path /var/cache/nginx/wordpress levels=1:2 keys_zone=WORDPRESS:100m inactive=60m;

# 缓存键
fastcgi_cache_key "$scheme$request_method$host$request_uri";

# WordPress特定规则
set $skip_cache 0;
if ($request_method = POST) { set $skip_cache 1; }
if ($query_string != "") { set $skip_cache 1; }
if ($request_uri ~* "/wp-admin/|/wp-json/|/cart/|/checkout/") {
    set $skip_cache 1;
}

# 缓存响应
fastcgi_cache WORDPRESS;
fastcgi_cache_valid 200 60m;
add_header X-Cache-Status $upstream_cache_status always;
```

### Step 4: 一键部署脚本

```bash
#!/bin/bash
# auto-claw-performance-fix.sh

set -e

WEB_ROOT="/www/wwwroot/linghangyuan1234.dpdns.org"
PHP_BIN="/www/server/php/82/bin/php"
WP_CLI="/usr/local/bin/wp"
WP="$PHP_BIN $WP_CLI --allow-root --path=$WEB_ROOT"

echo "🚀 开始性能优化..."

# 1. 安装WP Super Cache
echo "📦 安装WP Super Cache..."
$WP plugin install wp-super-cache --activate

# 2. 安装Redis
echo "📦 安装Redis..."
apt-get install -y redis-server > /dev/null 2>&1
systemctl enable redis > /dev/null 2>&1
systemctl start redis > /dev/null 2>&1

# 3. 安装Redis缓存插件
echo "📦 安装Redis对象缓存..."
$WP plugin install redis-cache --activate
$WP redis enable

# 4. 清理缓存
echo "🧹 清理WordPress缓存..."
$WP cache flush

# 5. 重启PHP-FPM
echo "🔄 重启PHP-FPM..."
systemctl restart php-fpm

echo "✅ 性能优化完成！"
echo ""
echo "验证命令:"
echo "  $WP plugin list | grep -E 'wp-super-cache|redis-cache'"
echo "  redis-cli ping"
```

---

## 📋 预期效果

| 指标 | 修复前 | 修复后 | 改善 |
|------|--------|--------|------|
| 性能评分 | 40/100 | 70+/100 | +75% |
| TTFB | 极高 | <500ms | -80% |
| 数据库查询 | 每次执行 | 缓存命中 | -70% |
| 并发能力 | 低 | 高 | +200% |

---

## ⏱️ 紧急程度

| 优先级 | 问题 | 理由 |
|--------|------|------|
| 🔴 高 | 页面缓存未启用 | TTFB极高，用户体验差 |
| 🔴 高 | 对象缓存未启用 | 数据库压力大 |
| 🟡 中 | Nginx FastCGI | 可选，更进一步 |

---

## ❌ 不可执行项（需用户授权）

以下操作属于 **MEDIUM/HIGH 风险**，需要通过Gate Pipeline审批：

1. `plugin install wp-super-cache` — MEDIUM
2. `plugin install redis-cache` — MEDIUM
3. `systemctl restart php-fpm` — HIGH

**回复 `approve performance` 授权执行，或手动SSH运行上述脚本。**

---

## 🔄 后续监控

修复后，每日监控命令：
```bash
cd /root/.openclaw/workspace/auto-company/projects/auto-claw
python3 cli.py performance --url http://linghangyuan1234.dpdns.org
```

配置Cron每日报告：
```bash
# 每天上午9点性能报告
0 9 * * * cd /root/.openclaw/workspace/auto-company/projects/auto-claw && python3 cli.py performance --url http://linghangyuan1234.dpdns.org >> logs/performance-daily.log 2>&1
```

---

*由 Auto-Claw CEO Agent 生成 | 2026-03-24*
