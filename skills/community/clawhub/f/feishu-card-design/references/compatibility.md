# 飞书卡片客户端兼容性

> **版本**：1.0.4 | **本文件作用**：定义不同客户端版本的兼容性差异 + 双重保险策略
> **测试覆盖**：飞书 PC 端 / Mac 端 / iOS / Android / 网页版

---

## 1. 客户端版本差异

### 1.1 关键版本里程碑

| 版本 | 发布时间 | 关键变化 |
|------|---------|---------|
| V7.4+ | 2024 Q4 | `column.background_style` 支持 |
| V7.9+ | 2025 Q2 | `column_set.background_style` 支持 |
| V8.0+ | 2025 Q3 | Card 2.0 Schema 正式稳定 |

### 1.2 兼容性矩阵

| 特性 | V7.4- | V7.4-V7.9 | V7.9-V8.0 | V8.0+ |
|------|-------|-----------|-----------|-------|
| Card 1.0 (`elements` 顶层) | ✅ | ✅ | ⚠️ 兼容 | ❌ 弃用 |
| Card 2.0 (`schema: "2.0"`) | ❌ | ⚠️ 部分 | ✅ | ✅ |
| `column.background_style` | ❌ | ✅ | ✅ | ✅ |
| `column_set.background_style` | ❌ | ❌ | ✅ | ✅ |
| `markdown` 元素 | ❌ | ✅ | ✅ | ✅ |
| `lark_md` 元素 | ✅ | ✅ | ⚠️ 兼容 | ⚠️ 兼容 |
| `button.behaviors` | ❌ | ✅ | ✅ | ✅ |
| `button.url`（旧） | ✅ | ⚠️ 兼容 | ⚠️ 兼容 | ❌ 弃用 |

---

## 2. 双重保险策略

### 2.1 配色双重保险

**问题**：`column_set.background_style` 在 V7.4-V7.9 客户端不渲染，导致配色丢失。

**解决方案**：同时设置 `column.background_style` 和 `column_set.background_style`。

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "blue-50",        // V7.9+ 生效
  "columns": [{
    "tag": "column",
    "width": "weighted",
    "weight": 1,
    "vertical_align": "top",
    "background_style": "blue-50",      // V7.4+ 全客户端生效
    "elements": [{"tag": "markdown", "content": "..."}]
  }]
}
```

**效果**：
- V8.0+ 客户端：column_set 和 column 都渲染（双重显示，无视觉差异）
- V7.9-V8.0 客户端：column_set 和 column 都渲染
- V7.4-V7.9 客户端：只有 column 渲染（不影响视觉）
- V7.4- 客户端：都不渲染（fallback 到无背景色，但仍可读）

### 2.2 Markdown 元素保险

**问题**：`lark_md` 不支持 `#`/`##`/`>` 等 Markdown 语法。

**解决方案**：所有正文用 `markdown` 元素，不用 `lark_md`。

```json
// ✅ 推荐
{"tag": "markdown", "content": "### 标题\n\n> 引用\n\n**加粗**"}

// ❌ 禁止（不支持 # ## >）
{"tag": "lark_md", "content": "### 标题\n\n> 引用\n\n**加粗**"}
```

**例外**：`note` 元素内仍可用 `lark_md`（note 不需要复杂格式）。

### 2.3 Button behaviors 保险

**问题**：`button.url` 在 V8.0+ 弃用。

**解决方案**：所有按钮用 `behaviors`，不用 `url`。

```json
// ✅ 推荐（Card 2.0）
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "📄 查看文档"},
  "type": "primary",
  "width": "fill",
  "behaviors": [{"type": "open_url", "default_url": "https://..."}]
}

// ❌ 禁止（已弃用）
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "📄 查看文档"},
  "type": "primary",
  "url": "https://..."
}
```

### 2.4 action 包装保险

**问题**：Card 1.0 用 `action` 包装 button，Card 2.0 直接用 button。

**解决方案**：所有 button 直接放 `body.elements`，不用 `action` 包装。

```json
// ✅ 推荐（Card 2.0）
{
  "body": {
    "elements": [
      {...},
      {"tag": "button", "text": {...}, "behaviors": [...]}
    ]
  }
}

// ❌ 禁止（Card 1.0 风格）
{
  "body": {
    "elements": [
      {...},
      {"tag": "action", "actions": [{"tag": "button", ...}]}
    ]
  }
}
```

---

## 3. 多端适配建议

### 3.1 PC 端（Windows/Mac）

