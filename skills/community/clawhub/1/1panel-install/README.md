# 1Panel 安装技能

一键安装 1Panel 服务器管理面板并获取访问信息。

## 功能

- ✅ 自动检测 1Panel 是否已安装
- ✅ 未安装时自动下载并安装（默认配置，不装 Docker）
- ✅ 已安装时直接显示访问信息
- ✅ 完整的错误处理和日志输出
- ✅ 自然语言格式的安装结果

## 安装方法

将 `1panel-install` 文件夹复制到 OpenClaw 的 skills 目录：

```bash
cp -r 1panel-install /root/.openclaw/workspace/skills/
```

## 使用方法

在对话中直接请求安装：

```
安装 1Panel
```

或者：

```
帮我部署 1Panel
```

助手会自动执行安装并返回访问地址、用户名、密码等信息。

## 技术细节

- 安装包来源：官方 Cloudflare CDN
- 1Panel 版本：v2.1.4
- 安装路径：/opt
- 是否安装 Docker：否
- 语言：中文
- 依赖：bash, curl, tar, systemd

## 测试

运行测试脚本：

```bash
cd /root/.openclaw/workspace/skills/1panel-install
chmod +x install.sh
sudo ./install.sh
```

预期输出：
- 如果未安装：显示安装进度，最后输出访问信息
- 如果已安装：直接输出访问信息

## 注意事项

⚠️ **需要 root 权限**：安装过程需要创建系统服务，请使用 sudo 执行或在 root 会话中运行。

⚠️ **网络要求**：需要能够访问 `resource.fit2cloud.com` 下载安装包。

⚠️ **安全提醒**：
- 安装完成后立即修改默认密码：`1pctl update password`
- 在云服务器安全组中打开 1Panel 端口（**注意：端口是随机生成的**）
- 定期更新系统和 1Panel

**访问提示**：
如果地址无法访问，或者服务器没有公网 IP，推荐使用 **Cloudflare Tunnel** 功能配置域名访问，实现安全的内网穿透，无需开放公网端口。

**重要**：1Panel 每次安装时，以下信息都是**随机生成**的：
- 端口号（默认范围 30000-40000）
- 访问路径（Security Entry，随机字符串）
- 面板用户名
- 面板密码

请以实际 `1pctl user-info` 输出为准。

## 故障排查

### 安装失败

查看安装日志：
```bash
cat /opt/1panel/install.log 2>/dev/null || echo "日志不存在"
```

### 服务无法启动

```bash
systemctl status 1panel-core
journalctl -u 1panel-core -n 50
```

### 无法访问面板

- 检查防火墙：`sudo ufw status` 或 `firewall-cmd --list-all`
- 检查端口是否监听：`ss -tlnp | grep 37987`
- 检查安全组（云服务器）

## License

MIT

## 作者

OpenClaw Agent
2025-03-13
