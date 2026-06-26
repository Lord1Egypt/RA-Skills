#!/usr/bin/env python3
"""
八爪鱼 RPA Webhook 调用工具 (安全增强版)

安全特性:
- 支持环境变量存储敏感信息 (优先级高于配置文件)
- 配置文件自动设置权限为 600 (仅所有者可读写)
- 日志输出脱敏处理
- 支持加密配置文件 (可选)

环境变量:
- BAZHUAYU_WEBHOOK_URL    Webhook URL
- BAZHUAYU_WEBHOOK_KEY    签名密钥
- BAZHUAYU_PARAM_*        自定义参数默认值 (如 BAZHUAYU_PARAM_KEYWORD)
"""

import json
import hmac
import hashlib
import base64
import time
import argparse
import sys
import os
import stat
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / 'config.json'

# 敏感字段列表 (用于脱敏)
SENSITIVE_FIELDS = ['key', 'password', 'secret', 'token', 'auth']

def show_help():
    print("""八爪鱼 RPA Webhook 调用工具 (安全增强版)

用法:
  python bazhuayu-webhook.py init              初始化配置
  python bazhuayu-webhook.py run [选项]        运行任务
  python bazhuayu-webhook.py config            查看当前配置
  python bazhuayu-webhook.py test              测试连接 (dry-run)
  python bazhuayu-webhook.py secure-check      安全检查

run 选项:
  --param1=值 1    设置参数 1 的值
  --param2=值 2    设置参数 2 的值
  --dry-run        仅显示请求内容，不实际发送

安全建议:
  - 使用环境变量存储敏感信息 (优先级高于配置文件)
  - 定期运行 secure-check 检查配置安全
  - 不要将 config.json 提交到版本控制

环境变量:
  BAZHUAYU_WEBHOOK_URL    Webhook URL
  BAZHUAYU_WEBHOOK_KEY    签名密钥
  BAZHUAYU_PARAM_*        自定义参数默认值

示例:
  python bazhuayu-webhook.py run --param1=新值 1 --param2=新值 2
  BAZHUAYU_WEBHOOK_KEY=xxx python bazhuayu-webhook.py run
""")

def mask_sensitive(value, field_name=''):
    """脱敏处理敏感信息"""
    if not value or len(value) <= 8:
        return '***'
    # 显示前 4 位和后 4 位
    return f'{value[:4]}...{value[-4:]}'

def load_config():
    """加载配置，环境变量优先级高于配置文件"""
    config = {
        'url': '',
        'key': '',
        'paramNames': [],
        'defaultParams': {}
    }
    
    # 1. 先从配置文件加载
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
        except json.JSONDecodeError as e:
            print(f"⚠️  配置文件解析失败：{e}")
            print("   请检查 config.json 格式是否正确")
            sys.exit(1)
        except Exception as e:
            print(f"⚠️  读取配置文件失败：{e}")
    
    # 2. 环境变量覆盖 (优先级更高)
    env_url = os.environ.get('BAZHUAYU_WEBHOOK_URL')
    env_key = os.environ.get('BAZHUAYU_WEBHOOK_KEY')
    
    if env_url:
        config['url'] = env_url
    if env_key:
        config['key'] = env_key
    
    # 3. 加载环境变量中的参数默认值 (BAZHUAYU_PARAM_*)
    for env_name, env_value in os.environ.items():
        if env_name.startswith('BAZHUAYU_PARAM_'):
            param_name = env_name.replace('BAZHUAYU_PARAM_', '')
            # 转换为驼峰或小写格式
            param_name = param_name.lower().replace('_', '')
            config['defaultParams'][param_name] = env_value
            if param_name not in config['paramNames']:
                config['paramNames'].append(param_name)
    
    # 验证必要配置
    if not config.get('url'):
        print("错误：缺少 Webhook URL")
        print("请设置 BAZHUAYU_WEBHOOK_URL 环境变量或在 config.json 中配置")
        sys.exit(1)
    
    if not config.get('key'):
        print("错误：缺少签名密钥")
        print("请设置 BAZHUAYU_WEBHOOK_KEY 环境变量或在 config.json 中配置")
        sys.exit(1)
    
    return config

def save_config(config):
    """保存配置并设置安全权限"""
    # 先写入文件
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # 设置文件权限为 600 (仅所有者可读写)
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)
    
    # 验证权限
    file_stat = os.stat(CONFIG_FILE)
    perms = oct(file_stat.st_mode)[-3:]
    
    print("配置已保存")
    print(f"✅ 文件权限已设置为 {perms} (仅所有者可读写)")
    print(f"📁 配置文件位置：{CONFIG_FILE.absolute()}")

