# 免费图片解决方案 - 使用示例

## 示例1：为技术博客配图

### 文章内容
"人工智能在医疗诊断中的应用正在改变传统医疗方式。通过深度学习算法，AI可以分析医学影像，辅助医生做出更准确的诊断。"

### 执行命令
```bash
# 进入技能目录
cd /Users/titan/.openclaw/workspace/free-image-skill

# 设置API密钥（使用免费额度）
export OPENAI_API_KEY="你的免费额度密钥"

# 生成图片
python3 scripts/main.py \
  --text "人工智能在医疗诊断中的应用正在改变传统医疗方式" \
  --count 8 \
  --output ./examples/demo/blog_images
```

### 预期结果
```
🆓 免费图片解决方案
============================================================
🔍 免费图片资源:
  • Unsplash: 商业免费，高质量
    链接: https://unsplash.com
  • Pexels: 商业免费，照片视频
    链接: https://www.pexels.com
  • Pixabay: 商业免费，矢量插画
    链接: https://pixabay.com
  • Freepik: 需署名，有免费选项
    链接: https://www.freepik.com

📋 执行计划:
  🎨 AI生成（重要图片）: 2张
    成本: $0.08（用免费额度）
  📷 免费图库: 6张
    关键词: 自动从文本提取
    成本: $0.00
  💰 总成本: $0.08（完全用免费额度）
```

## 示例2：只生成重要图片（用免费额度）

```bash
# 只使用AI生成重要图片
python3 scripts/ai_generator.py \
  --prompt "人工智能医疗诊断系统界面，医生使用AI分析医疗影像" \
  --count 3 \
  --output ./examples/demo/important_images
```

## 示例3：只搜索免费图片

```bash
# 只从免费图库搜索
python3 scripts/free_search.py \
  --keywords "医疗,科技,AI,诊断" \
  --count 15 \
  --output ./examples/demo/free_images
```

## 示例4：去除水印

```bash
# 假设下载的图片有水印
python3 scripts/watermark_remover.py \
  --input ./examples/demo/free_images \
  --output ./examples/demo/clean_images \
  --auto-detect
```

## 示例5：批量处理

```bash
# 批量优化所有图片
python3 scripts/batch_processor.py \
  --input ./examples/demo/clean_images \
  --output ./examples/demo/final_images \
  --resize 1200x800 \
  --optimize 85 \
  --convert webp
```

## 完整工作流脚本

创建 `complete_workflow.sh`:

```bash
#!/bin/bash
# 完整免费图片工作流

set -e

echo "🆓 开始免费图片工作流..."

# 1. 设置环境
export OPENAI_API_KEY="你的免费额度密钥"

# 2. 生成重要图片（用免费额度）
echo "🎨 生成重要图片..."
python3 scripts/ai_generator.py \
  --prompt "$1" \
  --count 2 \
  --output ./workflow/ai

# 3. 搜索免费图片
echo "🔍 搜索免费图片..."
python3 scripts/free_search.py \
  --keywords "$2" \
  --count 10 \
  --output ./workflow/free

# 4. 去除水印
echo "✨ 去除水印..."
python3 scripts/watermark_remover.py \
  --input ./workflow/free \
  --output ./workflow/clean \
  --auto-detect

# 5. 批量处理
echo "⚡ 批量处理..."
python3 scripts/batch_processor.py \
  --input ./workflow \
  --output ./workflow/final \
  --all

echo "✅ 工作流完成！"
echo "   输出目录: ./workflow/final"
```

使用：
```bash
chmod +x complete_workflow.sh
./complete_workflow.sh "人工智能医疗诊断" "医疗,科技,AI"
```

## 成本分析

### 场景：10张图片的博客文章
- **AI生成**：3张重要图片 × $0.04 = $0.12
- **免费图库**：7张图片 × $0.00 = $0.00
- **总成本**：$0.12（完全用免费额度）

### 免费额度使用规划
- 新用户：$5免费额度
- 可生成：125张标准图片
- 建议分配：
  - 30张重要图片（封面、图表）
  - 95张用免费图库
  - **总图片**：125张
  - **总成本**：$0.00

## 最佳实践

### 1. 最大化免费额度
```bash
# 先规划重要图片
python3 scripts/main.py --plan-only --text "你的长文章"

# 只对关键内容使用AI
python3 scripts/ai_generator.py --prompt "最重要的场景"
```

### 2. 智能关键词提取
```python
# 从文本自动提取
keywords = extract_keywords(article_text, count=10)
```

### 3. 批量操作节省时间
```bash
# 一次性处理所有图片
./scripts/batch_processor.py --all --input ./images
```

### 4. 质量检查
```bash
# 检查图片质量
find ./final_images -name "*.webp" -exec identify {} \;
```

## 故障排除

### 问题：API密钥无效
```bash
# 检查密钥
echo $OPENAI_API_KEY

# 测试连接
python3 -c "import openai; print('✅ OpenAI可用')"
```

### 问题：免费图库访问失败
```bash
# 检查网络
curl -I https://unsplash.com

# 尝试其他图库
python3 scripts/free_search.py --sources pexels,pixabay
```

### 问题：水印去除效果差
```bash
# 尝试不同方法
python3 scripts/watermark_remover.py --method inpaint
```

## 扩展使用

### 集成到内容创作流程
```bash
# 1. 写文章
# 2. 自动配图
python3 scripts/main.py --text "$(cat article.md)" --output ./article_images
# 3. 发布
```

### 定期更新图片库
```bash
# 每周搜索新图片
python3 scripts/free_search.py --keywords "最新趋势" --count 20
```

---

**原则**：不花钱，免费办大事儿！