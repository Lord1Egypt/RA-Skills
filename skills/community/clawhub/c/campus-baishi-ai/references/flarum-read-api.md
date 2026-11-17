# Flarum 论坛 读/检索 API（2026-08 实测验证）

查询功能依赖的公开 API。这些端点无需鉴权，AI 查询帖子时直接调用。

## 搜索帖子（关键：用 `?q=`，不要用 `filter[q]`）

- ✅ **可用**：`GET https://xysq.kcucu.com/api/discussions?q=关键词`（关键词用中文，URL 编码）
  - 返回 `data[]`，每项 `id`（讨论 id）、`attributes.title`（标题）、`relationships.firstPost.data.id`（首帖 id）。
- ❌ **不可用**：`?filter[q]=关键词` 会返回 `500 {"errors":[...]}`。别用。
- 同一问题可换多个关键词多次搜（如"食堂价格"、"东门"、加上学校名）提高命中率。
- 返回结果含标题匹配（如搜"食堂价格"会同时带回"看镜头，咪""最美校花"等无关帖），需按标题/学校 tag 二次过滤。

## 读取帖子正文 + 图片（关键：`contentHtml`）

- `GET https://xysq.kcucu.com/api/posts/{帖子id}` → `data.attributes.contentHtml`。
- **必须用 `contentHtml`**：`content` 字段是空的（匿名/未登录时拿不到），`contentHtml` 才有完整内容。
- `contentHtml` 里同时含**文字**和**图片**：
  - 图片形如 `<img class="FoFUpload--Upl-Image-Preview" src="https://xysq.kcucu.com/assets/files/YYYY-MM-DD/xxx.webp">`。
  - 提取图片 URL：正则 `src="([^"]*\.(?:webp|jpg|jpeg|png|gif))"`。
  - 提取纯文字：`re.sub('<[^>]+>',' ', html)` 后再压缩空白。
- 帖子 id 来源：搜索结果的 `relationships.firstPost.data.id`（讨论 id ≠ 帖子 id，如讨论 id=2 的食堂价格表，首帖 id=3）。

## 识图（图片内容识别，调论坛配置的视觉模型）

- `GET https://xysq.kcucu.com/vision.php?url=<图片完整地址>[&prompt=<可选提示词>]`
- 返回 `{"ok":true,"description":"中文图片描述","model":"...","cached":true/false}`。
- 识图结果存于用户看不到的地方，AI 通过本接口取 description 后，结合用户问题自然回复 + 真人式点评。
- **缓存优先（自动生效）**：用户**前端发帖上传图片时，后端监听 fof/upload 的 WasSaved 事件，后台异步识图自动写入隐藏索引 `image_index`**（用户看不到，AI 可查）。故论坛几乎所有图片上传时就已自动识图。AI 调本接口时，**该图已入库则命中缓存秒回**（`cached:true`，不调模型、0 秒）；未命中才现调模型并自动写回缓存。故同一张图只有首次会真正识图，之后走缓存；识图接口慢/挂也能兜底。AI 正常调用即可，无需自己处理缓存。带了 `&prompt=` 会跳过缓存重新识图（仅默认描述不够用才带）。
- ⚠️ 限流：每 IP 每分钟 10 次、每天 100 次（**每分钟限额是服务器端可配置值，管理员可调整**，遇到返回"达到每分钟限流"时先看是否改过配置，而不是当成写死的硬限制）。一帖多图可全部识别，但每张只识别一次、不重复同一张。
- **多图并行（实测有效）**：一帖多图时**并发**调用识图（每张一个独立请求），不要串行一张张等。实测 2 张串行 51.8s → 并行 30.0s。服务器支持并发，控制每分钟总请求 ≤10 即可。
- prompt 示例：`&prompt=请描述这张食堂价格表的菜名和价格`。

## 标签（tags）—— 常见坑：按数字 id 查单个标签会 404

- 列全部标签：`GET /api/tags`（返回 id、name、slug）。
- 按名字筛标签：`GET /api/tags?filter[q]=食堂`（返回含 slug，如 canteen）。
- 按标签过滤讨论：`GET /api/discussions?filter[tag]=<英文slug>`（如 canteen）。
- 查讨论归属标签：`GET /api/discussions/{id}?include=tags`（返回 tags 关系 + included 里的 tag name）。
- ❌ **`GET /api/tags/{数字id}` → 404**（`not_found`）；`GET /api/tags/中文名` → 405。Flarum Tags **没有**"按数字 id / 中文名直接读单个标签"的端点。别走这条路——要拿标签名，用 `GET /api/tags?filter[q]=名字`。

## 验证命令（curl 示例）

```bash
# 搜索
curl -s "https://xysq.kcucu.com/api/discussions?q=%E9%A3%9F%E5%A0%82%E4%BB%B7%E6%A0%BC"
# 读帖子正文+图片
curl -s "https://xysq.kcucu.com/api/posts/3"
```

## 陷阱小结

1. 搜索用 `?q=`，`filter[q]` 会 500。
2. 读正文用 `contentHtml` 而非 `content`（后者为空）。
3. `UPL-IMAGE-PREVIEW` / `FoFUpload--Upl-Image-Preview` 是图片占位，提取 src 即得图片 URL。
4. 讨论 id 与首帖 id 不同，需通过 `relationships.firstPost.data.id` 取。
