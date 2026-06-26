#!/usr/bin/env python3
"""
Security Scanner CLI v6.2.0 - 统一架构版

三层检测架构:
1. PatternEngine (Layer 1) - Aho-Corasick 快速预筛选
2. HybridRuleEngine (Layer 2) - AC 自动机 + Regex 精匹配
3. LLMEngine (Layer 3, 可选) - 语义分析

检测流程:
1. Layer 1 快速匹配 → 返回候选攻击类型
2. Layer 2 只匹配候选类型的规则子集 → 大幅减少匹配次数
3. Layer 3 可选 LLM 复核 CRITICAL 级别
"""

import argparse
import json
import sys
import os
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import Dict, List

# 添加 src 路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent))

# 导入三层架构引擎
from engines import PatternEngine, RuleEngine, LLMEngine
from engines.hybrid_scanner_v2 import TwoLayerACScanner
from engines.composite_detector import CompositeDetector
from whitelist_filter import WhitelistFilter
from config_detector import ConfigFileDetector
from security_tool_detector import SecurityToolDetector
from context_aware_filter import ContextAwareFilter
from curl_risk_classifier import CurlRiskClassifier, get_curl_classifier
from credential_theft_classifier import CredentialTheftClassifier, get_credential_classifier, generate_credential_report
from risk_tier_classifier import RiskTierClassifier, get_risk_tier_classifier, RISK_TIER_INFO

# 全局组件
# 全局组合检测器 (延迟初始化)
_composite_detector = None

def get_composite_detector():
    """获取或初始化组合检测器"""
    global _composite_detector
    if _composite_detector is None:
        _composite_detector = CompositeDetector()
    return _composite_detector

def _extract_yaml_payload(content: str) -> str:
    """从 YAML 文件中提取 payload 字段，避免 metadata 污染。
    
    如果无法解析或没有 payload 字段，返回原始内容。
    """
    try:
        import yaml
        doc = yaml.safe_load(content)
        if isinstance(doc, dict) and 'payload' in doc:
            payload = doc['payload']
            if isinstance(payload, str) and payload.strip():
                return payload
    except Exception:
        pass
    return content

whitelist_filter = WhitelistFilter()
config_detector = ConfigFileDetector()
security_tool_detector = SecurityToolDetector()
context_filter = ContextAwareFilter()

# ========== v6.2.0 优化:文件优先级配置 ==========
# 优先级数字越小越优先,timeout 为单文件超时预算 (秒)
FILE_PRIORITY_RULES = {
    # P0 - 必须扫描 (技能定义)
    'skill.md': (0, 10),

    # P1 - 核心工具代码
    '_tools.py': (1, 8),
    'tool_': (1, 8),
    'agent': (1, 8),
    'skill.py': (1, 8),
    'main.py': (1, 8),
    'handler': (1, 8),

    # P2 - 高风险关键词
    'inject': (2, 5),
    'hack': (2, 5),
    'bypass': (2, 5),
    'exploit': (2, 5),
    'subprocess': (2, 5),
    'eval': (2, 5),
    'exec': (2, 5),

    # P3 - 网络/凭据
    'request': (3, 5),
    'http': (3, 5),
    'curl': (3, 5),
    'api_key': (3, 5),
    'token': (3, 5),
    'secret': (3, 5),

    # P4 - 普通代码
    '.py': (4, 3),
    '.js': (4, 3),
    '.sh': (4, 3),
    '.bash': (4, 3),

    # P5 - 配置文件（放宽超时到 5 秒）
    '.yaml': (5, 5),
    '.yml': (5, 5),
    '.json': (5, 5),
    '.toml': (5, 5),
    
    # P6 - 文档 (最低优先级，严格熔断)
    'readme': (6, 1),
    'license': (6, 1),
    'changelog': (6, 1),
    'contributing': (6, 1),
    '.md': (6, 1),  # 所有 markdown 文件 1s 熔断
}

def get_file_priority(filepath: Path):
    """获取文件优先级 (priority, timeout)"""
    name_lower = filepath.name.lower()
    suffix = filepath.suffix.lower()

    # 检查精确匹配
    for pattern, (priority, timeout) in FILE_PRIORITY_RULES.items():
        if pattern.startswith('.'):
            # 后缀匹配
            if suffix == pattern:
                return priority, timeout
        elif pattern.endswith('.py') or pattern.endswith('.sh'):
            # 后缀模式
            if name_lower.endswith(pattern):
                return priority, timeout
        elif '*' in pattern:
            # 通配符
            if pattern.replace('*', '') in name_lower:
                return priority, timeout
        else:
            # 关键词/前缀匹配
            if pattern in name_lower or name_lower.startswith(pattern):
                return priority, timeout

    # 默认
    if suffix in {'.py', '.js', '.sh'}:
        return 4, 3
    elif suffix in {'.yaml', '.yml', '.json'}:
        return 5, 2
    else:
        return 6, 1


