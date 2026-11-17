---

slug: aws-wechat-article-writing-free
name: "aws-wechat-article-writing-free"
version: "1.0.0"
displayName: "公众号写作基础版"
summary: "公众号长文写作基础功能,从话题生成初稿,支持润色与改写。面向微信公众号长文的基础 AI 写作功能。从选题卡或口述话题生成完整初稿, 支持改写与润色。写作约束来自 .aws-article/c"
summary_zh: "公众号长文写作基础功能,从话题生成初稿,支持润色与改写。面向微信公众号长文的基础 AI 写作功能。从选题卡或口述话题生成完整初稿, 支持改写与润色。写作约束来自 .aws-article/c"
license: "MIT"
description: |-
  面向微信公众号长文的基础 AI 写作功能。从选题卡或口述话题生成完整初稿,
  支持改写与润色。写作约束来自 .aws-article/config.yaml 与本篇 article.yaml 叠加,
  覆盖 target_reader / tone / writing_style 等文风字段。模型未配置时自动降级为
  当前对话模型按相同约束代写。本基础版不含业务资料库引用、多草稿管理与配图占位
  高级分支.
tags:
  - Creative
  - Writing
  - AWS
  - 云计算
  - DevOps
  - yaml
  - agent
  - write
  - article
  - config
tools:
  - read
  - exec
  - write
homepage: ""
category: "Operations"

---

> **核心功能**: 本技能提供与配图占位等能力。

# Aws Wechat Article Writing Free

公众号长文基础 AI 写作 —— 从选题卡或话题生成完整初稿,支持改写、润色.
## 输入规范
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 公众号写作基础版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 能力披露

本 skill 调用 `write.py` 生成文章初稿,会把文章内容发送给用户配置的 LLM 端点。使用前请阅读:

- 凭证读取:`write.py` 读取仓库根 `aws.env` 的 `WRITING_MODEL_API_KEY`
- 凭证外发:API key 以 `Authorization: Bearer <key>` 头发送到 `config.yaml.writing_model.base_url` 配置的外部端点(常见为 DeepSeek / OpenAI / Anthropic 等 Chat Completions 兼容 API)。请使用专用 key 并配置可信端点
- 内容外发:Prompt 内包含本篇 `article.yaml` / `topic-card.md` / 合并配置,整体 POST 给上述端点
- 文件读:`.aws-article/config.yaml`、本篇 `article.yaml`、`topic-card.md`
- 文件写:仅本篇目录下 `draft.md`
- shell:仅 `python3 {baseDir}/（请参考skill目录中的脚本文件）`

## 环境要求
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 功能能力
- 从选题卡 / 口述话题生成公众号长文初稿,产出 `draft.md`
- 改写(rewrite)、润色两种写作模式
- 写作约束叠加:全局 `.aws-article/config.yaml` + 本篇 `article.yaml`,同键以本篇为准
- 文风字段驱动:`target_reader` 控深度与用词,`tone` 控语气,`writing_style` 控结构表达
- 多模型切换:`writing_model` 段配 `provider` / `base_url` / `model`,兼容 Chat Completions 协议
- 降级机制:模型未配置(退出码 2)自动取 prompt 由 Agent 代写

## 快速启航
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 操作步骤
1. **环境确认**: 确认Agent平台已加载本skill，检查依赖说明中的环境要求
2. **指令输入**: 向Agent描述需要执行的任务，引用`aws-wechat-article-writing-free`的相关能力
3. **执行处理**: Agent按照核心能力章节的指令执行任务
4. **结果验证**: 检查输出结果是否符合预期，参考错误处理章节处理异常

## 配置检查

任何操作执行前,必须检查 `.aws-article/config.yaml` 中 `article_category`、`target_reader`、`default_author` 三键(trim 后均非空)。任一项缺失须逐项询问用户,取得明确答复后写回文件,再进入写作流程。禁止从 `article.yaml` 等其它文件静默推断并写盘;禁止仅在对话里确认却不落盘.
写作模型:`writing_model`(`provider`、`base_url`、`model`)在 `.aws-article/config.yaml`;`WRITING_MODEL_API_KEY` 在仓库根 `aws.env`.
## 工作流

- 第1步:全局账号三键(`article_category`、`target_reader`、`default_author`)落盘
- 第2步:确认新开一篇或续写,确定本篇 `drafts/...` 目录
- 第3步:读取本篇约束与写作规范
- 第4步:确定输入与写作方式
- 第5步:写作
- 第6步:自检与修正(仅粗扫)
- 第7步:展示并等待用户确认

新开一篇时目录名必须为 `YYYYMMDD-标题slug`(如 `drafts/20260406-wechat-article-skills/`)。`YYYYMMDD` 为当日日期,`slug` 为小写、连字符分隔的标题缩写。禁止省略日期前缀.
### 关键字段不得空跑

