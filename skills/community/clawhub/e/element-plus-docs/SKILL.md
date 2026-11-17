---
name: element-plus-docs
description: Element Plus 基于 Vue 3 的桌面端组件库中文文档 — 包含 83+ 个组件的 API 参考、使用示例、设计指南、安装快速上手
---

# Element Plus 文档技能

基于 Vue 3 的桌面端组件库完整中文参考。本技能整合了 Element Plus 官方文档的核心内容，包含组件 API、可直接运行的代码示例、设计原则和快速上手指导。

---

## 💡 When to Use This Skill

当用户提问涉及以下任一情况时，应立即启用本技能：

### 触发关键词
- 直接提及 **Element Plus**、**el-xxx** 组件名
- 使用 Vue 3 + Element Plus 进行开发
- 使用中文提问模式，例如：
  - "Element Plus 的 xxx 怎么用？"
  - "el-table 如何实现 xxx？"
  - "Vue 3 里怎么做 xxx？（可用 Element Plus）"
  - "给一个 el-dialog 的例子"

### 具体触发场景
- **组件 API 查询**：属性 (Attributes)、事件 (Events)、方法 (Methods)、插槽 (Slots)、暴露 (Exposes)
- **代码示例需求**：需要可直接复制运行的 Vue 3 单文件组件代码（`<script setup>`）
- **表单相关**：表单验证规则、自定义校验、动态表单项
- **表格相关**：分页、排序、筛选、多选、自定义列、合并单元格、虚拟滚动
- **反馈类**：ElMessage 消息提示、ElNotification 通知、Loading 加载、Alert 警告
- **导航类**：菜单路由、标签页、面包屑、下拉菜单
- **布局相关**：栅格系统、容器布局、间距控制、分割面板
- **集成问题**：按需引入、主题定制、暗黑模式、国际化 i18n、SSR
- **设计规范**：颜色、字体、间距等设计指南参考

### 非触发场景
- 用户明确使用其他 UI 框架（Ant Design Vue、Vuetify、Naive UI 等）
- 纯 Vue 3 核心 API 问题（不涉及 Element Plus）
- Vue 2 / Element UI 相关问题（Element Plus 仅支持 Vue 3）

---

> 📋 完整组件列表见 `references/index.md`（83 个组件 + 13 篇指南 + 6 篇补充文档）

---

## 📚 Quick Reference – 常用代码示例

以下示例均提取自官方文档，涵盖最常用的使用模式。所有示例使用 Vue 3 Composition API（`<script setup>`）。

### 1. 按钮 – 基础用法与加载态 (Button)

```vue
<template>
  <!-- 类型变体 -->
  <el-button>Default</el-button>
  <el-button type="primary">主要按钮</el-button>
  <el-button type="success">成功按钮</el-button>
  <el-button type="danger">危险按钮</el-button>

  <!-- 朴素按钮 + 圆角 + 虚线 -->
  <el-button plain>Plain</el-button>
  <el-button type="primary" round>Round</el-button>
  <el-button type="primary" dashed>Dashed</el-button>

  <!-- 带图标 + 加载态 -->
  <el-button type="primary" :icon="Search" :loading="isLoading">
    {{ isLoading ? '搜索中...' : '搜索' }}
  </el-button>

  <!-- 图标按钮组 -->
  <el-button-group>
    <el-button type="primary" :icon="ArrowLeft">上一页</el-button>
    <el-button type="primary">下一页<el-icon class="el-icon--right"><ArrowRight /></el-icon></el-button>
  </el-button-group>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
const isLoading = ref(false)
</script>
```

### 2. 表格 – 带分页与操作列 (Table)

```vue
<template>
  <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
    <el-table-column prop="name" label="姓名" width="120" />
    <el-table-column prop="role" label="角色" />
    <el-table-column label="操作" width="180">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
        <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-pagination
    v-model:current-page="page"
    v-model:page-size="pageSize"
    :page-sizes="[10, 20, 50, 100]"
    layout="total, sizes, prev, pager, next"
    :total="total"
    @size-change="handleSizeChange"
    @current-change="handlePageChange"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
const loading = ref(false)
const tableData = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const handleEdit = (row: any) => { console.log('edit', row) }
const handleDelete = (row: any) => { console.log('delete', row) }
const handleSizeChange = (size: number) => { pageSize.value = size }
const handlePageChange = (p: number) => { page.value = p }
</script>
```

### 3. 表单验证 – 带自定义校验规则 (Form Validation)

