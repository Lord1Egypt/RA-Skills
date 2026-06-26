# Data Mover Skill - 跨系统数据搬运工

🤖 自动识别屏幕数据，跨系统复制粘贴，支持 Excel→CRM、邮件→ERP、网页→数据库等场景。

## ✨ 功能特性

- 📸 **OCR 识别** - 屏幕截图文字识别（支持中文）
- 🖱️ **自动复制粘贴** - 模拟键鼠操作
- 📊 **多系统支持** - Excel、CRM、ERP、数据库等
- 🗺️ **智能映射** - 自动字段映射
- ✅ **数据验证** - 格式校验和完整性检查

## 🚀 快速开始

### 安装依赖
```bash
pip install pyautogui paddleocr pandas opencv-python
```

### 运行演示
```bash
python3 scripts/mover.py --demo
```

## 📋 配置

```json
{
  "ocr": {
    "engine": "paddleocr",
    "languages": ["ch", "en"]
  },
  "automation": {
    "speed": "normal",
    "retry_count": 3
  }
}
```

## 🔒 安全

- 本地处理，数据不出境
- 操作日志完整记录
- 支持 dry-run 模式

## 📄 许可证

MIT License

**作者**: 于金泽  
**版本**: 1.0.0  
**日期**: 2026-03-16
