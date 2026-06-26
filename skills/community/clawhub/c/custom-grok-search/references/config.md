# custom-grok-search 配置说明

这个 Skill 支持两种模式：

## 1）官方 xAI 模式

不需要 `CUSTOM_*` 变量，只要有官方 xAI Key 即可。

示例：

```bash
export XAI_API_KEY="your-xai-key"
node scripts/grok_search.mjs "OpenAI latest news" --web
```

默认值：
- base URL：`https://api.x.ai/v1`
- model：`grok-4-1-fast`

## 2）公益站 / 第三方 Grok 兼容代理模式

如果存在 `CUSTOM_GROK_APIKEY`，脚本会自动切换到第三方代理模式。

适用于：
- 公益站提供的 Grok 兼容接口
- 自建代理
- 其他兼容 xAI / OpenAI Responses API 形态的第三方服务

推荐变量：

```bash
CUSTOM_GROK_APIKEY=your-proxy-key
CUSTOM_GROK_BASE_URL=https://your-proxy.example/v1
CUSTOM_GROK_MODEL=grok-4.20-beta
CUSTOM_GROK_USER_AGENT=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

## `.env` 放置位置

脚本会自动加载这些位置的 `.env`：

- 当前工作目录：`$PWD/.env`
- `~/.openclaw/.env`

所以如果 OpenClaw 从你的 workspace 启动命令，把 `CUSTOM_*` 写进对应 `.env` 就可以生效。

## 回退逻辑

- 如果存在 `CUSTOM_GROK_APIKEY` → 使用公益站 / 第三方代理模式
- 否则 → 使用官方 xAI 模式
- 如果命令里传了 `--model <id>`，则只覆盖当前这一次调用
