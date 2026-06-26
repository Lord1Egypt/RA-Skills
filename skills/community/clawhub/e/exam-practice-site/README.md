# 考试刷题网站生成器 (exam-practice-site)

> 一个数据驱动的考试刷题网站框架，只需替换题库即可适配任何考试。

## 适用场景

- 考研（管综、英语、政治、数学等）
- 公务员考试（行测、申论）
- 司法考试 / 法考
- CPA / 会计职称
- 教师资格证
- 医学考试
- 任何有题库的标准化考试

## 核心功能

- **每日抽题**：自动从题库随机抽取，去重不重复
- **答题判分**：在线作答，自动批改，显示解析
- **错题本**：自动收录错题，支持分类筛选和重新作答
- **周报分析**：错题类型分布图表 + 针对性复习建议
- **纯静态部署**：单页 HTML + JSON 数据驱动，无需后端

## 快速开始

1. 复制 `assets/template.html` 为 `index.html`，修改考试名称和题型分类
2. 构建 `data/questions/bank.json` 题库
3. 复制 `scripts/update_daily.py` 到项目根目录
4. 运行 `python3 update_daily.py` 生成今日题目
5. 启动本地服务器：`python3 -m http.server 8080`

## 目录结构

```
project/
├── index.html              # 主应用
├── update_daily.py         # 每日题目更新脚本
└── data/questions/
    ├── bank.json           # 题库（需按考试定制）
    ├── today.json          # 今日题目（自动生成）
    └── used_ids.json       # 已出题目记录（自动维护）
```

## 题库格式

```json
{
  "questions": [
    {
      "id": "2024-01",
      "type": "single_choice",
      "category": "分类-子分类",
      "source": "2024年真题·第1题",
      "question": "题目正文",
      "options": ["A. 选项A", "B. 选项B", "C. 选项C", "D. 选项D"],
      "answer": "A",
      "explanation": "解析内容"
    }
  ]
}
```

## License

MIT
