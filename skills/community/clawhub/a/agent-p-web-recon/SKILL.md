---
name: web-recon
description: 网站内容侦察技能。无需登录即可获取网站公开/半公开内容。使用场景：(1) 竞品分析收集公开信息，(2) 安全评估未授权访问点，(3) OSINT 情报收集，(4) 网站内容存档，(5) 监控页面变化。合法用途仅限：授权渗透测试、公开信息收集、自有系统审计。
---

# Web Recon - 网站内容侦察

## 角色设定

**P 的侦察模式** - 用黑客思维发现暴露面，用红客原则保护边界。

## 核心原则

1. **合法合规** - 仅用于授权测试/公开信息/自有系统
2. **被动优先** - 优先无接触方式（快照/缓存/搜索引擎）
3. **不留痕迹** - OSINT 手段不接触目标服务器
4. **道德边界** - 不绕过付费墙、不窃取敏感数据

---

## 技术方法库

### 方法 1: 搜索引擎快照（被动，无痕迹）

```bash
# Google 缓存
https://webcache.googleusercontent.com/search?q=cache:TARGET_URL

# Wayback Machine 历史快照
https://web.archive.org/web/*/TARGET_URL

# 搜索引擎 site: 语法
site:target.com inurl:admin
site:target.com filetype:pdf
```

**优点:** 完全被动，不留痕迹
**局限:** 依赖搜索引擎索引

### 方法 2: 爬虫模拟（半被动）

某些网站对爬虫开放内容（SEO 需求）：

```python
# 修改 User-Agent 伪装爬虫
headers = {
    "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
}
```

**识别信号:**
- 同一 URL，不同 User-Agent 返回不同内容
- robots.txt 允许爬虫访问的路径

### 方法 3: 公共 API 探测（主动）

很多网站有未授权或弱授权的 API：

```bash
# 常见 API 端点
/api/v1/posts
/api/v1/users
/graphql
/api/feed
/rss
/atom.xml
```

**工具:**
```bash
# 使用 gau 获取已知 URL
gau target.com | grep api

# 使用 waybackurls 获取历史 URL
waybackurls target.com | grep -E "\.json|xml|rss"
```

### 方法 4: 前端逻辑绕过（主动，需授权）

针对初级程序员的伪防护：

```javascript
// 禁用 JavaScript 绕过登录弹窗
// 方法：浏览器 DevTools → Settings → Disable JavaScript

// 直接访问渲染后的内容
// 某些 SPA 应用内容已加载，只是被遮罩层挡住

// 查看网络请求
// DevTools → Network → 查找 API 响应中的完整数据
```

### 方法 5: 目录扫描（主动，需授权）

发现未授权访问的路径：

```bash
# 使用 dirsearch
dirsearch -u https://target.com -e php,html,js,json

# 使用 gobuster
gobuster dir -u https://target.com -w common.txt
```

**常见暴露路径:**
```
/admin
/dashboard
/api/v1/export
/backup/
/.git/
/config.php
```

### 方法 6: RSS/Atom 订阅（被动）

很多网站提供公开 RSS：

```bash
# 常见位置
/rss
/rss.xml
/feed
/atom.xml
/blog/rss
```

---

## 工作流程

### 阶段 1: 被动收集（推荐优先）

```
1. 搜索引擎查询（site: / inurl: / filetype:）
2. Wayback Machine 历史快照
3. Google Cache 缓存
4. 检查 RSS/Atom 订阅
```

### 阶段 2: 半主动探测（需谨慎）

```
1. 修改 User-Agent 测试爬虫权限
2. 探测公共 API 端点
3. 检查 robots.txt 配置
```

### 阶段 3: 主动扫描（仅限授权）

```
1. 目录扫描（dirsearch/gobuster）
2. 前端逻辑测试（禁用 JS）
3. 网络请求分析（DevTools）
```

---

## 输出格式

```markdown
## 侦察报告：TARGET_URL

### 发现内容
| 路径 | 内容类型 | 访问方式 | 风险等级 |
|------|----------|----------|----------|
| /api/posts | JSON | 公开 | 中 |
| /admin | HTML | 未授权 | 高 |

### 敏感暴露
- [ ] 用户数据泄露
- [ ] 内部路径暴露
- [ ] 配置文件可访问
- [ ] 备份文件未保护

### 建议修复
1. ...
2. ...
```

---

## 安全与合规

### 合法用途 ✅
- 授权渗透测试
- 自有系统安全审计
- 公开信息收集（OSINT）
- 竞品公开信息分析

### 非法用途 ❌
- 未授权访问付费内容
- 窃取用户隐私数据
- 绕过商业系统的访问控制
- 恶意信息收集

### 风险评估

| 方法 | 法律风险 | 技术风险 | 建议 |
|------|----------|----------|------|
| 搜索引擎快照 | 无 | 无 | 安全 |
| Wayback Machine | 无 | 无 | 安全 |
| 爬虫模拟 | 低 | 低 | 注意 robots.txt |
| API 探测 | 中 | 中 | 仅限授权 |
| 目录扫描 | 高 | 高 | 必须授权 |

---

## 参考资源

- **OWASP 测试指南** → `references/owasp-testing.md`
- **OSINT 框架** → `references/osint-framework.md`
- **工具脚本** → `scripts/` 目录

---

*P 注：技术无罪，关键在用途。永远站在防御者一边。*
