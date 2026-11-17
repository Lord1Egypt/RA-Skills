---
name: bankai
version: 1.0.1
description: 银行AI写作助手——一句话需求即生成59种"银行味"公文底稿，严格遵循GB/T 9704-2012格式，内置反编造护栏。需自备DeepSeek API Key。
author: 王先生 (BankAI)
tags: [banking, 公文写作, deepseek, 银行, document-generation, finance]
license: MIT-0
homepage: https://www.deepwater84.cn/bankai/
agent_created: true
---

# 🏦 BankAI · 银行公文写作助手

> **一句话需求 → 59 种"银行味"公文底稿。** 严格遵循《党政机关公文格式》GB/T 9704-2012，内置反编造护栏，复制即可改、审核后可用。

BankAI 把你的口语化需求，按 59 种银行公文文种之一，调用 DeepSeek 生成一份**纯文本、格式合规、零编造**的底稿。它不替你拍板，只帮你把"从空白到初稿"这一步从半小时压到一分钟。

## ✨ 核心能力

- **59 种银行公文全覆盖**——监管回复、分析研判、规章制度、行政公文、汇报总结、自定义，六大类。
- **"银行味"国标格式**——强制中文全角标点、禁用 Markdown、套用 GB/T 9704-2012 公文结构，交上去不像 AI 写的。
- **反编造护栏（硬铁律）**——输入未给的任何数字、金额、人名、文号、日期，一律写成 `XX` 占位，文末附"需人工核实"清单。**绝不发生"看起来很真其实是编的"数据**。
- **双入口**——命令行（CI / 批处理友好）或直接对话触发。
- **数据不出域**——你自备 DeepSeek Key，调用在你本地或你指定的端点完成。

## 🔑 使用前提

⚠️ **你必须自备 DeepSeek API Key。** BankAI 不在云端代付，不收集你的任何数据，也不替你承担任何 API 费用——你用你自己的 Key 直连 DeepSeek。

没有 Key 时，可用 `--mock` 参数预览输出结构（不真实调用模型）。

## ⚙️ 环境变量配置

只需一步，把 Key 交给运行环境：

```bash
# Linux / macOS
export DEEPSEEK_API_KEY="sk-your-real-key-here"

# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="sk-your-real-key-here"
```

> 备用方案：运行时用 `--key-env` 指定其他环境变量名（默认即 `DEEPSEEK_API_KEY`）。

**私有化部署（数据不出行）：** 用 `--base-url` 指向你内网 / 自建的 OpenAI 兼容端点，或改 `config.json` 的 `baseUrl`：

```bash
node scripts/bankai_write.mjs --type 通知 --input @req.json --base-url https://your-intranet-endpoint/v1/chat/completions
```

## 🖥️ 方式一：命令行（CLI）

```bash
# 列出全部 59 种文种（含 id / 分类 / 名称）
node scripts/bankai_write.mjs --list

# 生成一篇公文：--type 接文种 id 或中文名称，--input 接 JSON 或 @文件
node scripts/bankai_write.mjs --type 贷后检查报告 --input '{"借款人":"XX科技有限公司","授信额度":"XX万元","检查周期":"2026年Q2"}'

# 结果写入文件（不写则打印到终端）
node scripts/bankai_write.mjs --type 请示 --input @req.json --output 请示_草稿.txt

# 预览结构（不真实调用，免 Key）
node scripts/bankai_write.mjs --type 通知 --input '{}' --mock
```

常用参数：

| 参数 | 说明 | 必填 |
|------|------|------|
| `--type` | 文种 id 或中文名称（如 `贷后检查报告`） | ✅ |
| `--input` | JSON 字符串，或 `@文件路径`（字段键值对） | ✅ |
| `--output` | 输出文件路径（缺省打印到终端） | ❌ |
| `--base-url` | 自建 / 私有化端点（合规内网部署） | ❌ |
| `--model` | 模型名（默认 `deepseek-chat`） | ❌ |
| `--key-env` | API Key 所在环境变量名（默认 `DEEPSEEK_API_KEY`） | ❌ |
| `--mock` | 用假数据预览输出结构，不调模型 | ❌ |
| `--list` | 列出全部 59 种文种 | — |

## 💬 方式二：对话触发

在装载了 BankAI 的助手（如 WorkBuddy / OpenClaw）里，直接用自然语言说：

> "帮我写一份关于XX支行二季度不良率上升的情况说明"
> "出个请示，关于申请增加柜面人员的"
> "写一份贷后检查报告，借款人XX科技"

