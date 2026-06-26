# 虚拟试衣工作流详解

## 概述

虚拟试衣是 ChaoJi AI 的核心能力之一，支持将服装图片快速穿到模特身上，生成逼真的上身效果。

## 工作流程

### 1. 输入准备

**服装图片要求**：
- 清晰的服装正面图
- 背景简洁（纯色最佳）
- 光线均匀，无明显阴影
- 建议分辨率：800x800 以上
- 支持格式：JPG, PNG

**模特图片要求**：
- 清晰的人像照片
- 姿势自然，身体完整可见
- 避免遮挡躯干
- 建议分辨率：800x1200 以上
- 支持格式：JPG, PNG

### 2. 输入处理

支持三种输入格式：

**本地文件**：
```python
cloth_input = "/path/to/cloth.jpg"
human_input = "/path/to/model.jpg"
# 自动上传到 OSS，获取 OSS Path
```

**URL**：
```python
cloth_input = "https://example.com/cloth.jpg"
human_input = "https://example.com/model.jpg"
# 提取 OSS Path 或直接使用
```

**OSS Path**：
```python
cloth_input = "marketing/image/1/xxx/cloth.jpg"
human_input = "marketing/image/1/xxx/model.jpg"
# 直接使用
```

### 3. 参数配置

**基本参数**：
- `cloth_length`: 上身区域
  - `upper`: 上装（T 恤、衬衫等）
  - `lower`: 下装（裤子、裙子等）
  - `overall`: 全身（连衣裙、外套等）

- `batch_size`: 生成数量（1-8）
  - 快速预览：1
  - 选择最佳：4
  - A/B 测试：8

- `dpi`: 输出 DPI
  - 网络使用：72-150
  - 打印使用：300
  - 高质量打印：600

- `output_format`: 输出格式
  - `jpg`: 适合照片，文件较小
  - `png`: 适合透明背景，无损

### 4. API 调用

使用统一执行器：
```bash
python chaoji-tools/scripts/run_command.py \
  --command model_tryon_quick \
  --input-json '{
    "image_cloth": "marketing/image/cloth.jpg",
    "list_images_human": ["marketing/image/model.jpg"],
    "cloth_length": "overall",
    "batch_size": 4
  }'
```

### 5. 结果处理

**成功响应**：
```json
{
  "ok": true,
  "command": "model_tryon_quick",
  "task_id": "1234567890",
  "media_urls": [
    "https://oss.chaoji.com/output/result1.jpg",
    "https://oss.chaoji.com/output/result2.jpg"
  ],
  "outputs": [
    {
      "workOutputUrl": "https://oss.chaoji.com/output/result1.jpg",
      "localPath": "/home/user/.openclaw/media/outbound/result1.jpg"
    }
  ]
}
```

**失败响应**：
```json
{
  "ok": false,
  "error_type": "INPUT_ERROR",
  "error_code": "INPUT_002",
  "error_name": "缺少必填参数",
  "user_hint": "命令 'model_tryon_quick' 缺少必填参数：image_cloth",
  "next_action": "请补充缺失的参数后重试"
}
```

## 最佳实践

### 场景 1：电商快速上架

**需求**：快速生成服装上身效果，用于商品详情页

**配置**：
```python
{
  "cloth_length": "overall",
  "batch_size": 1,
  "dpi": 150,
  "format": "jpg"
}
```

**理由**：
- 单张生成，速度最快
- 中等 DPI，适合网页展示
- JPG 格式，文件小，加载快

### 场景 2：营销海报制作

**需求**：高质量上身效果，用于海报和广告

**配置**：
```python
{
  "cloth_length": "overall",
  "batch_size": 4,
  "dpi": 300,
  "format": "png"
}
```

**理由**：
- 多张生成，选择最佳
- 高 DPI，适合打印
- PNG 格式，无损质量

### 场景 3：A/B 测试

**需求**：测试不同模特、不同服装的转化效果

**配置**：
```python
{
  "cloth_length": "upper",
  "batch_size": 8,
  "dpi": 150,
  "format": "jpg"
}
```

**理由**：
- 最大批量，一次生成 8 张
- 中等 DPI，适合在线测试
- 多模特多服装组合

## 常见问题

### Q1: 生成效果不自然怎么办？

**可能原因**：
1. 服装图片不清晰或有褶皱
2. 模特姿势过于复杂
3. 服装和模特体型不匹配

**解决方案**：
- 使用更清晰的服装图片
- 选择姿势简单的模特图
- 调整服装尺寸或选择合适体型的模特

### Q2: 生成速度慢怎么办？

**优化建议**：
1. 减小 `batch_size`（如从 4 改为 1）
2. 降低 `dpi`（如从 300 改为 150）
3. 避免高峰期调用

### Q3: 如何处理批量试衣？

**方案 1：使用 batch_size 参数**
```python
{
  "cloth_input": "cloth.jpg",
  "human_input": ["model1.jpg", "model2.jpg", "model3.jpg"],
  "batch_size": 3
}
```

**方案 2：循环调用**
```python
for model in models:
    result = tryon(cloth, model)
```

### Q4: 如何保存用户偏好？

**Project Mode**：
创建 `~/.openclaw/workspace/chaoji/PREFERENCE.md`：
```markdown
# 试衣偏好

## 常用参数
- cloth_length: overall
- batch_size: 4
- dpi: 300

## 偏好模特
- model_001: marketing/models/female_001.jpg
- model_002: marketing/models/male_001.jpg

## 历史成功案例
- 2024-01-15: 连衣裙试衣，使用 model_001，效果优秀
```

## 性能指标

**响应时间**：
- 单张生成：10-30 秒
- 批量生成（8 张）：60-120 秒

**成功率**：
- 标准输入：>95%
- 复杂姿势：>85%
- 低质量输入：>70%

**并发限制**：
- 单账户并发数：5
- 日配额：根据账户等级

## 相关资源

- [API 文档](https://open.chaoji.com/docs/tryon)
