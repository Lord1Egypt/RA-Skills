---
name: "autocomplete"
description: "Autocomplete 自动补全输入框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Autocomplete 自动补全输入框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/autocomplete.html"
---

---

# 自动补全输入框 [​](#自动补全输入框)

更新日志待解决

6

根据输入内容提供对应的输入建议。

## 基础用法 [​](#基础用法)

Autocomplete 组件提供输入建议。

`fetch-suggestions` 属性是返回建议输入的方法。 在此示例中， `querySearch(queryString, cb)` 方法通过 `cb(data)` 给 Autocomplete 组件返回建议。

list suggestions when activated

list suggestions on input

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1hdXRvY29tcGxldGVcIj5cbiAgICA8ZGl2IGNsYXNzPVwiZGVtby1ibG9ja1wiPlxuICAgICAgPGRpdiBjbGFzcz1cImRlbW8tdGl0bGVcIj5saXN0IHN1Z2dlc3Rpb25zIHdoZW4gYWN0aXZhdGVkPC9kaXY+XG4gICAgICA8ZWwtYXV0b2NvbXBsZXRlXG4gICAgICAgIHYtbW9kZWw9XCJzdGF0ZTFcIlxuICAgICAgICA6ZmV0Y2gtc3VnZ2VzdGlvbnM9XCJxdWVyeVNlYXJjaFwiXG4gICAgICAgIGNsZWFyYWJsZVxuICAgICAgICBjbGFzcz1cInctNTBcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBJbnB1dFwiXG4gICAgICAgIEBzZWxlY3Q9XCJoYW5kbGVTZWxlY3RcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiZGVtby1ibG9ja1wiPlxuICAgICAgPGRpdiBjbGFzcz1cImRlbW8tdGl0bGVcIj5saXN0IHN1Z2dlc3Rpb25zIG9uIGlucHV0PC9kaXY+XG4gICAgICA8ZWwtYXV0b2NvbXBsZXRlXG4gICAgICAgIHYtbW9kZWw9XCJzdGF0ZTJcIlxuICAgICAgICA6ZmV0Y2gtc3VnZ2VzdGlvbnM9XCJxdWVyeVNlYXJjaFwiXG4gICAgICAgIDp0cmlnZ2VyLW9uLWZvY3VzPVwiZmFsc2VcIlxuICAgICAgICBjbGVhcmFibGVcbiAgICAgICAgY2xhc3M9XCJ3LTUwXCJcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgSW5wdXRcIlxuICAgICAgICBAc2VsZWN0PVwiaGFuZGxlU2VsZWN0XCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IG9uTW91bnRlZCwgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbnRlcmZhY2UgUmVzdGF1cmFudEl0ZW0ge1xuICB2YWx1ZTogc3RyaW5nXG4gIGxpbms6IHN0cmluZ1xufVxuXG5jb25zdCBzdGF0ZTEgPSByZWYoJycpXG5jb25zdCBzdGF0ZTIgPSByZWYoJycpXG5cbmNvbnN0IHJlc3RhdXJhbnRzID0gcmVmPFJlc3RhdXJhbnRJdGVtW10+KFtdKVxuY29uc3QgcXVlcnlTZWFyY2ggPSAocXVlcnlTdHJpbmc6IHN0cmluZywgY2I6IGFueSkgPT4ge1xuICBjb25zdCByZXN1bHRzID0gcXVlcnlTdHJpbmdcbiAgICA/IHJlc3RhdXJhbnRzLnZhbHVlLmZpbHRlcihjcmVhdGVGaWx0ZXIocXVlcnlTdHJpbmcpKVxuICAgIDogcmVzdGF1cmFudHMudmFsdWVcbiAgLy8gY2FsbCBjYWxsYmFjayBmdW5jdGlvbiB0byByZXR1cm4gc3VnZ2VzdGlvbnNcbiAgY2IocmVzdWx0cylcbn1cbmNvbnN0IGNyZWF0ZUZpbHRlciA9IChxdWVyeVN0cmluZzogc3RyaW5nKSA9PiB7XG4gIHJldHVybiAocmVzdGF1cmFudDogUmVzdGF1cmFudEl0ZW0pID0+IHtcbiAgICByZXR1cm4gKFxuICAgICAgcmVzdGF1cmFudC52YWx1ZS50b0xvd2VyQ2FzZSgpLmluZGV4T2YocXVlcnlTdHJpbmcudG9Mb3dlckNhc2UoKSkgPT09IDBcbiAgICApXG4gIH1cbn1cbmNvbnN0IGxvYWRBbGwgPSAoKSA9PiB7XG4gIHJldHVybiBbXG4gICAgeyB2YWx1ZTogJ3Z1ZScsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vdnVlanMvdnVlJyB9LFxuICAgIHsgdmFsdWU6ICdlbGVtZW50JywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS9FbGVtZUZFL2VsZW1lbnQnIH0sXG4gICAgeyB2YWx1ZTogJ2Nvb2tpbmcnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL0VsZW1lRkUvY29va2luZycgfSxcbiAgICB7IHZhbHVlOiAnbWludC11aScsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vRWxlbWVGRS9taW50LXVpJyB9LFxuICAgIHsgdmFsdWU6ICd2dWV4JywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS92dWVqcy92dWV4JyB9LFxuICAgIHsgdmFsdWU6ICd2dWUtcm91dGVyJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS92dWVqcy92dWUtcm91dGVyJyB9LFxuICAgIHsgdmFsdWU6ICdiYWJlbCcsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vYmFiZWwvYmFiZWwnIH0sXG4gIF1cbn1cblxuY29uc3QgaGFuZGxlU2VsZWN0ID0gKGl0ZW06IFJlY29yZDxzdHJpbmcsIGFueT4pID0+IHtcbiAgY29uc29sZS5sb2coaXRlbSlcbn1cblxub25Nb3VudGVkKCgpID0+IHtcbiAgcmVzdGF1cmFudHMudmFsdWUgPSBsb2FkQWxsKClcbn0pXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWF1dG9jb21wbGV0ZSB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtd3JhcDogd3JhcDtcbiAgZ2FwOiAycmVtO1xufVxuXG4uZGVtby1ibG9jayB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gIGdhcDogMC41cmVtO1xufVxuXG4uZGVtby10aXRsZSB7XG4gIGZvbnQtc2l6ZTogMC44NzVyZW07XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIG1pbi1oZWlnaHQ6IDIuNWVtO1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA3NjhweCkge1xuICAuZGVtby1hdXRvY29tcGxldGUge1xuICAgIGdhcDogMXJlbTtcbiAgfVxuXG4gIC5kZW1vLWJsb2NrIHtcbiAgICB3aWR0aDogMTAwJTtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/autocomplete/autocomplete.vue)_

