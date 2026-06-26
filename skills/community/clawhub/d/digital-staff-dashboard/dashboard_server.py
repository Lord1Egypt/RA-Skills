#!/usr/bin/env python3
"""
Enhanced Agent Dashboard Server v2.1
支持从 OpenClaw 读取配置、创建新 Agent
"""

import json
import os
from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, abort

# 导入自定义模块
from openclaw_finder import get_finder, find_openclaw_home
from config import get_config_manager, get_config
from openclaw_config import get_openclaw_config_manager
from openclaw_skills import get_skills_manager

app = Flask(__name__)

# 项目目录
PROJECT_DIR = Path(__file__).parent
STATIC_DIR = PROJECT_DIR / "static"
DATA_DIR = PROJECT_DIR / "data"
AVATAR_DIR = DATA_DIR / "avatars"

# 确保目录存在
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

# 初始化管理器
config_manager = get_config_manager()
openclaw_config_manager = get_openclaw_config_manager()
finder = get_finder()
openclaw_home = finder.find_primary()
skills_manager = get_skills_manager(openclaw_home)

# 检查 OpenClaw 版本
MIN_OPENCLAW_VERSION = "2026.3.24"
version_ok, current_version, version_msg = finder.check_version(MIN_OPENCLAW_VERSION)

# 允许的头像文件扩展名
ALLOWED_AVATAR_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_avatar_file(filename: str) -> bool:
    """检查文件是否是允许的头像格式"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AVATAR_EXTENSIONS


def _validate_agent_name(agent_name: str) -> bool:
    """验证agent名称是否合法"""
    if not agent_name or not isinstance(agent_name, str):
        return False
    forbidden = ['/', '\\', '..', '~', '$']
    return not any(f in agent_name for f in forbidden)


def sync_openclaw_agents():
    """
    启动时从 OpenClaw 加载 agent 配置到内存
    
    注意：此操作只加载到内存，不会修改 Dashboard 的配置文件 (data/config.json)
    显示的 agents 完全以 OpenClaw 配置文件 (openclaw.json) 中的 agents.list 为准
    """
    print("[Sync] 正在从 OpenClaw 加载 Agent 配置...")
    result = openclaw_config_manager.sync_agents_to_dashboard(config_manager)
    print(f"[Sync] 加载完成: {result['synced_count']}/{result['total_agents']} 个 Agent")
    if result.get("message"):
        print(f"[Sync] 提示: {result['message']}")
    return result


# ============ 静态文件服务 ============

@app.route('/')
def index():
    """Serve the dashboard index.html"""
    return send_from_directory(STATIC_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory(STATIC_DIR, filename)


# ============ API端点 - OpenClaw URL ============

@app.route('/api/openclaw-url')
def get_openclaw_url():
    """Get OpenClaw base URL for agent chat links"""
    config = config_manager.get()
    base_url = config.get("openclaw_base_url", "http://127.0.0.1:18789")
    return jsonify({
        "base_url": base_url,
        "enabled": bool(base_url)
    })


# ============ API端点 - 配置相关 ============

@app.route('/api/config')
def get_config_endpoint():
    """获取Dashboard配置"""
    config = config_manager.get()
    token_cost = config.get("token_cost", {})
    return jsonify({
        "dashboard_name": config.get("dashboard_name", "Agent Dashboard"),
        "dashboard_subtitle": config.get("dashboard_subtitle", ""),
        "theme": config.get("theme", "dark"),
        "refresh_interval": config.get("refresh_interval", 30),
        "show_cost_estimates": config.get("show_cost_estimates", True),
        "cost_decimal_places": config.get("cost_decimal_places", 4),
        "currency": token_cost.get("currency", "CNY"),
        "token_cost": {
            "input_price_per_1m": token_cost.get("input_price_per_1m", 2.0),
            "output_price_per_1m": token_cost.get("output_price_per_1m", 8.0),
            "cache_price_per_1m": token_cost.get("cache_price_per_1m", 1.0),
            "currency": token_cost.get("currency", "CNY")
        },
        "agent_configs": config.get("agent_configs", {}),
        "view_mode": config.get("view_mode", "grid"),
        "agent_order": config.get("agent_order", [])
    })


@app.route('/api/config', methods=['POST'])
def update_config_endpoint():
    """更新Dashboard配置"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        success = config_manager.update(data)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/config/sync', methods=['POST'])