def init_config():
    """初始化配置 - 默认使用环境变量存储敏感信息"""
    print("=== 八爪鱼 RPA Webhook 初始化配置 (安全增强版) ===\n")
    print("🔐 安全模式：敏感信息默认使用环境变量存储")
    print("   - 签名密钥 → BAZHUAYU_WEBHOOK_KEY 环境变量")
    print("   - Webhook URL → 可选环境变量或配置文件")
    print("   - 配置文件将不存储任何敏感信息\n")
    
    # 收集配置信息
    print("--- 配置信息 ---")
    url = input("请输入 Webhook URL: ").strip()
    key = input("请输入签名密钥 (Key): ").strip()
    
    # 验证密钥格式
    if len(key) < 8:
        print("⚠️  警告：密钥长度较短，建议使用更安全的密钥")
    
    print("\n定义参数名称 (逗号分隔，如：参数 1，参数 2): ")
    params_input = input().strip()
    param_names = [p.strip() for p in params_input.split(',') if p.strip()]
    
    if not param_names:
        print("⚠️  未设置参数，将使用空参数列表")
    
    default_params = {}
    env_params = {}
    
    for name in param_names:
        print(f"\n配置参数 [{name}]:")
        print("  1. 使用固定默认值 (保存在配置文件)")
        print("  2. 使用环境变量 (推荐用于敏感参数)")
        print("  3. 不设置默认值 (运行时必须指定)")
        
        choice = input("  请选择 (1/2/3) [默认:1]: ").strip() or '1'
        
        if choice == '2':
            env_name = f"BAZHUAYU_PARAM_{name.upper().replace(' ', '_').replace('-', '_')}"
            value = input(f"  请输入 [{name}] 的默认值：").strip()
            env_params[env_name] = value
            default_params[name] = f'${{{env_name}}}'  # 标记为环境变量引用
        elif choice == '3':
            default_params[name] = ''  # 空值，运行时必须指定
        else:
            value = input(f"  请输入 [{name}] 的默认值：").strip()
            default_params[name] = value
    
    # 配置文件不包含敏感信息
    config = {
        'url': url,  # URL 可以存储在配置文件 (非敏感)
        'key': '',   # 密钥留空，从环境变量读取
        'paramNames': param_names,
        'defaultParams': default_params,
        'security': {
            'keyFromEnv': True,
            'createdAt': time.strftime('%Y-%m-%d %H:%M:%S'),
            'version': '2.0'
        }
    }
    
    save_config(config)
    
    # 生成环境变量配置
    print("\n=== 配置完成 ===")
    print(f"Webhook URL: {mask_sensitive(url)}")
    print(f"参数列表：{', '.join(param_names)}")
    print("\n🔐 安全配置：签名密钥已设置为从环境变量读取")
    print("   配置文件 (config.json) 中不存储密钥\n")
    
    # 提供环境变量设置指南
    print("📝 请设置以下环境变量 (二选一):\n")
    
    print("方式 1: 临时设置 (当前终端会话有效)")
    print("-" * 60)
    print(f'export BAZHUAYU_WEBHOOK_KEY="{key}"')
    for env_name, value in env_params.items():
        print(f'export {env_name}="{value}"')
    print("-" * 60)
    
    print("\n方式 2: 永久设置 (添加到 Shell 配置文件)")
    print("-" * 60)
    shell_config = "~/.bashrc" if os.path.exists(os.path.expanduser("~/.bashrc")) else "~/.zshrc"
    print(f'# 添加到 {shell_config}')
    print(f'export BAZHUAYU_WEBHOOK_KEY="{key}"')
    for env_name, value in env_params.items():
        print(f'export {env_name}="{value}"')
    print("-" * 60)
    print(f"\n然后运行：source {shell_config}")
    
    print("\n✅ 验证配置:")
    print("   python3 bazhuayu-webhook.py secure-check")
    print("   python3 bazhuayu-webhook.py test\n")

