# Platform Onboarding

## Supported Hosted Platforms

- <a href="https://ricebowl.ai">ricebowl.ai</a>

## First-Time Onboarding

```text
sign in
  -> buy credits or subscription
  -> open account / profile
  -> create API key
  -> copy plaintext key now
  -> ai-media config set-key ...
  -> ai-media models list --json
```

## ricebowl.ai

### 1. Recharge

- 打开 <a href="https://ricebowl.ai/pricing">ricebowl.ai/pricing</a>
- 选择适合的套餐或积分档位
- 完成支付后，credits 会进入当前账户

### 2. Generate API Key

基于站点源码，账号中心支持 `Profile -> API Keys`，并且 API Keys tab 的路由是：

```text
/profile?tab=api-keys
```

实际操作：

1. 登录 ricebowl.ai
2. 进入个人中心 `Profile`
3. 切到 `API Keys`
4. 点击 `Create API Key`
5. 立即复制明文 key

注意：

- 明文 key 只会完整显示一次
- key 前缀形如 `gm_xxx`
- 最好每个集成单独建一个 key，后续撤销更安全

### 3. Configure CLI

```bash
ai-media config set-key gm_xxx
ai-media config show
ai-media models list --json
```

## Environment Variable Setup

如果不想把 key 落到本地配置文件，可以直接用环境变量：

```bash
export AI_MEDIA_API_KEY=gm_xxx
```

历史兼容说明：

- 旧版脚本里可能还会出现 `AI_MEDIA_BASE_URL`
- 当前默认用户路径不再需要它
- 如果旧脚本依赖它，可以先保留，但新文档不再推荐

## First Working Commands

图片：

```bash
ai-media image generate \
  --model nano-banana \
  --prompt "a cinematic ramen bowl on a wooden table" \
  --aspect-ratio 1:1 \
  --wait
```

视频：

```bash
ai-media video generate \
  --model seedance-pro-fast \
  --prompt "steam rising from a rice bowl, cinematic close-up" \
  --aspect-ratio 16:9 \
  --duration 2 \
  --wait
```
