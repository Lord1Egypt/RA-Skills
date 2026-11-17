---
name: element-ui-docs
description: Element UI 基于 Vue 2.0 的桌面端组件库中文文档 - 包含 60+ 组件的 API 参考、使用示例、设计指南、安装快速上手
---

# Element UI 文档技能

基于 Vue 2.0 的桌面端组件库完整中文参考。本技能整合了 Element UI 的全部官方文档页，包含组件 API、可直接运行的代码示例、设计原则和快速上手指导。

---

## 💡 When to Use This Skill

当用户提问涉及以下任一情况时，应立即启用本技能：

### 触发关键词
- 直接提及 **Element UI**、**Element**、**饿了么 UI**、**el-xxx** 组件名
- 使用中文提问模式，例如：
  - "Element UI 的 xxx 怎么用？"
  - "el-table 如何实现 xxx？"
  - "Vue 2 里怎么做 xxx？（可用 Element UI）"
  - "给一个 el-dialog 的例子"

### 具体触发场景
- **组件 API 查询**：属性 (Attributes)、事件 (Events)、方法 (Methods)、插槽 (Slots)
- **代码示例需求**：需要可直接复制运行的 Vue 2 单文件组件代码
- **表单相关**：表单验证规则、自定义校验、动态表单项
- **表格相关**：分页、排序、筛选、多选、自定义列、合并单元格
- **反馈类**：Message 消息提示、Notification 通知、Loading 加载、Alert 警告
- **导航类**：菜单路由、标签页、面包屑、下拉菜单
- **布局相关**：栅格系统、容器布局、间距控制
- **集成问题**：按需引入、主题定制、国际化、自定义主题
- **设计规范**：颜色、字体、间距等设计指南参考

### 非触发场景
- 用户明确使用其他 UI 框架（Ant Design Vue、Vuetify、Naive UI 等）
- 纯 Vue 2 核心 API 问题（不涉及 Element UI）
- Vue 3 / Element Plus 相关问题（Element UI 仅支持 Vue 2）

---

> 📋 完整组件列表见 `references/index.md`（61 个组件 + 5 篇指南）

---

## 📚 Quick Reference – 常用代码示例

以下示例均提取自官方文档，涵盖最常用的使用模式。假设已通过 `Vue.use(ElementUI)` 全局注册所有组件。

### 1. 按钮 – 基础用法与加载态 (Button)
```html
<!-- 类型变体 -->
<el-button type="primary">主要按钮</el-button>
<el-button type="success">成功按钮</el-button>
<el-button type="danger">危险按钮</el-button>

<!-- 带图标 + 加载态 -->
<el-button type="primary" icon="el-icon-search" :loading="isLoading">
  {{ isLoading ? '搜索中...' : '搜索' }}
</el-button>
```

### 2. 表格 – 带分页与操作列 (Table + Pagination)
```html
<el-table :data="tableData" border stripe style="width: 100%">
  <el-table-column prop="name" label="姓名" width="120"></el-table-column>
  <el-table-column prop="role" label="角色"></el-table-column>
  <el-table-column label="操作" width="150">
    <template slot-scope="scope">
      <el-button size="mini" @click="handleEdit(scope.row)">编辑</el-button>
      <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
    </template>
  </el-table-column>
</el-table>

<el-pagination
  @current-change="handlePageChange"
  :current-page="page"
  :page-size="pageSize"
  layout="total, prev, pager, next"
  :total="total">
</el-pagination>
```

### 3. 表单验证 – 带自定义校验规则 (Form Validation)
```html
<el-form :model="form" :rules="rules" ref="form" label-width="80px">
  <el-form-item label="用户名" prop="username">
    <el-input v-model="form.username"></el-input>
  </el-form-item>
  <el-form-item label="邮箱" prop="email">
    <el-input v-model="form.email"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="submitForm">提交</el-button>
    <el-button @click="resetForm">重置</el-button>
  </el-form-item>
</el-form>

<script>
export default {
  data() {
    const validateEmail = (rule, value, callback) => {
      if (!value) return callback(new Error('邮箱不能为空'));
      const re = /\S+@\S+\.\S+/;
      re.test(value) ? callback() : callback(new Error('邮箱格式不正确'));
    };
    return {
      form: { username: '', email: '' },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 16, message: '长度在 3 到 16 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, validator: validateEmail, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    submitForm() {
      this.$refs.form.validate(valid => {
        if (valid) console.log('提交数据:', this.form);
      });
    },
    resetForm() {
      this.$refs.form.resetFields();
    }
  }
};
</script>
```

### 4. 全局消息与通知 (Message / Notification)
```javascript
// 四种类型的消息提示
this.$message.success('操作成功');
this.$message.warning('请注意检查');
this.$message.error('操作失败');
this.$message.info('这是一条普通消息');

// 带配置的弹出通知
this.$notify({
  title: '提醒',
  message: '你有新的订单待处理',
  type: 'warning',
  duration: 5000,
  position: 'top-right'
});

// 确认对话框（替代原生 confirm）
this.$confirm('确定删除该条记录吗？', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  type: 'warning'
}).then(() => {
  this.$message.success('删除成功');
}).catch(() => {
  this.$message.info('已取消删除');
});
```


---

## 📖 详细参考文件结构

