# ai-image-cli 使用示例

## 基础示例

### 文生图 (text2img)

```bash
# 简单生成
ai-image text2img "一个中国女孩,高清"

# 指定尺寸
ai-image text2img "夕阳下的海滩,唯美,高清" --size 1920x1920

# 使用随机种子（可复现）
ai-image text2img "雪山风景,壮丽" --seed 12345

# 调整引导系数
ai-image text2img "城市夜景,霓虹灯" --guidance-scale 3.5

# 添加水印
ai-image text2img "森林中的小木屋,童话风格" --watermark

# 完整参数
ai-image text2img "科幻城市,未来感,高清" \
    --size 1920x1920 \
    --seed 999 \
    --guidance-scale 3.0 \
    --watermark
```

### 图生图 (img2img)

```bash
# 基本用法
ai-image img2img "改成爱心形状的泡泡" https://example.com/bubbles.jpg

# 修改颜色
ai-image img2img "改变颜色为红色" https://example.com/car.jpg

# 风格转换
ai-image img2img "转为水彩画风格" https://example.com/photo.png

# 背景替换
ai-image img2img "替换背景为蓝天白云" https://example.com/portrait.jpg

# 使用随机种子
ai-image img2img "添加一只小猫" https://example.com/room.jpg --seed 777

# 调整引导系数（增强编辑强度）
ai-image img2img "转为油画风格" https://example.com/landscape.png --guidance-scale 7.0

# 完整参数
ai-image img2img "添加雪花效果" https://example.com/winter.jpg \
    --seed 888 \
    --guidance-scale 6.0 \
    --watermark
```

## 高级示例

### 模式 1：批量生成图片

使用相同提示词生成多张不同的图片（通过不同的种子）。

```bash
#!/bin/bash
# batch-generate.sh — 批量生成图片

PROMPT="${1:?用法: $0 <描述> [数量]}"
COUNT="${2:-5}"
OUTPUT_DIR="./output-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$OUTPUT_DIR"

echo "=== 批量生成: $PROMPT ==="
echo "数量: $COUNT"
echo "输出目录: $OUTPUT_DIR"
echo ""

for i in $(seq 1 $COUNT); do
    SEED=$((RANDOM * 100 + i))
    echo "[$i/$COUNT] 种子: $SEED"

    RESULT=$(ai-image text2img "$PROMPT" --seed $SEED)
    SUCCESS=$(echo "$RESULT" | jq -r '.success')

    if [ "$SUCCESS" = "true" ]; then
        URL=$(echo "$RESULT" | jq -r '.data.data[0].url')
        echo "  生成成功: $URL"
        echo "$URL" >> "$OUTPUT_DIR/urls.txt"
        echo "$RESULT" > "$OUTPUT_DIR/result-${i}.json"
    else
        ERROR=$(echo "$RESULT" | jq -r '.error')
        echo "  生成失败: $ERROR"
    fi

    # 避免请求过快
    [ $i -lt $COUNT ] && sleep 2
done

echo ""
echo "=== 完成 ==="
echo "结果保存在: $OUTPUT_DIR/"
```

使用示例：
```bash
bash batch-generate.sh "一只可爱的小猫" 5
```

### 模式 2：图片风格转换矩阵

对同一张图片应用多种风格。

