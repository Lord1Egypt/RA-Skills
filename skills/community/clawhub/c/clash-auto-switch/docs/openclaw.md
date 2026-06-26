# OpenClaw Skill 安装指南

本指南详细介绍如何在 OpenClaw 中安装和使用 clash-auto-switch Skill。

## 安装步骤

### 1. 安装 Skill

```bash
npx clawdhub install clash-auto-switch
```

### 2. 配置 Clash API

需要在 OpenClaw 配置文件中添加环境变量。

找到你的 `openclaw.json` 配置文件，添加以下内容：

```json
{
  "env": {
    "CLASH_API": "http://127.0.0.1:58871",
    "CLASH_SECRET": "你的Clash密钥",
    "CLASH_PROXY": "http://127.0.0.1:7890"
  }
}
```

> ⚠️ **注意**：端口可能因人而异，请查看你自己 Clash for Windows 的配置：
> - 打开 Clash for Windows
> - 点击设置 → 找到「实验性功能」中的 `external-controller`
> - 格式通常是 `127.0.0.1:端口号`

### 3. 重启 OpenClaw

配置完成后，重启 OpenClaw 使配置生效。

## 使用方法

安装并配置完成后，直接对 AI 说：

### 基础命令

| 命令 | 说明 |
|------|------|
| `/clash health` | 健康检查 |
| `/clash list` | 列出所有代理组和节点 |
| `/clash status` | 查看当前状态 |
| `/clash auto` | 自动切换到最佳节点 |

### 快速切换

| 命令 | 说明 |
|------|------|
| `/clash sg` | 切换到新加坡节点 |
| `/clash us` | 切换到美国节点 |
| `/clash jp` | 切换到日本节点 |
| `/clash hk` | 切换到香港节点 |

### 手动切换

```
/clash switch ChatGPT 新加坡-优化-Gemini-GPT
```

格式：`/clash switch <代理组名> <节点名>`

## 获取 Clash API 信息

### 方法 1：查看 Clash for Windows 配置

1. 打开 Clash for Windows
2. 点击左上角菜单 → 设置
3. 找到「外部控制」
4. 会看到类似 `127.0.0.1:58871` 的地址

### 方法 2：查看配置文件

打开 Clash 配置文件（config.yaml），查找：

```yaml
external-controller: 127.0.0.1:58871
secret: 你的密钥
```

## 定时自动切换

### 创建 Cron Job

在 OpenClaw 中创建定时任务，自动检查并切换：

```json
{
  "name": "clash-auto-switch",
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

这会每 15 分钟自动检查一次，如果代理不健康则自动切换。

## 常见问题

### Q: 为什么健康检查失败？

A: 检查以下几点：
1. Clash for Windows 是否正在运行
2. API 地址和端口是否正确
3. API 密钥是否正确
4. 代理是否已连接

### Q: 切换后仍然不健康怎么办？

A: 可以尝试：
1. 手动指定节点：`/clash switch ChatGPT 美国LA-优化-GPT`
2. 检查是否是目标网站本身的问题
3. 查看日志了解具体错误

### Q: 如何查看当前使用的节点？

A: 使用 `/clash status` 命令

## 示例对话

**用户**: 检查下代理状态  
**AI**: 调用 `/clash health` → 返回 `✓ 代理健康 (3/3)`

**用户**: 代理好慢  
**AI**: 调用 `/clash auto` → 自动切换到最佳节点

**用户**: 切换到新加坡  
**AI**: 调用 `/clash sg` → 切换完成

---

## 相关链接

- [GitHub 仓库](https://github.com/adminlove520/clash-auto-switch)
- [ClawHub](https://clawhub.com/package/clash-auto-switch)
- [原始 README](./README.md)
