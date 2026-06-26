# React 组合模式总结

> 来源：Vercel React Composition Patterns
> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 核心原则

1. **组合优于配置** — 通过组合而不是添加props来定制组件
2. **提升状态** — 状态放在提供者中，不要被困在组件里
3. **组合内部实现** — 子组件访问context，而不是props
4. **明确的变体** — 创建ThreadComposer、EditComposer，而不是带isThread的Composer

---

## 一、Component Architecture（组件架构）CRITICAL

### 1.1 Avoid Boolean Props（避免布尔属性）

**问题：**
- 布尔属性爆炸式增长
- 组件行为难以预测
- 可维护性下降

**错误示例：**
```tsx
// ❌ 不要这样做
<Button 
  isPrimary
  isLarge
  isDisabled
  isLoading
  hasIcon
/>
```

**正确示例：**
```tsx
// ✅ 使用组合变体
<PrimaryButton size="large">
  <Spinner />
  Submit
</PrimaryButton>
```

**原则：**
- 不要通过布尔属性定制行为
- 当属性超过2-3个时考虑拆分
- 创建明确的组件变体

---

### 1.2 Compound Components（复合组件）

**概念：**
- 将组件拆分为多个子组件
- 通过context共享状态
- 灵活的组合方式

**示例：**
```tsx
// ✅ 复合组件模式
<Dropdown>
  <Dropdown.Trigger>Open Menu</Dropdown.Trigger>
  <Dropdown.Menu>
    <Dropdown.Item>Item 1</Dropdown.Item>
    <Dropdown.Item>Item 2</Dropdown.Item>
  </Dropdown.Menu>
</Dropdown>
```

**优势：**
- 灵活性高
- API清晰
- 易于扩展
- 避免props传递

---

## 二、State Management（状态管理）HIGH

### 2.1 Lift State（提升状态）

**概念：**
- 将状态提升到provider组件
- 子组件通过context访问状态
- 避免状态下沉

**示例：**
```tsx
// ✅ 状态在provider中
<DialogProvider>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Content>Content</Dialog.Content>
</DialogProvider>
```

**优势：**
- 状态集中管理
- 易于测试
- 更好的复用性

---

### 2.2 Context Interface（Context接口）

**原则：**
- 定义清晰的context接口
- 包含state/actions/meta
- 类型安全

**示例：**
```tsx
interface DialogContext {
  isOpen: boolean;
  open: () => void;
  close: () => void;
}
```

---

### 2.3 Decouple Implementation（解耦实现）

**原则：**
- 状态管理与UI解耦
- 通过接口定义契约
- 实现可替换

---

## 三、Implementation Patterns（实现模式）MEDIUM

### 3.1 Children Over Render Props（Children优于Render Props）

**概念：**
- 优先使用children而不是renderX props
- 更自然的API
- 更好的TypeScript支持

**错误示例：**
```tsx
// ❌ 避免
<List 
  renderItem={(item) => <div>{item}</div>}
/>
```

**正确示例：**
```tsx
// ✅ 优先
<List>
  {items.map(item => (
    <List.Item key={item.id}>{item}</List.Item>
  ))}
</List>
```

---

### 3.2 Explicit Variants（明确变体）

**概念：**
- 创建明确的组件变体
- 避免通用组件加条件
- 更清晰的意图表达

**错误示例：**
```tsx
// ❌ 避免
<Composer isThread isEdit />
```

**正确示例：**
```tsx
// ✅ 明确变体
<ThreadComposer />
<EditComposer />
```

---

## 影响等级说明

- **CRITICAL** - 基础模式，防止不可维护代码
- **HIGH** - 显著的可维护性改进
- **MEDIUM** - 良好实践，代码更整洁

---

## 适用场景

### 适合使用组合模式的场景：
- UI组件库开发
- 复杂的交互组件
- 需要高度灵活性的组件
- 长期维护的项目

### 不适合的场景：
- 简单的一次性组件
- 原型快速开发
- 小团队快速迭代

---

## 最佳实践

1. **渐进式采用**：从简单组件开始，逐步应用
2. **保持简单**：不要过度设计，根据实际需求选择
3. **文档化**：清晰的使用示例和文档
4. **TypeScript优先**：利用类型系统提供更好的开发体验
5. **测试友好**：便于单元测试和集成测试

---

## 相关资源

- React官方文档 - Composition vs Inheritance
- Vercel Design Systems Guide
- Compound Components Pattern