def sync_config_endpoint():
    """手动同步 OpenClaw 配置"""
    try:
        result = sync_openclaw_agents()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ API端点 - Agent管理 ============

@app.route('/api/system-info')
def get_system_info():
    """获取系统信息"""
    return jsonify({
        "openclaw_home": str(openclaw_home) if openclaw_home else None,
        "agents_dir": str(finder.get_agents_dir()) if finder.get_agents_dir() else None,
        "server_time": datetime.now().isoformat(),
        "version": "2.1.0"
    })


@app.route('/api/agents')
def list_agents():
    """
    List all available agents with their configurations
    
    从 OpenClaw 配置文件中直接读取 agents.list，
    显示用户配置文件中实际存在的 agents，不修改任何配置文件
    """
    # 从 OpenClaw 配置读取 agents 列表（而不是从文件系统扫描）
    oc_config = openclaw_config_manager.read_global_config()
    oc_agent_list = oc_config.get("agents", {}).get("list", [])
    
    # 从文件系统获取 agent 信息（用于检查 sessions, avatar 等状态）
    fs_agents = {a["name"]: a for a in finder.get_agent_list()}
    
    result = []
    for agent_entry in oc_agent_list:
        agent_name = agent_entry.get("id")
        if not agent_name:
            continue
        
        # 从 OpenClaw agent entry 获取显示配置
        identity = agent_entry.get("identity", {})
        display_config = {
            "name": identity.get("name", agent_name),
            "role": identity.get("role", "Agent"),
            "emoji": identity.get("emoji", "🤖"),
            "color": identity.get("color", "cyan"),
            "description": identity.get("description", ""),
        }
        
        # 读取 OpenClaw 的 metadata（如果存在）
        metadata = openclaw_config_manager.read_agent_metadata(agent_name)
        if metadata:
            # metadata 优先
            display_config["name"] = metadata.get("display_name", display_config["name"])
            display_config["role"] = metadata.get("role", display_config["role"])
            display_config["emoji"] = metadata.get("emoji", display_config["emoji"])
            display_config["color"] = metadata.get("color", display_config["color"])
            display_config["description"] = metadata.get("description", display_config["description"])
        
        # 获取文件系统的 agent 信息
        fs_info = fs_agents.get(agent_name, {})
        
        # 检查是否有自定义头像
        custom_avatar_path = AVATAR_DIR / f"{agent_name}.png"
        has_custom_avatar = custom_avatar_path.exists()
        
        result.append({
            "name": agent_name,
            "has_sessions": fs_info.get("has_sessions", False),
            "has_avatar": fs_info.get("has_avatar", False) or has_custom_avatar,
            "has_config": fs_info.get("has_config", False),
            "display": display_config,
            "metadata": metadata,
            "model": agent_entry.get("model", ""),
            "subagents": agent_entry.get("subagents", {})
        })
    
    return jsonify(result)


@app.route('/api/agents', methods=['POST'])
def create_agent_endpoint():
    """创建新的 Agent"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        agent_name = data.get("name", "").strip().lower()
        if not agent_name:
            return jsonify({"success": False, "error": "Agent name is required"}), 400
        
        # 创建 agent
        result = openclaw_config_manager.create_agent(agent_name, data)
        
        if result["success"]:
            # 同步到 Dashboard 配置
            dashboard_config = {
                "name": data.get("display_name", agent_name),
                "role": data.get("role", "Agent"),
                "emoji": data.get("emoji", "🤖"),
                "color": data.get("color", "cyan"),
                "description": data.get("description", "")
            }
            
            config_manager.update({
                "agent_configs": {
                    agent_name: dashboard_config
                }
            })
            
            return jsonify({
                "success": True,
                "agent_name": agent_name,
                "message": f"Agent '{agent_name}' created successfully"
            })
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>', methods=['DELETE'])
def delete_agent_endpoint(agent_name):
    """删除 Agent"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        result = openclaw_config_manager.delete_agent(agent_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/sessions')
