# Brand Knowledge Base Builder (品牌知识母库构建 Skill)

## 简介
Brand Knowledge Base Builder 是一个面向品牌母库建设的底层 Skill。它的目标不是生成一次性的营销软文，而是将公司介绍、官网文案、产品资料、销售话术、案例、FAQ、竞品信息、品牌语气与禁用词等零散资料，整理为一套可复用的标准品牌资料包。

输出结果可以作为后续 AI Agent、RAG、官网 FAQ、销售支持、内容生成和 AI-GEO 系统的上游事实源。

## 当前版本
当前版本为 `v0.2`，已经支持：

- “上传资料”与“填写 intake 表单”双入口
- 多文件原始资料合并分析
- 结构化品牌 schema
- 资料完整度分析与追问清单
- 多格式导出：
  - `brand_knowledge_base.json`
  - `brand_knowledge_base.yaml`
  - `brand_knowledge_base.md`
  - `faq.md`
  - `glossary.md`
  - `standard_messaging.md`
  - `llms.txt`
  - `analysis_report.md`

## 公司在使用 Skill 前需要准备什么

第一次使用本 Skill 时，请明确要求公司至少提供以下 8 类资料：

1. 公司基础信息：品牌名称、公司名称、所属行业、产品类别、一句话定义、100 到 300 字公司简介
2. 官网与公开链接：官网首页、产品页、案例页、FAQ 页；如果没有完整官网，至少提供一个对外介绍页或文档
3. 产品与服务说明：卖什么、解决什么问题、怎么交付、如何收费
4. 目标客户信息：核心客户、次级客户、决策人、使用者、不适合客户
5. 核心卖点：至少 3 条，并尽量附证据、数据、客户反馈或资质依据
6. 联系方式：销售邮箱、支持邮箱、电话、微信/社媒、地址、工作时间、预约方式
7. 品牌语气与表达规范：语气关键词、必须出现的说法、禁用词、禁用承诺、安全替代表达
8. 合规边界：哪些能说、哪些不能说、哪些效果不能承诺、哪些内容必须人工审核

强烈建议同时提供：

- 客户案例 2 到 5 条
- FAQ 种子问题 10 到 20 条
- 竞品与替代方案
- 销售/客服话术
- 官网文案、宣传册、访谈纪要、录音转文字等原始素材

如果资料不完整，Skill 仍可生成初稿，但会把缺失项标记为 `待确认`，并在分析报告中列出追问清单。

## 如何使用

### 1. 先生成 intake 模板

```bash
python3 main.py --generate_intake_template --output_dir ./output
```

### 2. 只上传原始资料

```bash
python3 main.py \
  --input ./examples/example_input.md \
  --output_dir ./output
```

### 3. 混合模式：表单 + 原始资料

```bash
python3 main.py \
  --intake_file ./output/intake_form.yaml \
  --input ./examples/example_input.md \
  --output_dir ./output
```

### 4. 从已有 JSON 重新渲染整套产物

```bash
python3 main.py \
  --render_from_json ./output/brand_knowledge_base.json \
  --output_dir ./output_rerendered
```

### 5. 生成 ClawHub 可上传目录

如果 ClawHub 上传时报 `Remove non-text files`，通常是因为目录里混入了隐藏文件、`.env`、`__pycache__` 或 `.pyc` 缓存文件。

可直接运行：

```bash
python3 prepare_clawhub_upload.py
```

脚本会生成一个新的干净目录：

```text
../brand-knowledge-base-builder-clawhub-upload
```

这个目录会自动排除：

- `.env`
- `.env.example`
- `.clawhubignore`
- `__pycache__`
- `*.pyc`
- `output/` 等本地输出目录

建议上传这个新目录，而不是直接上传工作目录。

## 核心流程
1. Intake：接收表单与原始资料
2. Extraction：生成品牌母库核心 JSON
3. Analysis：识别缺失项、冲突项与追问清单
4. Asset Generation：生成 FAQ、术语库、标准话术和 llms 摘要
5. Export：导出完整资料包

## 备注
- 如果要读取 `.docx` / `.pdf`，请先安装 `requirements.txt` 中的可选依赖。
- 该 Skill 会将输入全文发送到你配置的 OpenAI-compatible API，请勿直接传入敏感机密资料。
