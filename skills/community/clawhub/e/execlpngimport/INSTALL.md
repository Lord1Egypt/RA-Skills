# excel-import-helper 安装指南

## 方式一：ClawHub 安装（推荐）

### 1. 登录 ClawHub

```bash
npx clawhub login
```

浏览器会自动打开，按提示完成登录。

### 2. 发布 Skill

```bash
npx clawhub publish ./excel-import-helper --slug excel-import-helper --name "Excel导入模板助手" --version 1.0.0
```

发布后，其他用户可以通过以下命令安装：

```bash
npx clawhub install excel-import-helper
```

---

## 方式二：手动安装

### 1. 复制 Skill 文件夹

将整个 `excel-import-helper` 文件夹复制到目标电脑的 Skill 目录：

```
~/.qclaw/workspace/skills/excel-import-helper/
```

### 2. 安装依赖

```bash
pip install openpyxl cnocr
```

### 3. 使用

在 QClaw 中直接说：

> "帮我把 xxx.png 导入到模板"

---

## 目录结构

```
excel-import-helper/
├── SKILL.md                    # Skill 说明文档
├── INSTALL.md                  # 本安装指南
└── scripts/
    ├── generate_template.py    # 主程序
    └── field_mapping.py         # 字段映射库
```

---

## 依赖说明

| 依赖 | 版本 | 说明 |
|-----|------|------|
| openpyxl | 最新 | Excel 文件读写 |
| cnocr | 最新 | OCR 文字识别（支持中文） |

---

## 使用示例

### 处理 Excel 文件

用户提供：
- 模板路径：`C:\...\Excel导入模板.xlsx`
- 数据源路径：`C:\...\功能字段.xlsx`
- 表中文名：`资产负债表`

系统自动生成：`资产负债表_导入模板.xlsx`

### 处理截图/图片

用户提供：
- 图片路径：`C:\...\现金流量.png`
- 表中文名：`现金流量表`

系统自动：
1. OCR 识别图片文字
2. 提取字段名
3. 生成中英文字段映射
4. 识别字段类型
5. 输出模板文件
