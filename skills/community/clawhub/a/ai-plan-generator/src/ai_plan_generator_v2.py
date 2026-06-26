#!/usr/bin/env python3
"""
AI Plan Generator v2 - Business Function Focused
Converts Code Archaeology analysis results into AI-executable development task lists.
Focuses on business functionality decomposition rather than language-specific implementation.
"""

import os
import json
import glob
from pathlib import Path
from typing import Dict, List, Any

class AIPlanGeneratorV2:
    def __init__(self, analysis_dir: str, output_dir: str = None):
        self.analysis_dir = Path(analysis_dir)
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.domains_dir = self.analysis_dir / "domains"
        self.memory_dir = self.analysis_dir / "memory"
        
        # Initialize data structures
        self.business_domains = {}
        self.security_vulnerabilities = []
        self.generated_tasks = {
            "phase_1_core_functionality": [],
            "phase_2_infrastructure": [],
            "phase_3_security_fixes": []
        }
        
    def parse_analysis_results(self):
        """Parse all Code Archaeology analysis results"""
        print("🔍 Parsing Code Archaeology analysis results...")
        
        # Parse business domains
        self._parse_business_domains()
        
        # Parse security vulnerabilities  
        self._parse_security_vulnerabilities()
        
        print(f"✅ Parsed {len(self.business_domains)} business domains")
        print(f"✅ Found {len(self.security_vulnerabilities)} security vulnerabilities")
        
    def _parse_business_domains(self):
        """Parse business domain analysis files"""
        if not self.domains_dir.exists():
            raise FileNotFoundError(f"Domains directory not found: {self.domains_dir}")
            
        analysis_files = list(self.domains_dir.glob("*.analysis.md"))
        
        for analysis_file in analysis_files:
            domain_name = analysis_file.stem.replace('.analysis', '')
            
            # Read analysis content
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis_content = f.read()
                
            # Try to read flows and model files
            flows_file = self.domains_dir / f"{domain_name}.flows.json"
            model_file = self.domains_dir / f"{domain_name}.model.json"
            
            flows_data = {}
            if flows_file.exists():
                try:
                    with open(flows_file, 'r', encoding='utf-8') as f:
                        flows_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"⚠️  Invalid JSON in {flows_file}")
                    
            model_data = {}
            if model_file.exists():
                try:
                    with open(model_file, 'r', encoding='utf-8') as f:
                        model_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"⚠️  Invalid JSON in {model_file}")
            
            self.business_domains[domain_name] = {
                "analysis_content": analysis_content,
                "flows_data": flows_data,
                "model_data": model_data,
                "analysis_file": str(analysis_file),
                "flows_file": str(flows_file) if flows_file.exists() else None,
                "model_file": str(model_file) if model_file.exists() else None
            }
    
    def _parse_security_vulnerabilities(self):
        """Parse security vulnerabilities from audit results"""
        # Look for security audit file in workspace root
        security_audit_path = Path("/Users/admin/.openclaw/workspace/zbs_php_security_audit_results.md")
        
        if security_audit_path.exists():
            with open(security_audit_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract vulnerability information
            vulnerabilities = self._extract_vulnerabilities_from_content(content)
            self.security_vulnerabilities.extend(vulnerabilities)
        else:
            print("⚠️  Security audit file not found")
            
    def _extract_vulnerabilities_from_content(self, content: str) -> List[Dict]:
        """Extract vulnerability information from security audit content"""
        vulnerabilities = []
        
        # Look for SQL injection vulnerabilities
        if "SQL注入" in content or "SQL injection" in content:
            vulnerabilities.append({
                "type": "sql_injection",
                "severity": "high",
                "description": "SQL injection vulnerabilities detected",
                "locations": ["Multiple locations in database queries"],
                "remediation": "Implement secure query practices"
            })
            
        # Look for hard-coded credentials
        if "硬编码" in content or "hard-coded" in content:
            vulnerabilities.append({
                "type": "hardcoded_credentials",
                "severity": "high", 
                "description": "Hard-coded credentials found",
                "locations": ["core/auth.php - SUPERDWP = '123qwe'"],
                "remediation": "Remove hard-coded credentials"
            })
            
        # Look for weak password policies
        if "弱密码" in content or "weak password" in content:
            vulnerabilities.append({
                "type": "weak_password_policy",
                "severity": "medium",
                "description": "Weak password storage and policies",
                "locations": ["User authentication modules"],
                "remediation": "Implement strong password practices"
            })
            
        return vulnerabilities
        
    def generate_tasks(self):
        """Generate AI-executable tasks from parsed analysis"""
        print("📋 Generating AI-executable tasks...")
        
        # Generate Phase 1: Core Business Functionality
        self._generate_core_functionality_tasks()
        
        # Generate Phase 2: Infrastructure Tasks  
        self._generate_infrastructure_tasks()
        
        # Generate Phase 3: Security Fix Tasks (as inventory, not for immediate execution)
        self._generate_security_fix_inventory()
        
        total_tasks = sum(len(tasks) for tasks in self.generated_tasks.values())
        print(f"✅ Generated {total_tasks} tasks across 3 phases")
        
    def _generate_core_functionality_tasks(self):
        """Generate core business functionality tasks (Phase 1)"""
        print("  📌 Phase 1: Core Business Functionality")
        
        for domain_name, domain_data in self.business_domains.items():
            # Extract business functions from flows data
            business_functions = self._extract_business_functions(domain_name, domain_data)
            
            for function_name, function_details in business_functions.items():
                task = self._create_business_function_task(
                    domain_name, function_name, function_details, domain_data
                )
                self.generated_tasks["phase_1_core_functionality"].append(task)
                
        print(f"    ✅ Generated {len(self.generated_tasks['phase_1_core_functionality'])} core functionality tasks")
        
    def _extract_business_functions(self, domain_name: str, domain_data: Dict) -> Dict[str, Dict]:
        """Extract business functions from domain analysis and flows"""
        functions = {}
        
        # Get flows data
        flows_data = domain_data.get("flows_data", {})
        
        # Default business functions based on common patterns
        default_functions = {
            "create": {"description": "Create new entity", "priority": "high"},
            "update": {"description": "Update existing entity", "priority": "high"}, 
            "view": {"description": "View entity details", "priority": "medium"},
            "delete": {"description": "Delete entity", "priority": "low"},
            "submit_approval": {"description": "Submit for approval", "priority": "high"},
            "approve": {"description": "Approve entity", "priority": "high"},
            "reject": {"description": "Reject entity", "priority": "high"},
            "complete": {"description": "Complete entity lifecycle", "priority": "high"}
        }
        
        # Special handling for specific domains
        if "contract" in domain_name:
            functions.update({
                "create": default_functions["create"],
                "submit_approval": default_functions["submit_approval"], 
                "approve": default_functions["approve"],
                "reject": default_functions["reject"],
                "complete": default_functions["complete"],
                "view_details": {"description": "View contract details page", "priority": "medium"}
            })
        elif "customer" in domain_name:
            functions.update({
                "create": default_functions["create"],
                "update": default_functions["update"],
                "view": default_functions["view"],
                "delete": default_functions["delete"]
            })
        elif "financial" in domain_name:
            functions.update({
                "process_payment": {"description": "Process payment transaction", "priority": "high"},
                "generate_invoice": {"description": "Generate invoice document", "priority": "high"},
                "reconcile_accounts": {"description": "Reconcile financial accounts", "priority": "medium"}
            })
        else:
            # Generic functions for other domains
            functions.update({
                "create": default_functions["create"],
                "update": default_functions["update"],
                "view": default_functions["view"]
            })
            
        return functions
        
    def _create_business_function_task(self, domain_name: str, function_name: str, 
                                    function_details: Dict, domain_data: Dict) -> Dict:
        """Create a business function task focused on what, not how"""
        task_id = f"{domain_name}_{function_name}"
        
        # Determine priority
        priority_map = {"high": "critical", "medium": "high", "low": "medium"}
        priority = priority_map.get(function_details.get("priority", "medium"), "medium")
        
        task = {
            "task_id": task_id,
            "task_type": "feature_implementation",
            "priority": priority,
            "phase": 1,
            "module": domain_name,
            "description": function_details["description"],
            "context": {
                "business_rules": self._extract_business_rules_from_analysis(domain_data["analysis_content"]),
                "business_workflows": self._extract_business_workflows(domain_data["flows_data"]),
                "data_models": self._extract_data_models(domain_data["model_data"])
            },
            "validation_criteria": [
                "business_function_implements_all_rules",
                "workflow_transitions_work_correctly", 
                "data_model_relationships_preserved",
                "user_acceptance_tests_pass"
            ],
            "dependencies": self._determine_dependencies(domain_name, function_name)
        }
        
        return task
        
    def _extract_business_rules_from_analysis(self, analysis_content: str) -> List[str]:
        """Extract business rules from analysis content (language-agnostic)"""
        rules = []
        
        # Look for common business rule patterns
        lines = analysis_content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['必须', '应该', '需要', 'required', 'must', 'should']):
                if len(line.strip()) > 10:  # Avoid very short lines
                    # Extract only the business logic, not technical implementation
                    clean_rule = self._clean_business_rule(line.strip())
                    if clean_rule:
                        rules.append(clean_rule)
                    
        # Limit to top 5 most relevant rules
        return rules[:5] if rules else ["No specific business rules identified"]
        
    def _clean_business_rule(self, rule_text: str) -> str:
        """Clean business rule text to remove technical implementation details"""
        # Remove PHP-specific syntax references
        cleaned = rule_text
        cleaned = cleaned.replace('$_SESSION', 'user session')
        cleaned = cleaned.replace('validate_admin', 'admin validation')
        cleaned = cleaned.replace('api4', 'API endpoint')
        # Focus on business meaning rather than technical implementation
        return cleaned.strip()
        
    def _extract_business_workflows(self, flows_data: Dict) -> List[str]:
        """Extract business workflows from flows data"""
        workflows = []
        
        if flows_data:
            # Extract state transitions
            if "states" in flows_data:
                states = flows_data["states"]
                workflows.append(f"Business states: {', '.join(states)}")
            
            if "transitions" in flows_data:
                transitions = flows_data["transitions"]
                workflow_desc = "State transitions: "
                for transition in transitions[:3]:  # Limit to first 3
                    workflow_desc += f"{transition.get('from', 'unknown')} → {transition.get('to', 'unknown')}; "
                workflows.append(workflow_desc)
                
        return workflows if workflows else ["No specific workflows identified"]
        
    def _extract_data_models(self, model_data: Dict) -> List[str]:
        """Extract data models from model data"""
        models = []
        
        if model_data:
            if "entities" in model_data:
                entities = model_data["entities"]
                entity_names = [entity.get("name", "unknown") for entity in entities[:3]]
                models.append(f"Core entities: {', '.join(entity_names)}")
                
            if "relationships" in model_data:
                relationships = model_data["relationships"]
                models.append(f"Entity relationships: {len(relationships)} relationships defined")
                
        return models if models else ["No specific data models identified"]
        
    def _determine_dependencies(self, domain_name: str, function_name: str) -> List[str]:
        """Determine task dependencies based on business logic"""
        dependencies = []
        
        # Create should be done before update/delete
        if function_name in ["update", "delete", "view"]:
            dependencies.append(f"{domain_name}_create")
            
        # Submit approval should be done after create
        if function_name == "submit_approval":
            dependencies.append(f"{domain_name}_create")
            
        # Approve/reject should be done after submit_approval
        if function_name in ["approve", "reject"]:
            dependencies.append(f"{domain_name}_submit_approval")
            
        return dependencies
        
    def _generate_infrastructure_tasks(self):
        """Generate infrastructure tasks (Phase 2)"""
        print("  🏗️  Phase 2: Infrastructure Tasks")
        
        infrastructure_tasks = [
            {
                "task_id": "multitenant_middleware_001",
                "task_type": "infrastructure_setup", 
                "priority": "high",
                "phase": 2,
                "module": "infrastructure",
                "description": "Implement multi-tenant data isolation middleware",
                "context": {
                    "business_rules": ["Data must be isolated between different tenants/customers"],
                    "business_workflows": ["All business operations must respect tenant boundaries"],
                    "data_models": ["Tenant identifier required for all data access operations"]
                },
                "validation_criteria": ["tenant_isolation_verified", "no_cross_tenant_data_access"],
                "dependencies": []
            },
            {
                "task_id": "authentication_system_002", 
                "task_type": "infrastructure_setup",
                "priority": "high",
                "phase": 2,
                "module": "infrastructure",
                "description": "Implement secure authentication and authorization system",
                "context": {
                    "business_rules": ["Only authorized users can access business functions", "Different roles have different permissions"],
                    "business_workflows": ["User authentication required before any business operation"],
                    "data_models": ["User roles and permissions must be properly managed"]
                },
                "validation_criteria": ["authentication_works", "authorization_enforced", "role_based_access_control"],
                "dependencies": []
            }
        ]
        
        self.generated_tasks["phase_2_infrastructure"] = infrastructure_tasks
        print(f"    ✅ Generated {len(infrastructure_tasks)} infrastructure tasks")
        
    def _generate_security_fix_inventory(self):
        """Generate security fix inventory (Phase 3 - for reference only)"""
        print("  🔒 Phase 3: Security Vulnerability Inventory")
        
        security_tasks = []
        for i, vuln in enumerate(self.security_vulnerabilities, 1):
            task = {
                "task_id": f"security_fix_{vuln['type']}_{i:03d}",
                "task_type": "security_fix",
                "priority": "low",  # Lowest priority as per requirements
                "phase": 3,
                "module": "security",
                "description": f"Address {vuln['type']} security vulnerability",
                "context": {
                    "business_rules": ["System must maintain data security and integrity"],
                    "business_workflows": ["Security considerations apply to all business operations"],
                    "data_models": ["Sensitive data must be properly protected"]
                },
                "vulnerability_details": {
                    "type": vuln["type"],
                    "severity": vuln["severity"], 
                    "description": vuln["description"],
                    "locations": vuln["locations"],
                    "remediation": vuln["remediation"]
                },
                "validation_criteria": ["vulnerability_addressed", "security_standards_met"],
                "dependencies": []
            }
            security_tasks.append(task)
            
        self.generated_tasks["phase_3_security_fixes"] = security_tasks
        print(f"    ✅ Generated {len(security_tasks)} security vulnerability inventory items")
        
    def generate_markdown_output(self) -> str:
        """Generate markdown output focused on business functionality"""
        print("📝 Generating Markdown output...")
        
        md_content = []
        md_content.append("# AI 开发任务清单")
        md_content.append("")
        md_content.append("## 项目信息")
        md_content.append("- **项目名称**: dms-erp")
        md_content.append("- **核心原则**: 业务功能分解，语言无关实现")
        md_content.append("- **执行策略**: 核心业务功能优先，安全修复最后")
        md_content.append("")
        md_content.append("## 任务优先级说明")
        md_content.append("1. **核心业务功能** (Phase 1) - 最高优先级")
        md_content.append("2. **基础设施完善** (Phase 2) - 中等优先级")  
        md_content.append("3. **安全漏洞修复** (Phase 3) - 最低优先级 (但提供完整漏洞清单)")
        md_content.append("")
        md_content.append("---")
        md_content.append("")
        
        # Phase 1: Core Business Functionality
        md_content.append("## Phase 1: 核心业务功能")
        md_content.append("")
        
        # Group tasks by module
        phase1_tasks = self.generated_tasks["phase_1_core_functionality"]
        modules = {}
        for task in phase1_tasks:
            module = task["module"]
            if module not in modules:
                modules[module] = []
            modules[module].append(task)
            
        for module, tasks in modules.items():
            md_content.append(f"### {module.replace('_', ' ').title()} 模块")
            md_content.append("")
            
            for task in tasks:
                md_content.append(f"#### 任务 {task['task_id']}")
                md_content.append(f"- **描述**: {task['description']}")
                md_content.append(f"- **优先级**: {task['priority']}")
                md_content.append("")
                md_content.append("- **业务规则**:")
                for rule in task["context"]["business_rules"]:
                    md_content.append(f"  - {rule}")
                md_content.append("")
                md_content.append("- **业务流程**:")
                for workflow in task["context"]["business_workflows"]:
                    md_content.append(f"  - {workflow}")
                md_content.append("")
                md_content.append("- **数据模型**:")
                for model in task["context"]["data_models"]:
                    md_content.append(f"  - {model}")
                md_content.append("")
                md_content.append("- **验证标准**:")
                for criterion in task["validation_criteria"]:
                    md_content.append(f"  - [ ] {criterion}")
                md_content.append("")
                if task["dependencies"]:
                    md_content.append(f"- **依赖任务**: {', '.join(task['dependencies'])}")
                md_content.append("")
                
        # Phase 2: Infrastructure
        md_content.append("## Phase 2: 基础设施完善")
        md_content.append("")
        
        for task in self.generated_tasks["phase_2_infrastructure"]:
            md_content.append(f"### 任务 {task['task_id']}")
            md_content.append(f"- **描述**: {task['description']}")
            md_content.append(f"- **模块**: {task['module']}")
            md_content.append("")
            md_content.append("- **业务规则**:")
            for rule in task["context"]["business_rules"]:
                md_content.append(f"  - {rule}")
            md_content.append("")
            md_content.append("- **验证标准**:")
            for criterion in task["validation_criteria"]:
                md_content.append(f"  - [ ] {criterion}")
            md_content.append("")
            
        # Phase 3: Security Vulnerability Inventory
        md_content.append("## Phase 3: 安全漏洞修复")
        md_content.append("")
        md_content.append("> **注意**: 这些任务在 Phase 3 执行，但需要完整的漏洞清单用于风险评估")
        md_content.append("")
        
        for task in self.generated_tasks["phase_3_security_fixes"]:
            md_content.append(f"### 漏洞 {task['task_id']}")
            md_content.append(f"- **类型**: {task['vulnerability_details']['type']}")
            md_content.append(f"- **严重性**: {task['vulnerability_details']['severity']}")
            md_content.append(f"- **描述**: {task['vulnerability_details']['description']}")
            md_content.append("- **位置**:")
            for location in task['vulnerability_details']['locations']:
                md_content.append(f"  - {location}")
            md_content.append(f"- **修复方案**: {task['vulnerability_details']['remediation']}")
            md_content.append("")
            
        return "\n".join(md_content)
        
    def generate_json_output(self) -> Dict:
        """Generate JSON output"""
        print("💾 Generating JSON output...")
        
        return {
            "project": "dms-erp",
            "ai_execution_plan": {
                "phase_1_core_functionality": self.generated_tasks["phase_1_core_functionality"],
                "phase_2_infrastructure": self.generated_tasks["phase_2_infrastructure"], 
                "phase_3_security_fixes": self.generated_tasks["phase_3_security_fixes"]
            },
            "metadata": {
                "generated_at": "2026-03-24T20:02:00Z",
                "source_analysis_dir": str(self.analysis_dir),
                "total_tasks": sum(len(tasks) for tasks in self.generated_tasks.values()),
                "philosophy": "business_function_decomposition_language_agnostic"
            }
        }
        
    def save_outputs(self):
        """Save both markdown and JSON outputs"""
        print("💾 Saving outputs...")
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save markdown
        md_content = self.generate_markdown_output()
        md_file = self.output_dir / "ai_execution_plan.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        # Save JSON
        json_content = self.generate_json_output()
        json_file = self.output_dir / "ai_execution_plan.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Saved outputs to {self.output_dir}")
        print(f"   - Markdown: {md_file}")
        print(f"   - JSON: {json_file}")
        
    def run(self):
        """Main execution method"""
        print("🚀 Starting AI Plan Generator v2 (Business Function Focused)...")
        
        try:
            self.parse_analysis_results()
            self.generate_tasks()
            self.save_outputs()
            
            print("🎉 AI Plan Generator v2 completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during execution: {e}")
            raise

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Plan Generator v2")
    parser.add_argument("analysis_dir", help="Path to Code Archaeology analysis results directory")
    parser.add_argument("--output-dir", "-o", help="Output directory for generated plans")
    
    args = parser.parse_args()
    
    generator = AIPlanGeneratorV2(args.analysis_dir, args.output_dir)
    generator.run()

if __name__ == "__main__":
    main()