---
name: AdvancedMLClassificationSkill
description: 自动化生成工业级机器学习分类算法代码、调用算法做预测、输出准确率对比和可视化结果，支持新手友好的结果解读。
---

# AdvancedMLClassificationSkill

## 输入参数

- `data_path: str`（必填）CSV 数据集路径
- `target_col: str`（必填）预测目标列名
- `algorithms: list[str]`（可选）默认 `[
  "逻辑回归", "决策树", "随机森林", "XGBoost", "LightGBM"
]`
- `test_size: float`（可选）默认 `0.2`
- `random_state: int`（可选）默认 `42`

## 输出结构

- `accuracy_results: dict[str, float|None]`
- `interpretation: str`
- `generated_codes: dict[str, str]`
- `visualization_data: dict`

## 关键流程

1. 自动预处理（缺失值、类别编码、数值标准化）
2. 按算法生成训练代码（优先 `code-davinci-002`，失败回退本地模板）
3. 执行算法代码并统计准确率（失败时返回具体错误）
4. 可选交叉验证（`StratifiedKFold`/`KFold`/`RepeatedStratifiedKFold`）
5. 可选参数搜索（`GridSearchCV`/`RandomizedSearchCV`）
6. 生成置换特征重要性排序（默认对最佳算法）
7. 生成新手友好中文解读（优先 `gpt-3.5-turbo`）
8. 输出可视化数据（柱状图/折线图）

## 运行示例

```bash
cd /Users/bamboo/skills/advanced-ml-classification-skill/scripts
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_complex_demo.py
python advanced_ml_skill.py --data-path ./demo_complex.csv --target-col target_label --enable-cv --enable-search
streamlit run app.py
```
