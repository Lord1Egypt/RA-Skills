# B站API使用指南

## 概览

本指南详细介绍B站用户信息查询的API使用方法、注意事项和常见问题。

## 目录

1. [API说明](#api说明)
2. [如何获取vmid](#如何获取vmid)
3. [错误码说明](#错误码说明)
4. [批量查询方法](#批量查询方法)
5. [常见问题](#常见问题)

## API说明

### 用户关系统计API

**接口地址：** `https://api.bilibili.com/x/relation/stat`

**请求方式：** GET

**参数说明：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vmid | string | 是 | 用户ID |

**返回示例：**

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "mid": 8047632,
    "following": 123,
    "whisper": 0,
    "black": 0,
    "follower": 456789
  }
}
```

**字段说明：**

- `code`: 状态码，0表示成功
- `message`: 返回信息
- `data.mid`: 用户ID
- `data.following`: 关注数
- `data.follower`: 粉丝数
- `data.whisper`: 悄悄关注数
- `data.black`: 黑名单数

### 用户名获取

用户名通过解析B站移动端页面获取：
- 页面地址：`https://m.bilibili.com/space/{vmid}`
- 解析方法：从页面title标签中提取

## 如何获取vmid

### 方法1：从个人主页URL获取

1. 访问B站用户个人主页
2. 查看URL，例如：`https://space.bilibili.com/8047632`
3. URL中的数字即为vmid（本例为8047632）

### 方法2：从视频页面获取

1. 打开任意UP主的视频页面
2. 点击UP主头像或名称进入个人空间
3. 从URL中获取vmid

### 方法3：通过搜索获取

1. 在B站搜索用户昵称
2. 进入用户主页
3. 从URL中获取vmid

## 错误码说明

| 错误码 | 说明 | 解决方法 |
|--------|------|----------|
| 0 | 成功 | - |
| -400 | 请求错误 | 检查参数格式 |
| -403 | 权限不足 | 检查是否需要登录 |
| -404 | 用户不存在 | 检查vmid是否正确 |
| -412 | 请求被拦截 | 降低请求频率 |
| -500 | 服务器错误 | 稍后重试 |

## 批量查询方法

### 方式1：Shell脚本循环

```bash
#!/bin/bash
# 批量查询多个用户的信息

vmids=("8047632" "1234567" "9876543")

for vmid in "${vmids[@]}"; do
    echo "查询用户: $vmid"
    python scripts/bili_query.py --vmid "$vmid"
    sleep 1  # 避免请求过快
done
```

### 方式2：Python批量处理

```python
import json
import time
from subprocess import run, PIPE

def batch_query(vmids, interval=1):
    """
    批量查询用户信息
    
    Args:
        vmids: 用户ID列表
        interval: 查询间隔（秒）
    """
    results = []
    
    for vmid in vmids:
        # 调用查询脚本
        result = run(
            ["python", "scripts/bili_query.py", "--vmid", str(vmid)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            results.append(data)
        
        time.sleep(interval)
    
    return results

# 使用示例
if __name__ == "__main__":
    vmids = [8047632, 1234567, 9876543]
    results = batch_query(vmids)
    print(json.dumps(results, ensure_ascii=False, indent=2))
```

## 常见问题

### Q1: 为什么粉丝数为0？

**可能原因：**
- 用户vmid错误
- 用户不存在或已被封禁
- 网络请求失败

**解决方法：**
- 检查vmid是否正确
- 查看脚本返回的错误信息
- 稍后重试

### Q2: 为什么无法获取用户名？

**可能原因：**
- B站页面结构变化
- 网络请求超时
- 用户设置了隐私保护

**解决方法：**
- 更新脚本中的正则表达式
- 检查网络连接
- 尝试使用其他方式获取

### Q3: 如何处理请求频率限制？

**建议：**
- 单次查询后等待1-2秒
- 批量查询时设置合理的间隔
- 避免短时间内大量请求同一接口

### Q4: 数据准确性如何？

**说明：**
- 粉丝数和关注数：实时数据，准确性高
- 用户名：可能存在延迟，建议以B站页面显示为准

### Q5: 是否需要登录或API Key？

**说明：**
- 公开API，无需登录
- 无需API Key或token
- 但需遵守B站使用条款和API调用规范

## 注意事项

1. **合法合规**：仅用于学习和合法的数据分析目的
2. **频率控制**：避免高频请求，尊重API限制
3. **数据时效**：粉丝数为实时数据，用户名可能延迟更新
4. **网络稳定**：确保网络连接稳定，避免超时错误
5. **错误处理**：脚本返回的JSON中包含error字段时表示出错

## 更新日志

- **v1.0** (2025-01)：初始版本，支持基本查询功能
