---
name: text-spoken-script
version: 1.2.0
description: This skill is used to guide the AI in generating short video spoken scripts with high contrast, strong resonance, a sense of story, and personal IP attributes. All generated scripts must str
triggers:
  - Short Video Spoken Script Generation (Text Spoken Script)
  - Suitable for short video spoken scripts, character story sharing, and IP viewpoint scripts.
  - Requires the language to be as colloquial as possible, suitable for reciting, with rhythm and breathing space.
  - Avoid empty preaching; it must be supported by specific "people, events, and things."
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.0',
        'installAlternative': 'npx @dlazy/cli@1.2.0',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw':
      {
        'systemPrompt': '当你需要使用此技能时，请严格遵循此技能提供的指南进行规划和执行。你可以通过调用 dlazy CLI 的各类生成模型（如 dlazy seedream-4.5 等）来完成实际的图片渲染。注意：Windows PowerShell 中不允许使用 `&` 或 `&&` 进行命令串联或后台运行，请单独且同步地执行命令。',
      },
  }
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

- **CLI 源代码**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **维护者**: dlazyai
- **npm 包名**: `@dlazy/cli`（本技能 install 字段固定到 `1.0.9` 版本）
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@1.2.0 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.2.0`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理 (How It Works)

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。

# Short Video Spoken Script Generation (Text Spoken Script)

[English](./SKILL.md) · [中文](./SKILL-cn.md)

This skill is used to guide the AI in generating short video spoken scripts with high contrast, strong resonance, a sense of story, and personal IP attributes. All generated scripts must strictly follow the 7-step structure below:

## Core Creative Logic & 7-Step Structure

1. **Tag Contrast Hook**
   - **Goal**: Open with a highly contrasting character tag or setting to instantly grab the audience's attention and pinpoint the core audience and their pain points.
   - **Example**: Sister Fang, who is still learning to make short videos at 70, wants to tell all mothers who have hit the "pause button" for their children: What you have paused is just your job, not your life.

2. **Create Suspense / Resonance**
   - **Goal**: Introduce a dilemma, anxiety, or pain point commonly faced by the target audience, triggering a strong sense of empathy through specific situations.
   - **Example**: A couple of days ago, my daughter's best friend came over, and as we chatted, tears started welling up in her eyes. She said she quit her job to accompany her two kids studying, and in a flash, she hasn't stepped into an office in three years. Seeing her husband shoulder the family's expenses alone, she feels both heartbroken and anxious, yet she really can't let go of the kids.

3. **Unfold the Story (Visual Imagery)**
   - **Goal**: Tell a specific event using detailed, visual language to portray the character's emotions (such as powerlessness, anxiety, unwillingness), making the audience feel as if they are there.
   - **Example**: She rubbed her hands and told me: "Aunt Fang, I feel like I'm about to be eliminated by society. Besides cooking and cleaning, I don't know anything anymore." In that look, there was anxiety, unwillingness, and a deep sense of powerlessness. I understand this feeling all too well.

4. **Deliver Core Viewpoint / Counter-Intuition**
   - **Goal**: Provide a core viewpoint that breaks conventional thinking, hitting the essence of the pain point and offering an enlightening conclusion.
   - **Example**: I told her, "Child, remember one sentence: Society never eliminates those who don't work, but those who don't learn."

5. **Deepen Story & Viewpoint (Combine Experience)**
   - **Goal**: Further demonstrate the viewpoint by combining the speaker's own real experiences (e.g., learning across ages, overcoming difficulties). Propose actionable micro-actions so the audience feels "I can do this too."
   - **Example**:
     - Right now, managing your family and children well is your most important "project" at this stage. But within this project, you must leave a "learning port" for yourself. It's not about immediately getting a certificate, but not letting your curiosity die out or your learning ability rust.
     - When I was 50, I decided to work in Beijing. In the guesthouse, whenever I had free time, I copied English words and learned to use the latest management system at the time. Many people laughed at me: "What's the use of learning this at your age?" I didn't care. I just felt that learning a little makes me a little newer. Later, these "useless" things became my confidence in managing my first hotel.
     - Now at 70, I'm still learning video editing and how to read backend data. Is it hard? Really hard. But the act of learning itself is telling the world: I'm still in the game, and I can still keep up.
     - When you pick up and drop off your kids every day, can you listen to an industry podcast? While doing housework, can you learn something interesting online? Even if you only invest half an hour a day, this half hour is charging you for your future "reboot." Your value lies not in whether you are on duty today, but in whether you still have the ability to be on duty tomorrow.

6. **Summarize and Elevate, Link Persona**
   - **Goal**: Elevate the topic, returning to personal growth or a grander theme of life, while strengthening the speaker's personal IP image (e.g., a constantly growing guide).
   - **Example**: A woman's roles are multiple, and sometimes trade-offs have to be made. This period of being a full-time homemaker is not a "break" in your career; it might precisely be a "gas station" for you to settle, observe, and accumulate power. Use learning to maintain your connection with the world, and your anxiety will turn into a clear path.

7. **Punchline Ending**
   - **Goal**: Conclude with a refined, powerful, philosophical, and highly spreadable punchline to leave a deep impression.
   - **Example**: The identity of a mother gives us a responsibility of love, not an excuse to stop growing. As long as you are still learning, the road will keep extending forward. The era cannot eliminate those who are always prepared.

## Applicable Scenarios and Limitations

- Suitable for short video spoken scripts, character story sharing, and IP viewpoint scripts.
- Requires the language to be as colloquial as possible, suitable for reciting, with rhythm and breathing space.
- Avoid empty preaching; it must be supported by specific "people, events, and things."

## Final Output Requirements

When the user invokes this skill and provides basic persona, pain points, or topics, please **directly output** the script content conforming to the 7-step structure above. Each step can serve as a paragraph (and during generation, keep or remove the step numbers depending on the user's request. If unspecified, output directly as a complete, well-paragraphed script).

## Next Step Suggestions

Call the `text-storyboard-script` skill to generate a storyboard script.

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
