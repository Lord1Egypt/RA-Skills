# Hacker News

## 常用模式

### 热门
```bash
autocli hackernews top --limit 10
```

### 最新
```bash
autocli hackernews new --limit 10
```

### Ask HN
```bash
autocli hackernews ask --limit 10
```

### Show HN
```bash
autocli hackernews show --limit 10
```

### Jobs
```bash
autocli hackernews jobs --limit 10
```

### 搜索
```bash
autocli hackernews search "OpenClaw" --limit 10
```

### 用户
```bash
autocli hackernews user <username>
```

## 最小说明

- Hacker News 多数命令属于公开读操作，通常不依赖浏览器登录态。
- 若搜索结果不理想，常见原因是查询词过宽，或更适合改用 top / new / ask / show 分流查看。
