# C02 - EdgeOne Pages

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C02 |
| 连接器名 | edgeone-pages |
| 显示名 | EdgeOne Pages |
| 层级 | L1 平台级 |
| 可替代 | ❌ 不可替代 |
| 分类 | 静态部署/CDN |

## 能力说明

EdgeOne Pages 提供边缘静态站点部署：

| 能力 | 说明 |
|------|------|
| 静态部署 | 一键部署 HTML/CSS/JS |
| 边缘节点 | 全球 CDN 节点加速 |
| 自定义域名 | 绑定自有域名，自动 HTTPS |
| 预览部署 | PR 预览，分支部署 |
| Serverless Functions | 边缘函数计算 |

## 为什么不可替代

**需要平台 CDN 基础设施**：
- 部署需要平台的全球边缘节点网络
- 域名绑定需要平台的 DNS 和证书管理
- 加速需要平台的 CDN 缓存和调度策略

**Skill 无法提供**：
- ❌ 无法提供全球 CDN 节点
- ❌ 无法提供域名解析和证书
- ❌ 无法提供边缘计算环境

## 使用场景

| 场景 | 说明 |
|------|------|
| 静态网站 | 博客、文档站、SPA 应用 |
| 前端部署 | React/Vue/Angular 应用部署 |
| 边缘计算 | 边缘函数、AB 测试 |
| 预览环境 | PR 预览、分支测试 |

## 配置方式

在 WorkBuddy 连接器管理页面启用 `edgeone-pages`，配置：
- API Token（EdgeOne API 令牌）
- Zone ID（站点 ID）

## 替代方案（非 Skill）

可使用其他静态部署平台：
- Vercel
- Netlify
- Cloudflare Pages
- GitHub Pages

但这些都需要平台账号和部署流程，不是 Skill 替代。
