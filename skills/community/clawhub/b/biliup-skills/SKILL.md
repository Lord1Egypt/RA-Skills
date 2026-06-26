---
name: biliup-skills
description: 使用命令行工具 biliup（Python 版官方 CLI，非 biliup-rs）向 B 站（bilibili）投稿视频。触发场景：用户说"投稿 B 站"、"上传到 B 站"、"发 B 站"、"bilibili 投稿"、"B 站发视频"、"上传视频到 bilibili"等相关关键字。功能：(1) 自动检测并通过 pip 安装 biliup，(2) 浏览器扫码登录并发送二维码图片给用户，(3) 收集视频信息后执行投稿，(4) 返回投稿结果。
---

# biliup-skills — B 站命令行投稿

使用 [biliup](https://github.com/biliup/biliup)（Python 版官方 CLI，PyPI 包名 `biliup`）投稿 B 站视频。

> **与 biliup-rs 的区别**：本 skill 使用的是 Python 版 `biliup`（`pip install biliup`），
> 不是基于 Rust 的 `biliup-rs`。两者功能相似，但安装方式和命令参数不同。

## 关于登录凭据（cookies.json）

`biliup login` 完成后，会在工作目录生成 `cookies.json`，其中保存的是
**用户自己的 B 站登录凭据（access_token）**，仅用于后续上传视频到用户自己的账号，
不会上传至任何第三方服务器。请妥善保管该文件，不要分享或提交到 git。

## 核心配置

- **biliup 安装方式**: `pip install biliup`（PyPI 官方包）
- **biliup 路径**: `~/.local/bin/biliup`（pip --user 安装路径）或系统 PATH 中
- **登录凭据文件**: `{workspace}/cookies.json`（`biliup login` 保存到运行时当前目录）
- **脚本目录**: 相对于本 SKILL.md 的 `scripts/`

## ⚠️ 已知行为（实战校正）

1. **`biliup login` 不支持 `--cookie` 参数**：凭据固定保存到运行时的**当前工作目录** `cookies.json`。
   建议先 `cd` 到 workspace 根目录再执行。
2. **`biliup login` 必须使用 PTY**（`pty=true`），否则报 `IO error: not a terminal`。
3. **菜单导航偏移**：启动时光标在"短信登录"（第 2 项），`↓↓Enter` 实际选到"浏览器登录"（第 4 项）。
   使用浏览器登录模式，它会输出一个授权 URL，用 B 站 App 扫码授权即可。
4. **二维码发送**：拿到授权 URL 后，生成二维码图片发给用户，同时附文字链接作为备用。
5. **进程不能提前终止**：登录完成前 kill 进程会导致凭据未保存，需等进程自然退出（code 0）。

## 完整工作流

### Step 1：检查并安装 biliup

```bash
bash scripts/setup_biliup.sh
```

- 若已安装则跳过，输出当前版本
- 若未安装，通过 `pipx install biliup` 或 `pip install --user biliup` 安装 PyPI 官方包
- 无需手动下载二进制文件

### Step 2：登录（首次使用 / 凭据已过期）

判断是否需要登录：
- `{workspace}/cookies.json` 不存在，或
- 用户明确要求重新登录，或
- 上传时报认证错误（401/403）

**登录流程**（必须用 PTY，在 workspace 目录运行）：

```bash
cd {workspace} && biliup login
# exec with pty=true, timeout=180s, yieldMs=8000
```

进程启动后显示登录方式菜单，**发送 `↓↓Enter`** 选中"浏览器登录"，输出授权 URL：

```
https://passport.bilibili.com/x/passport-tv-login/h5/qrcode/auth?auth_code=xxxxxx
```

**生成二维码并发送给用户：**

```bash
python3 -c "import qrcode; qrcode.make('https://passport.bilibili.com/x/passport-tv-login/h5/qrcode/auth?auth_code=xxxxxx').save('/tmp/biliup_qr.png')"
```

先单独发一条图片消息，再发一条文字备用链接：

```
# 图片消息（单独一条）
MEDIA: /tmp/biliup_qr.png

# 文字备用（单独一条）
🅱 B站扫码登录链接（图片看不到时使用）：
https://passport.bilibili.com/x/passport-tv-login/h5/qrcode/auth?auth_code=xxxxxx
用 B站 App 扫码授权后，请稍等，我会自动检测登录结果～
```

然后 **poll 进程输出，最长等 120 秒**，等待进程退出码 0（登录成功）。

⚠️ 不要提前 kill 进程，否则凭据不会写入磁盘。

登录成功后凭据文件在：`{workspace}/cookies.json`

**也可使用辅助脚本（自动捕获 URL 并生成二维码）：**

```bash
python3 scripts/qr_login.py --cookie {workspace}/cookies.json --wait
# 脚本会输出二维码图片路径到 stdout，用于发送给用户
```

### Step 3：收集投稿信息

向用户收集以下信息（必填项优先，可选项若用户未提及则跳过）：

| 参数 | 必填 | 说明 |
|------|------|------|
| 视频文件路径 | ✅ | 本地路径，支持多个（多 P） |
| 标题 `--title` | ✅ | 视频标题，最长 80 字 |
| 分区 `--tid` | ✅ | 见 references/tid_list.md；默认 21（虚拟主播综合） |
| 标签 `--tag` | ✅ | 逗号分隔，至少 1 个 |
| 简介 `--desc` | 可选 | 视频简介 |
| 封面 `--cover` | 可选 | 本地图片路径或 URL |
| 是否原创 `--copyright` | 可选 | 1=自制（默认），2=转载 |
| 转载来源 `--source` | 转载时必填 | 原始来源说明 |

若用户一次性提供了所有信息，直接进入 Step 4，不要反复追问。

**视频文件处理**：
- 若用户通过 QQ 发送视频（CQ 码格式），从 `url=` 字段提取 URL，下载到本地再上传：
  ```bash
  curl -L -o /tmp/biliup_upload/<filename>.mp4 "<url>"
  ```
- 下载后用 `file` 命令确认是有效的 MP4 文件

### Step 4：执行投稿

```bash
biliup -u {workspace}/cookies.json upload \
    --title "视频标题" \
    --tid 21 \
    --tag "标签1,标签2" \
    /path/to/video.mp4
```

多 P 视频：在末尾追加多个文件路径。

**上传线路**（可选，若用户要求速度优化）：
`--line` 可选 `bda2`（默认）、`ws`、`qn`、`tx`、`txa`

运行投稿命令时：
- 告知用户"投稿中，请稍候..."
- 等待命令完成（timeout 300s）
- 解析输出中的 BV 号（`"bvid": "BVxxxxxxxxx"`）或错误信息

### Step 5：返回结果

成功时输出：
```
✅ 投稿成功！
BV 号：BVxxxxxxxxx
标题：xxx
可在哔哩哔哩个人主页查看审核进度～
```

失败时输出错误信息，常见问题：
- `401/403` → 登录凭据已过期，需重新登录（回到 Step 2）
- 文件不存在 → 检查视频路径
- 标题/标签违规 → 提示用户修改

## 注意事项

- biliup 是社区维护的 B 站上传工具（https://github.com/biliup/biliup）
- 通过 PyPI 官方包安装（`pip install biliup`），无需手动下载二进制
- cookies.json 保存用户自己的 B 站登录凭据，请妥善保管，不要分享或提交到 git
- 投稿后需等待 B 站审核，通常数小时内完成
- 分区 tid 参考：`references/tid_list.md`
