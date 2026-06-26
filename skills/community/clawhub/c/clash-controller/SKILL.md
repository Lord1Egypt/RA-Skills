---
name: clash-controller
description: 管理Clash/mihomo代理环境，支持安装、启停代理、订阅管理、Web面板操作、Tun模式配置、升级内核等常用功能。触发场景：用户提到clash、mihomo、代理、clashctl、clashon、clashoff、clashui、订阅更新等关键词时使用。
---

# Clash Controller Skill
## 核心功能
支持Clash/mihomo代理全生命周期管理，适配`nelvko/clash-for-linux-install`一键安装脚本的所有功能。

## 环境前置说明
当前环境Clash命令通过自定义脚本加载，非登录shell执行前需先初始化环境：
```bash
# 加载Clash命令环境（必须先执行）
source /home/kklldog/clashctl/scripts/cmd/clashctl.sh
# 或使用交互式shell执行命令
bash -i -c "clashsub ls"
```
用户SSH登录时会自动加载`.bashrc`里的配置，可直接使用命令。

## 常用操作指南
### 1. 安装Clash
```bash
git clone --branch master --depth 1 https://gh-proxy.org/https://github.com/nelvko/clash-for-linux-install.git \
  && cd clash-for-linux-install \
  && bash install.sh
```
默认带gh-proxy加速，如失效可更换为其他github加速地址。

### 2. 代理启停
- 开启代理：`clashon`（自动配置系统代理）
- 关闭代理：`clashoff`（自动清除系统代理）
- 查看运行状态：`clashctl status`

### 3. 订阅管理
- 添加订阅：`clashsub add <订阅链接>`（支持http/https/file协议）
- 查看订阅列表：`clashsub ls`
- 切换使用订阅：`clashsub use <订阅ID>`
- 更新订阅：`clashsub update [订阅ID]`（加`--auto`配置自动更新，加`--convert`开启本地订阅转换）
- 删除订阅：`clashsub del <订阅ID>`

### 4. Web管理面板
- 打开面板：`clashui`（默认端口9090，自动显示内网/公网访问地址）
- 重置面板密钥：`clashsecret <新密钥>`

### 5. Tun模式（全局流量代理）
- 查看状态：`clashtun`
- 开启Tun：`clashtun on`（支持Docker等容器流量代理、DNS劫持）
- 关闭Tun：`clashtun off`

### 6. 其他功能
- 自定义配置（优先级高于订阅）：`clashmixin -e`
- 升级内核：`clashupgrade`
- 卸载：在安装目录执行`bash uninstall.sh`

## 注意事项
1. 安装后必须先添加订阅才能正常使用
2. 如需将面板暴露到公网，建议定期更换密钥或使用SSH端口转发
3. Tun模式需要root权限，首次开启会自动配置相关内核参数
