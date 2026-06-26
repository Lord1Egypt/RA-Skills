# L2前端测试模板

**适用**: BUILD-TEST任务生成L2前端测试时使用
**核心原则**: 测试必须覆盖真实组件，禁止使用内联假组件

---

## 必须遵守的规则

### ✅ 必须导入真实组件

```typescript
// ✅ 正确：导入真实组件
import ReportsPage from '@/views/ReportsPage.vue'
import ReportGenerate from '@/components/modules/ReportGenerate.vue'

const wrapper = mount(ReportsPage, {
  global: { plugins: [pinia, router] }
})
```

### ❌ 禁止使用内联假组件

```typescript
// ❌ 错误：定义内联假组件
const EmptyReportList = {
  template: `<div class="reports-page">...</div>`,
  props: {...}
}
const wrapper = mount(EmptyReportList, {...})
```

**为什么禁止？**
- 内联组件测试的是"测试代码中写的模板"，不是"真实程序代码"
- 无法发现程序BUG，只能发现测试自己的问题
- 测试失去意义

---

## L2前端测试标准结构

```typescript
/**
 * DeepTutor-Lite M-XX FE-L2 测试
 * 场景：S-XXX-XXX
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'

// ✅ 导入真实组件
import TargetComponent from '@/views/TargetPage.vue'
import ChildComponent from '@/components/modules/ChildComponent.vue'

// Mock API
vi.mock('@/api/module', () => ({
  apiMethod: vi.fn(),
}))

import { apiMethod } from '@/api/module'

// Mock数据
const mockData = {
  // ...
}

// 创建测试路由
const createTestRouter = () => createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/target', name: 'Target', component: { template: '<div />' } }
  ]
})

// 创建包装器工厂函数
function createWrapper() {
  return mount(TargetComponent, {
    global: {
      plugins: [createPinia(), createTestRouter()],
      stubs: {
        // 可选：stub子组件以隔离测试
        ChildComponent: true,
      }
    }
  })
}

describe('场景名称', () => {
  beforeEach(async () => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('功能点1', () => {
    it('应正确显示XXX', async () => {
      // Mock数据
      vi.mocked(apiMethod).mockResolvedValueOnce({ code: 'SUCCESS', data: mockData })

      // 挂载真实组件
      const wrapper = createWrapper()
      await flushPromises()

      // 验证DOM
      expect(wrapper.find('.target-element').exists()).toBe(true)
      expect(wrapper.text()).toContain('期望文本')
    })
  })
})
```

---

## 验证检查清单

验证子代理检查BUILD-TEST产出时，必须确认：

| 检查项 | 通过条件 |
|--------|---------|
| 导入真实组件 | 测试文件包含 `import ... from '@/views/` 或 `import ... from '@/components/` |
| 无内联假组件 | 不存在 `const Xxx = { template: ... }` 模式 |
| Mock正确配置 | API Mock返回数据结构符合API设计文档 |
| 断言验证DOM | 使用 `wrapper.find()`, `wrapper.text()`, `wrapper.findAll()` 而非 `wrapper.vm.xxx` |

---

## 铁律

1. **必须导入真实组件** — 测试真实程序代码，不是测试假组件
2. **禁止定义内联组件** — 内联组件测试毫无意义
3. **Mock必须符合API设计** — 返回数据结构必须与API文档一致
4. **断言验证用户可见行为** — DOM文本、样式、交互，不是内部状态

---

**更新时间**: 2026-05-13
**更新原因**: M-03 FE-L2测试发现子代理使用内联假组件，导致测试无效
