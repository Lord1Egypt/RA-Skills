# Skill Evaluator 测试夹具

本目录包含用于测试的 Skill 样本。

## 目录结构

```
fixtures/
├── README.md                    # 本文件
├── level1-skill/                # Level 1 Skill 样本（基础可用）
│   └── SKILL.md
├── level2-skill/                # Level 2 Skill 样本（稳定可靠）
│   ├── SKILL.md
│   ├── scripts/
│   │   └── main.py
│   └── evals/
│       └── skill-eval-config.yaml
└── level3-skill/                # Level 3 Skill 样本（生产就绪）
    ├── SKILL.md
    ├── README.md
    ├── scripts/
    │   └── main.py
    ├── evals/
    │   └── skill-eval-config.yaml
    ├── tests/
    │   ├── test_normal.py
    │   └── test_edge_cases.py
    └── .feedback/
        └── feedback-log.md
```

## 使用方式

在测试中引用：

```python
from scripts.evaluate import check_skill_structure, calculate_skill_level

# 测试 Level 3 Skill 结构
result = check_skill_structure("tests/fixtures/level3-skill")
assert result["has_skill_md"] == True
assert result["has_scripts"] == True
assert result["has_evals"] == True
assert result["has_tests"] == True
assert result["has_readme"] == True

# 测试 Level 3 判定
level = calculate_skill_level(result, {})
assert level == "Level 3"
```

## 运行测试

```bash
cd $OPENCLAW_ROOT/skills/skill-evaluator
pytest tests/test_evaluator.py -v --cov=scripts --cov-report=term-missing
```
