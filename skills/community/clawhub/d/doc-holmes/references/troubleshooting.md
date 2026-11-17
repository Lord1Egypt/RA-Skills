# 故障排查（doc-holmes 实锤坑清单）

> 每条都是真实撞过的墙；按"现象 → 原因 → 解法"组织。分区编号，引用时带区名（如"端点 #2"）。

## 安装与环境

1. **selfcheck 找不到引擎**
   现象：`未找到 pdf2zh_next 引擎`。
   解法：`uv tool install --python 3.12 pdf2zh-next`（推荐，入 `~/.local/bin`）或 `pip install pdf2zh-next`；仍找不到就 `export DOC_HOLMES_PDF2ZH_BIN=$(which pdf2zh_next)`。
2. **Python 版本**
   引擎要求 3.10-3.13；系统 3.10 可用，用 uv 建 3.12 venv 最省事。
3. **配置了 key 还是报缺 key**
   配置读取顺序：环境变量 > `~/.config/doc-holmes/env` > 默认。检查文件权限（建议仅本人可读）与行格式 `KEY=value`（不支持 export 前缀）。

## 端点

1. **Coding 订阅端点要求确认**
   现象：`检测到 GLM Coding Plan 订阅端点…不享套餐额度，按量扣除账户余额`。
   说明：这是计费知情确认（依据智谱官方 FAQ：套餐仅限指定编码工具，其他工具调用按量扣余额；多人共用订阅会被限制权益），不是故障。推荐官方开放平台 `https://open.bigmodel.cn/api/paas/v4`（glm-4.5-flash 免费）。确认知晓仍要用订阅：设 `DOC_HOLMES_ALLOW_CODING_ENDPOINT=1`（写 env 文件永久生效）。
2. **429 / 限流**
   默认 `--qps 4` 已保守；仍 429 就降到 2-3。引擎对 429 自动退避，无需重跑整个批次（续传会跳过已成功的）。
3. **模型超时（HTTP 000）或报"模型不存在"（code 1211）**
   先重试一次（实测 `glm-4.7-flash` 曾瞬时超时、复测恢复）；仍失败就换模型：`export DOC_HOLMES_MODEL=glm-4.5-flash`（默认，官方开放平台免费档）。模型名以端点商文档为准，拼错会返回 code 1211。

## 翻译质量

1. **扫描件译文质量差**
   C 级本来就是预览质量（OCR 错字会进译文）。正式用途请找原生 PDF；A/B 级才承诺保真。
2. **公式显示异常**
   引擎按"公式保护"处理（formular font/char pattern）；个别字体嵌入缺失的 PDF 会退化。先用 `--pages 1-3` 试翻确认，再全量。
3. **大文档在"自动术语抽取"或大段落上超时**
   现象：`Request timed out` / 卡在 Automatic Term Extraction。
   说明：术语抽取会把大块原文塞进单个巨型提示；超密页（单页 8000+ 字符，如 STTT 综述）大段落响应也慢。
   解法：`--no-glossary` 跳过术语抽取（术语一致性略降）+ `DOC_HOLMES_OPENAI_TIMEOUT=600`；仍重则 `--pages` 分段。
4. **水印/页眉被翻译了**
   跳翻规则用于体检报告与 OCR 通路；引擎通路的水印行由引擎自带清理处理，个别残留会记进 B 级噪声报告。深度修复不做（redaction 实测会摧毁重叠字形）；改为 span 级精确检测、计数与样本入审计。

## OCR 通道

1. **`tesseract 缺少语言包 zz`**
   `apt install tesseract-ocr-<lang>`（中文 `tesseract-ocr-chi-sim`）；或 `--ocr-lang` 选已装语言。查看已有语言：`tesseract --list-langs`。
2. **不想让扫描件走 OCR**
   `--ocr off`：C 级文件会被明确拒绝并给出指引，而不是硬翻一份烂的。

## 运行环境

1. **中文/空格路径**
   内部全程 realpath + UTF-8，Windows 下 WSL 挂载路径（/mnt/…）已验证；Windows 原生路径建议用短路径或引号包裹。
2. **批量中断后重跑会不会重复扣配额**
   不会。续传跳过 `status=success` 且产物仍在的文件；只有失败/超时的会重试。
3. **WSL 里 nvidia-smi 正常但引擎用不上 GPU**
   DocLayout-YOLO 走 ONNX，CPU 也能跑（慢 3-8 倍）。GPU 加速属引擎内配置，本 skill 不干预；批量时用 `--workers 2` 和 `--qps 4` 把端点与版面分析错开。
