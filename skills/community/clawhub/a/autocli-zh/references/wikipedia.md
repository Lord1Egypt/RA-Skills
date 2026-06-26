# Wikipedia

## 常用模式

### 搜索
```bash
autocli wikipedia search "马斯克"
autocli wikipedia search "Elon Musk" --lang en --limit 10
```

### 摘要
```bash
autocli wikipedia summary "Elon Musk"
```

### 热门词条
```bash
autocli wikipedia trending --limit 10
```

### 随机词条
```bash
autocli wikipedia random --limit 5
```

## 最小说明

- Wikipedia 多数命令属于公开读操作，通常不依赖浏览器登录态。
- 若中文查询结果偏离目标，可补试英文词条名或切换 `--lang`。
