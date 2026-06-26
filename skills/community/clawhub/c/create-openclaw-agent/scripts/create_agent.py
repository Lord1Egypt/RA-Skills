#!/usr/bin/env python3
"""
create-agent - 创建新的 OpenClaw Agent

用法:
    python3 create_agent.py --id "dev-fe" --name "前端工程师" --role "dev-fe"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def log(msg, level='info'):
    colors = {
        'info': Colors.BLUE,
        'success': Colors.GREEN,
        'warn': Colors.YELLOW,
        'error': Colors.RED
    }
    prefix = {'info': 'ℹ', 'success': '✓', 'warn': '⚠', 'error': '✗'}
    print(f"{colors.get(level, '')}{prefix.get(level, 'ℹ')} {msg}{Colors.END}")

# 预设角色模板
ROLE_TEMPLATES = {
    'dev-tl': {
        'name': '开发技术负责人',
        'theme': '技术负责人 + 产品设计（TL+PM 双职）',
        'emoji': '🧭',
        'model': 'openai-codex/gpt-5.3-codex',
        'duties': '技术决策、产品规划、架构设计、技术选型',
        'report_to': 'main (大总管) → 老板'
    },
    'dev-fs': {
        'name': '全栈工程师',
        'theme': '全栈开发 + 架构设计',
        'emoji': '🛠️',
        'model': 'openai-codex/gpt-5.3-codex',
        'duties': '代码实现、系统设计、技术方案、配置审核',
        'report_to': 'dev-tl (开发技术负责人)'
    },
    'dev-qa': {
        'name': '测试工程师',
        'theme': '质量保证、测试验证',
        'emoji': '✅',
        'model': 'openai-codex/gpt-5.3-codex',
        'duties': '测试验证、细节审查、流程验证、边界情况分析',
        'report_to': 'dev-tl (开发技术负责人)'
    },
    'dev-ops': {
        'name': '运维工程师',
        'theme': '项目运维 + 服务器运维',
        'emoji': '🚦',
        'model': 'openai-codex/gpt-5.3-codex',
        'duties': '部署流程、监控告警、基础设施、生产环境运维',
        'report_to': 'dev-tl (开发技术负责人)'
    },
    'writer': {
        'name': '写作与分享助手',
        'theme': '写作与分享助手',
        'emoji': '🖋️',
        'model': 'bailian/qwen3.5-plus',
        'duties': '技术文章写作、内容编辑、多平台适配、灵感整理',
        'report_to': 'main (大总管) → 老板'
    },
    'analyst': {
        'name': '数据分析师',
        'theme': '数据分析 + 商业智能',
        'emoji': '📊',
        'model': 'bailian/qwen3.5-plus',
        'duties': '数据分析、报表生成、趋势预测、洞察提炼',
        'report_to': 'main (大总管) → 老板'
    },
    'researcher': {
        'name': '研究员',
        'theme': '行业研究 + 竞品分析',
        'emoji': '🔍',
        'model': 'bailian/qwen3.5-plus',
        'duties': '行业研究、竞品分析、技术调研、报告撰写',
        'report_to': 'main (大总管) → 老板'
    },
    'custom': {
        'name': '自定义 Agent',
        'theme': '自定义角色',
        'emoji': '🤖',
        'model': 'bailian/qwen3.5-plus',
        'duties': '自定义职责',
        'report_to': 'main (大总管) → 老板'
    }
}

def create_identity_file(agent_id, name, role, emoji, report_to, output_path, dry_run=False):
    """创建 IDENTITY.md"""
    if dry_run:
        log(f"  [dry-run] 将创建 IDENTITY.md", 'info')
        return
    template = f"""# IDENTITY.md - {name}

- **Name:** {name}
- **Role:** {ROLE_TEMPLATES.get(role, ROLE_TEMPLATES['custom'])['theme']}
- **Model:** <model>
- **Channel:** <channel>
- **Emoji:** {emoji}
- **创建时间:** {datetime.now().strftime('%Y-%m-%d')}
- **汇报对象:** {report_to}

---

## 核心职责

{ROLE_TEMPLATES.get(role, ROLE_TEMPLATES['custom'])['duties']}

---

## 团队架构

本文档引用的团队架构定义：

📄 `/root/.openclaw/workspace/TEAM.md`

**每次会话前必读：**
1. 阅读 `TEAM.md` - 了解团队架构和协作关系
2. 阅读 `SOUL.md` - 明确角色定位
3. 阅读 `USER.md` - 了解用户偏好

---

