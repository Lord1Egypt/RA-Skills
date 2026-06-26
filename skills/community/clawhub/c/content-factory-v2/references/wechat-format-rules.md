# 微信公众号排版规范（微信安全过滤兼容版 - 2026-04-09更新）

**最后更新：2026-04-09（重大修订）**

---

## ⚠️ 微信安全过滤规则（实战经验）

**🚨 核心问题（血的教训）**：微信安全过滤会强制覆盖以下HTML标签的默认样式（变蓝色）：
- `<h1>/<h2>/<h3>` → 变蓝色
- `<p>` → 变蓝色
- `<strong>` → 变蓝色

**所有CSS class和 `<style>` 块都会被完全剥离！**

### ✅ 唯一安全的CSS用法

**所有样式必须写在 HTML 标签的 `style=""` 内联属性中**，并且：
- 二级标题 → 用 `<div>` 不能用 `<h2>`
- 正文段落 → 用 `<div>` 不能用 `<p>`
- 加粗强调 → 用 `<span style="color:#556b2f;font-weight:bold;">` 不能用 `<strong>`

```html
<!-- ✅ 正确：div内联样式 -->
<div style="font-size:17px;color:#556b2f;font-weight:bold;margin:28px 15px 14px;padding-left:12px;border-left:4px solid #556b2f;">二级标题</div>

<!-- ❌ 错误：h2会被微信强制覆盖为蓝色 -->
<h2 style="font-size:17px;color:#556b2f;">二级标题</h2>
```

---

## 文章标题（H1 - 供发布脚本提取）

```html
<!-- 供 wechat_publish.py 提取标题，必须保留 -->
<h1 style="display:none;">从张雪峰.skill到金谷园饺子馆.skill，给我们带来的思考</h1>
```
- `display:none` 隐藏视觉标题
- 脚本从此标签提取文章标题

---

## 二级标题（Section Title）

```html
<div style="font-size:17px;color:#556b2f;font-weight:bold;margin:28px 15px 14px;padding-left:12px;border-left:4px solid #556b2f;">一、章节标题</div>
```
- 字体：17px，墨绿色 #556b2f，加粗
- 左侧墨绿竖线：4px solid #556b2f
- 左侧留白：padding-left:12px
- 上下间距：margin:28px 15px 14px

---

## 段落正文

```html
<div style="margin:0 0 12px;padding:0 15px;line-height:1.8;">正文内容</div>
```
- 段间距：margin:0 0 12px（下一段前留12px）
- 左右留白：padding:0 15px
- 行高：line-height:1.8
- **禁止用 `<p>` 标签（会被微信覆盖为蓝色）**

---

## 重点样式

### 重点字词（砖红字体 + 奶黄背景）
```html
<span style="background:#fff8e7;padding:2px 6px;border-radius:3px;color:#b74134;font-weight:600;">重点字词</span>
```

### 重点句（墨绿点状下划线）
```html
<span style="border-bottom:2px dotted #556b2f;padding-bottom:2px;color:#556b2f;">重点句子</span>
```

### 数字强调
```html
<span style="color:#556b2f;font-weight:bold;">12天</span>
```

### 加粗（不能用strong标签）
```html
<span style="color:#556b2f;font-weight:bold;">加粗内容</span>
```

---

## Hook区域（开篇摘要框）

```html
<div style="background:#f6fff6;border-left:5px solid #556b2f;box-shadow:3px 3px 10px rgba(85,107,47,0.12);padding:18px 20px;border-radius:0 10px 10px 0;margin:0 0 24px 0;font-size:15px;line-height:1.9;">
    <span style="color:#556b2f;font-weight:bold;">2026年4月</span>，短短两天内...
</div>
```

---

## 列表（禁用ul/ol/li，改用缩进段落）

微信会强制给 `<ul>/<li>` 渲染圆点且样式不可控。

### 正确做法：段落缩进
```html
<div style="margin:0 0 6px 20px;font-size:15px;line-height:1.8;">• 第一条内容</div>
<div style="margin:0 0 6px 20px;font-size:15px;line-height:1.8;">• 最后一条</div>
```

---

## CTA结尾（必须添加）

```html
<div style="background:#556b2f;padding:16px;border-radius:10px;text-align:center;color:#fff;margin:24px 0 0;">
    <div style="margin:0;color:#fff;font-size:15px;line-height:1.8;">如果你觉得文章对你有所帮助，请关注就行</div>
</div>
```

---

## 颜色系统（Jeff品牌色）

| 用途 | 颜色值 | 示例 |
|------|--------|------|
| 二级标题 | #556b2f（墨绿） | `color:#556b2f;font-weight:bold;` |
| 左侧竖线 | #556b2f（墨绿） | `border-left:4px solid #556b2f;` |
| 重点句点下划线 | #556b2f（墨绿） | `border-bottom:2px dotted #556b2f;` |
| 重点字词背景 | #fff8e7（奶黄） | `background:#fff8e7;` |
| 重点字词字体 | #b74134（砖红） | `color:#b74134;` |
| CTA背景 | #556b2f（墨绿） | `background:#556b2f;` |

---

## 发布命令

```bash
cd /root/.openclaw/workspace/skills/content-factory && python3 -X utf8 scripts/wechat_publish.py --html "/root/.openclaw/workspace/output/YYYY-MM-DD-article-slug.html" --cover "/root/.openclaw/workspace/output/YYYY-MM-DD-article-slug-cover.png"
```

**必须加参数**：
- `-X utf8` — 防止中文变 `\uXXXX` 转义序列
- `--cover` — 指定封面图，否则用默认图

---

## 禁止规则

- ❌ 禁止 `<h1>/<h2>/<h3>` 用于视觉标题
- ❌ 禁止 `<p>` 用于正文段落
- ❌ 禁止 `<strong>` 用于加粗
- ❌ 禁止 `<style>` 块
- ❌ 禁止 CSS class 选择器
- ❌ 禁止 `<hr/>` 标签
- ❌ 禁止元信息（日期、版本号）
- ❌ 禁止版权声明

---

*此规范基于 2026-04-09 实战教训更新*
