# 模型选择说明

来源：硅基流动官方文档

## 主力模型：Pro/deepseek-ai/DeepSeek-V3

```
模型名：Pro/deepseek-ai/DeepSeek-V3
特点：
  - 支持图片和 PDF 输入（base64 或 URL）
  - 中文文档识别准确率极高
  - 支持专用 OCR prompt 格式（<image>\n<|grounding|>...）
  - 支持多图对比分析
适用：所有文档类型的首选模型
```

## 备用模型：Qwen2.5-VL-72B

```
模型名：Qwen/Qwen2.5-VL-72B-Instruct
特点：
  - 超大参数量，复杂文档理解力强
  - 支持图片输入（不支持 PDF base64）
  - 中英文双语文档效果好
适用：DeepSeek-OCR 效果不佳时的备选
```

## PaddleOCR-VL（专业 OCR 场景）

```
模型名：PaddlePaddle/PaddleOCR-VL
特点：
  - 专为 OCR 任务优化
  - 支持 CLI 和 API 两种调用方式
  - 对复杂版面（多列、表格）效果好
适用：需要精确版面还原的场景
```

## 图像输入计费（detail 参数影响）

```
detail=low：
  统一压缩为 448×448，约 256 token
  适合：文字较大、布局简单的文档

detail=high（推荐）：
  按实际像素计费：ceil(h/28) × ceil(w/28) token
  适合：字体较小、布局复杂、表格密集的文档

建议默认使用 detail=high，确保识别准确率
```

## 模型选择决策

```
发票/收据/证件        → DeepSeek-V3（中文场景最佳）
普通文档/报告         → DeepSeek-V3
复杂表格/多列版面     → DeepSeek-V3 或 PaddleOCR-VL
英文为主的文档        → Qwen2.5-VL-72B
DeepSeek 结果不满意  → 改用 Qwen2.5-VL-72B 重试
```
