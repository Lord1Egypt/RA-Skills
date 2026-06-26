# Level 3 测试 Skill

这是 Level 3 Skill 的测试样本，用于测试 skill-evaluator 的评估功能。

## 特点

- ✅ 完整的 SKILL.md
- ✅ scripts/ 目录
- ✅ evals/ 目录
- ✅ tests/ 目录
- ✅ README.md
- ✅ 用户反馈循环
- ✅ 版本管理记录

## 使用方法

```bash
# 运行评估
python scripts/score.py --skill-path tests/fixtures/level3-skill --output reports/

# 运行测试
pytest tests/fixtures/level3-skill/tests/ -v

# 运行基准测试
promptfoo eval -c tests/fixtures/level3-skill/evals/skill-eval-config.yaml
```

## 预期评估结果

- 能力等级：Level 3
- 准确性：> 95%
- 可靠性：> 97%
- 测试覆盖率：> 95%
