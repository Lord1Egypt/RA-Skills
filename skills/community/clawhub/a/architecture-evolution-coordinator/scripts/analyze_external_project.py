#!/usr/bin/env python3
"""
分析外部项目，作为理念级进化试点
支持GitHub项目URL分析
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.parse

def fetch_github_readme(repo_url):
    """
    获取GitHub仓库的README内容
    
    Args:
        repo_url: GitHub仓库URL，如 https://github.com/WeberG619/neveronce
    
    Returns:
        README内容字典
    """
    # 从URL提取用户和仓库名
    match = re.match(r'https?://github\.com/([^/]+)/([^/]+)', repo_url)
    if not match:
        raise ValueError(f"无效的GitHub URL: {repo_url}")
    
    user, repo = match.groups()
    
    # 尝试获取README（多种可能的文件名）
    readme_files = ['README.md', 'README.rst', 'README.txt', 'README']
    api_base = f"https://api.github.com/repos/{user}/{repo}/contents"
    
    for readme_file in readme_files:
        try:
            api_url = f"{api_base}/{readme_file}"
            req = urllib.request.Request(api_url)
            req.add_header('User-Agent', 'architecture-evolution-coordinator/1.0.0')
            
            # 如果有GitHub token，添加认证头
            github_token = os.environ.get('GITHUB_TOKEN')
            if github_token:
                req.add_header('Authorization', f'token {github_token}')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                if 'content' in data:
                    # Base64解码内容
                    import base64
                    content = base64.b64decode(data['content']).decode('utf-8')
                    return {
                        "success": True,
                        "repo": f"{user}/{repo}",
                        "readme_file": readme_file,
                        "content": content,
                        "size": len(content),
                        "url": repo_url
                    }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue  # 尝试下一个README文件
            else:
                return {
                    "success": False,
                    "error": f"HTTP错误 {e.code}: {e.reason}",
                    "url": repo_url
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": repo_url
            }
    
    return {
        "success": False,
        "error": "未找到README文件",
        "url": repo_url
    }

def extract_key_concepts(readme_content):
    """
    从README中提取关键概念
    
    Args:
        readme_content: README内容
    
    Returns:
        提取的概念列表
    """
    concepts = []
    
    # 提取项目描述
    description_patterns = [
        r'#+\s+(.*?)\n',  # 标题
        r'Description:?\s*(.*?)\n',  # 描述
        r'##+\s+Overview\s*\n(.*?)\n##',  # 概述部分
    ]
    
    for pattern in description_patterns:
        matches = re.findall(pattern, readme_content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            concepts.append({
                "type": "description",
                "content": match.strip(),
                "source": "readme"
            })
    
    # 提取关键特性
    feature_sections = re.findall(r'##+\s+(?:Features?|特性)\s*\n(.*?)(?=\n##|\Z)', 
                                 readme_content, re.DOTALL | re.IGNORECASE)
    
    for section in feature_sections:
        # 提取列表项
        items = re.findall(r'[-*]\s+(.*?)(?=\n[-*]|\n\n|\Z)', section, re.DOTALL)
        for item in items:
            concepts.append({
                "type": "feature",
                "content": item.strip(),
                "source": "readme_features"
            })
    
    # 提取技术关键词
    tech_keywords = [
        "memory", "learning", "AI", "persistent", "correctable", 
        "forgetting", "reinforcement", "neural", "vector", "embedding",
        "database", "storage", "retrieval", "search", "index"
    ]
    
    found_keywords = []
    for keyword in tech_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', readme_content, re.IGNORECASE):
            found_keywords.append(keyword)
    
    if found_keywords:
        concepts.append({
            "type": "tech_keywords",
            "content": ", ".join(found_keywords),
            "source": "keyword_scan"
        })
    
    return concepts

def map_to_existing_architecture(concepts):
    """
    将提取的概念映射到现有星型记忆架构
    
    Args:
        concepts: 提取的概念列表
    
    Returns:
        映射结果
    """
    # 现有插件功能类型映射
    plugin_mapping = {
        "memory": ["memory-integration", "semantic-vector-store", "co-occurrence-engine"],
        "learning": ["learning-coordinator", "correction-logger", "preference-tracker"],
        "forgetting": ["forgetting-curve"],
        "storage": ["ontology-storage", "memory-integration"],
        "retrieval": ["unified-query-gateway", "enhanced-search-service", "graph-query"],
        "monitoring": ["evolution-watcher", "heartbeat-manager"],
        "optimization": ["execution-optimizer", "constraint-validator", "rule-ranker"]
    }
    
    mappings = []
    
    for concept in concepts:
        concept_text = concept["content"].lower()
        matched_plugins = []
        
        for category, plugins in plugin_mapping.items():
            if re.search(r'\b' + re.escape(category) + r'\b', concept_text):
                matched_plugins.extend(plugins)
        
        # 去重
        matched_plugins = list(set(matched_plugins))
        
        if matched_plugins:
            mappings.append({
                "concept": concept["content"],
                "concept_type": concept["type"],
                "matched_plugins": matched_plugins,
                "mapping_confidence": "high" if len(matched_plugins) > 0 else "low"
            })
    
    return mappings

def generate_fusion_proposal(repo_info, concepts, mappings):
    """
    生成融合方案建议
    
    Args:
        repo_info: 仓库信息
        concepts: 提取的概念
        mappings: 架构映射
    
    Returns:
        融合方案
    """
    proposal = {
        "project": repo_info.get("repo", "unknown"),
        "analysis_date": datetime.now().isoformat(),
        "summary": "",
        "fusion_opportunities": [],
        "new_plugin_candidates": [],
        "existing_plugin_enhancements": [],
        "implementation_priority": "medium"
    }
    
    # 生成摘要
    description_concepts = [c for c in concepts if c["type"] == "description"]
    if description_concepts:
        proposal["summary"] = description_concepts[0]["content"][:200] + "..."
    
    # 识别融合机会
    unique_plugins = set()
    for mapping in mappings:
        for plugin in mapping["matched_plugins"]:
            unique_plugins.add(plugin)
    
    for plugin in unique_plugins:
        # 检查是否是现有插件
        plugin_path = Path(f"/root/.openclaw/workspace/skills/{plugin}")
        if plugin_path.exists():
            proposal["existing_plugin_enhancements"].append({
                "plugin": plugin,
                "enhancement_type": "feature_addition",
                "rationale": f"外部项目包含与{plugin}相关的功能概念",
                "priority": "medium"
            })
        else:
            # 可能是新插件候选
            proposal["new_plugin_candidates"].append({
                "name": plugin,
                "type": "conceptual",  # 仅概念，尚未实现
                "rationale": "从外部项目概念中识别出的潜在新功能",
                "feasibility": "requires_analysis"
            })
    
    # 基于映射生成具体机会
    feature_concepts = [c for c in concepts if c["type"] == "feature"]
    for i, concept in enumerate(feature_concepts[:5]):  # 限制前5个特性
        proposal["fusion_opportunities"].append({
            "id": f"opportunity_{i+1}",
            "external_feature": concept["content"],
            "potential_integration": "new_algorithm" if "algorithm" in concept["content"].lower() else "feature_extension",
            "estimated_effort": "medium",
            "potential_impact": "improves_existing_capability"
        })
    
    return proposal

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="分析外部项目作为理念级进化试点")
    parser.add_argument("url", help="GitHub项目URL")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--format", "-f", choices=["json", "markdown", "text"], default="markdown")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔍 理念级进化试点 - 外部项目分析")
    print("=" * 60)
    
    print(f"\n📋 分析项目: {args.url}")
    
    # 获取README
    print("📖 获取项目信息...")
    repo_info = fetch_github_readme(args.url)
    
    if not repo_info["success"]:
        print(f"❌ 获取项目信息失败: {repo_info.get('error', '未知错误')}")
        sys.exit(1)
    
    print(f"✅ 成功获取README: {repo_info['readme_file']} ({repo_info['size']} 字符)")
    
    # 提取关键概念
    print("\n🔧 提取关键概念...")
    concepts = extract_key_concepts(repo_info["content"])
    print(f"✅ 提取到 {len(concepts)} 个关键概念")
    
    if args.verbose:
        for i, concept in enumerate(concepts[:10]):  # 限制显示前10个
            print(f"  {i+1}. [{concept['type']}] {concept['content'][:80]}...")
    
    # 映射到现有架构
    print("\n🗺️  映射到星型记忆架构...")
    mappings = map_to_existing_architecture(concepts)
    print(f"✅ 生成 {len(mappings)} 个架构映射")
    
    if args.verbose:
        for mapping in mappings[:5]:  # 限制显示前5个映射
            print(f"  概念: {mapping['concept'][:60]}...")
            print(f"    匹配插件: {', '.join(mapping['matched_plugins'][:3])}")
    
    # 生成融合方案
    print("\n💡 生成融合方案...")
    proposal = generate_fusion_proposal(repo_info, concepts, mappings)
    
    # 输出结果
    if args.output:
        output_path = Path(args.output)
        if args.format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "repo_info": repo_info,
                    "concepts": concepts,
                    "mappings": mappings,
                    "proposal": proposal
                }, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON输出已保存: {output_path}")
        elif args.format == "markdown":
            markdown_content = generate_markdown_report(repo_info, concepts, mappings, proposal)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✅ Markdown报告已保存: {output_path}")
    else:
        # 控制台输出
        print("\n" + "=" * 60)
        print("📋 分析报告摘要")
        print("=" * 60)
        
        print(f"\n📊 项目: {proposal['project']}")
        print(f"📅 分析日期: {proposal['analysis_date']}")
        
        if proposal['summary']:
            print(f"\n📝 项目摘要: {proposal['summary']}")
        
        print(f"\n🔌 现有插件增强建议 ({len(proposal['existing_plugin_enhancements'])} 个):")
        for enhancement in proposal['existing_plugin_enhancements'][:5]:
            print(f"  • {enhancement['plugin']}: {enhancement['rationale']}")
        
        print(f"\n🆕 新插件候选 ({len(proposal['new_plugin_candidates'])} 个):")
        for candidate in proposal['new_plugin_candidates'][:5]:
            print(f"  • {candidate['name']}: {candidate['rationale']}")
        
        print(f"\n🎯 融合机会 ({len(proposal['fusion_opportunities'])} 个):")
        for opportunity in proposal['fusion_opportunities'][:5]:
            print(f"  • {opportunity['external_feature'][:60]}...")
            print(f"    类型: {opportunity['potential_integration']}, 预估工作量: {opportunity['estimated_effort']}")
        
        print(f"\n📈 实施优先级: {proposal['implementation_priority']}")
    
    print("\n" + "=" * 60)
    print("✅ 理念级分析完成")
    print("=" * 60)

def generate_markdown_report(repo_info, concepts, mappings, proposal):
    """生成Markdown格式报告"""
    report = []
    
    report.append(f"# 理念级进化分析报告: {repo_info['repo']}")
    report.append(f"**分析日期**: {proposal['analysis_date']}")
    report.append(f"**项目URL**: {repo_info['url']}")
    report.append("")
    
    report.append("## 📋 项目摘要")
    if proposal['summary']:
        report.append(proposal['summary'])
    else:
        report.append("*(无可用摘要)*")
    report.append("")
    
    report.append("## 🔍 关键概念提取")
    report.append(f"提取到 {len(concepts)} 个关键概念:")
    
    concept_types = {}
    for concept in concepts:
        concept_types[concept['type']] = concept_types.get(concept['type'], 0) + 1
    
    for ctype, count in concept_types.items():
        report.append(f"- **{ctype}**: {count} 个")
    
    # 显示部分概念示例
    report.append("\n**概念示例**:")
    for i, concept in enumerate(concepts[:10]):
        report.append(f"{i+1}. `{concept['type']}`: {concept['content'][:100]}...")
    report.append("")
    
    report.append("## 🗺️  架构映射")
    report.append(f"生成 {len(mappings)} 个架构映射:")
    
    for i, mapping in enumerate(mappings[:10]):
        report.append(f"\n### 映射 {i+1}")
        report.append(f"**概念**: {mapping['concept']}")
        report.append(f"**匹配插件**: {', '.join(mapping['matched_plugins'])}")
        report.append(f"**置信度**: {mapping['mapping_confidence']}")
    report.append("")
    
    report.append("## 💡 融合方案建议")
    
    report.append("### 🔌 现有插件增强")
    if proposal['existing_plugin_enhancements']:
        for enhancement in proposal['existing_plugin_enhancements']:
            report.append(f"- **{enhancement['plugin']}**")
            report.append(f"  - 增强类型: {enhancement['enhancement_type']}")
            report.append(f"  - 理由: {enhancement['rationale']}")
            report.append(f"  - 优先级: {enhancement['priority']}")
    else:
        report.append("*(无现有插件增强建议)*")
    report.append("")
    
    report.append("### 🆕 新插件候选")
    if proposal['new_plugin_candidates']:
        for candidate in proposal['new_plugin_candidates']:
            report.append(f"- **{candidate['name']}**")
            report.append(f"  - 类型: {candidate['type']}")
            report.append(f"  - 理由: {candidate['rationale']}")
            report.append(f"  - 可行性: {candidate['feasibility']}")
    else:
        report.append("*(无新插件候选)*")
    report.append("")
    
    report.append("### 🎯 具体融合机会")
    if proposal['fusion_opportunities']:
        for opportunity in proposal['fusion_opportunities']:
            report.append(f"#### {opportunity['id']}")
            report.append(f"- **外部特性**: {opportunity['external_feature']}")
            report.append(f"- **集成类型**: {opportunity['potential_integration']}")
            report.append(f"- **预估工作量**: {opportunity['estimated_effort']}")
            report.append(f"- **潜在影响**: {opportunity['potential_impact']}")
    else:
        report.append("*(无具体融合机会)*")
    report.append("")
    
    report.append("## 📈 实施建议")
    report.append(f"**总体优先级**: {proposal['implementation_priority']}")
    report.append("")
    report.append("### 推荐执行顺序:")
    report.append("1. 评估高置信度映射的可行性")
    report.append("2. 对现有插件增强进行沙盒测试")
    report.append("3. 设计新插件原型（如适用）")
    report.append("4. 集成测试验证")
    report.append("5. 用户确认后部署")
    
    report.append("\n---")
    report.append("*本报告由架构演进协调器自动生成，仅供参考。*")
    report.append("*具体实施前需进行详细技术评估和沙盒验证。*")
    
    return "\n".join(report)

if __name__ == "__main__":
    main()