---
name: ai-content-creator
description: All-in-one AI content creation agent — write blog posts, social media, newsletters, scripts, and product copy. Generate images, video, and voiceovers. Research topics, extract web content, and produce multimedia from a single workflow via x402.
version: 1.0.0
homepage: https://github.com/plagtech/ai-content-creator-skill
metadata:
  openclaw:
    primaryEnv: RESEARCH_API_KEY
    envVars:
      - name: RESEARCH_API_KEY
        required: true
        description: API key or x402 subscription key for the gateway.
      - name: RESEARCH_GATEWAY_URL
        required: false
        description: Gateway URL. Defaults to https://gateway.spraay.app
    requires:
      bins:
        - curl
        - python3
---

# AI Content Creator

End-to-end content creation agent. Research a topic, write copy, generate images, create voiceovers, and produce video — all in one workflow. 14 endpoints spanning text generation, image generation, video, TTS, speech-to-text, web research, and content extraction. Each call is a real x402 micropayment.

## How to call endpoints

```bash
bash {baseDir}/scripts/create.sh METHOD ENDPOINT '{"key":"value"}'
```

## Content workflows

Follow these workflows depending on what the user needs. Each workflow chains multiple endpoints together for a polished final product.

### Blog Post / Article

1. **Research** the topic with `web_search` and `web_qna` to gather facts and angles
2. **Extract** full content from the best source URLs with `web_extract` for deeper context
3. **Write** the post with `text_inference` using the research as context — specify tone, length, and audience
4. **Generate** a header image with `image_generation` using a prompt that matches the article theme
5. Deliver the article with the header image

### Social Media Post

1. **Write** platform-specific copy with `text_inference` — specify platform (X, LinkedIn, Instagram), character limits, and hashtag style
2. **Generate** an eye-catching image with `image_generation` — square for Instagram, landscape for X/LinkedIn
3. For carousel posts, generate multiple images with different prompts
4. Deliver copy + image together, ready to post

### Newsletter / Email

1. **Research** trending topics with `web_search` for timely hooks
2. **Write** sections with `text_inference` — intro, body sections, CTA
3. **Generate** section illustrations with `image_generation`
4. Deliver the full newsletter draft with visuals

### Podcast / Audio Content

1. **Write** the script with `text_inference` — specify conversational tone, pacing cues, and segment breaks
2. **Generate** the audio narration with `text_to_speech` — choose voice and style
3. **Create** cover art with `image_generation`
4. Deliver script + audio + cover art

### Video Content

1. **Write** the video script with `text_inference` — include scene descriptions and timing
2. **Generate** a thumbnail with `image_generation`
3. **Create** a short video clip with `video_generation` for intros, B-roll, or social teasers
4. **Narrate** the script with `text_to_speech` for voiceover
5. Deliver script + thumbnail + video + voiceover

### Product Description / Landing Page

1. **Research** competitor products with `web_search` and `web_extract`
2. **Write** compelling product copy with `text_inference` — headlines, features, benefits, CTA
3. **Generate** product lifestyle images with `image_generation`
4. Deliver copy + images ready for the page

### Repurposing Content

1. **Transcribe** existing audio/video with `speech_to_text`
2. **Rewrite** the transcript into a blog post, social thread, or newsletter with `text_inference`
3. **Generate** fresh visuals with `image_generation`
4. One piece of content becomes five

## Available endpoints (14 tools)

### Writing & Text

**Text Inference** — $0.003–$0.10
Generate any written content — blog posts, social copy, scripts, emails, product descriptions. Supports 11 models, system prompts, temperature control.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/compute/text-inference '{"model":"llama-3.1-70b","prompt":"Write a LinkedIn post about AI agents in supply chain management. Professional tone, under 300 words.","max_tokens":500}'
```

**Chat Completions** — $0.04
Multi-turn creative brainstorming. Use for ideation, outlining, and iterating on drafts.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/chat/completions '{"messages":[{"role":"system","content":"You are a creative director at a content agency."},{"role":"user","content":"Give me 5 angles for a blog post about remote work productivity."}]}'
```

### Visual Content