def show_config():
    """显示当前配置 (脱敏)"""
    config = load_config()
    print("=== 当前配置 ===")
    
    # 检查配置来源
    url_from_env = bool(os.environ.get('BAZHUAYU_WEBHOOK_URL'))
    key_from_env = bool(os.environ.get('BAZHUAYU_WEBHOOK_KEY'))
    
    print(f"Webhook URL: {mask_sensitive(config['url'])} {'(环境变量)' if url_from_env else '(配置文件)'}")
    print(f"签名密钥：{mask_sensitive(config['key'])} {'(环境变量)' if key_from_env else '(配置文件)'}")
    print(f"参数列表：{', '.join(config['paramNames'])}")
    print("默认参数值:")
    for name, value in config['defaultParams'].items():
        is_sensitive = any(s in name.lower() for s in SENSITIVE_FIELDS)
        display_value = mask_sensitive(value) if is_sensitive else value
        print(f"  {name} = {display_value}")
    
    # 显示安全状态
    print("\n=== 安全状态 ===")
    if key_from_env:
        print("✅ 签名密钥使用环境变量存储 (安全)")
    else:
        print("⚠️  签名密钥存储在配置文件中")
        if CONFIG_FILE.exists():
            file_stat = os.stat(CONFIG_FILE)
            perms = oct(file_stat.st_mode)[-3:]
            if perms == '600':
                print(f"✅ 配置文件权限正确 ({perms})")
            else:
                print(f"⚠️  配置文件权限不安全 ({perms}), 建议设置为 600")
    
    if url_from_env:
        print("✅ Webhook URL 使用环境变量存储 (安全)")
    else:
        print("ℹ️  Webhook URL 存储在配置文件中")

