# Freqtrade 一键部署

> 一键部署Freqtrade量化交易机器人

## 一、安装

```bash
bash <(curl -s https://raw.githubusercontent.com/freqtrade/freqtrade/develop/install.sh)
```

## 二、配置

```bash
cd freqtrade
freqtrade create-userdir --userdir user_data
freqtrade create-password --config user_data/config.json
```

编辑 `user_data/config.json`，填入API Key

## 三、启动

```bash
freqtrade trade --config user_data/config.json
```

## 四、WebUI

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

## 文档

- https://www.freqtrade.io
- https://www.itrade.icu/zh/freqtrade/freqtrade

## 开源协议

MIT License
基于 [Freqtrade](https://github.com/freqtrade/freqtrade) 构建
