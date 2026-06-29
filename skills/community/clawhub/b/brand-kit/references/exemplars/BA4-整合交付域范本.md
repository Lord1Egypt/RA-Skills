## BA4 整合交付域 范本

本文件包含 BA4 域（BA4-01 ~ BA4-04）的纯范本内容。

---

### BA4-01 HTML展示页 · 完整结构范本

**HTML骨架**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>{{公司全称}} · 品牌视觉资产</title>
  <link rel="icon" href="01_核心标志/favicon.ico" type="image/x-icon" sizes="16x16 32x32 48x48 64x64">
  <link rel="icon" type="image/png" sizes="32x32" href="01_核心标志/03_纯图标_32.png">
  <link rel="icon" type="image/png" sizes="64x64" href="01_核心标志/03_纯图标_64.png">
  <link rel="apple-touch-icon" sizes="180x180" href="01_核心标志/03_纯图标_256.png">
  <style>/* 见下方CSS */</style>
</head>
<body>
  <!-- 1. Hero区：Logo + 公司名 + 副标题 -->
  <!-- 2. 核心标志：横版/竖版/纯图标（SVG+PNG双格式对照卡片）+ 纯图标多尺寸(6 PNG展开) + favicon.ico多尺寸(4 PNG展开) -->
  <!-- 3. 商标注册：黑白稿 + 彩色稿（6个卡片） -->
  <!-- 4. 数字化应用：App/头像/水印/黑白/反白（5个卡片） -->
  <!-- 5. 办公文具：名片正反/信封/信纸（4个卡片） -->
  <!-- 6. 宣传物料：PPT/Banner/工牌（3个卡片） -->
  <!-- 7. 位图资源：横版多尺寸→竖版→图标多尺寸→favicon.ico -->
  <!-- 8. 使用指南：色彩规范 + 场景对照表 + 目录树 + SVG/PNG建议 -->
  <!-- Footer：公司联系信息 -->
</body>
</html>
```

**ICO多尺寸展示HTML范本**（位于核心标志区，纯图标多尺寸之后、商标注册之前）：

```html
<!-- favicon.ico 多尺寸 -->
<div class="png-toggle">
  <button onclick="document.getElementById('ico尺寸').classList.toggle('open'); this.textContent = this.textContent === '▼ 查看全部 favicon.ico 尺寸 (4 PNG)' ? '▲ 收起 favicon.ico 尺寸' : '▼ 查看全部 favicon.ico 尺寸 (4 PNG)'">▼ 查看全部 favicon.ico 尺寸 (4 PNG)</button>
</div>
<div class="png-expand" id="ico尺寸">
  <div class="png-grid">
    <div class="png-item"><img src="01_核心标志/favicon_16x16.png" alt="favicon_16x16"><div class="label">favicon_16×16</div></div>
    <div class="png-item"><img src="01_核心标志/favicon_32x32.png" alt="favicon_32x32"><div class="label">favicon_32×32</div></div>
    <div class="png-item"><img src="01_核心标志/favicon_48x48.png" alt="favicon_48x48"><div class="label">favicon_48×48</div></div>
    <div class="png-item"><img src="01_核心标志/favicon_64x64.png" alt="favicon_64x64"><div class="label">favicon_64×64</div></div>
  </div>
