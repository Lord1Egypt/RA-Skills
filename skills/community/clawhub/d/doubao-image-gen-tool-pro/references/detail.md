# 详细参考 - doubao-image-gen-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (yaml)

```yaml
batch:
  parallel_workers: 8              # 并行生成数
  max_retries: 3                    # 失败重试次数
  retry_delay: 5                    # 重试间隔（秒）
  queue_file: /tmp/generate-queue.json

generation:
  default_ratio: "3:4"              # 默认比例
  supported_ratios:                # 支持的比例
    - "3:4"
    - "1:1"
    - "4:3"
    - "16:9"
    - "9:16"
    - "2:3"
  candidates_per_item: 4            # 每项候选图数量
  auto_select: false                # 自动选择最佳（false 则人工选择）
prompt:
  enhance: true                     # 启用提示词增强
  enhance_model: "advanced"         # 增强模型版本
  auto_negative: true               # 自动生成负面提示词
  language: "zh"                    # 提示词语言
style:
  preset_directory: /config/styles/  # 风格预设目录
  default_preset: "general"         # 默认预设
  brand_consistency: true           # 品牌一致性检查
reference:
  enabled: false                    # 启用参考图
  preserve_style: true              # 保留参考图风格
  style_strength: 0.8               # 风格强度（0-1）
quality:
  check: true                       # 质量评估
  min_score: 0.7                    # 最低质量分
  auto_retry_low_quality: true      # 低质量自动重试
archive:
  enabled: true                     # 自动归档
  directory: /images/archive/       # 归档目录
  naming: "{id}_{ratio}_{timestamp}"  # 命名规则
  organize_by: "project"            # 按项目组织
report:
  enabled: true
  output: /tmp/reports/generate-report.json
  include_thumbnails: true          # 包含缩略图
  include_metadata: true            # 包含元数据
```

## 代码示例 (json)

```json
{
  "project": "电商商品图批量生成",
  "output_dir": "/images/products/",
  "items": [
    {
      "id": "product-001",
      "prompt": "白色 T 恤 俯拍 简约背景",
      "ratios": ["3:4", "1:1"],
      "style_preset": "ecommerce-clean"
    },
    {
      "id": "product-002",
      "prompt": "蓝色牛仔裤 平铺 电商风格",
      "ratios": ["3:4", "1:1"],
      "style_preset": "ecommerce-clean"
    }
  ],
  "options": {
    "enhance_prompt": true,
    "auto_archive": true,
    "quality_check": true
  }
}
```

## 代码示例 (json)

```json
{
  "name": "ecommerce-clean",
  "description": "电商简约风格",
  "style_keywords": [
    "简约背景",
    "柔光照明",
    "商品居中",
    "高质感",
    "电商摄影风格"
  ],
  "negative_keywords": [
    "复杂背景",
    "低质感",
    "模糊"
  ],
  "default_ratio": "3:4",
  "quality": "high"
}
```

## 代码示例 (json)

```json
{
  "templates": [
    {
      "id": "product-display",
      "name": "商品展示图",
      "template": "{product} 俯拍 简约背景 柔光 电商风格",
      "variables": ["product"]
    },
    {
      "id": "scene-design",
      "name": "场景设计图",
      "template": "{scene} {style} {lighting} {mood}",
      "variables": ["scene", "style", "lighting", "mood"]
    }
  ]
}
```

## 代码示例 (json)

```json
{
  "project": "品牌营销素材",
  "style_preset": "/config/brand-style.json",
  "items": [
    {"prompt": "产品宣传图 - 手机展示"},
    {"prompt": "产品宣传图 - 笔记本展示"},
    {"prompt": "产品宣传图 - 平板展示"}
  ],
  "options": {
    "ratios": ["3:4", "16:9"],
    "enhance_prompt": true,
    "auto_archive": true
  }
}
```

### 场景 1：电商商品图批量生成
某电商商家需要为 50 个商品生成展示图，每个商品需要 3:4 与 1:1 两种比例。

**批量配置 `batch-generate.json`：**

```json
{
  "project": "电商商品图批量生成",
  "output_dir": "/images/products/",
  "items": [
    {
      "id": "product-001",
      "prompt": "白色 T 恤 俯拍 简约背景",
      "ratios": ["3:4", "1:1"],
      "style_preset": "ecommerce-clean"
    },
    {
      "id": "product-002",
      "prompt": "蓝色牛仔裤 平铺 电商风格",
      "ratios": ["3:4", "1:1"],
      "style_preset": "ecommerce-clean"
    }
  ],
  "options": {
    "enhance_prompt": true,
    "auto_archive": true,
    "quality_check": true
  }
}
```

**执行命令：**

```bash
python3 batch_generate.py --config /path/to/batch-generate.json --parallel 8
```

**输出结构：**

```text
/images/products/
├── product-001/
│   ├── 3-4/
│   │   ├── candidate-1.png
│   │   ├── candidate-2.png
│   │   └── selected.png
│   └── 1-1/
│       └── selected.png
├── product-002/
│   └── ...
└── batch-report.json   # 批量生成报告
```



