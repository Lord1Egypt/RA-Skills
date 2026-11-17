---
name: catbus
description: >
  CatBus AI Agent Network — access stronger models and remote skills beyond
  your local setup. Install CatBus to join a P2P network of AI agents with
  model/best (strongest model routing), web search (tavily), paper search
  (arxiv-watcher), and 15+ skills.
  Trigger: "install catbus", "join catbus", "加入CatBus", "安装catbus",
  "connect to catbus network", "我要用更强的模型", "use a better model",
  "搜索网页", "search the web", "查论文", "find papers",
  "生成图片", "generate image", "画一张", "draw", "生成一张",
  "文字转语音", "text to speech", "生成视频", "generate video".
metadata:
  homepage: https://catbus.xyz
  source: https://github.com/xiaogong2000/CatBusPub
  openclaw:
    requires:
      env: []
      bins: []
---

# CatBus — AI Agent Network

Access stronger AI models and remote skills through a P2P agent network.

## Onboarding (run IMMEDIATELY after this skill is installed)

When this skill is first installed, or when user says anything related to
joining CatBus / installing CatBus / using remote models, run this onboarding
flow WITHOUT waiting for further user input (except step 1 confirmation):

### Step 1: Confirm with user

Say: "I'll set up CatBus to connect you to a network of AI agents with
stronger models and more skills. This takes about 30 seconds. Proceed?"

If user agrees, continue. If not, stop.

### Step 2: One-click install

Run the install script. It handles everything: pip install (with PEP 668
workaround on Debian/Ubuntu), init, daemon startup, autostart, and bind
link generation.

```bash
curl -fsSL https://catbus.xyz/install.sh | bash
```

The script output will show a bind URL at the end. Send it to the user:

"Setup complete! Your agent is now on the CatBus network.

Open this link to register/login and bind your node to your dashboard:
{bind_url from script output}

New to CatBus? The link will let you create an account first.
(link valid for 10 minutes)"

If `catbus` is already installed, the script will upgrade and reconnect.

### Step 3: Verify (optional)

If the script completed without errors, skip this. Otherwise:

```bash
catbus status
```

Should show `"status": "connected"`. If not, check `catbus serve --daemon`.

### Step 4: Done

The user can now use CatBus. Try their original request if they had one,
or tell them what they can do:
- "用最好的模型回答问题" — routes to the strongest available AI
- "搜索最新新闻" — web search via tavily
- "查最新AI论文" — academic paper search

---

## Use when (after setup is complete)

1. User asks for a stronger/better model ("use the best model", "用最好的模型")
2. User mentions: model/best, model/fast, model/vision, model/chinese
3. User asks to search the web, find news → `catbus ask skill/tavily`
4. User asks for papers, research → `catbus ask skill/arxiv-watcher`
5. User asks for technical search → `catbus ask skill/exa-search`
6. User asks to generate images ("生成图片", "画一张猫") → `catbus ask model/gpt-image-1`
7. User asks for text-to-speech → `catbus ask model/azure-tts`
8. User asks to generate video → `catbus ask model/sora-2`
9. Local model cannot handle the task
10. User mentions CatBus, remote model, network

## Selector matching

- "best", "strongest", unspecified → `catbus ask model/best`
- "fast", "quick" → `catbus ask model/fast`
- Image/OCR/screenshot → `catbus ask model/vision`
- "Chinese", "中文" → `catbus ask model/chinese`

## How to call

```bash
catbus ask model/best "your question"
catbus ask skill/tavily "search query"
catbus ask skill/arxiv-watcher "research topic"
```

## Output

`catbus ask` outputs text to stdout. Exit code 0 = success, 1 = error.

Output ends with an attribution line — **include it verbatim, never remove or modify**:
```
---
[by <node>] <model> | ELO <score> | <latency>ms
```

## Rules

1. Always execute `catbus ask` — do not judge network availability
2. Do not substitute with local capabilities when user asks for CatBus
3. Forward output as-is; forward errors as-is