vue

```
<template>
  <div class="demo-autocomplete">
    <div class="demo-block">
      <div class="demo-title">list suggestions when activated</div>
      <el-autocomplete
        v-model="state1"
        :fetch-suggestions="querySearch"
        clearable
        class="w-50"
        placeholder="Please Input"
        @select="handleSelect"
      />
    </div>
    <div class="demo-block">
      <div class="demo-title">list suggestions on input</div>
      <el-autocomplete
        v-model="state2"
        :fetch-suggestions="querySearch"
        :trigger-on-focus="false"
        clearable
        class="w-50"
        placeholder="Please Input"
        @select="handleSelect"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

interface RestaurantItem {
  value: string
  link: string
}

const state1 = ref('')
const state2 = ref('')

const restaurants = ref<RestaurantItem[]>([])
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? restaurants.value.filter(createFilter(queryString))
    : restaurants.value
  // call callback function to return suggestions
  cb(results)
}
const createFilter = (queryString: string) => {
  return (restaurant: RestaurantItem) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}
const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ]
}

const handleSelect = (item: Record<string, any>) => {
  console.log(item)
}

onMounted(() => {
  restaurants.value = loadAll()
})
</script>

<style scoped>
.demo-autocomplete {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.demo-block {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.demo-title {
  font-size: 0.875rem;
  color: var(--el-text-color-secondary);
  min-height: 2.5em;
  display: flex;
  align-items: center;
}

@media screen and (max-width: 768px) {
  .demo-autocomplete {
    gap: 1rem;
  }

  .demo-block {
    width: 100%;
  }
}
</style>
```

隐藏源代码

## 自定义模板 [​](#自定义模板)

自定义如何显示输入建议。

使用 `scoped slot` 自定义输入建议。 在这个范围中，你可以使用 `item` 键来访问当前输入建议对象。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYXV0b2NvbXBsZXRlXG4gICAgdi1tb2RlbD1cInN0YXRlXCJcbiAgICA6ZmV0Y2gtc3VnZ2VzdGlvbnM9XCJxdWVyeVNlYXJjaFwiXG4gICAgcG9wcGVyLWNsYXNzPVwibXktYXV0b2NvbXBsZXRlXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgQHNlbGVjdD1cImhhbmRsZVNlbGVjdFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI3N1ZmZpeD5cbiAgICAgIDxlbC1pY29uIGNsYXNzPVwiZWwtaW5wdXRfX2ljb25cIiBAY2xpY2s9XCJoYW5kbGVJY29uQ2xpY2tcIj5cbiAgICAgICAgPGVkaXQgLz5cbiAgICAgIDwvZWwtaWNvbj5cbiAgICA8L3RlbXBsYXRlPlxuICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cInsgaXRlbSB9XCI+XG4gICAgICA8ZGl2IGNsYXNzPVwidmFsdWVcIj57eyBpdGVtLnZhbHVlIH19PC9kaXY+XG4gICAgICA8c3BhbiBjbGFzcz1cImxpbmtcIj57eyBpdGVtLmxpbmsgfX08L3NwYW4+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1hdXRvY29tcGxldGU+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgb25Nb3VudGVkLCByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFZGl0IH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmludGVyZmFjZSBMaW5rSXRlbSB7XG4gIHZhbHVlOiBzdHJpbmdcbiAgbGluazogc3RyaW5nXG59XG5cbmNvbnN0IHN0YXRlID0gcmVmKCcnKVxuY29uc3QgbGlua3MgPSByZWY8TGlua0l0ZW1bXT4oW10pXG5cbmNvbnN0IHF1ZXJ5U2VhcmNoID0gKHF1ZXJ5U3RyaW5nOiBzdHJpbmcsIGNiKSA9PiB7XG4gIGNvbnN0IHJlc3VsdHMgPSBxdWVyeVN0cmluZ1xuICAgID8gbGlua3MudmFsdWUuZmlsdGVyKGNyZWF0ZUZpbHRlcihxdWVyeVN0cmluZykpXG4gICAgOiBsaW5rcy52YWx1ZVxuICAvLyBjYWxsIGNhbGxiYWNrIGZ1bmN0aW9uIHRvIHJldHVybiBzdWdnZXN0aW9uIG9iamVjdHNcbiAgY2IocmVzdWx0cylcbn1cbmNvbnN0IGNyZWF0ZUZpbHRlciA9IChxdWVyeVN0cmluZzogc3RyaW5nKSA9PiB7XG4gIHJldHVybiAocmVzdGF1cmFudDogTGlua0l0ZW0pID0+IHtcbiAgICByZXR1cm4gKFxuICAgICAgcmVzdGF1cmFudC52YWx1ZS50b0xvd2VyQ2FzZSgpLmluZGV4T2YocXVlcnlTdHJpbmcudG9Mb3dlckNhc2UoKSkgPT09IDBcbiAgICApXG4gIH1cbn1cbmNvbnN0IGxvYWRBbGwgPSAoKSA9PiB7XG4gIHJldHVybiBbXG4gICAgeyB2YWx1ZTogJ3Z1ZScsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vdnVlanMvdnVlJyB9LFxuICAgIHsgdmFsdWU6ICdlbGVtZW50JywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS9FbGVtZUZFL2VsZW1lbnQnIH0sXG4gICAgeyB2YWx1ZTogJ2Nvb2tpbmcnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL0VsZW1lRkUvY29va2luZycgfSxcbiAgICB7IHZhbHVlOiAnbWludC11aScsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vRWxlbWVGRS9taW50LXVpJyB9LFxuICAgIHsgdmFsdWU6ICd2dWV4JywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS92dWVqcy92dWV4JyB9LFxuICAgIHsgdmFsdWU6ICd2dWUtcm91dGVyJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS92dWVqcy92dWUtcm91dGVyJyB9LFxuICAgIHsgdmFsdWU6ICdiYWJlbCcsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vYmFiZWwvYmFiZWwnIH0sXG4gIF1cbn1cbmNvbnN0IGhhbmRsZVNlbGVjdCA9IChpdGVtOiBSZWNvcmQ8c3RyaW5nLCBhbnk+KSA9PiB7XG4gIGNvbnNvbGUubG9nKGl0ZW0pXG59XG5cbmNvbnN0IGhhbmRsZUljb25DbGljayA9IChldjogRXZlbnQpID0+IHtcbiAgY29uc29sZS5sb2coZXYpXG59XG5cbm9uTW91bnRlZCgoKSA9PiB7XG4gIGxpbmtzLnZhbHVlID0gbG9hZEFsbCgpXG59KVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5teS1hdXRvY29tcGxldGUgbGkge1xuICBsaW5lLWhlaWdodDogbm9ybWFsO1xuICBwYWRkaW5nOiA3cHg7XG59XG4ubXktYXV0b2NvbXBsZXRlIGxpIC5uYW1lIHtcbiAgdGV4dC1vdmVyZmxvdzogZWxsaXBzaXM7XG4gIG92ZXJmbG93OiBoaWRkZW47XG59XG4ubXktYXV0b2NvbXBsZXRlIGxpIC5hZGRyIHtcbiAgZm9udC1zaXplOiAxMnB4O1xuICBjb2xvcjogI2I0YjRiNDtcbn1cbi5teS1hdXRvY29tcGxldGUgbGkgLmhpZ2hsaWdodGVkIC5hZGRyIHtcbiAgY29sb3I6ICNkZGQ7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/autocomplete/autocomplete-template.vue)_

