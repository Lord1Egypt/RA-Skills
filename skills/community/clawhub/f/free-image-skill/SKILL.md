---
name: free-image-skill
description: 免费图片解决方案 - 重要图片用OpenAI免费额度，其他用免费图库，自动去水印
version: 1.0.0
author: Titan Cheung
homepage: https://github.com/openclaw/openclaw
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🆓",
        "requires": { "bins": ["python3"] },
        "primaryEnv": "OPENAI_API_KEY",
        "install":
          [
            {
              "id": "python-deps",
              "kind": "pip",
              "packages": ["openai", "requests", "pillow"],
              "label": "安装Python依赖",
            },
          ],
      },
  }
---

# 🆓 免费图片解决方案Skill

**零成本搞定所有图片需求！**

## 核心策略

| 图片类型 | 解决方案 | 成本 |
|----------|----------|------|
| **重要图片** | OpenAI免费额度生成 | $0.00 |
| **普通配图** | 免费图库下载 | $0.00 |
| **水印处理** | 智能去除工具 | $0.00 |
| **批量优化** | 开源工具处理 | $0.00 |

## 快速开始

### 1. 安装
```bash
# 设置OpenAI免费额度API密钥
export OPENAI_API_KEY="你的免费额度密钥"

# 安装技能依赖
cd {baseDir}
pip3 install openai requests pillow --break-system-packages
```

### 2. 基本使用
```bash
# 为文章生成图片
python3 scripts/main.py --text "文章内容" --output ./images

# 只生成重要图片（用免费额度）
python3 scripts/main.py --important-only --count 3

# 只搜索免费图片
python3 scripts/main.py --free-only --keywords "科技,商务" --count 10
```

### 3. 完整工作流
```bash
# 一键完成所有步骤
./scripts/complete_workflow.sh \
  --input "文章.txt" \
  --output ./final_images \
  --budget 0
```

## 核心功能

### 1. 免费额度AI生成
```python
# 使用OpenAI免费额度
python3 scripts/ai_generator.py \
  --prompt "专业商务场景" \
  --count 2 \
  --budget 0.08  # 只用$0.08免费额度
```

**免费额度计算：**
- 新用户：$5-18免费额度
- 可生成：125-450张图片
- 建议：重要图片才用AI

### 2. 智能免费图库搜索
```python
# 从多个免费图库搜索
python3 scripts/free_search.py \
  --keywords "科技 创新" \
  --sources unsplash,pexels \
  --count 20 \
  --no-watermark
```

**支持图库：**
- ✅ Unsplash - 商业免费
- ✅ Pexels - 商业免费  
- ✅ Pixabay - 商业免费
- ⚠️ Freepik - 需署名

### 3. 一键去水印
```python
# 自动去除水印
python3 scripts/remove_watermark.py \
  --input ./watermarked \
  --output ./clean \
  --auto-detect
```

### 4. 批量优化
```bash
# 统一处理所有图片
./scripts/batch_process.sh \
  --resize 1200x800 \
  --quality 85 \
  --format webp
```

## 使用示例

### 场景1：博客文章配图
```bash
# 生成10张图片，只用免费资源
python3 scripts/main.py \
  --text "人工智能技术文章" \
  --count 10 \
  --ai-budget 0.12  # 只用$0.12免费额度
```

**结果：**
- 3张AI图片（重要图表）
- 7张免费图库图片
- 总成本：$0.00

### 场景2：商业报告
```bash
# 20页报告配图
python3 scripts/main.py \
  --type report \
  --pages 20 \
  --output ./report_images
```

### 场景3：社交媒体
```bash
# 小红书帖子配图
python3 scripts/main.py \
  --platform xiaohongshu \
  --posts 5 \
  --size 1080x1350
```

## 配置文件

`config/settings.json`:
```json
{
  "free_mode": true,
  "max_ai_cost": 0.0,
  "prefer_free_sources": true,
  "watermark_removal": "auto",
  "output_format": "webp",
  "default_size": "1200x800"
}
```

## 项目结构
```
free-image-skill/
├── SKILL.md
├── scripts/
│   ├── main.py              # 主入口
│   ├── ai_generator.py      # AI生成（免费额度）
│   ├── free_search.py       # 免费图库搜索
│   ├── watermark_remover.py # 去水印
│   └── batch_processor.py   # 批量处理
├── config/
│   ├── settings.json        # 配置
│   ├── sources.json         # 免费图库配置
│   └── prompts.json         # 提示词模板
└── examples/
    └── demo/                # 使用示例
```

## 注意事项

1. **免费额度有限**：先规划重要图片
2. **版权合规**：确认免费图库许可
3. **水印伦理**：只去除允许的水印
4. **质量平衡**：重要内容用AI，普通用免费图

## 故障排除

```bash
# 测试所有组件
./scripts/test_all.sh

# 检查免费额度
python3 scripts/check_quota.py

# 验证图库访问
python3 scripts/test_sources.py
```

---

**版本**: 1.0.0  
**原则**: 不花钱，免费办大事儿！  
**状态**: ✅ 就绪