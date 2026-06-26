# AI Trending Sources — Reference Guide

## Primary Sources (must query every run)

### 1. GitHub Trending
- **URL**: https://github.com/trending?since=weekly&spoken_language_code=
- **AI-filtered URL**: https://github.com/trending?since=weekly&l=python (Python repos, most AI repos are Python)
- **Stars API**: `https://api.github.com/search/repositories?q=topic:llm+topic:ai&sort=stars&order=desc&per_page=30`
- **Key signals**: stars today, forks, watchers
- **Tip**: Filter by topics: `llm`, `large-language-model`, `ai`, `machine-learning`, `generative-ai`, `multimodal`, `rag`, `agent`

### 2. HuggingFace Hub — Trending
- **URL**: https://huggingface.co/models?sort=trending
- **Spaces trending**: https://huggingface.co/spaces?sort=trending
- **Datasets trending**: https://huggingface.co/datasets?sort=trending
- **Key signals**: downloads (30d), likes, model size, license

### 3. Papers With Code
- **URL**: https://paperswithcode.com/trending
- **Latest methods**: https://paperswithcode.com/methods
- **Key signals**: paper + GitHub stars combo = high-quality signal

### 4. arXiv
- **cs.AI (Artificial Intelligence)**: https://arxiv.org/list/cs.AI/recent
- **cs.CL (Computation and Language / NLP)**: https://arxiv.org/list/cs.CL/recent
- **cs.CV (Computer Vision)**: https://arxiv.org/list/cs.CV/recent
- **cs.LG (Machine Learning)**: https://arxiv.org/list/cs.LG/recent
- **Tip**: Look for papers with associated GitHub links in abstract

## Secondary Sources (query when possible)

### 5. Twitter / X Search
- Queries to run:
  - `#OpenSourceAI min_faves:500 lang:en -is:retweet`
  - `#LLM open source github since:7days`
  - `new model release github stars`
- **Tip**: High-engagement tweets about new model releases are leading indicators

### 6. Reddit
- **r/MachineLearning**: https://www.reddit.com/r/MachineLearning/hot/
- **r/LocalLLaMA**: https://www.reddit.com/r/LocalLLaMA/hot/
- **r/artificial**: https://www.reddit.com/r/artificial/hot/
- **Key signals**: upvotes, comment count, cross-posts

### 7. AI News Aggregators
- **The Batch (deeplearning.ai)**: https://www.deeplearning.ai/the-batch/
- **AI News (Ben's newsletter)**: https://buttondown.email/ainews/archive
- **Hacker News AI filter**: `https://hn.algolia.com/?q=LLM+open+source&dateRange=pastWeek`
- **TLDR AI**: https://tldr.tech/ai

### 8. Chinese AI Communities (for Z先生)
- **量子位**: https://qbitai.com
- **机器之心 / Synced**: https://jiqizhixin.com
- **AIBase**: https://top.aibase.com
- **GitHub中文社区热榜**: https://github.com/GrowingGit/GitHub-Chinese-Top-Charts

## Project Categories to Track

| Category | Keywords |
|----------|----------|
| LLM 底座模型 | foundation model, pretrained, base model, 7B/13B/70B |
| 多模态 | multimodal, VLM, vision-language, text-to-image, text-to-video |
| Agent / 工具链 | agent framework, tool-use, function-calling, MCP, ReAct |
| RAG / 知识库 | RAG, retrieval-augmented, vector DB, embedding |
| 推理加速 | inference, quantization, GGUF, vLLM, speculative decoding |
| 微调 / 数据 | fine-tuning, RLHF, DPO, LoRA, dataset, SFT |
| 代码生成 | code LLM, copilot, code generation |
| 语音 / TTS | TTS, ASR, speech, voice clone |
| 具身智能 | robotics, embodied AI, manipulation |

## Star Velocity Formula

```
velocity = (stars_now - stars_7d_ago) / 7
```

Projects with velocity > 500 stars/day are considered "爆火".
Projects with velocity > 200 stars/day are considered "热门".
Projects with velocity > 50 stars/day are "值得关注".

## Freshness Criteria

- **Hot** (🔥): Released or major update within past 14 days
- **Fresh** (✨): Released or major update within past 30 days  
- **Established** (📌): Older but consistently trending
