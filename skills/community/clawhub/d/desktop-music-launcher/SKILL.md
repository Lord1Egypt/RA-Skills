---
name: desktop-music-launcher
description: 检索本机已安装音乐软件，启动它，并根据用户需求推荐、搜索或播放歌曲；在 macOS 上可用 AppleScript 控制 Spotify 和 Apple Music，并为 Spotify 增加可选的精确点播链路。
version: 2.1.0
allowed-tools: Bash Python Read
metadata:
  category: music
  tags:
    - music
    - desktop
    - spotify
    - apple-music
    - player
    - launcher
    - control
    - applescript
  provider: local-desktop
  openclaw:
    emoji: "🎵"
    os:
      - windows
      - macos
      - linux
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md
---

# desktop-music-launcher

## 何时使用

当用户想要：

- 检查电脑里装了哪些音乐软件或播放器
- 打开 Spotify / Apple Music / QQ 音乐 / 网易云音乐 / VLC / mpv 等
- 按歌名、歌手、专辑、情绪、场景搜索音乐
- 根据“适合学习 / 跑步 / 睡前 / 聚会 / 失恋”等需求推荐可立即搜索的音乐方向
- 在 macOS 上直接控制 Spotify / Apple Music 的播放、暂停、下一首、上一首、状态查询
- 在 macOS 上对 Spotify / Apple Music 执行“按需求尽力开始播放”的 UI 自动化

## 不做什么

- 不伪造“已经开始播放”的结果；必须以脚本返回结果为准
- 不调用未声明的私有 API、逆向接口或账号 Cookie
- 不越权扫描无关目录；只检查常见安装路径和 PATH 中的可执行文件
- 不自动登录任何音乐服务，也不读取用户账号密码
- 不下载盗版资源，不绕过版权或付费限制
- 不承诺所有客户端、所有版本、所有语言 UI 下都能 100% 精确点开第一首歌

## 运行方式

统一使用：

```bash
python3 scripts/music_skill.py <command> [args]
```

若系统只有 `python`，则改用：

```bash
python scripts/music_skill.py <command> [args]
```

## 命令总览

### 1) 扫描本机音乐软件

```bash
python3 scripts/music_skill.py scan
```

返回 JSON，包含当前系统、识别到的应用、是否安装、命中的路径/命令、支持的能力；在 macOS 上还会返回是否存在 `osascript`。

### 2) 打开软件

```bash
python3 scripts/music_skill.py open --app spotify
python3 scripts/music_skill.py open --app vlc
```

### 3) 搜索歌曲 / 歌手 / 专辑

```bash
python3 scripts/music_skill.py search "周杰伦 稻香"
python3 scripts/music_skill.py search "lofi beats" --app spotify --open
```

### 4) 播放

```bash
python3 scripts/music_skill.py play "Eason Chan 富士山下" --app spotify --control-mode macos-ui
python3 scripts/music_skill.py play "Taylor Swift Love Story" --app apple-music --control-mode macos-ui
python3 scripts/music_skill.py play --file "~/Music/demo.mp3" --app vlc --open
python3 scripts/music_skill.py play --url "https://example.com/demo.mp3" --app mpv --open
```

行为说明：

- `play <query>`：  
  - macOS + Spotify / Apple Music 时，默认优先尝试控制版的 UI 自动化  
  - 其他系统或不支持控制的客户端，则退化为 URI / 网页搜索
- `play --file`：把本地音频文件交给 VLC / mpv / foobar2000 / MusicBee 等播放器
- `play --url`：把网络音频 URL 交给支持 URL 播放的播放器

### 5) 控制播放器

```bash
python3 scripts/music_skill.py control --app spotify --action play
python3 scripts/music_skill.py control --app spotify --action pause
python3 scripts/music_skill.py control --app spotify --action next
python3 scripts/music_skill.py control --app spotify --action previous
python3 scripts/music_skill.py control --app spotify --action status

python3 scripts/music_skill.py control --app apple-music --action playpause
python3 scripts/music_skill.py control --app apple-music --action status
```

支持动作：

- `play`
- `pause`
- `playpause`
- `next`
- `previous`
- `status`

### 6) 推荐

```bash
python3 scripts/music_skill.py recommend "适合写代码的歌"
python3 scripts/music_skill.py recommend "跑步音乐" -k 5
```

## 推荐工作流

当用户说“帮我放点适合学习的歌”时，按下面顺序执行：

1. 先运行 `scan`
2. 选一个已安装且支持搜索/播放的应用；在 macOS 上优先 Spotify / Apple Music 控制版
3. 运行 `recommend "<用户需求>"`
4. 从结果里挑最合适的 `suggestions[0].query`
5. macOS 上优先运行 `play "<query>" --app spotify --control-mode macos-ui`
6. 如果控制失败，再退回 `search "<query>" --open`

## 结果解释

典型 JSON 字段：

- `app`: 选中的应用 ID
- `method`: `uri` / `web` / `play_file` / `play_url` / `macos_ui_automation`
- `target`: 即将打开的 URI、URL、文件路径或音频地址
- `open_result.ok`: 是否成功发起打开动作
- `supports`: 该软件支持的能力集合
- `best_effort`: 是否属于“尽力而为”的 UI 自动化
- `requires_permissions`: 控制版需要的系统权限

## 失败时怎么处理

- 没检测到音乐软件：建议用户先安装 Spotify、Apple Music、VLC 或 mpv
- macOS 控制失败：先检查“辅助功能”和“自动化”权限，再重试
- 目标软件不支持统一搜索入口：给出 query，让用户手动在应用里搜索
- 本地文件不存在：明确报错，不要猜测路径
- Linux 缺少 `xdg-open`：提示安装桌面打开器或改为手动复制 URL

## 权限说明

macOS 控制版依赖：

- `osascript`
- 运行该 Skill 的宿主应用已获 **辅助功能**
- 运行该 Skill 的宿主应用已获 **自动化**，允许控制 Spotify / Music

没有这些权限时，控制版会失败，但扫描、推荐、普通搜索仍可用。

## 安全边界

- 仅执行本地启动、打开 URI/URL、把用户明确提供的文件/URL交给播放器
- 在 macOS 上仅调用可审计的 AppleScript 控制公开桌面应用
- 不读取浏览器 Cookie、不抓包、不注入播放器进程
- 不使用 `curl | bash`、远程脚本直灌、Base64 混淆执行
- 所有外部入口都在脚本返回结果中可审计
