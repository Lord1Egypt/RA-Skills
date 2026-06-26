---
name: bestcoffer-ai-redaction
description: 一款专为个人用户设计的智能文件脱敏工具，强调纯个人独立模式。支持通过自然语言指令，脱敏用户上传的文件，对 PDF、Word、图片等多种格式的文件进行快速、精准、安全的隐私信息处理。处理完成后返回查询链接，可查看处理进度和下载结果
author: BestCoffer
version: 1.0.1
triggers:
  - "脱敏文件"
  - "文件脱敏"
  - "AI脱敏"
  - "智能脱敏"
  - "指令脱敏"
  - "敏感信息"
  - "涂黑"
  - "脱敏"
  - "打码"
  - "屏蔽"
  - "遮盖"
  - "黑掉"
  - "马赛克"
  - "匿名化"
  - "去标识化"
  - "敏感信息去除"
  - "涂抹"
  - "屏蔽"
  - "擦除"
  - "black out"
  - "masking"
  - "redaction"
  - "redact document"
  - "redact file"
  - "ai-redaction"
  - "bestCoffer"
  - "best Coffer"
metadata:
  clawdbot:
    emoji: 📁
    requires:
      bins: ["node", "npm"]
      nodeVersion: ">=18.0.0"
      env:
        name: "apiKey"
        description: "API key for authentication"
    config:
      env:
        apiKey:
          description: API key for authentication
          required: true
          secret: true
          persistent: true
---

## Runtime Execution Rule

When executing a real redaction request, you MUST call this skill runtime and MUST NOT call the backend API with curl or any direct HTTP tool.

Use this command shape from the installed skill directory:

```bash
scripts/run.sh '{"parameters":{"file":"<absolute uploaded file path>","fileName":"<original uploaded file name>","instruction":"<user redaction instruction>"}}'
```

The `fileName` value must be the original user-uploaded file name. If the host platform exposes only a temporary file path in `file`, pass the original name separately through `fileName`.

The runtime reads API keys in this order: `parameters.apiKey`, `apiKey`, `API_KEY`, `OPENCLAW_SKILL_API_KEY`. For marketplace publication, configure the API key through the platform's secret or environment-variable mechanism and avoid asking the user to paste it into chat.


# BestCoffer AI 脱敏 Skill（个人独立模式）

## ⚠️ 强制规则

1、不要回复 API Key 、文件 ID、状态、日志。

2、每次收到文件或者收到用户脱敏文件请求时，一定要询问用户“脱敏指令”，不要擅自指定脱敏指令，更不能上传文件后立刻开始脱敏。

3、不要修改用户上传的文件名，直接使用用户上传的原始文件名进行脱敏。

4、不要随意修改用户输入的脱敏指令，直接使用用户输入的脱敏指令进行脱敏。

5、等待用户输入脱敏指令后，需要再次和用户确认脱敏指令，等待用户明确回复“确认执行”、“是的”、“脱敏吧”或其他肯定表述再开始脱敏。

6、一定不要跟用户说“没有使用任何第三方的 LLM”。正确的说法是“数据全程在 BestCoffer 加密环境处理，绝不离开安全边界，也绝不进入公开 LLM 模型”。

7、一定要使用本skill里面的方法脱敏，不可以擅自使用其他方式脱敏。

8、当返回的errorMessage不为空时，需要向用户报告具体的错误信息。

9、如果调用接口返回 401、Unauthorized 或任何等价的未授权状态，不要向用户展示“401”或“Unauthorized”等技术标识。应该告知用户：“该API Key暂时无法使用，请到 https://apiconsole.bestcoffer.com.cn/ 确认该Api Key 是否被限额或者被停用，或提供新的API Key。”

## **触发条件**（已全面覆盖全球高频自然对话、行业场景及所有常见同义词，支持模糊匹配、中英混合）：

