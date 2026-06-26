# API 字段大小写问题经验总结

**日期**: 2026-03-14  
**问题**: `check_domain()` 返回字段大小写导致误判  
**影响**: 批量查询 400+ 个域名，全部误判为"已注册"

---

## 🐛 问题现象

### 第一次查询（错误）

```python
result = client.check_domain("qwenbot.cn")
is_available = result.get('Available', False)  # ❌ 大写 A
print(is_available)  # 输出：False
```

**结果**: 查询 400+ 个域名，全部显示"已注册"

### 第二次查询（正确）

```python
result = client.check_domain("qwenbot.cn")
is_available = result.get('available', False)  # ✅ 小写 a
print(is_available)  # 输出：True/False（正确）
```

**结果**: 发现 43 个可注册域名

---

## 🔍 问题原因

### API 返回格式

阿里云 API 返回的字典字段都是**小写**：

```json
{
  "available": true,           // ✅ 小写
  "domain_name": "example.cn", // ✅ 小写
  "premium": false,            // ✅ 小写
  "avail_code": 1,             // ✅ 小写
  "price_info": [...],         // ✅ 小写
  "raw_response": {...}        // ✅ 小写
}
```

### 错误代码

```python
# ❌ 错误 - 使用大写字段名
is_available = result.get('Available', False)
# 返回：None 或 False（默认值）
```

### 正确代码

```python
# ✅ 正确 - 使用小写字段名
is_available = result.get('available', False)
# 返回：True 或 False
```

---

## 📊 影响范围

| 查询批次 | 域名数量 | 结果 | 原因 |
|:---|:---:|:---|:---|
| 第 1 批 | 30 | 全部已注册 ❌ | 字段大小写错误 |
| 第 2 批 | 50 | 全部已注册 ❌ | 字段大小写错误 |
| 第 3 批 | 60 | 全部已注册 ❌ | 字段大小写错误 |
| 第 4 批 | 80 | 全部已注册 ❌ | 字段大小写错误 |
| 第 5 批 | 100 | 全部已注册 ❌ | 字段大小写错误 |
| 第 6 批 | 100 | 全部已注册 ❌ | 字段大小写错误 |
| **第 7 批** | **30** | **13 个可注册 ✅** | **修复后正确** |
| **第 8 批** | **50** | **30 个可注册 ✅** | **修复后正确** |

**总计**: 浪费 6 次查询，约 420 个域名的无效检查

---

## ✅ 解决方案

### 1. 使用正确的字段名

```python
# ✅ 所有字段都是小写
result = client.check_domain(domain)
is_available = result.get('available', False)
domain_name = result.get('domain_name', '')
premium = result.get('premium', False)
avail_code = result.get('avail_code', 0)
price_info = result.get('price_info', [])
```

### 2. 批量查询前的验证

```python
# 先用随机域名测试 API 是否正常
test_domain = f"xyzabc{random.randint(10000, 99999)}.com"
result = client.check_domain(test_domain)

print(f'测试返回：{result.keys()}')
print(f'available: {result.get("available")}')

# 确认返回正常后再批量查询
if 'available' in result:
    print('✅ API 正常，开始批量查询')
else:
    print('❌ API 异常，检查问题')
```

### 3. 调试技巧

```python
# 打印完整响应
result = client.check_domain(domain)
print(f'返回类型：{type(result)}')
print(f'所有键：{list(result.keys())}')
print(f'完整返回：{json.dumps(result, indent=2)}')
```

---

## 📝 最佳实践

### 代码规范

```python
def check_and_register_domain(domain_name: str) -> bool:
    """检查域名是否可注册"""
    
    # 1. 查询域名
    result = client.check_domain(domain_name)
    
    # 2. 使用小写字段名
    is_available = result.get('available', False)
    
    # 3. 获取价格信息
    price_info = result.get('price_info', [])
    price = price_info[0].get('money', 'N/A') if price_info else 'N/A'
    
    # 4. 返回结果
    if is_available:
        print(f'✅ {domain_name} 可注册，价格：¥{price}')
        return True
    else:
        print(f'❌ {domain_name} 已注册')
        return False
```

### 批量查询模板

```python
def batch_check_domains(domains: List[str]) -> List[Dict]:
    """批量检查域名可注册性"""
    
    available_domains = []
    
    # 1. 先用随机域名测试 API
    test_result = client.check_domain("test123456.com")
    if 'available' not in test_result:
        print('❌ API 返回格式异常')
        return []
    
    # 2. 批量查询
    for domain in domains:
        result = client.check_domain(domain)
        
        # ⚠️ 使用小写字段名
        if result.get('available', False):
            price_info = result.get('price_info', [])
            available_domains.append({
                'domain': domain,
                'price': price_info[0].get('money', 'N/A') if price_info else 'N/A'
            })
    
    return available_domains
```

---

## 🎯 经验教训

### 1. API 字段命名规范

- ✅ 阿里云 SDK 返回的字典字段都是**小写**
- ✅ 使用 `result.get('field_name')` 而非 `result.get('FieldName')`
- ✅ 不确定时先打印 `result.keys()` 确认

### 2. 批量操作前的验证

- ✅ 先用少量测试数据验证 API 正常
- ✅ 检查返回字段名和数据结构
- ✅ 确认逻辑正确后再批量执行

### 3. 异常结果的分析

- ✅ 如果结果"好得不真实"（如 400 个域名全部已注册），要怀疑是 bug
- ✅ 用已知的可注册域名（如随机长域名）验证 API
- ✅ 对比多次查询结果，寻找异常模式

### 4. 代码注释的重要性

- ✅ 在关键 API 调用处添加字段名注释
- ✅ 标注易错点（如大小写、必填字段）
- ✅ 记录已知的坑和解决方案

---

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能说明文档（已更新此问题说明）
- [aliyun_domain.py](../scripts/aliyun_domain.py) - API 客户端代码

---

## 🔖 快速参考

| 字段 | 正确 | 错误 |
|:---|:---|:---|
| available | ✅ `result.get('available')` | ❌ `result.get('Available')` |
| domain_name | ✅ `result.get('domain_name')` | ❌ `result.get('DomainName')` |
| premium | ✅ `result.get('premium')` | ❌ `result.get('Premium')` |
| price_info | ✅ `result.get('price_info')` | ❌ `result.get('PriceInfo')` |

**记忆口诀**: API 返回全小写，字段名称要记牢！

---

**创建时间**: 2026-03-14  
**最后更新**: 2026-03-14
