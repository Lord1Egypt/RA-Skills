# clash-auto-switch

> Clash 代理自动切换 Skill for OpenClaw

自动检测代理健康状态并在故障时自动切换到最佳节点。

## 配置

首次使用需要配置 Clash API：

```bash
# 设置 API 地址和密钥
/clash config set --api http://127.0.0.1:58871 --secret 你的密钥
```

或通过环境变量：
- `CLASH_API`: Clash API 地址
- `CLASH_SECRET`: API 密钥
- `CLASH_PROXY`: 代理地址 (默认: http://127.0.0.1:7890)

## 功能

### 健康检查

检查当前代理是否正常工作：

```
/clash health
```

返回示例：
```
✓ 代理健康 (3/3)
- Telegram: OK
- Google: OK
- Anthropic: OK
```

### 列出节点

查看所有代理组和可用节点：

```
/clash list
```

### 自动切换

自动检测并切换到最佳节点：

```
/clash auto
```

逻辑：
1. 测试 Telegram / Google / Anthropic 连通性
2. 如果不健康，遍历所有节点
3. 测试延迟，优先选择新加坡/日本/香港/美国节点
4. 切换到最佳节点

### 手动切换

切换到指定节点：

```
/clash switch ChatGPT 新加坡-优化-Gemini-GPT
```

### 区域切换

快速切换到指定区域：

```
/clash sg    # 切换到新加坡
/clash us    # 切换到美国
/clash jp    # 切换到日本
/clash hk    # 切换到香港
```

### 状态查询

查看当前代理状态：

```
/clash status
```

## 在 Cron 中使用

添加到 cron job 实现定时健康检查：

```json
{
  "name": "clash-health-check",
  "schedule": {
    "kind": "every",
    "everyMs": 900000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "/clash auto"
  },
  "sessionTarget": "isolated"
}
```

## 在 Heartbeat 中使用

在 heartbeat 中添加健康检查：

```
# 在 HEARTBEAT.md 中添加
/clash health
```

## 支持的代理组

- ChatGPT
- Copilot
- GLOBAL
- Netflix
- Steam
- Telegram
- TikTok
- Twitter
- WhatsApp
- 境内使用
- 海外使用
- 节点选择
- 谷歌服务
- 微软服务
- 苹果服务

## 示例对话

**用户**: 检查代理状态  
**小溪**: 调用 `/clash health` → 返回健康度

**用户**: 代理好像很慢  
**小溪**: 调用 `/clash auto` → 自动切换到最佳节点

**用户**: 切换到新加坡节点  
**小溪**: 调用 `/clash sg` → 切换完成

## 实现原理

1. 调用 Clash API (`/proxies`) 获取所有代理组
2. 对每个 Selector 类型的代理组执行健康检查
3. 如果不健康，测试所有节点延迟
4. 优先选择优先区域的节点
5. 调用 Clash API (`/proxies/{group}`) 切换节点