def get_agent_sessions(agent_name):
    """Get all sessions for a specific agent"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    sessions_path = finder.get_agent_sessions_path(agent_name)
    
    if not sessions_path:
        return jsonify({})
    
    try:
        with open(sessions_path, 'r', encoding='utf-8') as f:
            sessions = json.load(f)
        
        # 添加成本计算
        config = config_manager.get()
        if config.get("show_cost_estimates", True):
            for session_key, session_data in sessions.items():
                cost = config_manager.calculate_cost(
                    session_data.get('inputTokens', 0),
                    session_data.get('outputTokens', 0),
                    session_data.get('cacheRead', 0),
                    session_data.get('cacheWrite', 0)
                )
                session_data['estimatedCost'] = cost
        
        return jsonify(sessions)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading sessions for {agent_name}: {e}")
        return jsonify({})


@app.route('/api/agents/<agent_name>/avatar', methods=['GET', 'POST'])
def agent_avatar(agent_name):
    """获取或更新agent头像"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    if request.method == 'GET':
        # 优先返回自定义头像
        custom_avatar = AVATAR_DIR / f"{agent_name}.png"
        if custom_avatar.exists():
            return send_from_directory(AVATAR_DIR, f"{agent_name}.png")
        
        # 其次查找OpenClaw目录中的头像
        avatar_path = finder.get_agent_avatar_path(agent_name)
        if avatar_path:
            return send_from_directory(avatar_path.parent, avatar_path.name)
        
        # 返回默认头像
        abort(404, "Avatar not found")
    
    elif request.method == 'POST':
        # 上传新头像
        if 'avatar' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['avatar']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if not allowed_avatar_file(file.filename):
            return jsonify({
                "success": False, 
                "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_AVATAR_EXTENSIONS)}"
            }), 400
        
        # 保存文件
        try:
            # 统一保存为png格式
            filename = f"{agent_name}.png"
            filepath = AVATAR_DIR / filename
            
            # 读取文件内容检查大小
            file_content = file.read()
            if len(file_content) > MAX_AVATAR_SIZE:
                return jsonify({
                    "success": False,
                    "error": f"File too large. Max size: {MAX_AVATAR_SIZE / 1024 / 1024}MB"
                }), 400
            
            # 保存文件
            with open(filepath, 'wb') as f:
                f.write(file_content)
            
            # 更新配置
            config_manager.update_agent_avatar(agent_name, str(filepath))
            
            return jsonify({
                "success": True,
                "message": "Avatar uploaded successfully",
                "path": f"/api/agents/{agent_name}/avatar"
            })
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/config', methods=['GET', 'POST'])
def agent_config_endpoint(agent_name):
    """获取或更新agent显示配置"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    if request.method == 'GET':
        config = config_manager.get_agent_config(agent_name)
        metadata = openclaw_config_manager.read_agent_metadata(agent_name)
        return jsonify({
            "dashboard_config": config,
            "openclaw_metadata": metadata
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # 更新 Dashboard 配置
            dashboard_updates = {
                "agent_configs": {
                    agent_name: {
                        "name": data.get("display_name", agent_name),
                        "role": data.get("role", "Agent"),
                        "emoji": data.get("emoji", "🤖"),
                        "color": data.get("color", "cyan"),
                        "description": data.get("description", "")
                    }
                }
            }
            config_manager.update(dashboard_updates)
            
            # 更新 OpenClaw metadata
            metadata_updates = {
                "display_name": data.get("display_name", agent_name),
                "role": data.get("role", "Agent"),
                "emoji": data.get("emoji", "🤖"),
                "color": data.get("color", "cyan"),
                "description": data.get("description", ""),
                "system_prompt": data.get("system_prompt", "")
            }
            openclaw_config_manager.update_agent_metadata(agent_name, metadata_updates)
            
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


# ============ API端点 - Subagents 管理 ============

@app.route('/api/agents/<agent_name>/subagents')
def get_agent_subagents_endpoint(agent_name):
    """获取指定 Agent 的 subagents 配置"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        result = openclaw_config_manager.get_agent_subagents(agent_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents/<agent_name>/subagents', methods=['POST'])