def create_scanner(args):
    """
    创建扫描器(统一三层架构 - 分层 AC)
    """
    rules_file = Path(__file__).parent / 'rules' / 'dist' / 'all_rules.json'

    # Layer 1: Pattern Engine (可选,用于兼容性)
    print("\n🔧 初始化 Layer 1: PatternEngine (兼容性保留)...")
    layer1 = PatternEngine()

    # Layer 2: TwoLayerACScanner (核心) - 分层 AC 自动机
    print("\n🔧 初始化 Layer 2: TwoLayerACScanner (分层 AC)...")
    layer2 = TwoLayerACScanner(rules_file=rules_file)

    # Layer 3: LLM Engine (可选)
    layer3 = None
    if args.llm:
        print(f"\n🤖 启用 Layer 3: LLMEngine (模型:{args.llm_model})")
        llm_config = {
            'model': args.llm_model,
            'api_key': args.llm_api_key or os.environ.get('LLM_API_KEY', ''),
            'threshold': args.llm_threshold
        }
        layer3 = LLMEngine(llm_config)

    return {
        'layer1': layer1,
        'layer2': layer2,
        'layer3': layer3
    }


def scan_file_with_timeout(file_path: Path, scanner, max_depth: int = -1, timeout_per_file: float = 3.0) -> dict:
    """扫描单个文件 (带超时控制 - 记录但不跳过)"""
    start_time = time.time()
    timed_out = False

    try:
        # 读取文件
        content = file_path.read_text(encoding='utf-8', errors='ignore')

        # 检查读取是否超时
        if time.time() - start_time > timeout_per_file:
            timed_out = True  # 记录超时,但继续扫描

        # 执行扫描
        result = scan_file(file_path, scanner, max_depth)
        result['priority'], result['timeout_budget'] = get_file_priority(file_path)
        result['scan_time'] = time.time() - start_time
        result['timed_out'] = timed_out
        return result

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'file': str(file_path),
            'error': str(e),
            'priority': get_file_priority(file_path)[0],
            'timeout_budget': timeout_per_file,
            'scan_time': elapsed,
            'timed_out': elapsed > timeout_per_file,
            'detected': False
        }