vue

```
<template>
  <el-autocomplete
    v-model="state"
    :fetch-suggestions="querySearch"
    popper-class="my-autocomplete"
    placeholder="Please input"
    @select="handleSelect"
  >
    <template #suffix>
      <el-icon class="el-input__icon" @click="handleIconClick">
        <edit />
      </el-icon>
    </template>
    <template #default="{ item }">
      <div class="value">{{ item.value }}</div>
      <span class="link">{{ item.link }}</span>
    </template>
  </el-autocomplete>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { Edit } from '@element-plus/icons-vue'

interface LinkItem {
  value: string
  link: string
}

const state = ref('')
const links = ref<LinkItem[]>([])

const querySearch = (queryString: string, cb) => {
  const results = queryString
    ? links.value.filter(createFilter(queryString))
    : links.value
  // call callback function to return suggestion objects
  cb(results)
}
const createFilter = (queryString: string) => {
  return (restaurant: LinkItem) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}
const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ]
}
const handleSelect = (item: Record<string, any>) => {
  console.log(item)
}

const handleIconClick = (ev: Event) => {
  console.log(ev)
}

onMounted(() => {
  links.value = loadAll()
})
</script>

<style>
.my-autocomplete li {
  line-height: normal;
  padding: 7px;
}
.my-autocomplete li .name {
  text-overflow: ellipsis;
  overflow: hidden;
}
.my-autocomplete li .addr {
  font-size: 12px;
  color: #b4b4b4;
}
.my-autocomplete li .highlighted .addr {
  color: #ddd;
}
</style>
```

隐藏源代码

## 远程搜索 [​](#远程搜索)

从服务端搜索数据。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYXV0b2NvbXBsZXRlXG4gICAgdi1tb2RlbD1cInN0YXRlXCJcbiAgICA6ZmV0Y2gtc3VnZ2VzdGlvbnM9XCJxdWVyeVNlYXJjaEFzeW5jXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgQHNlbGVjdD1cImhhbmRsZVNlbGVjdFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgb25Nb3VudGVkLCByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHN0YXRlID0gcmVmKCcnKVxuXG5pbnRlcmZhY2UgTGlua0l0ZW0ge1xuICB2YWx1ZTogc3RyaW5nXG4gIGxpbms6IHN0cmluZ1xufVxuXG5jb25zdCBsaW5rcyA9IHJlZjxMaW5rSXRlbVtdPihbXSlcblxuY29uc3QgbG9hZEFsbCA9ICgpID0+IHtcbiAgcmV0dXJuIFtcbiAgICB7IHZhbHVlOiAndnVlJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS92dWVqcy92dWUnIH0sXG4gICAgeyB2YWx1ZTogJ2VsZW1lbnQnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL0VsZW1lRkUvZWxlbWVudCcgfSxcbiAgICB7IHZhbHVlOiAnY29va2luZycsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vRWxlbWVGRS9jb29raW5nJyB9LFxuICAgIHsgdmFsdWU6ICdtaW50LXVpJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS9FbGVtZUZFL21pbnQtdWknIH0sXG4gICAgeyB2YWx1ZTogJ3Z1ZXgnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL3Z1ZWpzL3Z1ZXgnIH0sXG4gICAgeyB2YWx1ZTogJ3Z1ZS1yb3V0ZXInLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL3Z1ZWpzL3Z1ZS1yb3V0ZXInIH0sXG4gICAgeyB2YWx1ZTogJ2JhYmVsJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS9iYWJlbC9iYWJlbCcgfSxcbiAgXVxufVxuXG5sZXQgdGltZW91dDogUmV0dXJuVHlwZTx0eXBlb2Ygc2V0VGltZW91dD5cbmNvbnN0IHF1ZXJ5U2VhcmNoQXN5bmMgPSAocXVlcnlTdHJpbmc6IHN0cmluZywgY2I6IChhcmc6IGFueSkgPT4gdm9pZCkgPT4ge1xuICBjb25zdCByZXN1bHRzID0gcXVlcnlTdHJpbmdcbiAgICA/IGxpbmtzLnZhbHVlLmZpbHRlcihjcmVhdGVGaWx0ZXIocXVlcnlTdHJpbmcpKVxuICAgIDogbGlua3MudmFsdWVcblxuICBjbGVhclRpbWVvdXQodGltZW91dClcbiAgdGltZW91dCA9IHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNiKHJlc3VsdHMpXG4gIH0sIDMwMDAgKiBNYXRoLnJhbmRvbSgpKVxufVxuY29uc3QgY3JlYXRlRmlsdGVyID0gKHF1ZXJ5U3RyaW5nOiBzdHJpbmcpID0+IHtcbiAgcmV0dXJuIChyZXN0YXVyYW50OiBMaW5rSXRlbSkgPT4ge1xuICAgIHJldHVybiAoXG4gICAgICByZXN0YXVyYW50LnZhbHVlLnRvTG93ZXJDYXNlKCkuaW5kZXhPZihxdWVyeVN0cmluZy50b0xvd2VyQ2FzZSgpKSA9PT0gMFxuICAgIClcbiAgfVxufVxuXG5jb25zdCBoYW5kbGVTZWxlY3QgPSAoaXRlbTogUmVjb3JkPHN0cmluZywgYW55PikgPT4ge1xuICBjb25zb2xlLmxvZyhpdGVtKVxufVxuXG5vbk1vdW50ZWQoKCkgPT4ge1xuICBsaW5rcy52YWx1ZSA9IGxvYWRBbGwoKVxufSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/autocomplete/remote-search.vue)_

