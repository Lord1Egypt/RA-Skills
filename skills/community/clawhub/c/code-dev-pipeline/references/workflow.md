# 完整执行流程（含代码）

本文档包含完整的执行流程代码，供 Coordinator 参考。

## 主循环结构

```python
# ========== 初始化 ==========
project_name = "my-project"
current_version = "v0.0"
tech_debt_list = []
iteration_history = []

while True:  # 主循环，直到 Coordinator 决定结束
    
    # ========== Phase 0: Coordinator 协调决策 ==========
    coordinator_task = f"""
    你是协调员（Coordinator）。
    请阅读 references/coordinator.md 了解输出格式。
    
    【当前状态】
    项目: {project_name}
    当前版本: {current_version}
    技术债务清单: {tech_debt_list}
    历史迭代: {iteration_history}
    
    【上一轮验收报告】
    {validation_report if iteration_history else "首次启动，无上一轮报告"}
    
    【用户输入】
    {user_input if user_input else "等待 Coordinator 决策"}
    
    请做出决策：【启动新一轮迭代】/【直接交付】/【结束项目】
    如启动迭代，请输出完整的"迭代需求单"。
    """
    
    coordinator_result = spawn("coordinator", coordinator_task)
    
    # 解析 Coordinator 决策
    if "【结束项目】" in coordinator_result:
        output_project_summary(coordinator_result)
        break  # 退出主循环
    
    if "【直接交付】" in coordinator_result:
        output_delivery_summary(coordinator_result)
        wait_for_user_new_input()
        continue
    
    # 提取迭代需求单
    iteration_req = extract_iteration_requirement(coordinator_result)
    current_version = bump_version(current_version)
    
    # ========== Phase 1-6: 六人协作流水线 ==========
    MAX_ITERATIONS = 5
    iteration = 0
    code_accepted = False
    
    while not code_accepted and iteration < MAX_ITERATIONS:
        iteration += 1
        
        # Step 1: Analyst 需求分析
        analyst_task = f"""
        你是需求分析师（Analyst）。
        请阅读 references/analyst.md 了解输出格式。
        基于以下迭代需求单，输出结构化需求文档。
        
        【迭代需求单】
        {iteration_req}
        """
        requirements = spawn("analyst", analyst_task)
        
        # Step 2: Architect 架构设计
        architect_task = f"""
        你是架构师（Architect）。
        请阅读 references/architect.md 了解输出格式。
        基于需求文档，设计系统架构。
        
        【需求文档】
        {requirements}
        """
        architecture = spawn("architect", architect_task)
        
        # Step 3: Coder 代码编写
        coder_task = f"""
        你是代码编写员（Coder）。
        请阅读 references/coder.md 了解输出格式。
        基于需求和架构，编写完整可运行代码。
        {"【这是第" + str(iteration) + "轮迭代】" if iteration > 1 else ""}
        
        【需求文档】
        {requirements}
        
        【架构设计】
        {architecture}
        """
        code = spawn("coder", coder_task)
        
        # Step 4: Reviewer 代码审查
        reviewer_task = f"""
        你是代码审查员（Reviewer）。
        请阅读 references/reviewer.md 了解输出格式。
        必须输出第一行：【通过】或【不通过】
        如不通过，必须给出结构化修复清单。
        
        【需求】{requirements}
        【架构】{architecture}
        【代码】{code}
        """
        review_report = spawn("reviewer", reviewer_task)
        
        if "【不通过】" in review_report:
            if iteration < MAX_ITERATIONS:
                continue  # 打回修改
            else:
                tech_debt_list.append(create_tech_debt("review", review_report))
        
        # Step 5: Tester 测试验证
        tester_task = f"""
        你是测试验证员（Tester）。
        请阅读 references/tester.md 了解输出格式。
        必须输出第一行：【通过】或【发现bug】
        如发现bug，必须给出详细bug报告和修复清单。
        
        【需求】{requirements}
        【代码】{code}
        """
        test_report = spawn("tester", tester_task)
        
        if "【发现bug】" in test_report or "【不通过】" in test_report:
            if iteration < MAX_ITERATIONS:
                continue  # 打回修复
            else:
                tech_debt_list.append(create_tech_debt("test", test_report))
        
        code_accepted = True
    
    # Step 6: Validator 最终验收
    validator_task = f"""
    你是最终验收员（Validator）。
    请阅读 references/validator.md 了解输出格式。
    必须输出第一行：【通过】或【不通过】
    如不通过，给出返工要求；如通过，给出交付建议。
    必须列出所有技术债务。
    
    【需求】{requirements}
    【架构】{architecture}
    【代码】{code}
    【审查报告】{review_report}
    【测试报告】{test_report}
    【技术债务清单】{tech_debt_list}
    """
    validation_report = spawn("validator", validator_task)
    
    # 保存本轮产出到知识库
    save_to_knowledge_base(
        project=project_name,
        version=current_version,
        artifacts={
            "01-requirements.md": requirements,
            "02-architecture.md": architecture,
            "03-code.py": code,
            "04-review.md": review_report,
            "05-test.md": test_report,
            "06-validation.md": validation_report,
            "07-coordinator.md": coordinator_result
        }
    )
    
    # 更新技术债务（Validator 可能新增）
    if "【不通过】" in validation_report:
        tech_debt_list.append(create_tech_debt("validation", validation_report))
    
    iteration_history.append({
        "version": current_version,
        "iteration_count": iteration,
        "tech_debts": len(tech_debt_list),
        "validation": "通过" if "【通过】" in validation_report else "不通过"
    })
    
    # 自动回到 Coordinator（闭环）
    continue
```

## 辅助函数

```python
def bump_version(version: str) -> str:
    """版本号递增"""
    # v1.0 -> v1.1, v1.9 -> v2.0
    major, minor = version.replace("v", "").split(".")
    if int(minor) >= 9:
        return f"v{int(major) + 1}.0"
    return f"v{major}.{int(minor) + 1}"

def create_tech_debt(source: str, report: str) -> dict:
    """创建技术债务条目"""
    return {
        "id": f"TD-{len(tech_debt_list) + 1:03d}",
        "source": source,
        "description": extract_issues(report),
        "created_at": datetime.now(),
        "priority": assess_priority(report)
    }

def save_to_knowledge_base(project: str, version: str, artifacts: dict):
    """保存产出到知识库"""
    base_path = f"projects/{project}/{version}"
    os.makedirs(base_path, exist_ok=True)
    
    for filename, content in artifacts.items():
        with open(f"{base_path}/{filename}", "w") as f:
            f.write(content)
    
    # 更新 current 软链接
    current_link = f"projects/{project}/current"
    if os.path.islink(current_link):
        os.remove(current_link)
    os.symlink(version, current_link)
```

## 目录结构

```
projects/
└── {project-name}/
    ├── v1.0/
    │   ├── 01-requirements.md
    │   ├── 02-architecture.md
    │   ├── 03-code.py
    │   ├── 04-review.md
    │   ├── 05-test.md
    │   ├── 06-validation.md
    │   └── 07-coordinator.md
    ├── v1.1/
    ├── tech-debt.md
    ├── coordinator-log.md
    └── current -> v1.1
```