**Image Generation** — $0.02–$0.08
AI image generation via FLUX and SDXL. Blog headers, social media graphics, product shots, thumbnails, cover art.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/compute/image-generation '{"prompt":"minimalist flat illustration of a person working at a laptop with floating holographic screens, soft blue and purple gradient background","model":"flux"}'
```

**Bittensor Image Gen** — $0.05
Alternative image generation via decentralized Bittensor network. Different aesthetic from FLUX/SDXL.
```bash
bash {baseDir}/scripts/create.sh POST /bittensor/v1/images/generations '{"prompt":"abstract geometric pattern for newsletter header, corporate blue and white"}'
```

### Audio & Video

**Text to Speech** — $0.03–$0.05
Convert scripts to natural voiceovers. Multiple voices available. Use for podcasts, video narration, audio articles.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/compute/text-to-speech '{"text":"Welcome to this week's deep dive into the world of AI agents and how they're reshaping content creation.","voice":"alloy"}'
```

**Speech to Text** — $0.02
Transcribe audio or video to text. Use for repurposing podcasts, interviews, or meetings into written content.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/compute/speech-to-text '{"audio_url":"https://example.com/podcast-episode.mp3"}'
```

**Video Generation** — $0.40–$0.50
AI video from text prompts. Short clips for social teasers, intros, B-roll, and product demos.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/compute/video-generation '{"prompt":"aerial drone shot of a modern office building at golden hour, cinematic","duration":5}'
```

### Research & Inspiration

**Web Search** — $0.02
Search the web for trending topics, competitor content, statistics, and angles.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/search/web '{"query":"AI content creation trends 2026"}'
```

**Web Extract** — $0.02
Pull clean readable content from any URL. Use to analyze competitor articles, extract quotes, or gather source material.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/search/extract '{"urls":["https://example.com/competitor-blog-post"]}'
```

**Web Q&A** — $0.03
Quick factual answers from the live web. Use for fact-checking claims before publishing.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/search/qna '{"query":"What percentage of marketers use AI for content creation in 2026?"}'
```

### Utility

**Embeddings** — $0.005
Generate text embeddings for finding similar content, clustering topics, or building recommendation systems.
```bash
bash {baseDir}/scripts/create.sh POST /api/v1/compute/embeddings '{"text":"AI-powered content creation workflow automation"}'
```

**Bittensor Chat** — $0.03
Alternative AI for a different creative voice. Useful for A/B testing copy or getting a second perspective.
```bash
bash {baseDir}/scripts/create.sh POST /bittensor/v1/chat/completions '{"messages":[{"role":"user","content":"Rewrite this headline to be more engaging: AI Tools Save Time"}]}'
```

**Available Models** — $0.001
List available AI models and their strengths for choosing the right one per task.
```bash
bash {baseDir}/scripts/create.sh GET /api/v1/models '{}'
```

**GPU Models** — FREE
List available GPU model shortcuts including image and video models.
```bash
bash {baseDir}/scripts/create.sh GET /api/v1/gpu/models '{}'
```

## Cost estimates by workflow

| Workflow | Typical Calls | Estimated Cost |
|----------|--------------|----------------|
| Blog post + header image | 4-5 | $0.07–$0.15 |
| Social media post + image | 2 | $0.03–$0.12 |
| Newsletter (3 sections + images) | 6-8 | $0.10–$0.25 |
| Podcast script + audio + cover | 3 | $0.06–$0.18 |
| Video script + thumbnail + clip + VO | 4 | $0.48–$0.70 |
| Product description + images | 4-5 | $0.07–$0.20 |
| Content repurpose (audio → 3 formats) | 4-5 | $0.07–$0.18 |

## Tips for best results

- **Be specific with prompts** — "Write a 500-word blog post for a B2B SaaS audience about reducing churn, conversational tone, include 3 actionable tips" beats "Write about churn."
- **Chain endpoints** — research first, then write. Content grounded in real data performs better.
- **Use different models** — `llama-3.1-70b` for long-form, `llama-3.1-8b` for quick social copy, Bittensor for a different creative voice.
- **Generate multiple images** — create 2-3 variations and let the user pick.
- **Specify dimensions** — square for Instagram, 16:9 for YouTube thumbnails, landscape for blog headers.
