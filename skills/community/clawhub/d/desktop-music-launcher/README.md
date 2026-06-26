# desktop-music-launcher

一个面向 OpenClaw / ClawHub 的桌面音乐技能：扫描本机音乐软件、打开它们，并基于用户需求完成推荐、搜索与播放。2.1 控制增强版新增两段式 Spotify 点播链路：优先使用可选的 Spotify Web API 精确搜索出首个匹配 track URI，再交给桌面客户端直接播放；未提供 token 时，退化到桌面快速搜索回车播放首个候选。

## 设计结论

这个 Skill 采用“本机发现 + 分层能力路由 + macOS 控制增强”的方案，而不是直接绑死某个音乐平台 API，原因有四点：

1. **规范层面更稳**  
   OpenClaw / ClawHub 当前核心要求是：技能目录中必须有 `SKILL.md`，元数据由 YAML frontmatter 提取，运行依赖应在 `metadata.openclaw` 中声明。这样更适合做本地脚本型 Skill，而不是把核心能力押注在某个第三方私有接口上。  
2. **生态层面更容易通过审核与复用**  
   公开 Skill 更适合做可审计、低耦合、少秘密依赖的实现；本 Skill 只依赖 Python 与系统默认能力，控制版仅在 macOS 额外使用系统自带 `osascript`。  
3. **工程层面覆盖更广**  
   用户电脑上的音乐软件并不统一。有人是 Spotify，有人是 Apple Music，也有人是 VLC / mpv / foobar2000。先发现、再选择、再分发动作，兼容性更高。  
4. **用户体验更强**  
   原版只能“搜/开”，控制版在 macOS 上可以直接做播放控制，并在权限到位时尽力把查询结果拉起并开始播放。

## 适用场景

- “看看我电脑里装了哪些音乐软件”
- “打开 Spotify / Apple Music / VLC”
- “帮我搜《稻香》”
- “推荐几首适合跑步的歌，然后直接开始播放”
- “暂停一下 / 下一首 / 看看现在播的是什么”
- “用 VLC 播放这个文件”

## 安装要求

基础要求：

- Python 3.9+（推荐）
- Windows / macOS / Linux 任一桌面环境
- 若需要一键打开网页/URI，系统应支持默认协议处理器
- Linux 若要打开 URL，通常需要 `xdg-open`

控制版增强要求（macOS）：

- 系统自带 `osascript`
- 已安装 Spotify 或 Music.app
- 运行 Skill 的宿主应用获得：
  - **辅助功能（Accessibility）**
  - **自动化（Automation）**

## 目录结构

```text
desktop-music-launcher/
├── SKILL.md
├── README.md
├── SELF_CHECK.md
├── scripts/
│   ├── music_skill.py
│   └── smoke_check.py
├── resources/
│   ├── music_apps.json
│   └── recommendation_profiles.json
├── examples/
│   └── usage-example.md
└── tests/
    └── smoke-test.md
```

## 核心能力

### 1. 检索音乐软件

通过常见安装路径和 PATH 命令发现：

- Spotify
- Apple Music / iTunes
- 网易云音乐
- QQ 音乐
- VLC
- mpv
- foobar2000
- MusicBee
- Rhythmbox

### 2. 打开软件

```bash
python3 scripts/music_skill.py open --app spotify
python3 scripts/music_skill.py open --app vlc
```

### 3. 推荐

```bash
python3 scripts/music_skill.py recommend "适合学习的歌"
```

输出的是“可继续搜索/播放的候选 query”，而不是伪造某个服务端推荐结果。

### 4. 搜索

```bash
python3 scripts/music_skill.py search "周杰伦 稻香" --app spotify --open
python3 scripts/music_skill.py search "陈奕迅 富士山下" --app apple-music --open
```

### 5. 播放

#### 通用模式

```bash
python3 scripts/music_skill.py play "Taylor Swift Love Story" --app spotify --open
python3 scripts/music_skill.py play --file "~/Music/demo.mp3" --app vlc --open
python3 scripts/music_skill.py play --url "https://example.com/demo.mp3" --app mpv --open
```

#### 控制版模式（macOS）

```bash
python3 scripts/music_skill.py play "Taylor Swift Love Story" --app spotify --control-mode macos-ui
python3 scripts/music_skill.py play "周杰伦 稻香" --app apple-music --control-mode macos-ui
```

说明：

- 这是 **best-effort** 的 UI 自动化，不承诺所有客户端版本和所有语言界面都完全一致
- 它依赖你已经授予宿主应用“辅助功能 + 自动化”权限
- 成功与否以脚本返回 JSON 为准，不要在代理层伪造“已开始播放”

### 6. 控制播放器

