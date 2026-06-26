# Twitter / X

## 常用模式

### 时间线
```bash
autocli twitter timeline --limit 10
autocli twitter timeline --type following --limit 10
```

### 书签
```bash
autocli twitter bookmarks --limit 10
```

### 通知
```bash
autocli twitter notifications --limit 10
```

### 搜索
```bash
autocli twitter search "OpenClaw" --limit 10
```

### 用户主页
```bash
autocli twitter profile <username>
```

### 线程
```bash
autocli twitter thread --url "https://x.com/.../status/..."
```

## 最小说明

- 依赖浏览器登录态；若 X/Twitter 已掉登录，结果可能为空或异常。
- 写操作外部可见，且部分动作可能不可逆。