```bash
#!/bin/bash
# style-matrix.sh — 风格转换矩阵

IMAGE_URL="${1:?用法: $0 <图片URL>}"
OUTPUT_DIR="./styles-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$OUTPUT_DIR"

STYLES=(
    "转为水彩画风格"
    "转为油画风格"
    "转为卡通动漫风格"
    "转为素描风格"
    "转为像素艺术风格"
)

echo "=== 风格转换矩阵 ==="
echo "源图片: $IMAGE_URL"
echo "输出目录: $OUTPUT_DIR"
echo ""

for i in "${!STYLES[@]}"; do
    STYLE="${STYLES[$i]}"
    IDX=$((i + 1))

    echo "[$IDX/${#STYLES[@]}] $STYLE"

    RESULT=$(ai-image img2img "$STYLE" "$IMAGE_URL" --seed $((i * 100)))
    SUCCESS=$(echo "$RESULT" | jq -r '.success')

    if [ "$SUCCESS" = "true" ]; then
        URL=$(echo "$RESULT" | jq -r '.data.data[0].url')
        echo "  成功: $URL"
        echo "$URL" >> "$OUTPUT_DIR/urls.txt"
        echo "$STYLE|$URL" >> "$OUTPUT_DIR/index.txt"
    else
        ERROR=$(echo "$RESULT" | jq -r '.error')
        echo "  失败: $ERROR"
    fi

    sleep 2
done

echo ""
echo "=== 完成 ==="
cat "$OUTPUT_DIR/index.txt"
```

### 模式 3：参数对比实验

比较不同 guidance_scale 值的效果。

```bash
#!/bin/bash
# guidance-comparison.sh — 引导系数对比

PROMPT="${1:?用法: $0 <描述>}"
SEED="${2:-12345}"
OUTPUT_DIR="./guidance-test-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$OUTPUT_DIR"

# 文生图的推荐范围：2.0-4.0
GUIDANCE_SCALES=(2.0 2.5 3.0 3.5 4.0)

echo "=== 引导系数对比实验 ==="
echo "提示词: $PROMPT"
echo "固定种子: $SEED"
echo "输出目录: $OUTPUT_DIR"
echo ""

for scale in "${GUIDANCE_SCALES[@]}"; do
    echo "测试 guidance_scale=$scale"

    RESULT=$(ai-image text2img "$PROMPT" --seed $SEED --guidance-scale $scale)
    SUCCESS=$(echo "$RESULT" | jq -r '.success')

    if [ "$SUCCESS" = "true" ]; then
        URL=$(echo "$RESULT" | jq -r '.data.data[0].url')
        echo "  成功: $URL"
        echo "$scale|$URL" >> "$OUTPUT_DIR/comparison.txt"
    else
        ERROR=$(echo "$RESULT" | jq -r '.error')
        echo "  失败: $ERROR"
    fi

    sleep 2
done

echo ""
echo "=== 对比结果 ==="
cat "$OUTPUT_DIR/comparison.txt"
```

## 集成示例

### 与 jq 配合处理 JSON

```bash
# 提取图片 URL
ai-image text2img "一只狗" | jq -r '.data.data[0].url'

# 检查是否成功
RESULT=$(ai-image text2img "风景")
if [ "$(echo "$RESULT" | jq -r '.success')" = "true" ]; then
    echo "生成成功"
fi

# 提取模型信息
ai-image text2img "测试" | jq -r '.data.model'

# 提取 usage 信息
ai-image text2img "测试" | jq '.data.usage'

# 格式化为 Markdown
ai-image text2img "示例图片" | \
    jq -r '"![Image](" + .data.data[0].url + ")"'
```

### 下载生成的图片

```bash
#!/bin/bash
# generate-and-download.sh — 生成并下载图片

PROMPT="$1"
OUTPUT_FILE="${2:-output.jpg}"

echo "生成图片: $PROMPT"

RESULT=$(ai-image text2img "$PROMPT")
SUCCESS=$(echo "$RESULT" | jq -r '.success')

if [ "$SUCCESS" = "true" ]; then
    URL=$(echo "$RESULT" | jq -r '.data.data[0].url')
    echo "图片 URL: $URL"

    echo "下载中..."
    curl -s "$URL" -o "$OUTPUT_FILE"

    if [ -f "$OUTPUT_FILE" ]; then
        echo "已保存到: $OUTPUT_FILE"
        ls -lh "$OUTPUT_FILE"
    else
        echo "下载失败"
        exit 1
    fi
else
    ERROR=$(echo "$RESULT" | jq -r '.error')
    echo "生成失败: $ERROR"
    exit 1
fi
```

