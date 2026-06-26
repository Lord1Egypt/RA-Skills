# 设计系统：Webflow

## 1. 视觉主题与氛围

Webflow 的网站是一个视觉丰富、工具导向的平台，通过干净的白色表面、标志性的 Webflow Blue (`#146ef5`) 和丰富的辅助色彩（purple、pink、green、orange、yellow、red）传达"无需代码即可设计"的理念。定制的 WF Visual Sans Variable 字体创建了一个自信、精确的排版系统，展示字重为 600，正文字重为 500。

**主要特征：**
- 白色画布配近乎黑色 (`#080808`) 的文字
- Webflow Blue (`#146ef5`) 作为主要品牌色和交互色
- WF Visual Sans Variable — 自定义可变字体，字重 500–600
- 丰富的辅助色板：purple `#7a3dff`、pink `#ed52cb`、green `#00d722`、orange `#ff6b00`、yellow `#ffae13`、red `#ee1d36`
- 保守的 4px–8px border-radius — 锐利，非圆角
- 多层阴影堆叠（5 层级联阴影）
- 大写标签：10px–15px，字重 500–600，宽字间距（0.6px–1.5px）
- 按钮 hover 动画：translate(6px)

## 2. 色彩搭配与角色

### 主色
- **Near Black** (`#080808`)：主要文字
- **Webflow Blue** (`#146ef5`)：`--_color---primary--webflow-blue`，主要 CTA 和链接
- **Blue 400** (`#3b89ff`)：`--_color---primary--blue-400`，较浅的交互蓝色
- **Blue 300** (`#006acc`)：`--_color---blue-300`，较深的蓝色变体
- **Button Hover Blue** (`#0055d4`)：`--mkto-embed-color-button-hover`

### 辅助强调色
- **Purple** (`#7a3dff`)：`--_color---secondary--purple`
- **Pink** (`#ed52cb`)：`--_color---secondary--pink`
- **Green** (`#00d722`)：`--_color---secondary--green`
- **Orange** (`#ff6b00`)：`--_color---secondary--orange`
- **Yellow** (`#ffae13`)：`--_color---secondary--yellow`
- **Red** (`#ee1d36`)：`--_color---secondary--red`

### 中性色
- **Gray 800** (`#222222`)：深色次要文字
- **Gray 700** (`#363636`)：中等文字
- **Gray 300** (`#ababab`)：弱化文字、占位符
- **Mid Gray** (`#5a5a5a`)：链接文字
- **Border Gray** (`#d8d8d8`)：边框、分隔线
- **Border Hover** (`#898989`)：悬停边框

### 阴影
- **5 层级联**：`rgba(0,0,0,0) 0px 84px 24px, rgba(0,0,0,0.01) 0px 54px 22px, rgba(0,0,0,0.04) 0px 30px 18px, rgba(0,0,0,0.08) 0px 13px 13px, rgba(0,0,0,0.09) 0px 3px 7px`

## 3. 排版规则

### 字体：`WF Visual Sans Variable`，后备字体：`Arial`

| 角色 | 尺寸 | 字重 | 行高 | 字间距 | 备注 |
|------|------|--------|-------------|----------------|-------|
| Display Hero | 80px | 600 | 1.04 | -0.8px | |
| Section Heading | 56px | 600 | 1.04 | normal | |
| Sub-heading | 32px | 500 | 1.30 | normal | |
| Feature Title | 24px | 500–600 | 1.30 | normal | |
| Body | 20px | 400–500 | 1.40–1.50 | normal | |
| Body Standard | 16px | 400–500 | 1.60 | -0.16px | |
| Button | 16px | 500 | 1.60 | -0.16px | |
| Uppercase Label | 15px | 500 | 1.30 | 1.5px | 大写 |
| Caption | 14px | 400–500 | 1.40–1.60 | normal | |
| Badge Uppercase | 12.8px | 550 | 1.20 | normal | 大写 |
| Micro Uppercase | 10px | 500–600 | 1.30 | 1px | 大写 |
| Code: Inconsolata（配套等宽字体）

## 4. 组件样式

### 按钮
- 透明：文字 `#080808`，hover 时 translate(6px)
- 白色圆形：50% 圆角，白色背景
- 蓝色徽章：`#146ef5` 背景，4px 圆角，字重 550

### 卡片：`1px solid #d8d8d8`，4px–8px 圆角
### 徽章：蓝色调背景，10% 不透明度，4px 圆角

## 5. 布局
- 间距：分数比例（1px, 2.4px, 3.2px, 4px, 5.6px, 6px, 7.2px, 8px, 9.6px, 12px, 16px, 24px）
- 圆角：2px, 4px, 8px, 50% — 保守、锐利
- 断点：479px, 768px, 992px

## 6. 层次感：5 层级联阴影系统

## 7. 最佳实践
- 推荐：使用 WF Visual Sans Variable 字重 500–600。CTA 使用 Blue (#146ef5)。4px 圆角。translate(6px) hover 效果。
- 避免：功能元素圆角超过 8px。在主要 CTA 上使用辅助色。

## 8. 响应式：479px, 768px, 992px

## 9. Agent 提示指南
- 文字：Near Black (`#080808`)
- CTA：Webflow Blue (`#146ef5`)
- 背景：White (`#ffffff`)
- 边框：`#d8d8d8`
- 辅助色：Purple `#7a3dff`、Pink `#ed52cb`、Green `#00d722`
