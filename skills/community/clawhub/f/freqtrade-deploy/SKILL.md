---
name: freqtrade-deploy
description: 一键部署Freqtrade量化交易机器人。支持现货交易策略，自动安装依赖、配置策略、设置WebUI监控。
---

# Freqtrade 一键部署

## 安装命令

直接在终端执行：

```bash
bash <(curl -s https://raw.githubusercontent.com/freqtrade/freqtrade/develop/install.sh)
```

## 安装后配置

### 1. 创建用户目录和密码
```bash
cd freqtrade
freqtrade create-userdir --userdir user_data
freqtrade create-password --config user_data/config.json
```

### 2. 编辑配置文件
编辑 `user_data/config.json`，填入交易所API Key：
```json
{
    "exchange": {
        "name": "binance",
        "key": "你的API Key",
        "secret": "你的API Secret"
    }
}
```

### 3. 启动
```bash
freqtrade trade --config user_data/config.json
```

### 4. 访问WebUI
```
http://localhost:8080
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `freqtrade start` | 启动 |
| `freqtrade stop` | 停止 |
| `freqtrade status` | 状态 |
| `freqtrade balance` | 余额 |
| `freqtrade trades` | 交易记录 |

## 详细文档

- 官方: https://www.freqtrade.io
- 中文: https://www.itrade.icu/zh/freqtrade/freqtrade
