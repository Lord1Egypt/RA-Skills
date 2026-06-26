---
name: douyin-browser-publish
description: 抖音视频浏览器自动化发布。输入视频路径、标题、描述，自动完成上传发布。当用户说"发抖音"、"发布到抖音"时使用。
---

# 抖音视频发布（浏览器自动化）

## 使用场景
视频文件已准备好，需要发布到抖音创作者平台。

## 前置条件
- 浏览器已启动（browser tool，profile=openclaw）
- 抖音创作者平台已登录
- 视频文件已存在

## 发布流程

### 1. 导航到上传页面
浏览器打开: `https://creator.douyin.com/creator-micro/content/upload`

### 2. 让上传框可见
```javascript
document.querySelectorAll('input[type="file"]').forEach(el => {
  el.style.cssText = 'position:fixed!important;top:10px!important;left:10px!important;width:300px!important;height:50px!important;opacity:1!important;z-index:999999!important;display:block!important;visibility:visible!important;pointer-events:auto!important;';
});
```

### 3. 上传视频
使用 `browser upload` 工具，selector=`input[type="file"]`，paths=[视频绝对路径]

### 4. 等待上传完成
等待 10-15 秒，截图确认预览正常。

### 5. 填写标题
找到标题输入框（ref 从 snapshot 获取），用 `type` 写入标题。

### 6. 填写描述
找到 contenteditable div（在标题下方），用 JS 设置 textContent 并 dispatch input/change 事件：
```javascript
const editables = document.querySelectorAll('[contenteditable="true"]');
for (const el of editables) {
  const rect = el.getBoundingClientRect();
  if (rect.top > 200 && rect.top < 400 && rect.height > 30) {
    el.textContent = '描述内容';
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
    break;
  }
}
```

### 7. 发布
找到"发布"按钮，click。

### 8. 验证
等待 5 秒，截图确认跳转到"作品管理"页面且状态为"已发布"。

## 故障处理
- 上传框未找到 → 导航到 `https://creator.douyin.com/creator-micro/content/post/video`
- 登录过期 → 提示用户重新登录
- 上传失败 → 重试一次

## 元数据模板
标题：`{故事名} 琪琪睡前故事`
描述：`儿童成长故事，适合3-8岁小朋友 #儿童故事 #睡前故事 #亲子时光`
