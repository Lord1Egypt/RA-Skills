# WeChat Cover Photo Generation with GLM-Image API

This document explains how to generate professional WeChat Official Account cover photos (21:9 aspect ratio) using the GLM-Image API.

## Overview

The `generate_cover_photo.py` script uses Zhipu AI's GLM-Image API to automatically generate high-quality cover photos for WeChat articles based on article title and theme.

## Prerequisites

1. **GLM API Key**: Obtain from [Zhipu AI Platform](https://open.bigmodel.cn/)
2. **Python 3.7+** with `requests` library
3. **Environment Setup**: Set `GLM_API_KEY` environment variable

## API Configuration

- **Endpoint**: `https://open.bigmodel.cn/api/paas/v4/images/generations`
- **Authentication**: Bearer token (API key)
- **Models Available**:
  - `glm-image` (recommended, latest model)
  - `cogview-4-250304` (high quality)
  - `cogview-4` (stable version)
  - `cogview-3-flash` (fast generation)

## Supported Image Sizes

- `1280x720` - **Recommended for generation** (16:9 landscape)
- `1024x1024` - Square format
- `720x1280` - Portrait format
- `1280x1280` - High-resolution square

**After generation, image will be resized to 900x386 (21:9) for WeChat**

## Quality Options

- `standard` - Standard quality, faster generation
- `high` - High quality, better details, slower

## Usage

### Basic Usage

```bash
python scripts/generate_cover_photo.py \
  --title "Claude Cowork企业部署完全指南" \
  --theme "AI企业自动化" \
  --output "output/2026-01-19-claude-cowork-guide-cover.png"
```

### Advanced Usage with Custom Style

```bash
python scripts/generate_cover_photo.py \
  --title "AI代理如何改变企业工作流" \
  --theme "AI工作流自动化" \
  --style "futuristic tech" \
  --color-scheme "blue and purple gradient" \
  --model "cogview-4" \
  --size "1280x720" \
  --quality "high" \
  --output "output/2026-01-19-ai-workflow-cover.png"
```

### Using Custom Prompt

```bash
python scripts/generate_cover_photo.py \
  --title "Article Title" \
  --theme "Theme" \
  --custom-prompt "专业科技风格微信封面，蓝色渐变背景，现代简约设计，高清质量" \
  --output "output/cover.png"
```

### Setting API Key

**Option 1: Environment Variable (Recommended)**
```bash
export GLM_API_KEY="your-api-key-here"
python scripts/generate_cover_photo.py --title "..." --theme "..." --output "..."
```

**Option 2: Command Line Argument**
```bash
python scripts/generate_cover_photo.py \
  --api-key "your-api-key-here" \
  --title "..." \
  --theme "..." \
  --output "..."
```

## Command Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--title` | Yes | - | Article title |
| `--theme` | Yes | - | Main theme/topic |
| `--style` | No | `professional modern tech` | Visual style description |
| `--color-scheme` | No | `blue gradient` | Color scheme preference |
| `--output` | Yes | - | Output file path |
| `--model` | No | `glm-image` | GLM model to use |
| `--size` | No | `1280x720` | Image dimensions |
| `--quality` | No | `standard` | Image quality |
| `--api-key` | No | - | GLM API key (or use env var) |
| `--custom-prompt` | No | - | Custom prompt override |

## Prompt Engineering Guidelines

### Professional Business Style
```
专业的微信公众号封面图，主题：[topic]。
现代商务风格，蓝色渐变背景，简洁大气。
包含[key elements]，适合企业内容传播。
高质量，16:9横版构图。
```

### Tech/AI Theme
```
科技感微信封面图，主题：[AI topic]。
未来科技风格，蓝色光效，数字化元素。
展现[core concept]，专业且吸引眼球。
高清质量，适合公众号文章。
```

### Modern Minimalist
```
简约现代微信封面，主题：[topic]。
极简设计，蓝白配色，留白艺术。
突出[key message]，传递专业感。
1280x720高清横版。
```

## Integration with Content Factory Workflow

The cover photo generation is integrated into the content-factory skill workflow:

1. **After article writing** (Phase 3: Final Polish)
2. **Before WeChat publishing** (Section 9)
3. **Automatic generation** based on article title and theme

### Workflow Integration Example

```bash
# Step 1: Generate article content (handled by content-factory skill)
# ... article generation ...

# Step 2: Generate cover photo
python scripts/generate_cover_photo.py \
  --title "$(extract_title_from_article)" \
  --theme "$(extract_theme_from_article)" \
  --output "D:\AI\contents\CCoutput\2026-01-19-article-slug-cover.png"

# Step 3: Publish to WeChat with cover photo
python scripts/wechat_publish.py \
  --html "D:\AI\contents\CCoutput\2026-01-19-article-slug.html" \
  --cover "D:\AI\contents\CCoutput\2026-01-19-article-slug-cover.png"
```

## API Response Format

```json
{
  "created": 1234567890,
  "data": [
    {
      "url": "https://temporary-image-url.com/image.png"
    }
  ]
}
```

**Important**: Image URLs are temporary and valid for 30 days. The script automatically downloads and saves images locally.

## Error Handling

The script handles common errors:

- **Missing API key**: Prompts user to set environment variable
- **API request failure**: Displays error message and response details
- **Download failure**: Logs error and exits with non-zero status
- **Invalid parameters**: Validates input before API call

## Output

Successful execution produces:

```
🎨 Generating cover photo with GLM-Image API...
   Model: glm-image
   Size: 1280x720
   Quality: standard
   Prompt: 专业的微信公众号封面图，主题：AI企业自动化...
✅ Image generated successfully!
   URL: https://temporary-url.com/image.png
📥 Downloading image to: output/2026-01-19-article-cover.png
✅ Image downloaded successfully!
   Size: 245.3 KB
   Path: output/2026-01-19-article-cover.png

============================================================
✅ Cover photo generation completed!
   Output: output/2026-01-19-article-cover.png
============================================================
```

## Best Practices

1. **Use descriptive themes**: Provide clear, specific themes for better results
2. **Match article tone**: Align visual style with article content
3. **Consistent branding**: Use consistent color schemes across articles
4. **Test different models**: Try different models for varied styles
5. **Optimize prompts**: Refine prompts based on generation results
6. **Save API costs**: Use `standard` quality for drafts, `high` for final

## Troubleshooting

### Issue: "GLM API key required"
**Solution**: Set `GLM_API_KEY` environment variable or use `--api-key` argument

### Issue: API request timeout
**Solution**: Check network connection, increase timeout in script if needed

### Issue: Image quality not satisfactory
**Solution**:
- Try `--quality high` for better details
- Use `cogview-4` model for higher quality
- Refine prompt with more specific visual descriptions

### Issue: Download fails
**Solution**:
- Check output directory permissions
- Verify disk space available
- Ensure output path is valid

## Examples

### Example 1: AI Enterprise Article
```bash
python scripts/generate_cover_photo.py \
  --title "Claude Cowork如何改变企业协作" \
  --theme "AI企业协作工具" \
  --style "professional corporate" \
  --color-scheme "deep blue gradient" \
  --output "output/2026-01-19-claude-cowork-cover.png"
```

### Example 2: Tech Trend Article
```bash
python scripts/generate_cover_photo.py \
  --title "2026年AI代理发展趋势" \
  --theme "AI技术趋势预测" \
  --style "futuristic tech" \
  --color-scheme "blue and cyan gradient" \
  --model "cogview-4" \
  --quality "high" \
  --output "output/2026-01-19-ai-trends-cover.png"
```

### Example 3: Tutorial Article
```bash
python scripts/generate_cover_photo.py \
  --title "零基础学会使用AI工具" \
  --theme "AI工具入门教程" \
  --style "friendly approachable" \
  --color-scheme "light blue and white" \
  --output "output/2026-01-19-ai-tutorial-cover.png"
```

## API Rate Limits

- Check Zhipu AI platform for current rate limits
- Implement retry logic for production use
- Consider caching generated covers for reuse

## Cost Considerations

- GLM-Image API charges per generation
- `standard` quality is more cost-effective
- Batch generate covers when possible
- Reuse covers for similar topics

## Security Notes

- **Never commit API keys** to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API usage for anomalies

## Future Enhancements

- [ ] Batch generation support
- [ ] Template-based generation
- [ ] A/B testing for cover variations
- [ ] Integration with image editing tools
- [ ] Automatic style learning from successful covers
- [ ] Cover performance analytics

## Support

For issues or questions:
- Check GLM-Image API documentation: https://open.bigmodel.cn/dev/api
- Review error messages in script output
- Verify API key and permissions
- Test with simple prompts first

## License

This script is part of the content-factory skill for Claude Code.
