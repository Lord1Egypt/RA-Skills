# doubao-ai-image

## Description
Free AI image generation using Doubao (豆包) web interface through browser automation. Mimics human interaction to generate and download images without API costs.

## Usage Scenarios
- Free AI image generation for personal or business use
- When API-based image generation is not available or too expensive
- Automated image creation for reports, presentations, or social media
- Integration with other workflows requiring visual content

## Workflow
1. **Navigate to Doubao**: Open https://www.doubao.com/chat/ in browser
2. **Access Image Generation**: Click on "图像生成" or "AI 创作" feature
3. **Input Prompt**: Enter detailed image description in the text box
4. **Generate Images**: Submit the prompt and wait for AI generation
5. **Select Image**: Choose from the generated options (typically 4 variations)
6. **Capture Image**: Use browser automation to screenshot the large preview image (ref="preview") to avoid download issues
7. **Save Locally**: Store image in `/workspace/ai_images/doubao/` directory with timestamp
8. **Deliver**: Send image directly to Feishu chat or other specified destination

## Key Features
- Completely free AI image generation (no API costs)
- Human-like browser interaction to avoid bot detection
- Supports detailed prompts with style, composition, and quality specifications
- Automatic file management and delivery integration
- Works with Doubao's Seedream 4.5 model and various aspect ratios/styles

## Technical Requirements
- Browser automation capability with proper user agent
- Element targeting for precise screenshot capture (using ARIA refs)
- Image format handling (PNG, JPG, WebP)
- Error handling for generation failures or UI changes
- Wait mechanisms for AI generation completion
- Local file system access for image storage

## Best Practices
- Use specific, detailed prompts for better results
- Include style references when needed (e.g., "realistic", "cartoon", "anime")
- Specify aspect ratio if important for the use case
- Target the "preview" element (ref="preview") for clean screenshot capture
- Verify image quality and composition before delivery
- Handle cases where generation fails or produces unsuitable results
- Save images to standardized directory structure: `/workspace/ai_images/doubao/YYYY-MM-DD/`

## Limitations
- Dependent on Doubao web interface availability
- Subject to Doubao's usage limits and terms of service
- Download location may vary by system/browser configuration
- Generation time varies based on server load
- No guaranteed consistency in image quality or style

## Integration Points
- Can be combined with report generation skills (e.g., xiaoxiyouxi-5min-report)
- Suitable for avatar creation, concept visualization, or illustration needs
- Can feed into social media content pipelines
- Useful for rapid prototyping of visual concepts