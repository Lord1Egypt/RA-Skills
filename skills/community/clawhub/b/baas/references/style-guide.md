# 统一样式规范（高级版）

所有页面必须遵循此规范，确保视觉高级感和交互体验一致性。

---

## 一、Tailwind 配置

在每个页面的 `<head>` 中，Tailwind CDN 后添加统一配置：

```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#eff6ff',
                    100: '#dbeafe',
                    200: '#bfdbfe',
                    300: '#93c5fd',
                    400: '#60a5fa',
                    500: '#3b82f6',
                    600: '#2563eb',
                    700: '#1d4ed8',
                    800: '#1e40af',
                    900: '#1e3a8a',
                },
            },
            animation: {
                'fade-in': 'fadeIn 0.3s ease-out',
                'slide-up': 'slideUp 0.3s ease-out',
                'slide-down': 'slideDown 0.3s ease-out',
                'scale-in': 'scaleIn 0.2s ease-out',
                'spin-slow': 'spin 1.5s linear infinite',
                'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
                'bounce-soft': 'bounceSoft 0.5s ease-out',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideDown: {
                    '0%': { opacity: '0', transform: 'translateY(-20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                scaleIn: {
                    '0%': { opacity: '0', transform: 'scale(0.95)' },
                    '100%': { opacity: '1', transform: 'scale(1)' },
                },
                pulseSoft: {
                    '0%, 100%': { opacity: '1' },
                    '50%': { opacity: '0.7' },
                },
                bounceSoft: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-5px)' },
                },
            },
            boxShadow: {
                'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
                'soft-lg': '0 10px 40px -10px rgba(0, 0, 0, 0.1), 0 2px 10px -2px rgba(0, 0, 0, 0.04)',
                'inner-soft': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)',
                'glow': '0 0 20px rgba(59, 130, 246, 0.3)',
                'glow-lg': '0 0 40px rgba(59, 130, 246, 0.4)',
            },
            backdropBlur: {
                'xs': '2px',
            },
        }
    }
}
</script>
<style type="text/tailwindcss">
    /* 全局过渡效果 */
    @layer utilities {
        .transition-smooth {
            @apply transition-all duration-300 ease-out;
        }
        .transition-fast {
            @apply transition-all duration-150 ease-out;
        }
        /* 玻璃态效果 */
        .glass {
            @apply bg-white/80 backdrop-blur-md border border-white/20;
        }
        .glass-dark {
            @apply bg-gray-900/80 backdrop-blur-md border border-gray-700/50;
        }
        /* 渐变背景 */
        .gradient-primary {
            @apply bg-gradient-to-r from-primary-600 to-primary-500;
        }
        .gradient-subtle {
            @apply bg-gradient-to-br from-gray-50 to-gray-100;
        }
        /* 悬浮效果 */
        .hover-lift {
            @apply transition-smooth hover:-translate-y-1 hover:shadow-soft-lg;
        }
        .hover-glow {
            @apply transition-smooth hover:shadow-glow;
        }
        /* 点击效果 */
        .press-effect {
            @apply active:scale-[0.98] transition-fast;
        }
    }
</style>
```

---

## 二、页面布局

### 2.1 现代化基础结构

```html
<body class="bg-gradient-subtle min-h-screen">
    <!-- 顶部导航（玻璃态） -->
    <nav class="sticky top-0 z-50 glass border-b border-gray-200/50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center space-x-3">
                    <!-- Logo 带悬浮效果 -->
                    <div class="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center shadow-soft">
                        <span class="text-white font-bold text-sm">A</span>
                    </div>
                    <span class="text-xl font-semibold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                        应用名称
                    </span>
                </div>
                <div class="flex items-center space-x-2">
                    <!-- 导航项带悬浮效果 -->
                    <a href="#" class="px-4 py-2 rounded-lg text-gray-600 hover:text-primary-600 hover:bg-primary-50 transition-smooth">
                        首页
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <!-- 主内容区（带入场动画） -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        <!-- 页面内容 -->
    </main>
</body>
```

