# ATOM-DATA-022 - 创建 Metadata

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 创建 Metadata  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-022

**一句话描述：** 在 Metadata 文件中创建新的键值对条目

---

## 🎯 输入输出

### 输入
- **类型：** 字典
- **内容：** 键名 + 键值
- **格式：** @{key=value}

### 输出
- **类型：** 布尔值
- **内容：** 创建成功/失败
- **附加：** Metadata 文件路径

---

## ⚙️ 偏好设置

### Metadata 文件
- **路径：** `knowledge-base/metadata.md`
- **格式：** YAML Front Matter + Markdown
- **编码：** UTF-8

### 键名规范
- **格式：** 英文小写 + 下划线
- **示例：** `project_name`, `last_updated`, `version`
- **禁止：** 中文、大写字母、特殊符号

### 值类型
- **字符串：** "value"
- **数字：** 123
- **布尔：** true/false
- **数组：** [item1, item2]
- **对象：** {key: value}

---

## 📝 操作步骤

```powershell
# 1. 准备 Metadata 文件路径
$metadataPath = "C:\Users\Xiabi\.openclaw\workspace\knowledge-base\metadata.md"

# 2. 检查文件存在，不存在则创建
if (-not (Test-Path $metadataPath)) {
    "---`nmetadata:`n  created: $(Get-Date -Format 'yyyy-MM-dd')`n---" | 
        Set-Content $metadataPath -Encoding UTF8
}

# 3. 准备新条目
$newEntry = @{
    project_name = "感知与行动中心"
    created_date = "2026-03-07"
    status = "active"
}

# 4. 读取现有内容
$content = Get-Content $metadataPath -Raw

# 5. 追加新条目（YAML 格式）
foreach ($kv in $newEntry.GetEnumerator()) {
    $content += "`n$($kv.Key): $($kv.Value)"
}

# 6. 保存文件
$content | Set-Content $metadataPath -Encoding UTF8

# 7. 返回成功
Write-Host "✅ Metadata 已创建：$($newEntry.Count) 个条目"
return $true
```

---

## 🔄 使用场景

### 场景 1：新项目 Metadata
```
触发：创建项目卡片后
  ↓
调用：ATOM-DATA-022
  ↓
输出：Metadata 文件新增项目信息
```

### 场景 2：系统配置 Metadata
```
触发：系统初始化
  ↓
调用：ATOM-DATA-022
  ↓
输出：系统配置信息
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-DATA-024：更新 Metadata

### 常组合使用
- ATOM-DATA-022 + ATOM-DATA-023
  （创建 → 读取验证）

---

## ✅ 检查清单

执行前确认：
- [ ] 键名符合规范（英文小写 + 下划线）
- [ ] 值类型正确
- [ ] Metadata 文件可写
- [ ] 键名不重复（如重复则报错）

---

## ⚠️ 常见错误

### 错误 1：键名不规范
```
❌ 错误：Project-Name（大写 + 横线）
✅ 正确：project_name（小写 + 下划线）
```

### 错误 2：键名重复
```
❌ 错误：覆盖已有键
✅ 正确：检查键是否存在，存在则报错或调用更新动作
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
