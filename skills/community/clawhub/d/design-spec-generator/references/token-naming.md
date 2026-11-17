# Design Token 命名规范参考

用于在设计规范文档中保持命名一致性。

## 分类前缀

```text
color-    → 色彩
font-     → 字体
spacing-  → 间距
radius-   → 圆角
shadow-   → 阴影
icon-     → 图标
size-     → 尺寸
z-        → 层级
```

## 色彩令牌

```text
color-primary-{shade}    品牌主色    (050/100/200/300/400/500/600/700/800/900)
color-secondary-{shade}  辅助色
color-neutral-{shade}    中性色
color-semantic-{type}    语义色 (success/warning/error/info)
```

S h a d e 递减规则：500 为基准色，每档 ±10% 色阶。

## 字体令牌

```text
font-size-{level}   字号层级 (display/title/headline/body/caption/tiny)
font-weight-{name}  字重 (regular/medium/semibold/bold)
font-family-{name}  字体家族
line-height-{name}  行高
```

## 间距令牌

```text
spacing-{n}    间距值，n 为具体数字 (1/2/3/4/5/6/8)
```

基准单位：4px（移动端）/ 8px（桌面端）。spacing-4 = 4 × 基准单位。

## 圆角令牌

```text
radius-{size}   sm / md / lg / xl / full
```

## 阴影令牌

```text
shadow-{level}   1 / 2 / 3
```

## 尺寸令牌

```text
size-{component}-{property}
示例：size-button-height, size-icon-default
```

## 善用 Token 的好处

1. **一致性**：所有端共享同一套值，不会再出现色值偏差
2. **可维护性**：改一个变量，全局生效
3. **跨端同步**：Design Tokens JSON 可直接给前端使用
4. **沟通效率**：设计 ↔ 开发用同一套语言

## 推荐工具

| 工具 | 用途 |
|------|------|
| Figma Variables | Figma 内置设计令牌 |
| Token Studio (Figma) | 管理 + 导出 Design Tokens |
| Style Dictionary | Amazon 开源，生成各端代码 |
| 蓝湖 | 设计交付 + 标注 |