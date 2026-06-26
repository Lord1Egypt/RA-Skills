import os
import subprocess
import sys
import shutil

# 颜色常量
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg):
    print(f"\n{Colors.YELLOW}{Colors.BOLD}[*] {msg}{Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.GREEN}✔ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.RED}✘ {msg}{Colors.ENDC}")

# 1. 环境诊断 (Environment Diagnosis)
def check_network(host="github.com"):
    print(f"  - 网络连通性 ({host}): ", end="", flush=True)
    try:
        # 使用 ping 测试 (Mac/Linux -c 1)
        subprocess.check_output(['ping', '-c', '1', '-W', '2', host], stderr=subprocess.STDOUT)
        print(f"{Colors.GREEN}畅通{Colors.ENDC}")
        return True
    except:
        print(f"{Colors.RED}受限 (可能需要代理){Colors.ENDC}")
        return False

def check_permissions():
    print(f"  - 目录写入权限: ", end="", flush=True)
    if os.access(os.getcwd(), os.W_OK):
        print(f"{Colors.GREEN}通过{Colors.ENDC}")
    else:
        print(f"{Colors.RED}拒绝 (请检查文件夹权限){Colors.ENDC}")

def check_env_file():
    print(f"  - .env 配置文件: ", end="", flush=True)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        print(f"{Colors.GREEN}已发现{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}未配置 (需根据 .env.example 创建){Colors.ENDC}")

def check_openclaw_version():
    print(f"  - OpenClaw 版本: ", end="", flush=True)
    try:
        # 尝试通过 CLI 获取版本
        result = subprocess.run(['openclaw', '--version'], capture_output=True, text=True)
        version = result.stdout.strip().split('\n')[-1] # 取最后一行
        if version:
            print(f"{Colors.GREEN}{version}{Colors.ENDC}")
        else:
            print(f"{Colors.RED}无法获取{Colors.ENDC}")
    except:
        print(f"{Colors.RED}未安装或不在 PATH 中{Colors.ENDC}")