vue

```
<template>
  <el-autocomplete
    v-model="state"
    :fetch-suggestions="querySearchAsync"
    placeholder="Please input"
    @select="handleSelect"
  />
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

const state = ref('')

interface LinkItem {
  value: string
  link: string
}

const links = ref<LinkItem[]>([])

const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ]
}

let timeout: ReturnType<typeof setTimeout>
const querySearchAsync = (queryString: string, cb: (arg: any) => void) => {
  const results = queryString
    ? links.value.filter(createFilter(queryString))
    : links.value

  clearTimeout(timeout)
  timeout = setTimeout(() => {
    cb(results)
  }, 3000 * Math.random())
}
const createFilter = (queryString: string) => {
  return (restaurant: LinkItem) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}

const handleSelect = (item: Record<string, any>) => {
  console.log(item)
}

onMounted(() => {
  links.value = loadAll()
})
</script>
```

隐藏源代码

## 自定义加载 2.5.0 [​](#自定义加载)

修改加载区域内容

loading icon1

loading icon2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1hdXRvY29tcGxldGVcIj5cbiAgICA8ZGl2IGNsYXNzPVwiZGVtby1ibG9ja1wiPlxuICAgICAgPGRpdiBjbGFzcz1cImRlbW8tdGl0bGVcIj5sb2FkaW5nIGljb24xPC9kaXY+XG4gICAgICA8ZWwtYXV0b2NvbXBsZXRlXG4gICAgICAgIHYtbW9kZWw9XCJzdGF0ZVwiXG4gICAgICAgIDpmZXRjaC1zdWdnZXN0aW9ucz1cInF1ZXJ5U2VhcmNoQXN5bmNcIlxuICAgICAgICBjbGFzcz1cInctNTBcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgICAgIEBzZWxlY3Q9XCJoYW5kbGVTZWxlY3RcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI2xvYWRpbmc+XG4gICAgICAgICAgPHN2ZyBjbGFzcz1cImNpcmN1bGFyXCIgdmlld0JveD1cIjAgMCA1MCA1MFwiPlxuICAgICAgICAgICAgPGNpcmNsZSBjbGFzcz1cInBhdGhcIiBjeD1cIjI1XCIgY3k9XCIyNVwiIHI9XCIyMFwiIGZpbGw9XCJub25lXCIgLz5cbiAgICAgICAgICA8L3N2Zz5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtYXV0b2NvbXBsZXRlPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJkZW1vLWJsb2NrXCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZGVtby10aXRsZVwiPmxvYWRpbmcgaWNvbjI8L2Rpdj5cbiAgICAgIDxlbC1hdXRvY29tcGxldGVcbiAgICAgICAgdi1tb2RlbD1cInN0YXRlXCJcbiAgICAgICAgOmZldGNoLXN1Z2dlc3Rpb25zPVwicXVlcnlTZWFyY2hBc3luY1wiXG4gICAgICAgIGNsYXNzPVwidy01MFwiXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICAgICAgQHNlbGVjdD1cImhhbmRsZVNlbGVjdFwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjbG9hZGluZz5cbiAgICAgICAgICA8ZWwtaWNvbiBjbGFzcz1cImlzLWxvYWRpbmdcIj5cbiAgICAgICAgICAgIDxzdmcgY2xhc3M9XCJjaXJjdWxhclwiIHZpZXdCb3g9XCIwIDAgMjAgMjBcIj5cbiAgICAgICAgICAgICAgPGdcbiAgICAgICAgICAgICAgICBjbGFzcz1cInBhdGgyIGxvYWRpbmctcGF0aFwiXG4gICAgICAgICAgICAgICAgc3Ryb2tlLXdpZHRoPVwiMFwiXG4gICAgICAgICAgICAgICAgc3R5bGU9XCJhbmltYXRpb246IG5vbmU7IHN0cm9rZTogbm9uZVwiXG4gICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICA8Y2lyY2xlIHI9XCIzLjM3NVwiIGNsYXNzPVwiZG90MVwiIHJ4PVwiMFwiIHJ5PVwiMFwiIC8+XG4gICAgICAgICAgICAgICAgPGNpcmNsZSByPVwiMy4zNzVcIiBjbGFzcz1cImRvdDJcIiByeD1cIjBcIiByeT1cIjBcIiAvPlxuICAgICAgICAgICAgICAgIDxjaXJjbGUgcj1cIjMuMzc1XCIgY2xhc3M9XCJkb3Q0XCIgcng9XCIwXCIgcnk9XCIwXCIgLz5cbiAgICAgICAgICAgICAgICA8Y2lyY2xlIHI9XCIzLjM3NVwiIGNsYXNzPVwiZG90M1wiIHJ4PVwiMFwiIHJ5PVwiMFwiIC8+XG4gICAgICAgICAgICAgIDwvZz5cbiAgICAgICAgICAgIDwvc3ZnPlxuICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtYXV0b2NvbXBsZXRlPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBvbk1vdW50ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgc3RhdGUgPSByZWYoJycpXG5cbmludGVyZmFjZSBMaW5rSXRlbSB7XG4gIHZhbHVlOiBzdHJpbmdcbiAgbGluazogc3RyaW5nXG59XG5cbmNvbnN0IGxpbmtzID0gcmVmPExpbmtJdGVtW10+KFtdKVxuXG5jb25zdCBsb2FkQWxsID0gKCkgPT4ge1xuICByZXR1cm4gW1xuICAgIHsgdmFsdWU6ICd2dWUnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL3Z1ZWpzL3Z1ZScgfSxcbiAgICB7IHZhbHVlOiAnZWxlbWVudCcsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vRWxlbWVGRS9lbGVtZW50JyB9LFxuICAgIHsgdmFsdWU6ICdjb29raW5nJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS9FbGVtZUZFL2Nvb2tpbmcnIH0sXG4gICAgeyB2YWx1ZTogJ21pbnQtdWknLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL0VsZW1lRkUvbWludC11aScgfSxcbiAgICB7IHZhbHVlOiAndnVleCcsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vdnVlanMvdnVleCcgfSxcbiAgICB7IHZhbHVlOiAndnVlLXJvdXRlcicsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vdnVlanMvdnVlLXJvdXRlcicgfSxcbiAgICB7IHZhbHVlOiAnYmFiZWwnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL2JhYmVsL2JhYmVsJyB9LFxuICBdXG59XG5cbmxldCB0aW1lb3V0OiBSZXR1cm5UeXBlPHR5cGVvZiBzZXRUaW1lb3V0PlxuY29uc3QgcXVlcnlTZWFyY2hBc3luYyA9IChxdWVyeVN0cmluZzogc3RyaW5nLCBjYjogKGFyZzogYW55KSA9PiB2b2lkKSA9PiB7XG4gIGNvbnN0IHJlc3VsdHMgPSBxdWVyeVN0cmluZ1xuICAgID8gbGlua3MudmFsdWUuZmlsdGVyKGNyZWF0ZUZpbHRlcihxdWVyeVN0cmluZykpXG4gICAgOiBsaW5rcy52YWx1ZVxuXG4gIGNsZWFyVGltZW91dCh0aW1lb3V0KVxuICB0aW1lb3V0ID0gc2V0VGltZW91dCgoKSA9PiB7XG4gICAgY2IocmVzdWx0cylcbiAgfSwgNTAwMCAqIE1hdGgucmFuZG9tKCkpXG59XG5jb25zdCBjcmVhdGVGaWx0ZXIgPSAocXVlcnlTdHJpbmc6IHN0cmluZykgPT4ge1xuICByZXR1cm4gKHJlc3RhdXJhbnQ6IExpbmtJdGVtKSA9PiB7XG4gICAgcmV0dXJuIChcbiAgICAgIHJlc3RhdXJhbnQudmFsdWUudG9Mb3dlckNhc2UoKS5pbmRleE9mKHF1ZXJ5U3RyaW5nLnRvTG93ZXJDYXNlKCkpID09PSAwXG4gICAgKVxuICB9XG59XG5cbmNvbnN0IGhhbmRsZVNlbGVjdCA9IChpdGVtOiBSZWNvcmQ8c3RyaW5nLCBhbnk+KSA9PiB7XG4gIGNvbnNvbGUubG9nKGl0ZW0pXG59XG5cbm9uTW91bnRlZCgoKSA9PiB7XG4gIGxpbmtzLnZhbHVlID0gbG9hZEFsbCgpXG59KVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1hdXRvY29tcGxldGUge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LXdyYXA6IHdyYXA7XG4gIGdhcDogMnJlbTtcbn1cblxuLmRlbW8tYmxvY2sge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBnYXA6IDAuNXJlbTtcbn1cblxuLmRlbW8tdGl0bGUge1xuICBmb250LXNpemU6IDAuODc1cmVtO1xuICBjb2xvcjogdmFyKC0tZWwtdGV4dC1jb2xvci1zZWNvbmRhcnkpO1xuICBtaW4taGVpZ2h0OiAyLjVlbTtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cblxuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogNzY4cHgpIHtcbiAgLmRlbW8tYXV0b2NvbXBsZXRlIHtcbiAgICBnYXA6IDFyZW07XG4gIH1cbiAgLmRlbW8tYmxvY2sge1xuICAgIHdpZHRoOiAxMDAlO1xuICB9XG59XG48L3N0eWxlPlxuXG48c3R5bGU+XG4uY2lyY3VsYXIge1xuICBkaXNwbGF5OiBpbmxpbmU7XG4gIGhlaWdodDogMzBweDtcbiAgd2lkdGg6IDMwcHg7XG4gIGFuaW1hdGlvbjogbG9hZGluZy1yb3RhdGUgMnMgbGluZWFyIGluZmluaXRlO1xufVxuLnBhdGgge1xuICBhbmltYXRpb246IGxvYWRpbmctZGFzaCAxLjVzIGVhc2UtaW4tb3V0IGluZmluaXRlO1xuICBzdHJva2UtZGFzaGFycmF5OiA5MCwgMTUwO1xuICBzdHJva2UtZGFzaG9mZnNldDogMDtcbiAgc3Ryb2tlLXdpZHRoOiAyO1xuICBzdHJva2U6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICBzdHJva2UtbGluZWNhcDogcm91bmQ7XG59XG4ubG9hZGluZy1wYXRoIC5kb3QxIHtcbiAgdHJhbnNmb3JtOiB0cmFuc2xhdGUoMy43NXB4LCAzLjc1cHgpO1xuICBmaWxsOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgYW5pbWF0aW9uOiBjdXN0b20tc3Bpbi1tb3ZlIDFzIGluZmluaXRlIGxpbmVhciBhbHRlcm5hdGU7XG4gIG9wYWNpdHk6IDAuMztcbn1cbi5sb2FkaW5nLXBhdGggLmRvdDIge1xuICB0cmFuc2Zvcm06IHRyYW5zbGF0ZShjYWxjKDEwMCUgLSAzLjc1cHgpLCAzLjc1cHgpO1xuICBmaWxsOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgYW5pbWF0aW9uOiBjdXN0b20tc3Bpbi1tb3ZlIDFzIGluZmluaXRlIGxpbmVhciBhbHRlcm5hdGU7XG4gIG9wYWNpdHk6IDAuMztcbiAgYW5pbWF0aW9uLWRlbGF5OiAwLjRzO1xufVxuLmxvYWRpbmctcGF0aCAuZG90MyB7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlKDMuNzVweCwgY2FsYygxMDAlIC0gMy43NXB4KSk7XG4gIGZpbGw6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICBhbmltYXRpb246IGN1c3RvbS1zcGluLW1vdmUgMXMgaW5maW5pdGUgbGluZWFyIGFsdGVybmF0ZTtcbiAgb3BhY2l0eTogMC4zO1xuICBhbmltYXRpb24tZGVsYXk6IDEuMnM7XG59XG4ubG9hZGluZy1wYXRoIC5kb3Q0IHtcbiAgdHJhbnNmb3JtOiB0cmFuc2xhdGUoY2FsYygxMDAlIC0gMy43NXB4KSwgY2FsYygxMDAlIC0gMy43NXB4KSk7XG4gIGZpbGw6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICBhbmltYXRpb246IGN1c3RvbS1zcGluLW1vdmUgMXMgaW5maW5pdGUgbGluZWFyIGFsdGVybmF0ZTtcbiAgb3BhY2l0eTogMC4zO1xuICBhbmltYXRpb24tZGVsYXk6IDAuOHM7XG59XG5Aa2V5ZnJhbWVzIGxvYWRpbmctcm90YXRlIHtcbiAgdG8ge1xuICAgIHRyYW5zZm9ybTogcm90YXRlKDM2MGRlZyk7XG4gIH1cbn1cbkBrZXlmcmFtZXMgbG9hZGluZy1kYXNoIHtcbiAgMCUge1xuICAgIHN0cm9rZS1kYXNoYXJyYXk6IDEsIDIwMDtcbiAgICBzdHJva2UtZGFzaG9mZnNldDogMDtcbiAgfVxuICA1MCUge1xuICAgIHN0cm9rZS1kYXNoYXJyYXk6IDkwLCAxNTA7XG4gICAgc3Ryb2tlLWRhc2hvZmZzZXQ6IC00MHB4O1xuICB9XG4gIDEwMCUge1xuICAgIHN0cm9rZS1kYXNoYXJyYXk6IDkwLCAxNTA7XG4gICAgc3Ryb2tlLWRhc2hvZmZzZXQ6IC0xMjBweDtcbiAgfVxufVxuQGtleWZyYW1lcyBjdXN0b20tc3Bpbi1tb3ZlIHtcbiAgdG8ge1xuICAgIG9wYWNpdHk6IDE7XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/autocomplete/custom-loading.vue)_

