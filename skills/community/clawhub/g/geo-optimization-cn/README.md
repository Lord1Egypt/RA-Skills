# 企业营销内容生成器

企业营销内容智能生成器，支持生成搜索词、问答词、GEO优化QA知识库和企业信息提取。

## 安装依赖

```bash
uv tool install markitdown
pip install python-docx
```

## 使用方法

### 1. 生成搜索词

```bash
python3 scripts/business_content_generator.py search "公司名称" "行业"
```

### 2. 生成问答词

```bash
python3 scripts/business_content_generator.py qa "公司名称" "行业"
```

### 3. 生成QA知识库

```bash
python3 scripts/business_content_generator.py kb ./公司资料.docx
```

### 4. 提取企业信息

```bash
python3 scripts/business_content_generator.py extract ./公司资料.docx
```

## 支持行业

- 科技/互联网
- 制造业
- 教育培训
- 医疗健康
- 金融服务
- 电商零售
- 餐饮服务
- 房地产
- 咨询服务
- 物流运输

## 输出格式

### QA知识库
- 纯Q&A格式
- 无分类标题
- 无问题编号
- 无关键词标注
- 无版本/日期/工具信息

### 企业信息
- 纯文本格式
- 无表格
- 无标题页
- 无版本/日期/工具信息
- 7大章节 + 附录

## 文件说明

- `scripts/business_content_generator.py` - 主程序
- `scripts/convert_to_word.py` - Markdown转Word工具
- `SKILL.md` - 详细使用文档
- `quickref.md` - 快速参考
