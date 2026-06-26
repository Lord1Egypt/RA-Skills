# 电商分类采集技能 (Ecommerce Category Collector)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green)
![License](https://img.shields.io/badge/license-MIT-orange)

自动化批量提交电商网站分类链接采集任务到Audtools平台。

## ✨ 功能特性

- **批量处理**：支持单个CSV文件或整个目录
- **智能验证**：自动验证CSV格式和链接有效性
- **自动登录**：集成Audtools账号自动登录
- **参数配置**：可调节采集数量、间隔时间等
- **测试模式**：安全测试前几条数据
- **详细日志**：完整的操作日志和错误报告

## 🚀 快速开始

### 安装
```bash
# 复制到OpenClaw技能目录
cp -r ecommerce-category-collector ~/.openclaw/extensions/skills/

# 安装依赖
cd ~/.openclaw/extensions/skills/ecommerce-category-collector
npm install
```

### 配置
编辑 `scripts/collector.js` 中的账号信息：
```javascript
const CONFIG = {
  username: '你的手机号',   // 修改这里
  password: '你的密码',     // 修改这里
  // ... 其他配置
};
```

### 使用
```bash
# 测试模式
/collect-categories test/sample.csv --test

# 正式采集
/collect-categories /path/to/your.csv --items 9999

# 批量处理目录
/collect-categories /path/to/directory/
```

## 📁 项目结构

```
ecommerce-category-collector/
├── SKILL.md                    # 技能说明文档
├── README.md                   # 项目说明
├── package.json               # 项目配置
├── scripts/
│   └── collector.js           # 主采集脚本
├── references/
│   └── csv-format.md          # CSV格式规范
└── test/
    └── sample.csv             # 测试数据
```

## 📋 CSV格式要求

### 必需格式
必须包含"完整链接"列：
```csv
完整链接,分类路径,域名,1级分类,2级分类,3级分类
https://example.com/collections/dresses,dresses,example.com,Women,Dresses,
```

### 验证规则
1. ✅ 文件存在且可读
2. ✅ 包含"完整链接"列
3. ✅ 链接以http/https开头
4. ⚠️ 警告非collections链接

## ⚙️ 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `username` | `15715090600` | Audtools登录手机号 |
| `password` | `zzw12345` | Audtools登录密码 |
| `default_items` | `9999` | 默认采集商品数 |
| `default_interval` | `2000` | 操作间隔(ms) |
| `default_close_delay` | `3000` | Tab关闭延迟(ms) |

## 📖 详细文档

- [操作文档](../../工作/电商分类采集工具操作文档.md) - 完整的使用说明
- [快速指南](../../工作/电商分类采集工具快速指南.md) - 快速上手指南
- [CSV格式参考](references/csv-format.md) - 详细的CSV格式规范

## 🔧 开发指南

### 运行测试
```bash
npm test
```

### 代码结构
```javascript
// 主要函数
validateCSV(filePath)      // 验证CSV文件
getCSVFiles(dirPath)       // 获取目录下CSV文件
executeCollection(links, options) // 执行采集任务
```

### 扩展功能
1. 集成OpenClaw浏览器API
2. 添加断点续传功能
3. 支持更多电商平台
4. 添加结果导出功能

## 🐛 故障排除

### 常见问题
1. **CSV格式错误**：确保包含"完整链接"列
2. **登录失败**：检查账号密码配置
3. **处理中断**：使用测试模式验证

### 获取帮助
- 查看详细操作文档
- 检查错误日志输出
- 提交GitHub Issue

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👥 贡献者

- **张起荣** - 项目发起人
- **OpenClaw Assistant** - 技能开发

## 📞 联系方式

- 问题反馈：GitHub Issues
- 功能建议：OpenClaw社区
- 紧急支持：Discord社区

---

**提示**：使用前请确保遵守目标网站的使用条款和服务协议。

**最后更新**: 2026年3月18日  
**版本**: v1.0.0