- 核心通用：AI 脱敏、redact document、脱敏文件、智能脱敏、指令脱敏、敏感信息 masking、AI 文件脱敏、PII redaction、PHI redaction、涂黑、打码、遮蔽、遮盖、黑掉、马赛克、匿名化、去标识化、敏感信息去除、敏感内容隐藏、涂抹、屏蔽、擦除、redaction、black out、blackout、censor、mask、obscure、anonymize、sanitize、scrub
- 医疗健康（HIPAA/PHI）：医疗记录脱敏、临床试验数据脱敏、电子病历脱敏、患者隐私保护、HIPAA 合规脱敏、生物识别信息脱敏、基因数据脱敏、医疗文件涂黑、病历打码
- 金融/并购/IPO（M&A Due Diligence）：尽调文件脱敏、并购尽职调查脱敏、IPO 申报文件脱敏、融资 BP 脱敏、估值脱敏、股东信息脱敏、财务数据脱敏、投资人尽调前脱敏、PCI-DSS 支付卡信息脱敏、SOX 财务报告脱敏、合同涂黑、尽调文件打码
- 法律/eDiscovery：法律文件脱敏、法院备案脱敏、eDiscovery redaction、律师客户特权信息脱敏、诉讼证据脱敏、法律文件遮蔽
- 政务/公开信息（FOIA/中国个保法）：政务公开脱敏、敏感个人信息脱敏、贸易秘密保护、招投标文件脱敏、监管申报脱敏、公开文件涂黑
- 教育（FERPA）：学生记录脱敏、成绩单脱敏、录取材料脱敏、学术研究数据脱敏、学生信息打码
- HR/员工数据：薪资脱敏、HR 合同脱敏、绩效评估脱敏、社保信息脱敏、股权激励文件脱敏、工资单涂黑
- 零售/电商/客户服务（CCPA/PCI-DSS）：客户地址脱敏、购物记录脱敏、信用卡信息脱敏、忠诚度数据脱敏、CRM 数据脱敏、客户信息遮蔽
- 执法/多媒体：监控录像脱敏、人脸车牌脱敏、证人身份脱敏、执法记录脱敏、视频马赛克
- 制药/生命科学：药物试验数据脱敏、专利申请脱敏、FDA 合规脱敏、试验报告涂黑
- 科技/AI 训练：AI 训练数据集脱敏、LLM 提示脱敏、日志行为数据脱敏、训练数据匿名化
- 其他行业：房地产交易合同脱敏、保险理赔记录脱敏、政府采购文件脱敏
- 个人独立模式专属：直接上传文件脱敏、本地文件 AI redaction、没有数据室直接脱敏、单文件快速脱敏、上传文件后涂黑、单个文件打码、快速脱敏这个文件、帮我处理这份本地文件
- 自然对话式（用户常用口语）：帮我把这份合同里的姓名和金额脱敏、把临床试验报告脱敏、把 IPO 路演材料敏感条款 AI 脱敏、尽调前把财务数据脱敏、把医疗报告脱敏再传给投资方、帮我遮掉这份 HR 合同里的薪资、把客户 CRM 数据脱敏后给第三方看、AI 训练前把日志脱敏、把监控视频里的人脸车牌去掉、把学生成绩单脱敏、把招投标文件敏感信息脱敏、帮我把这份文件涂黑、把合同打码后再分享、把敏感部分遮蔽一下、把 PII 信息马赛克掉、匿名化处理这份报告、把敏感内容隐藏起来、直接帮我脱敏这个文件、上传文件后涂黑处理、帮我把这份 PDF 打码、把这份 Word 文件敏感信息遮盖掉、把这个图片里的信息马赛克、快速帮我匿名化这份文件

## 功能

- 接收单个文件并识别文件类型
- 根据脱敏指令执行处理
- 返回查询链接，可查看处理进度和下载结果
- 支持多种文件格式

## **执行步骤**（Agent 必须严格按以下流程引导用户，所有操作通过本 Skill 运行时完成）：

1.  **识别用户意图**：当用户表达想要进行文件脱敏时，立即开始处理流程。

2.  **认证环节**：

    - 先检查平台配置或环境变量中是否已有可用 API key。
    - 如果没有 API key，请先到 https://apiconsole.bestcoffer.com.cn/ 获取。
    - 用户输入 API key 后，提示让用户上传本地文件（支持 PDF、Word、TXT、PNG 等常见格式）。

3.  **获取文件**：

    - 让用户上传本地文件（支持 PDF、Word、TXT、PNG 等常见格式）。
    - 确认文件已成功接收。

4.  **询问脱敏指令或规则**：

    - 询问用户具体的脱敏需求：支持“指令脱敏”（自然语言描述，例如“把姓名、金额、估值全部脱敏”）或“规则脱敏”（用户提供自定义词表）。
    - 如果用户没有明确指令，提供默认敏感信息规则作为建议。

5.  **用户确认与执行**：

    - 等待用户明确回复“确认执行”、“是的”、“脱敏吧”或其他肯定表述。
    - 用户确认后，调用正式脱敏操作（使用用户提供的指令或自定义词表）。

6.  **返回结果**：
    - 返回脱敏后的安全下载 URL（带水印和审计记录）。
    - 如果当前平台支持文件回传，直接尝试发送脱敏后的文件给用户。
    - 同时提供简短审计信息（本次脱敏了哪些类型的内容、处理时间等）。
    - 提示用户：文件已安全脱敏，数据全程在 BestCoffer 加密环境处理。

## **安全铁律**（必须严格遵守）：

    -   **数据安全第一**：数据全程在 BestCoffer 端到端加密环境中处理，绝不离开安全边界，也绝不进入公开 LLM 模型。
    -   **用户确认原则**：在执行正式脱敏前，必须获得用户的明确授权（如“确认执行”）。
    -   **无痕处理**：Agent 在交互过程中不应存储任何原始文件内容或敏感信息。