</div>
```

**双格式对照卡片CSS**：
```css
.dual-labels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 1px solid #30363d;
}
.dual-labels .lbl { padding: 8px; text-align: center; font-size: 12px; font-weight: 500; }
.dual-labels .lbl.svg { color: #00CCFF; background: rgba(0,204,255,0.05); }
.dual-labels .lbl.png { color: #FF6B35; background: rgba(255,107,53,0.05); }

.dual-preview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 180px;
}
.dual-preview .side {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  overflow: hidden;
}
.dual-preview .side.dark { background: #0A1929; }
.dual-preview .side.check {
  background: #f5f5f5;
  background-image: linear-gradient(45deg,#ddd 25%,transparent 25%),
                    linear-gradient(-45deg,#ddd 25%,transparent 25%),
                    linear-gradient(45deg,transparent 75%,#ddd 75%),
                    linear-gradient(-45deg,transparent 75%,#ddd 75%);
  background-size: 20px 20px;
}
.dual-preview .side img {
  width: 100%;
  height: 160px;
  object-fit: contain;
  display: block;
  background: #FFFFFF;
}
```

**目录树CSS（关键）**：
```css
.tree {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 10px;
  padding: 22px 26px;
  font-family: Consolas, 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.8;
  color: #c9d1d9;
  overflow-x: auto;
  white-space: pre;  /* 关键：防止ASCII树形缩进折叠 */
}
```

**应用场景表格范本**（新格式：4列 — 分类/文件/尺寸/应用场景）：

```html
<table class="scene-table">
  <tr><th>分类</th><th>文件</th><th>尺寸</th><th>应用场景</th></tr>

  <!-- 01 核心标志 -->
  <tr><td rowspan="15">01 核心标志</td><td rowspan="5">01_横版标志</td><td>75px</td><td>浏览器标签页、小尺寸网站Logo</td></tr>
  <tr><td>150px</td><td>页面顶部导航栏、邮件签名</td></tr>
  <tr><td>300px</td><td>常规文档、信函抬头</td></tr>
  <tr><td>1200px</td><td>高清印刷、大屏展示</td></tr>
  <tr><td>原尺寸PNG</td><td>通用矢量源渲染版、印刷标准版</td></tr>

  <tr><td rowspan="5">02_竖版标志</td><td>60px</td><td>侧边栏、小尺寸标识</td></tr>
  <tr><td>120px</td><td>App导航、文档侧边栏</td></tr>
  <tr><td>240px</td><td>社交媒体头像、名片竖版</td></tr>
  <tr><td>960px</td><td>大尺寸印刷、展架</td></tr>
  <tr><td>原尺寸PNG</td><td>通用矢量源渲染版、印刷标准版</td></tr>

  <tr><td rowspan="7">03_纯图标</td><td>16px</td><td>浏览器favicon、书签图标</td></tr>
  <tr><td>32px</td><td>App桌面图标、书签栏</td></tr>
  <tr><td>64px</td><td>邮件签名、桌面快捷方式</td></tr>
  <tr><td>128px</td><td>应用商店图标</td></tr>
  <tr><td>256px</td><td>高分屏、PPT演示</td></tr>
  <tr><td>512px</td><td>高清印刷、海报</td></tr>
  <tr><td>原尺寸PNG</td><td>通用矢量源渲染版、印刷标准版</td></tr>

  <tr><td rowspan="4">favicon.ico</td><td>16×16</td><td>浏览器标签页</td></tr>
  <tr><td>32×32</td><td>书签栏、收藏夹</td></tr>
  <tr><td>48×48</td><td>桌面快捷方式、开始菜单</td></tr>
  <tr><td>64×64</td><td>高分屏浏览器、任务栏</td></tr>

  <!-- 02 商标注册 -->
  <tr><td rowspan="6">02 商标注册</td><td>01_黑白图形商标</td><td>SVG + PNG</td><td>商标注册申报、版权保护</td></tr>
  <tr><td>02_黑白文字商标</td><td>SVG + PNG</td><td>商标注册申报、版权保护</td></tr>
  <tr><td>03_黑白组合商标_推荐</td><td>SVG + PNG</td><td>商标注册申报（推荐提交版）</td></tr>
  <tr><td>04_彩色图形商标</td><td>SVG + PNG</td><td>版权保护备案</td></tr>
  <tr><td>05_彩色文字商标</td><td>SVG + PNG</td><td>版权保护备案</td></tr>
  <tr><td>06_彩色组合商标</td><td>SVG + PNG</td><td>版权保护备案</td></tr>

  <!-- 03 数字化应用 ~ 09 多媒体模板 -->
  <tr><td rowspan="5">03 数字化应用</td><td>01_App图标</td><td>SVG + PNG</td><td>App Store、Google Play图标</td></tr>
  <tr><td>02_社交媒体头像</td><td>SVG + PNG</td><td>微信、微博、LinkedIn头像</td></tr>
  <tr><td>03_文档水印</td><td>SVG + PNG</td><td>文档保护水印</td></tr>
  <tr><td>04_黑白版</td><td>SVG + PNG</td><td>黑白印刷、传真文件</td></tr>
  <tr><td>05_反白版</td><td>SVG + PNG</td><td>深色背景、暗色主题</td></tr>

  <tr><td rowspan="4">04 办公文具</td><td>01_名片正面</td><td>SVG + PNG</td><td>商务名片正面</td></tr>
  <tr><td>02_名片背面</td><td>SVG + PNG</td><td>商务名片背面</td></tr>
  <tr><td>03_C5信封</td><td>SVG + PNG</td><td>商务信函邮寄</td></tr>
  <tr><td>04_A4信纸</td><td>SVG + PNG</td><td>正式文档抬头</td></tr>

  <tr><td rowspan="3">05 宣传物料</td><td>01_PPT封面</td><td>SVG + PNG</td><td>演示文稿封面</td></tr>
  <tr><td>02_网站Banner</td><td>SVG + PNG</td><td>网站首页横幅</td></tr>
  <tr><td>03_员工工牌</td><td>SVG + PNG</td><td>员工身份标识</td></tr>

  <tr><td rowspan="3">06 品牌规范</td><td>01_色彩规范</td><td>SVG + PNG</td><td>VI手册、设计参考</td></tr>
  <tr><td>02_字体规范</td><td>SVG + PNG</td><td>VI手册、设计参考</td></tr>
  <tr><td>03_Logo使用规范</td><td>SVG + PNG</td><td>VI手册、设计参考</td></tr>

  <tr><td rowspan="3">07 环境应用</td><td>01_门头招牌</td><td>SVG + PNG</td><td>门店招牌制作</td></tr>
  <tr><td>02_展会背景板</td><td>SVG + PNG</td><td>展会现场背景</td></tr>
  <tr><td>03_易拉宝</td><td>SVG + PNG</td><td>展会立式展示</td></tr>

  <tr><td rowspan="3">08 产品周边</td><td>01_产品包装盒</td><td>SVG + PNG</td><td>产品外包装</td></tr>
  <tr><td>02_礼品袋</td><td>SVG + PNG</td><td>礼品包装</td></tr>
  <tr><td>03_笔记本封面</td><td>SVG + PNG</td><td>笔记本礼品</td></tr>

  <tr><td rowspan="3">09 多媒体模板</td><td>01_邮件签名</td><td>SVG + PNG</td><td>企业邮箱签名</td></tr>
  <tr><td>02_社交媒体配图</td><td>SVG + PNG</td><td>朋友圈、微博配图</td></tr>
  <tr><td>03_视频封面模板</td><td>SVG + PNG</td><td>视频平台封面</td></tr>
</table>
```

**目录树格式范本**：
```
{{品牌简称}}品牌资产/
├── {{品牌简称}}品牌资产.html          展示页
├── 01_核心标志/                   25 个文件
│   ├── 01_横版标志.svg            横版矢量源
│   ├── 01_横版标志.png            横版 1200×480
│   └── ...
```

---

### BA4-02 完整性校验 · 脚本调用说明

**脚本调用**：`verify_assets.py` 已封装完整性校验全流程（孤儿检测+悬空检测+PNG尺寸标注校验），直接执行即可。

**完整执行**：
```bash
python verify_assets.py <project_root>
```

**校验逻辑概念说明**（便于理解脚本内部流程）：

1. **实际文件扫描**：`os.walk()` 遍历项目目录，排除HTML文件本身，路径分隔符统一为`/`
2. **HTML引用提取**：正则匹配 `src="..."` 和 `href="..."`，排除锚点(#)、外部链接(http)、data URI、`<code>`标签内示例代码
3. **比对**：
   - 孤儿（orphans）= 实际文件 - HTML引用 → 存在但未引用
   - 悬空（dangling）= HTML引用 - 实际文件 → 引用但不存在
4. **PNG尺寸校验**：用PIL读取PNG实际像素，与HTML中标注的尺寸（如"1200×480"）比对

**输出示例**：
```
Actual files:   51
HTML references: 51
Orphans: 0
Dangling: 0
PNG dimension check:
  All PNG dimensions match labels
```

**注意事项**：
- 排除`<code>`标签内的示例代码引用（如`<link rel="icon" href="favicon.ico">`在说明文字中）——脚本已用 `re.sub(r'<code[^>]*>.*?</code>', '', html)` 处理
- 路径分隔符统一为`/`（HTML用正斜杠，Windows实际文件用反斜杠，比对前需统一）

---

### BA4-03 清理整理 · 清理清单范本

```markdown
## 清理清单

### 需删除的辅助文件
| 文件 | 类型 | 原因 |
|------|------|------|
| 01_核心标志/03_纯图标_小尺寸版.svg | 简化版SVG | 渲染辅助文件，不属于交付物 |
| archive/ | 归档目录 | 旧版本备份 |
| .workbuddy/ | 项目配置 | WorkBuddy配置目录 |

### 需去重的文件
| 保留 | 删除 | 原因 |
|------|------|------|
| 01_横版标志.png (600×240) | 01_横版标志_600.png | 字节完全相同（MD5一致） |
| 02_竖版标志.png (400×480) | 02_竖版标志_400.png | 字节完全相同（MD5一致） |
| 03_纯图标.png (480×480) | — | 无重复（480不在_16~_512序列中） |

### 不得删除
- 所有 .svg 文件（交付矢量源）
- 所有 .png 文件（交付位图，除去重外）
- 所有 .ico 文件
- 所有 .html 文件
```

---

### BA4-04 交付打包 · 交付报告范本

```markdown
## 交付报告

**项目**：{{公司全称}} 品牌视觉资产
**交付位置**：Downloads\{{公司简称}}品牌资产\（请根据实际路径调整）
**展示页**：{{公司简称}}品牌资产.html（双击打开）

### 文件统计
| 类型 | 数量 | 说明 |
|------|------|------|
| HTML | 2 | 展示页 + VI手册 |
| SVG | 33 | 矢量源文件（含3品牌规范+9扩展应用） |
| PNG | 51 | 核心标志21+VI系统18+品牌规范3+扩展应用9 |
| ICO | 1 | favicon多尺寸 |
| **合计** | **87** | |

### 目录结构
01_核心标志/    25个文件（3 SVG + 21 PNG + 1 ICO）
02_商标注册/    12个文件（6 SVG + 6 PNG）
03_数字化应用/  10个文件（5 SVG + 5 PNG）
04_办公文具/    8个文件（4 SVG + 4 PNG）
05_宣传物料/    6个文件（3 SVG + 3 PNG）
06_品牌规范/    6个文件（3 SVG + 3 PNG）
07_环境应用/    6个文件（3 SVG + 3 PNG）
08_产品周边/    6个文件（3 SVG + 3 PNG）
09_多媒体模板/  6个文件（3 SVG + 3 PNG）

### 校验结果
- 文件完整性：87个资源文件，0悬空0遗漏
- PNG尺寸标注：全部与实际像素一致

### 联系信息
{{姓名}} · {{手机}} · {{邮箱}} · {{网址}}
{{地址}}
```

---

### BA4域技术坑

**坑1：Edge file://协议缓存**
- 问题：修改HTML后Edge仍显示旧内容
- 修复：HTML head添加3个禁缓存meta标签（Cache-Control/Pragma/Expires）；建议Ctrl+F5或InPrivate窗口

**坑2：目录树渲染折叠**
- 问题：ASCII目录树（`├──`、`│`、`└──`）显示为一行
- 根因：浏览器默认折叠连续空格
- 修复：CSS添加`white-space: pre`

**坑3：重复PNG文件**
- 问题：`01_横版标志.png`与`01_横版标志_1200.png`字节完全相同
- 根因：渲染脚本同时生成无后缀标准版和有后缀的_1200版，尺寸相同
- 修复：保留无后缀标准版，删除_1200重复版，更新HTML引用和目录树

**坑4：应用场景表格排序与文件夹分类不一致**
- 问题：HTML展示页底部「应用场景总览」表格的行顺序与9个文件夹分类不对应，用户难以建立对应关系
- 根因：表格按场景维度分类（网站/名片/展会等），而非按文件夹维度分类
- 修复：将表格行顺序改为与9个文件夹分类完全一致（01核心标志→02商标注册→...→09多媒体模板），场景描述改为各文件夹包含资产的具体应用场景
- **预防**：生成HTML时，应用场景表格直接按文件夹编号顺序输出

**坑5：HTML中SVG不显示——CSS尺寸问题**
- 问题：HTML展示页中所有SVG显示为破碎图标❌
- 根因：CSS使用`max-width: 100%; max-height: 160px; object-fit: contain`时，SVG的`object-fit`属性在`<img>`标签中行为不可靠，导致所有SVG在HTML中破碎
- 修复：改用显式尺寸 `width: 100%; height: 160px; object-fit: contain; display: block; background: #FFFFFF`
- 触发场景：所有HTML中引用SVG的`<img>`标签
- **检查方法**：CSS中搜索`object-fit`和`max-height`的组合，如有则改为显式`width`+`height`

**坑6：HTML中SVG不显示——SVG XML特殊字符**
- 问题：HTML展示页中特定SVG显示为破碎图标❌
- 根因：SVG文本中含未转义的`&`（如`Specifications & Features`），XML解析器将`&`识别为实体引用开始符，解析失败
- 触发场景：SVG `<text>`标签中包含英文`&`、`<`、`>`、`"`、`'`
- 修复：所有SVG文本中的`&`→`&amp;`、`<`→`&lt;`、`>`→`&gt;`
- **检查命令**：`grep -rn '&[^a-zA-Z#;]' *.svg` 扫描所有SVG中的未转义`&`（排除`&amp;`、`&lt;`等合法实体）
- **影响范围**：仅含英文特殊字符的SVG会受影响（纯中文SVG不会触发）

**坑7：SVG `<defs>` 嵌套导致结构不规范**
- 问题：宣传物料SVG中存在双层`<defs>`嵌套，虽浏览器容忍但非SVG标准
- 根因：生成SVG时误将`<defs>`放入已存在的`<defs>`内；涉及3个宣传物料SVG
- 影响：Inkscape、印刷软件可能解析错误；不符合SVG 1.1标准
- 修复：删除外层多余的`<defs>`标签，保留单层结构
- **检查命令**：`for f in *.svg; do count=$(grep -c '<defs>' "$f"); if [ "$count" -gt 1 ]; then echo "NESTED: $f"; fi; done`

**坑8：SVG中包含占位符文本未替换**
- 问题：`[演示标题]`、`[副标题]`、`[笔记本标题占位]`、`{{标题}}`、`{{副标题}}`等占位符保留在最终SVG中
- 根因：生成SVG时填充了占位符但交付前未替换为实际内容
- 影响：交付物不完整，用户看到占位符而非品牌文案
- **检查命令**：`grep -rn '[\[\{]' *.svg | grep -v 'xlink:href' | grep -v 'font-size' | grep -v 'stop-color' | grep -v 'fill' | grep -v 'stroke'`
- 修复：交付前统一扫描并用实际文案替换
- **检查命令**：`grep -rn '\[' *.svg */*.svg | grep -v 'xlink:href'`

**坑9：SVG使用emoji字符跨平台不可见**
- 问题：SVG中的emoji（📱✉🌐📍）在Linux服务器、Mac部分字体环境下显示为方块□
- 根因：emoji渲染依赖系统字体；SVG标准不支持emoji字体回退机制
- 影响：名片正面在部分环境中显示异常
- 修复：使用SVG `<path>`绘制图标，或用普通字符替代
- **检查命令**：建议用肉眼检查，或使用 `grep -rn '[\x{1F000}-\x{1FFFF}]' *.svg`（需 GNU grep -P 支持 Unicode 字符类）

**坑10：HTML引用PNG但磁盘文件缺失**
- 问题：HTML展示页引用了8个PNG（名片背面、信纸、Banner、门头、背景板、易拉宝、礼品袋、社交媒体配图），但磁盘上这些PNG不存在
- 根因：渲染阶段遗漏或增量渲染跳过了这些文件；技能声称87个文件，实际仅XX个
- 影响：HTML页面中对应位置显示破损图片❌，用户无法查看SVG在暗色背景下的预览效果
- 修复：先确认SVG存在→删除旧PNG→重新运行`render_svg_to_png.py . --all`
- **预防**：交付前必须执行完整性校验：实际文件数=技能声称数=87，0悬空0遗漏

**坑11：技能声称文件数与实际不一致**
- 问题：技能声称"87个文件（2 HTML + 33 SVG + 51 PNG + 1 ICO）"，但实测项目仅产出XX个，缺XX个
- 根因：文件数量声称基于模板估算，未与实际产出核对
- 影响：交付物不完整，HTML出现破损图片
- 修复：每次交付前用`find . -type f | wc -l`统计实际文件数，与技能声称数比对；技能声称87时必须产出87个
- **预防**：将技能声称数写入requirements.md作为硬性约束，不写"约"或"预期"等模糊表述

**坑12：ICO构建完成但未提取内嵌PNG，HTML展示页缺少ICO多尺寸**
- 问题：ICO文件已生成（含4尺寸），但HTML展示页中无ICO多尺寸展示区域
- 根因：ICO构建后未执行内嵌PNG提取步骤
- 影响：用户无法在展示页中直观看到ICO的4个尺寸效果
- 修复：ICO构建后立即执行`extract_ico_pngs()`从ICO二进制提取4个PNG（16×16/32×32/48×48/64×64）存入01_核心标志目录
- **预防**：将ICO内嵌PNG提取写入BA3-03组装顺序，作为ICO构建后的必选步骤

**坑13：ICO内嵌PNG提取失败——ICO中存的是BMP而非PNG**
- 问题：ICO构建完成后尝试提取PNG但签名不是`\x89PNG`
- 根因：ICO格式允许内嵌BMP图像数据（较旧工具生成），脚本`build_ico()`构建时使用PNG编码，因此提取时一定为PNG；如果ICO来自外部工具（非脚本生成），可能为BMP
- 修复：检查图像数据前4字节：`\x89PNG`→PNG直接提取；其他→解析BMP后用PIL转PNG
