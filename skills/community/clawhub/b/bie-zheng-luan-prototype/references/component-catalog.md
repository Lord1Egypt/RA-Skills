# 前端组件目录参考

本文档提供前端组件的标准描述格式和常见组件模式，用于技术文档生成时的参考。

## 组件描述标准格式

### 1. 基础信息
```markdown
**组件名**: [组件名称]
**位置**: [在页面中的位置]
**功能**: [简要描述组件功能]
```

### 2. Props接口
```javascript
interface ComponentProps {
  // 数据相关
  data?: any;           // 组件显示的数据
  loading?: boolean;    // 加载状态
  
  // 交互回调
  onClick?: () => void;     // 点击事件
  onChange?: (value) => void; // 值变化事件
  onSubmit?: (data) => void; // 提交事件
  
  // 样式控制
  className?: string;   // 自定义样式类
  style?: React.CSSProperties; // 内联样式
  
  // 配置选项
  options?: any[];      // 下拉选项等配置
  disabled?: boolean;   // 是否禁用
  required?: boolean;   // 是否必填
  
  // 子内容
  children?: React.ReactNode;
}
```

### 3. 状态管理
```javascript
interface ComponentState {
  // 数据状态
  selectedItems: any[];     // 选中的项
  currentPage: number;      // 当前页码
  
  // UI状态
  isOpen: boolean;         // 是否展开/打开
  isLoading: boolean;      // 加载状态
  error: string | null;    // 错误信息
  
  // 表单状态
  formData: object;        // 表单数据
  validationErrors: object; // 验证错误
}
```

### 4. 交互逻辑
```markdown
- **初始化**: 组件挂载时执行的操作
- **用户交互**: 用户操作触发的行为
- **数据变化**: props变化时的响应
- **清理**: 组件卸载时的清理操作
```

## 常见组件模式

### 1. 数据展示组件

#### 表格组件 (DataTable)
```markdown
**组件名**: DataTable
**功能**: 展示结构化数据，支持排序、筛选、分页

**Props**:
- `columns`: Column[] - 列配置
- `dataSource`: any[] - 数据源
- `pagination`: Pagination - 分页配置
- `rowKey`: string - 行唯一键
- `onRowClick`: (record) => void - 行点击事件

**交互逻辑**:
1. 表头点击切换排序
2. 筛选器输入实时过滤
3. 分页器切换页面
4. 行选择/取消选择
```

#### 卡片组件 (Card)
```markdown
**组件名**: Card
**功能**: 信息卡片容器，支持标题、内容、操作区

**Props**:
- `title`: string | ReactNode - 卡片标题
- `extra`: ReactNode - 额外内容（通常为操作按钮）
- `cover`: ReactNode - 封面图片
- `actions`: ReactNode[] - 底部操作按钮

**样式特点**:
- 阴影效果增强层次感
- 圆角边框
- 悬停效果（可选）
```

### 2. 表单组件

#### 输入框 (Input)
```markdown
**组件名**: Input
**功能**: 文本输入控件

**Props**:
- `type`: 'text' | 'password' | 'email' | 'number' - 输入类型
- `placeholder`: string - 占位文本
- `value`: string - 当前值
- `onChange`: (e) => void - 值变化事件
- `prefix`: ReactNode - 前缀图标
- `suffix`: ReactNode - 后缀图标
- `allowClear`: boolean - 是否显示清除按钮

**验证规则**:
- 必填验证
- 格式验证（邮箱、手机号等）
- 长度限制
```

#### 下拉选择 (Select)
```markdown
**组件名**: Select
**功能**: 下拉选择控件

**Props**:
- `options`: Option[] - 选项列表
- `value`: string | string[] - 当前值
- `onChange`: (value) => void - 值变化事件
- `mode`: 'single' | 'multiple' - 单选/多选模式
- `placeholder`: string - 占位文本
- `loading`: boolean - 加载状态

**交互逻辑**:
1. 点击触发下拉菜单
2. 搜索框输入过滤选项
3. 选项点击选中
4. 多选模式下标签展示
```

### 3. 布局组件

#### 栅格布局 (Grid)
```markdown
**组件名**: Grid
**功能**: 响应式栅格布局系统

**Props**:
- `cols`: number - 列数（默认24）
- `gutter`: number | [number, number] - 栅格间距
- `span`: number - 栅格占位格数
- `offset`: number - 栅格左侧偏移格数

**响应式规则**:
- xs (<576px): 1-4列
- sm (≥576px): 1-8列  
- md (≥768px): 1-12列
- lg (≥992px): 1-16列
- xl (≥1200px): 1-24列
```

#### 布局容器 (Layout)
```markdown
**组件名**: Layout
**功能**: 页面整体布局容器

**结构**:
- `Header`: 顶部导航
- `Sider`: 侧边栏
- `Content`: 主内容区
- `Footer`: 底部区域

**Props**:
- `collapsed`: boolean - 侧边栏是否折叠
- `collapsedWidth`: number - 折叠时宽度
- `width`: number - 侧边栏宽度
```