def scan_file(file_path: Path, scanner, max_depth: int = -1) -> dict:
    # 跳过元数据文件
    if file_path.name in ('metadata.json', 'metadata.yml', 'metadata.yaml', 
                          'samples_index.json', 'invalid_samples.json'):
        return {
            'file': str(file_path),
            'detected': False,
            'score': 0,
            'findings_count': 0,
            'risk_level': 'SAFE',
            'matched_rules': [],
            'whitelist_applied': False,
            'is_config_file': False,
            'skipped_metadata': True
        }
    
    """扫描单个文件 (支持三层架构 + 白名单过滤)"""
    try:
        # 检查目录深度
        if max_depth > 0:
            try:
                depth = len(file_path.relative_to(Path(scanner['base_path'])).parts)
                if depth > max_depth:
                    return {'file': str(file_path), 'skipped': 'max_depth'}
            except (ValueError, KeyError):
                pass

        # 读取文件内容
        content = file_path.read_text(encoding='utf-8', errors='ignore')

        # v6.2.1 修复: YAML 样本文件只扫描 payload 字段，忽略 metadata 污染
        if file_path.suffix in ('.yaml', '.yml'):
            content = _extract_yaml_payload(content)

        # 配置文件识别 (v6.1.0 新增)
        file_type, config_risk = config_detector.classify_file(str(file_path), content)
        if file_type == 'config':
            if config_risk == 'malicious':
                return {
                    'file': str(file_path),
                    'detected': True,
                    'score': 80,
                    'findings_count': 1,
                    'risk_level': 'HIGH',
                    'matched_rules': ['CONFIG-MALICIOUS'],
                    'whitelist_applied': False,
                    'is_config_file': True
                }
            else:
                return {
                    'file': str(file_path),
                    'detected': False,
                    'score': 0,
                    'findings_count': 0,
                    'risk_level': 'SAFE',
                    'matched_rules': [],
                    'whitelist_applied': False,
                    'is_config_file': True
                }

        # 三层架构扫描
        # Layer 1: Pattern Engine (保留用于兼容性)
        layer1_result = scanner['layer1'].scan(content, str(file_path))

        # Layer 2: TwoLayerACScanner (分层 AC - 核心)
        layer2_result = scanner['layer2'].scan(content)

        # Layer 3: LLM Engine (可选) - 只复核 CRITICAL 级别
        layer3_result = None
        if scanner['layer3'] and layer2_result.get('hit_count', 0) > 0:
            if layer2_result.get('risk_level') == 'CRITICAL':
                layer3_result = scanner['layer3'].scan(content, layer1_result, layer2_result)

        # 合并结果
        result = {
            'layer1': layer1_result,
            'layer2': layer2_result,
            'layer3': layer3_result,
            'hit_count': layer2_result.get('hit_count', 0),
            'matches': layer2_result.get('matches', []),
            'score': layer2_result.get('score', 0),
            'risk_level': layer2_result.get('risk_level', 'SAFE')
        }

        # 白名单过滤
        layer2_hit_count = layer2_result.get('hit_count', 0)
        layer2_avg_conf = layer2_result.get('avg_confidence', 0)
        layer2_confirmed = layer2_result.get('confirmed_rule_ids', [])
        
        # P0 修复：保护高置信度检测不被 whitelist 误杀
        # 阈值：hit_count >= 3 && avg_conf >= 75 => 强制保留
        is_protected = layer2_hit_count >= 3 and layer2_avg_conf >= 75
        
        if result.get('matches'):
            # 检查是否是 benign/template/test 文件
            is_benign_file = (
                whitelist_filter.is_template_file(str(file_path), content) or
                whitelist_filter.is_test_file(str(file_path), content) or
                whitelist_filter.is_benign_path(str(file_path)) or
                whitelist_filter.is_benign_code(content) or
                whitelist_filter.uses_only_safe_calls(content)
            )
            
            filtered = whitelist_filter.filter_results(
                result['matches'],
                str(file_path),
                content
            )
            # P0 修复：保护高置信度检测不被 whitelist 误杀
            # 但不适用于 benign/template/test 文件
            if (is_protected and len(filtered) == 0 and len(layer2_confirmed) >= 3 and not is_benign_file):
                # whitelist 误杀了真实威胁，恢复 layer2 的 confirmed_rule_ids 作为证据
                result['matches'] = layer2_result.get('matches', [])[:3]  # 取前 3 条高置信规则
                result['protection_note'] = 'P0: 高置信度检测保护生效'
            else:
                result['matches'] = filtered
            result['hit_count'] = len(result['matches'])
            result['whitelist_applied'] = True
            
            # Bug 修复: whitelist 过滤后 matches 为空时，risk_level 必须同步降级
            if len(result['matches']) == 0:
                result['risk_level'] = 'SAFE'
                result['score'] = 0

        # ========== v6.2.1: 组合检测 (Plan A - 组合检测) ==========
        # 目标: 提升 credential_theft (346 rules, 153 missed) 和 resource_exhaustion (106 rules, 86 missed)
        # 方法: 组合多个弱信号检测复杂攻击模式
        composite_detector = get_composite_detector()
        composite_matches = composite_detector.scan(content, str(file_path))
        
        if composite_matches:
            # 合并组合检测结果
            composite_findings = []
            composite_categories = set()
            max_composite_score = 0
            
            for cm in composite_matches:
                composite_findings.append({
                    'rule_id': f'COMPOSITE-{cm.category.upper()}',
                    'name': cm.description,
                    'category': cm.category,
                    'score': cm.score,
                    'confidence': cm.confidence,
                    'severity': cm.severity,
                    'matched_indicators': cm.matched_indicators,
                    'is_composite': True
                })
                composite_categories.add(cm.category)
                max_composite_score = max(max_composite_score, cm.score)
            
            # v6.2.1 修复: 组合检测不能独立判定，必须配合规则引擎
            # 防止 API 客户端工具等良性代码被误报
            # 组合检测只用于提升已有检出文件的分数，不用于新增检出
            composite_threshold = 80  # 提高到 80，更严格
            if max_composite_score >= composite_threshold and result.get('detected', False):
                # 规则引擎已检出，composite 提升分数
                if max_composite_score > result.get('score', 0):
                    result['score'] = max_composite_score
                    result['risk_level'] = 'CRITICAL' if max_composite_score >= 80 else 'HIGH'
            
            # 合并 findings
            result['composite_findings'] = composite_findings
            result['composite_categories'] = list(composite_categories)
            result['composite_hit_count'] = len(composite_matches)
            
            # 增加命中数 (组合检测贡献)
            result['hit_count'] = result.get('hit_count', 0) + len(composite_findings)


        # v6.2.0: 上下文感知过滤
        original_risk = result.get('risk_level', 'SAFE')
        if result.get('hit_count', 0) > 0:
            context = context_filter.analyze_context(content)
            if context['context_score'] >= 0.3:
                adjusted_risk, reason = context_filter.should_downgrade_risk(
                    context, original_risk
                )
                result['risk_level'] = adjusted_risk
                result['context_score'] = context['context_score']
                result['context_reason'] = reason
                
                # 调整分数
                if adjusted_risk != original_risk:
                    score_reduction = {
                        'CRITICAL': 0.6,
                        'HIGH': 0.7,
                        'MEDIUM': 0.8,
                        'LOW': 0.9,
                        'SAFE': 1.0
                    }.get(adjusted_risk, 1.0)
                    result['score'] = int(result.get('score', 0) * score_reduction)

        # ========== v6.2.0: Curl 风险分级分类 ==========
        # 用户需求: curl 命令分级判定
        # HIGH: 远程执行 + 未知域名 + 混淆
        # MEDIUM: 静默执行 / 非标准动作 / 隐藏输出
        # LOW: 常见操作 + 透明
        curl_classifier = get_curl_classifier()
        curl_results = curl_classifier.classify_curl(content)
        if curl_results:
            # 获取最高风险
            highest_curl = curl_results[0]  # 已按风险排序
            
            # 构建 curl 特有 findings
            curl_findings = []
            for cr in curl_results:
                curl_findings.append({
                    'rule_id': f'CURL-{cr.level}-{cr.pattern}',
                    'name': f'Curl风险: {cr.pattern}',
                    'category': 'network_curl',
                    'score': {'HIGH': 85, 'MEDIUM': 50, 'LOW': 20}.get(cr.level, 10),
                    'confidence': 90,
                    'severity': cr.level,
                    'reason': cr.reason,
                    'snippet': cr.matched_content[:100],
                    'is_curl': True
                })
            
            # 合并到 result
            if 'composite_findings' not in result:
                result['composite_findings'] = []
            result['composite_findings'].extend(curl_findings)
            result['curl_findings'] = curl_findings
            result['curl_risk_level'] = highest_curl.level
            
            # 如果 curl 风险高于当前评估，提升风险等级
            curl_score = {'HIGH': 85, 'MEDIUM': 50, 'LOW': 20}.get(highest_curl.level, 10)
            if curl_score > result.get('score', 0):
                result['score'] = curl_score
                if highest_curl.level == 'HIGH' and result.get('risk_level') not in ['CRITICAL', 'HIGH']:
                    result['risk_level'] = 'HIGH'
                elif highest_curl.level == 'MEDIUM' and result.get('risk_level') == 'SAFE':
                    result['risk_level'] = 'MEDIUM'
            
            result['hit_count'] = result.get('hit_count', 0) + len(curl_findings)

        # ========== v6.2.0: 凭据窃取风险分级 ==========
        # 检测完整的凭据窃取攻击链：诱导→混淆→外发
        cred_classifier = get_credential_classifier()
        cred_results = cred_classifier.classify_credential_behavior(content)
        if cred_results:
            highest_cred = cred_results[0]
            
            # 构建凭据特有 findings
            cred_findings = []
            for cr in cred_results:
                cred_findings.append({
                    'rule_id': f'CRED-{cr.level.name}-{cr.pattern}',
                    'name': f'凭据风险: {cr.pattern}',
                    'category': 'credential_theft',
                    'score': min(cr.confidence * cr.level.value, 100),
                    'confidence': cr.confidence,
                    'severity': cr.level.name,
                    'reason': cr.reason,
                    'snippet': cr.matched_content[:100],
                    'attack_chain': cr.attack_chain,
                    'is_credential': True
                })
            
            # 合并到 result
            if 'composite_findings' not in result:
                result['composite_findings'] = []
            result['composite_findings'].extend(cred_findings)
            result['cred_findings'] = cred_findings
            result['cred_risk_level'] = highest_cred.level.name
            
            # 如果凭据风险高于当前评估，提升风险等级
            cred_score = {'CRITICAL': 95, 'HIGH': 85, 'MEDIUM': 50, 'LOW': 25}.get(highest_cred.level.name, 10)
            if cred_score > result.get('score', 0):
                result['score'] = cred_score
                if highest_cred.level.name in ['CRITICAL', 'HIGH'] and result.get('risk_level') not in ['CRITICAL', 'HIGH']:
                    result['risk_level'] = highest_cred.level.name
            
            result['hit_count'] = result.get('hit_count', 0) + len(cred_findings)

        # 转换为统一格式
        detected = result.get('hit_count', 0) > 0

        # ========== v6.2.0: 风险分级报告 ==========
        tier_classifier = get_risk_tier_classifier()
        tier_report = tier_classifier.generate_risk_report(result)

        return {
            'file': str(file_path),
            'detected': detected,
            'score': result.get('score', 0),
            'findings_count': result.get('hit_count', 0),
            'risk_level': result.get('risk_level', 'SAFE'),
            'matched_rules': list(set([m[0] if isinstance(m, tuple) else m.get('rule_id', m.get('pattern', '')) for m in result.get('matches', [])[:5]])),
            'whitelist_applied': result.get('whitelist_applied', False),
            'is_config_file': False,
            'layer1_result': layer1_result,
            'layer2_result': layer2_result,
            'layer3_llm': layer3_result,
            'composite_findings': result.get('composite_findings', []),
            'composite_categories': result.get('composite_categories', []),
            'composite_hit_count': result.get('composite_hit_count', 0),
            'curl_findings': result.get('curl_findings', []),
            'curl_risk_level': result.get('curl_risk_level', None),
            'cred_findings': result.get('cred_findings', []),
            'cred_risk_level': result.get('cred_risk_level', None),
            # v6.2.0 风险分级
            'risk_tier': {
                'level': tier_report['risk_level'],
                'icon': tier_report['risk_icon'],
                'title': tier_report['risk_title'],
                'description': tier_report['risk_description'],
                'score': tier_report['risk_score'],
                'user_action': tier_report['user_action'],
                'user_guidance': tier_report['user_guidance'],
                'categories': tier_report['matched_categories'][:5],
            },
            'detailed_findings': tier_report,
        }
    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e),
            'detected': False
        }