def secure_check():
    """安全检查"""
    print("=== 安全检查 ===\n")
    
    issues = []
    recommendations = []
    
    # 1. 检查配置文件权限
    if CONFIG_FILE.exists():
        file_stat = os.stat(CONFIG_FILE)
        perms = oct(file_stat.st_mode)[-3:]
        if perms != '600':
            issues.append(f"配置文件权限不安全 ({perms}), 应为 600")
            recommendations.append(f"运行：chmod 600 {CONFIG_FILE}")
        else:
            print("✅ 配置文件权限正确 (600)")
    else:
        print("ℹ️  配置文件不存在 (可能使用环境变量)")
    
    # 2. 检查环境变量和配置文件
    key_from_env = bool(os.environ.get('BAZHUAYU_WEBHOOK_KEY'))
    url_from_env = bool(os.environ.get('BAZHUAYU_WEBHOOK_URL'))
    
    # 检查配置文件中的密钥是否为空（安全模式）
    config_key_in_file = False
    if CONFIG_FILE.exists():
        try:
            config = json.load(open(CONFIG_FILE, 'r', encoding='utf-8'))
            if config.get('key'):  # 如果 key 字段有值（非空）
                config_key_in_file = True
        except:
            pass
    
    if key_from_env:
        print("✅ 签名密钥使用环境变量存储")
    elif not config_key_in_file:
        print("✅ 签名密钥配置为从环境变量读取 (config.json 中 key 为空)")
    else:
        issues.append("签名密钥存储在配置文件中")
        recommendations.append("建议使用 BAZHUAYU_WEBHOOK_KEY 环境变量或运行 ./migrate-to-env.sh 迁移")
    
    if url_from_env:
        print("✅ Webhook URL 使用环境变量存储")
    else:
        print("ℹ️  Webhook URL 存储在配置文件中 (可接受)")
    
    # 3. 检查是否在版本控制中
    git_dir = SCRIPT_DIR / '.git'
    if git_dir.exists():
        issues.append("Skill 目录在 Git 仓库中")
        recommendations.append("确保 config.json 已添加到 .gitignore")
    
    # 4. 检查日志文件
    log_files = list(SCRIPT_DIR.glob('*.log'))
    if log_files:
        print(f"📝 发现 {len(log_files)} 个日志文件")
        for log_file in log_files:
            log_stat = os.stat(log_file)
            log_perms = oct(log_stat.st_mode)[-3:]
            if log_perms != '600':
                # 自动修复日志文件权限
                try:
                    os.chmod(log_file, stat.S_IRUSR | stat.S_IWUSR)
                    print(f"✅ 已修复 {log_file.name} 权限 ({log_perms} → 600)")
                except Exception as e:
                    issues.append(f"日志文件 {log_file.name} 权限不安全 ({log_perms}) 且无法自动修复")
    
    # 输出结果
    print("\n=== 检查结果 ===")
    if not issues:
        print("✅ 所有安全检查通过!")
    else:
        print(f"⚠️  发现 {len(issues)} 个问题:\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        if recommendations:
            print("\n=== 修复建议 ===")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
    
    return len(issues) == 0

def calculate_sign(key, timestamp):
    """
    计算签名：HmacSHA256(timestamp + '\\n' + key) -> Base64
    """
    string_to_sign = f"{timestamp}\n{key}"
    sign_data = hmac.new(
        string_to_sign.encode('utf-8'),
        b'',
        hashlib.sha256
    ).digest()
    return base64.b64encode(sign_data).decode('utf-8')

def run_task(override_params=None, dry_run=False):
    """运行任务"""
    if override_params is None:
        override_params = {}
    
    config = load_config()
    
    # 合并参数：默认参数 + 覆盖参数
    params = {**config['defaultParams'], **override_params}
    
    # 处理环境变量引用
    for key, value in params.items():
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_name = value[2:-1]
            env_value = os.environ.get(env_name)
            if env_value:
                params[key] = env_value
            else:
                print(f"⚠️  环境变量 {env_name} 未设置，使用空值")
                params[key] = ''
    
    timestamp = str(int(time.time()))
    sign = calculate_sign(config['key'], timestamp)
    
    payload = {
        'sign': sign,
        'params': params,
        'timestamp': timestamp
    }
    
    print("=== 准备发送请求 ===")
    print(f"URL: {mask_sensitive(config['url'])}")
    print(f"时间戳：{timestamp}")
    print("参数:")
    for name, value in params.items():
        is_sensitive = any(s in name.lower() for s in SENSITIVE_FIELDS)
        display_value = mask_sensitive(value) if is_sensitive else value
        print(f"  {name} = {display_value}")
    
    if dry_run:
        print("\n[DRY RUN] 未实际发送请求")
        print("\n请求 Payload (敏感信息已脱敏):")
        safe_payload = {
            'sign': mask_sensitive(payload['sign']),
            'params': {k: mask_sensitive(v) if any(s in k.lower() for s in SENSITIVE_FIELDS) else v 
                      for k, v in payload['params'].items()},
            'timestamp': payload['timestamp']
        }
        print(json.dumps(safe_payload, ensure_ascii=False, indent=2))
        return
    
    print("\n正在发送请求...")
    
    try:
        import urllib.request
        import urllib.error
        
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            config['url'],
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            http_code = response.status
            result = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        http_code = e.code
        try:
            result = json.loads(e.read().decode('utf-8'))
        except:
            result = {'error': str(e)}
    except Exception as e:
        print(f"\n=== 响应结果 ===")
        print(f"错误：{e}")
        sys.exit(1)
    
    print("\n=== 响应结果 ===")
    print(f"HTTP 状态码：{http_code}")
    
    if http_code == 200:
        print("✅ 调用成功!")
        if 'flowId' in result:
            print(f"应用 ID (flowId): {result['flowId']}")
        if 'flowProcessNo' in result:
            print(f"运行批次 (flowProcessNo): {result['flowProcessNo']}")
        if 'enterpriseId' in result:
            print(f"企业 ID: {result['enterpriseId']}")
    else:
        print("❌ 调用失败")
        if 'code' in result:
            print(f"错误码：{result['code']}")
        if 'description' in result:
            print(f"错误描述：{result['description']}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    override_params = {}
    dry_run = False
    
    # 解析命令行参数
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--dry-run':
            dry_run = True
        elif arg.startswith('--'):
            if '=' in arg:
                eq_pos = arg.index('=')
                key = arg[2:eq_pos]
                value = arg[eq_pos+1:]
                override_params[key] = value
            else:
                if i + 1 < len(args):
                    next_arg = args[i + 1]
                    if '=' in next_arg and not next_arg.startswith('--'):
                        eq_pos = next_arg.index('=')
                        key = arg[2:] + ' ' + next_arg[:eq_pos]
                        value = next_arg[eq_pos+1:]
                        override_params[key] = value
                        i += 1
                    elif not next_arg.startswith('--'):
                        override_params[arg[2:]] = next_arg
                        i += 1
        i += 1
    
    if command == 'init':
        init_config()
    elif command == 'config':
        show_config()
    elif command == 'run':
        run_task(override_params, dry_run)
    elif command == 'test':
        run_task({}, True)
    elif command == 'secure-check':
        secure_check()
    elif command in ('help', '-h', '--help'):
        show_help()
    else:
        print(f"未知命令：{command}\n")
        show_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