```vue
<template>
  <el-form ref="formRef" :model="form" :rules="rules" label-width="auto" status-icon>
    <el-form-item label="密码" prop="pass">
      <el-input v-model="form.pass" type="password" autocomplete="off" />
    </el-form-item>
    <el-form-item label="确认密码" prop="checkPass">
      <el-input v-model="form.checkPass" type="password" autocomplete="off" />
    </el-form-item>
    <el-form-item label="年龄" prop="age">
      <el-input v-model.number="form.age" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm">提交</el-button>
      <el-button @click="resetForm">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

const formRef = ref<FormInstance>()

const form = reactive({
  pass: '',
  checkPass: '',
  age: '',
})

const validatePass2 = (_rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.pass) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const checkAge = (_rule: any, value: number, callback: any) => {
  if (!value) return callback(new Error('请输入年龄'))
  if (!Number.isInteger(value)) return callback(new Error('请输入数字'))
  if (value < 18) return callback(new Error('年龄必须大于 18 岁'))
  callback()
}

const rules = reactive<FormRules>({
  pass: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
  age: [{ validator: checkAge, trigger: 'blur' }],
})

const submitForm = () => {
  formRef.value?.validate((valid) => {
    if (valid) console.log('提交数据:', form)
    else console.log('验证失败')
  })
}

const resetForm = () => {
  formRef.value?.resetFields()
}
</script>
```

### 4. 全局消息与通知 (ElMessage / ElNotification)

```javascript
import { ElMessage, ElNotification, ElMessageBox } from 'element-plus'

// 四种类型的消息提示
ElMessage.success('操作成功')
ElMessage.warning('请注意检查')
ElMessage.error('操作失败')
ElMessage.info('这是一条普通消息')

// 带配置的弹出通知
ElNotification({
  title: '提醒',
  message: '你有新的订单待处理',
  type: 'warning',
  duration: 5000,
  position: 'top-right',
})

// 确认对话框（替代原生 confirm）
ElMessageBox.confirm('确定删除该条记录吗？', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  type: 'warning',
}).then(() => {
  ElMessage.success('删除成功')
}).catch(() => {
  ElMessage.info('已取消删除')
})
```

---

## 📖 详细参考文件结构

> ⚠️ **上下文优化**：参考文档已拆分为 102 个独立文件（每个组件/指南一个文件）。**按需查阅**，无需一次性加载。单文件平均 < 5K tokens。

### 主参考文献
- **llms.txt**：`references/llms.txt`（快速发现入口，标准格式索引全部文档）
- **索引**：`references/index.md`（~900 tokens，按类别列出全部组件）
- **组件文档**：`references/components/{组件名}.md`（83 个文件）
- **开发指南**：`references/guides/{指南名}.md`（13 个文件）
- **补充文档**：`references/extra-guides/{文档名}.md`（更新日志、设计原则等）

### 按需查阅示例
```
查 Table 组件   → references/components/table.md  (~15K tokens)
查 Button 组件  → references/components/button.md (~4K tokens)
查 Form 验证    → references/components/form.md   (~10K tokens)
查安装指南      → references/guides/installation.md (~3K tokens)
查快速上手      → references/guides/quickstart.md   (~3K tokens)
查组件列表      → references/index.md               (~900 tokens)
```

---

## 🛠 Working with This Skill

### 1. 按需查阅组件文档
```
1. 先在 index.md 确认组件文件名
2. 读取 components/{组件名}.md 获取完整文档
3. 不要一次性加载所有组件文件（会超出上下文窗口）
```

### 2. 提取可运行的代码示例
```
1. 读取目标组件的 .md 文件
2. 寻找代码块（```vue 或 ```typescript）—— 这些是来自官方文档的完整示例
3. 示例使用 <script setup lang="ts">，可直接复制使用
4. 优先提取核心 <el-*> 模板和关键的 ref/reactive 状态
```

### 3. 查询 API 参数
```
Attributes 表格（中文表头）：
  - 属性名    → prop 名称（版本标记如 2.2.0 表示引入版本）
  - 说明      → 中文描述
  - 类型      → string / boolean / number / enum / Component
  - 默认值    → "-" 表示无默认值

Events / Slots / Exposes 表格同理
```

### 4. 应对常见需求模式

| 需求 | 搜索关键词 | 关键组件/属性 |
|------|-----------|-------------|
| 表单验证 | `el-form` + `rules` | `rules` 对象、`validator` 自定义校验函数、`formRef.value.validate()` |
| 表格分页 | `el-table` + `Pagination` | `el-pagination` 的 `@current-change`、`v-model:current-page` |
| 表格多选 | `el-table` + `selection` | `type="selection"` 列 + `@selection-change` |
| 远程搜索下拉 | `remote` + `el-select` | `remote`、`:remote-method`、`filterable` |
| 文件上传 | `el-upload` | `action`、`:before-upload`、`:on-success`、`:file-list` |
| 全局提示 | `ElMessage` / `ElNotification` | 从 `element-plus` 导入，JS 方法调用 |
| 确认弹窗 | `ElMessageBox.confirm` | 返回 Promise，`.then()` 处理确认 |
| 树形控件 | `el-tree` | `:data`、`node-key`、`check-strictly` |
| 暗黑模式 | `dark` + CSS Vars | `html.dark` 类 + `import 'element-plus/theme-chalk/dark/css-vars.css'` |