### 2.2 页面标题（带装饰）

```html
<div class="mb-8">
    <h1 class="text-3xl font-bold bg-gradient-to-r from-gray-900 via-gray-800 to-gray-600 bg-clip-text text-transparent">
        页面标题
    </h1>
    <p class="mt-2 text-gray-500">页面描述文字</p>
</div>
```

---

## 三、高级组件规范

### 3.1 按钮（带交互效果）

```html
<!-- 主要按钮（渐变+发光+点击效果） -->
<button class="gradient-primary text-white px-6 py-2.5 rounded-xl font-medium shadow-soft
    hover:shadow-glow hover:scale-[1.02] active:scale-[0.98]
    transition-smooth disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100">
    提交
</button>

<!-- 次要按钮（边框+填充效果） -->
<button class="bg-white text-gray-700 px-6 py-2.5 rounded-xl font-medium border-2 border-gray-200
    hover:border-primary-300 hover:text-primary-600 hover:bg-primary-50
    active:scale-[0.98] transition-smooth">
    取消
</button>

<!-- 幽灵按钮（透明+悬浮变色） -->
<button class="text-gray-600 px-4 py-2 rounded-lg font-medium
    hover:text-primary-600 hover:bg-primary-50
    active:bg-primary-100 transition-smooth">
    更多
</button>

<!-- 危险按钮 -->
<button class="bg-gradient-to-r from-red-600 to-red-500 text-white px-6 py-2.5 rounded-xl font-medium shadow-soft
    hover:shadow-[0_0_20px_rgba(239,68,68,0.3)] hover:scale-[1.02] active:scale-[0.98] transition-smooth">
    删除
</button>

<!-- 图标按钮（圆形+悬浮效果） -->
<button class="w-10 h-10 rounded-full flex items-center justify-center text-gray-500
    hover:bg-gray-100 hover:text-gray-700 active:scale-95 transition-smooth">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
    </svg>
</button>
```

### 3.2 表单（现代风格）

#### 输入框（带焦点动画）

```html
<div class="mb-5 group">
    <label class="block text-sm font-medium text-gray-700 mb-1.5 group-focus-within:text-primary-600 transition-colors">
        字段名称 <span class="text-red-500">*</span>
    </label>
    <div class="relative">
        <input type="text" required
            class="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-xl
                focus:border-primary-500 focus:ring-4 focus:ring-primary-100
                hover:border-gray-300 outline-none transition-smooth
                placeholder:text-gray-400"
            placeholder="请输入...">
        <!-- 可选：右侧图标 -->
        <div class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
            </svg>
        </div>
    </div>
    <!-- 可选：帮助文本 -->
    <p class="mt-1.5 text-xs text-gray-500">帮助说明文字</p>
</div>
```

#### 下拉选择

```html
<div class="relative">
    <select class="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-xl appearance-none
        focus:border-primary-500 focus:ring-4 focus:ring-primary-100
        hover:border-gray-300 outline-none transition-smooth cursor-pointer">
        <option value="">请选择</option>
        <option value="1">选项一</option>
    </select>
    <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
    </div>
</div>
```

#### 文本域

```html
<textarea rows="4"
    class="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-xl
        focus:border-primary-500 focus:ring-4 focus:ring-primary-100
        hover:border-gray-300 outline-none transition-smooth resize-none
        placeholder:text-gray-400"
    placeholder="请输入详细内容..."></textarea>
```

#### 复选框（自定义样式）

```html
<label class="flex items-center space-x-3 cursor-pointer group">
    <div class="relative">
        <input type="checkbox" class="peer sr-only">
        <div class="w-5 h-5 border-2 border-gray-300 rounded-md
            peer-checked:bg-primary-600 peer-checked:border-primary-600
            peer-focus:ring-4 peer-focus:ring-primary-100
            group-hover:border-gray-400 transition-smooth"></div>
        <svg class="absolute top-0.5 left-0.5 w-4 h-4 text-white opacity-0 peer-checked:opacity-100 transition-opacity"
            fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
        </svg>
    </div>
    <span class="text-gray-700 group-hover:text-gray-900 transition-colors">记住我</span>
</label>
```