def check_clawhub():
    global IS_CLAWHUB_LOGGED_IN
    print(f"  - ClawHub CLI: ", end="", flush=True)
    IS_CLAWHUB_LOGGED_IN = False
    try:
        # 探测版本
        result = subprocess.run(['npx', 'clawhub', '--cli-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip().split()[-1]
            # 增加登录状态检测
            login_check = subprocess.run(['npx', 'clawhub', 'whoami'], capture_output=True, text=True)
            if login_check.returncode == 0:
                print(f"{Colors.GREEN}已登录 ({version}){Colors.ENDC}")
                IS_CLAWHUB_LOGGED_IN = True
            else:
                print(f"{Colors.YELLOW}就绪但未登录 ({version}){Colors.ENDC}")
            return True
        else:
            print(f"{Colors.YELLOW}待部署{Colors.ENDC}")
            return False
    except:
        print(f"{Colors.RED}未检测到 Node.js{Colors.ENDC}")
        return False

# 全局状态，记录是否已登录
IS_CLAWHUB_LOGGED_IN = False
# 国内加速镜像注册表 (示例)
CHINA_REGISTRY = "https://registry.npmmirror.com" 

def install_via_clawhub():
    print_step("通过 ClawHub 同步/更新技能...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    # 直接使用国内镜像加速
    os.environ["CLAWHUB_REGISTRY"] = CHINA_REGISTRY
    print(f"  {Colors.GREEN}已自动启用加速节点: {CHINA_REGISTRY}{Colors.ENDC}")
    
    for slug in CLAWHUB_SLUGS:
        target_path = os.path.join(base_dir, slug)
        # ... 保持后续逻辑一致 ...

def check_feishu_tools():
    print(f"  - 飞书官方工具栈: ", end="", flush=True)
    try:
        # 探测飞书官方工具包
        result = subprocess.run(['npx', '@larksuite/openclaw-lark-tools', '--help'], 
                             capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"{Colors.GREEN}发现并可用{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.YELLOW}待部署{Colors.ENDC}")
            return False
    except:
        print(f"{Colors.RED}无法调用 (需 Node.js){Colors.ENDC}")
        return False

def interactive_config():
    print_step("设置项目配置 (交互模式)")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(base_dir, ".env")
    env_example_path = os.path.join(base_dir, ".env.example")
    
    if os.path.exists(env_path):
        choice = input(f"  {Colors.YELLOW}[!] .env 文件已存在，是否重新配置？(y/N): {Colors.ENDC}").strip().lower()
        if choice != 'y':
            print(f"  {Colors.GREEN}跳过配置，保留现有文件。{Colors.ENDC}")
            return

    # 从 .env.example 读取 key
    config_data = {}
    if os.path.exists(env_example_path):
        with open(env_example_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key = line.split('=')[0].strip()
                    config_data[key] = ""
    else:
        # 兜底核心 Key
        config_data = {
            "FEISHU_APP_ID": "", "FEISHU_APP_SECRET": "",
            "OPENAI_API_KEY": "", "OPENAI_BASE_URL": "https://api.openai.com/v1"
        }

    print(f"\n{Colors.BLUE}>>> 请根据提示输入配置信息 (直接回车可跳过/保持默认):{Colors.ENDC}")
    final_config = []
    
    # 为了更好的体验，按分类提示
    categories = {
        "FEISHU": "飞书 (Feishu) 配置",
        "OPENAI": "AI (LLM) 配置",
        "MP_": "公众号推送配置"
    }

    current_cat = ""
    for key in config_data.keys():
        # 显示分类标题
        matched_cat = "其他"
        for prefix, title in categories.items():
            if key.startswith(prefix):
                matched_cat = title
                break
        
        if matched_cat != current_cat:
            print(f"\n  {Colors.BOLD}[ {matched_cat} ]{Colors.ENDC}")
            current_cat = matched_cat

        val = input(f"  > {key}: ").strip()
        final_config.append(f"{key}={val}\n")

    # 写入 .env
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(final_config)
    
    print(f"\n{Colors.GREEN}✔ .env 配置文件已生成！{Colors.ENDC}")

def check_skillhub():
    print(f"  - Tencent SkillHub: ", end="", flush=True)
    # 允许的路径
    common_paths = ['skillhub', os.path.expanduser('~/.local/bin/skillhub')]
    
    for path in common_paths:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"{Colors.GREEN}已就绪{Colors.ENDC}")
                return True
        except:
            continue
    
    print(f"{Colors.YELLOW}未发现{Colors.ENDC}")
    return False

def install_skillhub_cli():
    print_step("正在自动部署 Tencent SkillHub (国内加速源)...")
    try:
        # 使用用户提供的快速安装脚本
        install_cmd = "curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash -s -- --no-skills"
        result = subprocess.run(install_cmd, shell=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.GREEN}SkillHub CLI 部署成功{Colors.ENDC}")
            # 自动将本地路径加入当前进程环境，确保后续直接调用有效
            local_bin = os.path.expanduser('~/.local/bin')
            if local_bin not in os.environ["PATH"]:
                os.environ["PATH"] = f"{local_bin}:{os.environ['PATH']}"
            return True
        else:
            print(f"{Colors.RED}SkillHub 部署失败{Colors.ENDC}")
            return False
    except Exception as e:
        print(f"{Colors.RED}部署异常: {str(e)}{Colors.ENDC}")
        return False

def diagnose_env():
    print_step("正在开启多维度环境诊断...")
    
    # Python 检查
    py_version = sys.version.split()[0]
    print(f"  - Python 版本: {py_version} ... {Colors.GREEN}通过{Colors.ENDC}")
    
    # Git 检查
    try:
        git_version = subprocess.check_output(['git', '--version']).decode().strip()
        print(f"  - Git 版本: {git_version} ... {Colors.GREEN}通过{Colors.ENDC}")
    except:
        print_error("未检测到 Git，请先安装 Git。")
        sys.exit(1)
        
    # OpenClaw 版本检查
    check_openclaw_version()
    
    # 飞书工具检查
    check_feishu_tools()
    
    # ClawHub 检查
    check_clawhub()

    # SkillHub 检查
    check_skillhub()
    
    # 网络检查
    check_network()
    
    # 权限检查
    check_permissions()
    
# 2. 技能编排 (Skill Orchestration)
# 增加版本/分支管理，确保环境稳定性
SKILL_STORE = {
    "核心工具 (Core Tools) - [推荐必装]": {
        "Skill-Vetter": {"url": "https://github.com/kiwi-miwi/skill-vetter.git", "tag": "main"},
        "Exec-Tool": {"url": "https://github.com/openclaw/exec-tool.git", "tag": "main"},
        "ClawRouter": {"url": "https://github.com/openclaw/claw-router.git", "tag": "main"},
        "Channels-Setup": {"url": "https://github.com/openclaw/channels-setup.git", "tag": "main"}
    },
    "高级 Agent 扩展 (Advanced Agent Skills)": {
        "Self-Improving-Agent": {"url": "https://github.com/openclaw/self-improving-agent.git", "tag": "main"},
        "Find-Skills": {"url": "https://github.com/openclaw/find-skills.git", "tag": "main"},
        "Agent-Browser": {"url": "https://github.com/openclaw/agent-browser.git", "tag": "main"},
        "Github-Skill": {"url": "https://github.com/openclaw/github.git", "tag": "main"}
    },
    "实用工具 (Utilities)": {
        "Clawscan": {"url": "https://github.com/openclaw/clawscan.git", "tag": "main"},
        "IM-Master-Skills": {"url": "https://github.com/LeoYeAI/openclaw-master-skills.git", "tag": "main"},
        "Web-Search-Tavily": {"url": "https://github.com/tavily-ai/tavily-python.git", "tag": "master"}
    }
}

import urllib.request
import ssl

def setup_persona():
    print_step("配置内置 AI 人设 (Persona)")
    print(f"  {Colors.BLUE}正在从 agency-agents 仓库获取人设模板...{Colors.ENDC}")
    
    # 预设几个经典高分人设供用户选择
    personas = [
        {"name": "AI 工程师 (AI Engineer)", "path": "engineering/engineering-ai-engineer.md"},
        {"name": "资深前端开发 (Frontend Developer)", "path": "engineering/engineering-frontend-developer.md"},
        {"name": "软件架构师 (Software Architect)", "path": "engineering/engineering-software-architect.md"},
        {"name": "飞书集成开发专家 (Feishu Integration Developer)", "path": "engineering/engineering-feishu-integration-developer.md"},
        {"name": "代码审查专家 (Code Reviewer)", "path": "engineering/engineering-code-reviewer.md"},
        {"name": "跳过配置", "path": None}
    ]
    
    for i, p in enumerate(personas):
        print(f"  [{i+1}] {p['name']}")
        
    choice = input(f"\n{Colors.YELLOW}请选择一个内置人设作为当前 Agent 的默认属性 (1-{len(personas)}): {Colors.ENDC}").strip()
    
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(personas) or personas[idx]["path"] is None:
            print(f"  {Colors.GREEN}已跳过人设配置。{Colors.ENDC}")
            return
            
        selected = personas[idx]
        print(f"  正在下载人设: {selected['name']} ... ", end="", flush=True)
        
        # 从 github raw 下载
        raw_url = f"https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{selected['path']}"
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        persona_path = os.path.join(base_dir, "persona.md")
        
        # 忽略 SSL 警告
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            content = response.read().decode('utf-8')
            
        with open(persona_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"{Colors.GREEN}成功{Colors.ENDC}")
        print(f"  {Colors.YELLOW}人设已保存至: {persona_path}{Colors.ENDC}")
        print(f"  {Colors.BLUE}(你可以直接将该文件内容作为 System Prompt 注入 Agent){Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.RED}获取或保存人设失败: {e}{Colors.ENDC}")

# 核心技能标识 (Slugs)
CORE_SLUGS = [
    "skill-vetter", "exec-tool", "weather-skill", "claw-router", "channels-setup",
    "self-improving-agent", "find-skills", "agent-browser", "github"
]

def install_via_skillhub():
    print_step("通过 Tencent SkillHub 同步核心技能...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    # 路径搜寻逻辑
    skillhub_path = 'skillhub'
    potential_paths = ['skillhub', os.path.expanduser('~/.local/bin/skillhub')]
    
    def get_skillhub_cli():
        for p in potential_paths:
            try:
                if subprocess.run([p, '--version'], capture_output=True).returncode == 0:
                    return p
            except:
                continue
        return None

    skillhub_path = get_skillhub_cli()

    def print_skillhub_skip_msg():
        print(f"\n{Colors.YELLOW}⚠️ 可选模块执行失败（非核心，不影响使用）{Colors.ENDC}")
        print("因为没装skillhub工具，腾讯SkillHub同步模块自动跳过啦，飞书配置引导也自动跳过了，完全不影响现有功能哒😘\n")
        print(f"{Colors.GREEN}现在Auto-Config-Skiller的所有核心能力已全部就绪，可以直接使用环境诊断、自动配置、技能管理等功能~{Colors.ENDC}\n")

    if not skillhub_path:
        # 改为更加主动的安装策略
        print(f"  {Colors.YELLOW}[!] 未发现 SkillHub CLI，准备自动安装以开启加速模式...{Colors.ENDC}")
        if install_skillhub_cli():
            skillhub_path = get_skillhub_cli() or os.path.expanduser('~/.local/bin/skillhub')
        else:
            print_skillhub_skip_msg()
            return

    for slug in CORE_SLUGS:
        target_path = os.path.join(base_dir, slug)
        if os.path.exists(target_path):
            print(f"  [已存在] {slug} - 跳过同步")
            continue
            
        print(f"  [SkillHub] 正在安装 {slug} ... ", end="", flush=True)
        try:
            result = subprocess.run([skillhub_path, 'install', slug, '--dir', base_dir], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.GREEN}完成{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}跳过 (可能仓库未收录){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}异常: {str(e)}{Colors.ENDC}")

def configure_feishu_streaming():
    print_step("优化飞书流式卡片配置...")
    commands = [
        ['openclaw', 'config', 'set', 'channels.feishu.streaming', 'true'],
        ['openclaw', 'config', 'set', 'channels.feishu.footer.elapsed', 'true'],
        ['openclaw', 'config', 'set', 'channels.feishu.footer.status', 'true']
    ]
    for cmd in commands:
        print(f"  执行: {' '.join(cmd)} ... ", end="", flush=True)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.GREEN}成功{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}忽略 (可能环境未完全就绪){Colors.ENDC}")
        except:
            print(f"{Colors.RED}失败{Colors.ENDC}")

def install_feishu_plugin():
    print_step("初始化飞书官方通讯插件...")
    print(f"  [飞书] 正在调用官方安装程序 ... ", end="", flush=True)
    try:
        # 该命令会启动交互式安装 or 诊断修复
        print(f"\n{Colors.BLUE}>>> 提示: 接下来将启动官方飞书工具，如需跳过请 Ctrl+C{Colors.ENDC}")
        result = subprocess.run(['npx', '-y', '@larksuite/openclaw-lark-tools', 'install'], 
                             text=True)
        if result.returncode == 0:
            print(f"{Colors.GREEN}飞书插件部署完成{Colors.ENDC}")
            # 安装成功后自动执行流式配置
            configure_feishu_streaming()
        else:
            print(f"{Colors.RED}飞书插件安装退出{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}飞书安装异常: {str(e)}{Colors.ENDC}")

def install_via_clawhub():
    print_step("通过 ClawHub 尝试同步/更新 (可选)...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    # 自动启用国内镜像，避开登录逻辑干扰
    os.environ["CLAWHUB_REGISTRY"] = CHINA_REGISTRY
    
    for slug in CORE_SLUGS:
        target_path = os.path.join(base_dir, slug)
        
        if os.path.exists(target_path):
            continue
            
        print(f"  [ClawHub] 尝试后台拉取 {slug} ... ", end="", flush=True)
        try:
            # 增加参数尝试跳过登录交互
            result = subprocess.run(['npx', '-y', 'clawhub@latest', 'install', slug, '--no-input', '--dir', base_dir], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.GREEN}完成{Colors.ENDC}")
            else:
                # 即使失败也不再报错，提示已转入 Git 自动补齐
                print(f"{Colors.BLUE}已转入 Git 补全流程{Colors.ENDC}")
        except:
            print(f"{Colors.BLUE}跳过{Colors.ENDC}")

def install_skills():
    print_step("同步基础安装包 (Git Pull/Clone)...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    for category, skills in SKILL_STORE.items():
        print(f"\n{Colors.BLUE}{Colors.BOLD}--- {category} ---{Colors.ENDC}")
        for name, config in skills.items():
            target_path = os.path.join(base_dir, name)
            # 兼容性处理：如果文件夹名与 Slug 不同，但已由 Hub 安装，则跳过
            found_hub = False
            for s in CORE_SLUGS:
                if os.path.exists(os.path.join(base_dir, s)) and s.lower() in name.lower():
                    found_hub = True
                    break
            
            if found_hub:
                print(f"  [Hub已覆盖] {name}")
                continue

            url = config["url"]
            tag = config.get("tag", "main")
            
            if os.path.exists(target_path):
                print(f"  [已存在] {name} - 正在拉取更新 ... ", end="", flush=True)
                try:
                    result = subprocess.run(['git', '-C', target_path, 'pull', 'origin', tag], 
                                         capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"{Colors.GREEN}已更新{Colors.ENDC}")
                    else:
                        print(f"{Colors.YELLOW}更新失败 (跳过){Colors.ENDC}")
                except:
                    print(f"{Colors.YELLOW}异常{Colors.ENDC}")
            else:
                print(f"  [Git 克隆] {name} (适配分支: {tag}) ... ", end="", flush=True)
                try:
                    result = subprocess.run(['git', 'clone', '-b', tag, '--depth', '1', url, target_path], 
                                         capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"{Colors.GREEN}完成{Colors.ENDC}")
                    else:
                        print(f"{Colors.RED}失败{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.RED}异常: {str(e)}{Colors.ENDC}")

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}=======================================")
    print("   OpenClaw 自动配置助手 (傻瓜模式)")
    print(f"======================================={Colors.ENDC}")
    print(f"{Colors.BLUE}本工具将自动完成以下操作：")
    print("1. 诊断环境、配置飞书通道")
    print("2. 自动集成腾讯 SkillHub 加速源 (免登录同步核心技能)")
    print("3. 全量编排核心技能库并进行交互式配置")
    print(f"---------------------------------------{Colors.ENDC}")
    
    diagnose_env()
    
    # 飞书官方插件部署
    install_feishu_plugin()
    
    # --- 技能安装优先级流 ---
    # 优先使用国内加速源 SkillHub (解决付费/登录/网络限制)
    install_via_skillhub()
    
    # 尝试官方源补全 (ClawHub)
    install_via_clawhub()
    
    # 备选补全 Git 安装
    install_skills()
    
    # 交互式配置 (替代手动修改 .env.example)
    interactive_config()
    
    # 引导内置人设
    setup_persona()
    
    print_step("配置任务完成！")
    print("提示: 核心内容已就绪。请查看指南 ./docs/USAGE_GUIDE.md")
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 自动化流程执行完毕！{Colors.ENDC}")

if __name__ == "__main__":
    main()
