# Skills.md

## Skill Name
comic-to-realistic

---

## Description
Convert comic, anime, or illustration-style character images into high-quality, realistic human portraits.

This skill leverages AI-powered prompt enhancement and image-to-image generation to transform 2D artistic styles into photorealistic human visuals, while preserving key identity features such as hairstyle, facial structure, and expression.

---

## Service Overview

- 🌐 **Product Website / Console**:  
  https://ai.ngmob.com  

- 🔗 **API Base URL**:  
  https://api.ngmob.com  

> ⚠️ Note:  
> - `ai.ngmob.com` is used for product access, workflow management, and console operations  
> - `api.ngmob.com` is used strictly for API requests and workflow execution  

---

## Use Cases

- Anime / comic character → realistic human conversion  
- AI-generated avatars and profile images  
- Game character realism enhancement  
- Visual content creation for marketing and social media  

---

## Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| Image Input | string (URL) | ✅ | Publicly accessible image URL (anime/comic style) |

---

## Prompt Guidelines

To achieve the best results, include the following in your prompt:

### Style Keywords
- realistic / photorealistic / ultra realistic  
- cinematic  

### Photography Settings
- 85mm lens  
- shallow depth of field  
- studio lighting / soft lighting  

### Detail Enhancements
- detailed skin texture  
- natural skin tone  
- high detail face  

---

## Preview

![Comic](https://cdn.miraskill.cc/workflow_templates/138ba1390f7151b72981083d053aad31.jpg)
![Realistic](https://cdn.miraskill.cc/workflow_templates/22222221313.jpg)

### Example (Recommended)

```json
{
  "Image Input": "https://example.com/anime.jpg"
}