def _group_by_skill(files: list, target_path: Path) -> dict:
    """按 skill 目录分组统计文件数。
    
    返回: {skill_path: [file1, file2, ...]}
    skill_path 是 target_path 下的二级目录 (如 skills/author/skill-name)
    """
    skill_groups = {}
    target_parts_len = len(target_path.parts)
    
    for f in files:
        f_parts = f.parts
        # skill 目录是 target_path 下的前两级 (author/skill-name)
        if len(f_parts) > target_parts_len + 1:
            skill_path = Path(*f_parts[:target_parts_len + 2])
        else:
            skill_path = Path(*f_parts[:target_parts_len + 1])
        
        if skill_path not in skill_groups:
            skill_groups[skill_path] = []
        skill_groups[skill_path].append(f)
    
    return skill_groups


def scan_directory(target_path: Path, scanner, args) -> list:
    """扫描目录 (v6.2.0 优化:优先级 + 熔断 + 记录超时)"""
    print(f"\n📂 扫描目标:{target_path}")

    # 收集文件
    files_to_scan = []
    for ext in args.extensions.split(','):
        files_to_scan.extend(list(target_path.rglob(f'*{ext.strip()}')))

    # 去重
    files_to_scan = list(set(files_to_scan))

    # ========== v6.2.1: 单 Skill 文件数熔断 ==========
    # 目标: 跳过文件数异常的 skill (可能是误发布的 node_modules 或数据集)
    # 正常 skill: 5-30 个文件 | 超大 skill: 100+ 文件 (可疑)
    skill_file_limit = getattr(args, 'skill_max_files', 500)
    
    skill_groups = _group_by_skill(files_to_scan, target_path)
    total_skills = len(skill_groups)
    
    files_after_circuit = []
    circuit_breaker_skipped = []
    
    for skill_path, skill_files in skill_groups.items():
        if len(skill_files) > skill_file_limit:
            # 熔断: 跳过整个 skill 目录
            circuit_breaker_skipped.append({
                'skill': str(skill_path.relative_to(target_path)),
                'file_count': len(skill_files)
            })
        else:
            files_after_circuit.extend(skill_files)
    
    if circuit_breaker_skipped:
        print(f"\n⚡ 熔断触发: {len(circuit_breaker_skipped)}/{total_skills} 个 skill 被跳过 (>{skill_file_limit} 文件)")
        for skipped in sorted(circuit_breaker_skipped, key=lambda x: x['file_count'], reverse=True)[:10]:
            print(f"   🚫 {skipped['skill']}: {skipped['file_count']} 个文件")
        if len(circuit_breaker_skipped) > 10:
            print(f"   ... 还有 {len(circuit_breaker_skipped) - 10} 个")
    
    files_to_scan = files_after_circuit
    skipped_count = sum(s['file_count'] for s in circuit_breaker_skipped)
    print(f"\n✅ 熔断后: {len(files_to_scan)} 个文件 (跳过 {skipped_count} 个, 来自 {len(circuit_breaker_skipped)} 个 skill)")
    
    # v6.2.0 优化:按优先级排序
    files_with_priority = [(f, *get_file_priority(f)) for f in files_to_scan]
    files_with_priority.sort(key=lambda x: x[1])  # 优先级数字小的在前

    print(f"📊 排序完成: {len(files_with_priority)} 个文件 (已按优先级排序)")

    # 应用文件数限制
    if args.max_files > 0 and len(files_with_priority) > args.max_files:
        print(f"⚠️  文件数超过 {args.max_files},只扫描前 {args.max_files} 个")
        files_with_priority = files_with_priority[:args.max_files]

    # 并发扫描
    results = []
    timeout_count = 0
    
    # 记录熔断信息到结果中 (作为第一条)
    if circuit_breaker_skipped:
        results.append({
            'file': '__circuit_breaker_report__',
            'detected': False,
            'circuit_breaker': True,
            'skipped_skills': circuit_breaker_skipped,
            'skipped_file_count': skipped_count,
            'limit': skill_file_limit,
        })

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for filepath, priority, timeout in files_with_priority:
            future = executor.submit(scan_file_with_timeout, filepath, scanner, args.max_depth, timeout)
            futures.append((future, filepath, priority, timeout))

        for future, filepath, priority, timeout in tqdm(futures, total=len(futures), desc="扫描进度"):
            result = future.result()
            results.append(result)

            # 统计超时
            if result.get('timed_out'):
                timeout_count += 1

    # 超时率警告
    if timeout_count > 0:
        timeout_rate = timeout_count / len(results) * 100
        print(f"\n⚠️  超时文件:{timeout_count}/{len(results)} ({timeout_rate:.1f}%)")
        if timeout_rate > 20:
            print(f"💡 建议:超时率较高,可调整 --max-files 或增加超时阈值")

    return results