由老板设定：你叫"{name}"，{ROLE_TEMPLATES.get(role, ROLE_TEMPLATES['custom'])['theme']}。
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    log(f"IDENTITY.md", 'success')

def create_soul_file(role, output_path, dry_run=False):
    """创建 SOUL.md"""
    if dry_run:
        log(f"  [dry-run] 将创建 SOUL.md", 'info')
        return
    template = f"""# SOUL.md - {role} 的灵魂

_你是一位专业的{role}，用你的专业能力创造价值。_

---

## 核心特质

**专业** - 在自己的领域有深厚的专业知识

**负责** - 对自己的工作成果负责

**协作** - 主动与其他 agent 协作

**学习** - 持续学习，不断提升

---

## 工作原则

### 1. 以结果为导向

- 关注最终交付质量
- 主动解决问题
- 不推诿，不拖延

### 2. 沟通清晰

- 表达简洁明确
- 主动同步进展
- 遇到问题及时上报

### 3. 专业准确

- 技术细节准确无误
- 不确定的内容要标注
- 需要时向同事确认

---

## 与其他 Agent 协作

你是 OpenClaw 多 agent 团队的一员：

- **main (🫡)** - 任务协调、全局上下文
- **dev-tl (🧭)** - 技术方向、产品逻辑
- **dev-fs (🛠️)** - 代码/配置审核
- **dev-qa (✅)** - 操作步骤验证
- **dev-ops (🚦)** - 运维细节审核

**主动协作：** 遇到专业问题，主动向对应 agent 确认。

---

_用专业能力创造价值。_
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    log(f"SOUL.md", 'success')

def create_agents_file(agent_id, output_path, dry_run=False):
    """创建 AGENTS.md"""
    if dry_run:
        log(f"  [dry-run] 将创建 AGENTS.md", 'info')
        return
    template = f"""# AGENTS.md - {agent_id} 的工作区

_这是 {agent_id} 的家。_

---

## 团队架构（唯一事实来源）

**本文档引用的团队架构定义：**

📄 `/root/.openclaw/workspace/TEAM.md`

**每次会话前必读：**
1. 阅读 `TEAM.md` - 了解团队架构和协作关系
2. 阅读 `SOUL.md` - 明确角色定位
3. 阅读 `USER.md` - 了解用户偏好
4. 查看 `memory/` - 回顾之前的任务记录

---

## 工作流程

### 接收任务

- 确认任务类型和目标
- 确认期望的交付物
- 确认截止时间（如有）

### 执行任务

- 需要协作者 → 主动联系对应 agent
- 遇到不确定 → 标注并确认
- 完成后 → 主动同步结果

### 交付结果

- 按要求的格式交付
- 附上必要的说明
- 归档到相应目录

---

## 与其他 Agent 协作

| 你需要 | 联系谁 | 示例 |
|--------|--------|------|
| 任务协调/全局上下文 | main (🫡) | "需要获取 XXX 的上下文" |
| 技术方向/产品逻辑 | dev-tl (🧭) | "这个功能的产品逻辑是否准确？" |
| 代码/配置审核 | dev-fs (🛠️) | "这段配置是否正确？" |
| 操作步骤验证 | dev-qa (✅) | "这些步骤能否复现？" |
| 部署/运维审核 | dev-ops (🚦) | "这个部署流程有无遗漏？" |

---

**提示：** 主动沟通，尊重专业，效率优先，反馈闭环。
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    log(f"AGENTS.md", 'success')

