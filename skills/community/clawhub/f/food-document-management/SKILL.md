---
name: document-management
description: 文档管理能力；支持研发文档分类、版本管理、模板生成；当进行研发资料整理或文档编写时使用
dependency:
  python:
    - pandas==1.5.0
  system:
    - mkdir -p data/docs
---

# 文档管理

## 任务目标
- 本技能用于：规范研发文档管理和编写
- 核心能力：文档分类、版本控制、模板生成
- 触发条件：研发文档编写、资料整理、报告生成

## 数据来源

使用 `web_search` 获取文档规范：

```
# 文档规范
web_search(query="食品研发 文档管理 规范")
web_search(query="技术报告 格式 规范")
web_search(query="研发项目 文档模板 范例")
```

## 数据存储

文档数据保存在工作区 `data/docs/` 目录：
- `document_index.json` - 文档索引
- `templates/` - 文档模板
- `archive/` - 归档文档

## 操作步骤

### 1. 文档分类
1. 确定文档类别
2. 按项目/产品组织
3. 建立索引

### 2. 版本管理
1. 记录版本历史
2. 标注修改内容
3. 归档旧版本

### 3. 文档编写
1. 选择适用模板
2. 按规范填写
3. 审核发布

### 4. 检索利用
1. 建立检索目录
2. 快速定位文档
3. 复用已有资料

## 资源索引
- 文档管理脚本：见 [scripts/document_manager.py](scripts/document_manager.py)
- 文档模板：见 [assets/templates/](assets/templates/)
- 分类标准：见 [references/document_classification.md](references/document_classification.md)

## 注意事项
- 文档命名规范统一
- 及时更新版本号
- 做好备份存储
