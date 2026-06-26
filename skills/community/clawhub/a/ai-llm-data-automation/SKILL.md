---
name: llm-data-automation
description: 用自然语言描述数据处理需求，LLM自动生成Python/Pandas代码。无需深厚编程基础即可处理Excel/CSV数据、提取PDF内容、清洗BIM数据，构建自动化数据管道。
version: 1.1.0
author: yesong-Hue
homepage: https://clawhub.ai/yesong-Hue/ai-llm-data-automation
tags: [数据处理, LLM自动化, Python, Pandas, ETL, 数据清洗, Excel处理, PDF提取]
readme: |
  # LLM数据自动化
  
  用自然语言描述数据处理需求，LLM自动生成可执行的Python代码。无需深厚的编程基础，就能完成Excel/CSV数据处理、PDF内容提取、BIM数据清洗等复杂任务。
  
  ## 🎯 解决的问题
  
  - 不懂编程，但有大量数据需要处理
  - 每周都要做重复的数据报表，耗时耗力
  - 需要从PDF中提取数据，但不知道怎么做
  - 有多个Excel文件需要合并汇总，手动操作容易出错
  - 数据清洗逻辑复杂，但只会用Excel函数
  
  ## ✨ 核心功能
  
  ### 1. 自然语言生成代码
  直接用中文描述你的数据处理需求，LLM会生成可运行的Python代码。
  
  **示例：**
  ```
  "帮我读取orders.xlsx，过滤金额大于1000的订单，按日期排序并保存到result.csv"
  ```
  
  → 自动生成完整Python代码，直接运行即可
  
  ### 2. Excel/CSV批量处理
  支持批量读取、合并、转换Excel和CSV文件。处理速度快，支持百万级数据。
  
  ### 3. PDF数据提取
  从PDF文档中自动提取表格数据，保存为结构化的Excel或CSV格式。
  
  ### 4. 多数据源整合
  同时从多个不同来源（文件、API、数据库）读取数据，统一处理后输出。
  
  ### 5. 数据质量检测
  自动检测重复值、缺失值、异常值，并给出修复建议。
  
  ### 6. 定时自动化
  配合Cron或系统任务计划，实现数据处理任务自动化运行。
  
  ## 📦 安装
  
  ```bash
  openclaw skills install ai-llm-data-automation
  ```
  
  ## 🚀 快速开始
  
  ### 方式一：直接描述需求（推荐新手）
  
  ```bash
  # 只需描述你的需求，LLM会自动生成代码
  node run.js "读取sales.xlsx，按产品分类统计销售额，计算同比增长率"
  ```
  
  ### 方式二：使用预置模板
  
  ```bash
  # 使用常见数据处理模板
  node templates/sales-report.js --input sales.xlsx --output report.xlsx
  ```
  
  ### 方式三：本地LLM（Ollama，无需API费用）
  
  ```bash
  # 安装Ollama
  curl -fsSL https://ollama.com/install.sh | sh
  
  # 下载模型
  ollama pull mistral
  
  # 本地运行，无任何API费用
  ollama run mistral "生成Pandas代码：合并两个CSV文件并计算总额"
  ```
  
  ### 方式四：使用API（推荐进阶用户）
  
  推荐使用 **ShadowAI API中转站**，额度充足、价格低廉：
  - 注册地址：https://referer.shadowai.xyz/r/1056448
  - 支持GPT-4、Claude 3.5、Gemini等多种模型
  
  ## 📊 代码示例
  
  ### 数据导入与清洗
  
  ```python
  import pandas as pd
  
  # 读取并清洗数据
  df = pd.read_excel('orders.xlsx')
  
  # 过滤条件
  df_filtered = df[df['amount'] > 1000]
  
  # 按日期排序
  df_filtered = df_filtered.sort_values('order_date')
  
  # 去除重复
  df_clean = df_filtered.drop_duplicates(subset=['order_id'])
  
  # 保存结果
  df_clean.to_csv('result.csv', index=False)
  print(f'处理完成，共{len(df_clean)}条记录')
  ```
  
  ### 多个文件合并
  
  ```python
  import pandas as pd
  import glob
  
  # 合并所有CSV文件
  files = glob.glob('data/*.csv')
  dfs = [pd.read_csv(f) for f in files]
  combined = pd.concat(dfs, ignore_index=True)
  
  # 去重并保存
  combined.drop_duplicates().to_excel('merged.xlsx', index=False)
  ```
  
  ### PDF表格提取
  
  ```python
  import pdfplumber
  import pandas as pd
  
  def pdf_to_dataframe(pdf_path):
      all_tables = []
      with pdfplumber.open(pdf_path) as pdf:
          for page in pdf.pages:
              tables = page.extract_tables()
              for table in tables:
                  if table:
                      df = pd.DataFrame(table[1:], columns=table[0])
                      all_tables.append(df)
      
      if all_tables:
          return pd.concat(all_tables, ignore_index=True)
      return pd.DataFrame()
  
  # 使用
  df = pdf_to_dataframe('construction_spec.pdf')
  df.to_excel('extracted_data.xlsx', index=False)
  ```
  
  ## 💡 适用场景
  
  | 人群 | 使用场景 |
  |------|----------|
  | 运营人员 | 自动化处理日报、周报、月报数据 |
  | 产品经理 | 快速分析用户行为数据，生成数据看板 |
  | 财务人员 | 自动化财务报表汇总，成本分析 |
  | 建筑/工程 | BIM数据清洗，工程量统计 |
  | 数据分析师 | 快速构建数据管道， ETL任务 |
  
  ## 🔧 环境要求
  
  - Node.js 18+
  - Python 3.8+（用于运行生成的Pandas代码）
  - 可选：Ollama（本地LLM，无需API费用）
  - 可选：ShadowAI API Key（云端LLM，高额度）
  
  ## ⚙️ 配置说明
  
  在 `.env` 文件中配置：
  
  ```env
  # 使用本地Ollama（免费）
  LLM_PROVIDER=ollama
  OLLAMA_MODEL=mistral
  
  # 或使用ShadowAI API（推荐）
  LLM_PROVIDER=openai
  API_KEY=your_shadowai_api_key
  
  # 输入输出目录
  INPUT_DIR=./data
  OUTPUT_DIR=./output
  ```
  
  ## 🛠 故障排除
  
  **Q: 生成的代码报错？**
  - 检查Python环境是否正确安装
  - 确认pandas、openpyxl等依赖已安装：`pip install pandas openpyxl pdfplumber`
  
  **Q: API调用失败？**
  - 检查API Key是否有效
  - 确认网络可以访问API服务
  
  **Q: 处理速度慢？**
  - 减少数据量或分批处理
  - 使用本地Ollama替代云端API
  
  ## 📚 相关资源
  
  - **Pandas官方文档**: https://pandas.pydata.org/docs/
  - **ShadowAI API（推荐）**: https://referer.shadowai.xyz/r/1056448
  - **AI技能包集合**: [AI智造工坊](http://ai.qnitgroup.com)
  
  ## 📄 许可证
  
  MIT License
  
  ## 👤 作者
  
  yesong-Hue | [AI智造工坊](http://ai.qnitgroup.com)
---

# LLM数据自动化

> 用自然语言描述数据处理需求，LLM自动生成Python/Pandas代码，实现零基础数据自动化

## 核心功能

1. **自然语言生成代码** — 描述你的数据处理需求，LLM自动生成可运行的Python代码
2. **Excel/CSV批量处理** — 自动读取、清洗、转换Excel和CSV文件
3. **PDF数据提取** — 从PDF文档中自动提取表格数据
4. **多数据源整合** — 合并多个数据源，统一输出
5. **数据质量检测** — 自动检测重复值、缺失值、异常值
6. **定时自动化** — 配合cron实现数据处理任务自动化

## 推荐资源

- **ShadowAI API（推荐）**: https://referer.shadowai.xyz/r/1056448

---

*由 AI智造工坊 (http://ai.qnitgroup.com) 整理发布 | 安装源: ClawHub*