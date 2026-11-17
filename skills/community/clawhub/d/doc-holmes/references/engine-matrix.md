# 引擎矩阵与版本边界（doc-holmes）

> 立场：本 skill 是自有 MIT 胶水层；AGPL 引擎只以**子进程**调用其官方 CLI，零 vendor、零改源。引擎升级必须重跑回归集后才随版发布。

## 主路径引擎

| 组件 | 版本基线 | 说明 |
|---|---|---|
| pdf2zh-next | ≥2.9（2026-05-15 起，BabelDOC IR 后端） | 官方 CLI `pdf2zh_next`；v2.0 正式版（2026-09-08）同线。锁 minor 升级需回归 |
| BabelDOC | pdf2zh-next 内置 | IR 论文 arXiv:2605.10845，**已正式发表于 ACL 2026**（稳定性背书）；DocLayout-YOLO ONNX 版面分析 |
| PyMuPDF | ≥1.24 | triage / OCR 栅格化 / 说明页插入；pip 依赖唯一 |

## 翻译端点

| 端点 / 模型 | 用途 | 状态（2026-09-20 真网实测） |
|---|---|---|
| `https://open.bigmodel.cn/api/paas/v4` + `glm-4.5-flash`（**面向用户的推荐默认**） | 智谱开放平台官方 API（用户自己的 key） | 官方合法通道；flash 档免费 |
| `https://open.bigmodel.cn/api/coding/paas/v4` + `glm-5.3-flash` 等 | **仅限开发者自用**（Coding Plan 订阅） | ✅ 实测可用，但**分发默认禁止**：订阅仅限编码工具，第三方翻译接入违反 ToS 有封号风险（配置层默认拒绝，`DOC_HOLMES_ALLOW_CODING_ENDPOINT=1` 显式解锁） |
| 同端点 + `glm-4.6` / `glm-4.7` / `glm-4.5-flash` | 旧代兜底 | ✅ 200；`glm-4.7-flash` 曾瞬时超时（HTTP 000），复测 200，遇超时先重试 |
| `https://opencode.ai/zen/go/v1` + `deepseek-v4-flash` | **多厂商实测**（OpenCode Go 套餐） | ✅ 3s 出干净译文；Go 端点需 `x-opencode-session` 头（由调用方配置，本 skill 直连标准 OpenAI 兼容 API 时无需） |
| 同上 + `kimi-k2.6` 等 reasoning 系 | ⚠️ 不推荐做翻译引擎 | 推理 token 挤占输出预算（content 为空）；翻译选非 reasoning 模型 |
| SiliconFlow 等 OpenAI 兼容端点 | 备用 | 直接配置即可，不拦 |

> **模型选型口径**：翻译质量对决用固定医学段落（利妥昔单抗/ITP），对比术语准确度与流畅度；
> 默认取"最新一代 flash 层级"，`DOC_HOLMES_MODEL` 一行即可换。注意用量：Go 等套餐测试只用
> 短段落 × 单次，不跑批量。

## OCR 通道（C 级，实验性）

| 通道 | 要求 | 状态 |
|---|---|---|
| Tesseract | `apt install tesseract-ocr`（中文加 `tesseract-ocr-chi-sim`） | ✅ 已接入（能力探测，缺语言包给安装指引） |
| PP-Structure（GPU A5000，锁 paddleocr 2.9.1） | CUDA 11.8+cuDNN 8.9 | 计划中（82 服务器，后续版本评估） |
| GLM-OCR 0.9B（OmniDocBench 94.62） | transformers + 显存 | 计划中（后续版本评估） |

## 硬件参考（2026-09-20 WSL 实测）

- RTX 3070 Laptop 8GB：DocLayout-YOLO ONNX 可跑；无 GPU 时 CPU 版面分析可用（慢 3-8 倍）。
- 16 线程 CPU / 15GB 内存：批量 `--workers ≤4` 安全上限（超过会拖垮宿主机，runner 已硬编码拒绝）。

## 已知边界

1. `pdf2zh_next` 无 `--no-config-file` 参数（那是 pdf2zh 3.x 的）；配置自动落盘属引擎行为，与本 skill 无冲突。
2. 产物命名 `<stem>.<watermark_mode>.<lang>.dual/mono.pdf`，产物发现按 stem 前缀 + mtime 最新。
3. 引擎会自动抽取术语表 `*.glossary.csv`，当前版本不注入自定义术语（后续版本计划：医学词汇表走 `--glossaries`）。
4. `--no-dual/--no-mono` 可关掉对应产物；audit 的产物发现随之可能为空，属正常。
