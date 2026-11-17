---
name: central-model-switch
description: OpenClaw 模型切换与救援技能。当模型 API 不可用时切换模型，或处理节点配对问题。触发词：模型切换、API用完、Central救援、节点掉线。⚠️ 使用前必须配置环境变量，详见变量说明。
---

# OpenClaw 模型切换与救援

⚠️ **安全警告**：使用前必须配置以下环境变量，勿直接运行！

## 变量配置

| 变量 | 说明 | 示例值 |
|------|------|--------|
| CENTRAL_IP | 中央服务器 IP | 从配置文件获取 |
| SSH_KEY | SSH 私钥路径 | ~/.ssh/id_ed25519 |
| API_KEY | 模型 API Key | 从平台获取 |

## 实施步骤

### 1. 连接目标服务器
```bash
ssh -i $SSH_KEY root@$CENTRAL_IP
```

### 2. 检查当前配置
```bash
cat ~/.openclaw/openclaw.json | grep -A5 'primary'
```

### 3. 更新模型配置

根据你的模型提供商修改配置（以 OpenAI 为例）：

```bash
# 备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 使用 sed 修改默认模型（请根据实际情况调整）
sed -i 's/"primary": "[^"]*"/"primary": "gpt-4o-mini"/' ~/.openclaw/openclaw.json
```

或使用 Python：

```python3
import json

with open('/root/.openclaw/openclaw.json', 'r') as f:
    cfg = json.load(f)

# 修改默认模型
cfg['agents']['defaults']['model']['primary'] = 'your-model-id'

with open('/root/.openclaw/openclaw.json', 'w') as f:
    json.dump(cfg, f, indent=2)
```

### 4. 重启 Gateway

优先使用 systemd：
```bash
sudo systemctl restart openclaw-gateway
```

如无 systemd：
```bash
cd ~/.openclaw
pkill -f openclaw-gateway
nohup npx openclaw gateway > /tmp/gateway.log 2>&1 &
```

### 5. 验证
```bash
# 检查进程状态
ps aux | grep openclaw-gateway

# 测试 API
curl -s http://localhost:18789/health
```

## 节点配对救援（如掉线）

### 节点重新配对

```bash
# 删除旧的配对信息
rm ~/.openclaw/node.json

# 重新启动节点
cd ~/.openclaw
npx openclaw node run --host <gateway_ip> --port <gateway_port>
```

## 安全建议

1. **始终备份**：修改配置前先备份
2. **验证 IP**：确认目标服务器 IP 正确
3. **检查 Key**：API Key 只在本地使用，勿上传
4. **最小权限**：使用 sudo 而非 root 登录
5. **监控日志**：查看 `/tmp/gateway.log` 排查问题

## 相关文件

- `~/.openclaw/openclaw.json` - 配置文件
- `/tmp/gateway.log` - 运行日志
