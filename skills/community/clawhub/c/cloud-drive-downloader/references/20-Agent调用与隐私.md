# Agent 调用与隐私边界

## 适用方式

这个技能的稳定入口是同一个命令行脚本：

```bash
python3 <技能目录>/scripts/pan.py <command>
```

Codex 技能适配层、其他 agent、用户本机脚本都调用这一个入口；不需要为每个 agent 复制一份网盘协议代码，也不需要逐个安装各家官方客户端。

## 推荐 Agent 流程

1. 调用 `detect <url>` 识别网盘。
2. 调用 `get <url> --dry-run --json` 获取无凭据计划。
3. 如果 `missing` 或 `warnings` 要求登录、AList 路径或共享引擎，按提示操作，不编造下载成功。
4. 让用户在自己的本机终端完成 `login`、`secret set` 或官方 OAuth/扫码。
5. 再次 dry-run 通过后，去掉 `--dry-run` 实际下载。
6. 完成后只报告目录、文件数量、日志和失败项。

## 绝对不要做

- 不要在聊天、提示词、命令参数、日志或截图里要求用户粘贴账号密码、Cookie、Token、BDUSS。
- 不要把凭据写入技能目录、Git 仓库、iCloud、云盘、在线表格或第三方转换服务。
- 不要把 `secret` 命令替换成 `echo 密码 | ...` 后留在 shell 历史里；优先 `secret set` 的交互输入。
- 不要用多账号、IP 轮换、伪装客户端、篡改计时、验证码绕过等方式规避平台限制。
- 不要把“会员提速”描述成“破解限速”或“保证不限速”。

## 凭据落地位置

| 凭据 | 推荐位置 |
|---|---|
| WebDAV / AList 密码 | 系统凭据库，配置只写 `credential:engine.webdav` / `credential:engine.alist`（旧 `keychain:` 继续兼容） |
| 单网盘辅助密码 | 系统凭据库，配置只写 `credential:drive.<盘名>` |
| AList/rclone/BaiduPCS-Go 登录态 | 各自本机受保护配置目录 |
| 远程 NAS / 私有存储凭据 | 远程设备自己的系统凭据库或 rclone/AList 配置；禁止上传本机 config |
| 分享提取码 | 只传给本次 `get --pwd`，不作为账号凭据保存 |

## 系统凭据库命令

```bash
# 交互输入，不回显
python3 scripts/pan.py secret set engine.webdav

# agent 从受控 stdin 写入，不把密码放进 argv
printf '%s\n' "$SECRET" | python3 scripts/pan.py secret set engine.webdav --stdin

# 仅检查存在性，不打印密码
python3 scripts/pan.py secret check engine.webdav --json
python3 scripts/pan.py secret list --json

# 迁移旧配置明文
python3 scripts/pan.py secret migrate
```

## JSON 输出

`get --dry-run --json` 只输出：

- 识别的网盘与引擎；
- 目标目录；
- 打码后的命令计划；
- 是否使用 stdin 凭据；
- 缺失依赖和警告。

不会输出密码、Cookie、Token 或 `curl --config -` 的实际内容。

远程设备的 `remote list --json` 只返回协议、地址、远程目录和凭据引用，不返回远程密码。`remote get --dry-run --json` 的 SSH 命令会隐藏密码/凭据参数，但仍会保留分享链接和资源配置；不要把含敏感查询参数的私密链接交给不受信任的 agent。

## Windows

Windows 使用 `scripts\pan.ps1` 或 `scripts\pan.cmd`。凭据写入 Windows Credential Manager，配置文件位于 `%APPDATA%\pan-downloader\config.json`，日志位于 `%LOCALAPPDATA%\pan-downloader\logs\pan-downloader.log`。完整说明见 `references/22-Windows配置.md`。

## 会员与限速

账号等级只有在配置了可信 `tier_detector` 或用户明确记录 `account_tier` 时才升降并发。会员账号可能获得平台提供的更高速度，但会员权益以各平台官方规则为准。技能不承诺不限速，不绕过限速。
