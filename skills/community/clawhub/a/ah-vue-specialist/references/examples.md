# Vue Specialist — Code Examples

## Example 1

```vue
<template>
  <div class="user-profile">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else>
      <h1>{{ user?.name }}</h1>
      <button @click="updateProfile">Update</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, toRefs } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types'

// Props with TypeScript
interface Props {
  userId: string
  editable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  editable: false
})

// Emits with TypeScript
const emit = defineEmits<{
  update: [user: User]
  delete: [id: string]
}>()

// Reactive state
const loading = ref(false)
const error = ref<Error | null>(null)
const localUser = ref<User | null>(null)

// Store integration
const userStore = useUserStore()
const { currentUser } = storeToRefs(userStore)

// Computed properties
const isOwner = computed(() => 
  currentUser.value?.id === props.userId
)

const canEdit = computed(() => 
  props.editable && isOwner.value
)

// Watchers
watch(() => props.userId, async (newId) => {
  if (newId) {
    await fetchUser(newId)
  }
}, { immediate: true })

// Methods
async function fetchUser(id: string) {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`/api/users/${id}`)
    if (!response.ok) throw new Error('Failed to fetch user')
    
    localUser.value = await response.json()
  } catch (err) {
    error.value = err as Error
  } finally {
    loading.value = false
  }
}

async function updateProfile() {
  if (!localUser.value) return
  
  try {
    await userStore.updateUser(localUser.value)
    emit('update', localUser.value)
  } catch (err) {
    error.value = err as Error
  }
}

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted')
})

// Expose to template refs
defineExpose({
  refresh: () => fetchUser(props.userId)
})
</script>
```

## Example 2

```typescript
// composables/useApi.ts
import { ref, Ref, UnwrapRef } from 'vue'

interface UseApiOptions {
  immediate?: boolean
  onError?: (error: Error) => void
}

export function useApi<T>(
  url: string | Ref<string>,
  options: UseApiOptions = {}
) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  async function execute() {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(unref(url))
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      
      data.value = await response.json()
    } catch (err) {
      error.value = err as Error
      options.onError?.(err as Error)
    } finally {
      loading.value = false
    }
  }

  if (options.immediate) {
    execute()
  }

  return {
    data: readonly(data),
    error: readonly(error),
    loading: readonly(loading),
    execute
  }
}

// composables/useDebounce.ts
export function useDebounce<T>(value: Ref<T>, delay = 300) {
  const debouncedValue = ref<T>(value.value)
  let timeout: NodeJS.Timeout

  watchEffect(() => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      debouncedValue.value = value.value
    }, delay)
  })

  onUnmounted(() => clearTimeout(timeout))

  return debouncedValue
}

// composables/useInfiniteScroll.ts
export function useInfiniteScroll(
  callback: () => void | Promise<void>,
  options: { threshold?: number; root?: HTMLElement } = {}
) {
  const target = ref<HTMLElement>()
  const { threshold = 100 } = options

  function checkScroll() {
    if (!target.value) return
    
    const { scrollTop, scrollHeight, clientHeight } = 
      options.root || document.documentElement
    
    if (scrollTop + clientHeight >= scrollHeight - threshold) {
      callback()
    }
  }

  onMounted(() => {
    const element = options.root || window
    element.addEventListener('scroll', checkScroll)
  })

  onUnmounted(() => {
    const element = options.root || window
    element.removeEventListener('scroll', checkScroll)
  })

  return { target }
}
```

## Example 3

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { api } from '@/services/api'

interface UserState {
  users: User[]
  currentUser: User | null
  loading: boolean
  error: string | null
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    users: [],
    currentUser: null,
    loading: false,
    error: null
  }),

  getters: {
    getUserById: (state) => {
      return (id: string) => state.users.find(u => u.id === id)
    },
    
    isAuthenticated: (state) => !!state.currentUser,
    
    userCount: (state) => state.users.length,
    
    sortedUsers: (state) => {
      return [...state.users].sort((a, b) => 
        a.name.localeCompare(b.name)
      )
    }
  },

  actions: {
    async fetchUsers() {
      this.loading = true
      try {
        const users = await api.getUsers()
        this.users = users
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async login(credentials: LoginCredentials) {
      const user = await api.login(credentials)
      this.currentUser = user
      
      // Persist to localStorage
      localStorage.setItem('user', JSON.stringify(user))
      
      return user
    },

    logout() {
      this.currentUser = null
      localStorage.removeItem('user')
      
      // Reset other stores
      const cartStore = useCartStore()
      cartStore.$reset()
    },

    // Optimistic update pattern
    async updateUser(updates: Partial<User>) {
      const originalUser = this.currentUser
      
      // Optimistic update
      this.currentUser = { ...this.currentUser, ...updates }
      
      try {
        const updated = await api.updateUser(this.currentUser.id, updates)
        this.currentUser = updated
      } catch (error) {
        // Rollback on error
        this.currentUser = originalUser
        throw error
      }
    }
  },

  persist: {
    enabled: true,
    strategies: [
      {
        key: 'user',
        storage: localStorage,
        paths: ['currentUser']
      }
    ]
  }
})

