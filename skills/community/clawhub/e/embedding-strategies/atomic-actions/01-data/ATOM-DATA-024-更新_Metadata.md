# ATOM-DATA-024 - 更新 Metadata

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 更新 Metadata  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-024

**一句话描述：** 更新 Metadata 文件中已存在的键值对

---

## 🎯 输入输出

### 输入
- **类型：** 字典
- **内容：** 键名 + 新值
- **格式：** @{key=newValue}

### 输出
- **类型：** 布尔值
- **内容：** 更新成功/失败
- **附加：** 更新的键数量

---

## ⚙️ 偏好设置

### Metadata 文件
- **路径：** `knowledge-base/metadata.md`
- **格式：** YAML Front Matter + Markdown
- **编码：** UTF-8

### 更新模式
- **覆盖模式：** 直接覆盖旧值（默认）
- **追加模式：** 数组类型追加元素
- **版本控制：** 保留历史版本（可选）

### 验证规则
- **键必须存在：** 不存在则报错（或调用创建动作）
- **值类型匹配：** 类型不匹配则警告

---

## 📝 操作步骤

```powershell
# 1. 准备 Metadata 文件路径
$metadataPath = "C:\Users\Xiabi\.openclaw\workspace\knowledge-base\metadata.md"

# 2. 准备更新内容
$updates = @{
    status = "active"
    last_updated = "2026-03-07"
    version = "V2.0"
}

# 3. 读取文件内容
$content = Get-Content $metadataPath -Raw

# 4. 更新键值对
foreach ($kv in $updates.GetEnumerator()) {
    $key = $kv.Key
    $value = $kv.Value
    
    # 检查键是否存在
    if ($content -match "^$key:\s*(.*)$") {
        # 替换旧值
        $content = $content -replace "^$key:\s*.*$", "$key`: $value"
        Write-Host "✅ 已更新：$key = $value"
    } else {
        Write-Host "⚠️ 键不存在：$key（是否调用创建动作？）"
    }
}

# 5. 保存文件
$content | Set-Content $metadataPath -Encoding UTF8

# 6. 返回成功
Write-Host "✅ Metadata 已更新：$($updates.Count) 个条目"
return $true
```

---

## 🔄 使用场景

### 场景 1：更新项目状态
```
触发：项目状态变化
  ↓
调用：ATOM-DATA-024
  ↓
输入：@{status="completed"; last_updated="2026-03-07"}
  ↓
输出：Metadata 更新成功
```

### 场景 2：版本号递增
```
触发：新版本发布
  ↓
调用：ATOM-DATA-024
  ↓
输入：@{version="V2.0"}
  ↓
输出：版本号已更新
```

---

## 🔗 关联动作

### 前置动作
- ATOM-DATA-022：创建 Metadata（如果键不存在）

### 后置动作
- ATOM-DATA-023：读取 Metadata（验证更新）

### 常组合使用
- ATOM-DATA-023 + ATOM-DATA-024
  （读取 → 更新）

---

## ✅ 检查清单

执行前确认：
- [ ] Metadata 文件存在
- [ ] 键名正确
- [ ] 值类型匹配
- [ ] 编码 UTF-8

---

## ⚠️ 常见错误

### 错误 1：键不存在
```
❌ 错误：尝试更新不存在的键
✅ 正确：先用 ATOM-DATA-023 检查，或调用 ATOM-DATA-022 创建
```

### 错误 2：值类型不匹配
```
❌ 错误：字符串字段赋值数字
✅ 正确：保持类型一致
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
