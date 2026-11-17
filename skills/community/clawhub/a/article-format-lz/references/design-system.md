# 微信公众号排版设计系统 — 多风格令牌化

## 排版设计原则（三条底线）

所有组件模板和色值令牌服务于以下三条设计原则。生成排版时必须自检是否违反：

1. **克制装饰**：一篇文章最多 2 种强调色（PRIMARY + ACCENT），渐变仅用于分割线/强调卡/数据卡，不连续堆叠超过 2 个卡片组件，emoji 克制，正文以边框和留白制造层次（box-shadow 微信支持但克制使用）
2. **留白呼吸**：正文每段不超过 5 行（微信）/ 4 行（头条），组件间距 ≥ 8px，章节间距 ≥ 24px，卡片内 padding 16-20px，每 300 字插入小标题
3. **层级清晰**：字号阶梯 24>19>17>15px（各级 ≥ 2px 差距），标题用 PRIMARY 色装饰锚点，正文用 TEXT_BODY 色，一段一意，组件不越级，分割线单篇 ≤ 4 条

> 原则的详细说明和完整规则见 `SKILL.md`「排版设计原则」节。以下技术参数（字体/间距/圆角系统）是原则的量化实现。

---

## 色值令牌替换规则

所有组件模板中使用令牌占位，生成时替换为所选风格的实际色值。

### 令牌定义

| 令牌 | 含义 |
|------|------|
| `PRIMARY` | 主色 — 标题装饰、强调、链接、图标 |
| `ACCENT` | 辅色 — 渐变终点、数据卡片渐变 |
| `LIGHT_BG` | 浅底 — 引用块背景、提示框背景、卡片底色 |
| `PAGE_BG` | 页面背景底色 |
| `TEXT` | 标题文字色 |
| `MUTED` | 辅助文字色 — 副标题、署名、版权 |
| `TEXT_BODY` | 正文段落色 |
| `CODE_BG` | 代码块深色背景 |

### 通用风格色值映射表（7种）

| 令牌 | Linear蓝紫（默认） | 墨韵素雅 | 暖阳咖啡 | 青竹墨绿 | 莫兰迪雾 | 晨曦珊瑚 | 深蓝学术 |
|------|-------------------|----------|----------|----------|----------|----------|----------|
| `PRIMARY` | `#5B6FED` | `#2C2C2A` | `#8B5E3C` | `#2D5016` | `#534AB7` | `#D85A30` | `#0C447C` |
| `ACCENT` | `#764ba2` | `#5F5E5A` | `#C4956C` | `#639922` | `#7F77DD` | `#F0997B` | `#378ADD` |
| `LIGHT_BG` | `#f5f6fa` | `#F1EFE8` | `#F5E6D3` | `#EAF3DE` | `#EEEDFE` | `#FAECE7` | `#E6F1FB` |
| `PAGE_BG` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` |
| `TEXT` | `#1a1a2e` | `#2C2C2A` | `#6B4226` | `#27500A` | `#3C3489` | `#993C1D` | `#0C447C` |
| `MUTED` | `#999` | `#888780` | `#A07350` | `#639922` | `#534AB7` | `#D85A30` | `#185FA5` |
| `TEXT_BODY` | `#333` | `#5F5E5A` | `#8B5E3C` | `#3B6D11` | `#534AB7` | `#993C1D` | `#0C447C` |
| `CODE_BG` | `#1a1a2e` | `#1e1e1e` | `#2d1f12` | `#1a2a10` | `#1a1a2e` | `#2a1810` | `#0a1929` |

### 节日风格色值映射表（8种）

> 节日风格复用全部通用组件模板（组件1-23），仅替换令牌色值。色彩取自传统文化意象。

| 令牌 | 元旦·冰蓝迎新 | 春节·中国红金 | 元宵·暖灯红橙 | 清明·柳绿清雅 | 端午·艾绿五彩 | 中秋·月夜金桂 | 五一·活力橙绿 | 国庆·华诞红金 |
|------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| `PRIMARY` | `#4A90D9` | `#D4202A` | `#E8553A` | `#5E8B6E` | `#3A7D5C` | `#4A559E` | `#E8822E` | `#C0152B` |
| `ACCENT` | `#E6B422` | `#D4AF37` | `#F2A93B` | `#8FAE8B` | `#D45B3E` | `#E0B049` | `#4CA85A` | `#E6B422` |
| `LIGHT_BG` | `#EEF4FB` | `#FCEDE9` | `#FDEDE6` | `#EEF3ED` | `#E8F2EC` | `#EEF0FA` | `#FEF3E8` | `#FCEDEB` |
| `PAGE_BG` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` |
| `TEXT` | `#1F3A5F` | `#A30E19` | `#C2402B` | `#3A5A46` | `#1E5A3E` | `#2A3568` | `#C25E12` | `#8E0F1C` |
| `MUTED` | `#7A94B0` | `#C49A3E` | `#D98B3A` | `#8AA091` | `#C0763E` | `#B08D3C` | `#7BA85C` | `#C49A3E` |
| `TEXT_BODY` | `#2C4660` | `#8A1A1A` | `#9B3A2E` | `#4A6353` | `#2C5A45` | `#343E6E` | `#8A5A2E` | `#7A1622` |
| `CODE_BG` | `#1A2A3A` | `#4A0E0E` | `#3D1410` | `#1E2E24` | `#15301F` | `#161B3A` | `#3D2410` | `#3D0A0E` |

### 季节风格色值映射表（4种）

> 季节风格复用全部通用组件模板（组件1-23），仅替换令牌色值。色彩取自二十四节气与物候意象，四季各成一派：春之新芽樱粉、夏之海风晴蓝、秋之枫丹麦金、冬之雪霁冰蓝。

| 令牌 | 春·新芽樱粉 | 夏·海风晴蓝 | 秋·枫丹麦金 | 冬·雪霁冰蓝 |
|------|------------|------------|------------|------------|
| `PRIMARY` | `#7FB069` | `#0E9DCB` | `#C75B39` | `#2E6B9E` |
| `ACCENT` | `#F48FB1` | `#FF9F40` | `#E0A526` | `#7EB8D4` |
| `LIGHT_BG` | `#F2F7EC` | `#E8F6FB` | `#FBF1E6` | `#E8F1F8` |
| `PAGE_BG` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` | `#FAFAFA` |
| `TEXT` | `#4A5D3A` | `#0A6E92` | `#9E3B22` | `#1C3B54` |
| `MUTED` | `#A8C08A` | `#5CB8D6` | `#D08B4F` | `#6A8BA3` |
| `TEXT_BODY` | `#5A6B45` | `#0C7C9E` | `#A8492B` | `#284D6E` |
| `CODE_BG` | `#2E3A22` | `#0A2E3A` | `#2E1A12` | `#0F1A26` |

### 主题风格色值映射表（4种）

> 主题风格复用全部通用组件模板（组件1-23），仅替换令牌色值，并叠加各自的风格特色微调（见文末「风格特色微调」）。色彩取自用户指定的 4 类主题意象：官方权威、肃穆黑白、赛博克制霓虹、磨砂翡翠。

| 令牌 | 官方·严谨庄重 | 讣告·肃穆黑白 | 赛博·克制霓虹 | 磨砂·翡翠凝碧 |
|------|--------------|--------------|--------------|--------------|
| `PRIMARY` | `#1A4F8B` | `#333333` | `#0891B2` | `#3D8B6E` |
| `ACCENT` | `#3E6FA3` | `#666666` | `#C026D3` | `#7DC4A0` |
| `LIGHT_BG` | `#EEF3F8` | `#F0F0F0` | `#F0F9FB` | `#EDF7F2` |
| `PAGE_BG` | `#FAFAFA` | `#FFFFFF` | `#FAFBFC` | `#FAFAFA` |
| `TEXT` | `#14365E` | `#000000` | `#0F172A` | `#1E4A38` |
| `MUTED` | `#6E89A8` | `#888888` | `#64748B` | `#6BAA8E` |
| `TEXT_BODY` | `#27425F` | `#222222` | `#1E293B` | `#2E5C48` |
| `CODE_BG` | `#102A45` | `#1A1A1A` | `#0F172A` | `#0F1F18` |

> 赛博·克制霓虹额外使用渐变令牌 `NEON_GRAD = linear-gradient(90deg,#06b6d4,#d946ef)`，用于标题与核心洞察的渐变文字（模拟霓虹，不加 box-shadow，避免光污染）。磨砂·翡翠凝碧信息卡片用 LIGHT_BG 实色 `#EDF7F2` + `1px solid #C5DED2` 浅翡翠描边模拟磨砂质感，圆角加大至 12px、padding 加大至 18-22px 用留白替代透明度。详见文末「风格特色微调」。

### 节日风格自动匹配关键词

当用户未指定具体风格、且文章内容含以下关键词时，自动选用对应节日风格：

| 节日风格 | 触发关键词 |
|----------|-----------|
| 元旦·冰蓝迎新 | 元旦、新年、跨年、迎新、年终 |
| 春节·中国红金 | 春节、过年、除夕、新春、年味、拜年、春联、红包 |
| 元宵·暖灯红橙 | 元宵、汤圆、灯会、猜灯谜、花灯 |
| 清明·柳绿清雅 | 清明、踏青、青团、祭祖、扫墓、柳 |
| 端午·艾绿五彩 | 端午、粽子、龙舟、屈原、艾草、菖蒲 |
| 中秋·月夜金桂 | 中秋、月饼、赏月、团圆、桂花、婵娟 |
| 五一·活力橙绿 | 五一、劳动节、小长假、出游、露营、假期 |
| 国庆·华诞红金 | 国庆、十一、华诞、祖国、升旗、盛世、举国 |

> 匹配优先级：**用户显式指定 > 节日关键词命中 > 季节关键词命中 > 主题关键词命中 > 内容类型自动匹配 > 默认 Linear 蓝紫**。若一篇含多个节日关键词（如"春节元宵对比"），以文章主标题/核心主题判断；无法判断时用 AskUserQuestion 引导。

### 季节风格自动匹配关键词

当用户未指定具体风格、且文章主题为四季 / 二十四节气 / 物候节气时，自动选用对应季节风格：

| 季节风格 | 触发关键词 |
|----------|-----------|
| 春·新芽樱粉 | 春、立春、雨水、惊蛰、春分、谷雨、春游、踏青、樱花、新芽、春风、春回大地、春耕 |
| 夏·海风晴蓝 | 夏、立夏、小满、芒种、夏至、小暑、大暑、消暑、防暑、夏日、暑假、海风、清凉、蝉鸣 |
| 秋·枫丹麦金 | 秋、立秋、处暑、白露、秋分、寒露、霜降、丰收、贴秋膘、枫叶、桂花、秋日、秋高气爽 |
| 冬·雪霁冰蓝 | 冬、立冬、小雪、大雪、冬至、小寒、大寒、下雪、围炉、供暖、寒假、腊月、凛冬、冬藏 |

> 季节与节日存在交集：清明（节气/清明节）、中秋（秋月/中秋节）。若文章主题明确为「节日」本身（如清明祭扫、中秋赏月团圆），优先命中节日风格；若文章为节气科普、物候记录、季节生活方式等通用季节性内容，则命中季节风格。无法判断时用 AskUserQuestion 引导。

### 主题风格自动匹配关键词

当用户未指定具体风格、且文章主题属于以下特定领域时，自动选用对应主题风格：

| 主题风格 | 触发关键词 |
|----------|-----------|
| 官方·严谨庄重 | 官方、政府、政务、公告、通报、白皮书、政策、文件、权威发布、新闻联播、声明 |
| 讣告·肃穆黑白 | 讣告、逝世、悼念、哀悼、缅怀、沉痛、追思、唁电、千古、享年 |
| 赛博·克制霓虹 | 赛博、极客、黑客、代码、终端、开源、AI工程、技术极客、霓虹、极客前线 |
| 磨砂·翡翠凝碧 | 磨砂、亚克力、毛玻璃、翡翠、玉石、温润、通透、质感、润泽、设计美学、高级感 |

> 匹配优先级：**用户显式指定 > 节日关键词命中 > 季节关键词命中 > 主题关键词命中 > 内容类型自动匹配 > 默认 Linear 蓝紫**。若文章同时命中多个主题（如「政务公告+悼念」），以主标题/核心意图判断；无法判断时用 AskUserQuestion 引导。

> 主题风格与内容类型存在重叠（如「赛博」也可能命中技术类内容）。主题风格优先于内容类型自动匹配——一旦命中主题关键词即用对应主题风格，不再回落到内容类型（Linear 蓝紫等）。

### 透明度拼接规则

强调卡片需要带透明度的色值，手动拼接：

- `ACCENT22` = ACCENT + `22`（如 `#764ba222`）
- `PRIMARY11` = PRIMARY + `11`（如 `#5B6FED11`）
- `PRIMARY33` = PRIMARY + `33`（如 `#5B6FED33`）

## 字体系统

默认字体栈（所有风格通用）：

```
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
```

墨韵素雅风格使用衬线字体栈：

```
font-family: 'Noto Serif SC', 'Source Han Serif', Georgia, 'Times New Roman', serif;
```

| 元素 | 字号 | 字重 | 行高 | 字间距 |
|------|------|------|------|--------|
| 主标题 H1 | 24px | 700 | 1.5 | 1px |
| 二级标题 H2 | 19px | 700 | — | — |
| 三级标题 H3 | 17px | 600 | — | — |
| 正文 P | 15px | 400 | 2.0 | 0.5px |
| 引用文字 | 15px | 400 italic | 1.9 | — |
| 副标题/署名 | 13px | 400 | 1.6 | — |
| 标签胶囊 | 12px | 600 | — | 2px |
| 数据大字 | 36px | 800 | 1.2 | — |
| 提示框正文 | 14px | 400 | 1.85 | — |
| 对比栏正文 | 12px | 400 | 1.7 | — |

## 间距系统

| 用途 | 值 |
|------|-----|
| section 横向 padding | 6px |
| 组件纵向间距 | 8-12px |
| 章节间距 | 24px |
| 卡片内 padding | 16-20px |
| 元素间隙（gap） | 8-12px |

## 圆角系统

| 元素 | 圆角 |
|------|------|
| 小标签/胶囊 | 20px（全圆角） |
| 编号方块 | 6px |
| 小圆点 | 50%（圆形） |
| 卡片/提示框 | 10-12px |
| 引用块 | 0 8px 8px 0（左直角） |

> 暖阳咖啡风格：所有 10px 圆角调为 14px，6px 调为 10px。

---

## 组件代码模板

以下模板使用令牌占位，生成时替换为所选风格的实际色值。

### 1. 主标题区

```html
<section style="padding:32px 6px 8px;text-align:center">
  <section style="display:inline-block;padding:4px 16px;background:PRIMARY;border-radius:20px;margin-bottom:16px">
    <span style="font-size:12px;color:#fff;letter-spacing:2px;font-weight:600">标签文字</span>
  </section>
  <h1 style="font-size:24px;font-weight:700;color:TEXT;line-height:1.5;letter-spacing:1px;margin:0">文章主标题</h1>
  <section style="margin-top:12px">
    <span style="font-size:13px;color:MUTED">副标题或一句话描述</span>
  </section>
</section>
```

### 2. 分割线（渐变）

```html
<section style="padding:16px 6px">
  <section style="height:1px;background:linear-gradient(to right,transparent,PRIMARY,transparent)"></section>
</section>
```

### 3. 导语引用块

```html
<section style="padding:8px 6px 20px">
  <section style="background:LIGHT_BG;border-left:3px solid PRIMARY;border-radius:0 8px 8px 0;padding:16px 20px">
    <p style="font-size:15px;color:TEXT_BODY;line-height:1.9;margin:0">
      导语文字内容，用于文章开头的引言或摘要。
    </p>
  </section>
</section>
```

### 4. 二级标题

```html
<section style="padding:24px 6px 12px">
  <section style="display:flex;align-items:center;gap:10px">
    <section style="width:6px;height:22px;background:PRIMARY;border-radius:3px;flex-shrink:0"></section>
    <h2 style="font-size:19px;font-weight:700;color:TEXT;margin:0">章节标题</h2>
  </section>
</section>
```

### 5. 三级标题

```html
<section style="padding:20px 6px 8px">
  <section style="display:flex;align-items:center;gap:8px">
    <section style="width:20px;height:20px;background:PRIMARY;border-radius:6px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
      <span style="font-size:12px;color:#fff;font-weight:700">1.1</span>
    </section>
    <h3 style="font-size:17px;font-weight:600;color:TEXT;margin:0">小节标题</h3>
  </section>
</section>
```

### 6. 正文段落

```html
<section style="padding:4px 6px 12px">
  <p style="font-size:15px;color:TEXT_BODY;line-height:2;margin:0;letter-spacing:0.5px">
    正文文字内容。
  </p>
</section>
```

### 7. 行内强调

```html
<!-- 主色加粗文字 -->
<span style="color:PRIMARY;font-weight:600">强调文字</span>

<!-- 主色底高亮标签 -->
<span style="display:inline-block;padding:2px 8px;background:LIGHT_BG;border-radius:4px;font-size:13px;color:PRIMARY;font-weight:600">术语标签</span>
```

### 8. 强调卡片（核心洞察）

```html
<section style="padding:8px 6px 12px">
  <section style="background:linear-gradient(135deg,ACCENT22,PRIMARY11);border:1px solid PRIMARY33;border-radius:10px;padding:16px 20px">
    <p style="font-size:15px;color:TEXT;line-height:1.9;margin:0;font-weight:500">
      <span style="color:PRIMARY;font-weight:700">核心洞察：</span>强调内容文字。
    </p>
  </section>
</section>
```

### 9. 无序列表（圆点风格）

```html
<section style="padding:8px 6px 12px">
  <p style="font-size:15px;color:TEXT_BODY;line-height:1.9;margin:0 0 10px">列表标题（可选）：</p>
  <section style="padding-left:4px">
    <!-- 重复以下 section 为每个列表项 -->
    <section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px">
      <section style="width:8px;height:8px;background:PRIMARY;border-radius:50%;margin-top:9px;flex-shrink:0"></section>
      <p style="font-size:15px;color:TEXT_BODY;line-height:1.9;margin:0"><span style="font-weight:600;color:TEXT">项标题：</span>项描述内容</p>
    </section>
  </section>
</section>
```

### 10. 无序列表（箭头风格）

```html
<section style="padding:8px 6px 12px">
  <section style="padding-left:4px">
    <!-- 重复以下 section 为每个列表项 -->
    <section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px">
      <section style="min-width:16px;font-size:14px;color:PRIMARY;line-height:1.9;flex-shrink:0">▸</section>
      <p style="font-size:15px;color:TEXT_BODY;line-height:1.9;margin:0"><span style="font-weight:600;color:TEXT">项标题：</span>项描述内容</p>
    </section>
  </section>
</section>
```

### 11. 有序列表

```html
<section style="padding:8px 6px 12px">
  <p style="font-size:15px;color:TEXT_BODY;line-height:1.9;margin:0 0 12px">列表标题（可选）：</p>
  <section style="padding-left:4px">
    <!-- 重复以下 section 为每个列表项，编号递增 -->
    <section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px">
      <section style="min-width:24px;height:24px;background:PRIMARY;border-radius:6px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
        <span style="font-size:13px;color:#fff;font-weight:700">1</span>
      </section>
      <p style="font-size:15px;color:TEXT_BODY;line-height:1.9;margin:0;padding-top:2px"><span style="font-weight:600;color:TEXT">项标题：</span>项描述内容</p>
    </section>
  </section>
</section>
```

### 12. 引用块（带来源）

> 引用块左色条用 `border-left` 实现。`position:absolute` 微信编辑器实测支持粘贴后正常渲染，但 border-left 更简洁可维护。

```html
<section style="padding:8px 6px 12px">
  <section style="background:LIGHT_BG;border-left:4px solid PRIMARY;border-radius:0 10px 10px 0;padding:20px 20px 20px 24px">
    <p style="font-size:15px;color:#555;line-height:1.9;margin:0;font-style:italic">
      "引用文字内容。"
    </p>
    <p style="font-size:13px;color:#999;line-height:1.6;margin:8px 0 0;text-align:right">—— 来源署名</p>
  </section>
</section>
```

### 13. 信息提示框

```html
<section style="padding:8px 6px 12px">
  <section style="display:flex;align-items:flex-start;gap:12px;background:LIGHT_BG;border-radius:10px;padding:14px 16px">
    <section style="min-width:20px;font-size:16px;line-height:1.5">💡</section>
    <p style="font-size:14px;color:TEXT_BODY;line-height:1.85;margin:0">
      <span style="font-weight:700;color:PRIMARY">提示：</span>信息提示内容。
    </p>
  </section>
</section>
```

### 14. 警告提示框

> 警告框统一使用橙色系，不随风格变化，因为警告语义需要固定的视觉信号。

```html
<section style="padding:8px 6px 12px">
  <section style="display:flex;align-items:flex-start;gap:12px;background:#FFF8F0;border-radius:10px;padding:14px 16px">
    <section style="min-width:20px;font-size:16px;line-height:1.5">⚠️</section>
    <p style="font-size:14px;color:#6a5a4a;line-height:1.85;margin:0">
      <span style="font-weight:700;color:#e8923c">注意：</span>警告提示内容。
    </p>
  </section>
</section>
```

### 15. 数据高亮卡片

```html
<section style="padding:8px 6px 12px">
  <section style="background:linear-gradient(135deg,PRIMARY,ACCENT);border-radius:12px;padding:24px 20px;text-align:center">
    <p style="font-size:36px;font-weight:800;color:#fff;margin:0;line-height:1.2">87.3%</p>
    <p style="font-size:14px;color:#ffffffcc;margin:8px 0 0;line-height:1.6">数据说明文字</p>
  </section>
</section>
```

### 16. 对比双栏

```html
<section style="padding:8px 6px 12px">
  <section style="display:flex;gap:10px">
    <section style="flex:1;background:LIGHT_BG;border-radius:10px;padding:14px;text-align:center">
      <p style="font-size:13px;color:PRIMARY;font-weight:700;margin:0 0 6px">☁️ 左栏标题</p>
      <p style="font-size:12px;color:#666;line-height:1.7;margin:0">特点1<br>特点2<br>特点3<br>特点4</p>
    </section>
    <section style="flex:1;background:#f0fff4;border-radius:10px;padding:14px;text-align:center">
      <p style="font-size:13px;color:#00a663;font-weight:700;margin:0 0 6px">📱 右栏标题</p>
      <p style="font-size:12px;color:#666;line-height:1.7;margin:0">特点1<br>特点2<br>特点3<br>特点4</p>
    </section>
  </section>
</section>
```

### 17. 关键要点回顾

```html
<section style="padding:8px 6px 12px">
  <section style="background:LIGHT_BG;border-radius:10px;padding:16px 20px">
    <p style="font-size:14px;font-weight:700;color:TEXT;margin:0 0 12px">📌 关键要点回顾</p>
    <!-- 重复以下 section 为每个要点 -->
    <section style="margin-bottom:8px">
      <p style="font-size:14px;color:#555;line-height:1.8;margin:0"><span style="color:PRIMARY;font-weight:700">01</span> &nbsp; 要点内容</p>
    </section>
  </section>
</section>
```

### 18. 底部版权区

```html
<section style="padding:24px 6px 32px">
  <section style="height:1px;background:#e8e8e8;margin-bottom:20px"></section>
  <section style="text-align:center">
    <p style="font-size:13px;color:#999;line-height:1.8;margin:0">
      版权声明文字
    </p>
    <section style="margin-top:12px">
      <span style="display:inline-block;padding:4px 12px;background:LIGHT_BG;border-radius:20px;font-size:12px;color:PRIMARY;font-weight:600">标签文字</span>
    </section>
  </section>
</section>
```

### 19. 代码块（深色背景 + 语法高亮）

> 禁止用 `<pre>` + `white-space: pre-wrap`，微信编辑器不保留 `white-space` 属性，换行会丢失。改用 `<section>` + 显式 `<br>` 换行，缩进用 `&nbsp;` 替代空格。

```html
<section style="padding:4px 6px 12px">
  <section style="background:CODE_BG;border-radius:10px;padding:16px 18px;overflow-x:auto">
    <section style="font-family:'SF Mono',Monaco,Menlo,Consolas,monospace;font-size:12.5px;color:#c8d3f5;line-height:1.75;margin:0">
      <span style="color:#6b7394">// 注释文字</span><br>
      <span style="color:#c792ea">const</span> <span style="color:#82aaff">example</span> = <span style="color:#c3e88d">"hello"</span>;<br>
      <span style="color:#c792ea">console</span>.log(example);
    </section>
  </section>
</section>
```

**语法高亮色值参考（所有风格统一）：**

| 元素 | 色值 |
|------|------|
| 注释 | `#6b7394` |
| 关键字 | `#c792ea` |
| 函数名 | `#82aaff` |
| 字符串 | `#c3e88d` |
| 布尔值 | `#ff9cac` |
| 默认文字 | `#c8d3f5` |

> 每行代码之间用 `<br>` 显式换行；行首缩进用 `&nbsp;` 拼接（1 个空格 = `&nbsp;`）。

### 20. 表格

> **表头样式规则**：`<th>` 不使用背景色，字体为黑色加粗（`color:#000;font-weight:700`），边框使用中性灰（`#d0d0d0`）。这样避免了微信编辑器剥离 `<tr>` background 导致的表头背景丢失问题，同时视觉更简洁。
>
> **斑马行规则**：`<td>` 的 `background` 必须放在每个 `<td>` 上，**不能放在 `<tr>` 上**。微信编辑器会剥离 `<tr>` 的 background 属性。

```html
<section style="padding:8px 6px 12px">
  <section style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-size:13px">
      <thead>
        <tr>
          <th style="padding:8px 12px;color:#000;font-weight:700;text-align:left;border:1px solid #d0d0d0">列标题</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="background:LIGHT_BG;padding:8px 12px;color:TEXT;border:1px solid #e0e0e0">单元格内容</td>
        </tr>
        <tr>
          <td style="padding:8px 12px;color:TEXT;border:1px solid #e0e0e0">单元格内容</td>
        </tr>
      </tbody>
    </table>
  </section>
</section>
```

> 所有风格通用此表格组件。宽表格通过 `overflow-x:auto` 支持横向滚动。**每行的每个 `<td>` 都需要单独设置 `background`**，不能用 `<tr style="background:...">` 替代。`<th>` 统一使用黑字加粗无背景，不随风格变化。

### 21. 进度条（能力画像/数据评估）

> 三栏 flex 布局：标签 + 轨道 + 数值。填充条内可显示描述文字。颜色语义化（绿=优/蓝=良/橙=中/红=差），不随风格变化。
>
> **兼容性要点**：
> - 轨道必须加 `overflow:hidden` 约束填充条不溢出
> - 填充条高度用显式 `height:24px`，不用 `height:100%`
> - 间距用 `margin` 不用 `gap`（旧版客户端兼容）
> - 填充条文字垂直居中用 `line-height:24px`（与 height 同值），不用 flex

```html
<section style="padding:8px 6px 12px">
  <section style="display:flex;align-items:center;margin:0 0 14px 0;">
    <section style="width:80px;font-size:13px;color:#4a4a4a;text-align:right;margin:0 8px 0 0;flex-shrink:0;">
      能力标签
    </section>
    <section style="flex:1;height:24px;background:#f0f0f5;border-radius:100px;overflow:hidden;">
      <section style="height:24px;width:90%;background:#3b82f6;border-radius:100px;font-size:11px;color:#fff;font-weight:600;line-height:24px;padding-left:10px;overflow:hidden;">描述文字</section>
    </section>
    <section style="width:72px;font-size:13px;font-weight:700;color:#3b82f6;text-align:left;margin:0 0 0 8px;flex-shrink:0;">
      90%
    </section>
  </section>
  <!-- 重复以上 section 为每条进度条，替换 width/背景色/描述/数值 -->
</section>
```

**颜色语义（不随风格变化）：**

| 评级 | 颜色 | 色值 | width 参考 |
|------|------|------|------------|
| 优秀 | 绿色 | `#10b981` | 90-100% |
| 良好 | 蓝色 | `#3b82f6` | 70-89% |
| 中等 | 橙色 | `#f59e0b` | 50-69% |
| 较差 | 红色 | `#ef4444` | <50% |

> 标签宽度根据文字长度调整（5字用72px，6字用80px）。数值列宽度根据内容调整（百分比用60px，带单位用72px）。填充条窄时文字被 `overflow:hidden` 裁切，关键信息在标签和数值列。

---

## 宽表处理策略（表格替代形态决策树）

当表格出现以下情况时，**不应使用组件20（表格）**，改用卡片形态：

| 情况 | 改用方案 | 组件 |
|------|----------|------|
| **≥5 列** 或含**长文本列**（>8 字会换行） | 信息卡片（每行一卡）【首选】 | 组件22 |
| 行数很多（>8 行）想更省空间 | 紧凑卡片（卡内属性横排 `flex:1`） | 组件22 变体 |
| 仅 2~3 列且偏文字说明 | 键值列表 | 组件23 |
| 含数值/分值列 | 进度条可视化（分数条嵌入卡片） | 组件21 |
| ≤4 列且内容短 | 维持组件20 表格 | 组件20 |

**头条适配**：头条为纯语义 HTML（无 inline style），卡片形态用 `<blockquote>` 实现（见 T16/T17）：

- 进度条视觉在头条无法渲染 → 分值降级为「数值 + 等级词」（如 `1.0 优秀` / `0.85 良好` / `0.0 失败`）
- 头条算法敏感，避免过度装饰；`<blockquote>` 自带左侧竖条即满足卡片视觉

### 22. 信息卡片（宽表/长内容替代 · 每行一卡）

> 适用：表格 **≥5 列**，或含**长文本列**（某列文字 >8 字会换行挤压）导致窄屏拥挤时。将每一**行**转为一张卡片，列标题作卡内 `label`。这是宽表首选替代形态。
>
> **结构**：卡片（浅底圆角）→ 标题行（关键列 + 评价标签）→ 其余列用 flex 横排 `label:value`。
> **兼容性**：复用进度条已验证特性 —— `display:flex` ✅ / `margin` 间距 ✅ / 不用 `gap` / 不用 `height:100%`。

```html
<section style="padding:8px 6px 12px">
  <!-- 每张卡片 = 表格一行，重复即可 -->
  <section style="background:LIGHT_BG;border:1px solid #e6e8f0;border-radius:10px;padding:14px 16px;margin:0 0 10px">
    <section style="display:flex;align-items:baseline;margin:0 0 10px">
      <span style="font-size:15px;font-weight:700;color:TEXT;margin:0 8px 0 0">行标题/关键列</span>
      <span style="font-size:12px;color:#00a663;font-weight:600">✅ 评价标签</span>
    </section>
    <section style="display:flex;margin:0 0 6px">
      <span style="width:64px;font-size:12px;color:MUTED;flex-shrink:0">列名A</span>
      <span style="font-size:13px;color:TEXT;flex:1">值A</span>
    </section>
    <section style="display:flex;margin:0">
      <span style="width:64px;font-size:12px;color:MUTED;flex-shrink:0">列名B</span>
      <span style="font-size:13px;color:TEXT;flex:1">值B</span>
    </section>
  </section>
</section>
```

> 行数很多（>8）想更省空间时，卡内数值列改用 `display:flex` 横排等分（每个 `flex:1`，见下方"紧凑卡片"说明），而非竖排 label:value。

### 23. 键值列表（2~3 列文字说明表替代）

> 适用：仅 **2~3 列**、且内容偏**文字说明**（如 维度/内容/方法）。左侧竖条 + 上标题 + 下说明。
> **兼容性**：`border-left` ✅ 完全支持（与引用块同源方案）。

```html
<section style="padding:8px 6px 12px">
  <section style="border-left:3px solid PRIMARY;padding:2px 0 2px 14px">
    <section style="margin:0 0 14px">
      <p style="font-size:14px;font-weight:700;color:TEXT;margin:0 0 4px">条目标题</p>
      <p style="font-size:13px;color:#555;line-height:1.7;margin:0">说明文字内容</p>
      <p style="font-size:12px;color:MUTED;line-height:1.6;margin:4px 0 0">方法：补充信息</p>
    </section>
    <!-- 重复每个条目 -->
  </section>
</section>
```

---

## 风格特色微调

### 墨韵素雅 — 衬线字体

所有组件的 `style` 中添加：
```
font-family:'Noto Serif SC','Source Han Serif',Georgia,'Times New Roman',serif
```
标题区额外增加 `letter-spacing:2px` 增强留白感。

### 暖阳咖啡 — 圆角加大

所有 `border-radius`：`10px` → `14px`，`6px` → `10px`，营造柔和手作感。

### 青竹墨绿 — 辅色列表标记

无序列表圆点可改用辅色 `#639922`，或保持主色不变。

### 莫兰迪雾 — 降饱和处理

所有文字色在令牌基础上加 `opacity:0.9` 微调，增强雾蒙蒙的质感。

### 晨曦珊瑚 — 暖色描边替代

卡片组件可用 `border:1px solid #F5C4B3` 替代渐变底，营造更轻盈的暖意。

### 深蓝学术 — 数据密集

优先使用组件20（表格）展示数据密集型内容。表头统一黑字加粗无背景。

### 官方·严谨庄重 — 衬线权威

所有组件的 `style` 中添加衬线字体栈：

```
font-family:'Noto Serif SC','Source Han Serif',Georgia,'Times New Roman',serif
```

主标题额外增加 `letter-spacing:2px`，分割线改用实色深蓝（`PRIMARY` 值 `#1A4F8B`）增强公文感。无彩色装饰，色彩仅作微弱锚点。

### 讣告·肃穆黑白 — 纯黑白无彩色

- 完全不使用任何彩色：所有令牌退化为灰阶（PRIMARY `#333`、TEXT `#000`、PAGE_BG `#FFF`）。
- 所有组件 `style` 添加衬线字体栈（同官方）。
- 最大留白：章节间距、组件纵向间距取上限；标题加粗黑体，无圆点/渐变装饰。
- 强调用「加粗黑体 + 引号」而非色块。

### 赛博·克制霓虹 — 渐变文字模拟霓虹

- **不加 `box-shadow` / `text-shadow`**（光污染，与赛博克制霓虹的纯净感冲突）。
- 标题与主色强调文字用渐变文字：`<span>` 标签与核心洞察关键词 `background:NEON_GRAD;-webkit-background-clip:text;background-clip:text;color:transparent`。
- 数据高亮卡片（组件15）背景用 `linear-gradient(135deg,#06b6d4,#d946ef)`；信息卡片（组件22）用半透明 `linear-gradient(135deg,rgba(8,145,178,0.10),rgba(192,38,211,0.10))` + `1px solid #0891B244` 模拟发光描边。
- 仅浅底 + 克制霓虹，正文仍以深蓝黑 `#0F172A` 保证可读性，避免夜店式强对比。

### 磨砂·翡翠凝碧 — 实色翡翠底 + 细描边

> **重要**：公众号编辑器没有页面背景色，半透明白卡片贴在白底上会"消失"。因此磨砂风格用 LIGHT_BG 实色 + 细描边模拟磨砂质感，**不用半透明**。

- 所有卡片组件（强调卡、信息卡片、提示框、要点回顾）背景用 LIGHT_BG 实色 `#EDF7F2`（翡翠浅绿），**不用半透明**。
- 卡片描边用 `1px solid #C5DED2`（浅翡翠，与 PRIMARY 同系），在白底上可见但不抢眼，模拟磨砂边缘。
- 卡片圆角加大至 `12px`（其他风格默认 10px），强化柔和通透感。
- 卡片内 padding 加大至 `18-22px`（其他风格 14-16px），用留白代替透明度营造呼吸感。
- PAGE_BG 统一 `#FAFAFA`（与其他风格一致），主色 `#3D8B6E` 翡翠绿作锚点。
- 整体克制干净，不堆色彩，翡翠绿温润如玉，与冬·雪霁冰蓝的冷蓝形成明确色相对比。

---

## 页面外壳模板

完整 HTML 文件的外壳结构（包含工具栏 + 正文区域 + 复制脚本）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>文章标题</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif; background: #f0f0f3; padding: 40px 16px; }
  .page-wrap { max-width: 680px; margin: 0 auto; }
  .toolbar { background: #fff; border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .toolbar h1 { font-size: 18px; color: TEXT; margin-bottom: 6px; }
  .toolbar p { font-size: 13px; color: #888; line-height: 1.6; }
  .copy-btn { display: inline-block; margin-top: 12px; padding: 10px 24px; background: PRIMARY; color: #fff; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; transition: background .2s; }
  .copy-btn:hover { background: PRIMARY; }
  .preview-label { font-size: 12px; color: #aaa; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; padding-left: 4px; }
  .wechat-content { background: PAGE_BG; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
</style>
</head>
<body>
<div class="page-wrap">
  <div class="toolbar">
    <h1>文章标题</h1>
    <p>风格名称 · 全内联样式 · 复制下方预览区内容直接粘贴到公众号编辑器即可</p>
    <button class="copy-btn" onclick="copyContent()">一键复制排版内容</button>
  </div>
  <div class="preview-label">— 预览区 —</div>
  <div class="wechat-content" id="wechat-content">
    <!-- ===== 所有排版组件放在这里 ===== -->
  </div>
</div>
<script>
function copyContent() {
  var content = document.getElementById('wechat-content');
  var range = document.createRange();
  range.selectNodeContents(content);
  var selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
  try {
    document.execCommand('copy');
    var btn = document.querySelector('.copy-btn');
    var originalText = btn.textContent;
    btn.textContent = '✓ 已复制，可粘贴到公众号编辑器';
    btn.style.background = '#00a663';
    setTimeout(function() {
      btn.textContent = originalText;
      btn.style.background = 'PRIMARY';
    }, 3000);
  } catch (err) {
    alert('复制失败，请手动选中预览区内容复制');
  }
  selection.removeAllRanges();
}
</script>
</body>
</html>
```

> 外壳中的 `PRIMARY`、`TEXT`、`PAGE_BG` 同样替换为所选风格的实际色值。

---

## 微信编辑器兼容性备忘

| CSS 特性 | 兼容性 | 备注 |
|----------|--------|------|
| inline style | ✅ 必须使用 | 不要用 class |
| `display: flex` | ✅ 支持 | section + flex 安全使用，进度条三栏布局核心 |
| `flex:1` / `flex-shrink` | ✅ 支持 | 进度条轨道自适应宽度、标签/数值列固定宽度 |
| `overflow:hidden` | ✅ 支持 | 进度条轨道约束填充条不溢出，填充条约束文字不溢出 |
| `linear-gradient` | ✅ 支持 | 渐变背景正常显示 |
| `border-radius` | ✅ 支持 | 圆角正常 |
| `border-left` | ✅ 完全支持 | 引用块左色条首选方案 |
| `<br>` 换行 | ✅ 完全支持 | 代码块换行唯一可靠方案 |
| `&nbsp;` 缩进 | ✅ 完全支持 | 代码块行首缩进唯一可靠方案 |
| `<section>` 标签 | ✅ 最佳兼容 | 优先使用 section 而非 div |
| emoji | ✅ 支持 | 💡⚠️📌☁️📱 等正常显示 |
| `<tr>` 的 `background` | ❌ 禁止 | 微信会剥离 `<tr>` 上的 background，斑马行背景须放在每个 `<td>` 上 |
| `<th>` 的 `background` | ⚠️ 不推荐 | 虽然支持，但表头统一使用黑字加粗无背景，避免兼容问题和视觉冗余 |
| `<td>` 的 `background` | ✅ 完全支持 | 斑马行背景色放每个 `<td>` 上，不要放 `<tr>` |
| `position: absolute` | ✅ 支持 | 粘贴后正常渲染，引用块推荐 border-left（更简洁） |
| `<pre>` + `white-space` | ❌ 禁止 | 粘贴后换行丢失，改用 `<section>` + `<br>` + `&nbsp;` |
| `box-shadow` | ✅ 支持 | 正常渲染，正文设计上以边框和留白为主 |
| external CSS | ❌ 不支持 | 粘贴时全部丢失 |
| `<script>` | ❌ 仅预览用 | JS 仅用于复制按钮 |

---

# 今日头条排版设计系统 — 纯语义HTML

## 技术原理

头条编辑器基于 **ProseMirror**，使用 schema 白名单机制——所有 inline style 默认被剥离，只有 schema 中声明的语义标签才保留。因此头条排版必须使用**纯语义 HTML**，零 inline style。

### ProseMirror schema 支持的语义标签

| 标签 | 用途 |
|------|------|
| `h1`~`h6` | 标题 |
| `p` | 段落 |
| `strong` / `b` | 加粗 |
| `em` / `i` | 斜体 |
| `u` | 下划线 |
| `s` | 删除线 |
| `ul` / `ol` / `li` | 列表 |
| `blockquote` | 引用 |
| `pre` | 代码块 |
| `hr` | 分割线 |
| `a` | 链接 |
| `img` | 图片 |
| `table`/`thead`/`tbody`/`tr`/`th`/`td` | 表格 |

### 头条禁止使用的（会被 ProseMirror 剥离）

- ❌ 所有 inline style（`style="..."`）
- ❌ `<section>` 嵌套
- ❌ `<div>` 容器
- ❌ `<span>` 带 style
- ❌ `class` 属性

### 头条排版参数

| 参数 | 值 |
|------|-----|
| 正文字号 | 17px（编辑器默认，不可控） |
| 正文色 | #505050（编辑器默认，不可控） |
| 字间距 | 1px（编辑器默认） |
| 行高 | 2（编辑器默认） |
| 每段行数 | 不超过4行 |
| 小标题频率 | 每300字 |
| 层级建立 | 文字符号（◆★▶【】） |
| emoji | 最多2种，不连续 |
| 品牌色 | #F04142（仅预览CSS用，不内联） |

> 头条排版参数由编辑器控制，模板中不设置 inline style。预览页面的 CSS 仅用于浏览器渲染效果，不会被复制。

---

## 头条组件代码模板（T1-T17）

以下模板使用**纯语义 HTML**，零 inline style。预览CSS在外壳 `<style>` 中定义，不进入组件标签。

### T1. 主标题

```html
<h1>【深度解析】文章主标题写在这里</h1>
```

> 用【】符号增强标题视觉权重，不依赖 CSS 装饰。

### T2. 摘要引导

```html
<p><em>一句话摘要，引导读者继续往下看。保持简短，不超过两行。</em></p>
```

> 用 `<em>` 斜体区分摘要与正文。

### T3. 分割线

```html
<hr>
```

> 语义分割线，头条编辑器原生支持。

### T4. 正文段落

```html
<p>正文内容。每段控制在3-4行以内，段与段之间留空行，让页面有呼吸感。</p>
```

> 头条正文参数（17px/行高2/字间距1px）由编辑器控制，模板中不设置 inline style。

### T5. 行内加粗强调

```html
<p>关键数据和结论要<strong>单独成段并加粗</strong>，这是头条算法偏好的排版方式。</p>
```

> 用 `<strong>` 语义加粗，不用 `<span style="font-weight:700">`。

### T6. 章节标题

```html
<h2>◆ 章节小标题</h2>
```

> 用 ◆ 符号引导，不依赖 CSS 竖条装饰。每300字插入一个小标题。

### T7. 子标题

```html
<h3>▶ 子标题</h3>
```

> 用 ▶ 符号引导，用于章节内的进一步分层。

### T8. 核心结论（整段加粗）

```html
<p><strong>核心结论：重要的数据和观点单独成段加粗，让读者即使只扫读也能抓住重点。</strong></p>
```

> 整段用 `<strong>` 包裹，加粗单独成段。头条算法偏好这种信息密度突出方式。

### T9. 无序列表

```html
<ul>
  <li><strong>要点一：</strong>语义列表标签，简洁有力</li>
  <li><strong>要点二：</strong>每项之间空行分隔，阅读不累</li>
  <li><strong>要点三：</strong>关键数据加粗，一眼可见</li>
</ul>
```

> 用 `<ul><li>` 语义列表。li 内可用 `<strong>` 加粗关键词。一篇文章内列表符号保持统一。

### T10. 有序列表

```html
<ol>
  <li>第一步：写完文章内容，理清逻辑结构</li>
  <li>第二步：每300字插入小标题，分段不超过4行</li>
  <li>第三步：关键数据加粗单独成段，配图加图注</li>
  <li>第四步：手机端预览确认，再发布</li>
</ol>
```

> 用 `<ol><li>` 语义有序列表。步骤说明可在 li 内用"第X步："文字引导。

### T11. 引用块

```html
<blockquote>
  <p>"引用文字内容。"</p>
  <p>—— 来源署名</p>
</blockquote>
```

> 用 `<blockquote>` 语义引用，不用 `<section style="border-left">`。头条不适合花哨引用块，保持克制。

### T12. 数据高亮

```html
<p><strong>87.3%</strong></p>
<p><em>用户在3秒内决定是否继续阅读</em></p>
```

> 大数字用 `<strong>` 加粗单独成段，说明文字用 `<em>` 斜体紧随其后。不用渐变背景卡片。

### T13. 表格

```html
<table>
  <tr>
    <th>维度</th>
    <th>传统方式</th>
    <th>推荐方式</th>
  </tr>
  <tr>
    <td>排版风格</td>
    <td>花哨密集</td>
    <td>克制留白</td>
  </tr>
  <tr>
    <td>段落长度</td>
    <td>超长不分段</td>
    <td>3-4行分段</td>
  </tr>
</table>
```

> 纯语义表格，不用 inline style 美化。ProseMirror 原生支持表格编辑。第一行用 `<th>` 做表头。

### T14. 代码块

```html
<pre>const example = "hello";
console.log(example);</pre>
```

> 头条 ProseMirror schema 保留 `<pre>` 标签（与微信不同）。直接用 `<pre>` 即可，不需要 `<br>` 换行。不支持语法高亮（inline style 会被剥离）。

### T15. 底部签名

```html
<hr>
<p>关注我，获取更多实用干货</p>
<p><em>每周更新，欢迎转发分享</em></p>
```

> 分割线 + 签名文字。不用版权标签胶囊（需要 inline style）。

### T16. 信息卡片（每行一卡，宽表替代）

```html
<blockquote>
  <p><strong>行标题/关键列</strong> 评价标签</p>
  <p>列名A：值A</p>
  <p>列名B：值B</p>
</blockquote>
```

> 头条卡片 = `<blockquote>`（编辑器渲染为带左侧竖条的分块）。每张 blockquote = 表格一行。纯语义，零 inline style。

### T17. 键值列表（2~3 列文字表替代）

```html
<blockquote>
  <p><strong>条目标题</strong></p>
  <p>说明文字内容</p>
  <p>方法：补充信息</p>
</blockquote>
```

> 纯语义等价实现。含数值/分值列时，进度条视觉在头条无法渲染，分值改为「数值 + 等级词」（如 `1.0 优秀` / `0.85 良好` / `0.0 失败`）。

---

## 头条页面外壳模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>文章标题</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif; background: #f0f0f3; padding: 40px 16px; }
  .page-wrap { max-width: 680px; margin: 0 auto; }
  .toolbar { background: #fff; border-radius: 12px; padding: 20px 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .toolbar h1 { font-size: 18px; color: #1a1a2e; margin-bottom: 6px; }
  .toolbar p { font-size: 13px; color: #888; line-height: 1.6; }
  .copy-btn { display: inline-block; margin-top: 12px; padding: 10px 24px; background: #F04142; color: #fff; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; }
  .copy-btn:hover { background: #d03536; }
  .view-tabs { display: flex; gap: 0; margin-bottom: 0; border-radius: 12px 12px 0 0; overflow: hidden; }
  .view-tab { flex: 1; padding: 10px 16px; text-align: center; font-size: 13px; font-weight: 600; cursor: pointer; background: #e8e8e8; color: #888; border: none; }
  .view-tab.active { background: #fff; color: #F04142; }
  .preview-label { font-size: 12px; color: #aaa; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; padding-left: 4px; }

  /* 美化预览样式（仅浏览器渲染，不会被复制） */
  .toutiao-content { background: #fff; border-radius: 0 0 12px 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); padding: 28px 20px; }
  .toutiao-content h1 { font-size: 22px; font-weight: 700; color: #222; line-height: 1.5; margin: 0 0 12px; }
  .toutiao-content h2 { font-size: 18px; font-weight: 700; color: #222; line-height: 1.6; margin: 24px 0 12px; }
  .toutiao-content h3 { font-size: 16px; font-weight: 600; color: #333; line-height: 1.6; margin: 16px 0 8px; }
  .toutiao-content p { font-size: 17px; color: #505050; line-height: 2; margin: 0 0 12px; letter-spacing: 1px; }
  .toutiao-content strong { font-weight: 700; color: #222; }
  .toutiao-content em { font-style: italic; color: #777; }
  .toutiao-content blockquote { border-left: 3px solid #ddd; padding: 8px 0 8px 16px; margin: 12px 0; }
  .toutiao-content blockquote p { font-size: 16px; color: #666; line-height: 1.9; margin: 0 0 4px; }
  .toutiao-content hr { border: none; height: 1px; background: #eee; margin: 16px 0; }
  .toutiao-content ul, .toutiao-content ol { padding-left: 24px; margin: 0 0 12px; }
  .toutiao-content li { font-size: 17px; color: #505050; line-height: 2; margin-bottom: 6px; letter-spacing: 1px; }
  .toutiao-content table { width: 100%; border-collapse: collapse; margin: 12px 0; }
  .toutiao-content th { background: #f7f7f7; font-size: 14px; font-weight: 700; color: #222; padding: 10px 12px; border: 1px solid #e8e8e8; text-align: center; }
  .toutiao-content td { font-size: 14px; color: #666; padding: 10px 12px; border: 1px solid #e8e8e8; text-align: center; }
  .toutiao-content pre { background: #f5f5f5; border-radius: 8px; padding: 14px 16px; font-family: 'SF Mono', Monaco, Menlo, Consolas, monospace; font-size: 14px; color: #333; line-height: 1.7; overflow-x: auto; margin: 12px 0; }

  /* 头条实际效果模拟 */
  .toutiao-raw { background: #fff; border-radius: 0 0 12px 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); padding: 28px 20px; }
  .toutiao-raw h1 { font-size: 20px; font-weight: bold; color: #222; margin: 0 0 10px; }
  .toutiao-raw h2 { font-size: 17px; font-weight: bold; color: #222; margin: 20px 0 10px; }
  .toutiao-raw p { font-size: 16px; color: #333; line-height: 1.8; margin: 0 0 10px; }
  .toutiao-raw strong { font-weight: bold; }
  .toutiao-raw em { font-style: italic; }
  .toutiao-raw blockquote { border-left: 3px solid #ccc; padding-left: 12px; margin: 10px 0; color: #666; }
  .toutiao-raw hr { border: none; border-top: 1px solid #eee; margin: 12px 0; }
  .toutiao-raw ul, .toutiao-raw ol { padding-left: 20px; margin: 0 0 10px; }
  .toutiao-raw li { font-size: 16px; color: #333; line-height: 1.8; margin-bottom: 4px; }
  .toutiao-raw table { width: 100%; border-collapse: collapse; margin: 10px 0; }
  .toutiao-raw th, .toutiao-raw td { border: 1px solid #ddd; padding: 6px 10px; font-size: 14px; }
  .toutiao-raw pre { background: #f5f5f5; padding: 10px; font-size: 13px; font-family: monospace; }
</style>
</head>
<body>
<div class="page-wrap">
  <div class="toolbar">
    <h1>文章标题</h1>
    <p>今日头条 · 纯语义HTML · ProseMirror兼容 · 复制预览区内容直接粘贴到头条编辑器</p>
    <button class="copy-btn" onclick="copyContent()">一键复制排版内容</button>
  </div>
  <div class="view-tabs">
    <button class="view-tab active" onclick="switchView('styled')">美化预览</button>
    <button class="view-tab" onclick="switchView('raw')">头条实际效果</button>
  </div>
  <div class="preview-label">— 预览区 —</div>

  <!-- 美化预览 -->
  <div class="toutiao-content" id="styled-view">
    <!-- ===== 所有头条组件放在这里（纯语义HTML） ===== -->
  </div>

  <!-- 头条实际效果模拟 -->
  <div class="toutiao-raw" id="raw-view" style="display:none">
    <p style="font-size:13px;color:#aaa;text-align:center;margin-bottom:16px">↓ 以下模拟头条编辑器实际渲染效果（仅语义标签，无自定义样式） ↓</p>
    <div id="raw-content"></div>
  </div>
</div>
<script>
function copyContent() {
  var content = document.getElementById('styled-view');
  var range = document.createRange();
  range.selectNodeContents(content);
  var selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
  try {
    document.execCommand('copy');
    var btn = document.querySelector('.copy-btn');
    var originalText = btn.textContent;
    btn.textContent = '✓ 已复制，可粘贴到头条编辑器';
    btn.style.background = '#00a663';
    setTimeout(function() {
      btn.textContent = originalText;
      btn.style.background = '#F04142';
    }, 3000);
  } catch (err) {
    alert('复制失败，请手动选中预览区内容复制');
  }
  selection.removeAllRanges();
}
function switchView(view) {
  var tabs = document.querySelectorAll('.view-tab');
  var styledView = document.getElementById('styled-view');
  var rawView = document.getElementById('raw-view');
  if (view === 'styled') {
    tabs[0].classList.add('active');
    tabs[1].classList.remove('active');
    styledView.style.display = '';
    rawView.style.display = 'none';
  } else {
    tabs[0].classList.remove('active');
    tabs[1].classList.add('active');
    styledView.style.display = 'none';
    rawView.style.display = '';
    if (!document.getElementById('raw-content').innerHTML) {
      var clone = styledView.cloneNode(true);
      var all = clone.querySelectorAll('*');
      for (var i = 0; i < all.length; i++) {
        all[i].removeAttribute('class');
        all[i].removeAttribute('style');
      }
      var walker = document.createTreeWalker(clone, NodeFilter.SHOW_COMMENT, null, null);
      var comments = [];
      while (walker.nextNode()) comments.push(walker.currentNode);
      comments.forEach(function(c) { c.parentNode.removeChild(c); });
      document.getElementById('raw-content').innerHTML = clone.innerHTML;
    }
  }
}
</script>
</body>
</html>
```

> 外壳 CSS 仅用于浏览器预览渲染，不会被复制到剪贴板。复制时只有语义 HTML 标签进入剪贴板。

---

## 头条编辑器兼容性备忘

| HTML/CSS 特性 | 兼容性 | 备注 |
|---------------|--------|------|
| `<h1>`~`<h6>` | ✅ 支持 | schema 白名单 |
| `<p>` | ✅ 支持 | schema 白名单 |
| `<strong>` / `<b>` | ✅ 支持 | 语义加粗 |
| `<em>` / `<i>` | ✅ 支持 | 语义斜体 |
| `<ul>` / `<ol>` / `<li>` | ✅ 支持 | 语义列表 |
| `<blockquote>` | ✅ 支持 | 语义引用 |
| `<hr>` | ✅ 支持 | 语义分割线 |
| `<pre>` | ✅ 支持 | 代码块（与微信不同） |
| `<table>` 系列 | ✅ 支持 | 语义表格 |
| `<a>` | ✅ 支持 | 链接 |
| `<img>` | ✅ 支持 | 图片 |
| inline style | ❌ 全部剥离 | ProseMirror 不保留 |
| `<section>` | ❌ 忽略 | 不在 schema 白名单 |
| `<div>` | ❌ 忽略 | 不在 schema 白名单 |
| `<span>` | ❌ 剥离属性 | 仅保留文本 |
| `class` 属性 | ❌ 剥离 | 不保留 |
| `style` 属性 | ❌ 剥离 | 不保留 |
| `background` | ❌ 剥离 | 用语义标签替代 |
| `border-left` | ❌ 剥离 | 用 `<blockquote>` 替代 |
| `display:flex` | ❌ 剥离 | 用 `<ul>`/`<table>` 替代 |
| `linear-gradient` | ❌ 剥离 | 不支持 |
| `border-radius` | ❌ 剥离 | 不支持 |

---

## 微信 vs 头条 对比速查

| 维度 | 微信公众号 | 今日头条 |
|------|-----------|----------|
| 编辑器类型 | 富文本（保留 inline style） | ProseMirror（schema 白名单） |
| 样式方案 | 全内联 CSS | 纯语义 HTML（零 inline style） |
| 容器标签 | `<section>` 嵌套 | `<p>`/`<h2>`/`<blockquote>` |
| 加粗 | `<span style="font-weight:700">` | `<strong>` |
| 引用块 | `<section style="border-left">` | `<blockquote>` |
| 分割线 | `<section style="height:1px;background">` | `<hr>` |
| 列表 | `<section style="display:flex">` | `<ul><li>` / `<ol><li>` |
| 代码块 | `<section>` + `<br>` + `&nbsp;` | `<pre>`（头条支持） |
| 宽表/长内容 | 信息卡片（22）/键值列表（23） | `<blockquote>`（T16/T17） |
| 层级建立 | CSS 装饰（竖条/方块/渐变） | 文字符号（◆★▶【】）+ 语义标签 |
| 正文字号 | 15px（可控） | 17px（编辑器默认，不可控） |
| 风格配色 | 23种风格令牌替换（7通用+8节日+4季节+4主题） | 固定（#F04142红，仅预览CSS） |
| 复制结果 | 格式完整保留 | 语义结构保留 |
| emoji | 自由使用 | 最多2种，不连续 |
| 算法敏感 | 否 | 是（过度排版降权） |
