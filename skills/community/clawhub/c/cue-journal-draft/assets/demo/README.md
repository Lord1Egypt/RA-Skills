# 成品版面稿 demo

一份**可直接用浏览器打开**的版面稿：13 页，八种页面模板每种至少一页。

| 文件 | 是什么 |
|---|---|
| `demo.html` | 版面稿本体（mm 级绝对定位，零外部依赖，双击即开） |
| `content.demo.json` | 渲染它用的内容清单 |
| `img/` | **不含**。示例图原为 png，但发布平台禁止二进制文件，已在 `demo.html` 中改为等高等宽的占位块（`.fig-ph`），版面结构不受影响 |

## 先说清楚：哪些是虚构的

**全部内容都是虚构的** —— 机构（启明律师事务所）、刊物（《区域观察》）、人物、文件名目、
日期与业务信息均为示例，用于演示排版与体例，**不构成任何真实信息或法律意见**。
保留为实测值的只有**版式参数**（页面尺寸、版心、字号序列、色板、坐标）。

## 它能让你看到什么

1. **版式是「量」出来的**：页面尺寸、版心、栏位、字号序列与色板全部取自
   `examples/journal-qiming-regional/assets/stylespec.json` 的实测参数；
   HTML 用 mm 级绝对定位排版，不依赖浏览器打印设置，也不需要装字体。
2. **八种页面模板**：`cover` / `quote` / `masthead` / `toc` / `divider` / `unit_list` /
   `article` / `backcover`。
3. **图是代码画的不是生成的**：`img/` 两张图来自 `assets/diagram-templates/` 的定义文件，
   中文逐字可核、无水印、不吃额度。
4. **续页与分页是自动的**：5 条法规动态由分页器按估算高度装页，装不下自动续页并标「（续）」，
   不是手工切的。

## 怎么重新生成

从**技能根目录**运行（图片路径按根目录解析）：

```bash
python scripts/build_draft.py \
  --content assets/demo/content.demo.json \
  --spec examples/journal-qiming-regional/assets/stylespec.json \
  --out assets/demo --stats --no-baseline-gate
```

`--no-baseline-gate` 是**必须**的：示例稿只有 13 页，而它借用的 spec 带着 91 页样刊的
`scale_baseline`，不跳过就会按设计报 `[FAIL] 量级严重不足` 并以 `exit 1` 退出。

> ⚠️ **分发前要处理一次绝对路径。**
> `build_draft.py` 把图片写成 `file:///…` 的**绝对路径**，所以在自己机器上渲染的 HTML
> 换台机器就打不开图。本目录的 `demo.html` 入库前已做过一次「绝对路径 → 相对路径」替换。
> 你要把稿子发给别人时，需要同样处理一次。
