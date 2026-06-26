# Complex Interaction（复杂交互实现）

实现拖拽排序、虚拟滚动、富文本编辑器、实时协作、Canvas 优化等高难度交互，给出可落地的方案和关键代码。

## What It Does

- 用 @dnd-kit 实现拖拽排序、跨容器看板、拖拽上传
- 用 @tanstack/react-virtual 实现虚拟滚动（含动态行高、无限加载）
- 用 Tiptap 快速搭建富文本编辑器，支持自定义扩展
- 用 Yjs + y-websocket 实现多人实时协作（CRDT 自动冲突合并）
- Canvas 分层渲染、高 DPI 适配、OffscreenCanvas + Web Worker 优化

## How to Use

当用户说「拖拽排序」「虚拟滚动」「富文本编辑器」「实时协作」「Canvas 卡顿」时触发。先评估是否需要自己实现（通常不需要），给出推荐库和关键代码，并列出常见坑。

## Requirements

- 拖拽：@dnd-kit/core @dnd-kit/sortable
- 虚拟滚动：@tanstack/react-virtual
- 富文本：@tiptap/react @tiptap/starter-kit
- 实时协作：yjs y-websocket
- 适用于 React 项目