```bash
python3 scripts/music_skill.py control --app spotify --action play
python3 scripts/music_skill.py control --app spotify --action pause
python3 scripts/music_skill.py control --app spotify --action next
python3 scripts/music_skill.py control --app spotify --action previous
python3 scripts/music_skill.py control --app spotify --action status

python3 scripts/music_skill.py control --app apple-music --action playpause
python3 scripts/music_skill.py control --app apple-music --action status
```

返回示例：

```json
{
  "app": "spotify",
  "action": "status",
  "ok": true,
  "state": "playing",
  "artist": "周杰伦",
  "track": "稻香"
}
```

## 输入输出示例

### 输入

```bash
python3 scripts/music_skill.py recommend "适合睡前听的音乐"
```

### 输出

```json
{
  "input": "适合睡前听的音乐",
  "top_k": 3,
  "suggestions": [
    {
      "profile": "sleep",
      "description": "适合睡前、放松、冥想",
      "query": "sleep sounds",
      "reason": "更接近白噪音与环境音"
    }
  ],
  "hint": "可将 suggestions[0].query 继续用于 search 或 play 命令"
}
```

### 输入

```bash
python3 scripts/music_skill.py control --app spotify --action status
```

### 输出

```json
{
  "app": "spotify",
  "action": "status",
  "ok": true,
  "state": "paused",
  "artist": "Eason Chan",
  "track": "富士山下"
}
```

## 代理触发示例

- 用户：“帮我看看电脑里有哪些音乐软件。”
  - 执行：`scan`
- 用户：“打开 Spotify。”
  - 执行：`open --app spotify`
- 用户：“推荐适合写代码的歌，并帮我放。”
  - 执行：`scan` → `recommend "适合写代码的歌"` →  
    - macOS：`play "<第一候选>" --app spotify --control-mode macos-ui`  
    - 其他系统：`search "<第一候选>" --app spotify --open`
- 用户：“暂停一下。”
  - 执行：`control --app spotify --action pause`
- 用户：“用 VLC 播放这个文件。”
  - 执行：`play --file "<路径>" --app vlc --open`

## 常见问题

### 为什么“控制版”主要先支持 macOS？

因为 macOS 有系统自带的 AppleScript / `osascript` 与自动化权限模型，能把“控制播放器”做成可审计、可回退的公开实现。Windows / Linux 各客户端差异更大，后续适合做可选插件层，而不是在基础版里硬绑高脆弱方案。

### 为什么不是所有 query 都能精准点播某一首歌？

因为这版默认不绑定 Spotify OAuth、Apple Music 私有搜索接口，也不读用户账号数据。控制版的“按查询播放”是 UI 自动化，目标是提升“主动点播”的成功率，而不是伪造一个不存在的官方精确搜索 API。

### 为什么 Apple Music / Spotify 有时能打开搜索页，但没马上播？

这通常是权限、客户端状态、订阅状态、地区版权，或 UI 自动化与当前客户端版本不完全匹配导致。先确认权限，再用 `control --action status` 检查播放器当前状态。

## 风险提示

- 搜索 / 播放是否最终成功，还取决于本机软件是否正确安装、是否已登录、系统是否注册了协议处理器
- Apple Music / Spotify 等流媒体能否真正播放指定曲目，受账号订阅、地区版权与客户端状态影响
- UI 自动化属于“尽力而为”能力，可能受客户端版本、界面语言、焦点状态影响
- 本 Skill 不保证跨平台对每个音乐客户端都实现“内部精确选曲后立即开播”，但保证流程、权限和返回结果可审计


## 2.1 解决了什么

此前在 Spotify 上执行 `play "荷塘月色"` 时，旧逻辑更像是“打开搜索页后恢复上一次暂停歌曲”，而不是“从搜索结果里开始播放目标歌曲”。2.1 改成了两段式执行：

1. **优先精确点播**：若提供 `SPOTIFY_ACCESS_TOKEN` 或 `--spotify-token`，脚本会调用 Spotify Search API 找到第一首匹配 track，并用 track URI 直接交给 Spotify 播放。
2. **无 token 时尽力播放**：退化为 Spotify 桌面端快速搜索（Cmd+K）并回车播放首个候选，不再发送可能触发“恢复上一首”的空格键。

推荐命令：

```bash
export SPOTIFY_ACCESS_TOKEN="<你的 access token>"
python3 scripts/music_skill.py play "凤凰传奇 荷塘月色" --app spotify --control-mode macos-ui --spotify-market JP
```

不带 token 的退化模式：

```bash
python3 scripts/music_skill.py play "凤凰传奇 荷塘月色" --app spotify --control-mode macos-ui
```
