---
name: coding-lite
description: 轻量级编码助手，支持 Python 脚本生成与执行、Excel/WPS 函数自动化、小程序代码生成、SQL 查询助手。快速响应，不占用过多 context。
---

# Coding-Lite 轻量级编码助手

## 触发场景

当用户需要快速生成代码、自动化脚本、数据处理或查询时使用此技能。适合轻量级、高频的编码需求。

## 技术范围

### 1. Python 脚本生成与执行 🐍

**支持场景：**
- 文件批量处理（重命名、格式转换）
- 数据抓取（网页、API）
- 数据分析（pandas、numpy）
- 自动化办公（邮件、文件操作）
- 简单爬虫
- 文本处理

**示例：**
```python
# 批量重命名文件
import os
for i, f in enumerate(os.listdir('.')):
    os.rename(f, f'img_{i:03d}.jpg')
```

---

### 2. Excel / WPS 函数自动化 📊

**支持场景：**
- 复杂公式编写（VLOOKUP、INDEX/MATCH、数组公式）
- 数据透视表配置
- 条件格式设置
- VBA 宏脚本
- WPS 自动化（Python for WPS）

**常用公式模板：**
```excel
=VLOOKUP(A2,Sheet2!$A:$D,4,FALSE)
=INDEX($C:$C,MATCH(1,(A2=$A:$A)*(B2=$B:$B),0))
=SUMPRODUCT((A2:A100="条件")*(B2:B100))
```

---

### 3. 小程序代码生成 📱

**支持平台：**
- 微信小程序
- 支付宝小程序
- 抖音小程序

**支持内容：**
- 页面结构（WXML/AXML）
- 样式（WXSS/ACSS）
- 逻辑（JavaScript/TypeScript）
- 配置文件（app.json）
- 云函数

**示例（微信小程序）：**
```javascript
// pages/index/index.js
Page({
  data: { count: 0 },
  onTap() {
    this.setData({ count: this.data.count + 1 })
  }
})
```

---

### 4. SQL 查询助手 💾

**支持数据库：**
- MySQL
- PostgreSQL
- SQLite
- SQL Server
- Oracle

**支持场景：**
- 基础查询（SELECT、JOIN、GROUP BY）
- 复杂查询（子查询、窗口函数）
- 数据操作（INSERT、UPDATE、DELETE）
- 表结构查询
- 性能优化建议

**示例：**
```sql
-- 查询每个部门的平均工资
SELECT dept, AVG(salary) as avg_sal
FROM employees
GROUP BY dept
ORDER BY avg_sal DESC;

-- 窗口函数示例
SELECT name, dept, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
FROM employees;
```

---

## 使用原则

### ✅ 适合的场景
- 快速原型/脚本
- 一次性任务自动化
- 数据查询/处理
- 学习/参考代码
- 简单功能实现

### ❌ 不适合的场景
- 大型项目开发（需要完整工程化）
- 高并发/高性能要求
- 复杂系统架构
- 生产环境关键代码

---

## 输出规范

### 代码格式
- 简洁优先，避免过度设计
- 添加必要注释
- 标注依赖和运行环境
- 提供使用示例

### 安全提示
- 标注潜在安全风险（如 SQL 注入）
- 敏感操作需二次确认
- 不生成恶意代码

---

## 快速参考

### Python 常用命令
```bash
python script.py          # 运行脚本
pip install package       # 安装依赖
python -m venv venv       # 创建虚拟环境
```

### Excel 快捷键
```
Ctrl + `          显示公式
Ctrl + Shift + ↓  选中区域
Alt + =           自动求和
```

### SQL 调试
```sql
EXPLAIN SELECT ...    -- 查看执行计划
SHOW WARNINGS;        -- 查看警告
```

---

## 注意事项

- 执行代码前请确认环境安全
- 涉及数据的操作请先备份
- 生产环境代码需要完整测试
- 遵守开源许可证要求