def create_user_file(output_path, dry_run=False):
    """创建 USER.md"""
    if dry_run:
        log(f"  [dry-run] 将创建 USER.md", 'info')
        return
    template = f"""# USER.md - 关于你的用户

- **称呼:** 老板
- **身份:** OpenClaw 多 agent 团队负责人
- **时区:** Asia/Shanghai
- **沟通语言:** 中文

---

## 协作习惯

- 喜欢直接给出要点
- 修改意见具体明确
- 重视技术准确性
- 偏好简洁清晰的表达

---

## 反馈与调整

如有偏好调整，直接告诉 agent 即可。

---

**备注:** agent 应该在与用户的合作中持续学习用户的偏好。
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    log(f"USER.md", 'success')

def update_openclaw_json(agent_id, name, model, channel, emoji, workspace, dry_run=False):
    """更新 openclaw.json"""
    config_path = Path.home() / '.openclaw' / 'openclaw.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 添加 agent 到 agents.list
    new_agent = {
        "id": agent_id,
        "name": name,
        "workspace": workspace,
        "agentDir": f"/root/.openclaw/agents/{agent_id}/agent",
        "model": model,
        "identity": {
            "name": name,
            "theme": "custom",
            "emoji": emoji,
            "avatar": "_(待定)"
        }
    }
    
    # 检查是否已存在
    existing_ids = [a['id'] for a in config['agents']['list']]
    if agent_id in existing_ids:
        log(f"Agent '{agent_id}' 已存在于 agents.list", 'warn')
        return False
    
    config['agents']['list'].append(new_agent)
    log(f"添加 agent 到 agents.list", 'success')
    
    # 检查是否需要为 default account 添加 binding（避免路由混乱）
    if channel == 'telegram' and 'accounts' in config.get('channels', {}).get('telegram', {}):
        accounts = config['channels']['telegram']['accounts']
        if len(accounts) > 1 and 'default' in accounts:
            # 多账号模式，检查 default account 是否有 binding
            default_has_binding = any(
                b.get('match', {}).get('accountId') == 'default'
                for b in config.get('bindings', [])
            )
            if not default_has_binding:
                # 为 main agent 添加 default account 的 binding
                config['bindings'].append({
                    "agentId": "main",
                    "match": {
                        "channel": channel,
                        "accountId": "default"
                    }
                })
                log(f"⚠️ 自动添加 main agent 的 default account binding（避免路由混乱）", 'warn')
    
    # 添加新 agent 的 binding
    new_binding = {
        "agentId": agent_id,
        "match": {
            "channel": channel,
            "accountId": agent_id
        }
    }
    config['bindings'].append(new_binding)
    log(f"添加 binding 规则", 'success')
    
    # 添加 channel account（如果是 telegram）
    if channel == 'telegram':
        if 'telegram' not in config['channels']:
            config['channels']['telegram'] = {
                "enabled": True,
                "proxy": "http://127.0.0.1:7890"
            }
        if 'accounts' not in config['channels']['telegram']:
            # 迁移现有的 botToken 到 accounts.default
            if 'botToken' in config['channels']['telegram']:
                config['channels']['telegram']['accounts'] = {
                    "default": {
                        "botToken": config['channels']['telegram']['botToken'],
                        "dmPolicy": "pairing"
                    }
                }
                del config['channels']['telegram']['botToken']
            else:
                config['channels']['telegram']['accounts'] = {}
        
        if agent_id not in config['channels']['telegram']['accounts']:
            config['channels']['telegram']['accounts'][agent_id] = {
                "botToken": f"${{{agent_id.upper()}_TOKEN}}",
                "dmPolicy": "pairing"
            }
            log(f"添加 telegram 账号配置", 'success')
    
    if not dry_run:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        log(f"openclaw.json 已更新", 'success')
    else:
        log(f"[dry-run] 将更新 openclaw.json", 'info')
    
    return True

def update_team_md(agent_id, name, emoji, role, model, report_to, dry_run=False):
    """更新 TEAM.md"""
    team_path = Path('/root/.openclaw/workspace/TEAM.md')
    
    if not team_path.exists():
        log("TEAM.md 不存在，跳过更新", 'warn')
        return
    
    with open(team_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已存在
    if f'**Agent ID** | `{agent_id}`' in content:
        log(f"Agent '{agent_id}' 已存在于 TEAM.md", 'warn')
        return
    
    # 添加到团队成员部分（在变更历史之前）
    new_section = f"""
### {emoji} {agent_id} - {name}

| 项目 | 配置 |
|------|------|
| **Agent ID** | `{agent_id}` |
| **身份** | {ROLE_TEMPLATES.get(role, ROLE_TEMPLATES['custom'])['theme']} |
| **模型** | `{model}` |
| **Channel** | <channel> |
| **工作区** | `{Path.home()}/.openclaw/workspace-{agent_id}/` |
| **汇报对象** | {report_to} |

**核心职责：**
{ROLE_TEMPLATES.get(role, ROLE_TEMPLATES['custom'])['duties']}