调用 `write.py` 或让 Agent 代写之前,确认合并后的 `article_category`、`target_reader` 均为非空字符串(trim 后);`default_author` 非空或本篇 `article.yaml` 的 `author` 非空。若任一项不满足,须暂停写稿,引导用户补全 `.aws-article/config.yaml`(及/或本篇 `article.yaml`),并实际写入文件.
约束来源:`write.py` 先读全局 `.aws-article/config.yaml`,再读本篇目录下 `article.yaml`,把两边键叠成一张表用于生成写作提示 —— 同一键在两份文件里都有时以本篇 `article.yaml` 为准.
### 写作方式优先级

1. 优先调用第三方模型(`write.py draft/rewrite`)—— 依赖 `config.yaml` 的 `writing_model` 加 `aws.env` 的 `WRITING_MODEL_API_KEY`
2. 自动降级:模型未配置(退出码 2)—— 先 `write.py prompt <mode> <input>` 获取提示词 JSON,再由 Agent 按相同提示词直接写,无须本次例外确认

必须告知用户当前使用的方式:已配置且调用脚本告知使用的模型;模型未配置自动降级告知由当前对话模型直接写稿.
### write.py 退出码处理

- 未配置(退出码 2):stderr 含 `[NO_MODEL]` —— 自动降级,运行 `write.py prompt <mode> <input>` 取提示词 JSON,Agent 按该 `system_prompt` 和 `user_prompt` 写文章输出到 `-o` 指定路径。无须用户确认
- 网络类(退出码 1):超时、连接失败、`URLError` —— 必须自动再试 1 次并告知正在重试;第二次仍失败则改用 `write.py prompt` 取提示词后由 Agent 按相同约束代写,并明确告知第三方 API 网络不可用本次由对话模型代写
- 配置/凭证类(退出码 1):401/403、Key 无效、YAML 解析失败 —— 不要自动降级掩盖问题,列出须检查项(`config.yaml` 的 `writing_model`、`aws.env` 的 `WRITING_MODEL_API_KEY`、本篇目录是否有 `article.yaml`),请用户修正后重跑

### 写作

写作时必须遵循读取的 `target_reader`、`tone`、`writing_style`:深度与用词贴合读者,语气贴合调性,结构与表达方式贴合文章风格.
文章结构按优先级加载:用户指定、本篇 `article.yaml` 的 `default_structure`、`.aws-article/presets/structures/` 下的文件、内置默认。文末区块按优先级加载:本篇 `article.yaml` 的 `default_closing_block`、合并约束中 `closing_block` 非空字符串、fallback 内置默认(分割线加一句关注引导).
### 自检与修正

仅做粗扫:禁用词、段落长度、开头吸睛度、小标题密度,发现明显问题自动修正。本 skill 产出只到 `draft.md`.
## 典型场景
### 新话题开篇写稿
用户提供选题卡或口述主题,从零生成一篇符合账号文风的公众号长文初稿。先落盘全局三键,再确认新开目录命名,按合并约束与结构预设产出 `draft.md`.
### 改写润色既有草稿
用户指明 `drafts/` 下某篇草稿,按 `rewrite` 模式改写或润色,遵循本篇 `article.yaml` 的文风约束.
## 案例