### 5. 重要注意事项
- 所有代码为 **Vue 3 Composition API** 风格（`<script setup lang="ts">`）
- 全局方法（`ElMessage`、`ElNotification`、`ElMessageBox`）需要从 `element-plus` 导入，不再挂载于 `this`
- 获取组件实例使用 `ref()` + `formRef.value`，而非 `this.$refs.xxx`
- `v-model` 支持多个绑定（`v-model:current-page`、`v-model:page-size`）
- 涉及后端交互的组件（Upload、远程搜索 Select）示例中包含模拟 API，实际使用需替换
- Element Plus 图标使用 `@element-plus/icons-vue` 包导入，不再使用 class 名

---

## 🔑 关键概念

- **Vue 3 专属**：所有组件基于 Vue 3.x，使用 Composition API（`<script setup>`），不支持 Vue 2 Options API
- **全局注册 vs 按需引入**：推荐使用 `unplugin-vue-components` 实现自动按需引入；也可使用 `app.use(ElementPlus)` 全局注册
- **双向绑定 (`v-model`)**：所有表单组件均支持 `v-model`；支持多个 v-model 绑定（如 `v-model:current-page`）
- **事件系统**：组件通过 `$emit` 派发事件，常用事件：`change`、`update:modelValue`、`click`、`blur`、`focus`
- **插槽 (Slots)**：大部分组件支持具名插槽（如 `#header`、`#footer`、`#default`、`#content`）和作用域插槽
- **全局方法**：`ElMessage`、`ElMessageBox`、`ElNotification` 从 `element-plus` 导入后在任意位置调用
- **`ref` 操作**：通过 `const formRef = ref<FormInstance>()` 获取组件实例，调用其方法（如 `validate()`、`resetFields()`）
- **Teleport**：Dialog、Drawer 等弹出层组件通过 Teleport 渲染到 body，嵌套时需设置 `append-to-body`
- **暗黑模式**：通过 `html.dark` 类切换 + CSS Vars 技术实现，可覆盖 CSS 变量自定义主题
- **虚拟滚动**：TableV2、TreeV2、SelectV2、Transfer 等组件支持虚拟滚动处理大量数据

---

## 🔒 安全注意事项

> ⚠️ 本技能示例代码仅演示组件用法，未经生产安全审查。复制到生产环境前请完成以下加固：

1. **文件上传 (el-upload)**：`accept` 属性仅为客户端提示，**可被绕过**。服务端必须独立验证文件类型、大小和内容，使用随机文件名存储
2. **XSS 防护**：使用 `v-html`、自定义渲染模板或动态插槽内容时，**必须**对用户输入做 HTML 实体转义
3. **表单验证**：`el-form` 验证规则仅提升用户体验，**不可替代服务端校验**。敏感操作（密码修改、支付、权限变更）必须服务端二次验证
4. **敏感数据**：密码（`type="password"`）传输时必须使用 HTTPS，禁止在 URL 参数或日志中传递明文密码
5. **第三方依赖**：关注 [Element Plus 官方安全公告](https://github.com/element-plus/element-plus/releases)，及时更新版本

---

## 📄 补充文档

- [快速上手](guides/quickstart.md)：完整引入 vs 按需引入、Vite/Webpack 配置
- [安装指南](guides/installation.md)：npm/CDN 安装、浏览器兼容性、Sass 版本
- [暗黑模式](guides/dark-mode.md)：CSS Vars 切换、自定义主题变量
- [国际化](guides/i18n.md)：多语言配置
- [主题定制](guides/theming.md)：CSS 变量覆盖、自定义主题
- [从 Vue 2 迁移](guides/migration.md)：Element UI → Element Plus 迁移指南
- [SSR 支持](guides/ssr.md)：Nuxt 等服务端渲染配置
- [设计原则](guides/design.md)：一致性、反馈、效率、可控
- [导航指南](guides/nav.md)：侧边导航、顶部导航设计规范
- [更新日志](extra-guides/changelog.md)：完整版本历史

---

## ⚡ Element UI (Vue 2) → Element Plus (Vue 3) 关键差异

| Element UI (Vue 2) | Element Plus (Vue 3) |
|---------------------|----------------------|
| `this.$message()` | `import { ElMessage } from 'element-plus'` |
| `this.$refs.xxx.validate()` | `const ref = ref<FormInstance>(); ref.value?.validate()` |
| `slot-scope="scope"` | `#default="scope"` 或 `v-slot` |
| `v-model` 单个绑定 | 支持多 `v-model`（如 `v-model:current-page`） |
| 图标 class 名（`el-icon-xxx`） | 组件导入（`import { Search } from '@element-plus/icons-vue'`） |
| `data()`, `methods`, `computed` | `<script setup>` + `ref()` / `reactive()` / `computed()` |
| `Vue.use(ElementUI)` | `app.use(ElementPlus)` 或按需引入 |

---

*Generated by Skill Seeker + manual optimization — 基于 Element Plus 官方中文文档 v2.14.3*