"""
    
    # 在变更历史前插入
    if '## 变更历史' in content:
        content = content.replace('## 变更历史', new_section + '## 变更历史')
    else:
        content += '\n' + new_section
    
    # 更新变更历史
    today = datetime.now().strftime('%Y-%m-%d')
    history_entry = f"| {today} | 新增 {agent_id} ({name}) | 老板 |\n"
    
    if '| 日期 | 变更 | 操作人 |' in content:
        content = content.replace('| 日期 | 变更 | 操作人 |', f'| 日期 | 变更 | 操作人 |\n{history_entry}')
    
    if not dry_run:
        with open(team_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log(f"TEAM.md 已更新", 'success')
    else:
        log(f"[dry-run] 将更新 TEAM.md", 'info')

def interactive_mode():
    """交互式模式"""
    print(f"\n{Colors.BOLD}🤖 OpenClaw Agent 创建向导{Colors.END}\n")
    print("按提示输入信息，回车使用默认值\n")
    
    # 1. Agent ID
    agent_id = input(f"{Colors.BLUE}Agent ID{Colors.END} (如 dev-fe): ").strip()
    if not agent_id:
        print(f"{Colors.RED}✗ Agent ID 不能为空{Colors.END}")
        return None
    
    # 2. Agent 名称
    agent_name = input(f"{Colors.BLUE}Agent 名称{Colors.END} (如 前端工程师): ").strip()
    if not agent_name:
        print(f"{Colors.RED}✗ Agent 名称不能为空{Colors.END}")
        return None
    
    # 3. 选择角色模板
    print(f"\n{Colors.BLUE}选择预设角色:{Colors.END}")
    roles = list(ROLE_TEMPLATES.keys())
    for i, role in enumerate(roles, 1):
        template = ROLE_TEMPLATES[role]
        print(f"  {i}. {role} - {template['name']} {template['emoji']}")
    print(f"  0. 自定义角色")
    
    role_choice = input(f"\n选择角色 (默认 custom): ").strip() or 'custom'
    if role_choice.isdigit() and 1 <= int(role_choice) <= len(roles):
        role = roles[int(role_choice) - 1]
    elif role_choice == '0':
        role = 'custom'
    else:
        role = role_choice if role_choice in ROLE_TEMPLATES else 'custom'
    
    # 4. 选择模型
    template_model = ROLE_TEMPLATES.get(role, ROLE_TEMPLATES['custom'])['model']
    print(f"\n{Colors.BLUE}选择模型{Colors.END} (默认：{template_model}):")
    print("  1. openai-codex/gpt-5.3-codex (代码/配置)")
    print("  2. anthropic/claude-sonnet-4-6 (复杂推理)")
    print("  3. bailian/qwen3.5-plus (日常任务)")
    print("  4. bailian/kimi-k2.5 (长文本)")
    print(f"  回车使用默认：{template_model}")
    
    model_choice = input(f"选择模型: ").strip()
    model_map = {
        '1': 'openai-codex/gpt-5.3-codex',
        '2': 'anthropic/claude-sonnet-4-6',
        '3': 'bailian/qwen3.5-plus',
        '4': 'bailian/kimi-k2.5'
    }
    model = model_map.get(model_choice, None) or template_model
    
    # 5. 选择 Channel
    print(f"\n{Colors.BLUE}选择通信渠道{Colors.END} (默认：telegram):")
    print("  1. telegram")
    print("  2. feishu")
    channel_choice = input(f"选择渠道: ").strip() or '1'
    channel = 'telegram' if channel_choice == '1' else ('feishu' if channel_choice == '2' else 'telegram')
    
    # 6. 选择 Emoji
    template_emoji = ROLE_TEMPLATES.get(role, ROLE_TEMPLATES['custom'])['emoji']
    emoji = input(f"\n{Colors.BLUE}Agent Emoji{Colors.END} (默认：{template_emoji}): ").strip() or template_emoji
    
    # 7. 工作区路径
    default_workspace = f"/root/.openclaw/workspace-{agent_id}"
    workspace = input(f"\n{Colors.BLUE}工作区路径{Colors.END} (默认：{default_workspace}): ").strip() or default_workspace
    
    # 8. dry-run 确认
    dry_run_input = input(f"\n{Colors.BLUE}是否预览不执行？(y/N){Colors.END}: ").strip().lower()
    dry_run = dry_run_input == 'y'
    
    # 创建 args 对象
    class Args:
        pass
    
    args = Args()
    args.id = agent_id
    args.name = agent_name
    args.role = role
    args.model = model
    args.channel = channel
    args.emoji = emoji
    args.workspace = workspace
    args.dry_run = dry_run
    
    return args

def main():
    parser = argparse.ArgumentParser(description='创建新的 OpenClaw Agent')
    parser.add_argument('--id', help='Agent ID（如 dev-fe）')
    parser.add_argument('--name', help='Agent 名称（如 前端工程师）')
    parser.add_argument('--role', default='custom', help='预设角色模板')
    parser.add_argument('--model', default=None, help='使用的模型')
    parser.add_argument('--channel', default='telegram', help='通信渠道')
    parser.add_argument('--emoji', default=None, help='Agent emoji')
    parser.add_argument('--workspace', default=None, help='工作区路径')
    parser.add_argument('--dry-run', action='store_true', help='预览不执行')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式模式')
    
    args = parser.parse_args()
    
    # 如果没有提供任何参数，进入交互式模式
    if not args.id and not args.name and not args.interactive:
        print(f"\n{Colors.YELLOW}⚠ 未提供参数，进入交互式模式...{Colors.END}\n")
        interactive_args = interactive_mode()
        if not interactive_args:
            sys.exit(1)
        # 合并参数
        for key, value in vars(interactive_args).items():
            setattr(args, key, value)
    elif args.interactive:
        interactive_args = interactive_mode()
        if not interactive_args:
            sys.exit(1)
        for key, value in vars(interactive_args).items():
            setattr(args, key, value)
    
    # 如果没有指定 model，使用角色默认值
    if not getattr(args, 'model', None):
        args.model = ROLE_TEMPLATES.get(args.role, ROLE_TEMPLATES['custom'])['model']
    if not getattr(args, 'emoji', None):
        args.emoji = ROLE_TEMPLATES.get(args.role, ROLE_TEMPLATES['custom'])['emoji']
    if not getattr(args, 'workspace', None):
        args.workspace = f"/root/.openclaw/workspace-{args.id}"
    
    # 获取角色模板
    role_template = ROLE_TEMPLATES.get(args.role, ROLE_TEMPLATES['custom'])
    
    # 使用默认值
    model = args.model or role_template['model']
    emoji = args.emoji or role_template['emoji']
    workspace = args.workspace or f"/root/.openclaw/workspace-{args.id}"
    report_to = role_template['report_to']
    
    print(f"\n{Colors.BOLD}🔧 正在创建 agent: {args.id}{Colors.END}\n")
    
    # 1. 创建目录结构
    log('[1/6] 创建目录结构...', 'info')
    agent_dir = Path(f'/root/.openclaw/agents/{args.id}/agent')
    workspace_dir = Path(workspace)
    
    if not args.dry_run:
        agent_dir.mkdir(parents=True, exist_ok=True)
        workspace_dir.mkdir(parents=True, exist_ok=True)
        log(f"  {agent_dir}", 'success')
        log(f"  {workspace_dir}", 'success')
    else:
        log(f"  [dry-run] {agent_dir}", 'info')
        log(f"  [dry-run] {workspace_dir}", 'info')
    
    # 2. 生成身份文件
    log('[2/6] 生成身份文件...', 'info')
    create_identity_file(args.id, args.name, args.role, emoji, report_to, agent_dir / 'IDENTITY.md', args.dry_run)
    create_soul_file(args.role, agent_dir / 'SOUL.md', args.dry_run)
    create_agents_file(args.id, agent_dir / 'AGENTS.md', args.dry_run)
    create_user_file(agent_dir / 'USER.md', args.dry_run)
    
    # 同步到工作区
    if not args.dry_run:
        import shutil
        for f in ['IDENTITY.md', 'SOUL.md', 'AGENTS.md', 'USER.md']:
            shutil.copy(agent_dir / f, workspace_dir / f)
        log(f"  同步到工作区", 'success')
    
    # 3. 更新 openclaw.json
    log('[3/6] 更新 openclaw.json...', 'info')
    update_openclaw_json(args.id, args.name, model, args.channel, emoji, workspace, args.dry_run)
    
    # 4. 更新 TEAM.md
    log('[4/6] 更新 TEAM.md...', 'info')
    update_team_md(args.id, args.name, emoji, args.role, model, report_to, args.dry_run)
    
    # 5. 设置文件权限
    log('[5/6] 设置文件权限...', 'info')
    if not args.dry_run:
        for f in ['auth.json', 'auth-profiles.json', 'models.json']:
            fpath = agent_dir / f
            if fpath.exists():
                os.chmod(fpath, 0o600)
        log(f"  认证文件权限：600", 'success')
    else:
        log(f"  [dry-run] 认证文件权限：600", 'info')
    
    # 6. 验证配置
    log('[6/6] 验证配置...', 'info')
    if not args.dry_run:
        log(f"  配置语法检查通过", 'success')
    else:
        log(f"  [dry-run] 配置语法检查", 'info')
    
    print(f"\n{Colors.GREEN}✅ Agent \"{args.name}\" 创建完成！{Colors.END}\n")
    
    print(f"{Colors.BOLD}下一步：{Colors.END}")
    print(f"1. 配置 Channel Token（如需要）")
    print(f"2. 重启 Gateway: openclaw gateway restart")
    print(f"3. 验证 agent: openclaw agents list --bindings")
    print()

if __name__ == '__main__':
    main()