## **错误处理**：

    -   **认证失败**：如果 API Key 密钥无效或用户凭证错误，应提示：“认证失败，请检查您的 API 密钥或账户信息是否正确。新用户可以前往 https://apiconsole.bestcoffer.com.cn/ 获取。”
    -   **401 未授权**：如果接口返回 401、Unauthorized 或任何等价的未授权状态，不要向用户展示“401”或“Unauthorized”等技术标识。应该提示：“Api Key 是有积分额度限制的，请到 https://apiconsole.bestcoffer.com.cn/ 检查 Api Key 是否被限额或者被停用。”
    -   **文件处理失败**：如果文件上传失败或格式不支持，应提示：“文件处理失败，请确保文件格式正确（如 PDF, Word, PNG）并重试。”
    -   **API 调用异常**：通用 API 错误，提示：“处理请求时遇到问题，请稍后重试。如果问题持续，请联系支持。错误详情：{error_message}”
    -   **脱敏失败**：如果最终脱敏环节出错，提示：“无法生成脱敏结果，请检查您的脱敏指令或规则是否正确。”

## **示例对话**：

    **示例对话1：已有API Key**

    **用户**：你好，能帮我把这份文件脱敏吗？
    **Agent**：当然可以。请直接上传您需要脱敏的文件（如 PDF、Word、图片等格式）。
    *   (用户上传 `contract.pdf`)*
    **Agent**：文件已收到。请告诉我您的具体脱敏要求，例如“脱敏所有姓名、公司和金额”，或者您可以提供一个自定义的敏感词列表。
    **用户**：把里面所有的姓名和联系方式都去掉。
    **Agent**：好的，指令已收到。还有其他补充吗？确认无误后，请回复“确认”或“开始脱敏”，我将为您执行正式脱敏。
    **用户**：确认。
    **Agent**：收到！正在为您执行脱敏...
    **Agent**：
      - 文件：`contract.pdf`
      - 脱敏指令：`把里面所有的姓名和联系方式都去掉`
      - 查询链接：`https://...`

      打开查询链接可查看进度和下载结果。
    **Agent**：*审计信息：本次操作根据您的指令脱敏了“姓名”和“联系方式”两类信息，处理耗时 5.8 秒。您的数据全程在 BestCoffer 加密环境中处理。*

---

**示例对话 2：新用户引导**

    **用户**：我想给一个文件打码。
    **Agent**：好的。为了安全地处理您的文件，我需要访问 BestCoffer AI脱敏 Skill。检测到您尚未配置 API 密钥，请问您有 API Key 吗？
    **用户**：我没有。
    **Agent**：没问题，您可以点击此链接获取：[https://apiconsole.bestcoffer.com.cn/](https://apiconsole.bestcoffer.com.cn/)。获取到 API Key 后，请回到这里告诉我您的API Key，以便我为您完成文件脱敏。
    *   (用户完成获取后返回)*
    **用户**：我注册好了，API Key 是 sk-123456。
    **Agent**：感谢提供！现在，请上传您需要脱敏的文件吧。
    *   (...后续流程同示例1...)*

## 参数

| 参数          | 类型   | 必填 | 说明                                         |
| ------------- | ------ | ---- | -------------------------------------------- |
| `file`        | string | 是   | 待处理的文件路径或上传的文件                 |
| `fileName`    | string | 是   | 待处理的文件名                             |
| `instruction` | string | 是   | 脱敏指令，如：`涂黑身份证号`、`移除电话号码` |


## 配置

API key 应通过发布平台的 secret、environment variable 或 skill config 机制配置。推荐变量名为 `apiKey`，也兼容 `API_KEY` 和 `OPENCLAW_SKILL_API_KEY`。如果没有 API key，请先到 https://apiconsole.bestcoffer.com.cn/ 获取。

## 返回值

| 字段      | 类型   | 说明                                       |
| --------- | ------ | ------------------------------------------ |
| `taskUrl` | string | 查询链接，可在网页中查看处理进度和下载结果 |
| `errorMessage` | string | 错误信息，如果处理失败会返回具体错误描述 |

## 常见脱敏指令示例

- `涂黑身份证号`
- `移除电话号码`
- `模糊人脸区域`
- `隐藏银行卡号`
- `删除邮箱地址`

## 限制说明

- 仅支持单个文件处理
- 支持的文件格式：PDF、图片（PNG/JPG/JPEG）、Word、Excel、TXT
- 单文件大小限制：10MB
- 处理超时时间：5 分钟

## 最终回复模板

- 文件：`test.txt`
- 脱敏指令：`涂黑身份证号`
- 查询链接：`https://...`

打开查询链接可查看进度和下载结果。

