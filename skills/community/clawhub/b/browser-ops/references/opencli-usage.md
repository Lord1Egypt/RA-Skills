# opencli 使用指南

## 三层能力

### 1. web read — 读任意网页（Cookie 零配置）

```bash
opencli web read --url "https://internal-site.com"
```

通过 Chrome Extension Bridge 让浏览器自身发请求，天然带 Cookie。

### 2. operate — 浏览器交互（17 个命令）

```bash
opencli operate open "url"
opencli operate state                    # 可交互元素 [1][2][3]
opencli operate click 5 / type 3 "hello" / select 2 "选项"
opencli operate scroll down / keys Enter / wait text "Success"
opencli operate screenshot /tmp/shot.png / network / close
```

### 3. 平台适配器 — 75 站点结构化数据

```bash
opencli list                             # 查看所有适配器
opencli twitter trending / zhihu hot / hackernews top
opencli xiaohongshu search "旅行攻略"
opencli web read --url "https://any-url"  # 万能回退
```

### 自动生成适配器

```bash
opencli explore "https://new-site.com"   # 探测接口和策略
opencli generate "https://new-site.com"  # 生成 YAML 适配器
```

## 健康检查

```bash
opencli doctor    # 三个 OK: Daemon + Extension + Connectivity
```

## 常见问题

| 问题 | 解决 |
|------|------|
| exit 77 | Chrome 里重新登录目标网站 |
| Extension MISSING | 加载扩展: `$(npm root -g)/@jackwener/opencli/extension` |
| google search CAPTCHA | 回退到 WebSearch 或 Tavily |
