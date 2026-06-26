---
name: clash-vpn
description: Manage Clash VPN proxy service for accessing blocked websites like Google Play. Use when the user needs to (1) setup/configure VPN proxy, (2) update Clash proxy configuration, (3) start/stop VPN service, (4) test proxy connectivity, or (5) access blocked resources through proxy.
---

# Clash VPN 管理

此 Skill 用于管理 Clash VPN 代理服务，实现访问 Google Play 等被屏蔽的网站。

## 前置条件

- Clash 已安装: `/usr/local/bin/clash`
- 配置文件路径: `/root/.config/clash/config.yaml`
- 脚本路径: `scripts/clash-vpn.sh`

## 快速开始

### 1. 更新配置文件

用户提供新的 Clash 配置时:

```bash
# 使用脚本更新配置
cat << 'EOF' | scripts/clash-vpn.sh update
port: 7890
socks-port: 7891
# ... 完整配置内容 ...
EOF
```

或直接写入文件:
```bash
cat > /root/.config/clash/config.yaml << 'EOF'
# 配置内容
EOF
```

### 2. 启动 VPN

```bash
scripts/clash-vpn.sh start
```

### 3. 测试连接

```bash
scripts/clash-vpn.sh test
```

### 4. 查看状态

```bash
scripts/clash-vpn.sh status
```

## 代理地址

启动后使用以下代理地址:

| 类型 | 地址 |
|------|------|
| HTTP | `http://127.0.0.1:7890` |
| SOCKS5 | `socks5://127.0.0.1:7891` |
| Mixed | `http://127.0.0.1:7893` |

## 使用代理访问网站

```bash
# HTTP 代理
curl --proxy http://127.0.0.1:7890 https://play.google.com

# SOCKS5 代理
curl --proxy socks5://127.0.0.1:7891 https://play.google.com
```

## 配置管理

### 配置模板

参考 `references/config-guide.md` 获取配置模板和字段说明。

### 配置更新流程

1. 接收用户的新配置内容
2. 使用脚本更新配置（自动备份旧配置）
3. 验证配置格式
4. 重启服务（如果正在运行）

### 配置备份

每次更新会自动创建备份:
```
/root/.config/clash/config.yaml.bak.YYYYMMDDHHMMSS
```

## 故障排查

### 查看日志

```bash
tail -f /var/log/clash.log
```

### 验证配置

```bash
clash -t -f /root/.config/clash/config.yaml
```

### 常见问题

1. **DNS 端口被占用**: 不影响使用，可忽略
2. **MMDB 下载失败**: 禁用 GEOIP 规则或手动下载
3. **连接失败**: 检查节点配置和网络连接

## 脚本命令参考

```bash
scripts/clash-vpn.sh start     # 启动
scripts/clash-vpn.sh stop      # 停止
scripts/clash-vpn.sh restart   # 重启
scripts/clash-vpn.sh status    # 状态
scripts/clash-vpn.sh test      # 测试连接
scripts/clash-vpn.sh update    # 更新配置（从 stdin）
scripts/clash-vpn.sh help      # 帮助
```
