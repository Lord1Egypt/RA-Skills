# Freqtrade 详细使用指南

## API Key 配置

### 币安API创建
1. 登录币安网页版
2. 进入「API管理」
3. 创建新API密钥
4. 绑定IP白名单（推荐）
5. 权限设置：**只开现货交易**，关闭杠杆和提币

### 配置文件模板

```json
{
    "exchange": {
        "name": "binance",
        "key": "你的API Key",
        "secret": "你的API Secret"
    },
    "api_server": {
        "enabled": true,
        "bind_address": "0.0.0.0",
        "bind_port": 41808,
        "username": "freqtrade",
        "password": "your_secure_password"
    }
}
```

## 常用命令

```bash
# 启动交易
freqtrade trade --config user_data/config.json --strategy <策略名>

# 后台运行
nohup freqtrade trade --config user_data/config.json --strategy <策略名> &

# 查看日志
tail -f logs/freqtrade.log

# 停止
freqtrade stop

# 查看状态
freqtrade status

# 查看余额
freqtrade balance

# 强制平仓
freqtrade forceexit <trade_id>
```

## WebUI 使用

- 地址: http://服务器IP:41808
- 用户名: freqtrade（可在config.json修改）
- 密码: 你设置的密码

### WebUI功能
- 查看持仓
- 查看交易历史
- 查看盈亏
- 手动平仓
- 修改配置

## 策略配置

### 策略文件位置
`user_data/strategies/`

### 策略参数（示例）

根据所选策略调整参数，详细请参考官方文档：
https://www.freqtrade.io/en/stable/strategy-customization/

### 创建自定义策略

```bash
freqtrade new-strategy --strategy AwesomeStrategy
```

## 回测

```bash
freqtrade backtesting --config user_data/config.json --strategy <策略名> --timerange 20240101-20240301
```

## 优化参数 (Hyperopt)

```bash
freqtrade hyperopt --config user_data/config.json --strategy <策略名> --timerange 20240101-20240301 -j 4
```

## 故障排查

### 常见问题

1. **WebUI打不开**: 检查端口是否开放、防火墙设置
2. **连接交易所失败**: 检查API Key是否正确、网络是否通
3. **订单不成交**: 检查余额是否充足、最小交易额设置
4. **进程自动退出**: 查看日志 `logs/freqtrade.log`

### 日志位置
- 主日志: `logs/freqtrade.log`
- 交易日志: `logs/trades.json`

## 安全建议

1. **API权限最小化**: 只开现货交易
2. **IP白名单**: 绑定API到固定IP
3. **资金控制**: 不要全部资金放入交易
4. **定期检查**: 定期查看交易记录和余额
5. **备份配置**: 备份config.json和策略文件