使用示例：
```bash
bash generate-and-download.sh "一只猫" cat.jpg
```

### CI/CD 集成 — 自动化设计资源生成

```yaml
# .github/workflows/generate-assets.yml
name: Generate Design Assets

on:
  workflow_dispatch:
    inputs:
      prompts:
        description: '提示词列表（逗号分隔）'
        required: true
        default: 'logo设计,banner背景,图标素材'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Install ai-image-cli
        run: |
          pip install ai-image-cli \
            -i http://music-pypi.hz.netease.com/simple \
            --trusted-host music-pypi.hz.netease.com

      - name: Generate images
        env:
          LANGBASE_TOKEN: ${{ secrets.LANGBASE_TOKEN }}
        run: |
          mkdir -p output
          IFS=',' read -ra PROMPTS <<< "${{ github.event.inputs.prompts }}"
          for prompt in "${PROMPTS[@]}"; do
            echo "生成: $prompt"
            ai-image text2img "$prompt" --watermark > "output/${prompt//[ \/]/_}.json"
            sleep 3
          done

      - name: Extract URLs
        run: |
          cd output
          for file in *.json; do
            URL=$(jq -r '.data.data[0].url' "$file")
            echo "$file: $URL" >> urls.txt
          done

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: generated-images
          path: output/
```

### 与 Python 脚本集成

```python
#!/usr/bin/env python3
# generate_image.py — Python 集成示例

import json
import subprocess
import sys
from pathlib import Path

def generate_image(prompt: str, **kwargs) -> dict:
    """调用 ai-image text2img 生成图片"""
    cmd = ["ai-image", "text2img", prompt]

    if "size" in kwargs:
        cmd.extend(["--size", kwargs["size"]])
    if "seed" in kwargs:
        cmd.extend(["--seed", str(kwargs["seed"])])
    if "guidance_scale" in kwargs:
        cmd.extend(["--guidance-scale", str(kwargs["guidance_scale"])])
    if kwargs.get("watermark"):
        cmd.append("--watermark")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"错误: {e.stderr}", file=sys.stderr)
        return {"success": False, "error": e.stderr}

def main():
    prompts = [
        "一只可爱的小猫",
        "夕阳下的海滩",
        "科幻城市"
    ]

    output_dir = Path("./generated")
    output_dir.mkdir(exist_ok=True)

    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] 生成: {prompt}")

        result = generate_image(
            prompt,
            seed=i * 100,
            guidance_scale=2.5
        )

        if result["success"]:
            url = result["data"]["data"][0]["url"]
            print(f"  成功: {url}")

            # 保存结果
            output_file = output_dir / f"{i:02d}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            print(f"  失败: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
```

## 错误处理示例

### 带重试的图片生成

```bash
#!/bin/bash
# generate-with-retry.sh — 带重试的图片生成

PROMPT="$1"
MAX_RETRIES=3
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
    echo "尝试 $i/$MAX_RETRIES"

    RESULT=$(ai-image text2img "$PROMPT" 2>/dev/null)
    SUCCESS=$(echo "$RESULT" | jq -r '.success')

    if [ "$SUCCESS" = "true" ]; then
        echo "$RESULT"
        exit 0
    fi

    ERROR=$(echo "$RESULT" | jq -r '.error')
    echo "失败: $ERROR"

    if [ $i -lt $MAX_RETRIES ]; then
        echo "等待 ${RETRY_DELAY} 秒后重试..."
        sleep $RETRY_DELAY
    fi
done

echo "所有重试均失败" >&2
exit 1
```

### 验证环境配置