def analyze_security_tool(target_path: Path, results: list) -> Dict:
    """v6.2.0: 分析技能是否为安全/运维工具，调整风险等级"""
    # 读取 SKILL.md 或主文件内容
    skill_content = ''
    skill_md = target_path / 'SKILL.md'
    if skill_md.exists():
        skill_content = skill_md.read_text(encoding='utf-8', errors='ignore')
    
    # 也读取主代码文件
    main_files = list(target_path.glob('*.py')) + list(target_path.glob('*.js')) + list(target_path.glob('*.sh'))
    for f in main_files[:5]:  # 只读前 5 个主文件
        try:
            skill_content += f.read_text(encoding='utf-8', errors='ignore')[:2000]
        except:
            pass
    
    # 检测工具类型
    tool_info = security_tool_detector.detect_tool_type(str(target_path), skill_content)
    
    # 检查正常运维行为
    behaviors = security_tool_detector.check_legitimate_behavior(skill_content)
    
    # 调整风险等级
    adjusted_results = []
    for r in results:
        if r.get('detected') and tool_info['category']:
            # 获取原始风险等级
            original_risk = r.get('risk_level', 'MEDIUM')
            
            # 提取行为列表
            behavior_list = []
            for m in r.get('matched_rules', []):
                if 'subprocess' in m.lower() or 'shell' in m.lower():
                    behavior_list.append('shell_exec')
                elif 'network' in m.lower() or 'http' in m.lower():
                    behavior_list.append('network_call')
                elif 'config' in m.lower() or 'credential' in m.lower():
                    behavior_list.append('config_read')
            
            # 调整风险
            adjustment = security_tool_detector.adjust_risk_level(
                original_risk, 
                tool_info['tool_type'], 
                behavior_list
            )
            
            # 更新结果
            r['original_risk_level'] = original_risk
            r['risk_level'] = adjustment['adjusted_risk']
            r['tool_type'] = tool_info['tool_type']
            r['tool_confidence'] = tool_info['confidence']
            r['risk_adjustment'] = adjustment['adjustment']
            r['adjustment_reason'] = adjustment['reason']
        
        adjusted_results.append(r)
    
    return {
        'tool_type': tool_info['tool_type'],
        'tool_category': tool_info['category'],
        'confidence': tool_info['confidence'],
        'risk_adjustment': tool_info['risk_adjustment'],
        'legitimate_behaviors': [b['description'] for b in behaviors],
        'results': adjusted_results
    }


