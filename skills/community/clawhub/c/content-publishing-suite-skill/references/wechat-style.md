# 微信 135 编辑器兼容内联样式规范

微信公众号渲染会完全剥离 `<style>` 标签与 CSS class，只保留 inline style。本规范所有样式必须内联，且不使用外联资源。字号、行高、间距、颜色和背景唯一读取 `wechat_layout_baseline.json`；模板与生成脚本不得自行改写这些值。每次生成后运行 `scripts/validate_wechat_layout.py`，未通过不得交付。

## 容器规则

- 每个内容块用 `<section>` 包裹，不使用外层 `<div>` 容器（微信会自动提供宽度约束）。
- 文末必须加 `<v2></v2>` 版本标记，否则 135 编辑器会触发旧版迁移、破坏排版。
- 不使用 `<script>`、`<style>`、外联 class、`position:fixed/absolute`、外部字体。
- 图片用占位区域，用户后续替换。

## 组件样式（直接复制 inline）

### 文章标题（H1）
```html
<section style="padding:0;">
  <h1 style="font-size:23px;font-weight:700;text-align:center;color:#1a3a5c;margin:30px 16px 10px;line-height:1.45;">{{TITLE}}</h1>
</section>
```

### 摘要块

摘要是微信公众号长文标题下的短引子，不是摘要卡配文。长度最多 120 字符，通常控制在 30 字符以内；应与标题形成互补，承担正文引子或一句实质结论。不得把正文首段或 810×1080 摘要卡长配文直接复制到这里。生成器读取定稿 front matter 的 `summary` / `摘要` 字段时，超过 120 字符必须阻断。

```html
<section style="padding:0;">
  <blockquote style="margin:1.5em 0;padding:15px 20px;background:#f5f7fa;border-left:4px solid #1a3a5c;border-radius:0 8px 8px 0;"><p style="font-size:15px;line-height:1.7;color:#666666;margin:0;"><strong style="color:#1a3a5c;font-weight:700;">摘要</strong>：{{SUMMARY}}</p></blockquote>
</section>
```

### 章节小标题（H2，含 4px 色条）
```html
<section style="padding:0;">
  <h2 style="font-size:18px;font-weight:700;color:#1a1a1a;margin:2.5em 0 1em;padding-left:10px;border-left:4px solid #1a3a5c;line-height:1.5;">{{HEADING}}</h2>
</section>
```

### 正文段落
```html
<section style="padding:0;">
  <p style="font-size:16px;line-height:1.8;color:#333333;margin:0 0 1.5em;letter-spacing:1px;">{{PARAGRAPH}}</p>
</section>
```

### 关键判断句（加粗着色）
```html
<strong style="color:#1a3a5c;">{{KEY_JUDGMENT}}</strong>
```

### 引用块
```html
<section style="padding:0;">
  <blockquote style="margin:1.5em 0;padding:15px 20px;background:#f5f7fa;border-left:4px solid #1a3a5c;border-radius:0 8px 8px 0;"><p style="font-size:15px;line-height:1.7;color:#666666;margin:0;">{{QUOTE}}</p></blockquote>
</section>
```

### 列表项
```html
<section style="padding:0;">
  <p style="font-size:16px;line-height:1.8;color:#333333;margin:0 0 1.5em;letter-spacing:1px;"><span style="color:#1a3a5c;margin-right:6px;">•</span>{{ITEM}}</p>
</section>
```

### 表格（深蓝表头白字 + 斑马纹）
```html
<section style="padding:8px 16px;overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:14px;line-height:1.6;">
    <thead>
      <tr style="background:#1a3a5c;color:#fff;">
        <th style="padding:8px 10px;text-align:left;border:1px solid #1a3a5c;">{{H1}}</th>
        <th style="padding:8px 10px;text-align:left;border:1px solid #1a3a5c;">{{H2}}</th>
      </tr>
    </thead>
    <tbody>
      <tr style="background:#fff;"><td style="padding:8px 10px;border:1px solid #ddd;">{{C1}}</td><td style="padding:8px 10px;border:1px solid #ddd;">{{C2}}</td></tr>
      <tr style="background:#f5f7fa;"><td style="padding:8px 10px;border:1px solid #ddd;">{{C1}}</td><td style="padding:8px 10px;border:1px solid #ddd;">{{C2}}</td></tr>
    </tbody>
  </table>
</section>
```

## 风格禁忌

- 不使用科技电路风、发光、数字网格、渐变背景。
- 不堆砌 emoji；分隔用 `<section style="height:1px;background:#eee;margin:12px 16px;"></section>` 而非 `<hr>`（更可控）。
- 全部颜色取自深普鲁士蓝 `#1a3a5c` 与中性灰 `#333/#555/#ddd/#f5f7fa`，保持克制。