- 宽屏模式默认开启
- 多列布局正常显示
- 按钮宽度 `fill` 占满整行
- 长内容自动换行

### 3.2 移动端（iOS/Android）

- 自适应单列显示
- 多列布局自动堆叠
- 按钮宽度 `fill` 占满整行
- **注意**：长标题会截断，控制在 30 字符内

### 3.3 网页版（feishu.cn）

- 与 PC 端表现一致
- 支持鼠标悬停效果
- 支持右键复制

### 3.4 iPad

- 介于 PC 和移动端之间
- 横屏时按 PC 端显示
- 竖屏时按移动端显示

---

## 4. 测试矩阵

### 4.1 必测客户端

| 平台 | 版本 | 测试要点 |
|------|------|---------|
| Windows PC | 最新版 | 配色渲染、按钮点击 |
| Mac | 最新版 | 同上 |
| iOS | 最新版 | 单列布局、按钮宽度 |
| Android | 最新版 | 同上 |
| 网页版 | Chrome 最新 | 同 PC |

### 4.2 测试用例

#### 用例 1：配色渲染

发送一张含 4 种背景色（blue-50/yellow-50/grey-50/green-50）的卡片，验证：
- [ ] 4 种背景色都正确渲染
- [ ] column + column_set 双重设置无视觉异常
- [ ] 移动端单列堆叠正常

#### 用例 2：Markdown 渲染

发送一张含 `#`/`##`/`###`/`>`/`**`/列表/代码块的卡片，验证：
- [ ] 所有 Markdown 语法都正确渲染
- [ ] 代码块有等宽字体
- [ ] 引用块有左竖线

#### 用例 3：按钮点击

发送一张含 2 个按钮（primary + default）的卡片，验证：
- [ ] 按钮颜色正确（primary=蓝，default=灰）
- [ ] 按钮宽度 `fill` 占满整行
- [ ] 点击按钮跳转 URL 正常

#### 用例 4：长标题

发送一张标题 60 字符的卡片，验证：
- [ ] PC 端完整显示
- [ ] 移动端截断合理（不出现"..."在中间）
- [ ] subtitle 正常显示

---

## 5. 兼容性降级策略

### 5.1 V7.4- 客户端（极少数）

**现象**：Card 2.0 不识别，卡片显示为纯文本。

**降级方案**：发送 fallback 文本消息 + 链接。

```python
def send_card_with_fallback(user_open_id: str, card: dict, fallback_text: str):
    try:
        # 尝试发送卡片
        send_card_message(user_open_id, card)
    except CardNotSupportedError:
        # 降级为文本消息
        send_text_message(user_open_id, fallback_text)
```

### 5.2 配色不渲染

**现象**：客户端版本太旧，background_style 不渲染。

**降级方案**：在 markdown 内容中用 emoji 补充视觉提示。

```json
{
  "tag": "markdown",
  "content": "🟦 **主推块**\n\n核心信息..."
}
```

### 5.3 Button 不支持

**现象**：button.behaviors 不识别。

**降级方案**：在 markdown 中放链接。

```json
{
  "tag": "markdown",
  "content": "📄 [查看完整云文档](https://...)"
}
```

---

## 6. 客户端版本检测

### 6.1 通过 User-Agent 检测

飞书 OpenAPI 不直接返回客户端版本，但可通过消息回调中的 `user_agent` 字段推断：

```python
def get_client_version(user_agent: str) -> str:
    if "Feishu/7.4" in user_agent:
        return "V7.4"
    elif "Feishu/7.9" in user_agent:
        return "V7.9"
    elif "Feishu/8." in user_agent:
        return "V8.0+"
    return "unknown"
```

### 6.2 实际建议

- **不强制版本检测**：双重保险策略已覆盖所有版本
- **统计客户端分布**：通过消息已读回执统计
- **引导升级**：在 footer note 提示"建议升级到 V8.0+ 获得最佳体验"

---

## 7. 兼容性自检清单

- [ ] 所有 column_set 同时设置 column.background_style（V7.4+ 兼容）
- [ ] 所有正文用 markdown 元素（不用 lark_md）
- [ ] 所有按钮用 behaviors（不用 url）
- [ ] 所有 button 直接放 body.elements（不用 action 包装）
- [ ] schema 字段为字符串 "2.0"（不是数字 2）
- [ ] template 字段用枚举值（不用色值）
- [ ] background_style 用枚举值（不用色值）
- [ ] 测试 PC + 移动端 + 网页版 3 端渲染
