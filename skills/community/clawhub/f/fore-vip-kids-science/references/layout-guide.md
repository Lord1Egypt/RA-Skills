# 图文排版规范（排版页 · HTML 卡片）

将「每节图片 + 文字」组装为排版后的图文页。本文件提供 HTML 卡片模板，儿童友好、明亮、响应式，可直接本地预览或分享。

## 一、输出形式
- 生成 1 个自包含 HTML 文件（内联 CSS，图片用本地绝对路径或相对路径）。
- 保存路径：工作区 `generated-images/十万个为什么_{slug}.html`（slug 取问题缩写/拼音）。
- 同时在对话中展示文件链接与要点。

## 二、HTML 模板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>十万个为什么 · {question}</title>
<style>
  :root { --bg:#fff7e6; --card:#ffffff; --accent:#ffb703; --text:#3a3a3a; }
  * { box-sizing: border-box; }
  body { margin:0; font-family: "PingFang SC","Microsoft YaHei",sans-serif; background:var(--bg); color:var(--text); }
  .wrap { max-width: 720px; margin: 0 auto; padding: 24px 16px; }
  h1 { text-align:center; color:var(--accent); font-size: 28px; }
  .card { background:var(--card); border-radius:20px; padding:16px; margin:16px 0; box-shadow:0 6px 18px rgba(0,0,0,.08); display:flex; flex-direction:column; gap:12px; }
  .card img { width:100%; border-radius:14px; display:block; }
  .card h2 { margin:0; color:var(--accent); font-size:20px; }
  .card p { margin:0; line-height:1.7; font-size:16px; }
  .footer { text-align:center; color:#999; font-size:12px; margin-top:24px; }
</style>
</head>
<body>
  <div class="wrap">
    <h1>十万个为什么 · {question}</h1>

    <section class="card">
      <img src="{img1}" alt="一句话答案配图">
      <h2>一句话答案</h2>
      <p>{text1}</p>
    </section>

    <section class="card">
      <img src="{img2}" alt="为什么会这样配图">
      <h2>为什么会这样？</h2>
      <p>{text2}</p>
    </section>

    <section class="card">
      <img src="{img3}" alt="生活例子配图">
      <h2>生活里的小例子</h2>
      <p>{text3}</p>
    </section>

    <section class="card">
      <img src="{img4}" alt="冷知识配图">
      <h2>冷知识 / 延伸</h2>
      <p>{text4}</p>
    </section>

    <div class="footer">由前凌智选 fore.vip 提供 · AI 生成配图</div>
  </div>
</body>
</html>
```

## 三、排版要点
- 每节一张图在上、文字在下，卡片化排列，留白充足。
- 主色明亮温暖（橙黄 #ffb703 / 米白底），字号儿童易读（正文 ≥16px）。
- 图片路径用生成的本地路径；若需发布，替换为可访问 URL。
- 安全：不放入任何不适龄/恐怖画面；图片与文字主题一致。