#### 开关（Switch）

```html
<label class="relative inline-flex items-center cursor-pointer">
    <input type="checkbox" class="sr-only peer">
    <div class="w-11 h-6 bg-gray-200 rounded-full
        peer-checked:bg-primary-600 peer-focus:ring-4 peer-focus:ring-primary-100
        after:content-[''] after:absolute after:top-0.5 after:left-[2px]
        after:bg-white after:rounded-full after:h-5 after:w-5 after:shadow-soft
        after:transition-transform after:duration-300 peer-checked:after:translate-x-full
        transition-colors"></div>
    <span class="ml-3 text-gray-700">启用通知</span>
</label>
```

### 3.3 卡片（多层次阴影+悬浮效果）

```html
<!-- 基础卡片（悬浮上升） -->
<div class="bg-white rounded-2xl shadow-soft p-6 hover-lift cursor-pointer">
    <h3 class="text-lg font-semibold text-gray-900 mb-2">卡片标题</h3>
    <p class="text-gray-600">卡片内容描述</p>
</div>

<!-- 特色卡片（渐变边框） -->
<div class="relative group">
    <div class="absolute -inset-0.5 bg-gradient-to-r from-primary-600 to-purple-600 rounded-2xl opacity-0 group-hover:opacity-100 blur transition-opacity"></div>
    <div class="relative bg-white rounded-2xl p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">特色卡片</h3>
        <p class="text-gray-600">悬浮时显示渐变边框</p>
    </div>
</div>

<!-- 统计卡片 -->
<div class="bg-white rounded-2xl shadow-soft p-6 hover-lift">
    <div class="flex items-center justify-between">
        <div>
            <p class="text-sm text-gray-500 mb-1">总用户数</p>
            <p class="text-3xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
                12,345
            </p>
        </div>
        <div class="w-12 h-12 rounded-xl gradient-primary flex items-center justify-center shadow-soft">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
        </div>
    </div>
    <div class="mt-4 flex items-center text-sm">
        <span class="text-green-600 font-medium flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
            </svg>
            +12.5%
        </span>
        <span class="text-gray-400 ml-2">较上月</span>
    </div>
</div>
```

### 3.4 列表项（滑动效果）

```html
<div class="bg-white rounded-2xl shadow-soft overflow-hidden divide-y divide-gray-100">
    <!-- 列表项（左滑显示操作） -->
    <div class="group relative">
        <div class="p-4 flex items-center justify-between hover:bg-gray-50 transition-smooth cursor-pointer">
            <div class="flex items-center space-x-4">
                <div class="w-10 h-10 rounded-full gradient-primary flex items-center justify-center text-white font-medium shadow-soft">
                    J
                </div>
                <div>
                    <h4 class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors">John Doe</h4>
                    <p class="text-sm text-gray-500">john@example.com</p>
                </div>
            </div>
            <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-600 group-hover:translate-x-1 transition-all"
                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
        </div>
    </div>
</div>
```

### 3.5 表格（现代风格）

```html
<div class="bg-white rounded-2xl shadow-soft overflow-hidden">
    <table class="min-w-full">
        <thead>
            <tr class="bg-gradient-to-r from-gray-50 to-gray-100/50">
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">名称</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">状态</th>
                <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
            <tr class="hover:bg-primary-50/50 transition-colors group">
                <td class="px-6 py-4">
                    <div class="flex items-center">
                        <div class="w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center mr-3">
                            <span class="text-primary-600 font-medium text-sm">A</span>
                        </div>
                        <span class="font-medium text-gray-900">项目名称</span>
                    </div>
                </td>
                <td class="px-6 py-4">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
                        <span class="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5 animate-pulse"></span>
                        运行中
                    </span>
                </td>
                <td class="px-6 py-4 text-right">
                    <button class="text-gray-400 hover:text-primary-600 transition-colors p-1">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
                        </svg>
                    </button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### 3.6 徽章/状态标签

```html
<!-- 状态点+文字 -->
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
    <span class="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5 animate-pulse"></span>
    在线
