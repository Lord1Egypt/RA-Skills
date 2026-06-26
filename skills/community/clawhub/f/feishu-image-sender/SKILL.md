---
name: feishu-image-sender
description: |
  Send images to Feishu. Activate when user mentions sending images to Feishu, or when message contains image file paths/names (.png, .jpg, .jpeg, .gif, .webp).
---

# Feishu Image Sender Skill

## 触发条件

当以下情况时自动激活此技能：
- 用户要求发送图片到飞书
- 消息中包含图片文件路径或文件名（.png, .jpg, .jpeg, .gif, .webp）
- 需要通过飞书媒体消息发送本地图片

## 功能说明

这个 skill 用于在飞书中发送图片消息，并处理相关的权限和文件管理。

## 使用场景

当用户需要：
- 通过飞书发送本地图片
- 自动处理图片上传和消息发送
- 确保飞书权限正确配置

## 前置条件

1. **图片文件**
   - 图片必须保存在 workspace 目录
   - 支持格式：jpg, png, gif, webp

## 使用步骤

### 1. 检查图片文件

```bash
# 查找图片文件
find ~/.openclaw/workspace -name "图片名.png" -type f
```

### 2. 发送图片到飞书

使用 `message` 工具发送图片：

```javascript
message({
  action: "send",
  channel: "feishu",
  message: "图片说明文字",
  media: "/path/to/workspace/图片名.png"
})
```

### 3. 处理权限错误

如果遇到权限错误：
- 检查错误信息中的权限授权链接
- 提示管理员访问授权链接
- 等待授权完成后重试

## 常见问题

### Q: 发送图片时提示权限错误怎么办？

A: 访问权限授权链接，让管理员授权所需权限。

### Q: 图片发送成功但看不到？

A: 检查：
1. 图片路径是否正确
2. 图片格式是否支持
3. 飞书权限是否已授权

### Q: 如何批量发送多张图片？

A: 循环调用 message 工具，每次发送一张图片。

## 示例代码

### 发送单张图片

```javascript
// 发送 test.png
message({
  action: "send",
  channel: "feishu",
  message: "这是 test.png",
  media: "/path/to/workspace/test.png"
})
```

### 批量发送图片

```javascript
const images = ["test1.png", "test2.png", "test3.png"];

for (const img of images) {
  message({
    action: "send",
    channel: "feishu",
    message: `发送图片：${img}`,
    media: `/path/to/workspace/${img}`
  });
}
```

## 注意事项

1. **文件路径**：始终使用绝对路径
2. **权限检查**：发送前确认飞书权限已授权
3. **文件存在性**：发送前检查文件是否存在
4. **格式支持**：只发送支持的图片格式

## 维护记录

- 2026-02-19: 创建 skill，固化飞书图片发送流程