Skill 会：① 识别文种 → ② 追问缺失的必填字段 → ③ 生成纯文本底稿并附"需人工核实"清单。

## 📋 使用示例

**示例 1 · 监管报送（CLI）**
```bash
node scripts/bankai_write.mjs \
  --type 情况说明 \
  --input '{"事项":"XX支行二季度不良率上升至XX%","原因概述":"XX","已采取措施":"XX","后续安排":"XX"}'
```
→ 输出一份结构完整的监管情况说明底稿，缺失的量化指标以 `XX` 占位，文末列出需人工补实的数据。

**示例 2 · 内部请示（CLI + 文件）**
把需求写进 `req.json`：
```json
{"事项":"申请增配2名柜面人员","理由":"网点日均客流XX、峰值排队XX分钟","编制现状":"现有XX人"}
```
```bash
node scripts/bankai_write.mjs --type 请示 --input @req.json --output 请示_草稿.txt
```

**示例 3 · 对话生成**
> 你说：*"写个通知，全行周五下午3点开季度风控会"*
> BankAI：识别为「通知」文种，追问会议地点、主持人等必填项，补全后生成合规通知正文。

## 🗂️ 59 种公文类型（六大类）

> 完整字段定义与提示词见 `references/scenarios.mjs`（从线上源码提取，请勿手改）。运行 `--list` 可看全部 id。

- **监管回复（7）**：情况说明、调查报告、监管指标专项说明报告、监管检查整改回复、陈述申辩函、重大事项即时上报、银行询证函回复
- **分析研判（11）**：贷款贷后检查报告、风险分析报告、贷前调查报告、授信审批意见书、风险预警通知书、不良资产处置报告、合规审查意见书、财务分析报告、贷款五级分类认定、逾期催收通知书、产品说明书
- **规章制度（5）**：管理办法、实施方案、突发事件应急预案、岗位说明书、合作框架协议
- **行政公文（20）**：通知、函件、请示、通报、会议纪要、批复、意见、决定、公告、通告、工作计划、跨部门工作联系单、督办通知、合规承诺书、在职/收入证明、现金调拨申请、人事通知、客户投诉回复函、账户冻结告知函、贷款到期提醒函
- **汇报总结（15）**：工作总结、工作报告、述职报告、竞聘报告、工作简报、倡议书、备忘录、营销活动方案、柜面账务差错说明、预算编制/执行分析、年末财务决算报告、资金头寸报告、税务测算及申报说明、绩效考核通报、培训计划/总结
- **自定义（1）**：自定义公文

## ❓ 常见问题（FAQ）

**Q1：DeepSeek API Key 在哪获取？**
到 [DeepSeek 开放平台](https://platform.deepseek.com) 注册 → 充值 → 在「API Keys」页创建 Key（形如 `sk-...`）。Key 仅存于你本地环境变量，BankAI 不会上传。

**Q2：提示"未找到公文类型"？**
`--type` 必须填**精确**的文种 id 或中文名称（如 `贷后检查报告`），不支持模糊匹配（银行场景选错文种代价大，宁可报错）。先用 `--list` 查准确名称。

**Q3：调用超时 / 一直转圈？**
默认 120 秒超时并自动重试 3 次（429 / 5xx）。若仍失败：检查 Key 是否有效、网络是否可达 `api.deepseek.com`、账户余额是否充足。

**Q4：生成的数字靠谱吗？会不会编？**
不会编。反编造护栏强制：输入没给的具体数值一律 `XX` 占位，文末附"需人工核实"清单。**所有 AI 生成内容都必须经人工审核后使用，禁止直接提交。**

**Q5：能部署到银行内网吗？**
能。用 `--base-url` 指向你内网自建的 OpenAI 兼容推理端点（如 Ollama / vLLM），数据全程不出域。详见 `references/usage.md`。

**Q6：多少钱？**
模型费用由 DeepSeek 按量计收（你自己的账户），BankAI 本身免费。大致成本见 `references/usage.md`。

## 📮 联系与商业合作

- 🌐 官网：https://www.deepwater84.cn/bankai/
- 📧 邮箱：458468698@qq.com
- 💼 服务：企业私有化部署 / 专属文种定制 / 培训咨询

> 面向银行、消金、农商行的**内网私有化部署**与**专属文种定制**欢迎洽谈。

## 📄 许可证

[MIT-0](https://opensource.org/licenses/MIT-0) —— 免费使用、修改、分发，无需署名，无担保。

---

© BankAI. 生成内容仅供草稿参考，须经人工合规审核后使用。