</span>

<!-- 渐变徽章 -->
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-primary-500 to-purple-500 text-white shadow-soft">
    新功能
</span>

<!-- 边框徽章 -->
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border-2 border-primary-200 text-primary-600 bg-primary-50">
    进行中
</span>
```

### 3.7 模态框（带入场动画）

```html
<!-- 遮罩层 -->
<div id="modal" class="fixed inset-0 z-50 hidden">
    <!-- 背景遮罩（点击关闭） -->
    <div class="fixed inset-0 bg-black/50 backdrop-blur-sm animate-fade-in" onclick="closeModal()"></div>

    <!-- 模态框内容（缩放入场） -->
    <div class="fixed inset-0 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-soft-lg max-w-md w-full max-h-[90vh] overflow-hidden animate-scale-in">
            <!-- 头部 -->
            <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
                <h3 class="text-lg font-semibold text-gray-900">标题</h3>
                <button onclick="closeModal()"
                    class="w-8 h-8 rounded-full flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-smooth">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
            <!-- 内容 -->
            <div class="px-6 py-4 overflow-y-auto">
                <!-- 表单或内容 -->
            </div>
            <!-- 底部 -->
            <div class="px-6 py-4 border-t border-gray-100 flex justify-end space-x-3 bg-gray-50/50">
                <button onclick="closeModal()"
                    class="px-4 py-2 rounded-xl text-gray-700 hover:bg-gray-100 transition-smooth">
                    取消
                </button>
                <button class="gradient-primary text-white px-6 py-2 rounded-xl shadow-soft hover:shadow-glow transition-smooth">
                    确认
                </button>
            </div>
        </div>
    </div>
</div>

