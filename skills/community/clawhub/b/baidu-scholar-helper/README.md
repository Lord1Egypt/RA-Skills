# 学术科研助手

一个强大的学术论文搜索和下载工具，支持百度学术和arXiv。

## 功能特性

- 🔍 **多平台搜索**：支持百度学术和arXiv
- 📊 **智能排序**：百度学术按引用量排序，arXiv按相关度排序
- 🧠 **自动分析**：提取论文核心工作和创新点
- 🖼️ **模型图显示**：自动识别并显示论文中的模型图
- 📥 **PDF自动下载**：按论文方向分类保存到 `~/Desktop/papers/`
- 📝 **规范命名**：`标题_年份_J/C.pdf`（J=期刊，C=会议）
- arXiv预印本也按此格式命名

## 使用方法

### 命令行

```bash
# 百度学术搜索
python scripts/search.py baidu 大模型
python scripts/search.py baidu 人工智能 2026

# arXiv搜索
python scripts/search.py arxiv transformer
python scripts/search.py arxiv "deep learning" 5
```

### 对话方式

```
用户：百度学术搜索 大模型
用户：arXiv GPT 5
```

## 文件结构

```
baidu-scholar-helper/
├── SKILL.md           # 技能说明
├── skill.json         # 技能配置
├── requirements.txt   # Python依赖
└── scripts/
    ├── main.py        # 百度学术搜索
    ├── arxiv_search_v2.py  # arXiv搜索
    └── search.py      # 统一入口
```

## PDF保存位置

所有PDF保存在：`~/Desktop/papers/<论文方向>/`

每次搜索会自动创建以关键词命名的文件夹，方便管理。

## 注意事项

1. 百度学术可能触发验证码拦截
2. arXiv API有速率限制（已内置重试机制）
3. 请用于学术研究，尊重版权
