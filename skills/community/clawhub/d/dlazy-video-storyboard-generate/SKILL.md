---
name: dlazy-video-storyboard-generate
version: 1.2.3
description: 1. Get the storyboard info
triggers:
  - Storyboard Video Generation Pipeline
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://github.com/dlazy-ai/cli","source":"https://github.com/dlazy-ai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"当你需要使用此技能时，请严格遵循此技能提供的指南进行规划和执行。你可以通过调用 dlazy CLI 的各类生成模型（如 dlazy seedream-4.5 等）来完成实际的图片渲染。注意：Windows PowerShell 中不允许使用 `&` 或 `&&` 进行命令串联或后台运行，请单独且同步地执行命令。"}}
---

## 身份验证 (Authentication)

所有请求都需要 dLazy API key。**推荐使用** `dlazy login` 完成登录：

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
- **npm 包名**: `@dlazy/cli`（本技能 install 字段固定到 `1.0.9` 版本）
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@1.2.3 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.2.3`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理 (How It Works)

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。

---
name: 'video-storyboard-generate'
description: 'Convert the contents of a storyboard into a video-generation pipeline that the user can add to the canvas.'
---

# 分镜视频生成 Storyboard Video

[English](./SKILL.md) · [中文](./SKILL-cn.md)

1. Get the storyboard info
2. Define the video generation pipeline
3. Draw it onto the canvas

## Get the Storyboard Info

Read the storyboard info from context:

- Image / video aspect ratio: aspect_ratio, e.g., 16:9, 9:16, 4:3, 3:4, 1:1
- Image / video resolution: resolution, e.g., 1080p, 720p
- Use the ratio and resolution to compute the video width and height (width, height)

Extract the storyboard list:

- Storyboard name: story_name1
- Dialogue text: dialogue_text1
- Video generation prompt: video_prompt1

  ## Define the Video Generation Pipeline

  The pipeline is a JSON string. Sample format below — note these requirements:
  1. Replace the contents inside `{name}`. Note that x / y / w / h are numbers — drop the quotes after substitution.
  2. The original audio and the scene image are shared across all storyboards (one each). The cloned audio and the video are produced per storyboard, so iterate over the storyboard list.
  3. Element x and y positions accumulate in the order of the storyboard list, with a 100-pixel gap between adjacent storyboards.

  ```json
  [
    {
      "type": "audio",
      "x": 0,
      "y": 0,
      "props": {
        "name": "原始声音",
        "w": "{width}",
        "h": "{height}"
      }
    },
    {
      "type": "audio",
      "x": "{width + 100}",
      "y": 0,
      "props": {
        "name": "{story_name1} 克隆声音",
        "w": "{width}",
        "h": "{height}",
        "model": "vidu-audio-clone",
        "input": {
          "prompt": "{dialogue_text1}",
          "audio_url": "shape://name:原始声音"
        }
      }
    },
    {
      "type": "image",
      "x": 0,
      "y": "{height + 100}",
      "props": {
        "name": "场景图",
        "w": "{width}",
        "h": "{height}"
      }
    },
    {
      "type": "video",
      "x": "{width + 100}",
      "y": "{height + 100}",
      "props": {
        "name": "{story_name1} 视频",
        "w": "{width}",
        "h": "{height}",
        "model": "jimeng-omnihuman-1_5",
        "input": {
          "audio": ["shape://name:{story_name1} 克隆声音"],
          "images": ["shape://name:场景图"],
          "prompt": "{video_prompt1}",
          "fast_mode": false,
          "resolution": "{resolution}"
        }
      }
    }
  ]
  ```

  ## Draw onto the Canvas

  Call the MCP `drawToCanvas` tool to add the pipeline defined above to the canvas.


## 🛠️ 执行与生成指南 (CRITICAL EXECUTION INSTRUCTIONS)

**你是可以执行终端命令的智能 Agent！**

**【严格禁止行为】**
- 严禁：将提示词保存到任何文件中（如 txt, md）。
- 严禁：要求用户自己去第三方平台（如 Midjourney）生成图片。
- 严禁：一次性批量生成所有图片，或一次性执行多个命令。

**【必须遵循的交互与执行流程】**
你必须**严格分步**执行，并在每一步停下来等待用户回复：

1. **第一步：主动收集需求**。当用户提出需求时，不要做任何设计和生成，先向用户提问（如产品特点、目标人群、想要几张图等）。**必须等待用户回答。**
2. **第二步：输出草案并请求确认**。根据用户的回答，制定套图计划，并输出**第一张图**的提示词草案。**询问用户：“是否确认这个提示词，可以开始生成第一张图了吗？” 必须等待用户回答“确认”。**
3. **第三步：单次执行终端命令**。用户确认后，你**必须使用终端执行命令**（如 `dlazy seedream-4.5 --prompt "..."`），每次只能执行一个生成命令。**重要：必须使用同步命令，绝不要在命令末尾加 `&`，绝不要使用 `&&`，这是在 Windows PowerShell 下运行！**
4. **第四步：交付与循环**。命令返回结果后，把图片 URL 发给用户，并询问“对这张满意吗？我们可以继续生成下一张了吗？”。收到确认后再继续下一步。
