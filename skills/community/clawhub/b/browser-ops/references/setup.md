# 安装与验证

## 必装

```bash
npm i -g @jackwener/opencli
# Chrome 装扩展: $(npm root -g)/@jackwener/opencli/extension
opencli doctor  # 三个 OK
```

## 按需

```bash
npm i -g agent-browser               # 复杂交互
pip install browser-use               # AI Agent (或 uv pip install)
pip install zendriver                  # 反爬
pip install tavily-python              # 搜索 (需 TAVILY_API_KEY)
pip install firecrawl                  # 提取 (需 FIRECRAWL_API_KEY)
```

## 健康检查

```bash
bash scripts/sync-cookies.sh health
```

## 故障排查

| 问题 | 解决 |
|------|------|
| Extension MISSING | Chrome 加载扩展: `$(npm root -g)/@jackwener/opencli/extension` |
| Daemon not running | `opencli daemon restart` |
| web read 返回 302/403 | Chrome 里重新登录目标网站 |
| tavily/firecrawl API error | 检查环境变量: `echo $TAVILY_API_KEY` |
