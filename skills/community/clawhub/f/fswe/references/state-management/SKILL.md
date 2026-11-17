# State Management (Frontend)

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | string | en | en, id |
| depth | string | standard | quick, standard, deep |
| framework | string | vue3 | vue3, react |

## Checklist

### Pinia (Vue 3)
- [ ] Use Composition API style stores
- [ ] Keep stores small and focused (one concern each)
- [ ] Use getters for computed state
- [ ] Use actions for mutations (never mutate state directly)
- [ ] Use `storeToRefs()` for reactive destructuring
- [ ] Persist only what's needed (localStorage, not entire store)
- [ ] Avoid circular store dependencies

```typescript
// Pinia store template
export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const token = ref<string>('');

  const isAuthenticated = computed(() => !!user.value);

  async function login(credentials: LoginDTO) {
    const response = await api.login(credentials);
    user.value = response.user;
    token.value = response.token;
  }

  function logout() {
    user.value = null;
    token.value = '';
  }

  return { user, token, isAuthenticated, login, logout };
});
```

### Vuex → Pinia Migration
| Step | Action |
|------|--------|
| 1 | Install Pinia, remove Vuex |
| 2 | Convert each module to Pinia store |
| 3 | Replace `commit('mutation')` with `store.action()` |
| 4 | Replace `getters` with `computed` in setup function |
| 5 | Replace `mapState`/`mapGetters` with `storeToRefs()` |
| 6 | Remove `namespaced: true` (automatic in Pinia) |
| 7 | Test all store interactions |

### React State Patterns
| Pattern | When | Example |
|---------|------|---------|
| `useState` | Local component state | Form inputs, toggles |
| `useReducer` | Complex local state | Multi-step forms |
| `useContext` | Shared theme/auth | App-wide config |
| Zustand | Global client state | User session, cart |
| React Query | Server state | API data, caching |

### State Architecture
- [ ] Server state → React Query / SWR (not global store)
- [ ] UI state → Component local (`useState`)
- [ ] URL state → Router params/query
- [ ] Form state → React Hook Form / VeeValidate
- [ ] Global client state → Pinia / Zustand (sparingly)

### Performance
- [ ] Avoid unnecessary re-renders (memo, shallowRef)
- [ ] Use computed/watch for derived state
- [ ] Don't store derived data — compute it
- [ ] Lazy-load stores that aren't needed on mount
- [ ] Profile state updates with devtools

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Everything in global store | Split into local + server + global |
| Storing API data in Pinia | Use React Query / useAsyncData |
| Deep reactive objects | Use `shallowRef` for large objects |
| Circular store imports | Use dynamic imports |
| Mutating state in getters | Use actions for mutations |
