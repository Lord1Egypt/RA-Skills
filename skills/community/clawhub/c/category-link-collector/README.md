# Category Link Collector Skill

一个用于采集电商网站分类链接信息的OpenClaw技能。

## 功能特点
- ✅ 从分类链接URL中提取完整分类路径
- ✅ 自动解析一级和二级分类名称
- ✅ 生成结构化的CSV文件
- ✅ 支持自定义输出目录
- ✅ 自动以域名为文件名保存
- ✅ 包含完整的中文表头说明

## 快速开始

### 基本使用
```python
from scripts.collect_categories import collect_category_links

links = [
    "https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops",
    "https://lulumonclick-eu.shop/collections/women-women-clothes-bras-underwear"
]

csv_path = collect_category_links(links)
print(f"文件已保存: {csv_path}")
```

### 命令行使用
```bash
cd skills/category-link-collector
python3 scripts/collect_categories.py
```

## 输出格式
生成的CSV文件包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 完整链接 | 原始分类链接URL | https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops |
| 分类路径 | 从URL提取的分类路径 | women-women-clothes-tank-tops |
| 一级分类 | 解析得到的一级分类 | Women |
| 二级分类 | 解析得到的二级分类 | Tank Tops |
| 域名 | 网站域名 | lulumonclick-eu.shop |

## 文件结构
```
category-link-collector/
├── SKILL.md                    # 技能主文档
├── README.md                   # 本文件
├── scripts/
│   └── collect_categories.py   # 主采集脚本
├── config/
│   └── settings.json          # 配置文件
├── examples/
│   └── usage.md               # 使用示例
└── tests/
    └── test_collector.py      # 单元测试
```

## 配置选项
在 `config/settings.json` 中可以配置：
- `default_output_dir`: 默认输出目录
- `csv_encoding`: CSV文件编码
- `include_timestamp`: 是否包含时间戳
- `auto_create_dir`: 是否自动创建目录
- `log_level`: 日志级别

## 扩展能力
这个skill可以扩展以下功能：
1. **批量处理**: 支持从文件读取大量链接
2. **多级分类**: 支持三级、四级等更深层级的分类
3. **数据验证**: 验证链接格式和分类结构
4. **去重功能**: 自动去重相同的分类
5. **状态跟踪**: 记录采集状态和时间
6. **错误处理**: 更好的错误处理和重试机制
7. **API集成**: 集成到其他系统或工作流中

## 测试
运行测试确保功能正常：
```bash
cd tests
python3 -m unittest test_collector.py
```

## 注意事项
1. 确保输出目录有写入权限
2. 链接格式需要符合 `/collections/分类路径` 的格式
3. 分类路径解析基于连字符(`-`)分割
4. 二级分类提取逻辑可能需要根据具体网站调整

## 贡献
欢迎提交Issue和Pull Request来改进这个skill！