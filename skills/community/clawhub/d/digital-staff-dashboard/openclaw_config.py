#!/usr/bin/env python3
"""
OpenClaw Configuration Manager
管理 OpenClaw 的配置文件读写，支持 Agent 创建和配置同步

集成 OpenClaw 官方 JSON Schema 验证，确保配置合法性
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from openclaw_finder import get_finder
from openclaw_schema import (
    validate_config as validate_openclaw_config,
    validate_agent_config as validate_openclaw_agent_config,
    RESERVED_KEYWORDS,
    AGENT_ID_PATTERN,
    AGENT_ID_MAX_LENGTH
)


class OpenClawConfigManager:
    """OpenClaw 配置管理器 - 集成官方 Schema 验证"""
    
    def __init__(self, skip_validation: bool = False):
        self.finder = get_finder()
        self.openclaw_home = self.finder.find_primary()
        
        if not self.openclaw_home:
            raise RuntimeError("OpenClaw installation not found")
        
        self.config_file = self.openclaw_home / "openclaw.json"
        self.agents_dir = self.openclaw_home / "agents"
        self.backup_dir = self.openclaw_home / ".dashboard-backups"
        self.skip_validation = skip_validation
        
        # 确保备份目录存在
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证 OpenClaw 配置是否符合官方 Schema
        
        Returns:
            {"valid": bool, "errors": [], "warnings": []}
        """
        if self.skip_validation:
            return {"valid": True, "errors": [], "warnings": []}
        return validate_openclaw_config(config)
    
    def validate_agent_config(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证单个 Agent 配置是否符合官方 Schema
        
        Returns:
            {"valid": bool, "errors": [], "warnings": []}
        """
        if self.skip_validation:
            return {"valid": True, "errors": [], "warnings": []}
        return validate_openclaw_agent_config(agent_config)
    
    def check_agent_name_valid(self, name: str) -> Dict[str, Any]:
        """
        检查 agent 名称是否合法
        
        Returns:
            {"valid": bool, "error": str|None, "warnings": []}
        """
        errors = []
        warnings = []
        
        # 检查空值
        if not name or not isinstance(name, str):
            return {"valid": False, "error": "Agent 名称不能为空", "warnings": []}
        
        # 检查长度
        if len(name) > AGENT_ID_MAX_LENGTH:
            errors.append(f"名称长度不能超过 {AGENT_ID_MAX_LENGTH} 字符")
        
        # 检查命名规则
        if not AGENT_ID_PATTERN.match(name):
            errors.append(
                f"命名不合法: 必须以字母开头，只能包含字母、数字、连字符(-)和下划线(_)"
            )
        
        # 检查保留字
        if name.lower() in RESERVED_KEYWORDS:
            errors.append(f"'{name}' 是保留字，不能使用")
        
        # 检查常见非法模式
        if name.startswith("-") or name.startswith("_"):
            errors.append("名称不能以连字符或下划线开头")
        
        if name.endswith("-") or name.endswith("_"):
            warnings.append("名称以连字符或下划线结尾，虽然合法但不推荐")
        
        # 检查连续特殊字符
        if "--" in name or "__" in name:
            warnings.append("名称包含连续的连字符或下划线，虽然合法但不推荐")
        
        if errors:
            return {
                "valid": False,
                "error": "; ".join(errors),
                "warnings": warnings
            }
        
        return {"valid": True, "error": None, "warnings": warnings}
    
    def read_global_config(self) -> Dict[str, Any]:
        """读取 OpenClaw 全局配置"""
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[OpenClawConfig] 读取全局配置失败: {e}")
            return {}
    
    def backup_config(self) -> Optional[Path]:
        """备份 OpenClaw 配置文件"""
        if not self.config_file.exists():
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"openclaw.json.backup.{timestamp}"
            
            shutil.copy2(self.config_file, backup_file)
            
            # 保留最近 10 个备份，删除旧的
            backups = sorted(self.backup_dir.glob("openclaw.json.backup.*"))
            for old_backup in backups[:-10]:
                old_backup.unlink()
            
            print(f"[OpenClawConfig] 配置已备份到: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"[OpenClawConfig] 备份配置失败: {e}")
            return None
    
    def write_global_config(self, config: Dict[str, Any], validate: bool = True) -> bool:
        """
        写入 OpenClaw 全局配置（带备份和可选验证）
        
        Args:
            config: 要写入的配置
            validate: 是否进行 schema 验证（默认开启）
        """
        try:
            # Schema 验证
            if validate and not self.skip_validation:
                result = self.validate_config(config)
                if not result["valid"]:
                    print(f"[OpenClawConfig] 配置验证失败:")
                    for error in result["errors"]:
                        print(f"  - {error}")
                    return False
                if result["warnings"]:
                    print(f"[OpenClawConfig] 配置警告:")
                    for warning in result["warnings"]:
                        print(f"  - {warning}")
            
            # 先备份
            self.backup_config()
            
            # 更新 meta 信息
            if "meta" not in config:
                config["meta"] = {}
            config["meta"]["lastTouchedAt"] = datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"[OpenClawConfig] 配置已写入: {self.config_file}")
            return True
        except Exception as e:
            print(f"[OpenClawConfig] 写入全局配置失败: {e}")
            return False
    
    def add_agent_to_config(self, agent_name: str, agent_config: Dict[str, Any], 
                             validate: bool = True,
                             add_to_subagents: bool = True,
                             add_to_agent_to_agent: bool = True) -> bool:
        """
        添加 Agent 到 OpenClaw 全局配置
        
        Args:
            agent_name: Agent 名称
            agent_config: Agent 配置数据
            validate: 是否进行 schema 验证
            add_to_subagents: 是否将新 agent 添加到其他 agent 的 subagents.allowAgents 中
            add_to_agent_to_agent: 是否将新 agent 添加到 tools.agentToAgent.allow 中
        """
        try:
            # 验证 agent 名称
            name_check = self.check_agent_name_valid(agent_name)
            if not name_check["valid"]:
                print(f"[OpenClawConfig] Agent 名称验证失败: {name_check['error']}")
                return False
            
            config = self.read_global_config()
            
            # 确保 agents 部分存在
            if "agents" not in config:
                config["agents"] = {}
            if "list" not in config["agents"]:
                config["agents"]["list"] = []
            
            agent_list = config["agents"]["list"]
            
            # 检查是否已存在
            existing_idx = None
            for idx, agent in enumerate(agent_list):
                if agent.get("id") == agent_name:
                    existing_idx = idx
                    break
            
            # 构建 agent 配置
            new_agent_config = {
                "id": agent_name,
                "name": agent_name,
                "workspace": str(self.openclaw_home / f"workspace-{agent_name}"),
                "agentDir": str(self.agents_dir / agent_name / "agent"),
                "model": f"{agent_config.get('model_provider', 'deepseek')}/{agent_config.get('model_id', 'deepseek-chat')}",
                "identity": {
                    "name": agent_config.get("display_name", agent_name),
                    "emoji": agent_config.get("emoji", "🤖")
                }
            }
            
            # Schema 验证
            if validate and not self.skip_validation:
                result = self.validate_agent_config(new_agent_config)
                if not result["valid"]:
                    print(f"[OpenClawConfig] Agent 配置验证失败:")
                    for error in result["errors"]:
                        print(f"  - {error}")
                    return False
                if result["warnings"]:
                    for warning in result["warnings"]:
                        print(f"[OpenClawConfig] 警告: {warning}")
            
            # Note: system prompt 不保存在 openclaw.json 中
            # 它只保存在 metadata.json 中供 Dashboard 使用
            # OpenClaw 从 sessions 或 AGENTS.md 读取 system prompt
            
            is_new_agent = existing_idx is None
            
            # 添加或更新
            if existing_idx is not None:
                # 保留原有配置，只更新指定字段
                existing = agent_list[existing_idx]
                existing.update(new_agent_config)
                print(f"[OpenClawConfig] 更新现有 agent 配置: {agent_name}")
            else:
                agent_list.append(new_agent_config)
                print(f"[OpenClawConfig] 添加新 agent 配置: {agent_name}")
            
            # 新 agent 需要同步到 subagents 和 agentToAgent
            if is_new_agent:
                # 1. 将新 agent 添加到所有现有 agent 的 subagents.allowAgents 中
                if add_to_subagents:
                    for agent in agent_list:
                        if agent.get("id") != agent_name:  # 不添加到自己
                            if "subagents" not in agent:
                                agent["subagents"] = {}
                            if "allowAgents" not in agent["subagents"]:
                                agent["subagents"]["allowAgents"] = []
                            if agent_name not in agent["subagents"]["allowAgents"]:
                                agent["subagents"]["allowAgents"].append(agent_name)
                                print(f"[OpenClawConfig] 将 {agent_name} 添加到 {agent['id']}.subagents.allowAgents")
                    
                    # 同时添加到 defaults.subagents.allowAgents（如果存在 defaults）
                    defaults = config.get("agents", {}).get("defaults", {})
                    if defaults:
                        if "subagents" not in defaults:
                            defaults["subagents"] = {}
                        if "allowAgents" not in defaults["subagents"]:
                            defaults["subagents"]["allowAgents"] = []
                        if agent_name not in defaults["subagents"]["allowAgents"]:
                            defaults["subagents"]["allowAgents"].append(agent_name)
                            print(f"[OpenClawConfig] 将 {agent_name} 添加到 agents.defaults.subagents.allowAgents")
                
                # 2. 将新 agent 添加到 tools.agentToAgent.allow
                if add_to_agent_to_agent:
                    if "tools" not in config:
                        config["tools"] = {}
                    if "agentToAgent" not in config["tools"]:
                        config["tools"]["agentToAgent"] = {"enabled": True, "allow": []}
                    
                    # 确保 enabled 为 true
                    config["tools"]["agentToAgent"]["enabled"] = True
                    
                    if "allow" not in config["tools"]["agentToAgent"]:
                        config["tools"]["agentToAgent"]["allow"] = []
                    if agent_name not in config["tools"]["agentToAgent"]["allow"]:
                        config["tools"]["agentToAgent"]["allow"].append(agent_name)
                        print(f"[OpenClawConfig] 将 {agent_name} 添加到 tools.agentToAgent.allow，并确保 enabled=true")
            
            # 写入配置
            return self.write_global_config(config, validate=validate)
        
        except Exception as e:
            print(f"[OpenClawConfig] 添加 agent 到配置失败: {e}")
            return False
    
    def remove_agent_from_config(self, agent_name: str,
                                   remove_from_subagents: bool = True,
                                   remove_from_agent_to_agent: bool = True) -> bool:
        """
        从 OpenClaw 全局配置中移除 Agent
        
        Args:
            agent_name: Agent 名称
            remove_from_subagents: 是否从其他 agent 的 subagents.allowAgents 中移除
            remove_from_agent_to_agent: 是否从 tools.agentToAgent.allow 中移除
        """
        try:
            config = self.read_global_config()
            
            if "agents" not in config or "list" not in config["agents"]:
                return True
            
            agent_list = config["agents"]["list"]
            original_len = len(agent_list)
            
            # 过滤掉要删除的 agent
            config["agents"]["list"] = [
                a for a in agent_list 
                if a.get("id") != agent_name
            ]
            
            if len(config["agents"]["list"]) < original_len:
                print(f"[OpenClawConfig] 从配置中移除 agent: {agent_name}")
                
                # 从其他 agent 的 subagents.allowAgents 中移除
                if remove_from_subagents:
                    for agent in config["agents"]["list"]:
                        if "subagents" in agent and "allowAgents" in agent["subagents"]:
                            if agent_name in agent["subagents"]["allowAgents"]:
                                agent["subagents"]["allowAgents"].remove(agent_name)
                                print(f"[OpenClawConfig] 从 {agent['id']}.subagents.allowAgents 移除 {agent_name}")
                    
                    # 从 defaults.subagents.allowAgents 中移除
                    defaults = config.get("agents", {}).get("defaults", {})
                    if defaults and "subagents" in defaults and "allowAgents" in defaults["subagents"]:
                        if agent_name in defaults["subagents"]["allowAgents"]:
                            defaults["subagents"]["allowAgents"].remove(agent_name)
                            print(f"[OpenClawConfig] 从 agents.defaults.subagents.allowAgents 移除 {agent_name}")
                
                # 从 tools.agentToAgent.allow 中移除
                if remove_from_agent_to_agent:
                    tools_config = config.get("tools", {})
                    if "agentToAgent" in tools_config and "allow" in tools_config["agentToAgent"]:
                        if agent_name in tools_config["agentToAgent"]["allow"]:
                            tools_config["agentToAgent"]["allow"].remove(agent_name)
                            print(f"[OpenClawConfig] 从 tools.agentToAgent.allow 移除 {agent_name}")
                
                return self.write_global_config(config)
            
            return True
        
        except Exception as e:
            print(f"[OpenClawConfig] 从配置中移除 agent 失败: {e}")
            return False
    
    def read_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """读取指定 agent 的配置"""
        agent_dir = self.agents_dir / agent_name
        config_file = agent_dir / "agent" / "models.json"
        
        if not config_file.exists():
            return {}
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[OpenClawConfig] 读取 agent {agent_name} 配置失败: {e}")
            return {}
    
    def write_agent_config(self, agent_name: str, config: Dict[str, Any]) -> bool:
        """写入指定 agent 的配置"""
        agent_dir = self.agents_dir / agent_name
        config_file = agent_dir / "agent" / "models.json"
        
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[OpenClawConfig] 写入 agent {agent_name} 配置失败: {e}")
            return False
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """获取所有 agent 列表"""
        agents = []
        
        if not self.agents_dir.exists():
            return agents
        
        for agent_dir in sorted(self.agents_dir.iterdir()):
            if agent_dir.is_dir():
                agent_name = agent_dir.name
                config = self.read_agent_config(agent_name)
                
                # 检查是否有 sessions
                sessions_file = agent_dir / "sessions" / "sessions.json"
                has_sessions = sessions_file.exists()
                
                # 检查是否有头像
                avatar_file = agent_dir / "avatar.png"
                has_avatar = avatar_file.exists()
                
                agents.append({
                    "name": agent_name,
                    "config": config,
                    "has_sessions": has_sessions,
                    "has_avatar": has_avatar,
                    "path": str(agent_dir)
                })
        
        return agents
    
    def create_agent(self, agent_name: str, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新的 agent，完整配置到 OpenClaw
        
        Args:
            agent_name: agent 名称
            agent_data: agent 配置数据
        
        Returns:
            创建结果
        """
        # 验证 agent 名称（使用官方命名规则）
        name_check = self.check_agent_name_valid(agent_name)
        if not name_check["valid"]:
            return {"success": False, "error": f"非法的 Agent 名称: {name_check['error']}"}
        
        if name_check["warnings"]:
            for warning in name_check["warnings"]:
                print(f"[OpenClawConfig] 警告: {warning}")
        
        agent_dir = self.agents_dir / agent_name
        workspace_dir = self.openclaw_home / f"workspace-{agent_name}"
        
        # 检查是否已存在
        if agent_dir.exists():
            return {"success": False, "error": f"Agent '{agent_name}' already exists"}
        
        try:
            # 1. 创建目录结构
            (agent_dir / "agent").mkdir(parents=True, exist_ok=True)
            (agent_dir / "sessions").mkdir(parents=True, exist_ok=True)
            workspace_dir.mkdir(parents=True, exist_ok=True)
            
            # 2. 创建 agent 的模型配置
            model_provider = agent_data.get("model_provider", "deepseek")
            model_id = agent_data.get("model_id", "deepseek-chat")
            
            # 从全局配置获取模型提供商配置
            global_config = self.read_global_config()
            providers = global_config.get("models", {}).get("providers", {})
            
            agent_config = {
                "providers": {}
            }
            
            if model_provider in providers:
                # 复制提供商配置
                provider_config = providers[model_provider].copy()
                # 只保留选中的模型
                provider_config["models"] = [
                    m for m in provider_config.get("models", [])
                    if m.get("id") == model_id
                ]
                if not provider_config["models"]:
                    # 如果没找到指定模型，使用第一个
                    all_models = providers[model_provider].get("models", [])
                    if all_models:
                        provider_config["models"] = [all_models[0]]
                
                agent_config["providers"][model_provider] = provider_config
            
            # 3. 写入 agent 的模型配置
            self.write_agent_config(agent_name, agent_config)
            
            # 4. 创建空的 sessions.json
            sessions_file = agent_dir / "sessions" / "sessions.json"
            with open(sessions_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)
            
            # 5. 创建 metadata 文件存储 Dashboard 特有的元数据
            metadata = {
                "display_name": agent_data.get("display_name", agent_name),
                "role": agent_data.get("role", "Agent"),
                "emoji": agent_data.get("emoji", "🤖"),
                "description": agent_data.get("description", ""),
                "color": agent_data.get("color", "cyan"),
                "system_prompt": agent_data.get("system_prompt", ""),
                "model_provider": model_provider,
                "model_id": model_id,
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            metadata_file = agent_dir / "agent" / "metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # 6. 写入 soul.md 文件（系统提示词）到工作目录
            system_prompt = agent_data.get("system_prompt", "").strip()
            if system_prompt:
                soul_file = workspace_dir / "soul.md"
                with open(soul_file, 'w', encoding='utf-8') as f:
                    f.write(system_prompt)
                print(f"[CreateAgent] soul.md 已创建: {soul_file}")
            
            # 7. 添加到 OpenClaw 全局配置（关键步骤）
            if not self.add_agent_to_config(agent_name, agent_data):
                # 如果添加失败，清理已创建的文件
                if agent_dir.exists():
                    shutil.rmtree(agent_dir)
                if workspace_dir.exists():
                    shutil.rmtree(workspace_dir)
                return {"success": False, "error": "Failed to add agent to OpenClaw config"}
            
            return {
                "success": True,
                "agent_name": agent_name,
                "path": str(agent_dir),
                "workspace": str(workspace_dir),
                "metadata": metadata
            }
        
        except Exception as e:
            # 清理已创建的目录
            if agent_dir.exists():
                shutil.rmtree(agent_dir)
            if workspace_dir.exists():
                shutil.rmtree(workspace_dir)
            return {"success": False, "error": str(e)}
    
    def update_agent_metadata(self, agent_name: str, metadata: Dict[str, Any]) -> bool:
        """更新 agent 的元数据"""
        metadata_file = self.agents_dir / agent_name / "agent" / "metadata.json"
        
        try:
            # 读取现有元数据
            existing = {}
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            
            # 合并更新
            existing.update(metadata)
            existing["updated_at"] = datetime.now().isoformat()
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"[OpenClawConfig] 更新 agent {agent_name} 元数据失败: {e}")
            return False
    
    def read_agent_metadata(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """读取 agent 的元数据"""
        metadata_file = self.agents_dir / agent_name / "agent" / "metadata.json"
        
        if not metadata_file.exists():
            return None
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[OpenClawConfig] 读取 agent {agent_name} 元数据失败: {e}")
            return None
    
    def delete_agent(self, agent_name: str) -> Dict[str, Any]:
        """删除 agent"""
        agent_dir = self.agents_dir / agent_name
        workspace_dir = self.openclaw_home / f"workspace-{agent_name}"
        
        if not agent_dir.exists():
            return {"success": False, "error": f"Agent '{agent_name}' does not exist"}
        
        try:
            # 1. 从 OpenClaw 配置中移除
            if not self.remove_agent_from_config(agent_name):
                return {"success": False, "error": "Failed to remove agent from OpenClaw config"}
            
            # 2. 备份到 trash
            trash_dir = self.openclaw_home / ".trash" / "agents"
            trash_workspace_dir = self.openclaw_home / ".trash" / "workspaces"
            trash_dir.mkdir(parents=True, exist_ok=True)
            trash_workspace_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if agent_dir.exists():
                backup_path = trash_dir / f"{agent_name}_{timestamp}"
                shutil.move(str(agent_dir), str(backup_path))
            
            if workspace_dir.exists():
                backup_workspace = trash_workspace_dir / f"{agent_name}_{timestamp}"
                shutil.move(str(workspace_dir), str(backup_workspace))
            
            return {
                "success": True,
                "message": f"Agent '{agent_name}' moved to trash",
                "backup_path": str(trash_dir / f"{agent_name}_{timestamp}")
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _validate_agent_name(self, name: str) -> bool:
        """
        验证 agent 名称是否合法（向后兼容方法）
        使用官方命名规则进行验证
        """
        result = self.check_agent_name_valid(name)
        return result["valid"]
    
    def sync_agents_to_dashboard(self, dashboard_config_manager) -> Dict[str, Any]:
        """
        从 OpenClaw 读取 agent 配置，仅用于显示，不修改 Dashboard 配置文件
        
        读取 OpenClaw 中所有 agent 的 metadata，生成显示配置，
        但不会写入到 Dashboard 的配置文件中（data/config.json）
        
        如果需要持久化到配置文件，请使用 save_agent_display_config() 方法
        """
        agents = self.get_all_agents()
        agent_configs = {}
        
        for agent in agents:
            agent_name = agent["name"]
            metadata = self.read_agent_metadata(agent_name)
            
            if metadata:
                # 从 metadata 构建 dashboard 显示配置
                dashboard_config = {
                    "name": metadata.get("display_name", agent_name),
                    "role": metadata.get("role", "Agent"),
                    "emoji": metadata.get("emoji", "🤖"),
                    "color": metadata.get("color", "cyan"),
                    "description": metadata.get("description", ""),
                }
            else:
                # 没有 metadata，使用默认配置
                dashboard_config = self._get_default_dashboard_config(agent_name)
            
            agent_configs[agent_name] = dashboard_config
        
        # 只更新内存中的配置，不写入文件
        # 获取当前的 dashboard 配置
        current_config = dashboard_config_manager.get()
        
        # 合并 OpenClaw 的 agent 配置到内存中
        # 优先保留 Dashboard 配置文件中已有的配置
        merged_configs = {}
        existing_configs = current_config.get("agent_configs", {})
        
        for agent_name, oc_config in agent_configs.items():
            if agent_name in existing_configs:
                # 如果 Dashboard 配置文件中已有该 agent，保留现有配置
                merged_configs[agent_name] = existing_configs[agent_name]
            else:
                # 如果 Dashboard 配置文件中没有该 agent，使用 OpenClaw 的配置
                merged_configs[agent_name] = oc_config
        
        # 只更新内存中的配置
        current_config["agent_configs"] = merged_configs
        dashboard_config_manager._config = current_config
        
        return {
            "success": True,
            "synced_count": len(agent_configs),
            "total_agents": len(agents),
            "message": "配置已加载到内存，未写入配置文件"
        }
    
    def _get_default_dashboard_config(self, agent_name: str) -> Dict[str, str]:
        """获取默认的 Dashboard 配置"""
        defaults = {
            "main": {"name": "小七", "role": "主助手", "emoji": "🎯", "color": "main", "description": "主要对话助手"},
            "coder": {"name": "Coder", "role": "代码专家", "emoji": "💻", "color": "coder", "description": "专注代码编写"},
            "brainstorm": {"name": "Brainstorm", "role": "创意顾问", "emoji": "💡", "color": "brainstorm", "description": "头脑风暴"},
            "writer": {"name": "Writer", "role": "写作助手", "emoji": "✍️", "color": "writer", "description": "文档撰写"},
            "investor": {"name": "Investor", "role": "投资分析", "emoji": "📈", "color": "investor", "description": "投资分析"},
        }
        
        if agent_name in defaults:
            return defaults[agent_name]
        
        return {
            "name": agent_name.capitalize(),
            "role": "Agent",
            "emoji": "🤖",
            "color": "cyan",
            "description": f"{agent_name} agent"
        }
    
    def get_agents_display_config(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有 agent 的显示配置（从 OpenClaw 读取，不修改任何配置文件）
        
        Returns:
            {agent_name: display_config}
        """
        agents = self.get_all_agents()
        result = {}
        
        for agent in agents:
            agent_name = agent["name"]
            metadata = self.read_agent_metadata(agent_name)
            
            if metadata:
                display_config = {
                    "name": metadata.get("display_name", agent_name),
                    "role": metadata.get("role", "Agent"),
                    "emoji": metadata.get("emoji", "🤖"),
                    "color": metadata.get("color", "cyan"),
                    "description": metadata.get("description", ""),
                }
            else:
                display_config = self._get_default_dashboard_config(agent_name)
            
            result[agent_name] = display_config
        
        return result
    
    # ============ Subagents 管理方法 ============
    
    def get_agent_subagents(self, agent_name: str) -> Dict[str, Any]:
        """
        获取指定 Agent 的 subagents 配置
        
        Returns:
            {"allowAgents": [...], "maxConcurrent": int} 或 {}
        """
        try:
            config = self.read_global_config()
            agent_list = config.get("agents", {}).get("list", [])
            
            for agent in agent_list:
                if agent.get("id") == agent_name:
                    subagents = agent.get("subagents", {})
                    return {
                        "allowAgents": subagents.get("allowAgents", []),
                        "maxConcurrent": subagents.get("maxConcurrent", 4)
                    }
            
            return {"allowAgents": [], "maxConcurrent": 4}
        
        except Exception as e:
            print(f"[OpenClawConfig] 获取 agent {agent_name} subagents 失败: {e}")
            return {"allowAgents": [], "maxConcurrent": 4}
    
    def update_agent_allow_agents(self, agent_name: str, allow_agents: List[str], max_concurrent: Optional[int] = None) -> bool:
        """
        更新指定 Agent 的 allowAgents 列表
        
        Args:
            agent_name: Agent 名称
            allow_agents: 允许调度的 Agent 列表
            max_concurrent: 最大并发数（可选）
        
        Returns:
            是否成功
        """
        try:
            config = self.read_global_config()
            agent_list = config.get("agents", {}).get("list", [])
            
            # 查找目标 Agent
            target_agent = None
            for agent in agent_list:
                if agent.get("id") == agent_name:
                    target_agent = agent
                    break
            
            if not target_agent:
                print(f"[OpenClawConfig] Agent {agent_name} 不存在")
                return False
            
            # 确保 subagents 字段存在
            if "subagents" not in target_agent:
                target_agent["subagents"] = {}
            
            # 更新 allowAgents
            target_agent["subagents"]["allowAgents"] = allow_agents
            
            # 可选：更新 maxConcurrent
            if max_concurrent is not None:
                target_agent["subagents"]["maxConcurrent"] = max_concurrent
            
            # 写入配置
            return self.write_global_config(config)
        
        except Exception as e:
            print(f"[OpenClawConfig] 更新 agent {agent_name} allowAgents 失败: {e}")
            return False
    
    def add_agent_to_allow_agents(self, target_agent: str, agent_to_add: str) -> bool:
        """
        将指定 Agent 添加到目标 Agent 的 allowAgents 列表中
        
        Args:
            target_agent: 目标 Agent（调度者）
            agent_to_add: 要添加的 Agent（被调度者）
        
        Returns:
            是否成功
        """
        try:
            current = self.get_agent_subagents(target_agent)
            allow_agents = current.get("allowAgents", [])
            
            # 如果已存在，不重复添加
            if agent_to_add in allow_agents:
                return True
            
            allow_agents.append(agent_to_add)
            max_concurrent = current.get("maxConcurrent", 4)
            
            return self.update_agent_allow_agents(target_agent, allow_agents, max_concurrent)
        
        except Exception as e:
            print(f"[OpenClawConfig] 添加 {agent_to_add} 到 {target_agent} allowAgents 失败: {e}")
            return False
    
    def remove_agent_from_allow_agents(self, target_agent: str, agent_to_remove: str) -> bool:
        """
        从目标 Agent 的 allowAgents 列表中移除指定 Agent
        
        Args:
            target_agent: 目标 Agent（调度者）
            agent_to_remove: 要移除的 Agent（被调度者）
        
        Returns:
            是否成功
        """
        try:
            current = self.get_agent_subagents(target_agent)
            allow_agents = current.get("allowAgents", [])
            
            # 如果不在列表中，直接返回成功
            if agent_to_remove not in allow_agents:
                return True
            
            allow_agents.remove(agent_to_remove)
            max_concurrent = current.get("maxConcurrent", 4)
            
            return self.update_agent_allow_agents(target_agent, allow_agents, max_concurrent)
        
        except Exception as e:
            print(f"[OpenClawConfig] 从 {target_agent} allowAgents 移除 {agent_to_remove} 失败: {e}")
            return False


# 全局实例
_config_manager_instance: Optional[OpenClawConfigManager] = None


def get_openclaw_config_manager(skip_validation: bool = False) -> OpenClawConfigManager:
    """
    获取全局 OpenClaw 配置管理器
    
    Args:
        skip_validation: 是否跳过 schema 验证（用于开发调试）
    """
    global _config_manager_instance
    if _config_manager_instance is None:
        _config_manager_instance = OpenClawConfigManager(skip_validation=skip_validation)
    return _config_manager_instance


if __name__ == "__main__":
    # 测试
    manager = get_openclaw_config_manager()
    
    print("=" * 50)
    print("OpenClaw Config Manager Test")
    print("=" * 50)
    
    # 测试读取全局配置中的 agents
    config = manager.read_global_config()
    agents_config = config.get("agents", {})
    print(f"\nOpenClaw 中配置了 {len(agents_config.get('list', []))} 个 agents:")
    for agent in agents_config.get("list", []):
        print(f"  - {agent.get('id')}: {agent.get('identity', {}).get('name', 'N/A')}")
