# 测试报告模块使用指南

## 📖 概述

测试报告模块提供完整的测试报告解决方案：
- HTML格式测试报告（美观、易读）
- AI智能失败分析
- 报告导出（HTML/PDF）
- 测试统计汇总
- 历史报告管理

## 🚀 快速开始

### 1. 自动生成报告

测试执行完成后，系统会自动生成测试报告：

```bash
# 执行测试后，自动生成报告
POST http://localhost:8000/execute/run
Authorization: Bearer your_auth_code

{
  "script_id": 1,
  "environment": "dev",
  "timeout": 300
}

# 系统会自动创建执行记录和测试报告
```

### 2. 手动生成报告

如果需要重新生成报告或添加AI分析：

```bash
POST http://localhost:8000/api/report/generate
Authorization: Bearer your_auth_code

{
  "record_id": 123,
  "include_ai_analysis": true
}
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "报告生成成功",
  "data": {
    "id": 1,
    "record_id": 123,
    "script_id": 1,
    "script_name": "用户API测试",
    "script_type": "api",
    "result": "fail",
    "total_tests": 5,
    "passed_tests": 3,
    "failed_tests": 2,
    "duration": 10,
    "report_path": "data/reports/用户API测试_20260323_100000.html",
    "ai_analysis": "失败原因：\n1. 第3个测试用例断言失败...",
    "create_time": "2026-03-23 10:00:00"
  }
}
```

### 3. 查看报告列表

```bash
GET http://localhost:8000/api/report/list?script_id=1&limit=50
Authorization: Bearer your_auth_code
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "查询成功",
  "data": [
    {
      "id": 1,
      "script_name": "用户API测试",
      "script_type": "api",
      "result": "fail",
      "total_tests": 5,
      "passed_tests": 3,
      "failed_tests": 2,
      "duration": 10,
      "create_time": "2026-03-23 10:00:00"
    }
  ]
}
```

### 4. 获取报告详情

```bash
GET http://localhost:8000/api/report/1
Authorization: Bearer your_auth_code
```

### 5. 导出报告

**导出HTML：**

```bash
POST http://localhost:8000/api/report/export
Authorization: Bearer your_auth_code

{
  "report_id": 1,
  "format": "html",
  "include_screenshots": true
}

# 返回HTML文件下载
```

**导出PDF：**

```bash
POST http://localhost:8000/api/report/export

{
  "report_id": 1,
  "format": "pdf",
  "include_screenshots": true
}

# 返回PDF文件下载
```

### 6. AI失败分析

如果测试失败且报告未包含AI分析，可以手动生成：

```bash
POST http://localhost:8000/api/report/ai-analysis
Authorization: Bearer your_auth_code

{
  "report_id": 1,
  "log_content": "执行日志内容..."
}
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "AI分析生成成功",
  "data": {
    "report_id": 1,
    "analysis_result": "## 失败原因分析\n\n1. **断言失败**：期望状态码200，实际返回404\n   - 位置：test_user_api.py:15\n   - 可能原因：接口路径错误或接口未部署\n\n2. **超时错误**：请求超过5秒未响应\n   - 位置：test_user_api.py:22\n   - 可能原因：网络延迟或服务器响应慢\n\n## 解决建议\n\n1. 检查接口路径是否正确\n2. 确认测试环境API服务正常运行\n3. 增加请求超时时间或优化接口性能\n"
  }
}
```

## 📊 报告内容说明

### HTML报告包含

1. **报告头部**
   - 脚本名称和类型
   - 生成时间
   - 测试结果标识

2. **测试统计**
   - 总测试数
   - 通过数量
   - 失败数量
   - 执行耗时

3. **执行日志**
   - 完整的测试执行日志
   - 错误堆栈信息
   - 语法高亮显示

4. **AI分析**（如果启用）
   - 失败原因分析
   - 问题定位
   - 解决建议

### 报告样式

- ✅ 现代化UI设计
- ✅ 响应式布局（支持移动端）
- ✅ 彩色统计卡片
- ✅ 代码高亮显示
- ✅ 渐变背景效果

## 🔧 API 接口列表

