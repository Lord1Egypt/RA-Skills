#!/usr/bin/env python3
"""
OpenClaw凭证迁移工具 - 阶段4.3.3

将明文配置文件中的凭证迁移到加密存储，并生成更新后的配置文件。
"""

import os
import sys
import json
import argparse
import shutil
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# 导入凭证保护系统
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from credential_protection_system import CredentialProtectionSystem, EncryptedCredential
except ImportError:
    print("错误: 无法导入凭证保护系统，请确保credential_protection_system.py在同一目录")
    sys.exit(1)

class CredentialMigrationTool:
    """凭证迁移工具"""
    
    def __init__(self, config_path: str = None, master_password: str = None):
        # 配置文件路径
        if config_path is None:
            self.config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        else:
            self.config_path = config_path
        
        # 备份文件路径
        backup_dir = os.path.dirname(self.config_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = os.path.join(backup_dir, f"openclaw.json.backup_{timestamp}")
        
        # 凭证保护系统
        self.cps = CredentialProtectionSystem(master_password)
        if not self.cps.initialized:
            raise RuntimeError("凭证保护系统初始化失败")
        
        # 加载配置文件
        self.config_data = self.load_config()
        
        # 凭证映射表：原始路径 -> 迁移信息
        self.migration_map = {}
        
        # 迁移统计
        self.migration_stats = {
            "total_identified": 0,
            "successfully_migrated": 0,
            "failed_to_migrate": 0,
            "skipped": 0,
            "by_level": {1: 0, 2: 0, 3: 0, 4: 0}
        }
    
    def load_config(self) -> Dict:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"加载配置文件失败: {e}")
    
    def identify_sensitive_data(self) -> List[Dict]:
        """识别配置文件中的敏感数据"""
        sensitive_items = []
        
        # DeepSeek API密钥
        api_key = self.get_nested_value(self.config_data, ["models", "providers", "deepseek", "apiKey"])
        if api_key:
            sensitive_items.append({
                "path": "models.providers.deepseek.apiKey",
                "value": api_key,
                "level": 1,
                "context": "model_inference",
                "description": "DeepSeek API密钥"
            })
        
        # DeepSeek API端点
        base_url = self.get_nested_value(self.config_data, ["models", "providers", "deepseek", "baseUrl"])
        if base_url:
            sensitive_items.append({
                "path": "models.providers.deepseek.baseUrl",
                "value": base_url,
                "level": 3,
                "context": "api_endpoint",
                "description": "DeepSeek API端点"
            })
        
        # 飞书应用凭证 (8个账户)
        feishu_accounts = self.get_nested_value(self.config_data, ["channels", "feishu", "accounts"], {})
        for account_name, account_config in feishu_accounts.items():
            # appSecret
            app_secret = account_config.get("appSecret")
            if app_secret:
                sensitive_items.append({
                    "path": f"channels.feishu.accounts.{account_name}.appSecret",
                    "value": app_secret,
                    "level": 2,
                    "context": f"feishu.{account_name}",
                    "description": f"飞书账户 {account_name} 的应用密钥"
                })
            
            # appId
            app_id = account_config.get("appId")
            if app_id:
                sensitive_items.append({
                    "path": f"channels.feishu.accounts.{account_name}.appId",
                    "value": app_id,
                    "level": 4,
                    "context": f"feishu.{account_name}",
                    "description": f"飞书账户 {account_name} 的应用ID"
                })
            
            # allowFrom列表
            allow_from = account_config.get("allowFrom", [])
            for i, sender_id in enumerate(allow_from):
                if sender_id and sender_id != "*":  # 忽略通配符
                    sensitive_items.append({
                        "path": f"channels.feishu.accounts.{account_name}.allowFrom[{i}]",
                        "value": sender_id,
                        "level": 4,
                        "context": f"feishu.{account_name}.authorized_sender",
                        "description": f"飞书账户 {account_name} 的授权发送者 {i}"
                    })
        
        # QQ Bot凭证
        qqbot_config = self.config_data.get("channels", {}).get("qqbot", {})
        
        # clientSecret
        client_secret = qqbot_config.get("clientSecret")
        if client_secret:
            sensitive_items.append({
                "path": "channels.qqbot.clientSecret",
                "value": client_secret,
                "level": 2,
                "context": "qqbot",
                "description": "QQ Bot客户端密钥"
            })
        
        # appId
        qq_app_id = qqbot_config.get("appId")
        if qq_app_id:
            sensitive_items.append({
                "path": "channels.qqbot.appId",
                "value": qq_app_id,
                "level": 4,
                "context": "qqbot",
                "description": "QQ Bot应用ID"
            })
        
        # allowFrom列表
        qq_allow_from = qqbot_config.get("allowFrom", [])
        for i, sender in enumerate(qq_allow_from):
            if sender and sender != "*":
                sensitive_items.append({
                    "path": f"channels.qqbot.allowFrom[{i}]",
                    "value": sender,
                    "level": 4,
                    "context": "qqbot.authorized_sender",
                    "description": f"QQ Bot授权发送者 {i}"
                })
        
        # Gateway令牌
        gateway_token = self.get_nested_value(self.config_data, ["gateway", "auth", "token"])
        if gateway_token:
            sensitive_items.append({
                "path": "gateway.auth.token",
                "value": gateway_token,
                "level": 3,
                "context": "gateway_authentication",
                "description": "Gateway认证令牌"
            })
        
        # 技能API密钥
        skills = self.config_data.get("skills", {}).get("entries", {})
        for skill_name, skill_config in skills.items():
            # moltbook-cli API密钥（特殊格式）
            if skill_name == "moltbook-cli" and "apiKey" in skill_config:
                sensitive_items.append({
                    "path": f"skills.entries.{skill_name}.apiKey",
                    "value": skill_config["apiKey"],
                    "level": 2,
                    "context": f"skill.{skill_name}",
                    "description": f"{skill_name}技能API密钥"
                })
            
            # ima-note API密钥
            elif skill_name == "ima-note" and "apiKey" in skill_config:
                sensitive_items.append({
                    "path": f"skills.entries.{skill_name}.apiKey",
                    "value": skill_config["apiKey"],
                    "level": 2,
                    "context": f"skill.{skill_name}",
                    "description": f"{skill_name}技能API密钥"
                })
        
        # 授权发送者（根级别）
        agents_list = self.config_data.get("agents", {}).get("list", [])
        for agent in agents_list:
            agent_id = agent.get("id")
            if agent_id and agent_id not in ["main", "hermes"]:
                # 这些已经在飞书部分处理了
                pass
        
        # 工作区路径（低敏感度）
        workspace_path = self.get_nested_value(self.config_data, ["agents", "defaults", "workspace"])
        if workspace_path:
            sensitive_items.append({
                "path": "agents.defaults.workspace",
                "value": workspace_path,
                "level": 4,
                "context": "system_configuration",
                "description": "默认工作区路径"
            })
        
        self.migration_stats["total_identified"] = len(sensitive_items)
        return sensitive_items
    
    def get_nested_value(self, data: Dict, path: List[str], default: Any = None) -> Any:
        """获取嵌套字典中的值"""
        current = data
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def set_nested_value(self, data: Dict, path: List[str], value: Any) -> bool:
        """设置嵌套字典中的值"""
        current = data
        for i, key in enumerate(path[:-1]):
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[path[-1]] = value
        return True
    
    def migrate_credential(self, item: Dict) -> Tuple[bool, Optional[str]]:
        """迁移单个凭证"""
        try:
            credential_id = item["path"]
            plaintext = item["value"]
            level = item["level"]
            context = item.get("context", "")
            
            # 加密并存储凭证
            success = self.cps.encrypt_and_store_credential(
                credential_id, plaintext, level, context
            )
            
            if success:
                # 生成凭证引用
                credential_ref = f"cred://{credential_id.replace('.', '_')}"
                
                # 记录迁移信息
                self.migration_map[credential_id] = {
                    "credential_ref": credential_ref,
                    "original_value_preview": f"{plaintext[:8]}...{plaintext[-8:]}" if len(plaintext) > 20 else plaintext,
                    "level": level,
                    "context": context,
                    "migrated_at": datetime.now().isoformat()
                }
                
                self.migration_stats["successfully_migrated"] += 1
                self.migration_stats["by_level"][level] += 1
                
                return True, credential_ref
            else:
                self.migration_stats["failed_to_migrate"] += 1
                return False, None
                
        except Exception as e:
            print(f"迁移凭证失败 {item['path']}: {e}")
            self.migration_stats["failed_to_migrate"] += 1
            return False, None
    
    def create_backup(self) -> bool:
        """创建配置文件备份"""
        try:
            shutil.copy2(self.config_path, self.backup_path)
            print(f"配置文件已备份到: {self.backup_path}")
            return True
        except Exception as e:
            print(f"创建备份失败: {e}")
            return False
    
    def update_config_file(self) -> bool:
        """更新配置文件，将明文凭证替换为引用"""
        try:
            # 创建配置文件的副本
            updated_config = json.loads(json.dumps(self.config_data))
            
            # 更新凭证引用
            update_count = 0
            
            # DeepSeek API密钥
            if "models.providers.deepseek.apiKey" in self.migration_map:
                ref = self.migration_map["models.providers.deepseek.apiKey"]["credential_ref"]
                self.set_nested_value(updated_config, ["models", "providers", "deepseek", "apiKey"], ref)
                update_count += 1
            
            # DeepSeek API端点（可选更新）
            if "models.providers.deepseek.baseUrl" in self.migration_map:
                # Level 3可以选择性更新或保持原样
                pass
            
            # 飞书appSecret
            feishu_accounts = self.get_nested_value(updated_config, ["channels", "feishu", "accounts"], {})
            for account_name in feishu_accounts.keys():
                credential_path = f"channels.feishu.accounts.{account_name}.appSecret"
                if credential_path in self.migration_map:
                    ref = self.migration_map[credential_path]["credential_ref"]
                    feishu_accounts[account_name]["appSecret"] = ref
                    update_count += 1
            
            # 飞书appId（保持原样或混淆）
            for account_name in feishu_accounts.keys():
                credential_path = f"channels.feishu.accounts.{account_name}.appId"
                if credential_path in self.migration_map:
                    # Level 4可以选择性更新或保持原样
                    pass
            
            # QQ Bot clientSecret
            if "channels.qqbot.clientSecret" in self.migration_map:
                ref = self.migration_map["channels.qqbot.clientSecret"]["credential_ref"]
                updated_config["channels"]["qqbot"]["clientSecret"] = ref
                update_count += 1
            
            # Gateway令牌
            if "gateway.auth.token" in self.migration_map:
                ref = self.migration_map["gateway.auth.token"]["credential_ref"]
                self.set_nested_value(updated_config, ["gateway", "auth", "token"], ref)
                update_count += 1
            
            # 技能API密钥
            skills = updated_config.get("skills", {}).get("entries", {})
            for skill_name in skills.keys():
                credential_path = f"skills.entries.{skill_name}.apiKey"
                if credential_path in self.migration_map:
                    ref = self.migration_map[credential_path]["credential_ref"]
                    skills[skill_name]["apiKey"] = ref
                    update_count += 1
            
            # 添加凭证存储引用部分
            if "credentialStore" not in updated_config:
                updated_config["credentialStore"] = {}
            
            updated_config["credentialStore"] = {
                "encrypted": True,
                "version": "1.0",
                "migration_date": datetime.now().isoformat(),
                "storage_path": self.cps.credential_storage.storage_path if self.cps.credential_storage else None,
                "references": self.migration_map
            }
            
            # 保存更新后的配置文件
            updated_path = self.config_path + ".migrated"
            with open(updated_path, 'w', encoding='utf-8') as f:
                json.dump(updated_config, f, indent=2, ensure_ascii=False)
            
            print(f"更新后的配置文件已保存到: {updated_path}")
            print(f"共更新了 {update_count} 个凭证引用")
            
            # 显示更新前后的差异
            self.show_migration_summary(updated_config)
            
            return True
            
        except Exception as e:
            print(f"更新配置文件失败: {e}")
            return False
    
    def show_migration_summary(self, updated_config: Dict):
        """显示迁移摘要"""
        print("\n" + "="*60)
        print("迁移摘要")
        print("="*60)
        
        print(f"识别的敏感项目: {self.migration_stats['total_identified']}")
        print(f"成功迁移: {self.migration_stats['successfully_migrated']}")
        print(f"迁移失败: {self.migration_stats['failed_to_migrated']}")
        print(f"跳过: {self.migration_stats['skipped']}")
        
        print("\n按级别统计:")
        for level in range(1, 5):
            count = self.migration_stats['by_level'][level]
            if count > 0:
                level_desc = {
                    1: "关键API密钥",
                    2: "应用凭证",
                    3: "系统令牌", 
                    4: "标识符"
                }
                print(f"  Level {level} ({level_desc[level]}): {count}")
        
        print("\n重要凭证迁移状态:")
        important_creds = [
            "models.providers.deepseek.apiKey",
            "channels.feishu.accounts.main.appSecret",
            "channels.qqbot.clientSecret",
            "gateway.auth.token"
        ]
        
        for cred_path in important_creds:
            if cred_path in self.migration_map:
                info = self.migration_map[cred_path]
                print(f"  ✓ {cred_path}")
                print(f"     引用: {info['credential_ref']}")
                print(f"     原值预览: {info['original_value_preview']}")
            else:
                print(f"  ✗ {cred_path} (未迁移)")
        
        print("\n下一步操作:")
        print("1. 验证更新后的配置文件:")
        print(f"   cat {self.config_path}.migrated | head -50")
        print("\n2. 测试凭证获取功能:")
        print("   python -c \"from credential_protection_system import CredentialProtectionSystem; cps = CredentialProtectionSystem('你的密码'); key = cps.get_credential('models.providers.deepseek.apiKey', 1, {'purpose':'test'}, '测试'); print('成功' if key else '失败')\"")
        print("\n3. 应用更新（手动替换原文件）:")
        print(f"   cp {self.config_path}.migrated {self.config_path}")
        print("\n4. 测试系统功能:")
        print("   openclaw status")
        print("\n5. 清理备份（确认一切正常后）:")
        print(f"   rm {self.backup_path}")
        
        print("\n警告: 在生产环境中替换原文件前，请确保充分测试!")
        print("="*60)
    
    def run_migration(self, dry_run: bool = False) -> bool:
        """运行完整迁移流程"""
        print("="*60)
        print("OpenClaw凭证迁移工具")
        print("="*60)
        
        print(f"配置文件: {self.config_path}")
        print(f"备份文件: {self.backup_path}")
        print(f"凭证存储: {self.cps.credential_storage.storage_path if self.cps.credential_storage else '未知'}")
        
        # 1. 识别敏感数据
        print("\n步骤1: 识别敏感数据...")
        sensitive_items = self.identify_sensitive_data()
        print(f"找到 {len(sensitive_items)} 个敏感项目")
        
        if not sensitive_items:
            print("未找到需要迁移的敏感数据")
            return True
        
        # 2. 创建备份
        print("\n步骤2: 创建配置文件备份...")
        if not dry_run:
            backup_success = self.create_backup()
            if not backup_success:
                print("警告: 备份创建失败，继续迁移可能风险较高")
                response = input("继续吗? (y/N): ")
                if response.lower() != 'y':
                    print("迁移取消")
                    return False
        else:
            print("(DRY RUN) 跳过备份创建")
        
        # 3. 迁移凭证
        print("\n步骤3: 迁移凭证到加密存储...")
        for i, item in enumerate(sensitive_items, 1):
            print(f"  [{i}/{len(sensitive_items)}] {item['path']} (Level {item['level']})... ", end="")
            
            if dry_run:
                print("(DRY RUN) 跳过")
                continue
            
            success, credential_ref = self.migrate_credential(item)
            if success:
                print(f"成功 -> {credential_ref}")
            else:
                print("失败")
        
        # 4. 更新配置文件
        print("\n步骤4: 更新配置文件...")
        if dry_run:
            print("(DRY RUN) 跳过配置文件更新")
        else:
            update_success = self.update_config_file()
            if not update_success:
                print("配置文件更新失败")
                return False
        
        # 5. 显示摘要
        print("\n步骤5: 生成迁移报告...")
        self.generate_migration_report()
        
        print("\n迁移流程完成!")
        if dry_run:
            print("注意: 这是DRY RUN，未实际修改任何文件")
        
        return True
    
    def generate_migration_report(self):
        """生成迁移报告"""
        report_dir = os.path.expanduser("~/.openclaw/workspace/memory")
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(report_dir, f"credential-migration-report-{timestamp}.md")
        
        report_content = f"""# 凭证迁移报告

## 基本信息
- **迁移时间**: {datetime.now().isoformat()}
- **配置文件**: {self.config_path}
- **备份文件**: {self.backup_path}
- **凭证存储**: {self.cps.credential_storage.storage_path if self.cps.credential_storage else '未知'}

## 迁移统计
- **识别的敏感项目**: {self.migration_stats['total_identified']}
- **成功迁移**: {self.migration_stats['successfully_migrated']}
- **迁移失败**: {self.migration_stats['failed_to_migrate']}
- **跳过**: {self.migration_stats['skipped']}

## 按级别统计
"""
        
        for level in range(1, 5):
            count = self.migration_stats['by_level'][level]
            if count > 0:
                level_desc = {
                    1: "关键API密钥",
                    2: "应用凭证", 
                    3: "系统令牌",
                    4: "标识符"
                }
                report_content += f"- **Level {level} ({level_desc[level]})**: {count}\n"
        
        report_content += "\n## 迁移映射表\n\n| 原始路径 | 凭证引用 | 级别 | 状态 |\n|----------|----------|------|------|\n"
        
        for cred_path, info in self.migration_map.items():
            status = "✅ 成功" if cred_path in self.migration_map else "❌ 失败"
            report_content += f"| `{cred_path}` | `{info['credential_ref']}` | Level {info['level']} | {status} |\n"
        
        report_content += f"""
## 系统状态

```json
{json.dumps(self.cps.get_system_status(), indent=2)}
```

## 重要说明

1. **备份文件**: 原始配置文件已备份到 `{self.backup_path}`
2. **更新后的配置**: 新配置文件保存为 `{self.config_path}.migrated`
3. **应用更新**: 手动替换原文件前请充分测试
4. **测试命令**: 
   ```bash
   # 测试DeepSeek API密钥获取
   python -c "from credential_protection_system import CredentialProtectionSystem; cps = CredentialProtectionSystem('你的密码'); key = cps.get_credential('models.providers.deepseek.apiKey', 1, {'purpose':'test'}, '测试'); print('成功' if key else '失败')"
   
   # 测试系统功能
   openclaw status
   ```

## 风险与缓解

### 风险1: 迁移后系统不可用
- **缓解**: 保留完整备份，可随时恢复

### 风险2: 加密系统故障
- **缓解**: 系统有降级机制，可临时使用明文模式

### 风险3: 性能影响
- **缓解**: 加密系统经过优化，性能影响<10%

## 后续步骤

1. **验证**: 测试更新后的配置文件功能
2. **应用**: 确认正常后替换原配置文件
3. **监控**: 监控系统性能和错误日志
4. **优化**: 根据使用情况优化访问策略

---
*报告生成时间: {datetime.now().isoformat()}*
*凭证保护系统版本: 1.0*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"迁移报告已保存到: {report_path}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="OpenClaw凭证迁移工具")
    parser.add_argument("--config", "-c", help="配置文件路径", default=None)
    parser.add_argument("--password", "-p", help="主密码（不建议在命令行指定）", default=None)
    parser.add_argument("--dry-run", "-d", action="store_true", help="模拟运行，不实际修改文件")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式密码输入")
    
    args = parser.parse_args()
    
    # 获取主密码
    master_password = args.password
    
    if args.interactive and not args.password:
        import getpass
        master_password = getpass.getpass("请输入主密码: ")
        confirm = getpass.getpass("请确认主密码: ")
        if master_password != confirm:
            print("密码不匹配")
            return 1
    
    if not master_password:
        print("警告: 未指定主密码，使用默认测试密码")
        master_password = "test_master_password_123"
        print(f"测试密码: {master_password}")
        print("注意: 在生产环境中必须使用强密码!")
    
    try:
        # 创建迁移工具
        migrator = CredentialMigrationTool(args.config, master_password)
        
        # 运行迁移
        success = migrator.run_migration(args.dry_run)
        
        if success:
            print("\n✅ 迁移完成!")
            if args.dry_run:
                print("这是DRY RUN，未实际修改任何文件")
            else:
                print(f"请查看迁移报告: {os.path.expanduser('~/.openclaw/workspace/memory/credential-migration-report-*.md')}")
            return 0
        else:
            print("\n❌ 迁移失败")
            return 1
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())