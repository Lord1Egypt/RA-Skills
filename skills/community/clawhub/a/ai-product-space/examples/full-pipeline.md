# 示例：完整电商素材生成流水线

展示从上传产品图到获得全套素材的完整对话流程。

---

**用户**: 帮我生成蓝牙耳机的电商素材

**助手**: 好的，我来帮你生成蓝牙耳机的全套电商素材。首先创建一个专属工作空间。

→ `create_space({ name: "蓝牙耳机" })`

工作空间已创建（ID: abc123）。请提供蓝牙耳机的白底产品图，支持本地文件路径或图片 URL。

**用户**: 用这张图 https://example.com/earbuds.jpg

**助手**: 收到，正在上传产品图...

→ `upload_product_image({ space_id: "abc123", image_url: "https://example.com/earbuds.jpg" })`

产品图上传成功！你希望素材用什么语言输出？默认中文，也支持英语、日语、韩语等 10 种语言。

**用户**: 中文和英文都要

**助手**: 好的，先生成中文版本。全套流水线大约需要 2-5 分钟，包含商品主图、场景图、卖点海报和营销文案。

→ `run_ecommerce_pipeline({ space_id: "abc123", language: "zh", wait: true })`

中文版素材生成完成！共生成 22 张图片和 6 段文案。接下来生成英文版本...

→ `run_ecommerce_pipeline({ space_id: "abc123", language: "en", wait: true })`

全部完成！你的蓝牙耳机电商素材包已就绪：
- 🖼️ 44 张商品图（中/英各 22 张）
- ✍️ 12 段营销文案
- 需要生成 8 秒展示视频吗？

**用户**: 好的，做个视频

**助手**: 正在从商品图生成展示视频，大约需要 1-3 分钟...

→ `generate_video({ space_id: "abc123", image_urls: ["https://...main.jpg"], wait: true })`

视频生成完成！8 秒展示视频已就绪。你可以使用 `list_assets` 浏览和下载所有生成的素材。