<script>
function openModal() {
    document.getElementById('modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}
function closeModal() {
    document.getElementById('modal').classList.add('hidden');
    document.body.style.overflow = '';
}
</script>
```

### 3.8 消息提示（Toast）

```html
<!-- Toast 容器 -->
<div id="toast-container" class="fixed top-4 right-4 z-50 space-y-3"></div>

<script>
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');

    const styles = {
        success: 'bg-green-50 border-green-200 text-green-800',
        error: 'bg-red-50 border-red-200 text-red-800',
        warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
        info: 'bg-blue-50 border-blue-200 text-blue-800'
    };

    const icons = {
        success: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>',
        error: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>',
        warning: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>',
        info: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>'
    };

    toast.className = `flex items-center px-4 py-3 rounded-xl border shadow-soft-lg animate-slide-down ${styles[type]}`;
    toast.innerHTML = `
        <svg class="w-5 h-5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            ${icons[type]}
        </svg>
        <span class="font-medium">${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
</script>
```

### 3.9 空状态（插画风格）

```html
<div class="text-center py-16 animate-fade-in">
    <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-100 to-primary-50 flex items-center justify-center">
        <svg class="w-12 h-12 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-2">暂无数据</h3>
    <p class="text-gray-500 mb-6 max-w-sm mx-auto">还没有任何记录，点击下方按钮创建第一条</p>
    <button class="gradient-primary text-white px-6 py-2.5 rounded-xl shadow-soft hover:shadow-glow hover:scale-[1.02] transition-smooth">
        <span class="flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            立即创建
        </span>
    </button>
</div>
```

### 3.10 加载状态

```html
<!-- 页面加载（全屏） -->
<div class="fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="flex flex-col items-center">
        <div class="w-12 h-12 rounded-full border-4 border-primary-200 border-t-primary-600 animate-spin"></div>
        <p class="mt-4 text-gray-600 font-medium">加载中...</p>
    </div>
</div>

<!-- 按钮加载态 -->
<button disabled class="gradient-primary text-white px-6 py-2.5 rounded-xl opacity-80 cursor-wait flex items-center">
    <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    处理中...
</button>

<!-- 骨架屏 -->
<div class="animate-pulse space-y-4">
    <div class="h-4 bg-gray-200 rounded-full w-3/4"></div>
    <div class="h-4 bg-gray-200 rounded-full w-1/2"></div>
    <div class="h-32 bg-gray-200 rounded-xl"></div>
</div>
```

### 3.11 图片上传（拖拽+预览）

```html
<div class="mb-5">
    <label class="block text-sm font-medium text-gray-700 mb-1.5">上传图片</label>
    <div id="dropZone"
        class="relative border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center
            hover:border-primary-400 hover:bg-primary-50/50 transition-smooth cursor-pointer
            group"
        onclick="document.getElementById('fileInput').click()"
        ondragover="event.preventDefault(); this.classList.add('border-primary-500', 'bg-primary-50')"
        ondragleave="this.classList.remove('border-primary-500', 'bg-primary-50')"
        ondrop="handleDrop(event)">

        <input type="file" id="fileInput" accept="image/*" class="hidden" onchange="handleUpload(this)">

        <div id="uploadPlaceholder" class="space-y-3">
            <div class="w-16 h-16 mx-auto rounded-full bg-gray-100 group-hover:bg-primary-100 flex items-center justify-center transition-colors">
                <svg class="w-8 h-8 text-gray-400 group-hover:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
            </div>
            <div>
                <p class="text-gray-700 font-medium">点击或拖拽上传</p>
                <p class="text-sm text-gray-500 mt-1">支持 JPG、PNG、GIF，最大 5MB</p>
            </div>
        </div>

        <div id="uploadPreview" class="hidden">
            <img id="previewImage" class="max-h-48 mx-auto rounded-xl shadow-soft">
            <button type="button" onclick="event.stopPropagation(); clearUpload()"
                class="mt-3 text-sm text-red-600 hover:text-red-700 font-medium">
                移除图片
            </button>
        </div>
    </div>
</div>

<script>
function handleUpload(input) {
    const file = input.files[0];
    if (file) showPreview(file);
}

function handleDrop(event) {
    event.preventDefault();
    event.target.classList.remove('border-primary-500', 'bg-primary-50');
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        document.getElementById('fileInput').files = event.dataTransfer.files;
        showPreview(file);
    }
}

function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('uploadPlaceholder').classList.add('hidden');
        document.getElementById('uploadPreview').classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

function clearUpload() {
    document.getElementById('fileInput').value = '';
    document.getElementById('uploadPlaceholder').classList.remove('hidden');
    document.getElementById('uploadPreview').classList.add('hidden');
}
</script>
```

---

## 四、交互反馈规范

### 4.1 点击反馈
所有可点击元素必须添加：
- `transition-smooth` 或 `transition-fast`
- `hover:` 状态变化（颜色、背景、阴影）
- `active:scale-[0.98]` 或 `active:scale-95` 点击缩放

### 4.2 加载状态
- 按钮提交时显示 loading spinner
- 列表加载时显示骨架屏
- 页面切换时显示全屏加载

### 4.3 操作反馈
- 成功操作：绿色 Toast
- 失败操作：红色 Toast
- 表单错误：输入框红色边框 + 错误提示

### 4.4 动画时机
| 场景 | 动画 | 时长 |
|------|------|------|
| 页面入场 | `animate-fade-in` | 0.3s |
| 模态框入场 | `animate-scale-in` | 0.2s |
| Toast 入场 | `animate-slide-down` | 0.3s |
| 列表项入场 | `animate-slide-up` | 0.3s |
| hover 效果 | `transition-smooth` | 0.3s |
| 点击反馈 | `transition-fast` | 0.15s |

---

## 五、响应式与间距

### 5.1 响应式网格

```html
<!-- 自适应卡片网格 -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    <!-- 卡片 -->
</div>
```

### 5.2 间距规范

| 用途 | 推荐值 |
|------|--------|
| 页面内边距 | `px-4 sm:px-6 lg:px-8` |
| 页面上下边距 | `py-8` |
| 区块间距 | `mb-8` |
| 卡片内边距 | `p-6` |
| 卡片圆角 | `rounded-2xl` |
| 表单字段间距 | `mb-5` |
| 按钮组间距 | `space-x-3` |

---

## 六、字体规范

| 用途 | 类名 |
|------|------|
| 页面大标题 | `text-3xl font-bold` + 渐变色 |
| 区块标题 | `text-lg font-semibold text-gray-900` |
| 卡片标题 | `text-base font-medium text-gray-900` |
| 正文 | `text-sm text-gray-600` |
| 辅助文字 | `text-xs text-gray-500` |
| 链接 | `text-primary-600 hover:text-primary-700 transition-colors` |

---

## 七、前端 DOM 渲染安全强制规则（必须遵守）

### 7.1 状态节点禁止放入可覆盖容器

加载态、空状态、错误态等状态节点（如 loadingState、emptyState、errorState）**禁止写在会被 `innerHTML`、`replaceChildren()`、`append()` 整体覆盖的列表容器内部**。

状态节点必须与列表容器保持**同级兄弟关系**，通过 `style.display` 或 `classList` 控制显示/隐藏。

❌ 错误（状态节点在列表容器内部，会被 innerHTML 覆盖）：
```html
<div id="leaderboardList">
    <div id="loadingState">加载中...</div>
    <div id="emptyState">暂无数据</div>
</div>
```

✅ 正确（状态节点与列表容器同级）：
```html
<div id="loadingState">加载中...</div>
<div id="leaderboardList"></div>
<div id="emptyState">暂无数据</div>
```

### 7.2 显示/隐藏控制示例

```javascript
// 加载中
loadingState.style.display = 'block';
leaderboardList.style.display = 'none';
emptyState.style.display = 'none';

// 有数据
loadingState.style.display = 'none';
leaderboardList.style.display = 'block';
leaderboardList.innerHTML = renderList(data); // 只影响列表容器内部
emptyState.style.display = 'none';

// 无数据
loadingState.style.display = 'none';
leaderboardList.style.display = 'none';
emptyState.style.display = 'block';
```

---

## 八、图片/资源字段处理强制规则（必须遵守）

### 8.1 数据结构规则

所有图片字段必须使用**资源数组格式**，禁止使用字符串格式。

✅ 正确（资源数组格式）：
```javascript
images = [{ url: "https://xxx.jpg" }]
avatar = [{ url: "https://xxx.jpg" }]
cover  = [{ url: "https://xxx.jpg" }]
```

❌ 错误（字符串格式，严禁使用）：
```javascript
image = "https://xxx.jpg"
avatar = "https://xxx.jpg"
```

### 8.2 上传规则

上传接口返回成功后，只提取图片 URL，保存到数据库时保持数组格式：

```javascript
// 单图上传 — 提取 URL
const imageUrl = result?.data?.url || '';

// 保存到数据库 — 数组格式
updateData.avatar = [{ url: imageUrl }];

// 多图上传
updateData.images = fileList.map(url => ({ url }));
```

### 8.3 读取显示规则

读取图片必须安全访问，img 标签必须提供默认占位图：

```javascript
// 安全读取
const imageUrl = data?.images?.[0]?.url || '';
const avatarUrl = user?.avatar?.[0]?.url || '';

// img 标签设置，必须带兜底占位图
img.src = imageUrl || 'https://via.placeholder.com/300';
```

### 8.4 编辑回显规则

打开编辑弹窗时，必须正确回显已上传的图片：

```javascript
previewUrl = currentData?.images?.[0]?.url || '';
```

### 8.5 删除和替换规则

- 替换图片时覆盖第一个元素：`avatar = [{ url: newUrl }]`
- 多图删除时按数组索引删除，**不允许破坏数组结构**

### 8.6 稳定性规则

- 所有 DOM 操作前必须判空
- 所有上传失败必须有 toast 提示
- 所有 `null` / `undefined` 必须兼容处理
- 禁止改变现有 UI 风格
- 禁止影响已有页面初始化流程
