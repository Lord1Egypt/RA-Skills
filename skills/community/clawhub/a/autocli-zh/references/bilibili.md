# Bilibili

## 常用模式

### 热门
```bash
autocli bilibili hot --limit 10
```

### 排行榜
```bash
autocli bilibili ranking --limit 10
```

### 搜索
```bash
autocli bilibili search --keyword "OpenClaw"
```

### 动态
```bash
autocli bilibili feed --limit 10
```

### 历史
```bash
autocli bilibili history --limit 10
```

### 收藏夹
```bash
autocli bilibili favorite
```

## 最小说明

- 热门、排行、搜索通常较稳；动态、历史、收藏夹等个人数据更依赖登录态。
- 若 Bilibili 已掉登录，涉及个人数据的命令结果可能为空或异常。
