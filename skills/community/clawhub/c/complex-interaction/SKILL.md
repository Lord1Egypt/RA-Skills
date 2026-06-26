---
name: complex-interaction
description: Implements complex frontend interactions: drag-and-drop, virtual scrolling, rich text editors, real-time collaboration, canvas/WebGL, and gesture handling. Use when 拖拽, 虚拟滚动, 富文本, 实时协作, Canvas, WebGL, 手势, or complex UI interactions.
model: opus
---

# 复杂交互实现（Complex Interaction）

实现拖拽排序、虚拟滚动、富文本编辑器、实时协作、Canvas/WebGL 等高难度交互，给出可落地的方案和关键代码。

## 触发场景

- 「拖拽排序怎么做」「拖拽上传」「看板拖拽」
- 「列表有几万条，怎么不卡」「虚拟滚动」
- 「富文本编辑器」「表格编辑器」「低代码画布」
- 「多人实时协作」「冲突解决」
- 「Canvas 性能优化」「WebGL 入门」「手势识别」

---

## 执行流程

### 1. 先判断复杂度，选对方案

不要上来就自己实现，先评估：

| 场景 | 推荐方案 | 自己实现的条件 |
|------|---------|--------------|
| 简单拖拽排序（同列表） | `@dnd-kit/sortable` | 几乎不需要 |
| 复杂拖拽（跨容器、看板、树形） | `@dnd-kit/core` 自定义 | 有特殊约束时 |
| 长列表虚拟滚动 | `@tanstack/react-virtual` | 几乎不需要 |
| 富文本编辑器 | Tiptap / Slate.js | 极度定制化需求 |
| 实时协作 | Yjs + 对应绑定 | 几乎不需要 |
| Canvas 2D 交互 | Konva.js / Fabric.js | 性能极限场景 |
| 3D / WebGL | Three.js / React Three Fiber | 几乎不需要 |

**自己实现的成本远超预期**——拖拽涉及触摸事件、键盘无障碍、滚动容器、嵌套列表，富文本涉及光标、选区、撤销栈，这些库已经踩过所有坑。

### 2. 拖拽排序

**标准实现（@dnd-kit）：**

```tsx
import { DndContext, closestCenter } from '@dnd-kit/core'
import { SortableContext, useSortable, verticalListSortingStrategy, arrayMove } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'

function SortableItem({ id, children }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id })
  return (
    <div
      ref={setNodeRef}
      style={{
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1,
      }}
      {...attributes}
      {...listeners}
    >
      {children}
    </div>
  )
}

function SortableList({ items, onReorder }) {
  return (
    <DndContext
      collisionDetection={closestCenter}
      onDragEnd={({ active, over }) => {
        if (over && active.id !== over.id) {
          const oldIndex = items.findIndex(i => i.id === active.id)
          const newIndex = items.findIndex(i => i.id === over.id)
          onReorder(arrayMove(items, oldIndex, newIndex))
        }
      }}
    >
      <SortableContext items={items.map(i => i.id)} strategy={verticalListSortingStrategy}>
        {items.map(item => (
          <SortableItem key={item.id} id={item.id}>{item.name}</SortableItem>
        ))}
      </SortableContext>
    </DndContext>
  )
}
```

**跨容器拖拽（看板）的关键点：**
- 用 `DragOverlay` 渲染拖拽中的预览，避免原位置闪烁
- 用 `over.data.current` 判断拖到了哪个容器
- 状态更新要在 `onDragEnd` 里做，`onDragOver` 只做视觉反馈

**拖拽上传的关键点：**
- 用原生 `dragover` + `drop` 事件，不需要 dnd-kit
- `dragover` 必须 `preventDefault()` 才能触发 `drop`
- 用 `DataTransfer.items` 处理文件夹递归上传

### 3. 虚拟滚动

**何时需要虚拟滚动：** 列表超过 500 条且有明显卡顿，或超过 2000 条无论是否卡顿。

**标准实现（@tanstack/react-virtual）：**

```tsx
import { useVirtualizer } from '@tanstack/react-virtual'

function VirtualList({ items }) {
  const parentRef = useRef(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 56,          // 预估行高，影响滚动条比例
    overscan: 5,                      // 视口外额外渲染的行数
  })

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize() }}>  {/* 撑开滚动高度 */}
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              transform: `translateY(${virtualRow.start}px)`,
              height: `${virtualRow.size}px`,
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  )
}
```

**动态行高的处理：**

```tsx
const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 56,
  // 测量实际渲染高度，自动修正
  measureElement: (el) => el.getBoundingClientRect().height,
})

// 在每个 item 上加 ref
<div ref={virtualizer.measureElement} data-index={virtualRow.index}>
```

