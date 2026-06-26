name: 表情包生成器
version: "1.0.0"
description: "$desc"
license: MIT-0
tags:
  - tools


# 表情包生成器


生成趣味表情包图片，支持文字叠加和AI生成两种模式。

## 功能

- **文字模式**：在预设表情包模板上叠加文字（Top/Bottom Text）
- **AI模式**：使用Pollinations AI生成指定主题的表情包图片

## 使用方法

```bash
python3 cn_meme_generator.py --mode text --top "我太难了" --bottom "真的"
python3 cn_meme_generator.py --mode ai --prompt "加班到深夜的程序员"
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | 模式：text/ai | text |
| `--top` | 顶部文字 | 空 |
| `--bottom` | 底部文字 | 空 |
| `--prompt` | AI生成提示词 | 空 |
| `--output` | 输出路径 | meme_output.png |

## 依赖

- Python 3.x
- Pillow (pip install Pillow)
- requests (pip install requests)

## 使用说明

### 文字模式

1. 输入顶部文字（可选）
2. 输入底部文字（可选）
3. 选择背景颜色或渐变
4. 生成带文字的表情包图片

### AI模式

1. 输入描述提示词
2. 使用Pollinations免费API生成图片
3. 图片自动保存

## 示例

```bash
# 生成"打工人的周一"表情包
python3 cn_meme_generator.py --mode text --top "周一" --bottom "不想上班"

# AI生成深夜加班表情包
python3 cn_meme_generator.py --mode ai --prompt "深夜加班的程序员崩溃表情"
```

## 注意事项

- 文字模式无需联网
- AI模式使用Pollinations免费API，无API Key要求
- 生成图片为PNG格式，透明背景
- 文字自动换行，超长文字自动缩放

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