vue

```
<template>
  <div class="demo-autocomplete">
    <div class="demo-block">
      <div class="demo-title">loading icon1</div>
      <el-autocomplete
        v-model="state"
        :fetch-suggestions="querySearchAsync"
        class="w-50"
        placeholder="Please input"
        @select="handleSelect"
      >
        <template #loading>
          <svg class="circular" viewBox="0 0 50 50">
            <circle class="path" cx="25" cy="25" r="20" fill="none" />
          </svg>
        </template>
      </el-autocomplete>
    </div>
    <div class="demo-block">
      <div class="demo-title">loading icon2</div>
      <el-autocomplete
        v-model="state"
        :fetch-suggestions="querySearchAsync"
        class="w-50"
        placeholder="Please input"
        @select="handleSelect"
      >
        <template #loading>
          <el-icon class="is-loading">
            <svg class="circular" viewBox="0 0 20 20">
              <g
                class="path2 loading-path"
                stroke-width="0"
                style="animation: none; stroke: none"
              >
                <circle r="3.375" class="dot1" rx="0" ry="0" />
                <circle r="3.375" class="dot2" rx="0" ry="0" />
                <circle r="3.375" class="dot4" rx="0" ry="0" />
                <circle r="3.375" class="dot3" rx="0" ry="0" />
              </g>
            </svg>
          </el-icon>
        </template>
      </el-autocomplete>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

const state = ref('')

interface LinkItem {
  value: string
  link: string
}

const links = ref<LinkItem[]>([])

const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ]
}

let timeout: ReturnType<typeof setTimeout>
const querySearchAsync = (queryString: string, cb: (arg: any) => void) => {
  const results = queryString
    ? links.value.filter(createFilter(queryString))
    : links.value

  clearTimeout(timeout)
  timeout = setTimeout(() => {
    cb(results)
  }, 5000 * Math.random())
}
const createFilter = (queryString: string) => {
  return (restaurant: LinkItem) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}

const handleSelect = (item: Record<string, any>) => {
  console.log(item)
}

onMounted(() => {
  links.value = loadAll()
})
</script>

<style scoped>
.demo-autocomplete {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.demo-block {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.demo-title {
  font-size: 0.875rem;
  color: var(--el-text-color-secondary);
  min-height: 2.5em;
  display: flex;
  align-items: center;
}

@media screen and (max-width: 768px) {
  .demo-autocomplete {
    gap: 1rem;
  }
  .demo-block {
    width: 100%;
  }
}
</style>

<style>
.circular {
  display: inline;
  height: 30px;
  width: 30px;
  animation: loading-rotate 2s linear infinite;
}
.path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-color-primary);
  stroke-linecap: round;
}
.loading-path .dot1 {
  transform: translate(3.75px, 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
}
.loading-path .dot2 {
  transform: translate(calc(100% - 3.75px), 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.4s;
}
.loading-path .dot3 {
  transform: translate(3.75px, calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 1.2s;
}
.loading-path .dot4 {
  transform: translate(calc(100% - 3.75px), calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.8s;
}
@keyframes loading-rotate {
  to {
    transform: rotate(360deg);
  }
}
@keyframes loading-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -40px;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -120px;
  }
}
@keyframes custom-spin-move {
  to {
    opacity: 1;
  }
}
</style>
```

