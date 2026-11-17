# 可靠性策略

## 可靠性策略（快速失败 / 批量跳档 / 复核截图）

- **入口快速失败**：`cad_scan / read_cad / convert_dwg` 先跑 `scripts/cad_preflight.py` 的轻量预检
  （<5 秒，只读前 4KB，不调解析器）。空文件、<1KB、魔数不是 AC####/DXF-SECTION/%PDF 的头会立即标
  “快速失败”并跳过，不假装转换成功；DWG 版本不在支持列表时直接报“不支持的 DWG 版本”。
- **批量不中断**：`cad_batch.sh --out 台账` 对坏图/加密图/不支持版本逐图记录
  “缺口/失败原因”（`自检汇总.md` 与 `_state.json`），单图失败不影响其它图继续跑。
  - 加密 DWG（ezdwg 报 `encrypted/password`）记为“加密 DWG：需密码或人工解锁”。
  - 不支持版本记为“不支持的 DWG 版本”。
- **超时与内存看门狗**：单图沿用 `--budget` 阶段预算和 `--cap-mb` 内存闸；批量层对整条
  `cad_scan` 再加硬超时（超时 rc=124），退出码 -9/内存闸关键词被翻译成“内存看门狗终止”，原因写入台账。
- **PDF 复核截图**：`cad_pdf_ocr.sh --out-dir 输出` 自动把可疑页面截图写到
  `输出/_review/<图名>-p<页码>.png`，并写 `_review/index.json`（每页原因 + 图片相对路径）。
  - 触发条件：OCR 失败页、扫描页 OCR 无有效文字、整页平均置信 <60%、出现单行置信 <40% 的低置信区块。
  - 截图对应的候选项带 `review_image` 字段；`--no-review` 可关闭截图输出。
- 以上改动保持 `cad-file-reader/v0` 契约不变，`scripts/cad_validate.sh` 校验仍需通过。