// Setup store alternative syntax
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  
  function increment() {
    count.value++
  }
  
  return { count, doubleCount, increment }
})
```

## Example 4

```vue
<!-- pages/products/[id].vue -->
<template>
  <div>
    <ProductDetail :product="product" />
  </div>
</template>

<script setup>
// Auto-imported composables
const route = useRoute()
const { $api } = useNuxtApp()

// Data fetching with error handling
const { data: product, error } = await useFetch(
  `/api/products/${route.params.id}`,
  {
    transform: (data) => ({
      ...data,
      price: formatPrice(data.price)
    })
  }
)

if (error.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Product not found'
  })
}

// SEO metadata
useSeoMeta({
  title: product.value?.name,
  description: product.value?.description,
  ogImage: product.value?.image
})

// Server-only logic
if (process.server) {
  console.log('Running on server')
}
</script>

<!-- layouts/default.vue -->
<template>
  <div>
    <AppHeader />
    <main>
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<!-- composables/useAuth.ts -->
export const useAuth = () => {
  const user = useState<User | null>('auth.user', () => null)
  
  const login = async (credentials: LoginCredentials) => {
    const { data } = await $fetch('/api/auth/login', {
      method: 'POST',
      body: credentials
    })
    
    user.value = data.user
    await navigateTo('/dashboard')
  }
  
  const logout = async () => {
    await $fetch('/api/auth/logout', { method: 'POST' })
    user.value = null
    await navigateTo('/login')
  }
  
  return {
    user: readonly(user),
    login,
    logout,
    isAuthenticated: computed(() => !!user.value)
  }
}
```

## Example 5

```vue
<!-- Teleport for modals -->
<template>
  <button @click="showModal = true">Open Modal</button>
  
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click="showModal = false">
        <div class="modal-content" @click.stop>
          <slot />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<!-- Async components with Suspense -->
<template>
  <Suspense>
    <template #default>
      <AsyncDashboard />
    </template>
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<!-- Provide/Inject pattern -->
<script setup>
// Parent component
import { provide, ref } from 'vue'

const theme = ref('dark')
const toggleTheme = () => {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
}

provide('theme', {
  current: readonly(theme),
  toggle: toggleTheme
})

// Child component
import { inject } from 'vue'

const theme = inject<ThemeContext>('theme')
</script>

<!-- Dynamic components -->
<template>
  <component 
    :is="currentComponent" 
    v-bind="componentProps"
    @event="handleEvent"
  />
</template>

<script setup>
import { shallowRef } from 'vue'
import ComponentA from './ComponentA.vue'
import ComponentB from './ComponentB.vue'

const components = {
  a: ComponentA,
  b: ComponentB
}

const currentComponent = shallowRef(components.a)
</script>
```

## Example 6

```typescript
// Component testing
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import UserProfile from '@/components/UserProfile.vue'

describe('UserProfile', () => {
  it('renders user name', () => {
    const wrapper = mount(UserProfile, {
      props: {
        user: { id: '1', name: 'John Doe' }
      }
    })
    
    expect(wrapper.text()).toContain('John Doe')
  })
  
  it('emits update event', async () => {
    const wrapper = mount(UserProfile, {
      props: { user: { id: '1', name: 'John' } }
    })
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.emitted()).toHaveProperty('update')
    expect(wrapper.emitted('update')[0]).toEqual([
      { id: '1', name: 'John' }
    ])
  })
})

// Store testing
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '@/stores/user'

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })
  
  it('fetches users', async () => {
    const store = useUserStore()
    
    await store.fetchUsers()
    
    expect(store.users).toHaveLength(3)
    expect(store.loading).toBe(false)
  })
})
```