| 接口 | 方法 | 描述 | 权限 |
|------|------|------|------|
| `/api/report/generate` | POST | 生成测试报告 | execute/all |
| `/api/report/list` | GET | 获取报告列表 | execute/all |
| `/api/report/{id}` | GET | 获取报告详情 | execute/all |
| `/api/report/record/{record_id}` | GET | 根据执行记录获取报告 | execute/all |
| `/api/report/export` | POST | 导出报告（HTML/PDF） | execute/all |
| `/api/report/ai-analysis` | POST | 生成AI分析 | execute/all |
| `/api/report/{id}` | DELETE | 删除报告 | execute/all |

## 💡 最佳实践

### 1. 报告生成时机

**推荐流程：**

```
执行测试 → 保存执行记录 → 自动生成报告
      ↓
测试失败 → 生成AI分析
      ↓
用户查看报告 → 导出PDF存档
```

### 2. AI分析使用

- 仅在测试失败时使用（节省API调用）
- 提供完整的执行日志（分析更准确）
- 结合人工判断（AI建议仅供参考）

### 3. 报告管理

- 定期清理旧报告（节省存储空间）
- 重要报告导出PDF归档
- 失败报告保留AI分析记录

### 4. 报告分享

- HTML报告可直接分享文件
- PDF报告适合正式文档
- 报告链接需授权码访问

## ⚠️ 注意事项

1. **PDF导出**
   - 需要安装weasyprint：`pip install weasyprint`
   - Windows需要安装GTK+
   - 首次使用可能需要配置环境

2. **AI分析**
   - 需要配置DeepSeek API Key
   - 每次分析消耗API调用额度
   - 分析结果仅供参考

3. **报告存储**
   - 报告文件存储在 `data/reports/`
   - 定期清理避免占用过多空间
   - 重要报告建议导出备份

## 🐛 故障排查

### 报告生成失败

**可能原因：**
1. 执行记录不存在
2. 脚本已被删除
3. 日志解析错误

**解决方法：**
- 确认执行记录ID正确
- 检查脚本是否还存在
- 查看后端日志

### PDF导出失败

**可能原因：**
1. weasyprint未安装
2. GTK+环境缺失（Windows）
3. 报告HTML格式错误

**解决方法：**

```bash
# Linux/Mac
pip install weasyprint

# Windows（需要额外步骤）
pip install weasyprint
# 下载并安装GTK+：https://gtk.org/download/
```

### AI分析失败

**可能原因：**
1. DeepSeek API Key无效
2. 网络连接问题
3. API调用超限

**解决方法：**
- 检查 `.env` 文件中的 `DEEPSEEK_API_KEY`
- 验证网络连接
- 查看API使用额度

## 📈 报告示例

### 成功报告

```
测试结果: ✓ 通过
总测试数: 10
通过数量: 10
失败数量: 0
执行耗时: 15秒

执行日志：
test_login.py::test_login_success PASSED
test_login.py::test_login_invalid_password PASSED
test_user.py::test_create_user PASSED
...
```

### 失败报告（含AI分析）

```
测试结果: ✗ 失败
总测试数: 10
通过数量: 7
失败数量: 3
执行耗时: 20秒

AI分析：

## 失败原因

1. **断言失败**：test_user.py:25
   - 预期：status_code == 200
   - 实际：status_code == 404
   - 原因：用户ID不存在

2. **超时错误**：test_api.py:30
   - 请求超时（>30秒）
   - 可能原因：接口响应慢

## 解决建议

1. 检查测试数据是否正确
2. 优化接口性能
3. 增加超时时间
```

## 🎨 自定义报告

如果需要自定义报告样式，可以修改：
- `report_service.py` 中的 `_generate_html_report()` 方法
- 自定义HTML模板和CSS样式
- 添加公司Logo和品牌元素

## 📚 相关文档

- **测试执行指南**：`docs/API_TEST_GUIDE.md`
- **AI生成指南**：`docs/AI_GENERATOR_GUIDE.md`
- **API文档**：http://localhost:8000/docs

---

**版本：** v1.0.0
**更新时间：** 2026-03-23
