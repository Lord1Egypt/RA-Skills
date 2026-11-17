# 发布衔接（html-golive）

easy-html 生成并设好样式 / Title / FavIcon 的 HTML 后，**提醒**用户可以发布成线上页面。
用户确认后，用 [html-golive](https://github.com/Songhonglei/html-golive) 一键发布。

## 流程

1. HTML 已就绪（默认在 `./output/easy-html/<name>.html`，可用 `EASY_HTML_OUT` 改）
2. **提醒并询问**（不要直接发——对外操作先问）：
   > 页面已生成。要我发布成线上可访问的链接吗？
3. 用户确认后执行发布。

## 发布命令

```bash
pip install html-golive        # 首次
golive publish <生成的html路径> --name "<页面名称>"
```

- stdout 会给出可访问 URL（默认 `http://localhost:8787/<slug>`，
  自建服务器/对象存储后端时是对应域名）。
- `golive serve` 启动本地服务；完整用法见 html-golive 自身文档。

## favicon 兜底

- 若 HTML 已含有效 `<link rel="icon">`（包括 easy-html 设的 emoji data URI），
  发布时会原样保留，无需额外操作。
- 没设 favicon 也没关系，浏览器会用默认图标，**可以跳过**，不强制要求用户提供。
- 想显式指定图片 favicon，传一个可访问的图片 URL 给 `set_meta.py --favicon`。

## 用别的发布方式

easy-html 的产物是**自包含单文件 HTML**（CSS 内联、图表走 CDN），
所以任何静态托管都能直接用：

- 直接把文件发给对方 / 邮件附件
- GitHub Pages、Netlify、Vercel、S3 静态站点
- `python3 -m http.server` 本地预览

发布渠道不是 easy-html 的职责，选顺手的即可。

## 发布后

- 把可访问 URL 给用户（用业务名做锚文本）。
- 如需改样式/内容，重新生成后覆盖更新即可（`golive publish --update` 或对应平台的更新方式）。
