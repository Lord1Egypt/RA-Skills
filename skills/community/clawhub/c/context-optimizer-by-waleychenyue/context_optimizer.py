        report.append(f"工作空间: {self.workspace_path}")
        report.append("")
        
        # 总体统计
        report.append("## 总体统计")
        report.append(f"- 分析文件数: {analysis_results.get('files_analyzed', 0)}")
        report.append(f"- 原始token估算: {analysis_results.get('total_original_tokens', 0):,}")
        report.append(f"- 优化后token估算: {analysis_results.get('total_potential_tokens', 0):,}")
        report.append(f"- 总体节省潜力: {analysis_results.get('overall_reduction_percent', 0)}%")
        report.append("")
        
        # 文件详细分析
        report.append("## 文件分析详情")
        for filename, analysis in analysis_results.get("file_analyses", {}).items():
            if "error" not in analysis:
                report.append(f"### {filename}")
                report.append(f"  - 大小: {analysis.get('size_chars', 0):,} 字符")
                report.append(f"  - Token估算: {analysis.get('size_tokens', 0):,}")
                report.append(f"  - 优化分数: {analysis.get('overall_score', 0)}/100")
                
                # Skill提取潜力
                skill_pot = analysis.get('optimization_potential', {}).get('skill_extraction', {})
                if skill_pot.get('score', 0) > 30:
                    report.append(f"  - Skill提取: {skill_pot.get('recommendation', '')}")
        
        # 优化结果（如果有）
        if optimization_results:
            report.append("")
            report.append("## 优化执行结果")
            total_reduction = 0
            file_count = 0
            
            for result in optimization_results:
                if result.get("status") == "success":
                    report.append(f"- {result['filename']}: 减少 {result['reduction_percent']}%")
                    total_reduction += result['reduction_percent']
                    file_count += 1
            
            if file_count > 0:
                avg_reduction = total_reduction / file_count
                report.append(f"平均减少: {avg_reduction:.1f}%")
        
        # 建议
        report.append("")
        report.append("## 优化建议")
        for i, rec in enumerate(analysis_results.get("recommendations", []), 1):
            report.append(f"{i}. {rec}")
        
        report.append("")
        report.append("## 后续步骤")
        report.append("1. 执行优化命令: `python context_optimizer.py optimize`")
        report.append("2. 提取高价值Skill: `python context_optimizer.py extract-skill`")
        report.append("3. 配置自动优化: 编辑context_optimizer_config.json")
        
        report.append("=" * 60)
        
        return "\n".join(report)

def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python context_optimizer.py <命令> [参数]")
        print("命令:")
        print("  analyze - 分析工作空间优化潜力")
        print("  optimize [文件] - 优化指定文件或所有文件")
        print("  extract-skill <技能名> <类型> - 提取内容为Skill")
        print("  config - 显示当前配置")
        print("  report - 生成优化报告")
        return
    
    optimizer = ContextOptimizer()
    command = sys.argv[1]
    
    if command == "analyze":
        print("正在分析工作空间...")
        results = optimizer.analyze_workspace()
        report = optimizer.generate_report(results)
        print(report)
        
        # 保存分析结果
        report_file = os.path.join(optimizer.workspace_path, "context_optimization_report.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n详细报告已保存: {report_file}")
    
    elif command == "optimize":
        files_to_optimize = []
        
        if len(sys.argv) > 2:
            # 优化指定文件
            file_arg = sys.argv[2]
            if file_arg == "all":
                files_to_optimize = ["AGENTS.md", "SOUL.md", "MEMORY.md", "HEARTBEAT.md"]
            else:
                files_to_optimize = [file_arg]
        else:
            # 交互式选择
            print("选择要优化的文件:")
            print("1. AGENTS.md")
            print("2. SOUL.md")
            print("3. MEMORY.md")
            print("4. HEARTBEAT.md")
            print("5. 所有文件")
            
            choice = input("输入选择 (1-5): ").strip()
            choices_map = {
                "1": ["AGENTS.md"],
                "2": ["SOUL.md"],
                "3": ["MEMORY.md"],
                "4": ["HEARTBEAT.md"],
                "5": ["AGENTS.md", "SOUL.md", "MEMORY.md", "HEARTBEAT.md"]
            }
            
            files_to_optimize = choices_map.get(choice, [])
        
        if not files_to_optimize:
            print("未选择文件")
            return
        
        print(f"开始优化 {len(files_to_optimize)} 个文件...")
        results = []
        
        for filename in files_to_optimize:
            filepath = os.path.join(optimizer.workspace_path, filename)
            if os.path.exists(filepath):
                print(f"优化 {filename}...")
                result = optimizer.optimize_file(filepath)
                results.append(result)
                
                if result.get("status") == "success":
                    print(f"  ✅ 完成: 减少 {result['reduction_percent']}%")
                else:
                    print(f"  ❌ 失败: {result.get('error', '未知错误')}")
            else:
                print(f"  ⚠️ 文件不存在: {filename}")
        
        # 生成优化后分析
        print("\n优化完成，重新分析工作空间...")
        analysis = optimizer.analyze_workspace()
        report = optimizer.generate_report(analysis, results)
        print(report)
    
    elif command == "extract-skill" and len(sys.argv) >= 3:
        skill_name = sys.argv[2]
        skill_type = sys.argv[3] if len(sys.argv) > 3 else None
        
        print(f"提取Skill: {skill_name} (类型: {skill_type or '通用'})")
        
        # 选择源文件
        print("选择源文件:")
        print("1. AGENTS.md - 工作空间指南")
        print("2. SOUL.md - 身份定义和协调者框架")
        print("3. MEMORY.md - 文档模板和报告格式")
        
        choice = input("输入选择 (1-3): ").strip()
        file_map = {
            "1": "AGENTS.md",
            "2": "SOUL.md",
            "3": "MEMORY.md"
        }
        
        source_file = file_map.get(choice)
        if not source_file:
            print("无效选择")
            return
        
        filepath = os.path.join(optimizer.workspace_path, source_file)
        result = optimizer.extract_skill(filepath, skill_name, skill_type)
        
        if result.get("status") == "success":
            print(f"✅ Skill创建成功: {result['skill_path']}")
            print(f"   文件: {result['skill_file']}")
        else:
            print(f"❌ Skill创建失败: {result.get('error', '未知错误')}")
    
    elif command == "config":
        print("当前配置:")
        print(json.dumps(optimizer.config, indent=2, ensure_ascii=False))
    
    elif command == "report":
        results = optimizer.analyze_workspace()
        report = optimizer.generate_report(results)
        print(report)
    
    else:
        print("无效的命令或参数")

if __name__ == "__main__":
    main()