def generate_report(results, args, tool_analysis=None):
    """生成扫描报告 (v6.2.1 优化:超时统计 + 安全工具识别 + 熔断统计)"""
    # 提取熔断信息 (第一条记录)
    circuit_breaker_info = None
    real_results = []
    for r in results:
        if r.get('circuit_breaker'):
            circuit_breaker_info = r
        elif r.get('skipped_metadata'):
            continue
        else:
            real_results.append(r)
    results = real_results
    
    # 统计
    total = len(results)
    detected = sum(1 for r in results if r.get('detected'))
    safe = total - detected

    # 超时统计
    timeout_files = [r for r in results if r.get('timed_out')]
    timeout_count = len(timeout_files)
    timeout_rate = timeout_count / total * 100 if total > 0 else 0

    # 风险分布
    risk_dist = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'SAFE': 0}
    for r in results:
        risk_level = r.get('risk_level', 'SAFE')
        if risk_level in risk_dist:
            risk_dist[risk_level] += 1

    # LLM 统计
    llm_stats = None
    if args.llm:
        llm_count = sum(1 for r in results if r.get('layer3_llm'))
        llm_stats = {
            'analyzed': llm_count,
            'model': args.llm_model
        }

    # 超时建议
    timeout_recommendation = None
    if timeout_rate > 20:
        timeout_recommendation = {
            'issue': f'超时率过高 ({timeout_rate:.1f}%)',
            'suggestion': '建议增加超时阈值或减少扫描文件数',
            'config': {
                'current_timeout': '动态 (1-10s)',
                'recommendation': '可考虑增加 P4/P5/P6 文件超时预算'
            }
        }

    # 生成报告
    report = {
        'summary': {
            'total_files': total,
            'detected': detected,
            'safe': safe,
            'detection_rate': detected / total * 100 if total > 0 else 0,
            'scan_time': datetime.now().isoformat(),
            'timeout_count': timeout_count,
            'timeout_rate': timeout_rate
        },
        'config': {
            'version': '6.2.0',
            'rules_count': 846,
            'extensions': args.extensions,
            'max_files': args.max_files,
            'skill_max_files': args.skill_max_files,
            'llm_enabled': args.llm,
            'llm_model': args.llm_model if args.llm else None,
            'priority_scan': True,
            'timeout_tracking': True
        },
        'risk_distribution': risk_dist,
        'llm_stats': llm_stats,
        'security_tool_analysis': tool_analysis if tool_analysis else {'tool_type': 'unknown', 'confidence': 0, 'risk_adjustment': 0, 'legitimate_behaviors': []},
        'timeout_analysis': {
            'count': timeout_count,
            'rate': timeout_rate,
            'recommendation': timeout_recommendation,
            'files': [{'file': r['file'], 'priority': r.get('priority'), 'timeout_budget': r.get('timeout_budget'), 'scan_time': r.get('scan_time')} for r in timeout_files[:100]]  # 前 100 个超时文件
        },
        'circuit_breaker': {
            'enabled': circuit_breaker_info is not None,
            'skilled_skipped': circuit_breaker_info['skipped_skills'] if circuit_breaker_info else [],
            'total_skipped_files': circuit_breaker_info['skipped_file_count'] if circuit_breaker_info else 0,
            'limit': circuit_breaker_info['limit'] if circuit_breaker_info else 50,
        },
        'results': results
    }

    return report


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Security Scanner CLI v6.2.0 - 统一三层架构 (AC 自动机 + Pattern + Rule + LLM + 风险分级)')

    # 基本参数
    parser.add_argument('target', type=str, help='扫描目标 (文件或目录)')
    parser.add_argument('--extensions', type=str, default='.py,.python,.js,.javascript,.jsx,.ts,.tsx,.sh,.bash,.ps1,.yaml,.yml,.json,.go,.rb,.php,.java,.c,.cpp,.h,.hpp',
                        help='文件扩展名 (默认:.py,.js,.sh,.ps1,.yaml,.json)')
    parser.add_argument('--max-files', type=int, default=200000,
                        help='最大文件数 (默认:200000)')
    parser.add_argument('--max-depth', type=int, default=20,
                        help='最大目录深度 (默认:20)')
    parser.add_argument('--workers', type=int, default=8,
                        help='并发 workers (默认:8,稳定模式)')
    
    # v6.2.1: 单 Skill 文件数熔断 (跳过文件过多的异常 skill)
    parser.add_argument('--skill-max-files', type=int, default=500,
                        help='单 skill 最大文件数 (超过则跳过整个 skill, 默认:500)')

    # LLM 可选参数
    llm_group = parser.add_argument_group('LLM 选项 (可选)')
    llm_group.add_argument('--llm', action='store_true',
                          help='启用 LLM 深度分析 (仅对 CRITICAL 级别)')
    llm_group.add_argument('--llm-model', type=str, default='qwen',
                          choices=['minimax', 'qwen', 'openai'],
                          help='LLM 模型选择 (默认:qwen)')
    llm_group.add_argument('--llm-threshold', type=float, default=0.5,
                          help='LLM 分析阈值 (默认:0.5)')
    llm_group.add_argument('--llm-api-key', type=str, default='',
                          help='LLM API Key (默认:从 LLM_API_KEY 环境变量读取)')

    # 输出参数
    parser.add_argument('--output', type=str, default='text',
                        choices=['text', 'json'],
                        help='输出格式 (默认:text)')
    parser.add_argument('--output-file', type=str, default='scan_report.json',
                        help='输出文件路径 (默认:scan_report.json)')

    args = parser.parse_args()

    # 打印版本信息
    print("=" * 60)
    print("🛡️  Security Scanner CLI v6.2.0 - 统一架构版 (风险分级+熔断)")
    print("=" * 60)
    print(f"⏰ 开始时间:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 架构:Layer1(Pattern) → Layer2(Hybrid AC+Regex) → Layer3(LLM 可选)")
    print(f"👷 Workers:{args.workers} | 📁 Max Files:{args.max_files} | 🔍 Max Depth:{args.max_depth}")

    # 创建扫描器 (三层架构)
    scanner = create_scanner(args)
    scanner['base_path'] = args.target

    # 扫描
    target_path = Path(args.target)
    results = scan_directory(target_path, scanner, args)

    # v6.2.0: 安全工具识别 + 风险调整
    print("\n🛡️  安全工具识别...")
    tool_analysis = analyze_security_tool(target_path, results)
    results = tool_analysis['results']
    print(f"   工具类型:{tool_analysis['tool_type']} (置信度:{tool_analysis['confidence']})")
    print(f"   风险调整:{tool_analysis['risk_adjustment']}")
    if tool_analysis['legitimate_behaviors']:
        print(f"   正常行为:{', '.join(tool_analysis['legitimate_behaviors'][:3])}")

    # 生成报告
    report = generate_report(results, args, tool_analysis)

    # 输出
    if args.output == 'json':
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📂 报告已保存:{args.output_file}")
    else:
        print("\n" + "=" * 60)
        print("📊 扫描总结")
        print("=" * 60)
        print(f"⏱️  总耗时:N/A")
        print(f"📁 文件数:{report['summary']['total_files']}")
        print(f"✅ 检出:{report['summary']['detected']}")
        print(f"❌ 漏检:{report['summary']['safe']}")
        print(f"📈 检测率:{report['summary']['detection_rate']:.2f}%")
        print(f"\n🚨 风险分布:")
        for level, count in report['risk_distribution'].items():
            if count > 0:
                print(f"   {level}: {count} 个")
        if report['llm_stats']:
            print(f"\n🤖 LLM 分析:")
            print(f"   分析样本:{report['llm_stats']['analyzed']} 个")
            print(f"   模型:{report['llm_stats']['model']}")
        print("=" * 60)
        print("\n✅ 扫描完成!")

    return 0


if __name__ == '__main__':
    sys.exit(main())