**虚拟滚动 + 无限加载：**

```tsx
// 监听最后一个 item 进入视口
useEffect(() => {
  const lastItem = virtualItems[virtualItems.length - 1]
  if (!lastItem) return
  if (lastItem.index >= items.length - 1 && hasNextPage && !isFetchingNextPage) {
    fetchNextPage()
  }
}, [virtualItems, items.length, hasNextPage, isFetchingNextPage])
```

### 4. 富文本编辑器

**选型决策：**
- 需要协作编辑 → Tiptap（基于 ProseMirror，有 Yjs 扩展）
- 需要高度定制数据结构 → Slate.js（数据模型完全可控）
- 简单格式化（加粗/斜体/链接）→ Tiptap 基础版，5 分钟搭起来
- 类 Notion 块编辑器 → Tiptap + 自定义 Node

**Tiptap 快速上手：**

```tsx
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'

function RichTextEditor({ value, onChange }) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({ placeholder: '开始输入...' }),
    ],
    content: value,
    onUpdate: ({ editor }) => onChange(editor.getHTML()),
  })

  return (
    <div className="editor-wrapper">
      <Toolbar editor={editor} />
      <EditorContent editor={editor} />
    </div>
  )
}

function Toolbar({ editor }) {
  if (!editor) return null
  return (
    <div>
      <button onClick={() => editor.chain().focus().toggleBold().run()}
        className={editor.isActive('bold') ? 'active' : ''}>B</button>
      <button onClick={() => editor.chain().focus().toggleItalic().run()}>I</button>
    </div>
  )
}
```

### 5. 实时协作（Yjs）

**Yjs 的核心概念：**
- `Y.Doc`：共享文档，所有协作数据的容器
- CRDT：冲突自动合并，不需要手写冲突解决逻辑
- Provider：传输层（WebSocket、WebRTC、IndexedDB 本地持久化）

**与 Tiptap 集成：**

```tsx
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'
import { Collaboration } from '@tiptap/extension-collaboration'
import { CollaborationCursor } from '@tiptap/extension-collaboration-cursor'

const ydoc = new Y.Doc()
const provider = new WebsocketProvider('wss://your-server.com', 'room-name', ydoc)

const editor = useEditor({
  extensions: [
    StarterKit.configure({ history: false }),  // 禁用内置 history，用 Yjs 的
    Collaboration.configure({ document: ydoc }),
    CollaborationCursor.configure({
      provider,
      user: { name: '张三', color: '#f783ac' },
    }),
  ],
})
```

**后端 WebSocket 服务器（y-websocket）：**

```bash
# 最简单的方式：直接用官方服务器
HOST=localhost PORT=1234 npx y-websocket
```

### 6. Canvas 性能优化

**Canvas 卡顿的常见原因：**

| 原因 | 解法 |
|------|------|
| 每帧重绘整个画布 | 分层 Canvas（静态背景一层，动态元素一层） |
| 在主线程做大量计算 | 用 `OffscreenCanvas` + Web Worker |
| 频繁创建/销毁对象 | 对象池（Object Pool） |
| 没有用 `requestAnimationFrame` | 用 rAF 驱动动画循环 |
| 高 DPI 屏幕模糊 | `canvas.width = width * devicePixelRatio` |

**高 DPI 修复：**

```ts
function setupCanvas(canvas: HTMLCanvasElement) {
  const dpr = window.devicePixelRatio || 1
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  const ctx = canvas.getContext('2d')!
  ctx.scale(dpr, dpr)
  return ctx
}
```

**分层 Canvas（低代码画布场景）：**

```tsx
// 背景网格层（静态，只在 resize 时重绘）
<canvas ref={bgRef} style={{ position: 'absolute' }} />
// 元素层（拖拽时重绘）
<canvas ref={elementsRef} style={{ position: 'absolute' }} />
// 交互层（hover/选中高亮，频繁重绘）
<canvas ref={interactionRef} style={{ position: 'absolute' }} />
```

---

## 常见坑

| 场景 | 坑 | 解法 |
|------|-----|------|
| 拖拽 | 触摸设备不触发 mouse 事件 | dnd-kit 已处理，自己实现要加 touch 事件 |
| 虚拟滚动 | 滚动到底部时跳动 | 用 `measureElement` 测量实际高度 |
| 富文本 | 粘贴时带入外部样式 | 配置 `transformPastedHTML` 清理 |
| 实时协作 | 断线重连后数据不一致 | y-websocket 自动处理，确保 provider 有重连逻辑 |
| Canvas | 事件坐标偏移 | 用 `canvas.getBoundingClientRect()` 转换坐标 |
