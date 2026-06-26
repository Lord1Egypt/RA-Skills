# 无障碍标签审查 — 代码示例

基于 React + TDesign + @tencent/yb-component 的真实修复前后对比。

---

## 1. 纯图标按钮（icon-button-a11y）

### 修复前

```tsx
<div className={styles.operationItem} onClick={handleRestartBot}>
  <span className={styles.operationItemLabel}>{t('重启网关服务')}</span>
  <YbIcon className={styles.operationItemArrow} type="ic_arrow_large_16" />
</div>
```

上面这个**部分合规** — 有可见文本。但独立的图标按钮：

```tsx
<div className={styles.closeBtn} onClick={onClose}>
  <YbIcon type="ic_close_16" />
</div>
```

### 修复后

```tsx
<div
  className={styles.closeBtn}
  onClick={onClose}
  role="button"
  tabIndex={0}
  aria-label={t('关闭')}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClose();
    }
  }}
>
  <YbIcon type="ic_close_16" aria-hidden="true" />
</div>
```

---

## 2. div 模拟按钮（div-button-a11y）

### 修复前

```tsx
<div className={styles.clearHistoryButton} onClick={handleClearHistory}>
  <span>{t('清除该记录')}</span>
</div>
```

### 修复后

```tsx
<div
  className={styles.clearHistoryButton}
  onClick={handleClearHistory}
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClearHistory();
    }
  }}
>
  <span>{t('清除该记录')}</span>
</div>
```

**更好的做法** — 直接替换为原生 `<button>`：

```tsx
<button
  className={styles.clearHistoryButton}
  onClick={handleClearHistory}
  type="button"
>
  <span>{t('清除该记录')}</span>
</button>
```

---

## 3. 图片 alt 文本（img-alt-a11y）

### 修复前 — 缺失 alt

```tsx
<img src={avatarUrl} className={styles.avatar} />
```

### 修复后 — 有意义的 alt

```tsx
<img src={avatarUrl} className={styles.avatar} alt={t('用户头像')} />
```

### 修复前 — 装饰性图片未正确标注

```tsx
<img src={bgPattern.src} className={styles.bg} />
```

### 修复后 — 装饰性图片正确标记

```tsx
<img src={bgPattern.src} className={styles.bg} alt="" role="presentation" />
```

### 修复前 — 无意义的 alt 文本

```tsx
<img src={loadingIcon.src} alt="image" className={styles.spinner} />
```

### 修复后 — 描述性 alt

```tsx
<img src={loadingIcon.src} alt={t('加载中')} className={styles.spinner} />
```

---

## 4. 表单标签（form-label-a11y）

### 修复前 — 输入框缺少标签

```tsx
<div className={styles.searchBox}>
  <YbIcon type="ic_search_16" />
  <input
    className={styles.searchInput}
    placeholder={t('搜索')}
    value={keyword}
    onChange={handleChange}
  />
</div>
```

### 修复后 — 添加 aria-label

```tsx
<div className={styles.searchBox}>
  <YbIcon type="ic_search_16" aria-hidden="true" />
  <input
    className={styles.searchInput}
    placeholder={t('搜索')}
    aria-label={t('搜索')}
    value={keyword}
    onChange={handleChange}
  />
</div>
```

### 修复前 — 下拉框缺少标签

```tsx
<select value={modelType} onChange={handleModelChange}>
  <option value="custom">{t('自定义大模型')}</option>
  <option value="preset">{t('预设模型')}</option>
</select>
```

### 修复后 — 使用包裹式 label

```tsx
<label>
  <span className="sr-only">{t('模型类型')}</span>
  <select value={modelType} onChange={handleModelChange}>
    <option value="custom">{t('自定义大模型')}</option>
    <option value="preset">{t('预设模型')}</option>
  </select>
</label>
```

---

## 5. 弹窗/对话框（dialog-a11y）

### 修复前 — 弹窗缺少 aria-labelledby

```tsx
<YbcDialog visible={visible} onClose={onClose}>
  <div className={styles.title}>{t('确认删除')}</div>
  <div className={styles.content}>{t('删除后无法恢复')}</div>
  <div className={styles.footer}>
    <YBButton onClick={onClose}>{t('取消')}</YBButton>
    <YBButton onClick={onConfirm}>{t('确认')}</YBButton>
  </div>
</YbcDialog>
```

### 修复后 — 正确关联标题

```tsx
<YbcDialog
  visible={visible}
  onClose={onClose}
  aria-labelledby="delete-dialog-title"
  aria-describedby="delete-dialog-desc"
>
  <div className={styles.title} id="delete-dialog-title">{t('确认删除')}</div>
  <div className={styles.content} id="delete-dialog-desc">{t('删除后无法恢复')}</div>
  <div className={styles.footer}>
    <YBButton onClick={onClose}>{t('取消')}</YBButton>
    <YBButton onClick={onConfirm}>{t('确认')}</YBButton>
  </div>
</YbcDialog>
```

---

## 6. 实时区域（live-region-a11y）

### 修复前 — Toast 缺少 live region

```tsx
const ToastMessage = ({ message }: { message: string }) => (
  <div className={styles.toast}>
    <span>{message}</span>
  </div>
);
```

### 修复后 — 屏幕阅读器可播报

```tsx
const ToastMessage = ({ message }: { message: string }) => (
  <div className={styles.toast} role="status" aria-live="polite" aria-atomic="true">
    <span>{message}</span>
  </div>
);
```

### 修复前 — 错误消息未即时播报

```tsx
{errorMsg && (
  <div className={styles.error}>{errorMsg}</div>
)}
```

### 修复后 — 错误立即播报