> ⚠️ **上下文优化**：参考文档已拆分为 66 个独立文件（每个组件/指南一个文件）。**按需查阅**，无需一次性加载。单文件平均 ~2.7K tokens。

### 主参考文献
- **llms.txt**：`references/llms.txt`（快速发现入口，标准格式索引全部文档）
- **索引**：`references/index.md`（~900 tokens）
- **组件文档**：`references/components/{组件名}.md`（61 个文件）
- **开发指南**：`references/guides/{指南名}.md`（5 个文件）

### 按需查阅示例
```
查 Table 组件  → references/components/table.md   (~20K tokens)
查 Button 组件 → references/components/button.md  (~2K tokens)
查快速上手     → references/guides/quickstart.md   (~3K tokens)
查组件列表     → references/index.md               (~900 tokens)
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
2. 寻找 ````html` 代码块 —— 这些是完整可运行的示例
3. 示例自包含 <template>、<script>，可直接使用
4. 优先提取核心 <el-*> 模板和关键的 data/methods
```

### 3. 查询 API 参数
```
Attributes 表格（中文表头）：
  - 参数     → prop 名称
  - 类型     → string / boolean / number / array / object / function
  - 可选值   → 枚举值范围
  - 默认值   → "-" 表示无默认值

Events / Methods / Slots 表格同理，表头为中文
```

### 4. 应对常见需求模式

| 需求 | 搜索关键词 | 关键组件/属性 |
|------|-----------|-------------|
| 表单验证 | `el-form` + `rules` | `rules` 对象、`validator` 自定义校验函数、`validate()` |
| 表格分页 | `el-table` + `Pagination` | `el-pagination` 的 `@current-change`、`:total` |
| 表格多选 | `el-table` + `selection` | `type="selection"` 列 + `@selection-change` |
| 远程搜索下拉 | `remote` + `el-select` | `remote`、`:remote-method`、`filterable` |
| 文件上传 | `el-upload` | `action`、`:before-upload`、`:on-success`、`:file-list` |
| 全局提示 | `$message` / `$notify` | JS 方法调用，无需组件标签 |
| 确认弹窗 | `$confirm` | 返回 Promise，`.then()` 处理确认 |
| 树形控件 | `el-tree` | `:data`、`node-key`、`check-strictly` |

### 5. 重要注意事项
- 所有代码为 **Vue 2 Options API** 风格（`data()`, `methods`, `computed` 等）
- `v-model` 双向绑定的值类型需与组件期望一致（如 `el-select` 多选时期望数组）
- 涉及后端交互的组件（Upload、远程搜索 Select）示例中包含模拟 API，实际使用需替换
- 全局方法（`$message`、`$notify`、`$confirm`）挂载在 Vue 原型上，不需要额外引入

---

## 🔑 关键概念

- **Vue 2 专属**：所有组件基于 Vue 2.x，使用 Options API，不支持 Vue 3 Composition API
- **全局注册 vs 按需引入**：推荐配合 `babel-plugin-component` 按需引入以减小打包体积；文档示例默认已全局注册
- **双向绑定 (`v-model`)**：所有表单组件均支持 `v-model`，内部已处理 `:value` 和 `@input`
- **事件系统**：组件通过 `$emit` 派发事件，常用事件：`change`、`input`、`click`、`select`、`blur`、`focus`
- **插槽 (Slots)**：大部分组件支持具名插槽（如 `header`、`footer`、`label`、`default`）和默认插槽
- **全局方法**：`$message`、`$confirm`、`$alert`、`$prompt`、`$notify` 挂载于 `Vue.prototype`，可在任意组件 `this` 上调用
- **`$refs` 操作**：通过 `this.$refs.xxx` 获取组件实例，调用其方法（如表单的 `validate()`、`resetFields()`）
- **`$nextTick`**：在数据变更后需等到 DOM 更新完成才能操作组件时使用，常用于自动聚焦、展开等场景
- **响应式规则**：遵循 Vue 2 响应式限制，对象属性的新增/删除需使用 `this.$set()` / `this.$delete()`

---

## 🔒 安全注意事项

> ⚠️ 本技能示例代码仅演示组件用法，未经生产安全审查。复制到生产环境前请完成以下加固：

1. **文件上传 (el-upload)**：`accept` 属性仅为客户端提示，**可被绕过**。服务端必须独立验证文件类型、大小和内容，使用随机文件名存储
2. **XSS 防护**：使用 `v-html`、自定义渲染模板或动态插槽内容时，**必须**对用户输入做 HTML 实体转义
3. **表单验证**：`el-form` 验证规则仅提升用户体验，**不可替代服务端校验**。敏感操作（密码修改、支付、权限变更）必须服务端二次验证
4. **敏感数据**：密码（`type="password"`）传输时必须使用 HTTPS，禁止在 URL 参数或日志中传递明文密码
5. **第三方依赖**：关注 [Element UI 官方安全公告](https://github.com/ElemeFE/element/releases)

## 📄 补充文档

- [设计原则](extra-guides/design.md)：一致性、反馈、效率、可控四大设计原则
- [导航指南](extra-guides/nav.md)：侧边导航、顶部导航的设计规范
- [更新日志](extra-guides/changelog.md)：完整版本历史

---

*Generated by Skill Seeker's unified multi-source scraper*