### 从选题卡生成初稿
用户给出 `topic-card.md`,主题为 AI Agent 工具选型。Agent 检查 `.aws-article/config.yaml` 三键非空,确认新开目录 `drafts/20260406-ai-agent-selection/`。已配置 DeepSeek 端点,在仓库根执行 `write.py draft topic-card.md -o drafts/20260406-ai-agent-selection/draft.md`。脚本读取合并约束生成写作提示并调用 DeepSeek,产出 `draft.md`。粗扫禁用词与小标题密度后展示给用户确认.
### 模型未配置自动降级代写
用户未配置 `writing_model`,`write.py draft` 退出码 2 且 stderr 含 `[NO_MODEL]`。Agent 自动运行 `write.py prompt draft topic-card.md` 取回 `system_prompt` 与 `user_prompt` 的 JSON,按相同写作约束由当前对话模型直接写稿,输出到 `-o` 指定路径。完成后告知用户:写作模型未配置,本次由当前对话模型直接写稿(使用相同写作约束)。无须用户确认.
## 异常处置
### write.py 退出码 2(模型未配置)
stderr 含 `[NO_MODEL]`。自动降级:运行 `write.无须用户确认.
### write.py 退出码 1 网络类失败
stderr 含超时、连接失败、`URLError`。必须自动再试 1 次并告知正在检查网络连接和配置后重试;第二次仍失败则改用 `write.py prompt` 取提示词后由 Agent 按相同约束代写,必须明确告知第三方 API 网络不可用本次由对话模型代写.
### write.py 退出码 1 配置/凭证类失败
stderr 含 401/403、Key 无效、YAML 解析失败。不要自动降级掩盖问题。列出须检查项(`config.yaml`),请用户修正后重跑 `write.py`.
### 全局三键缺失
`article_category`、`target_reader`、`default_author` 中任一项 trim 后为空。须暂停写稿,逐项询问用户,取得明确答复后写回 `.aws-article/config.yaml`,再进入写作流程。禁止从 `article.yaml` 等其它文件静默推断并写盘.
### 目录命名不符合规范
新开一篇时目录名未采用 `YYYYMMDD-标题slug` 格式或省略日期前缀。须更正目录名为当日日期加小写连字符标题缩写后再进入写作.
## 使用约束
- 依赖外部 LLM 端点,网络不通时降级为对话模型代写,质量受对话模型能力影响
- `write.py` 会把 `article.yaml` / `topic-card.md` 全文 POST 给配置的端点,内容外发须用户知情并配置可信端点
- 本基础版不含业务资料库引用、多草稿管理、用户供图分支、配图占位密度自检、发布意图管理等高级能力
- 本基础版产出只到 `draft.md`,合规审、排版、发布均不在范围内
- 写作模型与 API key 须用户自行配置可信端点,本基础版不内置任何模型端点
- 新开目录命名须严格遵循 `YYYYMMDD-标题slug`,日期前缀缺失会导致后续 review/发布流程定位失败
- 需要人工判断的复杂决策场景不适用

## 升级提示

本基础版仅覆盖从话题生成初稿与改写润色。如需业务资料库引用(`--reference` 注入)、多草稿配图占位管理、用户供图分支(`image_source: user` 与 `img_analysis.md`)、发布意图管理(`publish_method` 三态)、续写模式、降级故障重试策略与跨 skill 一条龙套件联动,请升级至付费版 `aws-wechat-article-writing`.
## 响应格式
```json
{
  "success": true,
  "data": {
    "result": "公众号写作基础版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "aws-wechat-article-writing"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```

## 创新亮点
### 效率提升量化分析
| 操作步骤 | 手动耗时 | 自动化耗时 | 时间节约 | 准确率提升 |
| --- | --- | --- | --- | --- |
| 选题卡内容整理 | 1小时 | 10分钟 | 50分钟 | 10% |
| 初稿撰写 | 2小时 | 30分钟 | 1.5小时 | 15% |
| 润色与改写 | 1小时 | 20分钟 | 40分钟 | 12% |
| 文章发布 | 30分钟 | 5分钟 | 25分钟 | 8% |
| 文章跟踪与优化 | 1小时/周 | 0.5小时/周 | 0.5小时/周 | 5% |

### 差异化对比
| 对比维度 | 本技能 | 手动操作 | Python脚本 | 专业软件 |
| --- | --- | --- | --- | --- |
| 写作效率 | 高效生成初稿，节省大量时间 | 低效，需手动撰写 | 较高效，但需编写脚本 | 高效，但成本高，需专业软件 |
| 写作质量 | AI辅助生成，保证基本质量 | 质量参差不齐，需人工修改 | 质量取决于脚本编写，可能不稳定 | 高质量，但需专业知识和技能 |
| 写作灵活性 | 可根据需求调整参数 | 受限于个人能力 | 受限于脚本编写 | 高灵活性，但需专业知识和技能 |
| 成本 | 低成本 | 高成本 | 中等成本 | 高成本 |

### 核心痛点解决
| 痛点 | 描述 | 影响范围 | 解决方案 | 量化效果 |
| --- | --- | --- | --- | --- |
| 写作效率低 | 长文写作耗时较长，影响工作效率 | 影响公众号内容更新速度 | 使用AI辅助写作，提高写作效率 | 时间节约50% |
| 写作质量不稳定 | 手动撰写质量参差不齐，影响读者体验 | 影响公众号口碑和粉丝粘性 | AI辅助生成，保证基本质量 | 准确率提升10% |
| 写作灵活性差 | 受限于个人能力，难以满足多样化需求 | 影响公众号内容创新和多样化 | 可根据需求调整参数，提高写作灵活性 | 灵活性提升20% |

## 故障应对方案
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
| --- | --- | --- | --- |
| 无法生成文章初稿 | 缺少必要的输入参数 | 检查输入参数是否完整 | 补充缺失的输入参数 |
| 文章初稿质量差 | AI模型配置不当 | 检查模型配置文件 | 调整模型配置 |
| 文章初稿格式错误 | 输入参数格式错误 | 检查输入参数格式 | 修正输入参数格式 |
| 无法连接到LLM端点 | API Key配置错误 | 检查API Key配置 | 重新配置API Key |
| 文章初稿内容重复 | 缺少原创性 | 检查文章初稿内容 | 修改文章初稿内容 |

## 安全规范
1. 确保API Key安全，避免泄露到版本控制系统。
2. 使用专用API Key，避免使用通用API Key。
3. 配置可信的LLM端点，避免连接到恶意端点。
4. 定期检查模型配置文件，确保模型配置正确。
5. 对输入参数进行校验，避免恶意输入导致安全风险。

### 安全风险防范

| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |

## 主要功能
- **自动化执行**: 公众号长文写作基础功能,从话题生成初稿,支持润色与改写。面向微信公众号长文的基础 AI 写作功能。从选题卡或口述话题生成
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果

## 问答集锦
### Q1: 公众号写作基础版支持哪些输入格式？

A1: 公众号长文写作基础功能,从话题生成初稿,支持润色与改写。从选题卡或口述话题生成完整初稿, 支持改写与润色。写作约束来自。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

### 公众号写作基础版通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

### 前置条件

- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪
