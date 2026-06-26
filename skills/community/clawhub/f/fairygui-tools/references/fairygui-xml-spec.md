# FairyGUI XML 规范手册

> 本文档从 FairyGUI 官方文档（24 篇）和官方示例工程（176 个 XML 文件）中提炼，作为生成和校验 FairyGUI 工程文件的唯一权威参考。

---

## 1. 文件类型与根元素

FairyGUI 工程包含两类 XML 文件：

### 1.1 package.xml（包描述文件）

```xml
<?xml version="1.0" encoding="utf-8"?>
<packageDescription id="唯一ID" [jpegQuality="80"] [compressPNG="true"]>
  <resources>
    <!-- 资源声明 -->
  </resources>
  <publish name="包名">
    <atlas name="Default" index="0"/>
  </publish>
</packageDescription>
```

**packageDescription 属性：**
| 属性 | 必需 | 说明 |
|------|------|------|
| id | 是 | 包的唯一标识符，由编辑器生成的短字符串 |
| jpegQuality | 否 | JPEG 质量，默认 80 |
| compressPNG | 否 | 是否压缩 PNG，`"true"` 或 `"false"` |

### 1.2 组件 XML（Component）

```xml
<?xml version="1.0" encoding="utf-8"?>
<component size="宽,高" [其他属性...]>
  <controller .../>*
  <displayList>
    <!-- 显示元件 -->
  </displayList>
  <扩展元素/>?
  <transition .../>*
</component>
```

**component 根元素属性：**
| 属性 | 必需 | 格式 | 说明 |
|------|------|------|------|
| size | 是 | `"w,h"` | 组件尺寸 |
| extention | 否 | 枚举 | `Button`/`Label`/`ProgressBar`/`Slider`/`ScrollBar`/`ComboBox` |
| overflow | 否 | 枚举 | `visible`(默认)/`hidden`/`scroll` |
| scroll | 否 | 枚举 | `vertical`(默认)/`horizontal`/`both` |
| scrollBar | 否 | URL | 滚动条资源 URL |
| scrollBarFlags | 否 | 整数 | 滚动条标志位 |
| mask | 否 | 元件ID | 自定义遮罩 |
| reversedMask | 否 | `"true"` | 反向遮罩 |
| hitTest | 否 | `"id,宽,高"` | 点击测试 |
| opaque | 否 | `"true"`/`"false"` | 是否不透明 |
| bgColor | 否 | 颜色值 | 编辑器背景色（非运行时） |
| bgColorEnabled | 否 | `"true"` | 启用背景色 |
| initName | 否 | 字符串 | 初始名字 |
| pivot | 否 | `"x,y"` | 轴心，0~1 |
| designImageLayer | 否 | 整数 | 设计图层 |
| designImageAlpha | 否 | 浮点数 | 设计图透明度 |

---

## 2. package.xml 资源声明

`<resources>` 下允许的子元素及属性：

### 2.1 通用属性

所有资源元素共享：
| 属性 | 必需 | 说明 |
|------|------|------|
| id | 是 | 资源唯一 ID |
| name | 是 | 资源文件名 |
| path | 是 | 资源在包内的路径，如 `"/images/"`, `"/components/"`, `"/"` |
| exported | 否 | `"true"` 表示导出（可被其他包引用/可代码动态创建） |

### 2.2 资源类型及专属属性

**image（图片）**
| 属性 | 必需 | 值域 | 说明 |
|------|------|------|------|
| scale | 否 | `"9grid"`, `"tile"`, `""` | 缩放模式 |
| scale9grid | 当 scale="9grid" 时必需 | `"x,y,w,h"` | 九宫格区域 |
| duplicatePadding | 否 | `"true"` | 复制填充 |
| texture | 否 | 资源ID | 纹理引用（仅 font 使用） |

**component（组件）** — 仅 id, name, path, exported

**movieclip（动画）** — 仅 id, name, path, exported

**font（字体）**
| 属性 | 说明 |
|------|------|
| texture | 关联的纹理图片 ID |

**sound（声音）** — 仅 id, name, path, exported

**swf（SWF）** — 仅 id, name, path, exported

### 2.3 publish 元素

```xml
<publish name="包名" [packageCount="n"]>
  <atlas name="纹理集名" index="0"/>
</publish>
```

---

## 3. displayList 元素（显示列表）

`<displayList>` 是组件 XML 的核心，其合法子元素：

### 3.1 通用属性

所有 displayList 子元素共享：
| 属性 | 必需 | 格式 | 说明 |
|------|------|------|------|
| id | 是 | 字符串 | 元件唯一 ID |
| name | 是 | 字符串 | 元件名称 |
| xy | 否 | `"x,y"` | 位置坐标 |
| size | 否 | `"w,h"` | 尺寸 |
| pivot | 否 | `"x,y"` | 轴心点，0~1 |
| anchor | 否 | `"true"` | 轴心同时作为锚点 |
| scale | 否 | `"sx,sy"` | 缩放 |
| skew | 否 | `"sx,sy"` | 倾斜 |
| rotation | 否 | 数值 | 旋转角度 |
| alpha | 否 | 0~1 | 透明度 |
| visible | 否 | `"true"`/`"false"` | 可见性 |
| touchable | 否 | `"true"`/`"false"` | 可触摸 |
| grayed | 否 | `"true"` | 变灰 |
| group | 否 | 元件ID | 所属组 |
| tooltips | 否 | 字符串 | 提示文字 |

### 3.2 image（图片元件）

```xml
<image id="..." name="..." src="资源ID" [fileName="相对路径"]
       [xy="x,y"] [size="w,h"] [pivot="x,y"] [anchor="true"]
       [aspect="true"] [color="#RRGGBB"] [flip="hz|vt|both"]
       [fillMethod="radial360|..."] [fillClockwise="true|false"]
       [fillOrigin="0~3"] [fillAmount="0~100"]
       [alpha="0~1"] [group="组ID"] .../>
```

专属属性：
| 属性 | 说明 |
|------|------|
| src | 引用 package.xml 中资源的 ID |
| fileName | 资源文件相对路径 |
| aspect | `"true"` 保持宽高比 |
| color | 变色，`#RRGGBB` 或 `#AARRGGBB` |
| flip | 翻转：`"hz"`, `"vt"`, `"both"` |
| fillMethod | 填充方式：`"radial360"`, `"radial180"`, `"radial90"`, `"horizontal"`, `"vertical"` |
| fillClockwise | 顺时针 |
| fillOrigin | 填充起点 |
| fillAmount | 填充量 |

### 3.3 graph（图形元件）⭐

这是白模/灰盒模式的核心元件，用于替代 image 作为占位符。

```xml
<graph id="..." name="..."
       [xy="x,y"] [size="w,h"]
       [type="rect|eclipse|polygon|regular_polygon"]
       [lineSize="数值"] [lineColor="#AARRGGBB"]
       [fillColor="#AARRGGBB"]
       [corner="圆角"] [points="..."] [sides="边数"]
       [startAngle="角度"] [distances="..."]
       .../>
```

**type 类型详解：**
| type | 说明 | 专属属性 |
|------|------|----------|
| （不设置） | 空图形，用作占位符 | 无 |
| `rect` | 矩形 | `corner`（圆角半径，**仅支持单个整数**，如 `corner="20"`；不支持四角分别设置） |
| `eclipse` | 椭圆/圆形 | 无 |
| `polygon` | 多边形 | `points`（坐标对，格式 `"x1,y1,x2,y2,..."`，坐标为相对于元件左上角的浮点数） |
| `regular_polygon` | 正多边形 | `sides`（边数），`startAngle`（旋转角度），`distances`（各顶点距中心的距离比） |

> ⚠️ **polygon 重要说明**：多边形的顶点属性格式为逗号分隔的数字序列 `"x1,y1,x2,y2,..."`，坐标对数量必须为偶数。编辑器使用 `Single.Parse` 逐个解析数值。

**颜色格式：** `#AARRGGBB`（8位，Alpha 在前）或 `#RRGGBB`（6位）
- `fillColor` 中 Alpha=`00` 表示全透明（中空图形）
- `lineSize="0"` 表示不描边

**Graph 典型用法：**
- 背景色块：`type="rect" fillColor="#ff333333"`
- 占位矩形：`type="rect" lineSize="2"`（带描边轮廓）
- 触摸区域：不设 type（空图形）
- 遮罩：`type="rect"` 或 `type="eclipse"` 配合组件的 mask 属性
- 雷达图：`type="regular_polygon" sides="6" distances="0.57,0.82,..."`

### 3.4 text（文本元件）

```xml
<text id="..." name="..."
      [xy="x,y"] [size="w,h"]
      [fontSize="数值"] [font="字体名或URL"]
      [color="#RRGGBB"] [align="left|center|right"]
      [vAlign="top|middle|bottom"]
      [leading="行距"] [letterSpacing="字距"]
      [autoSize="none|both|height|shrink"]
      [singleLine="true"] [bold="true"] [italic="true"]
      [underline="true"] [strikethrough="true"]
      [strokeColor="#RRGGBB"] [strokeSize="数值"]
      [shadowColor="#RRGGBB"] [shadowOffset="x,y"]
      [ubbEnabled="true"]
      text="文本内容"/>
```

**换行：** 在 text 属性中使用 `&#xA;`

### 3.5 richtext（富文本元件）

属性与 text 基本相同，标签名为 `richtext`。

### 3.6 inputtext（输入文本）

属性与 text 基本相同，标签名为 `inputtext`，额外属性：
| 属性 | 说明 |
|------|------|
| password | `"true"` 密码模式 |
| maxLength | 最大长度 |
| restrict | 输入限制正则 |
| promptText | 提示文字 |
| keyboardType | 键盘类型 |

### 3.7 loader（装载器）

```xml
<loader id="..." name="..."
        [xy="x,y"] [size="w,h"]
        [url="资源URL"] [fill="none|scale|scaleMatchHeight|scaleMatchWidth|scaleFree|scaleNoBorder"]
        [align="left|center|right"] [vAlign="top|middle|bottom"]
        [shrinkOnly="true"] [autoSize="true"]
        [color="#RRGGBB"] [playing="true|false"] [frame="帧号"]
        .../>
```

### 3.8 component（组件引用）

```xml
<component id="..." name="..."
           src="package.xml中组件资源ID"
           [fileName="组件文件相对路径"]
           [xy="x,y"] [size="w,h"]
           ...>
  <扩展元素/>?
  <relation .../>*
  <gear元素/>*
</component>
```

**关键规则：** 引用的组件必须在同一 package.xml 的 `<resources>` 中有对应的 `<component>` 声明。

### 3.9 movieclip / jta（动画）

```xml
<movieclip id="..." name="..."
           src="资源ID" [fileName="路径"]
           [xy="x,y"] [playing="true|false"] [frame="帧号"]
           .../>
```

### 3.10 list（列表）

```xml
<list id="..." name="..."
      [xy="x,y"] [size="w,h"]
      [layout="column|row|flow_hz|flow_vt"]
      [overflow="visible|hidden|scroll"]
      [scroll="vertical|horizontal|both"]
      [scrollBar="URL"] [scrollBarFlags="整数"]
      [margin="top,bottom,left,right"]
      [clipSoftness="x,y"]
      [lineGap="行间距"] [colGap="列间距"]
      [defaultItem="ui://包ID+资源ID"]
      [selectionMode="single|multiple|none"]
      [autoResizeItem="true"]
      [foldInvisibleItems="true"]
      [lineCount="行数"] [columnCount="列数"]
      ...>
  <item [title="标题"] [icon="图标URL"] [url="组件URL"] [name="名称"]/>*
</list>
```

**defaultItem 格式（重要）：**
- 必须使用 `ui://` URL 格式，**绝不能使用文件路径**（如 `components/Foo.xml`）
- 包内引用：`"ui://包ID资源ID"`，例如 `"ui://a1b2c3d4gen_05"`
  - 注意：包ID 和资源ID **直接拼接**，中间无分隔符
- 可读格式：`"ui://包名/资源名"`，例如 `"ui://MyPackage/MyItem"`
- 省略时列表无默认项目类型

**layout 值域：**
- `column`（默认）：单列垂直
- `row`：单行水平
- `flow_hz`：水平流式
- `flow_vt`：垂直流式
- `pagination`：分页

### 3.11 group（组）

```xml
<group id="..." name="..."
       [xy="x,y"] [size="w,h"]
       [advanced="true"]
       .../>
```

`advanced="true"` 表示高级组（有独立的大小、可被 gear 控制）。

---

## 4. 控制器（Controller）

定义在 `<component>` 根下，`<displayList>` 之前。

```xml
<controller name="控制器名"
            pages="0,页面名0,1,页面名1,..."
            [selected="默认页索引"]
            [autoRadioGroupDepth="true"]
            [exported="true"]/>
```

**pages 格式：** `"索引,名称,索引,名称,..."`
- 索引从 0 开始递增
- 名称可为空字符串
- 示例：`pages="0,,1,"` 表示两个无名页面；`pages="0,up,1,down,2,over,3,selectedOver"` 表示按钮状态

---

## 5. Gear 子元素（属性控制）

Gear 元素作为 displayList 元件的子元素，实现控制器联动。

### 5.1 所有 Gear 类型

| Gear 元素 | 功能 | 适用元件 |
|-----------|------|----------|
| gearDisplay | 显示控制 | 所有 |
| gearDisplay2 | 显示控制-2 | 所有 |
| gearXY | 位置控制 | 所有 |
| gearSize | 大小控制 | 所有 |
| gearColor | 颜色控制 | image, text, richtext, loader |
| gearLook | 外观控制（透明度/变灰/旋转/不可触摸） | 所有 |
| gearAni | 动画控制 | movieclip, loader |
| gearText | 文本控制 | text, richtext, Label, Button, ComboBox |
| gearIcon | 图标控制 | loader, Label, Button |
| gearFontSize | 字体大小控制 | text, richtext, Label, Button |

### 5.2 通用属性

```xml
<gear元素 controller="控制器名"
         pages="参与页面索引列表（逗号分隔）"
         [values="对应值列表（|分隔各页）"]
         [default="默认值"]
         [tween="true"]
         [condition="0|1"]/>  <!-- 仅 gearDisplay2 -->
```

### 5.3 各 Gear 的 values 格式

| Gear | values 格式 | 示例 |
|------|------------|------|
| gearDisplay | 无 values，仅 pages | `pages="1"` |
| gearDisplay2 | 无 values，有 condition | `pages="1" condition="0"` |
| gearXY | `"x,y\|x,y"` 或 `"-"` 跳过 | `"181,271\|60,328"` |
| gearSize | `"w,h,sx,sy\|w,h,sx,sy"` | `"196,174,1,1"` |
| gearColor | `"#颜色,#颜色\|..."` | `"#000000,#000000"` |
| gearLook | `"alpha,rotation,grayed,touchable"` | `"0.54,180,0,0"` |
| gearAni | `"frame,playing"` (p/s) | `"0,s"` |
| gearText | `"text1\|text2\|text3"` | `"拉\|释放\|Loading"` |
| gearIcon | `"url1\|url2"` | URL 列表 |
| gearFontSize | `"size"` | `"74"` |

---

## 6. 关联（Relation）

定义元件之间的位置/大小关系。

```xml
<relation target="目标元件name或空" sidePair="关系对1,关系对2,..."/>
```

- `target=""` 表示目标为容器组件本身
- `target="n1"` 表示目标为名为 n1 的元件

**sidePair 合法值：**

| 关系对 | 说明 |
|--------|------|
| `left-left` | 左->左 |
| `left-center` | 左->中 |
| `left-right` | 左->右 |
| `center-center` | 左右居中 |
| `right-left` | 右->左 |
| `right-center` | 右->中 |
| `right-right` | 右->右 |
| `leftext-left` | 左延展->左 |
| `leftext-right` | 左延展->右 |
| `rightext-left` | 右延展->左 |
| `rightext-right` | 右延展->右 |
| `width-width` | 宽->宽 |
| `top-top` | 顶->顶 |
| `top-middle` | 顶->中 |
| `top-bottom` | 顶->底 |
| `middle-middle` | 上下居中 |
| `bottom-top` | 底->顶 |
| `bottom-middle` | 底->中 |
| `bottom-bottom` | 底->底 |
| `topext-top` | 顶延展->顶 |
| `topext-bottom` | 顶延展->底 |
| `bottomext-top` | 底延展->顶 |
| `bottomext-bottom` | 底延展->底 |
| `height-height` | 高->高 |

百分比模式在 sidePair 值后加 `%`，如 `left-center%`。

---

## 7. 扩展定义元素

当组件设置了 `extention` 属性或引用了扩展组件时，需要对应的扩展元素。

### 7.1 使用位置

- **组件定义中（根级）：** `<component extention="Button">` 内直接放 `<Button/>`
- **组件实例中（displayList 内）：** `<component src="..."><Button title="..."/></component>`

### 7.2 Button

```xml
<!-- 组件定义（根级） -->
<Button [mode="Common|Check|Radio"] [sound="URL"] [soundVolumeScale="0~1"]/>

<!-- 组件实例（displayList 内的 component 子元素） -->
<Button [title="标题"] [icon="图标URL"]
        [selectedTitle="选中标题"] [selectedIcon="选中图标URL"]
        [checked="true"]
        [controller="控制器名"] [page="页面索引"]/>
```

**Button 约定命名：**
- `title`：文本元件，显示标题
- `icon`：装载器元件，显示图标
- `button`：控制器，管理按钮状态（up/down/over/selectedOver）

### 7.3 Label

```xml
<Label [title="标题"] [icon="图标URL"] [titleColor="#RRGGBB"]
       [titleFontSize="数值"]/>
```

约定命名：`title`（文本），`icon`（装载器）

### 7.4 ProgressBar

```xml
<!-- 组件定义 -->
<ProgressBar [titleType="percent|value|valueAndMax|max"]
             [reverse="true"]/>

<!-- 组件实例 -->
<ProgressBar [value="数值"] [max="数值"]/>
```

约定命名：`bar`（进度条图片/装载器），`title`（文本显示进度值），`ani`（动画）

### 7.5 Slider

```xml
<!-- 组件定义 -->
<Slider [titleType="percent|value|valueAndMax|max"]
        [wholeNumbers="true"] [reverse="true"]/>

<!-- 组件实例 -->
<Slider [value="数值"] [max="数值"]/>
```

约定命名：`bar`（进度条），`title`（文本），`grip`（拖动按钮）

### 7.6 ScrollBar

```xml
<ScrollBar [fixedGripSize="true"]/>
```

约定命名：`grip`（滑块按钮），`bar`（轨道），`arrow1`/`arrow2`（箭头按钮）

### 7.7 ComboBox

```xml
<ComboBox [titleColor="#RRGGBB"] [visibleItemCount="数值"]
          [dropdown="资源URL"]>
  <item title="选项标题" [value="值"] [icon="图标URL"]/>*
</ComboBox>
```

约定命名：`title`（文本），`icon`（装载器），`list`（下拉列表）

---

## 8. 动效/过渡（Transition）

定义在 `<component>` 根下，`<displayList>` 之后。

```xml
<transition name="动效名"
            [autoPlay="true"]
            [autoPlayRepeat="-1|次数"]
            [autoPlayDelay="秒"]>
  <item .../>*
</transition>
```

### 8.1 item 属性

```xml
<item time="帧号"
      type="动效类型"
      [target="目标元件ID"]
      [tween="true"]
      [startValue="起始值"]
      [endValue="结束值"]
      [value="非tween值"]
      [duration="持续帧数"]
      [ease="缓动函数"]
      [repeat="重复次数"]
      [yoyo="true"]
      [label="标签"]
      [label2="标签2"]
      [path="路径数据"]/>
```

- 无 `target`：作用于组件自身
- `time` 单位为帧号（整数）

### 8.2 type 类型及值格式

| type | value 格式 | startValue/endValue 格式 | 说明 |
|------|-----------|-------------------------|------|
| XY | `"x,y"` | `"x,y"` (`"-"` 表示不改变该轴) | 改变位置 |
| Size | `"w,h"` | `"w,h"` | 改变大小 |
| Scale | `"sx,sy"` | `"sx,sy"` | 改变缩放 |
| Pivot | `"px,py"` | `"px,py"` | 改变轴心 |
| Alpha | `"0~1"` | `"0~1"` | 改变透明度 |
| Rotation | `"角度"` | `"角度"` | 改变旋转 |
| Color | `"#RRGGBB"` | `"#RRGGBB"` | 改变颜色 |
| ColorFilter | `"b,c,s,h"` | `"b,c,s,h"` | 颜色滤镜 |
| Visible | `"true"/"false"` | — | 改变可见性（无 tween） |
| Sound | `"url[,volume]"` | — | 播放声音（无 tween） |
| Transition | `"动效名"` | — | 播放嵌套动效（无 tween） |
| Shake | `"强度,持续秒"` | — | 震动（无 tween） |
| Animation | `"帧号,p/s"` | — | 动画控制 (p=playing, s=stopped) |
| Text | `"文本"` | — | 改变文本（无 tween） |
| Icon | `"URL"` | — | 改变图标（无 tween） |
| FontSize | `"大小"` | — | 改变字体大小（无 tween） |
| Skew | `"sx,sy"` | `"sx,sy"` | 改变倾斜 |

### 8.3 ease（缓动函数）合法值

`Linear`, `Quad.In`, `Quad.Out`, `Quad.InOut`,
`Cubic.In`, `Cubic.Out`, `Cubic.InOut`,
`Quart.In`, `Quart.Out`, `Quart.InOut`,
`Quint.In`, `Quint.Out`, `Quint.InOut`,
`Sine.In`, `Sine.Out`, `Sine.InOut`,
`Bounce.In`, `Bounce.Out`, `Bounce.InOut`,
`Circ.In`, `Circ.Out`, `Circ.InOut`,
`Expo.In`, `Expo.Out`, `Expo.InOut`,
`Elastic.In`, `Elastic.Out`, `Elastic.InOut`,
`Back.In`, `Back.Out`, `Back.InOut`,
`Custom`

---

## 9. 值格式参考

### 9.1 颜色

- 8位：`#AARRGGBB`（Alpha + RGB）
- 6位：`#RRGGBB`（无 Alpha，等效 Alpha=FF）
- 全部大写或小写均可

### 9.2 坐标/尺寸

- `"x,y"` — 如 `"100,200"`
- 负数允许 — 如 `"-20,50"`
- 小数允许 — 如 `"0.5,0.5"`

### 9.3 资源 URL

- 包内：`"资源ID"`（如 `"rpmb1"`）— 用于 src 属性
- 跨包：`"ui://包ID+资源ID"`（如 `"ui://9leh0eyfrpmb6"`）— 用于 url/icon/font 属性
- 可读格式：`"ui://包名/资源名"` — 两种格式通用

### 9.4 ID 规则

- 由编辑器生成，通常是字母数字短字符串
- 白模生成时可自定义，建议格式：`"gen_" + 自增数字`（如 `gen_01`, `gen_02`）
- 包 ID 建议：8 字符随机字母数字（如 `"ab12cd34"`）

---

## 10. 结构约束总结

### 10.1 XML 节点顺序（component 内）

```
<component>
  <controller/>*          ← 0或多个，必须在 displayList 之前
  <displayList>           ← 必须且仅一个
    <元件/>*
  </displayList>
  <扩展定义元素/>?        ← 0或1个（Button/Label/ProgressBar/...）
  <transition/>*          ← 0或多个，必须在 displayList 之后
</component>
```

### 10.2 displayList 合法子元素

`image`, `graph`, `text`, `richtext`, `inputtext`, `loader`, `loader3d`, `component`, `movieclip`/`jta`, `list`, `group`

### 10.3 displayList 元件的合法子元素

- gear 元素：`gearDisplay`, `gearDisplay2`, `gearXY`, `gearSize`, `gearColor`, `gearLook`, `gearAni`, `gearText`, `gearIcon`, `gearFontSize`
- `<relation/>`
- 扩展实例元素：`<Button/>`, `<Label/>`, `<ProgressBar/>`, `<Slider/>`, `<ScrollBar/>`, `<ComboBox/>`

### 10.4 组件闭环原则

当生成包含子组件引用的 XML 时（如 list 的 defaultItem 或 component 的 src），**必须**：
1. 在 package.xml 中声明被引用的组件资源
2. 提供被引用组件的完整 XML 文件
3. component 实例的 `fileName` 属性必须匹配 package.xml 中的 `path + name`

### 10.5 绝对禁止

- ❌ XML 中使用 HTML 注释 `<!-- -->`（FairyGUI 编辑器不支持）
- ❌ 使用未在本规范中列出的标签或属性
- ❌ 组件引用缺少 src 属性
- ❌ displayList 之前出现 transition
- ❌ displayList 之后出现 controller
- ❌ 引用不存在的资源 ID
- ❌ list 的 defaultItem 使用文件路径（如 `components/Foo.xml`），必须用 `ui://` URL 格式

---

## 11. 白模生成规范

使用 graph 替代 image 构建 UI 原型时的约定：

### 11.1 颜色约定

| UI 元素 | 推荐 graph 设置 |
|---------|----------------|
| 背景 | `type="rect" fillColor="#ff333333"` |
| 按钮 | `type="rect" fillColor="#ff4a90d9" corner="8"` |
| 输入框 | `type="rect" lineSize="1" lineColor="#ff999999" fillColor="#ff222222"` |
| 头像/图标 | `type="eclipse" fillColor="#ff666666"` 或 `type="rect" fillColor="#ff666666"` |
| 进度条背景 | `type="rect" fillColor="#ff444444" corner="4"` |
| 进度条填充 | `type="rect" fillColor="#ff4a90d9" corner="4"` |
| 分隔线 | `type="rect" fillColor="#ff555555"` |
| 遮罩/触摸区域 | 不设 type（空图形） |

### 11.2 命名规范

遵循 FairyGUI 扩展机制的"名称约定"：
- 按钮标题 → `title`
- 按钮图标 → `icon`
- 按钮控制器 → `button`
- 进度条填充 → `bar`
- 滑块拖动按钮 → `grip`
- 窗口框架 → `frame`
