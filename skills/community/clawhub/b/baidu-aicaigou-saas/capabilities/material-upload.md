# 子能力 A：素材库上传

当需求是"上传素材/上传图片到爱采购素材库"时，使用此流程。

前置依赖：[浏览器框架](../shared/browser-framework.md) | [登录处理](../shared/login.md) | [失败降级](../shared/fallback.md)

## A1. 进入素材管理页面

访问：`https://b2bwork.baidu.com/shop/material/index`

## A2. 检查素材输入

- 确认图片文件路径存在且可访问
- 支持单张或多张图片上传
- 支持的格式：JPG、PNG 等常见图片格式

## A3. 上传执行

获取页面快照，找到并点击"本地上传"按钮，然后根据可用能力选择路径：

**路径 1：DOM 自动化（优先）**

使用 `playwright-cli run-code` 定位 `input[type="file"]` 元素并设置文件路径触发上传：

```bash
playwright-cli run-code "async page => {
  const input = page.locator('input[type=\"file\"]');
  await input.setInputFiles(['/path/to/image1.jpg', '/path/to/image2.jpg']);
}"
```

**路径 2：点击交互（备选）**
- 点击"本地上传"按钮
- 引导用户在系统文件选择器中选择文件

## A4. 成功确认

- 等待上传完成，检查页面是否显示上传成功状态
- 必要时刷新页面，确认素材已出现在素材列表中
- 回报上传结果（成功数量、失败数量及原因）
