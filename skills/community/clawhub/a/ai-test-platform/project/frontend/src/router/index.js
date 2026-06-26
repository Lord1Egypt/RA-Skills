import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue')
  },
  {
    path: '/test-cases',
    name: 'TestCases',
    component: () => import('@/pages/TestCases.vue')
  },
  {
    path: '/api-scripts',
    name: 'ApiScripts',
    component: () => import('@/pages/ApiScripts.vue')
  },
  {
    path: '/ui-scripts',
    name: 'UiScripts',
    component: () => import('@/pages/UiScripts.vue')
  },
  {
    path: '/execution',
    name: 'Execution',
    component: () => import('@/pages/Execution.vue')
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/pages/Reports.vue')
  },
  {
    path: '/system',
    name: 'System',
    component: () => import('@/pages/System.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authCode = localStorage.getItem('auth_code')

  // 如果访问登录页面，直接通过
  if (to.path === '/login') {
    next()
    return
  }

  // 如果没有授权码，跳转到登录页面
  if (!authCode) {
    next('/login')
    return
  }

  // 其他情况直接通过
  next()
})

export default router