def update_agent_subagents_endpoint(agent_name):
    """更新指定 Agent 的 subagents 配置"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        allow_agents = data.get('allowAgents', [])
        max_concurrent = data.get('maxConcurrent')
        
        success = openclaw_config_manager.update_agent_allow_agents(
            agent_name, allow_agents, max_concurrent
        )
        
        if success:
            return jsonify({"success": True, "message": f"Subagents updated for {agent_name}"})
        else:
            return jsonify({"success": False, "error": "Failed to update subagents"}), 500
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/subagents/add', methods=['POST'])
def add_agent_to_subagents_endpoint(agent_name):
    """将指定 Agent 添加到目标 Agent 的 allowAgents 列表"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        data = request.get_json()
        agent_to_add = data.get('agentToAdd')
        
        if not agent_to_add:
            return jsonify({"success": False, "error": "agentToAdd is required"}), 400
        
        success = openclaw_config_manager.add_agent_to_allow_agents(agent_name, agent_to_add)
        
        if success:
            return jsonify({
                "success": True, 
                "message": f"{agent_to_add} added to {agent_name}'s allowAgents"
            })
        else:
            return jsonify({"success": False, "error": "Failed to add agent"}), 500
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/subagents/remove', methods=['POST'])
def remove_agent_from_subagents_endpoint(agent_name):
    """从目标 Agent 的 allowAgents 列表中移除指定 Agent"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        data = request.get_json()
        agent_to_remove = data.get('agentToRemove')
        
        if not agent_to_remove:
            return jsonify({"success": False, "error": "agentToRemove is required"}), 400
        
        success = openclaw_config_manager.remove_agent_from_allow_agents(agent_name, agent_to_remove)
        
        if success:
            return jsonify({
                "success": True, 
                "message": f"{agent_to_remove} removed from {agent_name}'s allowAgents"
            })
        else:
            return jsonify({"success": False, "error": "Failed to remove agent"}), 500
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ API端点 - 模型/提供商相关 ============

@app.route('/api/model-providers')
def get_model_providers():
    """获取可用的模型提供商列表"""
    try:
        global_config = openclaw_config_manager.read_global_config()
        providers = global_config.get("models", {}).get("providers", {})
        
        print(f"[API] 读取到 {len(providers)} 个模型提供商")
        
        result = []
        for provider_id, provider_config in providers.items():
            models = []
            for model in provider_config.get("models", []):
                models.append({
                    "id": model.get("id"),
                    "name": model.get("name", model.get("id")),
                    "contextWindow": model.get("contextWindow", 0),
                    "maxTokens": model.get("maxTokens", 0)
                })
            
            # 使用配置中的 name 或格式化 id
            provider_name = provider_config.get("name", provider_id.capitalize())
            
            result.append({
                "id": provider_id,
                "name": provider_name,
                "models": models
            })
            print(f"[API]   - {provider_id}: {len(models)} 个模型")
        
        return jsonify(result)
    except Exception as e:
        print(f"[API] 获取模型提供商失败: {e}")
        return jsonify({"error": str(e)}), 500


# ============ API端点 - 统计相关 ============

@app.route('/api/stats')
def get_stats():
    """Get aggregated stats across all agents with cost calculations"""
    total_tokens = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cache_tokens = 0
    total_sessions = 0
    running_agents = 0
    
    stats_by_agent = {}
    
    agents = finder.get_agent_list()
    for agent_info in agents:
        agent_name = agent_info["name"]
        sessions_path = finder.get_agent_sessions_path(agent_name)
        
        agent_tokens = 0
        agent_input = 0
        agent_output = 0
        agent_cache = 0
        agent_session_count = 0
        agent_running = False
        
        current_model = None
        current_model_provider = None
        latest_session = None
        
        if sessions_path:
            try:
                with open(sessions_path, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
                
                # 找到最新的会话
                if sessions:
                    latest_session = max(sessions.values(), 
                                        key=lambda s: s.get('updatedAt', 0))
                    current_model = latest_session.get('model')
                    current_model_provider = latest_session.get('modelProvider')
                    
                    # 只基于最新会话判断运行状态
                    if latest_session.get('status') == 'running':
                        agent_running = True
                        running_agents += 1
                
                # 统计所有会话的 token 使用量
                for session_key, session_data in sessions.items():
                    input_t = session_data.get('inputTokens', 0)
                    output_t = session_data.get('outputTokens', 0)
                    cache_r = session_data.get('cacheRead', 0)
                    cache_w = session_data.get('cacheWrite', 0)
                    
                    agent_input += input_t
                    agent_output += output_t
                    agent_cache += cache_r + cache_w
                    agent_tokens += session_data.get('totalTokens', 0)
                    agent_session_count += 1
            
            except Exception as e:
                print(f"Error processing sessions for {agent_name}: {e}")
        
        total_tokens += agent_tokens
        total_input_tokens += agent_input
        total_output_tokens += agent_output
        total_cache_tokens += agent_cache
        total_sessions += agent_session_count
        
        # 计算该agent的成本
        agent_cost = config_manager.calculate_cost(agent_input, agent_output, 0, agent_cache)
        
        # 格式化当前模型显示
        current_model_display = None
        if current_model and current_model_provider:
            current_model_display = f"{current_model_provider}/{current_model}"
        elif current_model:
            current_model_display = current_model
        
        stats_by_agent[agent_name] = {
            'tokens': agent_tokens,
            'inputTokens': agent_input,
            'outputTokens': agent_output,
            'cacheTokens': agent_cache,
            'sessions': agent_session_count,
            'isRunning': agent_running,
            'estimatedCost': agent_cost,
            'currentModel': current_model_display,
            'currentModelProvider': current_model_provider,
            'currentModelName': current_model
        }
    
    # 计算总成本
    show_cost = config_manager.get().get("show_cost_estimates", True)
    
    total_cost = None
    if show_cost:
        total_cost = config_manager.calculate_cost(
            total_input_tokens, total_output_tokens, 0, total_cache_tokens
        )
    
    # 如果不需要显示费用，从每个 agent 的统计中移除
    if not show_cost:
        for agent_stats in stats_by_agent.values():
            agent_stats['estimatedCost'] = None
    
    return jsonify({
        'totalTokens': total_tokens,
        'totalInputTokens': total_input_tokens,
        'totalOutputTokens': total_output_tokens,
        'totalCacheTokens': total_cache_tokens,
        'totalSessions': total_sessions,
        'runningAgents': running_agents,
        'totalCost': total_cost,
        'byAgent': stats_by_agent
    })


@app.route('/api/stats/cost-summary')
def get_cost_summary():
    """获取成本汇总信息"""
    config = config_manager.get()
    cost_config = config.get("token_cost", {})
    
    # 获取所有统计信息
    stats = get_stats().get_json()
    
    return jsonify({
        "cost_config": {
            "input_price_per_1m": cost_config.get("input_price_per_1m", 2.0),
            "output_price_per_1m": cost_config.get("output_price_per_1m", 8.0),
            "cache_price_per_1m": cost_config.get("cache_price_per_1m", 1.0),
            "currency": cost_config.get("currency", "CNY")
        },
        "total_cost": stats.get("totalCost"),
        "by_agent": {
            k: v.get("estimatedCost") 
            for k, v in stats.get("byAgent", {}).items()
        }
    })


# ============ 启动服务器 ============

def print_startup_info():
    """打印启动信息"""
    config = config_manager.get()
    
    print("=" * 60)
    print(f"  {config.get('dashboard_name', 'Agent Dashboard')} v2.1")
    print("=" * 60)
    
    # 显示版本信息
    if current_version:
        print(f"OpenClaw: v{current_version} {'✓' if version_ok else '⚠️'}")
    if version_msg:
        print(f"  ⚠️  WARNING: {version_msg}")
        print(f"  ℹ️  请升级: npm install -g openclaw@latest")
        print()
    
    print(f"Dashboard: http://localhost:{config.get('port', 5178)}")
    print(f"OpenClaw Home: {openclaw_home or 'Not found'}")
    print(f"Agents Dir: {finder.get_agents_dir() or 'Not found'}")
    print(f"Auto-refresh: {config.get('refresh_interval', 30)}s")
    print(f"Cost Estimates: {'Enabled' if config.get('show_cost_estimates', True) else 'Disabled'}")
    
    agents = finder.get_agent_list()
    print(f"\nFound {len(agents)} Agents:")
    for agent in agents:
        status = "✓" if agent["has_sessions"] else "✗"
        avatar = "🖼️" if agent["has_avatar"] else "❌"
        print(f"  - {agent['name']}: sessions[{status}] avatar[{avatar}]")
    
    print("\nPress Ctrl+C to stop")
    print("=" * 60)


# ============ API端点 - 技能管理 ============

@app.route('/api/skills')
def list_skills():
    """获取所有可用技能列表（包括配置中声明的）"""
    try:
        config = openclaw_config_manager.read_global_config()
        skills = skills_manager.get_all_available_skills(config)
        return jsonify({
            "success": True,
            "skills": [skill.to_dict() for skill in skills]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/skills/<skill_id>')
def get_skill_detail(skill_id):
    """获取技能详细信息"""
    try:
        detail = skills_manager.get_skill_detail(skill_id)
        if not detail:
            return jsonify({"success": False, "error": f"Skill '{skill_id}' not found"}), 404
        return jsonify({"success": True, "skill": detail})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/skills')
def get_agent_skills(agent_name):
    """获取指定 Agent 的技能列表（包括启用状态）"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        # 读取全局配置
        config = openclaw_config_manager.read_global_config()
        skills = skills_manager.get_agent_skills(agent_name, config)
        return jsonify({
            "success": True,
            "agent": agent_name,
            "skills": skills
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/skills/<skill_id>/enable', methods=['POST'])
def enable_agent_skill(agent_name, skill_id):
    """为指定 Agent 启用技能"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        success, message = skills_manager.enable_skill_for_agent(agent_name, skill_id)
        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/skills/<skill_id>/disable', methods=['POST'])
def disable_agent_skill(agent_name, skill_id):
    """为指定 Agent 禁用技能"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        success, message = skills_manager.disable_skill_for_agent(agent_name, skill_id)
        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/agents/<agent_name>/skills/install', methods=['POST'])
def install_agent_skill(agent_name):
    """为 Agent 安装新技能（调用 OpenClaw CLI）"""
    if not _validate_agent_name(agent_name):
        abort(400, "Invalid agent name")
    
    try:
        data = request.get_json()
        skill_id = data.get('skillId')
        
        if not skill_id:
            return jsonify({"success": False, "error": "skillId is required"}), 400
        
        # 调用 OpenClaw CLI 安装技能
        import subprocess
        result = subprocess.run(
            ['openclaw', 'skills', 'install', skill_id],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            # 安装成功后，自动启用该技能
            skills_manager.enable_skill_for_agent(agent_name, skill_id)
            return jsonify({
                "success": True, 
                "message": f"Skill '{skill_id}' installed and enabled for '{agent_name}'",
                "output": result.stdout
            })
        else:
            return jsonify({
                "success": False, 
                "error": f"Failed to install skill: {result.stderr}",
                "output": result.stdout
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({"success": False, "error": "Skill installation timeout"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    # 启动时同步 OpenClaw 配置
    sync_openclaw_agents()
    
    config = config_manager.get()
    print_startup_info()
    
    app.run(
        host=config.get('host', '0.0.0.0'),
        port=config.get('port', 5178),
        debug=config.get('debug', False),
        threaded=True
    )