```bash
#!/bin/bash
# check-env.sh — 检查 ai-image 环境配置

echo "=== ai-image 环境检查 ==="

# 1. 检查命令是否存在
if command -v ai-image &>/dev/null; then
    VERSION=$(ai-image --version 2>/dev/null || echo '未知')
    echo "[OK] ai-image 已安装: $VERSION"
else
    echo "[FAIL] ai-image 未安装"
    echo "  安装命令: pip install ai-image-cli -i http://music-pypi.hz.netease.com/simple --trusted-host music-pypi.hz.netease.com"
    exit 1
fi

# 2. 检查认证
if [ -n "$LANGBASE_TOKEN" ]; then
    echo "[OK] LANGBASE_TOKEN 已设置"
elif [ -n "$ARK_API_KEY" ]; then
    echo "[OK] ARK_API_KEY 已设置"
else
    echo "[FAIL] 未配置认证"
    echo "  设置: export LANGBASE_TOKEN='appId.appKey'"
    echo "  或: export ARK_API_KEY='appId.appKey'"
    exit 1
fi

# 3. 测试 capabilities
echo -n "测试 capabilities... "
CAPS=$(ai-image capabilities 2>/dev/null)
if echo "$CAPS" | jq -e '.tools' &>/dev/null; then
    echo "[OK]"
else
    echo "[FAIL]"
    exit 1
fi

# 4. 测试生成（可选，会消耗配额）
read -p "是否测试图片生成？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -n "测试图片生成... "
    RESULT=$(ai-image text2img "test" --seed 1 2>/dev/null)
    if echo "$RESULT" | jq -e '.success' &>/dev/null; then
        echo "[OK]"
        URL=$(echo "$RESULT" | jq -r '.data.data[0].url')
        echo "  图片 URL: $URL"
    else
        echo "[FAIL]"
        ERROR=$(echo "$RESULT" | jq -r '.error')
        echo "  错误: $ERROR"
        exit 1
    fi
fi

echo "=== 所有检查通过 ==="
```

## 提示词优化示例

### 文生图提示词模板

```bash
#!/bin/bash
# prompt-template.sh — 提示词模板生成器

# 模板：主体 + 环境 + 风格 + 质量
generate_from_template() {
    local SUBJECT="$1"      # 主体
    local ENVIRONMENT="$2"  # 环境
    local STYLE="$3"        # 风格
    local QUALITY="${4:-高清,细节丰富}"  # 质量

    PROMPT="${SUBJECT},${ENVIRONMENT},${STYLE},${QUALITY}"

    echo "生成提示词: $PROMPT"
    ai-image text2img "$PROMPT"
}

# 示例用法
generate_from_template \
    "一个穿着红色连衣裙的中国女孩" \
    "在夕阳下的海滩上微笑" \
    "柔和光线,唯美" \
    "高清,细节丰富"
```

### 图生图提示词建议

```bash
# 好的提示词：简洁明确
ai-image img2img "将背景改成蓝天白云" https://example.com/photo.jpg

# 避免：过于复杂
# ai-image img2img "将背景改成蓝天白云,同时保持人物清晰,添加一些鸟,增强色彩饱和度" ...

# 推荐：分步编辑
ai-image img2img "将背景改成蓝天白云" https://example.com/photo.jpg
# 使用上一步的结果继续编辑
ai-image img2img "添加飞鸟" https://result-url-from-step1.jpg
```

## 最佳实践

### 1. 使用固定种子进行 A/B 测试

```bash
# 测试不同提示词，保持其他参数一致
SEED=12345

ai-image text2img "一只猫" --seed $SEED > result_a.json
ai-image text2img "一只可爱的猫" --seed $SEED > result_b.json
ai-image text2img "一只可爱的小猫,高清" --seed $SEED > result_c.json
```

### 2. 批量处理时添加延迟

```bash
# 避免请求过快被限流
for prompt in "${PROMPTS[@]}"; do
    ai-image text2img "$prompt"
    sleep 2  # 等待 2 秒
done
```

### 3. 保存完整的生成记录

```bash
# 保存 JSON 结果用于后续分析
PROMPT="测试图片"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_DIR="./history"

mkdir -p "$OUTPUT_DIR"

ai-image text2img "$PROMPT" | tee "$OUTPUT_DIR/${TIMESTAMP}.json"
```