```tsx
<div className={styles.error} role="alert" aria-live="assertive" aria-atomic="true">
  {errorMsg}
</div>
```

注意：live region 容器必须在内容出现之前就存在于 DOM 中。条件渲染整个容器不会触发播报。

---

## 7. 跨平台兼容性（compat-a11y）

### 7a. `inert` 属性回退

#### 修复前 — 仅用 inert，X5/小程序不支持

```tsx
<div inert={modalOpen || undefined}>
  <MainContent />
</div>
```

#### 修复后 — 兼容回退

```tsx
const supportsInert = typeof HTMLElement !== 'undefined' && 'inert' in HTMLElement.prototype;

{supportsInert ? (
  <div inert={modalOpen || undefined}>
    <MainContent />
  </div>
) : (
  <div
    aria-hidden={modalOpen ? 'true' : undefined}
    style={modalOpen ? { pointerEvents: 'none' } : undefined}
  >
    <MainContent />
  </div>
)}
```

### 7b. 语义化元素替代 role（适用于微信/QQ 内置浏览器）

#### 修复前 — div + role，X5 内核可能忽略 role

```tsx
<div
  className={styles.navItem}
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={handleKeyDown}
>
  {t('设置')}
</div>
```

#### 修复后 — 使用原生 button，所有引擎都能正确识别

```tsx
<button
  className={styles.navItem}
  onClick={handleClick}
  type="button"
>
  {t('设置')}
</button>
```

### 7c. `:focus-visible` 兼容样式

#### 修复前 — 仅用 :focus-visible，X5 无效

```scss
.actionBtn {
  &:focus-visible {
    outline: 2px solid var(--brand-color);
  }
}
```

#### 修复后 — 渐进增强，所有浏览器可用

```scss
.actionBtn {
  &:focus {
    outline: 2px solid var(--brand-color);
    outline-offset: 2px;
  }
  &:focus:not(:focus-visible) {
    outline: none;
  }
  &:focus-visible {
    outline: 2px solid var(--brand-color);
    outline-offset: 2px;
  }
}
```

### 7d. 动态通知多通道回退

#### 修复前 — 仅依赖 aria-live，微信/QQ 中不播报

```tsx
<div role="status" aria-live="polite" aria-atomic="true">
  {successMsg}
</div>
```

#### 修复后 — 多通道反馈：ARIA + 视觉动画 + 条件震动

```tsx
import { isMpWebview } from '@tencent/yb-util/src/utils/detect-env';

const NotificationBanner = ({ message }: { message: string }) => {
  useEffect(() => {
    if (message && isMpWebview() && navigator.vibrate) {
      navigator.vibrate(200);
    }
  }, [message]);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className={cn(styles.notification, message && styles.notificationVisible)}
    >
      {message}
    </div>
  );
};
```

### 7e. suppressHydrationWarning 与 alt 共存

#### 修复前 — 有 suppressHydrationWarning 但缺少 alt

```tsx
<img
  src={loadingIcon.src}
  className={styles.spinner}
  suppressHydrationWarning
/>
```

#### 修复后 — 同时保证 alt 和水合兼容

```tsx
<img
  src={loadingIcon.src}
  alt={t('加载中')}
  className={styles.spinner}
  suppressHydrationWarning
/>
```

### 7f. 焦点管理的平台适配

#### 修复前 — 直接操作 DOM focus，小程序中可能失效

```tsx
const dialogRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  if (visible) {
    dialogRef.current?.focus();
  }
}, [visible]);
```

#### 修复后 — 平台感知的焦点管理

```tsx
import { isMpWebview } from '@tencent/yb-util/src/utils/detect-env';

const dialogRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  if (visible) {
    if (isMpWebview()) {
      // 小程序 WebView 中 focus() 不可靠，依赖库组件的焦点管理
      return;
    }
    requestAnimationFrame(() => {
      dialogRef.current?.focus();
    });
  }
}, [visible]);
```

---

## 审查报告示例

完整审查的输出格式如下：

```
## 无障碍审查报告 — src/components/im-group/setting/bot-setting/index.tsx

| 行号 | 规则 | 问题 | 已应用修复 |
|------|------|------|-----------|
| 42 | icon-button-a11y | onClick 处理器中的 `<YbIcon type="ic_close_16">` 缺少 aria-label | 已添加 `aria-label={t('关闭')}` |
| 78 | div-button-a11y | `<div onClick={handleClearHistory}>` 缺少 role、tabIndex、键盘交互 | 已添加 `role="button"` `tabIndex={0}` `onKeyDown` |
| 95 | img-alt-a11y | `<img src={loadingIcon.src}>` — alt="image" 无描述意义 | 已改为 `alt={t('加载中')}` |
| 120 | dialog-a11y | `<YbcDialog>` 缺少 aria-labelledby | 已添加 `aria-labelledby` 指向标题 id |
| 155 | form-label-a11y | `<input placeholder="搜索">` 缺少标签关联 | 已添加 `aria-label={t('搜索')}` |

| 180 | compat-a11y | `:focus-visible` 无 `:focus` 回退，X5 内核中焦点样式丢失 | 已添加 `:focus` 基础样式 + `:focus:not(:focus-visible)` 回退 |
| 210 | compat-a11y | `<img suppressHydrationWarning>` 缺少 alt | 已添加 `alt={t('加载中')}` |

### 汇总
- 🔴 严重：2 项（交互控件缺少标签）
- 🟡 重要：2 项（弹窗标注、表单标注）
- 🟠 兼容：2 项（焦点样式回退、水合图片 alt）
- 🟢 次要：1 项（图片 alt 改进）
- **共发现 7 个问题，已自动修复 7 个**
```
