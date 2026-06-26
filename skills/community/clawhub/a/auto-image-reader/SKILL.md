---
name: auto-image-reader
description: 自动读取用户上传的图片。当用户发送图片时（通过飞书/Telegram等渠道），系统会在消息中附带图片路径。触发后自动读取图片内容并理解，无需手动查找路径。
version: 1.0.0
---

# Auto Image Reader — 自动图片读取技能

## 触发条件
- 用户发送了图片，并询问图片内容
- 用户上传了图片，希望AI读取并分析
- 任何包含图片消息的场景

## 核心问题
系统发送图片时，路径可能是相对路径（如 `user_input_files/image.png`），
直接用这个路径访问会返回404。

**正确做法：用 `images_list` 先查找图片的真实绝对路径。**

## 工作流程

### Step 1：查找图片的真实路径
使用 `images_list` 工具，遍历找到对应的图片文件：

```
images_list(start=0, number=20)
```
在返回结果中找到图片的 `Path` 字段，如：
```
/workspace/user_input_files/image.png
/workspace/imgs/xxx.jpg
```

**匹配逻辑：**
- 如果文件名包含用户消息中的关键词（如用户说"这张图"），匹配
- 如果有多张最新图片，取最新的（按修改时间）
- 如果是唯一的 user_input_files/image.png，直接使用

### Step 2：用 images_understand 读取图片
找到真实路径后，用 `images_understand` 分析：

```
images_understand(
  image_info=[
    {
      "file": "/workspace/user_input_files/image.png",  # 真实绝对路径
      "prompt": "请详细描述这张图片的所有内容，包括：文字、布局、颜色、背景色、右下角是否有水印，以及整体视觉效果。"
    }
  ]
)
```

### Step 3：读取并回答用户
根据图片内容，用自然语言回答用户的问题。

## 常见场景模板

| 用户说 | 解读prompt |
|--------|-----------|
| "这张图的内容是什么" | 请详细描述这张图片的所有内容 |
| "图片里右下角有水印吗" | 请仔细检查图片右下角和边缘是否有水印（特别是'Created by...'字样） |
| "图片里写的什么" | 请提取图片中所有可见的文字内容 |
| "这张图有什么问题" | 请分析这张图片是否存在问题（如水印、背景异常、显示错误） |

## 重要注意事项

- **绝对路径格式**：`/workspace/...` 而不是 `user_input_files/...`
- **先查再读**：不要直接用消息中的相对路径，必须先用 `images_list` 确认真实路径
- **文件名重复**：如果 user_input_files 下有多个 image.png，用时间或内容特征区分
- **图片可能已删除**：如果 images_list 找不到，说明图片已被清理，从消息元数据中无法追溯

## 自动读取逻辑（伪代码）

```
当收到用户图片消息时：
    1. 从消息元数据提取文件名（如 image.png）
    2. 调用 images_list(start=0, number=20)
    3. 在结果中搜索包含该文件名的记录
    4. 找到 → 提取 Path 字段（真实绝对路径）
    5. 调用 images_understand(file=真实路径, prompt=用户问题)
    6. 回答用户
```

---

## 已在 MEMORY.md 中固化

本技能的核心理念已写入 MEMORY.md：
- 收到图片消息时，必须先用 images_list 查找真实路径
- 不能假设消息中的文件名可以直接访问
- images_list 能看到 /workspace 下所有图片的真实路径