隐藏源代码

## 自定义头部与底部 2.10.6 [​](#自定义头部与底部)

你可以通过插槽来自定义下拉菜单的头部和底部。

使用插槽自定义内容。

Custom header content

Custom footer content

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYXV0b2NvbXBsZXRlLWN1c3RvbS1oZWFkZXItZm9vdGVyXCI+XG4gICAgPGRpdj5cbiAgICAgIDxwPkN1c3RvbSBoZWFkZXIgY29udGVudDwvcD5cbiAgICAgIDxlbC1hdXRvY29tcGxldGVcbiAgICAgICAgdi1tb2RlbD1cImhlYWRlclNsb3RTdGF0ZVwiXG4gICAgICAgIDpmZXRjaC1zdWdnZXN0aW9ucz1cInF1ZXJ5U2VhcmNoQXN5bmNcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgICAgIEBzZWxlY3Q9XCJoYW5kbGVTZWxlY3RcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI2hlYWRlcj5oZWFkZXIgY29udGVudDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLWF1dG9jb21wbGV0ZT5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2PlxuICAgICAgPHA+Q3VzdG9tIGZvb3RlciBjb250ZW50PC9wPlxuICAgICAgPGVsLWF1dG9jb21wbGV0ZVxuICAgICAgICByZWY9XCJmb290ZXJBdXRvY29tcGxldGVSZWZcIlxuICAgICAgICB2LW1vZGVsPVwiZm9vdGVyU2xvdHN0YXRlXCJcbiAgICAgICAgOmZldGNoLXN1Z2dlc3Rpb25zPVwicXVlcnlTZWFyY2hBc3luY1wiXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICAgICAgQHNlbGVjdD1cImhhbmRsZVNlbGVjdFwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgICAgIDxlbC1idXR0b24gbGluayBzaXplPVwic21hbGxcIiBAY2xpY2s9XCJoYW5kbGVDbGVhclwiPiBDbGVhciA8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtYXV0b2NvbXBsZXRlPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBvbk1vdW50ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaGVhZGVyU2xvdFN0YXRlID0gcmVmKCcnKVxuY29uc3QgZm9vdGVyU2xvdHN0YXRlID0gcmVmKCcnKVxuXG5pbnRlcmZhY2UgTGlua0l0ZW0ge1xuICB2YWx1ZTogc3RyaW5nXG4gIGxpbms6IHN0cmluZ1xufVxuXG5jb25zdCBsaW5rcyA9IHJlZjxMaW5rSXRlbVtdPihbXSlcblxuY29uc3QgbG9hZEFsbCA9ICgpID0+IHtcbiAgcmV0dXJuIFtcbiAgICB7IHZhbHVlOiAndnVlJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS92dWVqcy92dWUnIH0sXG4gICAgeyB2YWx1ZTogJ2VsZW1lbnQnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL0VsZW1lRkUvZWxlbWVudCcgfSxcbiAgICB7IHZhbHVlOiAnY29va2luZycsIGxpbms6ICdodHRwczovL2dpdGh1Yi5jb20vRWxlbWVGRS9jb29raW5nJyB9LFxuICAgIHsgdmFsdWU6ICdtaW50LXVpJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS9FbGVtZUZFL21pbnQtdWknIH0sXG4gICAgeyB2YWx1ZTogJ3Z1ZXgnLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL3Z1ZWpzL3Z1ZXgnIH0sXG4gICAgeyB2YWx1ZTogJ3Z1ZS1yb3V0ZXInLCBsaW5rOiAnaHR0cHM6Ly9naXRodWIuY29tL3Z1ZWpzL3Z1ZS1yb3V0ZXInIH0sXG4gICAgeyB2YWx1ZTogJ2JhYmVsJywgbGluazogJ2h0dHBzOi8vZ2l0aHViLmNvbS9iYWJlbC9iYWJlbCcgfSxcbiAgXVxufVxuXG5sZXQgdGltZW91dDogUmV0dXJuVHlwZTx0eXBlb2Ygc2V0VGltZW91dD5cbmNvbnN0IHF1ZXJ5U2VhcmNoQXN5bmMgPSAocXVlcnlTdHJpbmc6IHN0cmluZywgY2I6IChhcmc6IGFueSkgPT4gdm9pZCkgPT4ge1xuICBjb25zdCByZXN1bHRzID0gcXVlcnlTdHJpbmdcbiAgICA/IGxpbmtzLnZhbHVlLmZpbHRlcihjcmVhdGVGaWx0ZXIocXVlcnlTdHJpbmcpKVxuICAgIDogbGlua3MudmFsdWVcblxuICBjbGVhclRpbWVvdXQodGltZW91dClcbiAgdGltZW91dCA9IHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNiKHJlc3VsdHMpXG4gIH0sIDMwMDAgKiBNYXRoLnJhbmRvbSgpKVxufVxuY29uc3QgY3JlYXRlRmlsdGVyID0gKHF1ZXJ5U3RyaW5nOiBzdHJpbmcpID0+IHtcbiAgcmV0dXJuIChyZXN0YXVyYW50OiBMaW5rSXRlbSkgPT4ge1xuICAgIHJldHVybiAoXG4gICAgICByZXN0YXVyYW50LnZhbHVlLnRvTG93ZXJDYXNlKCkuaW5kZXhPZihxdWVyeVN0cmluZy50b0xvd2VyQ2FzZSgpKSA9PT0gMFxuICAgIClcbiAgfVxufVxuXG5jb25zdCBoYW5kbGVTZWxlY3QgPSAoaXRlbTogUmVjb3JkPHN0cmluZywgYW55PikgPT4ge1xuICBjb25zb2xlLmxvZyhpdGVtKVxufVxuXG5vbk1vdW50ZWQoKCkgPT4ge1xuICBsaW5rcy52YWx1ZSA9IGxvYWRBbGwoKVxufSlcblxuY29uc3QgZm9vdGVyQXV0b2NvbXBsZXRlUmVmID0gcmVmKClcbmNvbnN0IGhhbmRsZUNsZWFyID0gKCkgPT4ge1xuICBmb290ZXJTbG90c3RhdGUudmFsdWUgPSAnJ1xuICBmb290ZXJBdXRvY29tcGxldGVSZWYudmFsdWUuZ2V0RGF0YSgpXG59XG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5hdXRvY29tcGxldGUtY3VzdG9tLWhlYWRlci1mb290ZXIge1xuICBkaXNwbGF5OiBmbGV4O1xufVxuXG4uYXV0b2NvbXBsZXRlLWN1c3RvbS1oZWFkZXItZm9vdGVyID4gZGl2IHtcbiAgZmxleDogMTtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuLmF1dG9jb21wbGV0ZS1jdXN0b20taGVhZGVyLWZvb3RlciA+IGRpdiA+IDpkZWVwKC5lbC1hdXRvY29tcGxldGUpIHtcbiAgd2lkdGg6IDUwJTtcbn1cblxuLmF1dG9jb21wbGV0ZS1jdXN0b20taGVhZGVyLWZvb3RlciA+IGRpdjpub3QoOmxhc3QtY2hpbGQpIHtcbiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/autocomplete/custom-header-footer.vue)_

