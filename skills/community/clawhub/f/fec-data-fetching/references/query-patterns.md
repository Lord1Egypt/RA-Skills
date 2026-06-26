# Server State 数据获取模式

## 先判断是否需要查询库

- 简单静态请求、一次性提交或已有框架 loader 足够表达的页面，不必默认引入查询库。
- 需要跨组件缓存、去重、后台刷新、分页、乐观更新、预取或 SSR hydration 时，再使用 TanStack Query、SWR、Nuxt 数据获取或项目既有请求缓存方案。
- 查询库只管理 server state，不替代本地 UI 状态、表单状态、权限判断或 Service Worker 缓存。

## 选型参考

先沿用仓库已有请求层和缓存方案；新增依赖时再按框架与复杂度选择。

| 场景 | 候选方案 | 注意点 |
| --- | --- | --- |
| React server state | TanStack Query / SWR / 项目既有封装 | TanStack Query 适合 mutation、invalidation 和无限查询；SWR 适合轻量读取缓存。 |
| Vue server state | TanStack Query Vue adapter / VueUse / Nuxt `useFetch` / 项目既有封装 | 不要让 Vue 项目照搬 React-only hook 示例。 |
| Solid / Svelte / 跨框架 | TanStack Query 对应 adapter 或项目既有资源层 | cache key、staleTime、mutation 回滚原则保持一致。 |
| 简单页面请求 | 框架 loader、组件内轻量请求或 API composable | 仍要处理 loading/error/empty 和取消或过期响应。 |
| SSR / SSG | 框架预取、水合或服务端数据边界 | 确保服务端 key 与客户端 key 一致，避免重复请求和水合错配。 |

## 通用边界

- API 函数只负责请求、解析和错误归一化，不包含 UI toast、loading 或缓存逻辑。
- cache key/query key 必须包含所有影响响应的参数。
- mutation 成功后按实体或列表失效；乐观更新必须先保存快照，失败时回滚。
- 无限查询只处理数据分页；DOM 虚拟化由列表虚拟化流程处理。
- 预取要有明确用户路径或首屏收益，不为所有可能数据提前请求。

## QueryClient 默认配置

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 30 * 60 * 1000,
      retry: 2,
      refetchOnWindowFocus: true,
    },
  },
});
```

## Query Key

- 推荐：`["users", "list", { page, status }]`
- 详情：`["users", "detail", userId]`
- 所有影响请求结果的参数都必须进入 key。

## 乐观更新

```tsx
const mutation = useMutation({
  mutationFn: () => api.likePost(postId),
  onMutate: async () => {
    await queryClient.cancelQueries({ queryKey: ["post", postId] });
    const previousPost = queryClient.getQueryData(["post", postId]);
    queryClient.setQueryData(["post", postId], (old: Post) => ({
      ...old,
      likes: old.likes + 1,
      liked: true,
    }));
    return { previousPost };
  },
  onError: (_error, _variables, context) => {
    queryClient.setQueryData(["post", postId], context?.previousPost);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ["post", postId] });
  },
});
```

## Infinite Query

```tsx
const feed = useInfiniteQuery({
  queryKey: ["feed"],
  queryFn: ({ pageParam = 1 }) => api.fetchFeed({ page: pageParam, limit: 20 }),
  getNextPageParam: (lastPage, pages) => (lastPage.hasMore ? pages.length + 1 : undefined),
  initialPageParam: 1,
});
```

虚拟列表场景将数据分页与 DOM 虚拟化分开设计。

## API 层整合

```ts
export async function getUserList(params: GetUserListParams): Promise<GetUserListResponse> {
  return request.get("/api/users", { params });
}

export function useUsers(params: GetUserListParams) {
  return useQuery({
    queryKey: ["users", "list", params],
    queryFn: () => getUserList(params),
    select: (response) => response.list,
  });
}
```

API 函数不包含 UI toast、loading 或缓存逻辑。
