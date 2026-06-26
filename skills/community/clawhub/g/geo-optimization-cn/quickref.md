# 企业营销内容生成器 - 快速参考

## 安装依赖

```bash
uv tool install markitdown
pip install python-docx
```

---

## 快速使用

### 1. 生成搜索词（前缀5个 + 后缀5个）

```bash
python business_content_generator.py search "粤腊煌食品有限公司" "餐饮"
```

### 2. 生成问答词（15个）

```bash
python business_content_generator.py qa "粤腊煌食品有限公司" "餐饮"
```

### 3. Word → QA知识库

```bash
# 生成提示词（复制给Claude）
python business_content_generator.py kb ./公司资料.docx

# Claude生成内容后，保存为 .md 文件，然后转换为Word
python convert_to_word.py QA知识库.md QA知识库.docx
```

### 4. Word → 企业信息提取

```bash
# 生成提示词（复制给Claude）
python business_content_generator.py extract ./公司资料.docx

# Claude生成内容后，保存为 .md 文件，然后转换为Word
python convert_to_word.py 企业信息.md 企业信息.docx
```

---

## 完整工作流程示例

```bash
# 1. 生成搜索词和问答词
python business_content_generator.py search "小米科技" "互联网"
python business_content_generator.py qa "小米科技" "互联网"

# 2. 准备Word资料（公司介绍.docx）

# 3. 生成QA知识库
python business_content_generator.py kb ./公司介绍.docx
# → 复制输出的提示词给Claude
# → Claude生成QA内容
# → 保存为 QA.md
python convert_to_word.py QA.md QA.docx

# 4. 提取企业信息
python business_content_generator.py extract ./公司介绍.docx
# → 复制输出的提示词给Claude
# → Claude生成企业信息
# → 保存为 信息.md
python convert_to_word.py 信息.md 信息.docx
```

---

## 输出格式说明

### QA知识库格式

```markdown
### 问题1？

答案内容...

---

### 问题2？

答案内容...

---
```

**特点：**
- 纯Q&A，无分类标题
- 无问题编号（Q1, Q2）
- 无关键词标注
- 无版本/日期/工具信息

### 企业信息格式

```markdown
## 一、公司名称

工商全称：XXX
常用简称/品牌名：XXX

---

## 二、公司及业务范围介绍

企业核心简介：...

主营业务范围：
- XXX
- XXX

...
```

**特点：**
- 纯文本，无表格
- 7大章节 + 附录
- 无标题页
- 无版本/日期/工具信息

---

## 支持行业

| 行业 | 关键词 |
|------|--------|
| 科技/互联网 | 互联网、软件、IT |
| 制造业 | 制造、工厂、生产 |
| 教育培训 | 教育、培训、学校 |
| 医疗健康 | 医疗、健康、医院 |
| 金融服务 | 金融、银行、保险 |
| 电商零售 | 电商、零售 |
| 餐饮服务 | 餐饮、美食、餐厅 |
| 房地产 | 房地产、房产、地产 |
| 咨询服务 | 咨询、顾问 |
| 物流运输 | 物流、快递、运输 |

---

## 文件结构

```
business-content-generator/
├── SKILL.md                    # 详细使用文档
├── business_content_generator.py  # 主程序
├── convert_to_word.py          # Markdown转Word工具
└── quickref.md                 # 本快速参考
```

---

## 常见问题

**Q: 读取Word失败？**  
A: 确保安装了 `markitdown`: `uv tool install markitdown`

**Q: 生成Word失败？**  
A: 确保安装了 `python-docx`: `pip install python-docx`

**Q: 行业不匹配？**  
A: 尝试使用不同的行业关键词，如"食品"、"批发"等

**Q: 如何修改输出格式？**  
A: 编辑主程序中的提示词模板（`generate_kb_prompt` 和 `generate_extract_prompt` 函数）