vue

```
<template>
  <div class="autocomplete-custom-header-footer">
    <div>
      <p>Custom header content</p>
      <el-autocomplete
        v-model="headerSlotState"
        :fetch-suggestions="querySearchAsync"
        placeholder="Please input"
        @select="handleSelect"
      >
        <template #header>header content</template>
      </el-autocomplete>
    </div>
    <div>
      <p>Custom footer content</p>
      <el-autocomplete
        ref="footerAutocompleteRef"
        v-model="footerSlotstate"
        :fetch-suggestions="querySearchAsync"
        placeholder="Please input"
        @select="handleSelect"
      >
        <template #footer>
          <el-button link size="small" @click="handleClear"> Clear </el-button>
        </template>
      </el-autocomplete>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

const headerSlotState = ref('')
const footerSlotstate = ref('')

interface LinkItem {
  value: string
  link: string
}

const links = ref<LinkItem[]>([])

const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ]
}

let timeout: ReturnType<typeof setTimeout>
const querySearchAsync = (queryString: string, cb: (arg: any) => void) => {
  const results = queryString
    ? links.value.filter(createFilter(queryString))
    : links.value

  clearTimeout(timeout)
  timeout = setTimeout(() => {
    cb(results)
  }, 3000 * Math.random())
}
const createFilter = (queryString: string) => {
  return (restaurant: LinkItem) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}

const handleSelect = (item: Record<string, any>) => {
  console.log(item)
}

onMounted(() => {
  links.value = loadAll()
})

const footerAutocompleteRef = ref()
const handleClear = () => {
  footerSlotstate.value = ''
  footerAutocompleteRef.value.getData()
}
</script>

<style scoped>
.autocomplete-custom-header-footer {
  display: flex;
}

.autocomplete-custom-header-footer > div {
  flex: 1;
  text-align: center;
}
.autocomplete-custom-header-footer > div > :deep(.el-autocomplete) {
  width: 50%;
}

.autocomplete-custom-header-footer > div:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
</style>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` | — |
| placeholder | 占位文本 | `string` | — |
| clearable | 是否可清空 | `boolean` | false |
| disabled | 自动补全组件是否被禁用 | `boolean` | false |
| value-key | 输入建议对象中用于显示的键名 | `string` | value |
| debounce | 获取输入建议的防抖延时，单位为毫秒 | `number` | 300 |
| placement | 菜单弹出位置 | `enum` | bottom-start |
| fetch-suggestions | 获取输入建议的方法， 仅当你的输入建议数据 resolve 时，通过调用 `callback(data:[])` 来返回它 | `array` / `Function` | — |
| trigger-on-focus | whether show suggestions when input focus | `boolean` | true |
| select-when-unmatched | 在输入没有任何匹配建议的情况下，按下回车是否触发 `select` 事件 | `boolean` | false |
| name | 等价于原生 input `name` 属性 | `string` | — |
| aria-label a11y 2.7.2 | 原生 `aria-label`属性 | `string` | — |
| hide-loading | 是否隐藏远程加载时的加载图标 | `boolean` | false |
| popper-class | 下拉列表的类名 | `string` / `object` | '' |
| popper-style 2.11.4 | autocomplete 下拉列表的类名 | `string` / `object` | — |
| popper-options 2.14.0 | [popper.js](https://popper.js.org/docs/v2/) parameters | `object`refer to [popper.js](https://popper.js.org/docs/v2/) doc | {} |
| show-after 2.14.0 | 下拉菜单的内容是否有箭头 | `boolean` | true |
| teleported | 是否将下拉列表元素插入 append-to 指向的元素下 | `boolean` | true |
| append-to 2.9.9 | 下拉框挂载到哪个 DOM 元素 | `CSSSelector` / `HTMLElement` | — |
| highlight-first-item | 是否默认高亮远程搜索结果的第一项 | `boolean` | false |
| fit-input-width | 下拉框的宽度是否与输入框相同 | `boolean` | false |
| popper-append-to-body deprecated | 是否将下拉列表插入至 body 元素。 在下拉列表的定位出现问题时，可将该属性设置为 false | `boolean` | false |
| loop-navigation 2.11.4 | 键盘导航是否从末尾循环到开头 | `boolean` | true |
| [input props](https://element-plus.org/zh-CN/component/input#attributes) | — | — | — |

### Events [​](#events)

| 事件名 | 详情 | 类型 |
| --- | --- | --- |
| blur | 当选择器的输入框失去焦点时触发 | `Function` |
| focus | 当选择器的输入框获得焦点时触发 | `Function` |
| input | 在 Input 值改变时触发 | `Function` |
| clear | 在点击由 `clearable` 属性生成的清空按钮时触发 | `Function` |
| select | 点击选中建议项时触发 | `Function` |
| change | 在 Input 值改变时触发 | `Function` |

### Slots [​](#slots)

| 插槽名 | 描述说明 | 类型 |
| --- | --- | --- |
| default | 自定义输入建议的内容。 | `object` |
| header 2.10.6 | 下拉列表顶部的内容 | \- |
| footer 2.10.6 | 下拉列表底部的内容 | \- |
| prefix | 输入框头部内容 | \- |
| suffix | 输入框尾部内容 | \- |
| prepend | 输入框前置内容，在 prefix 之前 | \- |
| append | 输入框后置内容，在 suffix 之后 | \- |
| loading 2.5.0 | 修改加载区域内容 | \- |

### Exposes [​](#exposes)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| activated | 自动补全输入框是否被激活 | `object` |
| blur | 使 input 失去焦点 | `Function` |
| close | 折叠建议列表 | `Function` |
| focus | 使 input 获取焦点 | `Function` |
| handleSelect | 手动触发选中建议事件 | `Function` |
| handleKeyEnter | 手动触发键盘回车事件 | `Function` |
| highlightedIndex | 当前高亮显示选项的索引 | `object` |
| highlight | 在建议中高亮显示一个项目 | `Function` |
| inputRef | el-input 组件实例 | `object` |
| loading | 远程获取提示内容的加载状态指示器 | `object` |
| popperRef | el-tooltip 组件实例 | `object` |
| suggestions | 获取自动补全结果 | `object` |
| getData 2.8.4 | 加载建议列表 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/autocomplete) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/autocomplete.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/autocomplete.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/24540820?v=4&size=64)](https://github.com/catanswer)[![](https://avatars.githubusercontent.com/u/78132554?v=4&size=64)](https://github.com/momei-LJM)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/32381310?v=4&size=64)](https://github.com/dormadekhin)[![](https://avatars.githubusercontent.com/u/7897937?v=4&size=64)](https://github.com/myronliu347)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/25103518?v=4&size=64)](https://github.com/richex-cn)[![](https://avatars.githubusercontent.com/u/22910740?v=4&size=64)](https://github.com/StephenKe)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/6063358?v=4&size=64)](https://github.com/xxholly32)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/36978416?v=4&size=64)](https://github.com/SimonaliaChen)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/66454152?v=4&size=64)](https://github.com/bryqiu)[![](https://avatars.githubusercontent.com/u/140705167?v=4&size=64)](https://github.com/zhongli-kira)[![](https://avatars.githubusercontent.com/u/65594411?v=4&size=64)](https://github.com/Heising)[![](https://avatars.githubusercontent.com/u/109908413?v=4&size=64)](https://github.com/sleepyShen1989)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/166272183?v=4&size=64)](https://github.com/voyagerFeng)[![](https://avatars.githubusercontent.com/u/40999116?v=4&size=64)](https://github.com/jasonren0403)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)

[Config Provider 全局配置](https://element-plus.org/zh-CN/component/config-provider)

[Cascader 级联选择器](https://element-plus.org/zh-CN/component/cascader)


