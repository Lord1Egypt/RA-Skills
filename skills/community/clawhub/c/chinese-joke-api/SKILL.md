# Chinese Joke API Skill

## 概述

这个 skill 使用第三方中文笑话 API 获取有趣的中式幽默。

## API 源

### 1. 一言 API (Hitokoto)

**特点**: 包含各种类型的中文短句，包括笑话

**基础 URL**: `https://v1.hitokoto.cn`

**用法**:
```bash
curl "https://v1.hitokoto.cn?c=j"
```

参数:
- `c=j` - 搞笑类别
- `c=a` - 动画
- `c=b` - 漫画
- `c=c` - 原创

### 2. 简短笑话 API

**特点**: 专门的笑话 API，返回中文短笑话

**基础 URL**: `https://api.jokeapi.cn`

**用法**:
```bash
curl "https://api.jokeapi.cn/joke/Any?safe-mode"
```

## 快速开始

### 使用 Bash

```bash
# 获取一言搞笑
curl -s "https://v1.hitokoto.cn?c=j" | python3 -m json.tool

# 获取简短笑话
curl -s "https://api.jokeapi.cn/joke/Any?safe-mode" | python3 -m json.tool
```

### 使用 Python

```python
import requests

# 一言搞笑
resp = requests.get("https://v1.hitokoto.cn?c=j")
data = resp.json()
print(f"{data['hitokoto']} - {data['from']}")

# 简短笑话
resp = requests.get("https://api.jokeapi.cn/joke/Any?safe-mode")
data = resp.json()
if data['type'] == 'single':
    print(data['joke'])
else:
    print(data['setup'])
    print(data['delivery'])
```

## 示例代码

### Bash 脚本

```bash
#!/bin/bash
# 获取一言搞笑
curl -s "https://v1.hitokoto.cn?c=j" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'「{d['hitokoto']}」')
print(f'—— {d.get('from_') or d.get('from')}')
"
```

### Python 脚本

```python
#!/usr/bin/env python3
import requests
import json

def get_chinese_joke():
    """获取中文笑话"""
    try:
        # 尝试一言 API
        resp = requests.get("https://v1.hitokoto.cn?c=j", timeout=5)
        data = resp.json()
        print(f"「{data['hitokoto']}」")
        print(f"—— {data.get('from_', data.get('from'))}")
        return True
    except Exception as e:
        print(f"获取失败：{e}")
        return False

if __name__ == "__main__":
    get_chinese_joke()
```

## 注意事项

⚠️ 这些 API 都是第三方服务，可用性可能不稳定：
- 一言 API：偶尔响应慢
- 简短笑话 API：可能有时限流

建议：
- 添加错误处理
- 设置超时
- 考虑备用 API

## 相关链接

- [Hitokoto 一言](https://hitokoto.cn/)
- [简短笑话 API](https://jokeapi.cn/)
