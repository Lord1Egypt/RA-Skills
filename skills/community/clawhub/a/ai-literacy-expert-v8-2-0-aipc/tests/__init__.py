"""
tests/ - ai-literacy-expert-V8.1-AIPC 单元测试套件（≈ 141 项 · 8 文件）

覆盖范围（合计 ≈ 141 项）：
  - pii_redactor (test_all.py):              9 项
      · L1 姓名（单姓 + 复姓 2 项）
      · L2 身份证（18 位 + 15 位 + 中文上下文，2 项）
      · L3 手机号（中文上下文）
      · L4 家庭住址
      · 递归脱敏（redact_abstract_data）
      · 5% 抽样审计 pass + fail（2 项）
  - edge_cloud_dispatch (test_edge_cloud.py): 6 项
      · build_request 结构 + validate + missing_field（3 项）
      · degradation 状态机 NPU 不可用 → Level 4 + NPU 可用 → Level 1（2 项）
      · PII 脱敏集成（exchange 流程）
  - lesson_plan_guard (test_guard_cost.py):    5 项
      · G001 知识点不足触发 + 充足通过（2 项）
      · G007 英文术语通过 + 非法动词触发（2 项）
      · G008 成本熔断拒绝
  - cost_monitor (test_guard_cost.py):         3 项
      · record_cost 累计 + alert_level 阈值（none/warning_50/warning_80/critical_100 共 1 项）+ 状态持久化
  - select_knowledge (test_pipeline.py):       4 项
      · extract_keywords（中文 bigram + 英文 token，2 项）
      · score_segment（关键词命中 + 负面词惩罚，2 项）
  - compose_lesson (test_pipeline.py):         2 项
      · render_markdown（含版本号 v8-aipc 断言）+ render_assessment
  - analyze_courseware (test_pipeline.py):     1 项
      · mock_analyze_segment（知识点标签 + 难度 1~5）
  - skill_runtime (test_pipeline.py):          1 项
      · python_version_supported（3.10~3.12 通过 / 3.8~3.9 拒绝）
  - work_summary (test_work_summary.py):       12 项
      · V7-AIPC 每次工作后本地 vs 云端对比
  - v7.3.2 改进 (test_v732_improvements.py):  23 项
      · V7.3.2 5 项改进（多 provider / timeout 拆分 / 硬件探测 / LLM 缓存 / degradation 上报）
  - p5.js 按钮完整性 (test_p5js_buttons.py):  29 项
      · V8-AIPC：每个 button 必须实际可用（B1-B9 强制门控）
  - p5.js 全互动控件 (test_p5js_interactive.py): 36 项
      · V8.1-AIPC 新增：每个 button/slider/select/input/canvas/key/touch/drag 必须实际可用
      · ButtonRegistry 解析器 5 项 + B1-B7 + 控件 S/Se/I/C/K/T/D 系列 + 集成报告

版本说明：
  本套件随 V7.3.0 引入，V7.3.1 / V7.3.2 / V7-AIPC / V8-AIPC 持续扩充；
  V8.1-AIPC（8.1.0-aipc）新增 test_p5js_interactive.py（36 项）+ 整合 work_summary 12 项。
  历史：
    V7.2 → 23 项
    V7.3 → 33 项
    V7-AIPC (7.4.0-aipc) → 72 项
    V8-AIPC (8.0.0-aipc) → ≈ 105 项（+29 按钮门控）
    V8.1-AIPC (8.1.0-aipc) → ≈ 141 项（+36 互动控件门控）
  注：上述计数是该目录中实际 def test_ 数量；不计入 __init__ 与辅助类。

V8.1-AIPC 关键新增：
  - 每个 p5.js 课件 / 游戏必须在 HTML 注释中声明 [INTERACTIVE_REGISTRY]（或继续用 V8-AIPC 的 [BUTTON_REGISTRY]）。
  - 自动化测试分两套独立运行：
    · tests/test_p5js_buttons.py（V8-AIPC 29 项）—— 按钮 9 项门控
    · tests/test_p5js_interactive.py（V8.1-AIPC 36 项）—— 8 类 27 项全控件门控
  - 任一控件 B/S/Se/I/C/K/T/D 不通过 = 课件/游戏不得交付。
  - 详见 references/p5js-courseware-guide.md 第三章·二 与 references/p5js-game-design-guide.md 第七章·五·5。

运行：
    cd <SKILL_DIR>
    # 全部
    python -m unittest discover -s tests -v
    # 仅 V8.1-AIPC 互动控件门控
    python -m unittest tests.test_p5js_interactive -v
    # 仅 V8-AIPC 按钮门控
    python -m unittest tests.test_p5js_buttons -v
    # 两者一起跑
    python -m unittest tests.test_p5js_buttons tests.test_p5js_interactive -v
"""
