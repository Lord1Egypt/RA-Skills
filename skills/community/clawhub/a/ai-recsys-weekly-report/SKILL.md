---
name: AI RecSys Weekly Report
slug: ai-recsys-weekly-report
version: 1.0.0
description: >
  自动生成关于"AI大模型（LLM、VLM等）技术在搜索、广告、推荐（搜广推）领域应用"的深度技术周报，
  并自动同步到 IMA（腾讯文档/知识库）。触发词：AI搜广推技术周报、搜广推周报、大模型推荐报告、
  推荐系统技术周报、生成式推荐周报、Transformer推荐系统报告、Scaling Law推荐系统、
  MoE推荐系统、稀疏注意力推荐、RankMixer、OneTrans、MixFormer、BlossomRec。
  当用户要求定期生成搜广推领域的技术研究报告、论文综述或行业动态分析时触发此 skill。
author: fandywang
license: MIT-0
tags:
  - recommendation
  - search
  - advertising
  - weekly-report
  - automation
  - arxiv
  - transformer
  - llm
triggers:
  - AI搜广推技术周报
  - 搜广推周报
  - 大模型推荐报告
  - 推荐系统技术周报
  - 生成式推荐周报
  - Transformer推荐系统报告
  - Scaling Law推荐系统
  - MoE推荐系统
  - 稀疏注意力推荐
---

# AI 搜广推技术周报 - 自动化 Skill

> 本 Skill 将完整的"信息搜集 → 报告生成 → IMA 同步"流程打包，可迁移到任意 WorkBuddy 账号使用。

## 前置依赖

### 必须安装的 Skill

本 Skill 依赖以下 Skill，使用前请确保已安装：

1. **ima-skills**（或 **腾讯ima**）— 用于上传文件到 IMA 知识库
   - 安装后需配置 Client ID 和 API Key（见下方「IMA 配置」）

### 可选但推荐的 Skill

- **wechat-article-search** — 搜索微信公众号文章
- **zhihu-search-api-skill** — 搜索知乎文章
- **ArXiv论文追踪** — 搜索 ArXiv 最新论文

## IMA 配置

在使用此 Skill 前，必须先配置 IMA 凭证：

```bash
# 1. 打开 https://ima.qq.com/agent-interface 获取 Client ID 和 API Key

# 2. 存储凭证
mkdir -p ~/.config/ima
echo "你的Client_ID" > ~/.config/ima/client_id
echo "你的API_Key" > ~/.config/ima/api_key
```

## 使用方式

### 方式一：单次执行（手动触发）

当用户要求"生成搜广推周报"、"出一份大模型推荐系统的技术报告"时，按以下步骤执行：

#### Step 1：信息搜集

并行执行以下搜索（至少覆盖 ArXiv + 中文来源）：

**ArXiv 论文搜索**（核心）：
- `site:arxiv.org recommendation system transformer backbone 2025 2026`
- `site:arxiv.org recommendation MoE mixture of experts ranking`
- `site:arxiv.org sparse attention recommendation transformer`
- `site:arxiv.org generative recommendation LLM`

**中文技术文章搜索**：
- 微信公众号：`大模型推荐系统 Transformer 搜广推` （通过 wechat-article-search 或 web_search）
- 知乎：`搜广推 Scaling Law 推荐系统 大模型` （通过 zhihu-search 或 web_search）
- 技术博客：InfoQ、腾讯云开发者社区、CSDN 等

**特定技术追踪**：
- DeepSeek Sparse Attention (DSA)
- Kimi Attention Residuals (AttnRes)
- Qwen Gated Attention
- Muon 优化器
- SwiGLU 激活函数
- DeepSeekMoE

对搜索到的重要论文，使用 `web_fetch` 获取 arXiv 页面的详细信息（标题、作者、摘要、核心贡献）。

#### Step 2：生成报告

将搜集到的信息整理为 Markdown 格式的技术周报，必须包含以下章节：

1. **本周热点综述**（3-5条核心趋势，每条含论文链接）
2. **深度技术解读**（选择2-5篇最重要的工作，每篇包含）：
   - 论文基本信息（标题、作者、机构、会议/期刊、链接）
   - 核心创新点
   - 关键实验数据（具体数字）
   - 对搜广推领域的启示和建议
3. **技术对比分析**：
   - 至少一个对比表格（如不同架构对比、不同注意力机制对比）
   - 可选 ASCII 架构图展示演进路线
