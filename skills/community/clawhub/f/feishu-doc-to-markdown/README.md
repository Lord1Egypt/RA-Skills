# 飞书文档智能转换Markdown技能

自动将飞书文档转换为高可用、高信息密度的Markdown文档，智能处理飞书私有资源、无效占位符、冗余引用，生成不同纯净度的版本满足不同场景需求。

## 功能特性
- 📝 **多版本输出**：支持原始备份版、纯文本增强版、最终优化版三个等级
- 🧠 **智能内容提取**：自动识别图片、图表、白板等非文本内容的核心信息并转换为结构化文本
- 🧹 **冗余自动清理**：自动移除无效占位符、无法访问的内部引用、无意义标签
- 🗂️ **自动分类归档**：按日期/项目自动分类保存到知识库
- 🔗 **知识自动关联**：自动提取核心要点，关联到对应项目/领域标签

## 安装
```bash
clawdhub install feishu-doc-to-markdown
```

## 使用方法
### 基础使用
转换飞书文档，默认生成最终优化版：
```bash
feishu_doc_convert https://bytedance.larkoffice.com/docx/xxxxxx
```

### 指定输出版本
```bash
# 原始备份版（完整保留所有原始内容和标签）
feishu_doc_convert https://bytedance.larkoffice.com/docx/xxxxxx --version raw

# 纯文本增强版（提取非文本核心信息，保留完整上下文）
feishu_doc_convert https://bytedance.larkoffice.com/docx/xxxxxx --version enhanced

# 最终优化版（清理冗余，输出高信息密度内容）
feishu_doc_convert https://bytedance.larkoffice.com/docx/xxxxxx --version optimized
```

### 其他参数
```bash
# 指定输出目录
feishu_doc_convert https://bytedance.larkoffice.com/docx/xxxxxx --output ./docs/

# 自动同步到知识库
feishu_doc_convert https://bytedance.larkoffice.com/docx/xxxxxx --sync-to-knowledgebase
```

## 依赖要求
- OpenClaw 版本 >= 0.8.0
- 已安装并配置 `feishu` 插件
- 飞书账号授权：拥有文档阅读权限

## 配置选项
在 `openclaw.json` 中可以配置默认行为：
```json
{
  "plugins": {
    "feishu-doc-to-markdown": {
      "default_version": "optimized",
      "auto_archive": true,
      "archive_path": "./raw_sources/",
      "auto_sync_to_kb": false
    }
  }
}
```

## 示例
转换后的最终优化版效果：
- 移除所有无效占位符、内部引用链接
- 图片/图表内容自动提取核心信息转换为文字描述或表格
- 内容精简，无冗余信息，可直接阅读使用

## License
MIT
