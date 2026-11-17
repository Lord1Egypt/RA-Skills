---
name: dlazy-picture-book
version: 1.3.5
description: "绘本生成、儿童绘本、图画书、睡前故事书、picture book、storybook——根据一个主题创作完整绘本：编写分页故事、用 dlazy gpt-image-2 逐页生成风格统一的插图、用 dlazy elevenlabs-music 生成匹配基调的背景音乐，最后组装成一个左图右文、可翻页、带背景音乐的独立 HTML 绘本。默认 10 页。当用户想做绘本 / 图画书 / 儿童故事书 / 睡前故事，或说“帮我做一本关于……的绘本”时使用。"
metadata:
  {
    'clawdbot':
      {
        'emoji': '📖',
        'requires': { 'bins': ['npm', 'npx', 'python3', 'curl'] },
        'install': 'npm install -g @dlazy/cli@1.2.3',
        'installAlternative': 'npx @dlazy/cli@1.2.3',
        'homepage': 'https://github.com/dlazy-ai/cli',
        'source': 'https://github.com/dlazy-ai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw':
      {
        'systemPrompt': '当你需要制作绘本时，请严格遵循此技能的工作流：先确认主题与分页故事，再用 dlazy gpt-image-2 逐页生成插图（首页确立角色与画风，后续页用首页作参考图保持一致），用 dlazy elevenlabs-music 生成背景音乐，最后用本技能自带的 scripts/build_book.py 把 book.json 组装成 index.html。注意：Windows PowerShell 中不允许用 `&` 或 `&&` 串联命令，请逐条同步执行；不要一次性批量生成所有图片。',
      },
  }
---

# 绘本生成 Picture Book

[English](./SKILL.md) · [中文](./SKILL-cn.md)

绘本生成、儿童绘本、图画书、睡前故事书、picture book、storybook——根据一个主题创作完整绘本：编写分页故事、用 dlazy gpt-image-2 逐页生成风格统一的插图、用 dlazy elevenlabs-music 生成匹配的背景音乐，最后组装成一个**左图右文、可翻页、带背景音乐的独立 HTML 绘本**。默认 10 页。

## 触发关键词

- 绘本 / 绘本生成
- 儿童绘本 / 图画书
- 睡前故事 / 故事书
- picture book / storybook
- 帮我做一本关于……的绘本

## 身份验证 (Authentication)

所有 dlazy 请求都需要 dLazy API key。**推荐使用** `dlazy login` 完成登录：

```bash
dlazy login
```

该命令使用设备码流程（远程终端也可用），登录成功后 **自动把 API key 写入本地 CLI 配置**，无需手动复制粘贴。

### 备选：手动设置 API Key

如果你已有 API key，也可以直接保存：

```bash
dlazy auth set YOUR_API_KEY
```

CLI 会把 key 保存在你的用户配置目录（macOS/Linux 上为 `~/.dlazy/config.json`，Windows 上为 `%USERPROFILE%\.dlazy\config.json`），文件权限仅限当前操作系统用户访问。你也可以用 `DLAZY_API_KEY` 环境变量按次传入。

### 手动获取 API Key

1. 登录或在 [dlazy.com](https://dlazy.com) 创建账号
2. 访问 [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. 复制 API Key 区域显示的密钥

每个 key 都属于你自己的 dLazy 组织，可在同一控制面板**随时轮换或吊销**。

## 关于与来源 (Provenance)

- **CLI 源代码**: [github.com/dlazy-ai/cli](https://github.com/dlazy-ai/cli)
- **维护者**: dlazyai
- **npm 包名**: `@dlazy/cli`
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@1.2.3 <command>
```

安装前建议先到 GitHub 仓库审阅源码。

## 工作原理 (How It Works)

绘本的**插图**由 `dlazy gpt-image-2` 生成、**背景音乐**由 `dlazy elevenlabs-music` 生成，二者都是 dLazy 托管 API 的轻量封装：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入的本地参考图会先上传到 dLazy 媒体存储（`files.dlazy.com`），生成结果 URL 也由 `files.dlazy.com` 托管。

**故事文本、分页编排、HTML 组装**都在本地完成——由你（Agent）编写故事、调用本技能自带的 `scripts/build_book.py` 把内容注入 `assets/template.html` 模版，产出一个自包含的 HTML。这是标准的 SaaS 调用模式，技能本身不越权访问网络或文件系统。

---

## 成品长什么样

一个可以直接双击打开的文件夹，`index.html` 就是绘本：

```
<绘本标题>/
├── index.html        ← 最终绘本（左图右文、翻页、背景音乐）
├── book.json         ← 内容数据（标题、每页图文、音乐）
├── images/           ← cover.png, page-01.png … page-10.png
└── music/            ← bgm.mp3
```

阅读体验：**封面**（大图 + 标题 + “开始阅读”）→ **内页**（左边 3:4 插图，右边故事文字，可用方向键 / 点击左右 / 底部圆点翻页）→ **尾页**。右上角有背景音乐开关。手机上自动变为上图下文。

图片与音乐都用**相对路径**引用，所以整个文件夹拷走即可分享，无需联网。

---

## 工作流

绘本是「故事 + 画面 + 声音」的整体，质量取决于三者是否协调。按下面的顺序做，每一步都为下一步打好基础。

### 第 0 步：确认创作简报

动手前先和用户对齐这几件事（用户没说的，用合理默认值并说明，不要追问到底）：

- **主题 / 故事内核**：讲什么？想传递什么（勇气、分享、友谊…）？
- **页数**：默认 **10 页**，用户可指定。
- **受众年龄**：默认 3–6 岁。决定文字难度与句子长度。
- **画风**：默认温暖治愈的水彩儿童绘本风。也可以是扁平插画、蜡笔、3D 皮克斯风等。
- **主角**：外形要具体（如“一只戴红围巾的小狐狸”），因为它要在每一页保持一致。

### 第 1 步：编写分页故事，落到 book.json

先把**整本书的文字**写完，再去生成图。这样画面才有统一的叙事线索。

- 一个完整的故事弧：**开场（介绍主角与世界）→ 出发 / 愿望 → 遇到困难 → 转折 → 温暖的结局**。10 页就按这个节奏铺开。
- 每页 **1–3 句**，口语化、有画面感，适合朗读。低龄段句子更短。
- 同时为每页想好**画面描述**（这一页画什么），下一步生成插图要用。

把结果先写成 `book.json`（图片 / 音乐路径先占位，生成后已经是对的路径）：

```json
{
  "title": "小狐狸的星星灯",
  "subtitle": "一个关于分享的温暖故事",
  "cover_image": "images/cover.png",
  "music": "music/bgm.mp3",
  "pages": [
    { "image": "images/page-01.png", "text": "森林深处住着一只戴红围巾的小狐狸……" },
    { "image": "images/page-02.png", "text": "……" }
  ]
}
```

### 第 2 步：逐页生成插图（保持角色与画风一致）

一致性是绘本最容易翻车的地方——同一只小狐狸不能每页长得都不一样。做法是**用首页当“风格锚点”**：

1. **先生成第 1 页**，提示词里把角色外形、画风、色调、构图都写足、写细。这张确立整本书的视觉基调。

   ```bash
   dlazy gpt-image-2 --quality low --size 1024x1536 \
     --prompt "儿童绘本插画，温暖水彩风格，3:4 竖构图。一只戴红色围巾的橙色小狐狸趴在窗台上望着窗外圆圆的月亮，夜晚，柔和的暖色灯光，治愈童真的氛围，画面留白干净。"
   ```

2. **后续每一页都把第 1 页作为参考图**传给 `--images`，让主角和画风延续，只改场景：

   ```bash
   dlazy gpt-image-2 --quality low --size 1024x1536 \
     --images images/page-01.png \
     --prompt "同一只戴红围巾的橙色小狐狸，同样的水彩绘本画风与色调。这一页：小狐狸背起小背包，踏着月光走进森林。3:4 竖构图。"
   ```

3. 命令返回后，结果 URL 在 `result.outputs[0].url`。**用 curl 下载到 `images/`**：

   ```bash
   curl -L -o images/page-01.png "<返回的 url>"
   ```

关于参数：`--quality low` 是低质量（快、省积分，绘本小图足够）；`--size 1024x1536` 是最接近 3:4 的小竖图（gpt-image-2 没有精确的 3:4 档，模版会按 3:4 裁切，视觉上正好）。

**封面**同理：用第 1 页作参考图，生成一张更有氛围感的主视觉存到 `images/cover.png`。

> **执行纪律（重要）**：一次只跑一个生成命令，等它返回、下载好，再跑下一个——不要一次性把 10 张图的命令一股脑并发或用 `&`/`&&` 串起来。这既是因为要拿上一张的结果当参考图，也因为在 Windows PowerShell 下 `&`/`&&` 会报错。

### 第 3 步：生成背景音乐

根据故事基调写一句音乐提示词，时长给足以覆盖阅读（睡前故事 60–90 秒即可，循环播放）：

```bash
dlazy elevenlabs-music --duration 75 \
  --prompt "温柔舒缓的儿童睡前音乐，轻柔的钢琴与八音盒，梦幻温暖，适合绘本朗读的背景，无人声。"
```

返回后同样 `curl` 下载到 `music/bgm.mp3`。

### 第 4 步：组装成 HTML

确认 `book.json` 里的路径和实际下载的文件对得上，然后运行本技能自带的构建脚本：

```bash
python3 <本技能目录>/scripts/build_book.py book.json -o index.html
```

脚本会把 `book.json` 注入 `assets/template.html`，生成自包含的 `index.html`。把 `index.html` 和 `images/`、`music/` 放在同一文件夹即可。

### 第 5 步：交付

告诉用户成品文件夹路径，说明双击 `index.html` 就能翻阅、右上角可开关背景音乐。附上封面图 URL 让用户先睹为快。

---

## 命令速查

**插图 · gpt-image-2**（完整帮助：`dlazy gpt-image-2 -h`）

| 参数 | 绘本用法 |
| --- | --- |
| `--prompt` | 画面描述（角色 + 场景 + 画风 + “3:4 竖构图”） |
| `--images` | 参考图（首页图路径），用于保持角色/画风一致，最多 5 张 |
| `--quality` | `low`（绘本小图够用，快且省积分） |
| `--size` | `1024x1536`（最接近 3:4 的小竖图） |

**背景音乐 · elevenlabs-music**（完整帮助：`dlazy elevenlabs-music -h`）

| 参数 | 绘本用法 |
| --- | --- |
| `--prompt` | 音乐氛围描述（乐器、情绪、“无人声”、适合朗读） |
| `--duration` | 时长（秒），睡前故事 60–90 即可，循环播放 |

生成结果统一在 `result.outputs[0].url`，用 `curl -L -o <本地路径> "<url>"` 下载。

## 错误处理

| Code | 错误类型                         | 示例信息                                                                                             |
| ---- | -------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 401  | 未授权 (API Key缺失或无效)       | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                          |
| 501  | 缺少必填参数                     | `error: required option '--prompt <prompt>' not specified`                                            |
| 502  | 本地文件读取失败                 | `Error: Image file not found: C:\path\to\your\file`                                                  |
| 503  | API 请求失败（余额不足）         | `ok: false, code: "insufficient_balance"`                                                            |
| 503  | API 请求失败（服务端错误）       | `HTTP status code error (500 server crash)`                                                          |
| 504  | 异步任务执行失败                 | `=== Generation Failed ===` / `{后端返回的具体失败原因，如提示词违反安全策略}`                        |

> **智能体关键指令**:
> 1. 如果返回 `code: "insufficient_balance"`（余额不足），必须明确告知用户积分不足，并引导前往充值：[https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. 如果返回 `code: "unauthorized"` 或提示缺少 API Key，必须告知用户前往 [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) 获取 API Key 并用 `dlazy auth set <key>` 保存，然后继续任务。
> 3. 若某张图违反安全策略被拒，改写该页提示词（去掉敏感/暴力/写实人物等描述）后重试，不要中断整本书。

## Tips

Visit https://dlazy.com for more information.