4. **创新思考与建议**（2-4条可操作的建议）
5. **趋势预测**（2-4个方向的前瞻性判断）
6. **延伸阅读推荐**（6-12条，分类整理：综述类 / 经典必读 / 技术博客）
7. **优化调整思考建议**（新增！本次研究的局限与后续改进方向）
8. **参考文献**（所有引用的完整列表，每项含可点击链接）

**格式要求**：
- 每篇论文/工作必须附带 arXiv 链接和 PDF 直接下载链接
- 尽可能附上中文解读链接（知乎/CSDN/博客园等）
- 如有 GitHub 开源仓库，附上 GitHub 链接
- 报告字数：2000-4000 字
- 文件命名：`AI搜广推技术周报_YYYY-MM-DD.md`

#### Step 3：上传到 IMA 知识库

**关键：必须使用 cos-upload.cjs 官方脚本上传 COS，不可用 curl 手动传。**

标准三步流程：

```bash
# 配置常量（每次执行时替换实际值）
FILE_PATH="<生成的报告路径>"
FILE_NAME="AI搜广推技术周报_YYYY-MM-DD.md"
FILE_EXT="md"
KB_ID="<目标知识库ID>"          # 用户需提供
MEDIA_TYPE=7                     # Markdown 固定为7
CONTENT_TYPE="text/markdown"

# 工具路径
NODE="/Users/fandywang/.workbuddy/binaries/node/versions/22.12.0/bin/node"
# 注意：目标账号需要确认 node 路径，可能不同
COS_SCRIPT="<skill目录>/scripts/upload-to-ima.py"

# 执行上传脚本
python3 "$COS_SCRIPT" --file "$FILE_PATH" \
  --kb-id "$KB_ID" \
  --title "$FILE_NAME"
```

或直接调用 `scripts/upload-to-ima.py` 封装脚本（见下方脚本说明）。

### 方式二：自动化定时任务

创建每周定时执行的自动化任务：

```
名称: AI大模型搜广推技术周报
频率: FREQ=WEEKLY;BYDAY=MO;BYHOUR=9;BYMINUTE=0
prompt: 请加载 ai-recsys-weekly-report skill，完整执行一次周报生成并同步到 IMA 知识库。
      知识库ID: <用户提供>
cwds: <用户的工作空间路径>
status: ACTIVE
```

## 脚本说明

### scripts/upload-to-ima.py

IMA 知识库上传封装脚本，内部实现标准的三步流程：

1. `create_media` — 获取 media_id 和 COS 上传凭证
2. `cos-upload.cjs` — 使用腾讯云 SDK 上传文件到 COS
3. `add_knowledge` — 将已上传文件关联到知识库

**用法**：
```bash
python3 scripts/upload-to-ima.py --file <报告路径> --kb-id <知识库ID> [--title <自定义标题>]
```

**依赖**：
- Python 3.x
- ima-skills 中的 `cos-upload.cjs` 脚本
- Node.js（用于运行 cos-upload.cjs）

**重要注意事项**：
- 如果 `cos-upload.cjs` 返回非零退出码，立即终止流程，不要继续调用 `add_knowledge`
- Node 路径需要在脚本中配置正确（不同环境可能路径不同）
- IMA 凭证从 `~/.config/ima/client_id` 和 `~/.config/ima/api_key` 读取

## 研究范围参考

以下是本 Skill 覆盖的核心技术方向，供搜索时参考关键词：

| 技术方向 | 代表性工作 | 搜索关键词 |
|:---|:---|:---|
| 统一 Backbone | OneTrans, RankMixer, MixFormer | unified backbone recommender, one transformer |
| Scaling Law | 10亿参数推荐Transformer | scaling law recommendation system |
| MoE 架构 | DeepSeekMoE, 专家路由 | mixture of experts recommendation |
| 稀疏注意力 | BlossomRec, DSA, ISA | sparse attention sequential recommendation |
| 残差连接革新 | Kimi AttnRes | attention residuals transformer |
| 门控注意力 | Qwen Gated Attention | gated attention mechanism |
| 优化器迁移 | Muon, Adam-mini | efficient optimizer recommendation |
| 激活函数 | SwiGLU, GeGLU | activation function recommender |
| 生成式推荐 | GRU4Rec, GenRec, MTGR | generative recommendation LLM |
