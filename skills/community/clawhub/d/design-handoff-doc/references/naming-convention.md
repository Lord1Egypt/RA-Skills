# 资源命名规范（各平台）

## 通用格式

```text
模块_组件_状态_尺寸_平台
示例：home_button_primary_normal_88x88_ios.png
```

## 各平台对比

### 小程序

```text
模块_组件_状态_尺寸
示例：home_icon_tab_normal_48.png
```

- 使用下划线 `_` 分隔
- 小写字母
- 尺寸用实际输出尺寸（@2x）

### iOS

```text
模块_组件_状态_尺寸_平台
示例：home_button_primary_highlighted_44x44_ios.png
```

- @1x / @2x / @3x 三套
- 命名结尾加 `_ios`
- 文件名不含中文

### Android

```text
模块_组件_状态_尺寸_平台
示例：ic_home_tab_selected_24dp_android.png
```

- `ic_` 前缀（图标）
- mdpi / hdpi / xhdpi / xxhdpi / xxxhdpi 五套
- 命名结尾加 `_android`

### Web

```text
模块-组件-状态-尺寸
示例：home-button-primary-hover-40.svg
```

- 使用连字符 `-` 分隔（kebab-case）
- SVG 优先，PNG @2x 备选

### 大屏

```text
模块_组件_状态
示例：map_panel_normal.png
```

- 按实际分辨率输出
- 背景图按基准分辨率 ×2 导出

## 状态后缀

| 状态 | 后缀 |
|------|------|
| 正常 | normal |
| 选中 | selected / active |
| 按压 | pressed / highlighted |
| 禁用 | disabled |
| 悬停 | hover |
| 加载 | loading |
| 错误 | error |
| 空 | empty |

## 命名建议

1. **语义清晰**：用业务名词而非通用名（`cart_icon` 而非 `icon_1`）
2. **不要用中文**：文件名统一英文
3. **统一分隔符**：同一项目只用一种分隔方式
4. **保持一致**：后端、前端、设计三方用同一套命名