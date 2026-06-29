# arXiv 论文翻译技能指南

## 工具链

### 1. Crossref API（优先）
```bash
curl -s "https://api.crossref.org/works/https://doi.org/10.48550/arXiv.XXXXXXX"
```
返回：title, authors, abstract, DOI, date

### 2. arXiv API
```bash
curl -s "http://export.arxiv.org/api/query?id_list=XXXXXXX"
```
返回：元数据 + 摘要（Atom XML格式）

### 3. 网页内容获取
- 摘要页：`https://arxiv.org/abs/XXXXXXX`
- HTML全文：`https://arxiv.org/html/XXXXXXX`（部分论文有）
- PDF：`https://arxiv.org/abs/XXXXXXX`（需pdfplumber/PyPDF2解析）
- Google Scholar缓存

### 4. 网络搜索（Tavily）
```bash
tavily_search query="paper title" count=5
tavily_extract urls=["https://arxiv.org/abs/XXXXXXX"]
```

## ID提取规则

| 输入 | 提取ID |
|------|--------|
| `https://arxiv.org/abs/2301.00001` | `2301.00001` |
| `https://arxiv.org/pdf/2301.00001` | `2301.00001` |
| `https://arxiv.org/html/2301.00001` | `2301.00001` |
| `2301.00001` | `2301.00001` |

## PDF内容解析

```python
import pdfplumber

with pdfplumber.open("paper.pdf") as pdf:
    text = "\n".join([page.extract_text() for page in pdf.pages])
```

## 翻译规范

### 标题
- 英文标题作为一级标题
- 中文翻译作为二级标题
- 格式：`# 英文标题\n## 中文标题`

### 摘要翻译
- 保留 DOI 和 arXiv ID
- 专业术语首次出现附英文原词
- 公式符号保留英文

### 常见术语对照

| 英文 | 中文 |
|------|------|
| object detection | 目标检测 |
| mean Average Precision (mAP) | 平均精度均值 |
| precision/recall | 精确率/召回率 |
| lightweight | 轻量化 |
| backbone | 主干网络 |
| feature pyramid | 特征金字塔 |
| attention mechanism | 注意力机制 |
| bounding box | 边界框 |
| transfer learning | 迁移学习 |
| domain adaptation | 域适应 |
| few-shot/zero-shot | 少样本/零样本 |
| state-of-the-art (SOTA) | 最先进 |
| intersection over union (IoU) | 交并比 |
|非极大值抑制（NMS）|

## 常见问题处理

### 403/Access Denied
→ 使用网络搜索 + Tavily extract + Crossref API 多源拼合

### PDF无法下载
→ 先尝试HTML版本：`/html/`
→ 再尝试网络搜索找其他镜像

### 内容缺失
→ Crossref获取摘要后，用网络搜索补充论文详情
→ 查找同作者的其他论文作为上下文参考

## 完整翻译流程检查清单

- [ ] 识别arXiv ID
- [ ] 确认论文语言（全英文/含其他语言）
- [ ] 通过最优方案获取摘要/全文
- [ ] 提取作者信息
- [ ] 翻译摘要（保留专业术语英文原词）
- [ ] 提炼核心贡献点
- [ ] 解析方法核心创新
- [ ] 整理实验数据表格
- [ ] 翻译结论
- [ ] 添加说明注释
- [ ] 格式检查