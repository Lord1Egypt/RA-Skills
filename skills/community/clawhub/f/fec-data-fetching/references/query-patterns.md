# Server State data acquisition mode

## First determine whether a query library is needed

- Simple static requests, one-time submissions, or pages with sufficient expression in the existing framework loader do not need to introduce the query library by default.
- When cross-component caching, deduplication, background refresh, paging, optimistic updates, prefetching or SSR hydration are required, use TanStack Query, SWR, Nuxt data acquisition or the project's existing request caching solution.
- The query library only manages server state and does not replace local UI state, form state, permission judgment or Service Worker cache.

## Selection reference

First, use the existing request layer and caching solution in the warehouse; when adding new dependencies, choose based on the framework and complexity.

| Scenarios | Alternative solutions | Notes |
| --- | --- | --- |
| React server state | TanStack Query / SWR / Project existing package | TanStack Query is suitable for mutation, invalidation and infinite queries; SWR is suitable for lightweight read caching. |
| Vue server state | TanStack Query Vue adapter / VueUse / Nuxt `useFetch` / Project existing package | Don’t let Vue projects copy React-only hook examples. |
| Solid / Svelte / Cross-framework | TanStack Query corresponds to the existing resource layer of the adapter or project | The cache key, staleTime, and mutation rollback principles are consistent. |
| Simple page requests | Framework loaders, lightweight requests within components, or API composable | Still have to handle loading/error/empty and cancellation or expiration responses. |
| SSR / SSG | Framework prefetching, hydration or server-side data boundaries | Ensure that the server key is consistent with the client key to avoid repeated requests and hydration mismatches. |

## Universal Boundary

- API functions are only responsible for requesting, parsing and error normalization, and do not include UI toast, loading or caching logic.
- The cache key/query key must contain all parameters that affect the response.
- Mutation fails by entity or list after success; optimistic update must save the snapshot first and roll back when it fails.
- Infinite queries only handle data paging; DOM virtualization is handled by the list virtualization process.
- Prefetching must have a clear user path or above-the-fold revenue, and do not request all possible data in advance.

## QueryClient default configuration

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

- Recommended: `["users", "list", { page, status }]`
- Details: `["users", "detail", userId]`
- All parameters that affect the request result must enter key.

## Optimistic update

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

The virtual list scenario is designed to separate data paging and DOM virtualization.

## API layer integration

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

API functions do not contain UI toast, loading or caching logic.
