# Vue 3 编码规范（前端工程师实现必读）

适用：Vue 3.4+ / `<script setup>` + TypeScript strict / Vite / Vue Router 4 / Pinia。

## 1. 工程结构

```
src/
├── api/            # 请求层：client 封装 + 按域模块 + 类型定义
├── components/
│   ├── base/       # 基础组件（Base 前缀：BaseButton、BaseInput，五态齐全）
│   └── business/   # 业务组件
├── views/          # 路由页面
├── composables/    # useXxx 组合式函数
├── stores/         # Pinia store（按域拆分）
├── router/         # 路由（路由级懒加载）
├── types/          # 全局类型
└── utils/
```

## 2. 组件规则

- 一律 `<script setup lang="ts">`；组件名多词（基础组件 Base 前缀）；
  单文件组件 ≤ 200 行，超限拆子组件。
- Props 用 `defineProps<{...}>()` 类型声明 + 运行时校验（复杂校验用 validator）；
  事件 `defineEmits<{...}>()` 显式声明；`defineModel` 处理双向绑定。
- 模板内不写复杂逻辑（计算属性/方法承接）；`v-if` 与 `v-for` 不同节点，
  必须 `v-for` 时 key 用稳定业务 id 禁止下标。
- 复用逻辑抽 `composables/useXxx.ts`（`use` 前缀、返回响应式引用、内部可组合生命周期），
  禁止 mixin。

## 3. 类型纪律

- `strict: true`；禁止 `any` 与 `as` 断言链；API 响应类型集中在 `api/` 定义，
  组件从 api 层导入，不重复手写。
- ref 泛型显式：`ref<Order[]>([])`；解构 props 保响应式（`toRefs`）；
  Pinia store 中 state 用类型断言到接口定义（`state: () => ({ list: [] as Order[] })`）。

## 4. 状态与数据

- Pinia 按域拆 store；服务端数据与 UI 态分仓；服务端数据优先 `@tanstack/vue-query`
  或组合式请求 hook（useXxxApi：loading/error/data/refresh 一体）。
- 跨组件通信优先 props/emit 与 store；禁用全局事件总线。
- 依赖注入 `provide/inject` 必须带类型 key（`InjectionKey<T>`）。

## 5. 性能与可达性

- 路由组件 `() => import(...)` 懒加载；`v-memo`/`shallowRef` 先测后用。
- `v-for` 大列表虚拟滚动（@tanstack/vue-virtual）。
- 语义化标签、键盘可遍历、focus-visible 样式；表单 label 关联。

## 6. 质量命令

```bash
npm run lint && npm run build && npm run test:unit -- --run
```

提交前三项全过；ESLint（vue + typescript-eslint strict）无 ERROR。
