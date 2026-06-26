# arXiv Paper Resolver - 使用示例

## 快速使用

### 方式一：命令行直接运行

```bash
# 通过 arXiv ID
python3 arxiv_section_extractor.py 2604.25405

# 通过完整 URL
python3 arxiv_section_extractor.py https://arxiv.org/abs/2604.25405

# 自定义输出目录
python3 arxiv_section_extractor.py 2604.25405 -o ./my_papers
```

### 方式二：通过 Python 导入使用（TODO）

```python
from arxiv_section_extractor import extract_arxiv_id, get_paper_info_from_abs

arxiv_id = extract_arxiv_id("https://arxiv.org/abs/2604.25836")
title, links = get_paper_info_from_abs(arxiv_id)
print(f"论文: {title}")
```

## 输出示例

```text
============================================================
arXiv 论文提取器
论文 ID: 2604.25405
============================================================

[1/5] 获取论文信息...
  标题: Leveraging Previous-Traversal Point Cloud Map Priors for Camera-Based 3D Object Detection and Tracking
  PDF:  https://arxiv.org/pdf/2604.25405
  HTML: https://arxiv.org/html/2604.25405v1
  TeX:  https://arxiv.org/src/2604.25405

[2/5] 创建目录...
  目录: /home/user/papers/leveraging-previous-traversal-point-cloud-map-priors/

[3/5] 下载 PDF...
  PDF 已下载: .../2604.25405.pdf (1824 KB)

[4/5] 获取 HTML 实验版全文...
  HTML 获取成功: https://arxiv.org/html/2604.25405v1 (50219 字符)

[5/5] 解析章节结构...
  共解析出 6 个章节
  章节已保存: 01_Introduction.txt (1240 字符)
  章节已保存: 02_Related_Work.txt (980 字符)
  ...

============================================================
提取完成！
============================================================
论文: Leveraging Previous-Traversal Point Cloud Map Priors ...
目录: /home/user/papers/leveraging-previous-traversal-.../
PDF:  /home/user/papers/leveraging-previous-traversal-.../2604.25405.pdf
章节数: 6

章节结构:
  1. I Introduction
  2. II Related Work
  3. III Technical Approach
      - A. Multi-Model Motion Estimation
      - B. Motion-State-Driven Cascade Association
  4. IV Experimental Evaluation
  5. V Discussion
  6. VI Conclusion
```

## 常见问题

**Q: 为什么 PDF 下载失败？**
A: 检查网络连接，确认 arXiv 服务器可用。PDF 下载失败不影响章节提取。

**Q: 为什么 HTML 解析失败？**
A: arXiv 可能更新了 HTML 格式，需要更新脚本中的解析逻辑。可提交 Issue。

**Q: 如何修改输出目录？**
A: 使用 `-o` 参数或设置 `ARXIV_PAPERS_DIR` 环境变量。

**Q: 如何批量解析多篇论文？**
A: 可以写一个循环脚本调用 extractor，或提交 PR 添加批量支持。
