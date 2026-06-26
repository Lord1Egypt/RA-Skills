#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ Sigma + YARA 规则集成系统

功能:
1. 统一加载 Sigma 和 YARA 规则
2. 规则格式转换 (Sigma → Runtime/YARA)
3. 规则验证与优化
4. 规则索引生成
5. 与 agent-defender 集成

作者：Agent Security System
日期：2026-03-23
"""

import os
import sys
import json
import yaml
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILLS_DIR = WORKSPACE / "skills"
AGENT_DEFENDER_DIR = SKILLS_DIR / "agent-defender"
SECURITY_SCANNER_DIR = SKILLS_DIR / "agent-security-skill-scanner" / "expert_mode"

# 规则目录 (支持多个源)
SIGMA_RULES_DIRS = [
    SECURITY_SCANNER_DIR / "rules" / "sigma",
    SKILLS_DIR / "security-sample-generator" / "rules" / "sigma"
]
YARA_RULES_DIRS = [
    SECURITY_SCANNER_DIR / "rules" / "yara",
    SKILLS_DIR / "security-sample-generator" / "rules" / "yara",
    SECURITY_SCANNER_DIR / "rules" / "prompt_injection" / "yara"
]
DEFENDER_RULES_DIR = AGENT_DEFENDER_DIR / "rules"

# 输出目录
OUTPUT_DIR = AGENT_DEFENDER_DIR / "integrated_rules"
LOG_FILE = OUTPUT_DIR / "integration.log"

# 确保目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class RuleIntegrator:
    """Sigma + YARA 规则集成器"""
    
    def __init__(self):
        self.sigma_rules = []
        self.yara_rules = []
        self.integrated_rules = []
        self.stats = {
            "sigma_loaded": 0,
            "yara_loaded": 0,
            "sigma_converted": 0,
            "yara_converted": 0,
            "total_integrated": 0,
            "errors": 0
        }
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"
        print(log_msg)
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    
    def load_sigma_rules(self) -> List[Dict]:
        """加载 Sigma 规则 (支持多个目录)"""
        self.log(f"从 {len(SIGMA_RULES_DIRS)} 个目录加载 Sigma 规则...")
        sigma_rules = []
        
        for sigma_dir in SIGMA_RULES_DIRS:
            if not sigma_dir.exists():
                self.log(f"目录不存在：{sigma_dir}", "WARNING")
                continue
            
            self.log(f"  扫描：{sigma_dir}")
            for yaml_file in sigma_dir.rglob("*.yaml"):
                try:
                    with open(yaml_file, "r", encoding="utf-8") as f:
                        rule = yaml.safe_load(f)
                        if rule and "id" in rule:
                            rule["_source_file"] = str(yaml_file)
                            rule["_type"] = "sigma"
                            sigma_rules.append(rule)
                            self.stats["sigma_loaded"] += 1
                except Exception as e:
                    self.log(f"加载 Sigma 规则失败 {yaml_file}: {e}", "ERROR")
                    self.stats["errors"] += 1
        
        self.sigma_rules = sigma_rules
        self.log(f"成功加载 {len(sigma_rules)} 条 Sigma 规则")
        return sigma_rules
    
    def load_yara_rules(self) -> List[Dict]:
        """加载 YARA 规则 (支持多个目录)"""
        self.log(f"从 {len(YARA_RULES_DIRS)} 个目录加载 YARA 规则...")
        yara_rules = []
        
        for yara_dir in YARA_RULES_DIRS:
            if not yara_dir.exists():
                self.log(f"目录不存在：{yara_dir}", "WARNING")
                continue
            
            self.log(f"  扫描：{yara_dir}")
            for yar_file in yara_dir.rglob("*.yar"):
                try:
                    with open(yar_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        rule = {
                            "_source_file": str(yar_file),
                            "_type": "yara",
                            "_raw_content": content,
                            "id": self._extract_yara_rule_id(content, yar_file.name),
                            "name": self._extract_yara_rule_name(content)
                        }
                        yara_rules.append(rule)
                        self.stats["yara_loaded"] += 1
                except Exception as e:
                    self.log(f"加载 YARA 规则失败 {yar_file}: {e}", "ERROR")
                    self.stats["errors"] += 1
        
        self.yara_rules = yara_rules
        self.log(f"成功加载 {len(yara_rules)} 条 YARA 规则")
        return yara_rules
    
    def _extract_yara_rule_id(self, content: str, filename: str) -> str:
        """从 YARA 规则内容提取 ID"""
        import re
        match = re.search(r'rule\s+(\w+)', content)
        if match:
            rule_name = match.group(1)
            return f"YARA-{rule_name}"
        return f"YARA-{hashlib.md5(filename.encode()).hexdigest()[:8]}"
    
    def _extract_yara_rule_name(self, content: str) -> str:
        """从 YARA 规则内容提取名称"""
        import re
        match = re.search(r'description\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)
        match = re.search(r'rule\s+(\w+)', content)
        if match:
            return match.group(1)
        return "Unknown YARA Rule"
    
    def convert_sigma_to_runtime(self, sigma_rule: Dict) -> Dict:
        """将 Sigma 规则转换为 Runtime 格式"""
        detection = sigma_rule.get("detection", {})
        condition = detection.get("condition", "")
        selection = detection.get("selection", {})
        
        # 提取命令行模式
        patterns = []
        for key, value in selection.items():
            if isinstance(value, str):
                patterns.append(value.replace("*", ".*"))
            elif isinstance(value, list):
                patterns.extend([v.replace("*", ".*") for v in value])
        
        runtime_rule = {
            "id": sigma_rule.get("id", "UNKNOWN"),
            "name": sigma_rule.get("title", "Unknown"),
            "type": "Runtime",
            "source": "sigma",
            "severity": sigma_rule.get("level", "medium"),
            "description": sigma_rule.get("description", ""),
            "author": sigma_rule.get("author", ""),
            "tags": sigma_rule.get("tags", []),
            "detection": {
                "type": "pattern_match",
                "patterns": patterns,
                "condition": "any"
            },
            "metadata": {
                "original_id": sigma_rule.get("id"),
                "converted_at": datetime.now().isoformat(),
                "source_file": sigma_rule.get("_source_file", "")
            }
        }
        
        self.stats["sigma_converted"] += 1
        return runtime_rule
    
    def convert_yara_to_json(self, yara_rule: Dict) -> Dict:
        """将 YARA 规则转换为 JSON 格式 (用于 agent-defender)"""
        import re
        
        raw_content = yara_rule.get("_raw_content", "")
        
        # 提取元数据
        meta_match = re.search(r'meta:\s*([\s\S]*?)(?=strings:|condition:)', raw_content)
        meta = {}
        if meta_match:
            meta_text = meta_match.group(1)
            for line in meta_text.strip().split("\n"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    meta[key.strip()] = value.strip().strip('"')
        
        # 提取字符串
        strings_match = re.search(r'strings:\s*([\s\S]*?)(?=condition:)', raw_content)
        strings = []
        if strings_match:
            strings_text = strings_match.group(1)
            for line in strings_text.strip().split("\n"):
                if "=" in line and line.strip().startswith("$"):
                    strings.append(line.strip())
        
        # 提取条件
        condition_match = re.search(r'condition:\s*(.+)', raw_content)
        condition = condition_match.group(1).strip() if condition_match else ""
        
        json_rule = {
            "id": yara_rule.get("id", "UNKNOWN"),
            "name": yara_rule.get("name", "Unknown"),
            "type": "YARA",
            "source": "yara",
            "severity": meta.get("severity", "medium"),
            "description": meta.get("description", ""),
            "author": meta.get("author", ""),
            "tags": [
                meta.get("attack_type", ""),
                meta.get("mitre_id", "")
            ],
            "detection": {
                "type": "yara",
                "strings": strings,
                "condition": condition,
                "raw_rule": raw_content
            },
            "metadata": {
                "original_id": yara_rule.get("id"),
                "converted_at": datetime.now().isoformat(),
                "source_file": yara_rule.get("_source_file", ""),
                "mitre_id": meta.get("mitre_id", ""),
                "attack_type": meta.get("attack_type", "")
            }
        }
        
        self.stats["yara_converted"] += 1
        return json_rule
    
    def integrate_rules(self) -> List[Dict]:
        """集成所有规则"""
        self.log("开始集成规则...")
        
        integrated = []
        
        # 转换 Sigma 规则
        for sigma_rule in self.sigma_rules:
            try:
                runtime_rule = self.convert_sigma_to_runtime(sigma_rule)
                integrated.append(runtime_rule)
            except Exception as e:
                self.log(f"转换 Sigma 规则失败 {sigma_rule.get('id')}: {e}", "ERROR")
                self.stats["errors"] += 1
        
        # 转换 YARA 规则
        for yara_rule in self.yara_rules:
            try:
                json_rule = self.convert_yara_to_json(yara_rule)
                integrated.append(json_rule)
            except Exception as e:
                self.log(f"转换 YARA 规则失败 {yara_rule.get('id')}: {e}", "ERROR")
                self.stats["errors"] += 1
        
        self.integrated_rules = integrated
        self.stats["total_integrated"] = len(integrated)
        self.log(f"成功集成 {len(integrated)} 条规则")
        
        return integrated
    
    def save_integrated_rules(self, output_file: Path = None):
        """保存集成后的规则"""
        if output_file is None:
            output_file = OUTPUT_DIR / "integrated_rules.json"
        
        self.log(f"保存集成规则到 {output_file}...")
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "version": "1.0",
                "generated_at": datetime.now().isoformat(),
                "stats": self.stats,
                "rules": self.integrated_rules
            }, f, indent=2, ensure_ascii=False)
        
        self.log(f"已保存 {len(self.integrated_rules)} 条规则")
    
    def generate_index(self, index_file: Path = None):
        """生成规则索引"""
        if index_file is None:
            index_file = OUTPUT_DIR / "RULES_INDEX.yaml"
        
        self.log(f"生成规则索引 {index_file}...")
        
        index_data = {
            "index_version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "total_rules": len(self.integrated_rules),
            "sigma_rules": self.stats["sigma_loaded"],
            "yara_rules": self.stats["yara_loaded"],
            "rules": []
        }
        
        for rule in self.integrated_rules:
            index_entry = {
                "id": rule.get("id"),
                "name": rule.get("name"),
                "type": rule.get("type"),
                "source": rule.get("source"),
                "severity": rule.get("severity"),
                "description": rule.get("description"),
                "tags": rule.get("tags", [])
            }
            index_data["rules"].append(index_entry)
        
        with open(index_file, "w", encoding="utf-8") as f:
            yaml.dump(index_data, f, allow_unicode=True, default_flow_style=False)
        
        self.log(f"已生成索引，包含 {len(index_data['rules'])} 条规则")
    
    def _deduplicate_rules(self):
        """去重规则 (基于 ID)"""
        seen_ids = set()
        unique_rules = []
        duplicates = 0
        
        for rule in self.integrated_rules:
            rule_id = rule.get("id", "")
            if rule_id and rule_id not in seen_ids:
                seen_ids.add(rule_id)
                unique_rules.append(rule)
            else:
                duplicates += 1
                self.log(f"跳过重复规则：{rule_id}", "DEBUG")
        
        if duplicates > 0:
            self.log(f"去重：移除 {duplicates} 条重复规则")
        
        self.integrated_rules = unique_rules
        self.stats["total_integrated"] = len(unique_rules)
    
    def sync_to_defender(self):
        """同步规则到 agent-defender"""
        self.log("同步规则到 agent-defender...")
        
        # 按攻击类型分类
        rules_by_type = {}
        for rule in self.integrated_rules:
            attack_type = rule.get("metadata", {}).get("attack_type", "unknown")
            if not attack_type:
                # 从标签推断
                tags = rule.get("tags", [])
                for tag in tags:
                    if "prompt_injection" in tag:
                        attack_type = "prompt_injection"
                    elif "tool_poisoning" in tag:
                        attack_type = "tool_poisoning"
                    elif "data_exfil" in tag:
                        attack_type = "data_exfil"
            
            if attack_type not in rules_by_type:
                rules_by_type[attack_type] = []
            rules_by_type[attack_type].append(rule)
        
        # 为每个攻击类型生成规则文件
        for attack_type, rules in rules_by_type.items():
            output_file = DEFENDER_RULES_DIR / f"{attack_type}_integrated.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({
                    "attack_type": attack_type,
                    "generated_at": datetime.now().isoformat(),
                    "rule_count": len(rules),
                    "rules": rules
                }, f, indent=2, ensure_ascii=False)
            
            self.log(f"已同步 {len(rules)} 条规则到 {output_file.name}")
    
    def run(self):
        """执行完整集成流程"""
        self.log("=" * 60)
        self.log("🛡️ Sigma + YARA 规则集成系统")
        self.log("=" * 60)
        
        # 1. 加载规则 (支持多个目录)
        self.load_sigma_rules()
        self.load_yara_rules()
        
        # 清理重复规则
        self._deduplicate_rules()
        
        # 2. 转换规则
        self.integrate_rules()
        
        # 3. 保存集成规则
        self.save_integrated_rules()
        
        # 4. 生成索引
        self.generate_index()
        
        # 5. 同步到 agent-defender
        self.sync_to_defender()
        
        # 6. 输出统计
        self.log("=" * 60)
        self.log("📊 集成统计:")
        self.log(f"  Sigma 规则加载：{self.stats['sigma_loaded']}")
        self.log(f"  YARA 规则加载：{self.stats['yara_loaded']}")
        self.log(f"  Sigma 规则转换：{self.stats['sigma_converted']}")
        self.log(f"  YARA 规则转换：{self.stats['yara_converted']}")
        self.log(f"  总集成规则：{self.stats['total_integrated']}")
        self.log(f"  错误数：{self.stats['errors']}")
        self.log("=" * 60)
        
        return self.stats


def main():
    """主函数"""
    integrator = RuleIntegrator()
    stats = integrator.run()
    
    if stats["errors"] > 0:
        print(f"\n⚠️  集成完成，但有 {stats['errors']} 个错误")
        return 1
    
    print("\n✅ 规则集成完成!")
    print(f"📁 集成规则：{OUTPUT_DIR / 'integrated_rules.json'}")
    print(f"📋 规则索引：{OUTPUT_DIR / 'RULES_INDEX.yaml'}")
    print(f"🛡️ Defender 规则：{DEFENDER_RULES_DIR / '*_integrated.json'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