### 4. 反馈组件

#### 模态框 (Modal)
```markdown
**组件名**: Modal
**功能**: 模态对话框

**Props**:
- `visible`: boolean - 是否显示
- `title`: string | ReactNode - 标题
- `onOk`: () => void - 确定按钮点击
- `onCancel`: () => void - 取消按钮点击
- `footer`: ReactNode - 自定义底部
- `maskClosable`: boolean - 点击遮罩是否关闭

**交互逻辑**:
1. 打开时禁止背景滚动
2. 键盘ESC键关闭
3. 确定按钮提交表单
4. 关闭时执行清理
```

#### 消息提示 (Message)
```markdown
**组件名**: Message
**功能**: 全局消息提示

**方法**:
- `success(content, duration)`: 成功提示
- `error(content, duration)`: 错误提示
- `warning(content, duration)`: 警告提示
- `info(content, duration)`: 信息提示
- `loading(content, duration)`: 加载提示

**位置选项**:
- `top`: 顶部居中
- `topLeft`: 左上角
- `topRight`: 右上角
- `bottom`: 底部居中
- `bottomLeft`: 左下角
- `bottomRight`: 右下角
```

## 组件交互模式

### 1. 数据获取模式
```javascript
// 组件内数据获取
useEffect(() => {
  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await api.getData(params);
      setData(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };
  fetchData();
}, [params]);
```

### 2. 表单处理模式
```javascript
// 受控表单组件
const [formData, setFormData] = useState(initialData);

const handleChange = (field, value) => {
  setFormData(prev => ({
    ...prev,
    [field]: value
  }));
};

const handleSubmit = async () => {
  // 验证表单
  const errors = validateForm(formData);
  if (Object.keys(errors).length > 0) {
    setValidationErrors(errors);
    return;
  }
  
  // 提交数据
  await api.submit(formData);
};
```

### 3. 事件处理模式
```javascript
// 防抖处理
const handleSearch = useDebounce((keyword) => {
  searchApi(keyword);
}, 300);

// 节流处理  
const handleScroll = useThrottle(() => {
  checkScrollPosition();
}, 100);

// 事件委托
const handleListClick = (e) => {
  if (e.target.matches('.item')) {
    const id = e.target.dataset.id;
    selectItem(id);
  }
};
```

## 样式规范参考

### 1. 命名规范
- BEM命名法：`block__element--modifier`
- 示例：`user-card__avatar--large`

### 2. 颜色系统
```css
/* 主色调 */
--primary-color: #1890ff;
--primary-hover: #40a9ff;
--primary-active: #096dd9;

/* 功能色 */
--success-color: #52c41a;
--warning-color: #faad14;
--error-color: #f5222d;
--info-color: #1890ff;

/* 中性色 */
--text-color: rgba(0, 0, 0, 0.85);
--text-color-secondary: rgba(0, 0, 0, 0.45);
--border-color: #d9d9d9;
--background-color: #f0f2f5;
```

### 3. 间距系统
```css
/* 基于8px基数 */
--spacing-xs: 4px;    /* 0.25rem */
--spacing-sm: 8px;    /* 0.5rem */
--spacing-md: 16px;   /* 1rem */
--spacing-lg: 24px;   /* 1.5rem */
--spacing-xl: 32px;   /* 2rem */
```

### 4. 动画曲线
```css
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
```

## 性能优化提示

### 1. 减少重渲染
- 使用 `React.memo()` 包裹纯展示组件
- 使用 `useMemo()` 缓存计算结果
- 使用 `useCallback()` 缓存函数引用

### 2. 代码分割
```javascript
// 动态导入组件
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

// 使用时包裹Suspense
<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>
```

### 3. 图片优化
- 使用 WebP 格式（兼容性考虑提供回退）
- 实现懒加载
- 使用响应式图片（srcset）
- 预加载关键图片

## 可访问性要求

### 1. 键盘导航
- 所有交互元素支持键盘访问
- 合理的 Tab 顺序
- 快捷键支持

### 2. 屏幕阅读器
- 语义化 HTML 标签
- ARIA 属性正确使用
- 焦点管理合理

### 3. 颜色对比度
- 文本与背景对比度 ≥ 4.5:1
- 大文本对比度 ≥ 3:1
- 非文本元素对比度 ≥ 3:1

---

## 使用说明

在技术文档中描述组件时，应参考以下结构：

1. **组件基本信息**：名称、位置、功能
2. **Props接口**：所有可配置属性
3. **状态管理**：组件内部状态
4. **交互逻辑**：用户操作响应
5. **样式特点**：外观和动画
6. **性能考虑**：优化建议
7. **可访问性**：无障碍支持

确保描述准确、完整，便于大模型理解并生成对应代码。