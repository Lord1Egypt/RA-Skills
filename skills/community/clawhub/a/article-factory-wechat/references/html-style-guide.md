# HTML 排版样式规范

## 元素样式表

| 元素 | 样式 |
|------|------|
| 标题 | h1，居中，26px，#333 |
| 作者 | p，居中，灰色#888，14px |
| 导读框 | section，渐变色背景#667eea→#764ba2，白色文字，圆角8px，padding:15px |
| 章节标题 | h2，左边框 4px solid #e74c3c，padding-left:12px |
| 正文 | p，15px，行高1.9，首行缩进2em，#333 |
| 代码块 | section，背景#2d3436，等宽字体，圆角6px |
| 重点文字 | strong，#e74c3c红色 |
| 数据卡片 | section，display:flex，三栏布局，圆角8px，阴影 |
| 提示框 | section，渐变色背景#00b894→#00cec9，白色文字，圆角8px |
| 结语 | section，深色渐变#2d3436→#636e72，居中，白色文字 |
| 数据来源 | section，浅灰#f5f5f5背景，12px，#999 |

## 颜色方案

```css
/* 主色 */
--red: #e74c3c;
--blue: #3498db;
--purple: #9b59b6;

/* 背景 */
--light-bg: #fafafa;
--dark-bg: #2d3436;

/* 文字 */
--text: #333;
--muted: #888;
--source: #999;
```

## 完整 HTML 模板

```html
<section style="max-width:100%;margin:0 auto;padding:20px;">
  <!-- 标题 -->
  <h1 style="text-align:center;font-size:26px;color:#333;">文章标题</h1>

  <!-- 导读框 -->
  <section style="background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:15px;border-radius:8px;margin:20px 0;">
    导读内容...
  </section>

  <!-- 正文 -->
  <h2 style="border-left:4px solid #e74c3c;padding-left:12px;">章节标题</h2>
  <p style="font-size:15px;line-height:1.9;text-indent:2em;color:#333;">正文内容...</p>

  <!-- 重点 -->
  <p><strong style="color:#e74c3c;">重点文字</strong></p>

  <!-- 代码块 -->
  <section style="background:#2d3436;color:#dfe6e9;padding:15px;border-radius:6px;font-family:monospace;font-size:13px;">
    代码内容...
  </section>

  <!-- 数据卡片 -->
  <section style="display:flex;gap:10px;margin:20px 0;">
    <section style="flex:1;background:#f8f9fa;padding:15px;border-radius:8px;text-align:center;">
      <p style="font-size:24px;font-weight:bold;color:#e74c3c;">数据1</p>
      <p style="font-size:12px;color:#888;">标签</p>
    </section>
    <!-- 重复更多卡片 -->
  </section>

  <!-- 提示框 -->
  <section style="background:linear-gradient(135deg,#00b894,#00cec9);color:#fff;padding:15px;border-radius:8px;">
    提示内容...
  </section>

  <!-- 结语 -->
  <section style="background:linear-gradient(135deg,#2d3436,#636e72);color:#fff;padding:20px;border-radius:8px;text-align:center;margin-top:30px;">
    <p style="font-size:16px;">结语内容...</p>
  </section>

  <!-- 数据来源 -->
  <section style="background:#f5f5f5;padding:12px;border-radius:6px;margin-top:20px;">
    <p style="font-size:12px;color:#999;">📖 数据来源：xxx</p>
  </section>
</section>
```

## 微信公众号 HTML 注意事项

1. **内联样式** — 微信不支持 `<style>` 标签，所有样式必须 inline
2. **不支持 position/float** — 用 flex 替代
3. **图片用 `<image>`** — 不是 `<img>`，且需先上传到微信素材库
4. **最大宽度** — 设置 `max-width:100%` 防止溢出
5. **字体** — 微信默认字体，不要自定义 @font-face
